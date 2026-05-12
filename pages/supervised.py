import base64
import io

import dash
from dash import html, dcc, callback, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import joblib

from scripts.firebase_config import build_event_payload, log_to_firebase


dash.register_page(__name__, path="/supervised", name="Supervised Learning")

feature_cols = joblib.load("models/feature_cols.pkl")
model = joblib.load("models/customer_model.pkl")
le = joblib.load("models/label_encoder.pkl")
df_raw = pd.read_csv("data/cleaned_data.csv")

SEGMENT_ICON = {"ชอบกาแฟ": "☕", "ชอบชา": "🍵", "ชอบทั้งกาแฟและชา": "🍵☕"}
SEGMENT_COLOR = {"ชอบกาแฟ": "#6F4E37", "ชอบชา": "#8f8f8f", "ชอบทั้งกาแฟและชา": "#21cdb6"}
CAMPAIGN_REC = {
    "ชอบกาแฟ": "📱 Facebook/Instagram | 🎯 'กาแฟสดในขวด รสชาติเหมือนร้าน พกพาได้ทุกที่'",
    "ชอบชา": "📱 Facebook | 🎯 'ชาพรีเมียม ไม่มีน้ำตาล — Healthy Choice ของคนรักชา'",
    "ชอบทั้งกาแฟและชา": "📱 LINE | 🎯 'ครบทุกอารมณ์ ทั้งกาแฟและชา เลือกได้ตามวัน'",
}

COLUMN_ALIASES = {
    "Age": ["Age", "อายุ"],
    "S_Frequency": ["S_Frequency", "ความถี่ในการเปิดรับสื่อในแต่ละช่องทางต่อสัปดาห์ [ออนไลน์]"],
    "S_Screentime": ["S_Screentime", "ระยะเวลาในการเสพสื่อต่อวัน ในแต่ละช่องทาง [ออนไลน์]"],
    "S_Occasion": ["S_Occasion", "คุณใช้โซเชียลมีเดียใดบ่อยที่สุด"],
    "C_Frequency": ["C_Frequency", "คุณดื่มกาแฟประเภทใดบ่อยที่สุด"],
    "C_Favorite": ["C_Favorite", "คุณชอบกาแฟประเภทใดมากที่สุด"],
    "C_Occasion": ["C_Occasion", "คุณดื่มกาแฟพร้อมดื่ม (Ready to drink) ในโอกาส/โมเมนต์ใดบ้าง (เลือกได้หลายคำตอบ)"],
    "T_Frequency": ["T_Frequency", "คุณดื่มชาประเภทใดบ่อยที่สุด"],
    "T_Favorite": ["T_Favorite", "คุณชอบดื่มชาประเภทใดมากที่สุด"],
    "T_Occasion": ["T_Occasion", "คุณดื่มชาพร้อมดื่ม ในโอกาส/โมเมนต์ใดบ้าง (เลือกได้หลายคำตอบ)"],
    "T_Channel": ["T_Channel", "คุณซื้อชาพร้อมดื่ม (Ready to drink) จากช่องทางใดบ้าง"],
}

LABEL_COLUMNS = ["Age", "S_Frequency", "S_Screentime"]
SINGLE_CHOICE_COLUMNS = ["S_Occasion", "C_Frequency", "C_Favorite", "T_Frequency", "T_Favorite"]
MULTI_CHOICE_COLUMNS = ["C_Occasion", "T_Occasion", "T_Channel"]


def unique_options(col):
    return sorted(df_raw[col].dropna().astype(str).unique())


def split_unique_options(col):
    values = set()
    for raw_value in df_raw[col].dropna().astype(str):
        values.update(v.strip() for v in raw_value.split(",") if v.strip())
    return sorted(values)


def label_map(col):
    return {value: index for index, value in enumerate(sorted(df_raw[col].dropna().astype(str).unique()))}


LABEL_MAPS = {col: label_map(col) for col in LABEL_COLUMNS}
MODEL_LABELS = [label.replace("Cluster_ID_", "") for label in le.classes_]


