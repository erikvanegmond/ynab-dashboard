import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from layout.components.nav_bar import nav_bar


def get_layout(pathname="/", brand="", children=None):
    layout = html.Div(
        [
            nav_bar(pathname, brand),
            html.Div("Different"),
            dbc.Container(children)
        ]
    )
    return layout
