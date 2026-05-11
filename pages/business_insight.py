import dash
from dash import html
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/business-insight", name="Business Insight")


def insight_content(points, takeaway):
    return html.Div([
        html.Div("Key Insights", className="insight-heading"),
        html.Div([
            html.Div([
                html.Span(label, className="insight-label"),
                html.Span(text, className="insight-text"),
            ], className="insight-point")
            for label, text in points
        ]),
        html.Div([
            html.Div("Strategic Takeaway", className="takeaway-title"),
            html.Div(takeaway, className="takeaway-text"),
        ], className="takeaway-box"),
    ])


def insight_block(num, title, img_path, insight):
    return dbc.Card(dbc.CardBody([
        html.H5(f"กราฟที่ {num}: {title}", className="chart-title"),
        dbc.Row([
            dbc.Col(
                html.Div(html.Img(src=img_path, className="chart-image"), className="chart-image-frame"),
                lg=7,
            ),
            dbc.Col(
                html.Div(insight, className="insight-side insight-panel"),
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
        insight_content(
            [
                ("โซเชียลมีเดีย:", "ครองอันดับ 1 (40.2%) เป็นช่องทางหลักที่ influence ลูกค้าทุกกลุ่ม"),
                ("แพลตฟอร์มวิดีโอ:", "อันดับ 2 (15.8%) สะท้อนพลังของ Visual Content"),
                ("โทรทัศน์:", "ยังคงมีบทบาท (12.1%) แต่ถูก Digital เข้ามาแทนที่มากขึ้น"),
                ("สื่อ ณ จุดขาย:", "แม้สัดส่วนน้อย (11.1%) แต่สำคัญมากในขั้นตอนตัดสินใจสุดท้าย"),
            ],
            "เน้นลงทุนใน Social + Video Content เพื่อประสิทธิภาพสูงสุดในการกระตุ้นยอดขาย",
        ),
    ),

    insight_block(
        2,
        "จำนวนผู้ได้รับอิทธิพลจากโฆษณาแต่ละช่องทาง",
        "/assets/charts/bi_bar_influence.png",
        insight_content(
            [
                ("โซเชียลมีเดียมีอิทธิพลสูงสุด:", "มีผู้ได้รับอิทธิพลกว่า 130 คน นำหน้าสื่ออื่นๆ อย่างชัดเจน"),
                ("วิดีโอ & โทรทัศน์:", "เป็นช่องทางรองที่สำคัญ (39-51 คน) สะท้อนความสำคัญของสื่อภาพเคลื่อนไหว"),
                ("สื่อสิ่งพิมพ์ถดถอย:", "หนังสือพิมพ์และนิตยสารมีอิทธิพลน้อยที่สุด (11-17 คน)"),
            ],
            "เน้นทำ Creative Content บน Social Media และ Video Platform เป็นหลักเพื่อ Impact สูงสุด",
        ),
    ),

    insight_block(
        3,
        "แพลตฟอร์มที่ใช้งานประจำ แบ่งตามกลุ่มลูกค้า",
        "/assets/charts/bi_platform_by_cluster.png",
        insight_content(
            [
                ("กลุ่ม Both Lovers (52%):", "กระจายตัวทุกแพลตฟอร์ม เป็นกลุ่ม Mass ที่เข้าถึงง่ายที่สุด"),
                ("กลุ่ม Coffee Lovers:", "มีแนวโน้มใช้ Facebook และ Instagram เพื่อติดตามคอนเทนต์เฉพาะกลุ่ม"),
                ("กลุ่ม Tea Lovers:", "เน้นแพลตฟอร์มด้าน Health & Lifestyle Content เป็นหลัก"),
            ],
            "ทำ Targeted Ad แยกตาม Cluster และแพลตฟอร์มที่กลุ่มนั้น Active ไม่ควรใช้แบบ One-size-fits-all",
        ),
    ),

    insight_block(
        4,
        "พฤติกรรมการใช้สื่อช่วงเทศกาลสงกรานต์",
        "/assets/charts/bi_festival_behavior.png",
        insight_content(
            [
                ("พฤติกรรมรวม:", "ลูกค้าส่วนใหญ่ทุก Cluster ใช้สื่อ \"เท่าเดิมหรือมากขึ้น\" ไม่มี Drop-off"),
                ("กลุ่ม Both Lovers:", "ใช้สื่อเพิ่มขึ้นมากที่สุด เป็นโอกาสทองในการทำ Campaign"),
                ("กลุ่ม Tea Lovers:", "แนวโน้มใช้ \"เท่าเดิม\" สูง ต้องใช้ Creative ที่โดดเด่นเพื่อดึงดูด"),
            ],
            "ไม่ควรหยุด Ads ช่วงสงกรานต์ — เพิ่ม Budget และเน้น Seasonal Campaign เป็นพิเศษ",
        ),
    ),
], className="page-wrapper")