def make_dropdown(id_, label, options):
    return html.Div([
        html.Label(label, className="form-label-brown"),
        dcc.Dropdown(
            id=id_,
            options=[{"label": option, "value": option} for option in options],
            placeholder=f"เลือก {label}",
            clearable=False,
            style={"fontFamily": "Sarabun, Tahoma"},
        ),
    ], className="mb-3")


def split_answers(value):
    if pd.isna(value):
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]


def decode_upload(contents):
    _, encoded = contents.split(",", 1)
    raw_bytes = base64.b64decode(encoded)
    for encoding in ("utf-8-sig", "utf-8", "cp874"):
        try:
            return pd.read_csv(io.BytesIO(raw_bytes), encoding=encoding)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(io.BytesIO(raw_bytes))


def normalize_uploaded_columns(upload_df):
    normalized = pd.DataFrame(index=upload_df.index)
    missing = []

    for target_col, aliases in COLUMN_ALIASES.items():
        source_col = next((col for col in aliases if col in upload_df.columns), None)
        if source_col:
            normalized[target_col] = upload_df[source_col]
        else:
            normalized[target_col] = np.nan
            missing.append(target_col)

    return normalized, missing


def build_feature_frame(input_df):
    rows = []

    for _, source in input_df.iterrows():
        row = {col: 0 for col in feature_cols}

        for col in LABEL_COLUMNS:
            if col in row:
                row[col] = LABEL_MAPS[col].get(str(source.get(col, "")), 0)

        for col in SINGLE_CHOICE_COLUMNS:
            feature_name = f"{col}_{source.get(col, '')}"
            if feature_name in row:
                row[feature_name] = 1

        for col in MULTI_CHOICE_COLUMNS:
            for answer in split_answers(source.get(col, "")):
                feature_name = f"{col}_{answer}"
                if feature_name in row:
                    row[feature_name] = 1

        rows.append(row)

    return pd.DataFrame(rows, columns=feature_cols).values.astype(float)


def predict_segments(input_df):
    x_in = build_feature_frame(input_df)
    probas = model.predict_proba(x_in)
    pred_indices = np.argmax(probas, axis=1)
    segments = [label.replace("Cluster_ID_", "") for label in le.inverse_transform(pred_indices)]

    result_df = input_df.copy()
    result_df.insert(0, "Predicted_Segment", segments)
    for label_index, label in enumerate(MODEL_LABELS):
        result_df[f"Probability_{label}"] = (probas[:, label_index] * 100).round(1)

    return result_df


def render_single_result(segment, proba):
    icon = SEGMENT_ICON.get(segment, "🎯")
    color = SEGMENT_COLOR.get(segment, "#6F4E37")
    rec = CAMPAIGN_REC.get(segment, "")

    return html.Div([
        html.Div([
            html.Div(icon, style={"fontSize": "56px"}),
            html.H3(segment, style={"fontWeight": "700", "marginTop": "8px"}),
            html.P("กลุ่มลูกค้าที่ทำนายได้", style={"opacity": "0.85"}),
        ], className="predict-result mb-3", style={"background": f"linear-gradient(135deg, {color}, #C8860A)"}),

        dbc.Card(dbc.CardBody([
            html.H6("ความน่าจะเป็นแต่ละกลุ่ม", className="fw-bold mb-3", style={"color": "#6F4E37"}),
            *[html.Div([
                html.Div(
                    f"{label}  {p * 100:.1f}%",
                    style={"fontSize": "13px", "marginBottom": "4px", "fontWeight": "600" if label == segment else "400"},
                ),
                dbc.Progress(
                    value=round(p * 100, 1),
                    max=100,
                    style={"height": "18px", "marginBottom": "10px"},
                    color="warning" if label == segment else "secondary",
                ),
            ]) for label, p in zip(MODEL_LABELS, proba)],
        ]), className="chart-card mb-3"),
        dbc.Card(dbc.CardBody([
            html.H6("💡 Campaign Recommendation", className="fw-bold mb-2", style={"color": "#6F4E37"}),
            html.P(rec, style={"fontSize": "14px", "margin": "0"}),
        ]), className="chart-card"),
    ])


