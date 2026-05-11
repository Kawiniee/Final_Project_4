import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd


dash.register_page(__name__, path="/", name="Home")

df = pd.read_csv("data/cleaned_data.csv")

n_customers = len(df)
n_clusters = 3
test_accuracy = "94.12%"
top_cluster = df["Cluster_ID"].value_counts().idxmax()
cluster_counts = df["Cluster_ID"].value_counts()


def cluster_percent(cluster_name):
    return f"{cluster_counts.get(cluster_name, 0) / n_customers * 100:.1f}%"


layout = html.Div([
    html.Section([
        dbc.Row([
            dbc.Col([
                html.Div("RTD Customer Intelligence Dashboard", className="eyebrow"),
                html.H1("☕ AI-Driven Marketing Campaign System", className="home-title"),
                html.P(
                    "ระบบวิเคราะห์กลุ่มลูกค้าและแนะนำแคมเปญสำหรับตลาด Ready-to-Drink โดยเชื่อมผลจาก K-Means, Business Insight และ XGBoost ไว้ใน dashboard เดียว",
                    className="home-subtitle",
                ),
            ], lg=8),
            dbc.Col([
                html.Div([
                    html.Div("Top Segment", className="mini-label"),
                    html.Div(top_cluster, className="mini-value"),
                    html.Div("กลุ่มที่มีสัดส่วนมากที่สุดในชุดข้อมูล", className="mini-note"),
                ], className="hero-summary"),
            ], lg=4),
        ], className="align-items-center g-4"),
    ], className="home-hero"),

    dbc.Row([
        dbc.Col(html.Div([html.Div(f"{n_customers}", className="kpi-number"), html.Div("จำนวนลูกค้าทั้งหมด", className="kpi-label")], className="kpi-card"), md=3),
        dbc.Col(html.Div([html.Div(f"{n_clusters}", className="kpi-number"), html.Div("จำนวน Cluster", className="kpi-label")], className="kpi-card"), md=3),
        dbc.Col(html.Div([html.Div(test_accuracy, className="kpi-number"), html.Div("Test Accuracy (XGBoost)", className="kpi-label")], className="kpi-card"), md=3),
        dbc.Col(html.Div([html.Div(cluster_percent(top_cluster), className="kpi-number"), html.Div("สัดส่วนกลุ่มหลัก", className="kpi-label")], className="kpi-card"), md=3),
    ], className="g-3 mb-4"),

    dbc.Row([
        dbc.Col([
            html.H4("ภาพรวมระบบ", className="section-title"),
            html.Div([
                html.Div([
                    html.Div(step, className="flow-step"),
                ]) for i, step in enumerate(["Survey Data", "→", "Data Cleaning", "→", "K-Means", "→", "XGBoost", "→", "Dashboard"])
            ], className="flow-card"),
        ], lg=7),

        dbc.Col([
            html.H4("สิ่งที่ระบบช่วยตัดสินใจ", className="section-title"),
            html.Div([
                html.Div([html.Div("1", className="point-number"), html.Div([html.H6("เข้าใจ segment", className="point-title"), html.P("แบ่งกลุ่มลูกค้าตามพฤติกรรมและความชอบกาแฟ/ชา RTD", className="point-text")])], className="decision-point"),
                html.Div([html.Div("2", className="point-number"), html.Div([html.H6("เลือกช่องทางสื่อ", className="point-title"), html.P("ใช้ insight จากแพลตฟอร์มและพฤติกรรมช่วงเทศกาลเพื่อจัดงบแคมเปญ", className="point-text")])], className="decision-point"),
                html.Div([html.Div("3", className="point-number"), html.Div([html.H6("ทำนายลูกค้าใหม่", className="point-title"), html.P("กรอกข้อมูลพฤติกรรมแล้วรับผล segment พร้อมคำแนะนำ campaign", className="point-text")])], className="decision-point"),
            ], className="soft-panel"),
        ], lg=5),
    ], className="g-4 mb-4"),

    html.H4("Model Performance Summary", className="section-title"),
    dbc.Row([
        dbc.Col(html.Div([html.Div("96.23%", className="metric-value"), html.Div("Train Accuracy", className="metric-label")], className="metric-card"), md=4),
        dbc.Col(html.Div([html.Div("94.12%", className="metric-value"), html.Div("Test Accuracy", className="metric-label")], className="metric-card metric-card-primary"), md=4),
        dbc.Col(html.Div([html.Div("92.45%", className="metric-value"), html.Div("Cross-val Accuracy (±3.41%)", className="metric-label")], className="metric-card"), md=4),
    ], className="g-3 mb-4"),

    html.H4("Customer Segments", className="section-title"),
    dbc.Row([
        dbc.Col(html.Div([
            html.Div("☕", className="segment-icon"),
            html.H5("ชอบกาแฟ", className="segment-title"),
            html.P("เน้นกลิ่นหอม รสชาติสด และความรู้สึกเหมือนกาแฟร้าน", className="segment-text"),
            html.Div(cluster_percent("ชอบกาแฟ"), className="segment-share"),
        ], className="segment-card coffee"), md=4),
        dbc.Col(html.Div([
            html.Div("🍵☕", className="segment-icon"),
            html.H5("ชอบทั้งกาแฟและชา", className="segment-title"),
            html.P("ตอบรับ variety และ lifestyle message ได้ดี เหมาะกับแคมเปญหลายรสชาติ", className="segment-text"),
            html.Div(cluster_percent("ชอบทั้งกาแฟและชา"), className="segment-share"),
        ], className="segment-card both"), md=4),
        dbc.Col(html.Div([
            html.Div("🍵", className="segment-icon"),
            html.H5("ชอบชา", className="segment-title"),
            html.P("สนใจความหอมของชา ทางเลือกสุขภาพ และสูตรน้ำตาลน้อย", className="segment-text"),
            html.Div(cluster_percent("ชอบชา"), className="segment-share"),
        ], className="segment-card tea"), md=4),
    ], className="g-3"),
], className="page-wrapper")
