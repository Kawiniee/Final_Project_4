# BUILD PROMPT — AI-Driven Marketing Campaign System

## โครงสร้างโปรเจคที่ต้องการ

จัดไฟล์ใหม่ให้เป็นแบบนี้ (ไฟล์ที่มีอยู่แล้วไม่ต้องแก้ ย้ายมาวางในตำแหน่งที่ถูกต้องเท่านั้น):

```
FINAL_PROJECT_4/
├── app.py                        ← สร้างใหม่
├── .env                          (คงเดิม)
├── assets/
│   ├── style.css                 ← สร้างใหม่
│   └── charts/                   (คงเดิม — PNG ทุกไฟล์อยู่ที่นี่แล้ว)
│       ├── unsup_cluster_heatmap.png
│       ├── unsup_correlation.png
│       ├── unsup_elbow_silhouette.png
│       ├── unsup_pca_scatter.png
│       ├── bi_bar_influence.png
│       ├── bi_donut_influence.png
│       ├── bi_festival_behavior.png
│       └── bi_platform_by_cluster.png
├── data/
│   ├── cleaned_data.csv          (คงเดิม)
│   ├── encoded_data.csv          (คงเดิม)
│   └── unsupervised_results.csv  (คงเดิม)
├── models/
│   ├── customer_model.pkl        (คงเดิม)
│   ├── feature_cols.pkl          (คงเดิม)
│   └── label_encoder.pkl         (คงเดิม)
├── notebooks/                    ← ย้ายมารวมกัน
│   ├── business_insight.ipynb
│   ├── supervised.ipynb
│   └── unsupervised.ipynb
├── scripts/                      ← ย้ายมารวมกัน
│   ├── cleaned_data.py
│   ├── firebase_config.py
│   └── retrain.py
└── pages/
    ├── home.py                   ← สร้างใหม่
    ├── unsupervised.py           ← สร้างใหม่
    ├── business_insight.py       ← สร้างใหม่
    └── supervised.py             ← สร้างใหม่
```

---

## สิ่งที่ต้องสร้างใหม่ทั้งหมด

### 1. `app.py`

```python
import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap"],
    suppress_callback_exceptions=True
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("🏠 Home",                  href="/",                active="exact")),
        dbc.NavItem(dbc.NavLink("🔍 Unsupervised Learning", href="/unsupervised",     active="exact")),
        dbc.NavItem(dbc.NavLink("📈 Business Insight",      href="/business-insight", active="exact")),
        dbc.NavItem(dbc.NavLink("🎯 Supervised Learning",   href="/supervised",       active="exact")),
    ],
    brand="☕ AI-Driven Marketing Campaign",
    brand_href="/",
    color="#6F4E37",
    dark=True,
)

app.layout = html.Div([
    navbar,
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)
```

---

### 2. `assets/style.css`

```css
body {
    font-family: 'Sarabun', 'Tahoma', sans-serif;
    background-color: #FFF8F0;
    color: #3E2723;
}
.page-wrapper   { padding: 28px; }
.section-title  { color: #6F4E37; font-weight: 700; margin-bottom: 16px; }
.chart-card     { border-radius: 12px; box-shadow: 0 2px 10px rgba(111,78,55,0.12); margin-bottom: 24px; background: #fff; }
.insight-box    { background-color: #FFF8F0; border-left: 4px solid #6F4E37; padding: 12px 16px; border-radius: 0 8px 8px 0; font-size: 14px; margin-top: 12px; }
.kpi-card       { border-radius: 12px; padding: 20px; background: #fff; box-shadow: 0 2px 10px rgba(111,78,55,0.12); border-top: 4px solid #6F4E37; text-align: center; }
.kpi-number     { font-size: 36px; font-weight: 700; color: #6F4E37; }
.kpi-label      { font-size: 14px; color: #8D6E63; }
.persona-card   { border-radius: 12px; padding: 20px; background: #fff; box-shadow: 0 2px 10px rgba(111,78,55,0.12); height: 100%; }
.predict-result { border-radius: 12px; padding: 24px; background: linear-gradient(135deg, #6F4E37, #C8860A); color: white; text-align: center; }
.navbar-nav .nav-link { color: rgba(255,255,255,0.85) !important; }
.navbar-nav .nav-link.active { color: #fff !important; font-weight: 700; border-bottom: 2px solid #D2B48C; }
```

