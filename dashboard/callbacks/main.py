import logging
from datetime import datetime

from dash.dependencies import Input, Output
from app import app

from layout.components.graphs.line_chart import line_chart
from model.ynab_api import api

logger = logging.getLogger("ynab_dashboard")


@app.callback(
    Output('age-of-money-graph', 'children'),
    [Input('budgets-dropdown', 'value'), Input('slider-start-date', 'value'), Input('slider-end-date', 'value')])
def age_of_money_controller(budget_id, start_date, end_date):
    if budget_id and start_date and end_date:
        logger.debug("Age of money controller")
        df = api.get_budget_months(budget_id)
        df = df[
            (df.month > datetime.strptime(start_date, "%Y-%m-%d")) &
            (df.month <= datetime.strptime(end_date, "%Y-%m-%d"))
            ]
        return line_chart(df, x="month", y="age_of_money")
