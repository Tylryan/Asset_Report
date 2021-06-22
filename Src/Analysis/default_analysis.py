#!/usr/bin/python
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
sys.path.append('../')


class Analysis():

    def __init__(self, predictions_df):
        self.predictions_df = predictions_df
        self.tickers = predictions_df.columns
    # TODO Might need to add a __super__ method for the plot_dataframe so I can add default analysis or any other to Analysis __init__()

    def default_analysis(self, sensitivity: float = 0.025):
        """
        Takes in a column of predicted prices and returns their moving averages.
        """

        # Finding the moving averages
        # long_close_df.reset_index(inplace=True)
        # long_close_df['Date'] = long_close_df['Date'].apply(
        #     lambda x: str(x)[:10])
        # long_close_df.set_index('Date', inplace=True)

        # Setting up the new dataframe.

        analysis_df = pd.DataFrame()
        analysis_df[self.tickers[0]] = self.predictions_df.iloc[:, 0]
        analysis_df[f'{self.tickers[0]} 50ma'] = self.predictions_df.iloc[:, 0].rolling(
            window=50).mean()
        analysis_df[f'{self.tickers[0]} 100ma'] = self.predictions_df.iloc[:, 0].rolling(
            window=100).mean()

        for ticker in predicted_df[1:]:
            analysis_df[ticker] = self.predictions_df[ticker]
            analysis_df[f'{ticker} 50ma'] = self.predictions_df[ticker].rolling(
                window=50).mean()
            analysis_df[f'{ticker} 100ma'] = self.predictions_df[ticker].rolling(
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
        return analysis_df

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
    import sys
    sys.path.append('../')
    from Models import arima_test
    from Collection_Preprocess.new_data import Stock_Data, Crypto_Data

    # ticker = ["AAPL", "GOOGL"]
    # stocks = Stock_Data(ticker)
    # long_df = stocks.get_long_period_raw_df(period="2y")

    # stock_predictions = arima_test.arima_predictions()
    # stock_predictions = stock_predictions.run_multiple_tests(stocks)

    # current_price_df = stocks.current_close_price()

    # stock_analysis = Analysis(stocks)

    predicted_df = pd.read_csv(
        "../stock_predictions.csv",
        index_col="Date",
        parse_dates=True
    )
    print(predicted_df)

    analysis_df = Analysis(predicted_df)
    default_analysis = analysis_df.default_analysis()
    print(default_analysis)

    # df = default_analysis(
    #     long_df,
    #     current_price_df,
    #     sensitivity=0.01
    # )
    # da = default_analysis(long_df, current_price_df)
    # print(da)
    # plot_dataframe(ticker, long_df)
    # plot_dataframe_zoomed(ticker, long_df)
