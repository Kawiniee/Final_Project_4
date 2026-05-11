import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/unsupervised", name="Unsupervised Learning")


def chart_block(title, img_path, insight):
    return dbc.Card(dbc.CardBody([
        html.H5(title, className="chart-title"),
        dbc.Row([
            dbc.Col(
                html.Div(html.Img(src=img_path, className="chart-image"), className="chart-image-frame"),
                lg=8,
            ),
            dbc.Col(
                html.Div([html.Strong("📌 คำอธิบาย"), html.Div(insight)], className="insight-side"),
                lg=4,
            ),
        ], className="chart-layout g-3"),
    ]), className="chart-card")


def chart_block_with_cards(title, img_path, insight_cards):
    return dbc.Card(dbc.CardBody([
        html.H5(title, className="chart-title"),
        dbc.Row([
            dbc.Col(
                html.Div(html.Img(src=img_path, className="chart-image"), className="chart-image-frame"),
                lg=8,
            ),
            dbc.Col([
                html.Div([
                    html.Strong(card_title),
                    html.Div(card_text),
                ], className="insight-side mb-3")
                for card_title, card_text in insight_cards
            ], lg=4),
        ], className="chart-layout g-3"),
    ]), className="chart-card")


def chart_only_block(title, img_path):
    return dbc.Card(dbc.CardBody([
        html.H5(title, className="chart-title"),
        html.Div(html.Img(src=img_path, className="chart-image"), className="chart-image-frame"),
    ]), className="chart-card")


persona_section = dbc.Row([
    dbc.Col(dbc.Card(dbc.CardBody([
        html.Div("☕", style={"fontSize": "48px", "textAlign": "center"}),
        html.H4("ชอบกาแฟ", className="text-center mt-2 fw-bold"),
        html.Hr(),
        html.P("ให้ความสำคัญกับกลิ่นหอมและรสชาติสดของกาแฟ ไม่ค่อยสนใจชา RTD"),
    ]), className="persona-card", style={"borderTop": "4px solid #6F4E37"}), md=4),

    dbc.Col(dbc.Card(dbc.CardBody([
        html.Div("🍵☕", style={"fontSize": "48px", "textAlign": "center"}),
        html.H4("ชอบทั้งกาแฟและชา", className="text-center mt-2 fw-bold"),
        html.Hr(),
        html.P("ให้ความสำคัญทั้งสองด้านสูง ชอบ variety และ lifestyle"),
    ]), className="persona-card", style={"borderTop": "4px solid #21cdb6"}), md=4),

    dbc.Col(dbc.Card(dbc.CardBody([
        html.Div("🍵", style={"fontSize": "48px", "textAlign": "center"}),
        html.H4("ชอบชา", className="text-center mt-2 fw-bold"),
        html.Hr(),
        html.P("ให้ความสำคัญกับชาเป็นหลัก ชอบไม่หวาน พกพาสะดวก"),
    ]), className="persona-card", style={"borderTop": "4px solid #8f8f8f"}), md=4),
], className="g-3")


layout = html.Div([
    html.H2("🔍 Unsupervised Learning", className="section-title"),
    html.P("การวิเคราะห์และแบ่งกลุ่มลูกค้าด้วย K-Means Clustering", className="text-muted mb-4"),

    dbc.Tabs([
        dbc.Tab(label="📊 Correlation Analysis", tab_id="corr", children=[html.Br(),
            chart_block(
                "Correlation Heatmap — Coffee & Tea Features",
                "/assets/charts/unsup_correlation.png",
                html.Div([
                    html.Strong("ความสัมพันธ์ภายในกลุ่ม:"),
                    html.Div("ไม่ว่าจะชาหรือกาแฟก็มักจะมีความสัมพันธ์ภายในกลุ่มอยู่ในระดับที่สูง"),
                    html.Br(),
                    html.Strong("ความสัมพันธ์ข้ามผลิตภัณฑ์:"),
                    html.Div("ความสัมพันธ์ของกาแฟและชาค่อนข้างเป็นอิสระต่อกัน"),
                ]),
            ),
        ]),

        dbc.Tab(label="📉 Elbow & Silhouette", tab_id="elbow", children=[html.Br(),
            chart_block_with_cards(
                "Elbow Method & Silhouette Score",
                "/assets/charts/unsup_elbow_silhouette.png",
                [
                    (
                        "Elbow Method",
                        "จุดหักศอก (Elbow Point) อยู่ที่ k = 3 ซึ่งเป็นจุดที่ความชันเริ่มลดลงอย่างเห็นได้ชัด",
                    ),
                    (
                        "Silhouette Analysis",
                        "ค่า Silhouette Score ที่เข้าใกล้ 1 มากที่สุดอยู่ที่ k = 3 ยืนยันความเหมาะสมในการจัดกลุ่ม",
                    ),
                ],
            ),
        ]),

        dbc.Tab(label="🗺️ PCA Scatter", tab_id="pca", children=[html.Br(),
            chart_block(
                "Customer Segmentation — PCA 2D",
                "/assets/charts/unsup_pca_scatter.png",
                html.Div([
                    html.Strong("การวิเคราะห์การจัดกลุ่ม:"),
                    html.Div("ข้อมูลในแต่ละกลุ่มมีการกระจายตัวและแยกออกจากกันได้ค่อนข้างชัดเจน"),
                    html.Div("จุดศูนย์กลางของแต่ละกลุ่มอยู่ห่างกันพอสมควร ช่วยให้ระบุลักษณะเฉพาะของกลุ่มลูกค้าได้ง่าย"),
                ]),
            ),
        ]),

        dbc.Tab(label="🔥 Cluster Profiling", tab_id="heatmap", children=[html.Br(),
            chart_only_block(
                "Cluster Profiling Heatmap — Mean Score ของแต่ละกลุ่ม",
                "/assets/charts/unsup_cluster_heatmap.png",
            ),
            html.H4("👤 Customer Persona", className="section-title mt-4"),
            persona_section,
        ]),
    ], id="unsup-tabs", active_tab="corr"),
], className="page-wrapper")
