import dash_html_components as html
from flask import Response


def get_body():
    Response('Not Found', 404)
    return html.Div(["""Not found"""])