---

### 3. `pages/home.py`

```python
import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path="/", name="Home")

df = pd.read_csv("data/cleaned_data.csv")

n_customers   = len(df)
n_clusters    = 3
test_accuracy = "94.12%"
top_cluster   = df["Cluster_ID"].value_counts().idxmax()

layout = html.Div([
    # Header
    html.Div([
        html.H1("☕ AI-Driven Marketing Campaign System", className="section-title", style={"fontSize":"28px"}),
        html.P("ร้านกาแฟสาขากว่า 4,000 แห่ง ขยายสู่ตลาด Ready-to-Drink (RTD)", className="text-muted"),
    ], className="mb-4"),

    # KPI Cards
    dbc.Row([
        dbc.Col(html.Div([html.Div(f"{n_customers}", className="kpi-number"), html.Div("จำนวนลูกค้าทั้งหมด", className="kpi-label")], className="kpi-card"), md=3),
        dbc.Col(html.Div([html.Div(f"{n_clusters}",  className="kpi-number"), html.Div("จำนวน Cluster",       className="kpi-label")], className="kpi-card"), md=3),
        dbc.Col(html.Div([html.Div(test_accuracy,    className="kpi-number"), html.Div("Test Accuracy (XGBoost)", className="kpi-label")], className="kpi-card"), md=3),
        dbc.Col(html.Div([html.Div(top_cluster,      className="kpi-number", style={"fontSize":"20px","paddingTop":"8px"}), html.Div("กลุ่มที่ใหญ่ที่สุด", className="kpi-label")], className="kpi-card"), md=3),
    ], className="mb-5"),

    # System Architecture
    html.H4("🏗️ System Architecture", className="section-title"),
    dbc.Card(dbc.CardBody(
        html.Div([
            *[html.Div([
                html.Div(label, style={"background":"#6F4E37","color":"#fff","padding":"10px 18px","borderRadius":"8px","fontWeight":"600","whiteSpace":"nowrap"}),
                html.Div("→", style={"fontSize":"20px","margin":"0 8px","color":"#6F4E37"}) if i < 4 else html.Div()
            ]) for i, label in enumerate(["Survey Data","Data Cleaning","K-Means Clustering","XGBoost + SMOTE","Dashboard"])],
        ], style={"display":"flex","alignItems":"center","justifyContent":"center","flexWrap":"wrap","gap":"4px","padding":"16px"})
    ), className="chart-card mb-5"),

    # Model Performance Summary
    html.H4("📊 Model Performance Summary", className="section-title"),
    dbc.Card(dbc.CardBody(
        dbc.Row([
            dbc.Col(html.Div([html.Div("96.23%", className="kpi-number", style={"fontSize":"28px"}), html.Div("Train Accuracy", className="kpi-label")]), className="text-center", md=4),
            dbc.Col(html.Div([html.Div("94.12%", className="kpi-number", style={"fontSize":"28px"}), html.Div("Test Accuracy",  className="kpi-label")]), className="text-center", md=4),
            dbc.Col(html.Div([html.Div("92.45%", className="kpi-number", style={"fontSize":"28px"}), html.Div("Cross-val Accuracy (±3.41%)", className="kpi-label")]), className="text-center", md=4),
        ])
    ), className="chart-card mb-5"),

    # Team
    html.H4("👥 ทีมงาน", className="section-title"),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("👤", style={"fontSize":"32px","textAlign":"center"}),
            html.P(name,  className="text-center mb-0 fw-bold"),
            html.P(role,  className="text-center text-muted", style={"fontSize":"13px"}),
        ]), className="chart-card"), md=2)
        for name, role in [
            ("Member 1","Business Analyst"), ("Member 2","Data Engineer"),
            ("Member 3","ML Engineer"),      ("Member 4","Backend Dev"),
            ("Member 5","Frontend Dev"),
        ]
    ]),
], className="page-wrapper")
```

---

### 4. `pages/unsupervised.py`

