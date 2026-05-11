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


layout = html.Div([
    html.H2("🔍 Unsupervised Learning", className="section-title"),
    html.P("การวิเคราะห์และแบ่งกลุ่มลูกค้าด้วย K-Means Clustering", className="text-muted mb-4"),

    dbc.Tabs([
        dbc.Tab(label="📊 Correlation Analysis", tab_id="corr", children=[html.Br(),
            chart_block(
                "Correlation Heatmap — Coffee & Tea Features",
                "/assets/charts/unsup_correlation.png",
                "ความสัมพันธ์ภายในกลุ่มกาแฟ (C_*) และกลุ่มชา (T_*) มีค่าสูง แสดงว่าผู้ที่ให้ความสำคัญกับคุณสมบัติหนึ่งมักให้ความสำคัญกับคุณสมบัติอื่นในกลุ่มเดียวกัน ในขณะที่ความสัมพันธ์ข้ามกลุ่มมีค่าต่ำ บ่งบอกว่าความชอบกาแฟและชา RTD เป็นอิสระต่อกัน สามารถแบ่ง segment ได้ชัดเจน",
            ),
        ]),

        dbc.Tab(label="📉 Elbow & Silhouette", tab_id="elbow", children=[html.Br(),
            chart_block(
                "Elbow Method & Silhouette Score",
                "/assets/charts/unsup_elbow_silhouette.png",
                "Elbow Method พบจุดหักศอกที่ K=3 และ Silhouette Score สูงสุดที่ K=3 เช่นกัน ยืนยันว่าการแบ่ง 3 กลุ่มเหมาะสมที่สุดสำหรับข้อมูลชุดนี้",
            ),
        ]),

        dbc.Tab(label="🗺️ PCA Scatter", tab_id="pca", children=[html.Br(),
            chart_block(
                "Customer Segmentation — PCA 2D",
                "/assets/charts/unsup_pca_scatter.png",
                "ทั้ง 3 กลุ่มมีการกระจายตัวแยกออกจากกันค่อนข้างชัดเจนใน 2 มิติหลัก แสดงว่าโมเดล K-Means สามารถแบ่งกลุ่มลูกค้าได้อย่างมีความหมาย กลุ่มชอบกาแฟและชอบชาอยู่คนละด้าน ส่วนกลุ่มชอบทั้งสองอยู่ตรงกลาง",
            ),
        ]),

        dbc.Tab(label="🔥 Cluster Profiling", tab_id="heatmap", children=[html.Br(),
            chart_block(
                "Cluster Profiling Heatmap — Mean Score ของแต่ละกลุ่ม",
                "/assets/charts/unsup_cluster_heatmap.png",
                "กลุ่มชอบกาแฟ: คะแนนสูงที่ C_Aroma และ C_Fresh_Taste | กลุ่มชอบชา: คะแนนสูงที่ T_Aroma และ T_No_Sugar | กลุ่มชอบทั้งสอง: คะแนนสูงทั้งสองด้าน ข้อมูลนี้ใช้ออกแบบ creative ของ campaign แต่ละกลุ่มได้โดยตรง",
            ),
        ]),

        dbc.Tab(label="👤 Customer Persona", tab_id="persona", children=[html.Br(),
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("☕", style={"fontSize": "48px", "textAlign": "center"}),
                    html.H4("ชอบกาแฟ", className="text-center mt-2 fw-bold"),
                    html.Hr(),
                    html.P("ให้ความสำคัญกับกลิ่นหอมและรสชาติสดของกาแฟ ไม่ค่อยสนใจชา RTD"),
                    html.P("🏆 Top: C_Aroma, C_Fresh_Taste, C_Alert"),
                    html.Div("💡 Facebook/Instagram | 18.00-21.59 น. | 'กาแฟสดในขวด รสชาติเหมือนร้าน'", className="insight-box"),
                ]), className="persona-card", style={"borderTop": "4px solid #6F4E37"}), md=4),

                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("🍵☕", style={"fontSize": "48px", "textAlign": "center"}),
                    html.H4("ชอบทั้งกาแฟและชา", className="text-center mt-2 fw-bold"),
                    html.Hr(),
                    html.P("ให้ความสำคัญทั้งสองด้านสูง ชอบ variety และ lifestyle"),
                    html.P("🏆 Top: C_Aroma, T_Aroma, T_Portable"),
                    html.Div("💡 LINE | 18.00-21.59 น. | 'ครบทุกอารมณ์ ทั้งกาแฟและชา'", className="insight-box"),
                ]), className="persona-card", style={"borderTop": "4px solid #21cdb6"}), md=4),

                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("🍵", style={"fontSize": "48px", "textAlign": "center"}),
                    html.H4("ชอบชา", className="text-center mt-2 fw-bold"),
                    html.Hr(),
                    html.P("ให้ความสำคัญกับชาเป็นหลัก ชอบไม่หวาน พกพาสะดวก"),
                    html.P("🏆 Top: T_Aroma, T_No_Sugar, T_Intense"),
                    html.Div("💡 Facebook | 18.00-21.59 น. | 'ชาพรีเมียม ไม่มีน้ำตาล Healthy Choice'", className="insight-box"),
                ]), className="persona-card", style={"borderTop": "4px solid #8f8f8f"}), md=4),
            ]),
        ]),
    ], id="unsup-tabs", active_tab="corr"),
], className="page-wrapper")
