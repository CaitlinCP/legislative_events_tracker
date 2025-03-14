import webbrowser
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc

# ---------------------------- Init App ---------------------------------------
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True
)
app.title = "Legislative Events Tracker"

# ---------------------------- Define Layout ----------------------------------
app.layout = dbc.Container(
    [
        dcc.Tabs(
            id="tabs",
            value="landing",
            children=[
                dcc.Tab(label="About", value="landing"),
                dcc.Tab(label="Explore", value="explore"),
                dcc.Tab(label="Considerations", value="considerations"),
            ],
        ),
        html.Div(id="tabs-content"),
    ],
    fluid=True,
)

# Home Page Layout
landing_page = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Legislative Events Tracker", className="text-center display-3 fw-bold mb-4"),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.P("Description", className="lead text-center"),
                width=10,
                className="mx-auto",
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H3(" ", className="mt-5 text-center fw-semibold"),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H3(" ", className="mt-5 text-center fw-semibold"),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div([dcc.Markdown("Instructins", dangerously_allow_html=True)])
            )
        ),
    ],
    fluid=True,
    className="py-5",
)
# Explore Page Layout
explore_page = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Legislative Events Traker", className="text-center display-4 fw-bold mb-4"),
                width=12,
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Label("State:", className="fw-semibold"),
                                dcc.Input(
                                    id="state-input",
                                    type="text",
                                    placeholder="Enter your State",
                                    value=" ",
                                    className="form-control",
                                ),
                            ]
                        ),
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Label("Start date:", className="fw-semibold"),
                                dcc.Input(
                                    id="start_date",
                                    type="text",
                                    placeholder="Start date",
                                    value="03-14-2025",
                                    className="form-control",
                                ),
                            ]
                        ),
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Label("End date:", className="fw-semibold"),
                                dcc.Input(
                                    id="end_date",
                                    type="text",
                                    placeholder="End date",
                                    value="04-13-2025",
                                    className="form-control",
                                ),
                            ]
                        ),
                    ),
                    width=4,
                ),
            ],
            className="justify-content-center mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(dcc.Graph(id="events_table")),
                        className="shadow",
                    ),
                    width=12,
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
    className="py-5",
)

# Considerations Page Layout
considerations_page = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Considerations", className="text-center display-4 fw-bold mb-4"),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H3("Data Sources", className="mt-4 fw-semibold"),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.P("Data Sources", className="text-muted"),
                width=10,
                className="mx-auto",
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H3("GitHub Repository", className="mt-4 fw-semibold"),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.A("repo_str", href="#", target="_blank", className="btn btn-primary"),
                width=12,
                className="text-center",
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H3("Authors & Acknowledgements", className="mt-4 fw-semibold"),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.P("authors_str", className="text-muted"),
                width=10,
                className="mx-auto",
            )
        ),
    ],
    fluid=True,
    className="py-5",
)

# ---------------------------- App Callbacks ----------------------------------
# Update page content based on selected tab
@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value"),
    suppress_callback_exceptions=True,
)
def update_tab(tab_name):
    if tab_name == "landing":
        return landing_page
    elif tab_name == "explore":
        return explore_page
    elif tab_name == "considerations":
        return considerations_page

# Run application on web browser
if __name__ == "__main__":
    port = 8050
    url = f"http://127.0.0.1:{port}/"
    print(f"Running on {url}")
    webbrowser.open(url, new=2)
    app.run_server(debug=True, port=port)