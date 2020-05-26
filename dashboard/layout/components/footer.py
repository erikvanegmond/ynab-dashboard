import dash_html_components as html

import dash_bootstrap_components as dbc

from layout.components.graphs.indicator import indicator
from model.ynab_api import api


def footer():
    value, limit = api.get_rate_limit()
    return html.Footer(
        dbc.Container(children=[
            dbc.Row(
                indicator(value, limit)
            ),
            dbc.Row(f"© 2020")
            ]
        ),
        className="footer"
    )