def log_single_prediction(input_data, segment, proba):
    payload = build_event_payload(
        mode="single",
        input_data=input_data,
        prediction_data={
            "predicted_segment": segment,
            "probabilities": {label: round(float(p) * 100, 1) for label, p in zip(MODEL_LABELS, proba)},
        },
    )
    log_to_firebase("predictions/single", payload)


def render_batch_result(result_df, filename, missing_columns):
    segment_counts = result_df["Predicted_Segment"].value_counts()
    preview_cols = ["Predicted_Segment", "Age", "S_Occasion", "C_Favorite", "T_Favorite"]
    preview_cols += [col for col in result_df.columns if col.startswith("Probability_")]
    preview_cols = [col for col in preview_cols if col in result_df.columns]
    preview_df = result_df[preview_cols].head(10)

    warning = None
    if missing_columns:
        warning = dbc.Alert(
            "ไฟล์นี้ไม่มีบางคอลัมน์ที่ใช้ทำนาย: "
            + ", ".join(missing_columns)
            + " ระบบจะใส่ค่าเริ่มต้นให้ feature เหล่านั้น",
            color="warning",
            className="mb-3",
        )

    return html.Div([
        warning,
        dbc.Row([
            dbc.Col(html.Div([
                html.Div(f"{len(result_df)}", className="kpi-number"),
                html.Div("จำนวนรายการที่ทำนาย", className="kpi-label"),
            ], className="kpi-card"), md=3),
            *[
                dbc.Col(html.Div([
                    html.Div(str(segment_counts.get(label, 0)), className="kpi-number"),
                    html.Div(label, className="kpi-label"),
                ], className="kpi-card"), md=3)
                for label in MODEL_LABELS
            ],
        ], className="g-3 mb-4"),

        dbc.Card(dbc.CardBody([
            html.H5("📄 Preview ผลการทำนาย", className="fw-bold mb-3", style={"color": "#6F4E37"}),
            dash_table.DataTable(
                data=preview_df.to_dict("records"),
                columns=[{"name": col, "id": col} for col in preview_df.columns],
                page_size=10,
                style_table={"overflowX": "auto"},
                style_cell={"fontFamily": "Sarabun, Tahoma", "fontSize": "13px", "padding": "8px", "textAlign": "left"},
                style_header={"backgroundColor": "#FFF8F0", "fontWeight": "700", "color": "#6F4E37"},
            ),
            dbc.Button(
                "⬇️ Download Prediction CSV",
                id="download-batch-btn",
                n_clicks=0,
                className="mt-3",
                style={"backgroundColor": "#6F4E37", "border": "none", "fontWeight": "600"},
            ),
            html.Div(filename, className="text-muted mt-2", style={"fontSize": "13px"}),
        ]), className="chart-card"),
    ])


def log_batch_prediction(result_df, filename, missing_columns):
    segment_counts = result_df["Predicted_Segment"].value_counts().to_dict()
    payload = build_event_payload(
        mode="batch",
        input_data={
            "filename": filename,
            "missing_columns": missing_columns,
            "row_count": int(len(result_df)),
        },
        prediction_data={
            "segment_counts": segment_counts,
        },
    )
    log_to_firebase("predictions/batch", payload)


