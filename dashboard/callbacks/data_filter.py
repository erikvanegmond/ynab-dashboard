import json
import logging

from dash.dependencies import Input, Output
from app import app
from layout.components.month_slider import month_slider, empty_slider
from model.data import get_category_transactions
from model.ynab_api import api

logger = logging.getLogger("ynab_dashboard")

@app.callback(
    Output('month-slider-container', 'children'),
    [Input('budgets-dropdown', 'value')])
def month_slider_controller(budget_id):

    if budget_id:
        logger.debug(f"month slider with budget id: {budget_id}")
        budgets = api.get_budget_months(budget_id)
        min_date = budgets['month'].min()
        max_date = budgets['month'].max()
        return month_slider(min_date, max_date)
    return empty_slider()


# was al gecomment?
# @app.callback(
#     [Output('slider-start-date', 'value'), Output('slider-end-date', 'value')],
#     [Input('month-slider', 'value'), Input('month-slider-values', 'children')])
# def _month_slider_output_updater(value, slider_values):
#     slider_values = slider_values[0]
#     if value:
#         slider_values = json.loads(slider_values)
#         return slider_values[str(value[0])], slider_values[str(value[1])]
#     return "", ""
