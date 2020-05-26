import dash_bootstrap_components as dbc


def get_body():
    page = [
        dbc.Row(id="balance-graph"),
        dbc.Row(id="category-balance-graph"),
        dbc.Row(id="category-budgeted-graph")
    ]
    return page