model_info = dbc.Card(dbc.CardBody([
    html.H5("📋 Model Information", className="fw-bold mb-3", style={"color": "#6F4E37"}),
    html.Table([
        html.Tr([html.Td("Algorithm", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("XGBClassifier", className="fw-bold")]),
        html.Tr([html.Td("SMOTE", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("✅ Class Balancing")]),
        html.Tr([html.Td("Test Acc", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("94.12%", className="fw-bold", style={"color": "#6F4E37"})]),
        html.Tr([html.Td("Cross-val", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("92.45% ±3.41%")]),
        html.Tr([html.Td("Train Acc", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("96.23%")]),
        html.Tr([html.Td("Classes", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("3 กลุ่ม")]),
    ], style={"width": "100%", "borderCollapse": "separate", "borderSpacing": "0 6px"}),
]), className="chart-card mb-3")

classification_report = dbc.Card(dbc.CardBody([
    html.H5("📊 Classification Report", className="fw-bold mb-3", style={"color": "#6F4E37"}),
    html.Table([
        html.Thead(html.Tr([html.Th("Class"), html.Th("Precision"), html.Th("Recall"), html.Th("F1")])),
        html.Tbody([
            html.Tr([html.Td("ชอบกาแฟ"), html.Td("0.86"), html.Td("1.00"), html.Td("0.92")]),
            html.Tr([html.Td("ชอบชา"), html.Td("1.00"), html.Td("0.82"), html.Td("0.90")]),
            html.Tr([html.Td("ชอบทั้งกาแฟและชา"), html.Td("0.94"), html.Td("1.00"), html.Td("0.97")]),
        ]),
    ], style={"width": "100%", "textAlign": "center"}),
]), className="chart-card")

single_prediction_tab = dbc.Row([
    dbc.Col([model_info, classification_report], md=4),
    dbc.Col([
        dbc.Card(dbc.CardBody([
            html.H5("🔮 กรอกข้อมูลเพื่อทำนาย", className="fw-bold mb-3", style={"color": "#6F4E37"}),
            make_dropdown("dd-age", "อายุ", unique_options("Age")),
            make_dropdown("dd-freq", "ความถี่การใช้โซเชียลมีเดีย (S_Frequency)", unique_options("S_Frequency")),
            make_dropdown("dd-screen", "เวลาหน้าจอต่อวัน (S_Screentime)", unique_options("S_Screentime")),
            make_dropdown("dd-occasion", "แพลตฟอร์มที่ใช้ประจำ (S_Occasion)", unique_options("S_Occasion")),
            make_dropdown("dd-cfav", "ชอบกาแฟประเภทไหน (C_Favorite)", unique_options("C_Favorite")),
            make_dropdown("dd-tfav", "ชอบชาประเภทไหน (T_Favorite)", unique_options("T_Favorite")),
            make_dropdown("dd-tch", "ซื้อชาจากที่ไหน (T_Channel)", split_unique_options("T_Channel")),
            dbc.Button("🔮 Predict Segment", id="predict-btn", n_clicks=0, className="predict-button"),
        ]), className="chart-card mb-3"),
        html.Div(id="predict-output"),
    ], md=8),
])

batch_prediction_tab = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H5("📤 Upload Raw Survey CSV", className="fw-bold mb-3", style={"color": "#6F4E37"}),
                html.P(
                    "อัปโหลดไฟล์ข้อมูลดิบรูปแบบเดียวกับ RTD_Brew.csv ระบบจะจัดคอลัมน์ที่จำเป็น แปลง feature และทำนาย segment ให้ทั้งไฟล์",
                    className="text-muted",
                ),
                dcc.Upload(
                    id="batch-upload",
                    children=html.Div(["ลากไฟล์มาวาง หรือ ", html.A("เลือกไฟล์ CSV")]),
                    className="upload-box",
                    multiple=False,
                    accept=".csv",
                ),
                dbc.Button("🚀 Predict Uploaded File", id="batch-predict-btn", n_clicks=0, className="predict-button mt-3"),
            ]), className="chart-card"),
        ], lg=5),
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H5("สิ่งที่ระบบใช้จากไฟล์", className="fw-bold mb-3", style={"color": "#6F4E37"}),
                html.Div([
                    html.Div("อายุ / พฤติกรรมออนไลน์", className="batch-feature-pill"),
                    html.Div("ประเภทกาแฟและชาที่ดื่ม", className="batch-feature-pill"),
                    html.Div("โอกาสในการดื่ม RTD", className="batch-feature-pill"),
                    html.Div("ช่องทางซื้อชาพร้อมดื่ม", className="batch-feature-pill"),
                ], className="batch-feature-list"),
                html.P("หากเจอคำตอบหรือ category ใหม่ที่โมเดลไม่เคยเห็น ระบบจะข้าม feature นั้นและยังทำนายต่อได้", className="text-muted mt-3 mb-0"),
            ]), className="chart-card"),
        ], lg=7),
    ], className="g-3"),
    dcc.Store(id="batch-result-store"),
    dcc.Download(id="batch-download"),
    html.Div(id="batch-output"),
])

