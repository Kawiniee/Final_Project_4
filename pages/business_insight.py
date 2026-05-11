import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/business-insight", name="Business Insight")


def insight_block(num, title, img_path, insight):
    return dbc.Card(dbc.CardBody([
        html.H5(f"กราฟที่ {num}: {title}", className="chart-title"),
        dbc.Row([
            dbc.Col(
                html.Div(html.Img(src=img_path, className="chart-image"), className="chart-image-frame"),
                lg=7,
            ),
            dbc.Col(
                html.Div([html.Strong("📌 Insight"), html.Div(insight)], className="insight-side"),
                lg=5,
            ),
        ], className="chart-layout g-3"),
    ]), className="chart-card")


layout = html.Div([
    html.H2("📈 Business Insight", className="section-title"),
    html.P("วิเคราะห์พฤติกรรมผู้บริโภคและช่องทางสื่อสำหรับ RTD Campaign", className="text-muted mb-4"),

    insight_block(
        1,
        "สัดส่วนช่องทางที่มีอิทธิพลต่อการตัดสินใจซื้อ",
        "/assets/charts/bi_donut_influence.png",
        "โซเชียลมีเดียมีอิทธิพลสูงสุดต่อการตัดสินใจซื้อ รองลงมาคือแพลตฟอร์มวิดีโอ สอดคล้องกับพฤติกรรม digital-first ของกลุ่มเป้าหมายอายุ 23-29 ปี — ควรเน้น budget บน Digital Channel เป็นหลัก",
    ),

    insight_block(
        2,
        "จำนวนผู้ได้รับอิทธิพลจากโฆษณาแต่ละช่องทาง",
        "/assets/charts/bi_bar_influence.png",
        "ช่องทาง Online ครองสัดส่วนมากกว่า 70% ของการรับรู้โฆษณา สื่อ Offline อย่างบิลบอร์ดและรถไฟฟ้ามีผลน้อยกว่ามาก — Digital Marketing คือ channel หลักที่ควร allocate budget",
    ),

    insight_block(
        3,
        "แพลตฟอร์มที่ใช้งานประจำ แบ่งตามกลุ่มลูกค้า",
        "/assets/charts/bi_platform_by_cluster.png",
        "กลุ่มชอบทั้งกาแฟและชา นิยม LINE มากที่สุด ส่วนกลุ่มชอบกาแฟและชอบชา กระจายตัวบน Facebook และ Instagram — ใช้ข้อมูลนี้ทำ platform targeting แยกตาม segment ได้โดยตรง",
    ),

    insight_block(
        4,
        "พฤติกรรมการใช้สื่อช่วงเทศกาลสงกรานต์",
        "/assets/charts/bi_festival_behavior.png",
        "ลูกค้าส่วนใหญ่ทุกกลุ่มใช้โซเชียลมีเดียมากขึ้นช่วงสงกรานต์ — นี่คือโอกาสสำคัญในการ launch RTD campaign ช่วงเทศกาล เพราะ reach และ engagement สูงกว่าปกติ",
    ),

    html.H4("💡 Strategic Recommendations", className="section-title mt-2"),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("☕", style={"fontSize": "32px", "textAlign": "center"}),
            html.H5("ชอบกาแฟ", className="text-center fw-bold"),
            html.P("📱 Facebook / Instagram", className="text-center"),
            html.P("⏰ 18.00 – 21.59 น.", className="text-center"),
            html.P("🎯 'กาแฟสดในขวด รสชาติเหมือนร้าน พกพาได้ทุกที่'", className="text-center", style={"fontSize": "13px"}),
        ]), style={"borderTop": "4px solid #6F4E37", "backgroundColor": "#FFF8F0", "borderRadius": "12px"}), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("🍵☕", style={"fontSize": "32px", "textAlign": "center"}),
            html.H5("ชอบทั้งกาแฟและชา", className="text-center fw-bold"),
            html.P("📱 LINE", className="text-center"),
            html.P("⏰ 18.00 – 21.59 น.", className="text-center"),
            html.P("🎯 'ครบทุกอารมณ์ ทั้งกาแฟและชา เลือกได้ตามวัน'", className="text-center", style={"fontSize": "13px"}),
        ]), style={"borderTop": "4px solid #21cdb6", "backgroundColor": "#FFF8F0", "borderRadius": "12px"}), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.Div("🍵", style={"fontSize": "32px", "textAlign": "center"}),
            html.H5("ชอบชา", className="text-center fw-bold"),
            html.P("📱 Facebook", className="text-center"),
            html.P("⏰ 18.00 – 21.59 น.", className="text-center"),
            html.P("🎯 'ชาพรีเมียม ไม่มีน้ำตาล — Healthy Choice ของคนรักชา'", className="text-center", style={"fontSize": "13px"}),
        ]), style={"borderTop": "4px solid #8f8f8f", "backgroundColor": "#FFF8F0", "borderRadius": "12px"}), md=4),
    ], className="g-3"),
], className="page-wrapper")
