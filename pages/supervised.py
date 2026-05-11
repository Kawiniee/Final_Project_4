import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import joblib


dash.register_page(__name__, path="/supervised", name="Supervised Learning")

feature_cols = joblib.load("models/feature_cols.pkl")
model = joblib.load("models/customer_model.pkl")
le = joblib.load("models/label_encoder.pkl")
df_raw = pd.read_csv("data/cleaned_data.csv")

SEGMENT_ICON = {"ชอบกาแฟ": "☕", "ชอบชา": "🍵", "ชอบทั้งกาแฟและชา": "🍵☕"}
SEGMENT_COLOR = {"ชอบกาแฟ": "#6F4E37", "ชอบชา": "#8f8f8f", "ชอบทั้งกาแฟและชา": "#21cdb6"}
CAMPAIGN_REC = {
    "ชอบกาแฟ": "📱 Facebook/Instagram | ⏰ 18.00-21.59 น. | 🎯 'กาแฟสดในขวด รสชาติเหมือนร้าน พกพาได้ทุกที่'",
    "ชอบชา": "📱 Facebook | ⏰ 18.00-21.59 น. | 🎯 'ชาพรีเมียม ไม่มีน้ำตาล — Healthy Choice ของคนรักชา'",
    "ชอบทั้งกาแฟและชา": "📱 LINE | ⏰ 18.00-21.59 น. | 🎯 'ครบทุกอารมณ์ ทั้งกาแฟและชา เลือกได้ตามวัน'",
}


def unique_options(col):
    return sorted(df_raw[col].dropna().astype(str).unique())


def split_unique_options(col):
    values = set()
    for raw_value in df_raw[col].dropna().astype(str):
        values.update(v.strip() for v in raw_value.split(",") if v.strip())
    return sorted(values)


def label_map(col):
    return {value: index for index, value in enumerate(sorted(df_raw[col].dropna().astype(str).unique()))}


LABEL_MAPS = {
    "Age": label_map("Age"),
    "S_Frequency": label_map("S_Frequency"),
    "S_Screentime": label_map("S_Screentime"),
}


def make_dropdown(id_, label, options):
    return html.Div([
        html.Label(label, style={"fontWeight": "600", "color": "#6F4E37", "marginBottom": "4px"}),
        dcc.Dropdown(
            id=id_,
            options=[{"label": option, "value": option} for option in options],
            placeholder=f"เลือก {label}",
            clearable=False,
            style={"fontFamily": "Sarabun, Tahoma"},
        ),
    ], className="mb-3")


layout = html.Div([
    html.H2("🎯 Supervised Learning — Customer Segment Prediction", className="section-title"),
    html.P("กรอกข้อมูลพฤติกรรมเพื่อทำนายกลุ่มลูกค้า และรับคำแนะนำ Campaign", className="text-muted mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H5("📋 Model Information", className="fw-bold mb-3", style={"color": "#6F4E37"}),
                html.Table([
                    html.Tr([html.Td("Algorithm", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("XGBClassifier", className="fw-bold")]),
                    html.Tr([html.Td("SMOTE", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("✅ Class Balancing")]),
                    html.Tr([html.Td("Test Acc", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("94.12%", className="fw-bold", style={"color": "#6F4E37"})]),
                    html.Tr([html.Td("Cross-val", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("92.45% ±3.41%")]),
                    html.Tr([html.Td("Train Acc", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("96.23%")]),
                    html.Tr([html.Td("Classes", style={"paddingRight": "12px", "color": "#8D6E63"}), html.Td("3 กลุ่ม")]),
                ], style={"width": "100%", "borderCollapse": "separate", "borderSpacing": "0 6px"}),
            ]), className="chart-card mb-3"),

            dbc.Card(dbc.CardBody([
                html.H5("📊 Classification Report", className="fw-bold mb-3", style={"color": "#6F4E37"}),
                html.Table([
                    html.Thead(html.Tr([html.Th("Class"), html.Th("Precision"), html.Th("Recall"), html.Th("F1")])),
                    html.Tbody([
                        html.Tr([html.Td("ชอบกาแฟ"), html.Td("0.86"), html.Td("1.00"), html.Td("0.92")]),
                        html.Tr([html.Td("ชอบชา"), html.Td("1.00"), html.Td("0.82"), html.Td("0.90")]),
                        html.Tr([html.Td("ชอบทั้งกาแฟและชา"), html.Td("0.94"), html.Td("1.00"), html.Td("0.97")]),
                    ]),
                ], style={"width": "100%", "textAlign": "center"}),
            ]), className="chart-card"),
        ], md=4),

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

                dbc.Button(
                    "🔮 Predict Segment",
                    id="predict-btn",
                    n_clicks=0,
                    style={"backgroundColor": "#6F4E37", "border": "none", "width": "100%", "marginTop": "8px", "fontWeight": "600"},
                ),
            ]), className="chart-card mb-3"),

            html.Div(id="predict-output"),
        ], md=8),
    ]),
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
def predict(n, age, freq, screen, occasion, cfav, tfav, tch):
    if not all([age, freq, screen, occasion, cfav, tfav, tch]):
        return dbc.Alert("⚠️ กรุณากรอกข้อมูลให้ครบทุกช่อง", color="warning")

    try:
        input_dict = {col: 0 for col in feature_cols}

        for col_base, val in [("Age", age), ("S_Frequency", freq), ("S_Screentime", screen)]:
            if col_base in input_dict:
                input_dict[col_base] = LABEL_MAPS[col_base].get(str(val), 0)

        for prefix, val in [
            ("S_Occasion_", occasion),
            ("C_Favorite_", cfav),
            ("T_Favorite_", tfav),
            ("T_Channel_", tch),
        ]:
            col = prefix + val
            if col in input_dict:
                input_dict[col] = 1

        x_in = pd.DataFrame([input_dict], columns=feature_cols).values.astype(float)
        proba = model.predict_proba(x_in)[0]
        pred_i = int(np.argmax(proba))
        pred = le.inverse_transform([pred_i])[0]
        segment = pred.replace("Cluster_ID_", "")

        icon = SEGMENT_ICON.get(segment, "🎯")
        color = SEGMENT_COLOR.get(segment, "#6F4E37")
        rec = CAMPAIGN_REC.get(segment, "")
        labels = [label.replace("Cluster_ID_", "") for label in le.classes_]

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
                        f"{lbl}  {p * 100:.1f}%",
                        style={"fontSize": "13px", "marginBottom": "4px", "fontWeight": "600" if lbl == segment else "400"},
                    ),
                    dbc.Progress(
                        value=round(p * 100, 1),
                        max=100,
                        style={"height": "18px", "marginBottom": "10px"},
                        color="warning" if lbl == segment else "secondary",
                    ),
                ]) for lbl, p in zip(labels, proba)],
            ]), className="chart-card mb-3"),

            dbc.Card(dbc.CardBody([
                html.H6("💡 Campaign Recommendation", className="fw-bold mb-2", style={"color": "#6F4E37"}),
                html.P(rec, style={"fontSize": "14px", "margin": "0"}),
            ]), className="chart-card"),
        ])

    except Exception as e:
        return dbc.Alert(f"❌ เกิดข้อผิดพลาด: {str(e)}", color="danger")