```python
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/unsupervised", name="Unsupervised Learning")

def chart_block(title, img_path, insight):
    return dbc.Card(dbc.CardBody([
        html.H5(title, className="fw-bold mb-3", style={"color":"#6F4E37"}),
        html.Img(src=img_path, style={"width":"100%","borderRadius":"8px"}),
        html.Div([html.Strong("📌 คำอธิบาย: "), insight], className="insight-box mt-3"),
    ]), className="chart-card")

layout = html.Div([
    html.H2("🔍 Unsupervised Learning", className="section-title"),
    html.P("การวิเคราะห์และแบ่งกลุ่มลูกค้าด้วย K-Means Clustering", className="text-muted mb-4"),

    dbc.Tabs([

        dbc.Tab(label="📊 Correlation Analysis", tab_id="corr", children=[html.Br(),
            chart_block(
                "Correlation Heatmap — Coffee & Tea Features",
                "/assets/charts/unsup_correlation.png",
                "ความสัมพันธ์ภายในกลุ่มกาแฟ (C_*) และกลุ่มชา (T_*) มีค่าสูง แสดงว่าผู้ที่ให้ความสำคัญกับคุณสมบัติหนึ่งมักให้ความสำคัญกับคุณสมบัติอื่นในกลุ่มเดียวกัน ในขณะที่ความสัมพันธ์ข้ามกลุ่มมีค่าต่ำ บ่งบอกว่าความชอบกาแฟและชา RTD เป็นอิสระต่อกัน สามารถแบ่ง segment ได้ชัดเจน"
            ),
        ]),

        dbc.Tab(label="📉 Elbow & Silhouette", tab_id="elbow", children=[html.Br(),
            chart_block(
                "Elbow Method & Silhouette Score",
                "/assets/charts/unsup_elbow_silhouette.png",
                "Elbow Method พบจุดหักศอกที่ K=3 และ Silhouette Score สูงสุดที่ K=3 เช่นกัน ยืนยันว่าการแบ่ง 3 กลุ่มเหมาะสมที่สุดสำหรับข้อมูลชุดนี้"
            ),
        ]),

        dbc.Tab(label="🗺️ PCA Scatter", tab_id="pca", children=[html.Br(),
            chart_block(
                "Customer Segmentation — PCA 2D",
                "/assets/charts/unsup_pca_scatter.png",
                "ทั้ง 3 กลุ่มมีการกระจายตัวแยกออกจากกันค่อนข้างชัดเจนใน 2 มิติหลัก แสดงว่าโมเดล K-Means สามารถแบ่งกลุ่มลูกค้าได้อย่างมีความหมาย กลุ่มชอบกาแฟและชอบชาอยู่คนละด้าน ส่วนกลุ่มชอบทั้งสองอยู่ตรงกลาง"
            ),
        ]),

        dbc.Tab(label="🔥 Cluster Profiling", tab_id="heatmap", children=[html.Br(),
            chart_block(
                "Cluster Profiling Heatmap — Mean Score ของแต่ละกลุ่ม",
                "/assets/charts/unsup_cluster_heatmap.png",
                "กลุ่มชอบกาแฟ: คะแนนสูงที่ C_Aroma และ C_Fresh_Taste | กลุ่มชอบชา: คะแนนสูงที่ T_Aroma และ T_No_Sugar | กลุ่มชอบทั้งสอง: คะแนนสูงทั้งสองด้าน ข้อมูลนี้ใช้ออกแบบ creative ของ campaign แต่ละกลุ่มได้โดยตรง"
            ),
        ]),

        dbc.Tab(label="👤 Customer Persona", tab_id="persona", children=[html.Br(),
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("☕", style={"fontSize":"48px","textAlign":"center"}),
                    html.H4("ชอบกาแฟ", className="text-center mt-2 fw-bold"),
                    html.Hr(),
                    html.P("ให้ความสำคัญกับกลิ่นหอมและรสชาติสดของกาแฟ ไม่ค่อยสนใจชา RTD"),
                    html.P("🏆 Top: C_Aroma, C_Fresh_Taste, C_Alert"),
                    html.Div("💡 Facebook/Instagram | 18.00-21.59 น. | 'กาแฟสดในขวด รสชาติเหมือนร้าน'", className="insight-box"),
                ]), className="persona-card", style={"borderTop":"4px solid #6F4E37"}), md=4),

                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("🍵☕", style={"fontSize":"48px","textAlign":"center"}),
                    html.H4("ชอบทั้งกาแฟและชา", className="text-center mt-2 fw-bold"),
                    html.Hr(),
                    html.P("ให้ความสำคัญทั้งสองด้านสูง ชอบ variety และ lifestyle"),
                    html.P("🏆 Top: C_Aroma, T_Aroma, T_Portable"),
                    html.Div("💡 LINE | 18.00-21.59 น. | 'ครบทุกอารมณ์ ทั้งกาแฟและชา'", className="insight-box"),
                ]), className="persona-card", style={"borderTop":"4px solid #21cdb6"}), md=4),

                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("🍵", style={"fontSize":"48px","textAlign":"center"}),
                    html.H4("ชอบชา", className="text-center mt-2 fw-bold"),
                    html.Hr(),
                    html.P("ให้ความสำคัญกับชาเป็นหลัก ชอบไม่หวาน พกพาสะดวก"),
                    html.P("🏆 Top: T_Aroma, T_No_Sugar, T_Intense"),
                    html.Div("💡 Facebook | 18.00-21.59 น. | 'ชาพรีเมียม ไม่มีน้ำตาล Healthy Choice'", className="insight-box"),
                ]), className="persona-card", style={"borderTop":"4px solid #8f8f8f"}), md=4),
            ]),
        ]),

    ], id="unsup-tabs", active_tab="corr"),
], className="page-wrapper")
```

