import dash_html_components as html

import dash_bootstrap_components as dbc

from layout.components.budget_list import budget_dropdown
from layout.components.month_slider import empty_slider
from model.ynab_api import api


def data_filter():
    filter_dom = html.Div(dbc.Container(id="filter",
                                        children=[
                                            dbc.Row(
                                                children=[
                                                    dbc.Col(
                                                        budget_dropdown(api.get_budgets()),
                                                        width=3
                                                    ),
                                                    dbc.Col(
                                                        dbc.ButtonGroup(
                                                            [dbc.Button("This Month"),
                                                             dbc.Button("Latest 3 Months"),
                                                             dbc.Button("Latest 12 Months"),
                                                             dbc.Button("This Year"),
                                                             dbc.Button("Last Year"),
                                                             dbc.Button("All Dates")],
                                                            size="md",
                                                            className="mr-1",
                                                        )
                                                    )
                                                ]
                                            ),
                                            dbc.Row(
                                                dbc.Col(id="month-slider-container", children=empty_slider())
                                            )
                                        ]), className="filter-bar")
    return filter_dom
