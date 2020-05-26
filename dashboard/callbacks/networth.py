from datetime import datetime

from dash.dependencies import Input, Output
from app import app
import dash_html_components as html

from layout.components.graphs.bar_chart import bar_chart
from layout.components.graphs.networth_chart import networth_chart
from model.data import get_balance_per_account, get_category_transactions, get_categorized_budgets


@app.callback(
    Output('balance-graph', 'children'),
    [Input('budgets-dropdown', 'value'), Input('slider-start-date', 'value'), Input('slider-end-date', 'value')])
def networth_account_controller(budget_id, start_date, end_date):
    if budget_id and start_date and end_date:
        transactions = get_category_transactions(budget_id)
        balances = get_balance_per_account(transactions, frequency="M")
        balances = balances[
            (balances.date > datetime.strptime(start_date, "%Y-%m-%d")) &
            (balances.date <= datetime.strptime(end_date, "%Y-%m-%d"))
            ]
        return networth_chart(balances, group="account_name", frequency="M")
    else:
        return html.Div("no budget selected")


@app.callback(
    Output('category-balance-graph', 'children'),
    [Input('budgets-dropdown', 'value'), Input('slider-start-date', 'value'), Input('slider-end-date', 'value')])
def networth_account_controller(budget_id, start_date, end_date):
    if budget_id and start_date and end_date:
        balances = get_categorized_budgets(budget_id)
        balances = balances[
            (balances.month > datetime.strptime(start_date, "%Y-%m-%d")) &
            (balances.month <= datetime.strptime(end_date, "%Y-%m-%d"))
            ]

        return bar_chart(balances, x='month', y='balance', color='name')
    return html.Div("no budget selected")

@app.callback(
    Output('category-budgeted-graph', 'children'),
    [Input('budgets-dropdown', 'value'), Input('slider-start-date', 'value'), Input('slider-end-date', 'value')])
def networth_account_controller(budget_id, start_date, end_date):
    if budget_id and start_date and end_date:
        balances = get_categorized_budgets(budget_id)
        balances = balances[
            (balances.month > datetime.strptime(start_date, "%Y-%m-%d")) &
            (balances.month <= datetime.strptime(end_date, "%Y-%m-%d"))
            ]

        return bar_chart(balances, x='month', y='budgeted', color='name')
    return html.Div("no budget selected")

