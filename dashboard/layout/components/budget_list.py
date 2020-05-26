import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


def budget_dropdown(budgets):
    dropdown = dcc.Dropdown(
        id='budgets-dropdown',
        options=[
            {'label': budget['name'], 'value': budget['id']} for budget in budgets
        ]
    )
    return dropdown
