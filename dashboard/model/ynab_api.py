import logging
from datetime import datetime

import pandas as pd
from agithub.base import API, ConnectionProperties, Client

from app import cache

import pickle as pickle
from os import path

from config import token

logger = logging.getLogger("ynab_dashboard")


class YNAB_API(API):
    def __init__(self, api_token, *args, **kwargs):
        extra_headers = {
            "Authorization": f"Bearer {api_token}"
        }
        props = ConnectionProperties(
            api_url='api.youneedabudget.com',
            secure_http=True,
            extra_headers=extra_headers
        )
        self.setClient(Client(*args, **kwargs))
        self.setConnectionProperties(props)


class YNAB():
    budgets_pickle_path = "pickles/budgets.pickle"
    budget_months_pickle_path = "pickles/{budget_id}_budget_months.pickle"
    budget_months_detail_pickle_path = "pickles/{budget_id}_budget_months_detail.pickle"
    transactions_pickle_path = "pickles/{budget_id}_transactions.pickle"

    def __init__(self, api_token, preload=False):
        self.ynab = YNAB_API(api_token)

        if preload:
            self.get_budgets()

    def get_rate_limit(self):
        try:
            headers = {k: v for k, v in self.ynab.getheaders()}
            left, limit = headers.get("X-Rate-Limit", "200/200").rsplit("/")
            return int(left), int(limit)
        except TypeError:
            return -1, 200

    @cache.memoize()
    def get_budgets(self):
        pickle_path = self.budgets_pickle_path
        budgets = None
        if path.exists(pickle_path):
            with open(pickle_path, 'rb') as f:
                budgets = pickle.load(f)
        else:
            url = self.ynab.v1.budgets
            logger.info(f"Getting {url}")
            response, data = url.get()
            if response == 200:
                budgets = data['data']['budgets']
                with open(pickle_path, 'wb') as f:
                    pickle.dump(budgets, f, pickle.HIGHEST_PROTOCOL)
            else:
                logger.warning(f"Response: {response}, {data}")
        return budgets

    @cache.memoize()
    def get_transactions(self, budget_id):
        pickle_path = self.transactions_pickle_path.format(budget_id)

        url = self.ynab.v1.budgets[budget_id].transactions
        logger.info(f"Getting {url}")
        if path.exists(pickle_path):
            with open(pickle_path, 'rb') as f:
                (server_knowledge, transactions) = pickle.load(f)
                response, data = url.get(last_knowledge_of_server=server_knowledge)
                if response == 200:
                    transactions += data['data']['transactions']
        else:
            response, data = url.get()
            transactions = data['data']['transactions']

        with open(pickle_path, 'wb') as f:
            pickle.dump((data['data']['server_knowledge'], transactions), f, pickle.HIGHEST_PROTOCOL)

        transactions_df = pd.DataFrame(transactions)
        transactions_df['date'] = pd.to_datetime(transactions_df['date'])
        transactions_df['amount'] = transactions_df.amount / 1000
        return transactions_df

    @cache.memoize()
    def get_categories(self, budget_id):
        url = self.ynab.v1.budgets[budget_id].categories
        logger.info(f"Getting {url}")
        response, data = url.get()

        if response == 200:
            category_groups = data['data']['category_groups']
            return category_groups
        logger.warning(f"Response: {response}, {data}")

    @cache.memoize()
    def get_budget_months(self, budget_id):
        url = self.ynab.v1.budgets[budget_id].months
        logger.info(f"Getting {url}")
        response, data = url.get()
        if response == 200:
            df = pd.DataFrame(data['data']['months'])
            df['month'] = pd.to_datetime(df['month'])
            return df
        logger.warning(f"Response: {response}, {data}")

    def get_complete_budget_months(self, budget_id):
        def _get_complete_budget_months(budget_id_, last_month_=None):
            months = self.get_budget_months(budget_id_)
            if last_month_ and type(last_month_) in (datetime, pd.Timestamp):
                logger.debug(f"Getting the budget months since {last_month_}")
                months = months[months.month > last_month_]
            budget_months_ = []
            for month in months.month:
                month: datetime = pd.to_datetime(month)
                logger.debug(f"type of month ({month}): {type(month)}")
                url = self.ynab.v1.budgets[budget_id_].months[month.strftime("%Y-%m-%d")]
                logger.info(f"Getting {url}")
                response, data = url.get()
                budget_month = data['data']['month']
                month_cats = pd.DataFrame(budget_month['categories'])
                month_cats['month'] = budget_month['month']
                month_cats['month'] = pd.to_datetime(month_cats['month'])
                budget_months_.append(month_cats)
            return months.month.min(), months.month.max(), pd.concat(budget_months_) if len(
                budget_months_) else pd.DataFrame()

        pickle_path = f'pickles/{budget_id}_budget.pickle'
        if path.exists(pickle_path):
            with open(pickle_path, 'rb') as f:
                (last_month, orig_budget_months) = pickle.load(f)
                logger.debug(f"last_month type after unpickle: {type(last_month)}")
                logger.debug(f"opened budget pickle, last month: {last_month}")
                first_month, last_month, budget_months = _get_complete_budget_months(budget_id, last_month_=last_month)
                logger.debug(f"last_month type after function: {type(last_month)}")
                budget_months = pd.concat([orig_budget_months, budget_months])
        else:
            first_month, last_month, budget_months = _get_complete_budget_months(budget_id)
            logger.debug(f"last_month type after function: {type(last_month)}")

        with open(pickle_path, 'wb') as f:
            pickle.dump((last_month, budget_months), f, pickle.HIGHEST_PROTOCOL)
        budget_months = budget_months[budget_months.name != "Inflows"]
        budget_months.balance = budget_months.balance / 1000
        return budget_months


api = YNAB(token, preload=True)

