import dash_html_components as html
import dash_bootstrap_components as dbc


def get_body():
    page = [
        dbc.Row(
            children=[
                dbc.Jumbotron(
                    [
                        html.H1("YNAB Dashboard", className="display-3"),
                        html.P(
                            "Hello World",
                            className="lead",
                        ),
                        html.Hr(className="my-2"),
                        html.P(
                            "It tells you what this dashboard is for"
                        ),
                        html.P(dbc.Button("Tables", color="primary", href="/tables"), className="lead"),
                    ]
                )
            ]
        ),
        dbc.Row(id="age-of-money-graph")
    ]
    return page
