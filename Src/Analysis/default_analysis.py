#!/usr/bin/python
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import sys
from Collection_Preprocess.new_data import Stock_Data, Crypto_Data
sys.path.append('../')


class Analysis():

    # TODO Might need to add a __super__ method for the plot_dataframe so I can add default analysis or any other to Analysis __init__()

    def default_analysis(self, sensitivity: float = 0.025):

        # Finding the moving averages
        # long_close_df.reset_index(inplace=True)
        # long_close_df['Date'] = long_close_df['Date'].apply(
        #     lambda x: str(x)[:10])
        # long_close_df.set_index('Date', inplace=True)
        long_close_df['50ma'] = long_close_df['Close'].rolling(
            window=50).mean()
        long_close_df['100ma'] = long_close_df['Close'].rolling(
            window=100).mean()

        # # If the current price is near either, email me.
        # current_50_ma = long_close_df['50ma'].tail(1).values
        # current_100_ma = long_close_df['100ma'].tail(1).values

        # # Current price
        # current_price = current_price_close_df.Close.values
        # # Conditions to be met
        # conditions = [
        #     # If the current price is plus or minus 5% of the 50 day moving average.
        #     (current_price <= current_50_ma *
        #      1.05) & (current_price > current_50_ma * 0.95),
        #     # If the current price is plus or minus 5% of the 200 day moving average.
        #     (current_price <= current_100_ma *
        #      1.05) & (current_price > current_100_ma * 0.95),
        # ]
        return long_close_df[['Close', '50ma', '100ma']]

    # Eg of Super
    # self.analysis_df would be used here instead of regular self.
    # Really, the only needed graphs are the absolutely best oportunities.
    def plot_dataframe(self):
        start = str(df.index[-200])[:10]
        end = str(df.index[-6])[:10]

        actual_close = df['Close'][-200:-4]
        actual_50 = df['50ma'][-200:-4]
        actual_100 = df['100ma'][-200:-4]

        predicted_close = df['Close'][-5:]
        predicted_50 = df['50ma'][-5:]
        predicted_100 = df['100ma'][-5:]

        actual_close.plot(
            title=f"{ticker} from {start} to {end} + 5",
            c="b",
            legend=True,
            grid=True
        )
        actual_50.plot(c="yellow", legend=True)
        actual_100.plot(c="orange", legend=True)

        predicted_close.plot(c="red", legend=True)
        predicted_50.plot(c="green", legend=True)
        predicted_100.plot(c="black", legend=True)
        # plt.show()
        plt.savefig("./Functions/Email/stock_image1.png",
                    orientation="landscape")

    def plot_dataframe_zoomed(self):
        start = str(df.index[-50])[:10]
        end = str(df.index[-6])[:10]
        actual_close = df['Close'][-50:-4]
        actual_50 = df['50ma'][-50:-4]
        actual_100 = df['100ma'][-50:-4]

        predicted_close = df['Close'][-5:]
        predicted_50 = df['50ma'][-5:]
        predicted_100 = df['100ma'][-5:]

        actual_close.plot(
            title=f"{ticker} from {start} to {end} + 5",
            c="b",
            legend=True,
            grid=True
        )
        actual_50.plot(c="yellow", legend=True)
        actual_100.plot(c="orange", legend=True)

        predicted_close.plot(c="red", legend=True)
        predicted_50.plot(c="green", legend=True)
        predicted_100.plot(c="black", legend=True)
        # plt.show()
        plt.savefig("./Functions/Email/stock_image2.png",
                    orientation="landscape")


if __name__ == "__main__":
    ticker = ["AAPL", "GOOGL"]
    stocks = Stock_Data(ticker)
    long_df = stocks.get_long_period_raw_df(period="2y")
    current_price_df = stocks.current_close_price()

    stock_analysis = Analysis(stocks)
    default_stock_analysis = stocks.default_analysis()

    # df = default_analysis(
    #     long_df,
    #     current_price_df,
    #     sensitivity=0.01
    # )
    # da = default_analysis(long_df, current_price_df)
    # print(da)
    # plot_dataframe(ticker, long_df)
    # plot_dataframe_zoomed(ticker, long_df)
