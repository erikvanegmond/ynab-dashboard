import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from layout.components.data_filter import data_filter
from layout.components.footer import footer
from layout.components.nav_bar import nav_bar


def get_layout():
    layout = html.Div(
        [
            html.Div(id="nav-bar-container"),
            data_filter(),
            dbc.Container(id="content-container"),
            footer()
        ]
    )
    return layout
