import logging

import pandas as pd
from pandas.tseries.offsets import *
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from app import app

import json
import math

from model.data import get_category_transactions

logger = logging.getLogger("ynab_dashboard")


def empty_slider():
    empty = [
        dcc.RangeSlider(
            id='month-slider',
            updatemode='mouseup',
            count=1,
            min=1,
            step=1,
            pushable=1,
            tooltip={"always_visible": False}
        ),
        html.Div(children=[
            dcc.Input(id='slider-start-date', type='text'),
            dcc.Input(id='slider-end-date', type='text'),
        ], id="month-slider-result", style={'display': 'block'}),
        html.Div(id="month-slider-values", style={'display': 'none'})
    ]
    return empty


def month_slider(min_date, max_date):
    logger.debug(f"Making slider with {min_date} {max_date}")
    date_values, slider = _date_range(min_date, max_date)
    return [
        slider,
        html.Div(children=[
            dcc.Input(id='slider-start-date', type='text'),
            dcc.Input(id='slider-end-date', type='text'),
        ], id="month-slider-result", style={'display': 'block'}),
        html.Div(children=[json.dumps(date_values)], id="month-slider-values", style={'display': 'none'})
    ]


def _date_range(min_date, max_date):
    datelist = pd.date_range(start=min_date, end=max_date, freq='M')  # list of months as dates
    maxmarks = len(datelist)
    dlist = pd.DatetimeIndex(datelist).normalize()
    tags = {}  # dictionary relating marks on slider to tags. tags are shown as "Apr', "May', etc
    datevalues = {}  # dictionary relating mark to date value
    x = 1

    modulo = math.ceil(len(dlist) / 24)

    date: pd.Timestamp
    for i, date in enumerate(dlist):
        if i % modulo == 0:
            tags[x] = (date + DateOffset(months=1)).strftime(
                '%b\n%Y')  # gets the string representation of next month ex:'Apr'
        datevalues[x] = date.strftime("%Y-%m-%d")
        x = x + 1

    return datevalues, dcc.RangeSlider(
        id='month-slider',
        updatemode='mouseup',
        count=1,
        min=1,
        max=maxmarks,
        step=1,
        value=[max(maxmarks - 5, 1), maxmarks],
        marks=tags,
        pushable=1,
        tooltip={"always_visible": False}
    )


# @app.callback(
#     [Input('slider-start-date', 'value'), Input('slider-end-date', 'value')],
#     [Output('month-slider', 'value'), Output('month-slider-values', 'children')])
# def _month_slider_output_updater(value, slider_values):
#     slider_values = slider_values[0]
#     if value:
#         slider_values = json.loads(slider_values)
#         return slider_values[str(value[0])], slider_values[str(value[1])]
#     return "", ""

@app.callback(
    [Output('slider-start-date', 'value'), Output('slider-end-date', 'value')],
    [Input('month-slider', 'value'), Input('month-slider-values', 'children')])
def _month_slider_output_updater(value, slider_values):
    if value and slider_values:
        slider_values = slider_values[0]
        slider_values = json.loads(slider_values)
        return slider_values[str(value[0])], slider_values[str(value[1])]
    return "", ""
