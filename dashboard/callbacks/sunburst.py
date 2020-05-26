from datetime import datetime

from dash.dependencies import Input, Output
from app import app
import dash_html_components as html

from layout.components.graphs.sunburst_chart import sunburst_chart
from model.data import get_category_transactions


@app.callback(
    Output('sunburst-graph', 'children'),
    [Input('budgets-dropdown', 'value'), Input('slider-start-date', 'value'), Input('slider-end-date', 'value')])
def sunburst_controller(budget_id, start_date, end_date):
    if budget_id and start_date and end_date:
        cats = get_category_transactions(budget_id)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        cats = cats[
            (cats.date > start_date) & (cats.date <= end_date)]
        cats = cats[cats["parent_category_name"] != "Internal Master Category"]
        cats = cats[cats.category_id.notna()]
        cats = cats[cats.parent_category_id.notna()]
        cats = cats[cats.amount < 0]
        cats["all_spending"] = "All Spending"
        cats['amount'] = cats['amount'] * -1
        return sunburst_chart(cats, path=["all_spending", "parent_category_name", "category_name"], values="amount")
    return html.Div("no budget selected")