---

### 5. `pages/business_insight.py`

```python
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/business-insight", name="Business Insight")

def insight_block(num, title, img_path, insight):
    return dbc.Card(dbc.CardBody([
        html.H5(f"กราฟที่ {num}: {title}", className="fw-bold mb-3", style={"color":"#6F4E37"}),
        html.Img(src=img_path, style={"width":"100%","borderRadius":"8px"}),
        html.Div([html.Strong("📌 Insight: "), insight], className="insight-box mt-3"),
    ]), className="chart-card")

layout = html.Div([
    html.H2("📈 Business Insight", className="section-title"),
    html.P("วิเคราะห์พฤติกรรมผู้บริโภคและช่องทางสื่อสำหรับ RTD Campaign", className="text-muted mb-4"),

    insight_block(1, "สัดส่วนช่องทางที่มีอิทธิพลต่อการตัดสินใจซื้อ",
        "/assets/charts/bi_donut_influence.png",
        "โซเชียลมีเดียมีอิทธิพลสูงสุดต่อการตัดสินใจซื้อ รองลงมาคือแพลตฟอร์มวิดีโอ สอดคล้องกับพฤติกรรม digital-first ของกลุ่มเป้าหมายอายุ 23-29 ปี — ควรเน้น budget บน Digital Channel เป็นหลัก"),

    insight_block(2, "จำนวนผู้ได้รับอิทธิพลจากโฆษณาแต่ละช่องทาง",
        "/assets/charts/bi_bar_influence.png",
        "ช่องทาง Online ครองสัดส่วนมากกว่า 70% ของการรับรู้โฆษณา สื่อ Offline อย่างบิลบอร์ดและรถไฟฟ้ามีผลน้อยกว่ามาก — Digital Marketing คือ channel หลักที่ควร allocate budget"),

    insight_block(3, "แพลตฟอร์มที่ใช้งานประจำ แบ่งตามกลุ่มลูกค้า",
        "/assets/charts/bi_platform_by_cluster.png",
        "กลุ่มชอบทั้งกาแฟและชา นิยม LINE มากที่สุด ส่วนกลุ่มชอบกาแฟและชอบชา กระจายตัวบน Facebook และ Instagram — ใช้ข้อมูลนี้ทำ platform targeting แยกตาม segment ได้โดยตรง"),

    insight_block(4, "พฤติกรรมการใช้สื่อช่วงเทศกาลสงกรานต์",
        "/assets/charts/bi_festival_behavior.png",
        "ลูกค้าส่วนใหญ่ทุกกลุ่มใช้โซเชียลมีเดียมากขึ้นช่วงสงกรานต์ — นี่คือโอกาสสำคัญในการ launch RTD campaign ช่วงเทศกาล เพราะ reach และ engagement สูงกว่าปกติ"),

    # Strategic Recommendations
    html.H4("💡 Strategic Recommendations", className="section-title mt-2"),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("☕", style={"fontSize":"32px","textAlign":"center"}),
            html.H5("ชอบกาแฟ", className="text-center fw-bold"),
            html.P("📱 Facebook / Instagram", className="text-center"),
            html.P("⏰ 18.00 – 21.59 น.", className="text-center"),
            html.P("🎯 'กาแฟสดในขวด รสชาติเหมือนร้าน พกพาได้ทุกที่'", className="text-center", style={"fontSize":"13px"}),
        ]), style={"borderTop":"4px solid #6F4E37","backgroundColor":"#FFF8F0","borderRadius":"12px"}), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("🍵☕", style={"fontSize":"32px","textAlign":"center"}),
            html.H5("ชอบทั้งกาแฟและชา", className="text-center fw-bold"),
            html.P("📱 LINE", className="text-center"),
            html.P("⏰ 18.00 – 21.59 น.", className="text-center"),
            html.P("🎯 'ครบทุกอารมณ์ ทั้งกาแฟและชา เลือกได้ตามวัน'", className="text-center", style={"fontSize":"13px"}),
        ]), style={"borderTop":"4px solid #21cdb6","backgroundColor":"#FFF8F0","borderRadius":"12px"}), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("🍵", style={"fontSize":"32px","textAlign":"center"}),
            html.H5("ชอบชา", className="text-center fw-bold"),
            html.P("📱 Facebook", className="text-center"),
            html.P("⏰ 18.00 – 21.59 น.", className="text-center"),
            html.P("🎯 'ชาพรีเมียม ไม่มีน้ำตาล — Healthy Choice ของคนรักชา'", className="text-center", style={"fontSize":"13px"}),
        ]), style={"borderTop":"4px solid #8f8f8f","backgroundColor":"#FFF8F0","borderRadius":"12px"}), md=4),
    ]),
], className="page-wrapper")
```