layout = html.Div([
    html.H2("🎯 Supervised Learning — Customer Segment Prediction", className="section-title"),
    html.P("ทำนายกลุ่มลูกค้าได้ทั้งแบบกรอกทีละคน และแบบอัปโหลดไฟล์ CSV เพื่อทำนายหลายรายการ", className="text-muted mb-4"),
    dbc.Tabs([
        dbc.Tab(single_prediction_tab, label="🔮 Single Prediction", tab_id="single"),
        dbc.Tab(batch_prediction_tab, label="📤 Batch Prediction", tab_id="batch"),
    ], id="supervised-tabs", active_tab="single"),
], className="page-wrapper")


@callback(
    Output("predict-output", "children"),
    Input("predict-btn", "n_clicks"),
    State("dd-age", "value"),
    State("dd-freq", "value"),
    State("dd-screen", "value"),
    State("dd-occasion", "value"),
    State("dd-cfav", "value"),
    State("dd-tfav", "value"),
    State("dd-tch", "value"),
    prevent_initial_call=True,
)
def predict_single(n, age, freq, screen, occasion, cfav, tfav, tch):
    if not all([age, freq, screen, occasion, cfav, tfav, tch]):
        return dbc.Alert("⚠️ กรุณากรอกข้อมูลให้ครบทุกช่อง", color="warning")

    try:
        input_df = pd.DataFrame([{
            "Age": age,
            "S_Frequency": freq,
            "S_Screentime": screen,
            "S_Occasion": occasion,
            "C_Favorite": cfav,
            "T_Favorite": tfav,
            "T_Channel": tch,
        }])
        x_in = build_feature_frame(input_df)
        proba = model.predict_proba(x_in)[0]
        segment = le.inverse_transform([int(np.argmax(proba))])[0].replace("Cluster_ID_", "")
        log_single_prediction(input_df.iloc[0].to_dict(), segment, proba)
        return render_single_result(segment, proba)

    except Exception as e:
        return dbc.Alert(f"❌ เกิดข้อผิดพลาด: {str(e)}", color="danger")


@callback(
    Output("batch-output", "children"),
    Output("batch-result-store", "data"),
    Input("batch-predict-btn", "n_clicks"),
    State("batch-upload", "contents"),
    State("batch-upload", "filename"),
    prevent_initial_call=True,
)
def predict_batch(n_clicks, contents, filename):
    if not contents:
        return dbc.Alert("⚠️ กรุณาอัปโหลดไฟล์ CSV ก่อน", color="warning"), None

    try:
        upload_df = decode_upload(contents)
        normalized_df, missing_columns = normalize_uploaded_columns(upload_df)
        result_df = predict_segments(normalized_df)
        output = render_batch_result(result_df, filename or "uploaded.csv", missing_columns)
        log_batch_prediction(result_df, filename or "uploaded.csv", missing_columns)
        return output, result_df.to_json(orient="split", force_ascii=False)

    except Exception as e:
        return dbc.Alert(f"❌ อ่านไฟล์หรือทำนายไม่สำเร็จ: {str(e)}", color="danger"), None


@callback(
    Output("batch-download", "data"),
    Input("download-batch-btn", "n_clicks"),
    State("batch-result-store", "data"),
    prevent_initial_call=True,
)
def download_batch_result(n_clicks, stored_json):
    if not stored_json:
        return None
    result_df = pd.read_json(io.StringIO(stored_json), orient="split")
    return dcc.send_data_frame(result_df.to_csv, "batch_prediction_results.csv", index=False, encoding="utf-8-sig")
