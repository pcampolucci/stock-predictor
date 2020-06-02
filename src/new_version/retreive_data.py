"""
Title: Data retrieval class for the oil company, euro value and oil

Author: Pietro Campolucci
"""

# other packages
import datetime as dt
import pandas as pd
import yfinance as yf

# DEBUG
DEBUG = False


class GetDataset:
    """ Get data from Yahoo Finance """

    def __str__(self):
        return "Dataset class of " + self.company

    def __init__(self, company, interval, days):
        self.company = company
        self.interval = interval
        self.past = days
        self.database = self.build_database()

    def get_extremes(self):
        current = dt.datetime.now()
        past = current - dt.timedelta(days=self.past)
        current = str(current)[:10]
        past = str(past)[:10]
        return current, past

    def build_database(self):
        past = self.get_extremes()[1]
        current = self.get_extremes()[0]

        # retrieve information
        company = yf.download(self.company, start=past, end=current, interval=self.interval)
        euro = yf.download("EURUSD=X", start=past, end=current, interval=self.interval)
        oil = yf.download("CL=F", start=past, end=current, interval=self.interval)

        # build database
        data = pd.DataFrame()
        data = data.assign(company_open=company['Open'])
        data = data.assign(company_close=company['Close'])
        data = data.assign(euro_open=euro['Open'])
        data = data.assign(euro_close=euro['Close'])
        data = data.assign(oil_open=oil['Open'])
        data = data.assign(oil_close=oil['Close'])
        data = data.dropna()

        # add return value for each interval
        data = data.assign(company_return=(company["Close"] - company["Open"]))
        data = data.assign(euro_return=(euro["Close"] - euro["Open"]))
        data = data.assign(oil_return=(oil["Close"] - oil["Open"]))

        return data


# debugging script =============================================================================================
if DEBUG:
    company_name = "RDS-B"
    interval_test = "1d"
    days_test = 5000
    dataset = GetDataset(company_name, interval_test, days_test)
    print(dataset)
    print(dataset.database)