---

### 6. `pages/supervised.py`

```python
import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import joblib

dash.register_page(__name__, path="/supervised", name="Supervised Learning")

# โหลด assets ตอน startup
feature_cols = joblib.load("models/feature_cols.pkl")
model        = joblib.load("models/customer_model.pkl")
le           = joblib.load("models/label_encoder.pkl")
df_enc       = pd.read_csv("data/encoded_data.csv")

# ดึง unique values สำหรับ dropdown จาก encoded_data
df_raw = pd.read_csv("data/cleaned_data.csv")

SEGMENT_ICON = {"ชอบกาแฟ": "☕", "ชอบชา": "🍵", "ชอบทั้งกาแฟและชา": "🍵☕"}
SEGMENT_COLOR = {"ชอบกาแฟ": "#6F4E37", "ชอบชา": "#8f8f8f", "ชอบทั้งกาแฟและชา": "#21cdb6"}
CAMPAIGN_REC = {
    "ชอบกาแฟ":         "📱 Facebook/Instagram | ⏰ 18.00-21.59 น. | 🎯 'กาแฟสดในขวด รสชาติเหมือนร้าน พกพาได้ทุกที่'",
    "ชอบชา":           "📱 Facebook | ⏰ 18.00-21.59 น. | 🎯 'ชาพรีเมียม ไม่มีน้ำตาล — Healthy Choice ของคนรักชา'",
    "ชอบทั้งกาแฟและชา": "📱 LINE | ⏰ 18.00-21.59 น. | 🎯 'ครบทุกอารมณ์ ทั้งกาแฟและชา เลือกได้ตามวัน'",
}

def make_dropdown(id_, label, options):
    return html.Div([
        html.Label(label, style={"fontWeight":"600","color":"#6F4E37","marginBottom":"4px"}),
        dcc.Dropdown(id=id_, options=[{"label":o,"value":o} for o in options],
                     placeholder=f"เลือก {label}", clearable=False,
                     style={"fontFamily":"Sarabun, Tahoma"}),
    ], className="mb-3")

layout = html.Div([
    html.H2("🎯 Supervised Learning — Customer Segment Prediction", className="section-title"),
    html.P("กรอกข้อมูลพฤติกรรมเพื่อทำนายกลุ่มลูกค้า และรับคำแนะนำ Campaign", className="text-muted mb-4"),

    dbc.Row([
        # ── Left: Model Info ──
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H5("📋 Model Information", className="fw-bold mb-3", style={"color":"#6F4E37"}),
                html.Table([
                    html.Tr([html.Td("Algorithm",    style={"paddingRight":"12px","color":"#8D6E63"}), html.Td("XGBClassifier", className="fw-bold")]),
                    html.Tr([html.Td("SMOTE",        style={"paddingRight":"12px","color":"#8D6E63"}), html.Td("✅ Class Balancing")]),
                    html.Tr([html.Td("Test Acc",     style={"paddingRight":"12px","color":"#8D6E63"}), html.Td("94.12%", className="fw-bold", style={"color":"#6F4E37"})]),
                    html.Tr([html.Td("Cross-val",    style={"paddingRight":"12px","color":"#8D6E63"}), html.Td("92.45% ±3.41%")]),
                    html.Tr([html.Td("Train Acc",    style={"paddingRight":"12px","color":"#8D6E63"}), html.Td("96.23%")]),
                    html.Tr([html.Td("Classes",      style={"paddingRight":"12px","color":"#8D6E63"}), html.Td("3 กลุ่ม")]),
                ], style={"width":"100%","borderCollapse":"separate","borderSpacing":"0 6px"}),
            ]), className="chart-card mb-3"),

            dbc.Card(dbc.CardBody([
                html.H5("📊 Classification Report", className="fw-bold mb-3", style={"color":"#6F4E37"}),
                html.Table([
                    html.Thead(html.Tr([html.Th("Class"),html.Th("Precision"),html.Th("Recall"),html.Th("F1")])),
                    html.Tbody([
                        html.Tr([html.Td("ชอบกาแฟ"),         html.Td("0.86"),html.Td("1.00"),html.Td("0.92")]),
                        html.Tr([html.Td("ชอบชา"),           html.Td("1.00"),html.Td("0.82"),html.Td("0.90")]),
                        html.Tr([html.Td("ชอบทั้งกาแฟและชา"), html.Td("0.94"),html.Td("1.00"),html.Td("0.97")]),
                    ]),
                ], style={"width":"100%","textAlign":"center"}),
            ]), className="chart-card"),
        ], md=4),

        # ── Right: Prediction Form ──
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H5("🔮 กรอกข้อมูลเพื่อทำนาย", className="fw-bold mb-3", style={"color":"#6F4E37"}),
                make_dropdown("dd-age",      "อายุ",
                    sorted(df_raw["Age"].dropna().unique())),
                make_dropdown("dd-freq",     "ความถี่การใช้โซเชียลมีเดีย (S_Frequency)",
                    ["ทุกวัน","5-6 ครั้ง/อาทิตย์","3-4 ครั้ง/อาทิตย์","1-2 ครั้ง/อาทิตย์","น้อยกว่า 1 ครั้ง/อาทิตย์"]),
                make_dropdown("dd-screen",   "เวลาหน้าจอต่อวัน (S_Screentime)",
                    ["มากกว่า 6 ชม./วัน","5-6 ชม./วัน","3-4 ชม./วัน","1-2 ชม./วัน","น้อยกว่า 1 ชม./วัน"]),
                make_dropdown("dd-occasion", "แพลตฟอร์มที่ใช้ประจำ (S_Occasion)",
                    ["Facebook","Instagram","LINE","TikTok","Twitter"]),
                make_dropdown("dd-cfav",     "ชอบกาแฟประเภทไหน (C_Favorite)",
                    ["กาแฟสดคั่วบด เช่น ร้านกาแฟสด","แคปซูลกาแฟ","กาแฟกระป๋อง/พร้อมดื่ม","ไม่ดื่มกาแฟ"]),
                make_dropdown("dd-tfav",     "ชอบชาประเภทไหน (T_Favorite)",
                    ["ชาแก้วขายตามร้าน เช่น Kamu","ชาขวดพร้อมดื่ม เช่น Tea P+","ชงเอง","ไม่ดื่มชา"]),
                make_dropdown("dd-tch",      "ซื้อชาจากที่ไหน (T_Channel)",
                    ["ซื้อจากร้านสะดวกซื้อ เช่น 7-11","ซื้อออนไลน์","ซื้อจากร้านชา","ไม่ซื้อชา ready to drink"]),

                dbc.Button("🔮 Predict Segment", id="predict-btn", n_clicks=0,
                           style={"backgroundColor":"#6F4E37","border":"none","width":"100%","marginTop":"8px","fontWeight":"600"}),
            ]), className="chart-card mb-3"),

            html.Div(id="predict-output"),
        ], md=8),
    ]),
], className="page-wrapper")


@callback(
    Output("predict-output", "children"),
    Input("predict-btn", "n_clicks"),
    State("dd-age",      "value"),
    State("dd-freq",     "value"),
    State("dd-screen",   "value"),
    State("dd-occasion", "value"),
    State("dd-cfav",     "value"),
    State("dd-tfav",     "value"),
    State("dd-tch",      "value"),
    prevent_initial_call=True,
)
def predict(n, age, freq, screen, occasion, cfav, tfav, tch):
    # Validate
    if not all([age, freq, screen, occasion, cfav, tfav, tch]):
        return dbc.Alert("⚠️ กรุณากรอกข้อมูลให้ครบทุกช่อง", color="warning")

    try:
        # Build input vector
        input_dict = {col: 0 for col in feature_cols}

        # Label encode: Age, S_Frequency, S_Screentime
        for col_base, val in [("Age", age), ("S_Frequency", freq), ("S_Screentime", screen)]:
            if col_base in input_dict:
                uniq = sorted(df_enc[col_base].dropna().unique())
                if val in uniq:
                    input_dict[col_base] = int(uniq.index(val))

        # One-hot: S_Occasion, C_Favorite, T_Favorite, T_Channel
        for prefix, val in [
            ("S_Occasion_", occasion),
            ("C_Favorite_", cfav),
            ("T_Favorite_", tfav),
            ("T_Channel_",  tch),
        ]:
            col = prefix + val
            if col in input_dict:
                input_dict[col] = 1

        X_in   = pd.DataFrame([input_dict]).values.astype(float)
        proba  = model.predict_proba(X_in)[0]
        pred_i = int(np.argmax(proba))
        pred   = le.inverse_transform([pred_i])[0]
        # strip "Cluster_ID_" prefix if present
        segment = pred.replace("Cluster_ID_", "")

        icon   = SEGMENT_ICON.get(segment, "🎯")
        color  = SEGMENT_COLOR.get(segment, "#6F4E37")
        rec    = CAMPAIGN_REC.get(segment, "")
        labels = [l.replace("Cluster_ID_","") for l in le.classes_]

        return html.Div([
            # Result card
            html.Div([
                html.Div(icon, style={"fontSize":"56px"}),
                html.H3(segment, style={"fontWeight":"700","marginTop":"8px"}),
                html.P("กลุ่มลูกค้าที่ทำนายได้", style={"opacity":"0.85"}),
            ], className="predict-result mb-3", style={"background":f"linear-gradient(135deg, {color}, #C8860A)"}),

            # Probability bars
            dbc.Card(dbc.CardBody([
                html.H6("ความน่าจะเป็นแต่ละกลุ่ม", className="fw-bold mb-3", style={"color":"#6F4E37"}),
                *[html.Div([
                    html.Div(f"{lbl}  {p*100:.1f}%",
                             style={"fontSize":"13px","marginBottom":"4px","fontWeight":"600" if lbl==segment else "400"}),
                    dbc.Progress(value=round(p*100,1), max=100,
                                 style={"height":"18px","marginBottom":"10px"},
                                 color="warning" if lbl==segment else "secondary"),
                ]) for lbl, p in zip(labels, proba)],
            ]), className="chart-card mb-3"),

            # Campaign recommendation
            dbc.Card(dbc.CardBody([
                html.H6("💡 Campaign Recommendation", className="fw-bold mb-2", style={"color":"#6F4E37"}),
                html.P(rec, style={"fontSize":"14px","margin":"0"}),
            ]), className="chart-card"),
        ])

    except Exception as e:
        return dbc.Alert(f"❌ เกิดข้อผิดพลาด: {str(e)}", color="danger")
```

---

## สิ่งที่ต้องติดตั้ง

```bash
pip install dash dash-bootstrap-components pandas numpy joblib scikit-learn xgboost
```

## รันโปรเจค

```bash
python app.py
# เปิด http://localhost:8050
```

## Checklist

- [ ] จัดโครงสร้างไฟล์ตาม folder structure ด้านบน
- [ ] สร้าง `app.py`
- [ ] สร้าง `assets/style.css`
- [ ] สร้าง `pages/home.py`
- [ ] สร้าง `pages/unsupervised.py`
- [ ] สร้าง `pages/business_insight.py`
- [ ] สร้าง `pages/supervised.py`
- [ ] รันแล้วทดสอบ Navbar ทั้ง 4 หน้า
- [ ] ทดสอบ Predict บนหน้า Supervised
