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
        Takes in a column of predicted prices and returns a new dataframe containing all tickers that are near or below their moving average in order of closeness.
        """

        # Create an empty list instead of dataframe because pandas doesn't seem to work.
        buy_df = []

        do_not_buy_df = []
        # For ticker in dataframe

        for ticker in self.predictions_df:
            buy_df = pd.DataFrame()
        #     # Create the moving averages
            predicted_ma_100 = self.predictions_df[ticker].rolling(
                window=100).mean()[-1]
            predicted_ma_250 = self.predictions_df[ticker].rolling(
                window=250).mean()[-1]
            predicted_price = self.predictions_df[ticker][-1]

            current_ma_100 = self.predictions_df[ticker].rolling(
                window=100).mean()[-5]
            current_ma_250 = self.predictions_df[ticker].rolling(
                window=250).mean()[-5]
            current_price = self.predictions_df[ticker][-5]

        #     # If any of these conditions are true, then we append the ticker and its info to the buy dataframe.
            buy_condition = [
                # Predicted price is less than the predicted 100 day ma
                (predicted_price < predicted_ma_100) |
                # Predicted price is less than the predicted 100 day ma * 2%
                (predicted_price < (predicted_ma_100 * 1.02)) |
                # Predicted price is less than the predicted 250
                (predicted_price < predicted_ma_250) |

                (current_price < current_ma_100) |
                (current_price < (current_ma_100 * 1.02)) |
                (current_price < current_ma_250)
            ]

            # For some reason I can't just say "if buy_condition"
            if buy_condition == True:
                buy_opportunity = {
                    "Ticker": ticker,
                    "Current Price": current_price,
                    "Current 100": current_ma_100,
                    "Current 250": current_ma_250,
                    "Predicted Price": predicted_price,
                    "Predicted 100": predicted_ma_100,
                    "Predicted 250": predicted_ma_250
                }
                buy_df.append(buy_opportunity)

            else:
                no_opportunity = {
                    "Ticker": ticker,
                    "Current Price": current_price,
                    "Current 100": current_ma_100,
                    "Current 250": current_ma_250,
                    "Predicted Price": predicted_price,
                    "Predicted 100": predicted_ma_100,
                    "Predicted 250": predicted_ma_250
                }
                do_not_buy_df.append(no_opportunity)
        do_not_buy_df = pd.DataFrame(do_not_buy_df)
        buy_df = pd.DataFrame(buy_df)

        # This will return two values if possible.
        # If it is not possible, it will only return one.
        try:
            buy_email_df = self.closeness_caluclator(buy_df)
            do_not_buy_email_df = self.closeness_caluclator(do_not_buy_df)
            return do_not_buy_email_df.set_index("Ticker"), buy_email_df.set_index("Ticker")

        except KeyError as e:
            print(e)
            do_not_buy_email_df = self.closeness_caluclator(do_not_buy_df)
            return do_not_buy_email_df.set_index("Ticker")

    def closeness_caluclator(self, df):
        # Finding how far price is from the ma
        df["Actual Closeness"] = df["Current Price"] / \
            df["Current 250"] - 1
        df["Predicted Closeness"] = df["Predicted Price"] / \
            df["Predicted 250"] - 1

        df.sort_values(
            by=["Actual Closeness"],
            inplace=True)
        return df.round(2)

########################## POSSIBLE FUTURE ADDITION ##########################
    # def plot_dataframe(self):
    #     start = str(df.index[-200])[:10]
    #     end = str(df.index[-6])[:10]

    #     actual_close = df['Close'][-200:-4]
    #     actual_50 = df['50ma'][-200:-4]
    #     actual_100 = df['100ma'][-200:-4]

    #     predicted_close = df['Close'][-5:]
    #     predicted_50 = df['50ma'][-5:]
    #     predicted_100 = df['100ma'][-5:]

    #     actual_close.plot(
    #         title=f"{ticker} from {start} to {end} + 5",
    #         c="b",
    #         legend=True,
    #         grid=True
    #     )
    #     actual_50.plot(c="yellow", legend=True)
    #     actual_100.plot(c="orange", legend=True)

    #     predicted_close.plot(c="red", legend=True)
    #     predicted_50.plot(c="green", legend=True)
    #     predicted_100.plot(c="black", legend=True)
    #     # plt.show()
    #     plt.savefig("./Functions/Email/stock_image1.png",
    #                 orientation="landscape")

    # def plot_dataframe_zoomed(self):
    #     start = str(df.index[-50])[:10]
    #     end = str(df.index[-6])[:10]
    #     actual_close = df['Close'][-50:-4]
    #     actual_50 = df['50ma'][-50:-4]
    #     actual_100 = df['100ma'][-50:-4]

    #     predicted_close = df['Close'][-5:]
    #     predicted_50 = df['50ma'][-5:]
    #     predicted_100 = df['100ma'][-5:]

    #     actual_close.plot(
    #         title=f"{ticker} from {start} to {end} + 5",
    #         c="b",
    #         legend=True,
    #         grid=True
    #     )
    #     actual_50.plot(c="yellow", legend=True)
    #     actual_100.plot(c="orange", legend=True)

    #     predicted_close.plot(c="red", legend=True)
    #     predicted_50.plot(c="green", legend=True)
    #     predicted_100.plot(c="black", legend=True)
    #     # plt.show()
    #     plt.savefig("./Functions/Email/stock_image2.png",
    #                 orientation="landscape")


if __name__ == "__main__":
    import sys
    sys.path.append('../')
    from Models import arima_test
    from Collection_Preprocess.new_data import Stock_Data, Crypto_Data

    ticker = ["LOW", "AMZN"]
    stocks = Stock_Data(ticker)
    long_df = pd.DataFrame(stocks.get_long_period_raw_df(period="2y").Close)

    stock_predictions = arima_test.arima_predictions()
    stock_predictions = stock_predictions.run_multiple_tests(long_df)

    stock_analysis = Analysis(stock_predictions)

    try:
        do_not_buy_df, buy_df = stock_analysis.default_analysis()
    except Exception as e:
        print(e)
        do_not_buy_df = stock_analysis.default_analysis()
    print(do_not_buy_df)

    # predicted_df = pd.read_csv(
    #     "../stock_predictions.csv",
    #     index_col="Date",
    #     parse_dates=True
    # )
    # print(predicted_df)

    # analysis_df = Analysis(predicted_df)
    # default_analysis = analysis_df.default_analysis()

    # df = default_analysis(
    #     long_df,
    #     current_price_df,
    #     sensitivity=0.01
    # )
    # da = default_analysis(long_df, current_price_df)
    # print(da)
    # plot_dataframe(ticker, long_df)
    # plot_dataframe_zoomed(ticker, long_df)
