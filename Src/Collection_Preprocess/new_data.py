#!/usr/bin/python

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
import numpy as np
import json
import datetime

import requests


class Stock_Data():

    def __init__(self, ticker):
        self.ticker = ticker

    def get_long_period_raw_df(self, period="1y", interval="1d", threads=True):
        long_period_df = yf.download(
            self.ticker,
            interval=interval,
            period=period,
            threads=threads
        )
        self.long_period_df = long_period_df
        return self.long_period_df

    def get_short_period_raw_df(self, period='60d', interval='1h', threads=True):
        short_df = yf.download(
            self.ticker,
            interval=interval,
            period=period,
            threads=threads
        )
        self.short_period_df = short_df
        return self.short_period_df

    def get_current_close_price(self, period='1d', interval='5m', threads=True):
        current_price_df = yf.download(
            self.ticker,
            period=period,
            interval=interval,
            threads=threads
        )

        current_close_price = current_price_df["Close"].tail().to_frame()
        self.current_close_price = current_close_price

        return self.current_close_price


# Example intervals
# SEC, MIN, HRS, DAY
class Crypto_Data():
    def __init__(self, api_key):
        self.api_key = api_key

    def get_only_one_close_df(self, ticker, years: int = 2, interval: str = '1DAY'):
        """
        Returns only the closing price of a given Crypto Currency from the last 2 years.
        """
        # Date range of the request
        total_days = years * 365  # Bitcoin is traded 24/7
        end = datetime.date.today()
        start = end - datetime.timedelta(days=total_days)
        # limit = str(end - start).split()[0]
        # Distance between ticks
        interval = interval
        url = f'https://rest.coinapi.io/v1/exchangerate/{ticker}/USD/history?period_id={interval}&time_start={start}&time_end={end}&limit={total_days}'
        # Authenticating the request
        headers = {'X-CoinAPI-Key': self.api_key}
        # Requesting the data
        response = requests.get(url, headers=headers).json()
        print(response)
        # Turning response to a dataframe
        df = pd.DataFrame(response)
        # Changing the column name to 'Date' for easier use
        df['Date'] = df['time_close']
        # Renaming the rate_close column to 'Close'
        df[f'{ticker[0]}'] = df['rate_close']
        # Only Retrieve the Date and Close Columns
        df = df[['Date', f'{ticker[0]}']]
        # Only Show Year Month Day
        df['Date'] = pd.to_datetime(df['Date'].str[:10])
        df.set_index('Date', inplace=True)
        # Don't return self..., you will not be able to replace it.
        return df

    # This one is most likely to be ran as most people probably want to keep track of multiple tickers.
    def get_multiple_close_df(self, tickers: list, years: int = 2, interval: str = "1Day"):
        main_crypto_df = Crypto_Data(
            self.api_key).get_only_one_close_df(
            ticker=tickers[0],
            years=years
        )
        main_crypto_df.columns = [f"{tickers[0]}"]
        # TODO Rename "CLOSE" column to "BTC"
        # Do the same for the rest.
        # This will make it more like the Stock Data

        # main_crypto_df.columns = [f"{tickers[0]} Close"]
        # main_crypto_df[f"{tickers[0]} Close"] = main_crypto_df

        # Glueing new crypto dfs to the existing one.
        for ticker in tickers[1:]:
            new_crypto_df = Crypto_Data(
                self.api_key).get_only_one_close_df(ticker)

            main_crypto_df[ticker] = new_crypto_df

        return main_crypto_df

        # TODO GET CURRENT CRYPTO PRICE
        # You want the price at least within the last 5 minutes.
        # You will have to read a bunch of documentation.
        def get_current_crypto_price(
                self,
                ticker: str,
                interval: str = '5MIN'
        ):
            end = datetime.date.today()
            start = end - datetime.timedelta(1)

            # Date range of the request
            limit = 1
        # TODO Figure out this part to get the current price.
        # TODO Break this url up into variables that are more readable.
        # E.g.
        # base = 'https://rest.coinapi.io/v1/'
        # daily_prices = 'sa;lfdkj;asldfkjas;ldfkj'

        url = f'https://rest.coinapi.io/v1/exchangerate/{ticker}/USD/history?period_id={interval}&time_start={start}&time_end={end}&limit={limit}'
        # Authenticating the request
        headers = {'X-CoinAPI-Key': self.api_key}
        # Requesting the data
        response = requests.get(url, headers=headers).json()
        # Turning response to a dataframe
        df = pd.DataFrame(response)
        # # Changing the column name to 'Date' for easier use
        df['Date'] = df['time_close']
        # # Renaming the rate_close column to 'Close'
        df['Close'] = df['rate_close']
        # # Only Retrieve the Date and Close Columns
        df = df[['Date', 'Close']]
        # # Only Show Year Month Day
        df['Date'] = pd.to_datetime(df['Date'].str[:10])
        df.set_index('Date', inplace=True)
        print(f"Start: {start}")
        print(f"End: {end}")
        print(f"Limit: {limit}")

        return df


class Data():

    # Extra Useful Functions

    @staticmethod
    def get_log_returns(df):
        """ Return Cumulative return in percent form.
        Requires a single column of a dataframe to be passed
        """
        df1 = df.copy()
        df2 = np.log(
            df1 / df1.shift(1))
        return df2

    @staticmethod
    def get_cumulative_returns_in_dollars(df, starting_amount=1):
        """
        Cumulative return in dollar form.
        Requires a single column of a dataframe to be passed
        """
        cumulative_returns = (1 + df) * starting_amount
        return cumulative_returns

    @staticmethod
    def simple_returns_to_cumulative_returns(df):
        """
        Turns a simple returns column into cumulative Returns.
        Multiply this value by a starting price and you get the dollar amount
        """
        df1 = (1+df).cumprod()
        return df1


if __name__ == "__main__":
    ################# STOCKS ###############################
    # Initialize the class with ticker
    long_term_stock_data = Stock_Data(["GME", "TSLA"])

    # Get Historical prices
    long_term_stock_data = long_term_stock_data.get_long_period_raw_df()
    # Only get the closing prices.
    ldf_close = pd.DataFrame(long_term_stock_data.Close)

    ################ CRYPTO ###################################

    import sys
    sys.path.append("../")
    print('\n\n\n\nCrypto Data')
    tickers = ["BTC", "ETH"]

    # end = datetime.date.today()
    # start = end - datetime.timedelta(days=505)

    import read_config
    env_location = '../../Data/.env'
    user_name, password, crypto_api = read_config.export_variables(
        env_location)

    # Instantiate the Crypto Data Class
    crypto_closing_df = Crypto_Data(
        crypto_api)

    crypto_df = crypto_closing_df.get_multiple_close_df(tickers)

    # PRODUCES THE EXACT SAME FORMAT FOR BOTH CRYPTO AND STOCK
    print(ldf_close)
    print(crypto_df)

    # ################### OTHER ###################################

    # # ldf["Cumulative Returns"] = Data.get_log_returns(ldf.Close)

    # # ldf["Cumulative Dollar Returns"] = Data.get_dollar_cumulative_returns(
    # #     ldf["Cumulative Returns"])
    # # ldf["Simple"] = ldf.Close.pct_change()
    # # ldf["Cum"] = Data.simple_returns_to_cumulative_returns(
    # #     ldf["Simple"]) * 1000
    # # print(ldf)
