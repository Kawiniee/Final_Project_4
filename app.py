import dash
import dash_bootstrap_components as dbc
from dash import html


app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap",
    ],
    suppress_callback_exceptions=True,
)

server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("🏠 Home", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("🔍 Unsupervised Learning", href="/unsupervised", active="exact")),
        dbc.NavItem(dbc.NavLink("📈 Business Insight", href="/business-insight", active="exact")),
        dbc.NavItem(dbc.NavLink("🎯 Supervised Learning", href="/supervised", active="exact")),
    ],
    brand="☕ AI-Driven Marketing Campaign",
    brand_href="/",
    color="#6F4E37",
    dark=True,
)

app.layout = html.Div([
    navbar,
    dash.page_container,
])


if __name__ == "__main__":
    app.run(debug=False, dev_tools_ui=False)
