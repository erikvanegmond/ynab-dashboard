import logging

from layout.components.nav_bar import nav_bar

logger = logging.getLogger("ynab_dashboard")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

from config_pages import config_pages
from layout.pages import error
from layout import default, alternative
from app import app
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from callbacks import *

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(children=default.get_layout())
    ]
)


# CALBACKS
@app.callback(
    [Output('nav-bar-container', 'children'),Output('content-container', 'children')],
    [
        Input('url', 'pathname')
    ]
)
def display_page(pathname):
    body = error

    for page in config_pages:
        if pathname in config_pages[page]['link']:
            body = config_pages[page]['body']
            break
    nav = nav_bar(pathname, "Dashboard for YNAB")
    content = body.get_body()
    return nav, content


if __name__ == "__main__":
    logger.debug("Starting App")
    app.run_server(debug=True)
