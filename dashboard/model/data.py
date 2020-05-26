import pandas as pd

from app import cache
from model.ynab_api import api


@cache.memoize()
def get_categorized_transactions(budget_id, hierarchy, category_names):
    transactions_df = api.get_transactions(budget_id)
    transactions_df = pd.merge(transactions_df, hierarchy,
                               left_on="category_id",
                               right_on="category_id",
                               how="left")
    transactions_df = pd.merge(transactions_df, category_names,
                               left_on="parent_category_id",
                               right_on="cat_id",
                               how="left").rename(columns={'cat_name': 'parent_category_name'})
    return transactions_df


@cache.memoize()
def get_categorized_budgets(budget_id):
    simple_categories, bottom_up_dict, category_names, hierarchy = api.get_simple_categories(budget_id)
    month_budgets = api.get_complete_budget_months(budget_id)
    month_budgets = pd.merge(month_budgets, hierarchy,
                             left_on="id",
                             right_on="category_id",
                             how="left")
    month_budgets = pd.merge(month_budgets, category_names,
                             left_on="parent_category_id",
                             right_on="cat_id",
                             how="left").rename(columns={'cat_name': 'parent_category_name'})
    return month_budgets


def get_budget_by_name(name):
    budgets = api.get_budgets()
    for budget in budgets:
        if budget['name'] == name:
            return budget


@cache.memoize()
def get_simple_categories(budget_id, unhide=True):
    category_groups = api.get_categories(budget_id)

    simple_categories = {}
    bottom_up_dict = {}
    for group in category_groups:
        simple_categories[group['id']] = {'name': group['name'], 'sub_categories': {}}
        for subcat in group['categories']:
            if group['name'] == "Hidden Categories" and unhide:
                continue
            else:
                simple_categories[group['id']]['sub_categories'][subcat['id']] = {'name': subcat['name']}
                bottom_up_dict[subcat['id']] = group['id']

        if unhide:
            for subcat in group['categories']:
                if group['name'] == "Hidden Categories":
                    simple_categories[subcat['original_category_group_id']]['sub_categories'][subcat['id']] = {
                        'name': subcat['name']}
                    bottom_up_dict[subcat['id']] = subcat['original_category_group_id']

    category_names = pd.DataFrame([[k, v] for d in [
        {**{sub_cat: v2['name'] for sub_cat, v2 in v['sub_categories'].items()}, **{cat: v['name']}} for cat, v in
        simple_categories.items()] for k, v in d.items()], columns=['cat_id', 'cat_name'])
    hierarchy = pd.DataFrame([[k, v] for k, v in bottom_up_dict.items()],
                             columns=["category_id", "parent_category_id"])
    return simple_categories, bottom_up_dict, category_names, hierarchy


@cache.memoize()
def get_sub_transactions(transactions_df, hierarchy, category_names):
    sub_trans = []
    for i, row in transactions_df[transactions_df.category_name == "Split SubCategory"].iterrows():
        df = pd.DataFrame(row.subtransactions)
        #     print(row.date)
        df['date'] = row.date
        df['account_name'] = row.account_name

        sub_trans.append(df[['id', 'date', 'amount', 'category_id', 'category_name', "account_name"]])
    if sub_trans:
        sub_trans = pd.concat(sub_trans)
        sub_trans['amount'] = sub_trans.amount / 1000
        sub_trans = pd.merge(sub_trans, hierarchy, left_on="category_id", right_on="category_id", how="left")
        sub_trans = pd.merge(sub_trans, category_names, left_on="parent_category_id", right_on="cat_id",
                             how="left").rename(columns={'cat_name': 'parent_category_name'})
        return sub_trans[
            ['id', 'date', 'amount', 'category_id', 'category_name', 'parent_category_id', 'parent_category_name',
             'account_name']]
    return pd.DataFrame(
        columns=['id', 'date', 'amount', 'category_id', 'category_name', 'parent_category_id', 'parent_category_name',
                 'account_name'])


@cache.memoize()
def get_category_transactions(budget_id):
    simple_categories, bottom_up_dict, category_names, hierarchy = get_simple_categories(budget_id)
    transactions_df = get_categorized_transactions(budget_id, hierarchy, category_names)
    sub_transactions = get_sub_transactions(transactions_df, hierarchy, category_names)
    category_transactions = pd.concat([transactions_df[['id', 'date', 'amount', 'category_id', 'category_name',
                                                        'parent_category_id', 'parent_category_name', 'account_name']],
                                       sub_transactions])
    return category_transactions


def get_balance_per_category(month_budgets):
    return month_budgets[['month', 'balance', 'name']]


def get_balance_per_account(category_transactions, frequency="M"):
    accounts = category_transactions.account_name.unique()
    running_balances = []
    for account in accounts:
        df = category_transactions[category_transactions.account_name == account]
        df = df.append(pd.DataFrame([[pd.Timestamp.now(), 0, account]], columns=["date", "amount", "account_name"]),
                       sort=False, ignore_index=True)
        df["running_balance"] = df.amount.cumsum()
        df = df.resample(frequency, on='date')['running_balance', 'account_name'].agg('last')
        df = df.fillna(method='ffill')
        running_balances.append(pd.DataFrame(df))

    return pd.concat(running_balances).reset_index()
