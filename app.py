from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("output.csv")
df["date"] = pd.to_datetime(df["date"])

app = Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Soul Foods — Sales Visualiser</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
        <style>
            *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                background-color: #0d0d0d;
                color: #f0ece2;
                font-family: "DM Mono", monospace;
                min-height: 100vh;
                overflow-x: hidden;
            }

            /* Grain overlay */
            body::before {
                content: "";
                position: fixed;
                inset: 0;
                background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
                pointer-events: none;
                z-index: 999;
                opacity: 0.35;
            }

            .wrapper {
                max-width: 1100px;
                margin: 0 auto;
                padding: 60px 40px 80px;
            }

            /* Header */
            .header {
                display: flex;
                align-items: flex-end;
                justify-content: space-between;
                border-bottom: 1px solid #2a2a2a;
                padding-bottom: 28px;
                margin-bottom: 48px;
            }

            .brand-block {}

            .brand-eyebrow {
                font-family: "DM Mono", monospace;
                font-size: 10px;
                font-weight: 400;
                letter-spacing: 0.25em;
                text-transform: uppercase;
                color: #e8462a;
                margin-bottom: 8px;
            }

            .brand-title {
                font-family: "Playfair Display", serif;
                font-size: clamp(28px, 4vw, 48px);
                font-weight: 900;
                line-height: 1.05;
                color: #f0ece2;
                letter-spacing: -0.02em;
            }

            .brand-title span {
                color: #e8462a;
            }

            .header-meta {
                font-size: 10px;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                color: #3d3d3d;
                text-align: right;
                line-height: 1.8;
            }

            /* Filter bar */
            .filter-section {
                display: flex;
                align-items: center;
                gap: 32px;
                margin-bottom: 36px;
                flex-wrap: wrap;
            }

            .filter-label {
                font-size: 10px;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                color: #555;
                flex-shrink: 0;
            }

            /* Radio button overrides */
            .region-radio .dash-radioitems {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }

            .region-radio label {
                font-family: "DM Mono", monospace;
                font-size: 11px;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                cursor: pointer;
                padding: 8px 18px;
                border: 1px solid #2a2a2a;
                border-radius: 2px;
                color: #777;
                transition: all 0.18s ease;
                user-select: none;
                background: transparent;
            }

            .region-radio label:hover {
                border-color: #e8462a;
                color: #e8462a;
            }

            .region-radio input[type="radio"] {
                display: none;
            }

            .region-radio input[type="radio"]:checked + label {
                background-color: #e8462a;
                border-color: #e8462a;
                color: #0d0d0d;
                font-weight: 500;
            }

            /* Chart container */
            .chart-container {
                background: #111;
                border: 1px solid #1e1e1e;
                border-radius: 4px;
                padding: 8px;
                position: relative;
                overflow: hidden;
            }

            .chart-container::before {
                content: "";
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 2px;
                background: linear-gradient(90deg, #e8462a 0%, transparent 60%);
            }

            /* Footer rule */
            .footer {
                margin-top: 48px;
                padding-top: 20px;
                border-top: 1px solid #1e1e1e;
                font-size: 10px;
                letter-spacing: 0.15em;
                text-transform: uppercase;
                color: #2e2e2e;
                display: flex;
                justify-content: space-between;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(
    className="wrapper",
    children=[
        # Header
        html.Div(
            className="header",
            children=[
                html.Div(
                    className="brand-block",
                    children=[
                        html.P("Soul Foods Co. — Analytics", className="brand-eyebrow"),
                        html.H1(
                            ["Pink Morsel ", html.Span("Sales"), " Visualiser"],
                            className="brand-title"
                        ),
                    ]
                ),
                html.Div(
                    ["Daily Sales Trend", html.Br(), "Regional Breakdown"],
                    className="header-meta"
                )
            ]
        ),

        # Filter bar
        html.Div(
            className="filter-section",
            children=[
                html.Span("Filter by region", className="filter-label"),
                html.Div(
                    className="region-radio",
                    children=[
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "South", "value": "south"},
                                {"label": "East", "value": "east"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            inputStyle={"display": "none"},
                            labelStyle={
                                "fontFamily": "'DM Mono', monospace",
                                "fontSize": "11px",
                                "letterSpacing": "0.12em",
                                "textTransform": "uppercase",
                                "cursor": "pointer",
                                "padding": "8px 18px",
                                "border": "1px solid #2a2a2a",
                                "borderRadius": "2px",
                                "color": "#777",
                                "marginRight": "8px",
                                "display": "inline-block",
                                "transition": "all 0.18s ease",
                            }
                        )
                    ]
                )
            ]
        ),

        # Chart
        html.Div(
            className="chart-container",
            children=[dcc.Graph(id="sales-graph")]
        ),

        # Footer
        html.Div(
            className="footer",
            children=[
                html.Span("Soul Foods Pink Morsel — Internal Dashboard"),
                html.Span("Data: output.csv")
            ]
        )
    ]
)


@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    daily_sales = (
        filtered_df.groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
    )

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title=f"Sales Trend — {selected_region.title()}"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0d0d0d",
        font=dict(family="DM Mono, monospace", color="#666", size=11),
        title=dict(
            font=dict(family="Playfair Display, serif", size=20, color="#f0ece2"),
            x=0.03,
            y=0.96,
        ),
        xaxis=dict(
            gridcolor="#1c1c1c",
            linecolor="#2a2a2a",
            tickcolor="#2a2a2a",
            tickfont=dict(size=10, color="#555"),
            title_font=dict(size=10, color="#555"),
        ),
        yaxis=dict(
            gridcolor="#1c1c1c",
            linecolor="#2a2a2a",
            tickcolor="#2a2a2a",
            tickfont=dict(size=10, color="#555"),
            title_font=dict(size=10, color="#555"),
        ),
        margin=dict(l=56, r=32, t=64, b=48),
    )

    fig.update_traces(
        line=dict(color="#e8462a", width=2),
        mode="lines",
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)