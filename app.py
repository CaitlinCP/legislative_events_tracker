import webbrowser
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from utils_app import description, instructions_str

# ---------------------------- Init App ---------------------------------------
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True
)
app.title = "Legislative Events Tracker"

def pull_data(state, start_date, end_date):
    # Mock function to return event data
    return [
        {"name": "Hearing on Education Reform", "committee": "Education", "description": "Discussion on new education policies", "start_date": "03-20-2025", "bill_data": "HB1234", "location": "State Capitol"},
        {"name": "Budget Planning Session", "committee": "Finance", "description": "Review of budget proposals", "start_date": "03-25-2025", "bill_data": "SB5678", "location": "State Capitol"},
    ]

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
                html.P(description, className="lead text-center"),
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
                html.Div([dcc.Markdown(instructions_str, dangerously_allow_html=True)])
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
                html.H1("Legislative Events Tracker", className="text-center display-4 fw-bold mb-4"),
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
                                dcc.Dropdown(['Texas', 'California', 'Colorado'], id="state"),
                            ]
                        ),
                    ),
                    width=2,
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
                                    value="2025-03-14",
                                    className="form-control",
                                ),
                            ]
                        ),
                    ),
                    width=2,
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
                                    value="2025-04-13",
                                    className="form-control",
                                ),
                            ]
                        ),
                    ),
                    width=2,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Label(" ", className="fw-semibold"),
                                dbc.Button("Submit", id="submit-val", n_clicks=0, color="primary", className="w-100 fw-bold"),
                            ]
                        ),
                    ),
                    width=2,
                ),
            ],
            className="justify-content-center mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dash_table.DataTable(
                                id="events_table",
                                columns=[
                                    {"name": col, "id": col} for col in [
                                        "name", "committee", "description", "start_date", "bill_data", "location"
                                    ]
                                ],
                                data=[],  # Empty initially, can be updated dynamically
                                style_table={"overflowX": "auto"},
                                style_header={"fontWeight": "bold"},
                            )
                        ),
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

# Callback to update the table on submit
@app.callback(
    Output("events_table", "data"),
    Input("submit-val", "n_clicks"),
    State("state", "value"),
    State("start_date", "value"),
    State("end_date", "value"),
    prevent_initial_call=True,
)
def update_table(n_clicks, state, start_date, end_date):
    if state and start_date and end_date:
        return pull_data(state, start_date, end_date)
    return []

# Run application on web browser
if __name__ == "__main__":
    port = 8050
    url = f"http://127.0.0.1:{port}/"
    print(f"Running on {url}")
    webbrowser.open(url, new=2)
    app.run_server(debug=True, port=port)
