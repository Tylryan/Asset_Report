#!/usr/bin/python
import os
from time import sleep
import pandas as pd
import yfinance as yf
import datetime
from time import sleep
import warnings
warnings.filterwarnings('ignore')


class AssetReport():
    import sys
    sys.path.append(
        './Src/')
    ####################### CUSTOM IMPORTS #####################################
    from Collection_Preprocess.new_data import Stock_Data, Crypto_Data, Data
    from Models import arima_test
    from Analysis import default_analysis
    from Email.email_user import Email
    import read_config

    def user_data(self):
        ###################### Customizable Variables ##############################
        # Tickers to watch
        stocks_crypto_file_location = "Data/assets.csv"
        self.stock_tickers, self.crypto_tickers = Data.read_from_file(
            stocks_crypto_file_location)

        # Can be changed to a more desired location
        self.env_location = 'Data/.env'
        self.email_address, self.password, self.crypto_api = read_config.export_variables(
            self.env_location)

    def analysis(self):

        ###################### BRING IN DATA #####################################

        stocks_df = pd.DataFrame(Stock_Data(
            self.stock_tickers).get_long_period_raw_df().Close)
        self.crypto_go_ahead = True
        # Getting a dataframe with 2 closing columns
        # Note: the 2 paramater means years of data to collect.
        try:
            crypto_closing_df = Crypto_Data(self.crypto_api).get_multiple_close_df(
                self.crypto_tickers, 2)
        except ValueError as e:
            print("\n\nYou have used the crypto api too many times.")
            print(
                """
        You have 2 options:
        1) Upgrade you API to a paid version.
        2) Wait 24 hours until you call again.

        More Information Below\n\n

                """, e
            )
            self.crypto_go_ahead = False
        ################# STOCKS ###############################

        ###################### FEED IT TO ARIMA #################################

        stock_predictions = arima_test.arima_predictions()
        stock_predictions = stock_predictions.run_multiple_tests(stocks_df)

        stock_predictions.to_csv("Src/stock_predictions.csv")

        # If the user hasn't exhausted their api calls ...
        if self.crypto_go_ahead == True:
            # Instantiating the arima model
            crypto_predictions = arima_test.arima_predictions()
            # Running the model on 2 columns
            crypto_predictions = crypto_predictions.run_multiple_tests(
                crypto_closing_df)
        else:
            pass
        #################### Basic Analysis ######################################

        stock_analysis = default_analysis.Analysis(stock_predictions)
        try:
            self.do_not_buy_stock_df, self.buy_stock_df = stock_analysis.default_analysis()
        except Exception as e:
            print(e)
            self.do_not_buy_stock_df = stock_analysis.default_analysis()

        if self.crypto_go_ahead == True:
            crypto_analysis = default_analysis.Analysis(crypto_predictions)
            try:
                self.do_not_buy_crypto_df, self.buy_crypto_df = crypto_analysis.default_analysis()
            except Exception as e:
                print(e)
                self.do_not_buy_crypto_df = crypto_analysis.default_analysis()
                print("\n\nCRYPTO ANALYSIS\n\n")
                print(self.do_not_buy_crypto_df)

        print("\n\nSTOCK ANALYSIS\n\n")
        print(self.do_not_buy_stock_df)
        return 0

    # def email(self):
    #     email_user = Email()
    #     email_user.report()

        # SENDING THE ACTUAL EMAIL
        # send_email(email, password)

        # print(f'\nPredicted Prices and Moving Averages for {stock_ticker}\n')
        # print(stock_analysis_df.tail(10))
        # print("---------------------------------------------------------")
        # print(f"\nRandom Walk RMSE: {stock_prediction_benchmark_mse}")
        # print(f"ARIMA Train RMSE: {stock_train_prediction_mse}")

        # Get in all the stock data


if __name__ == "__main__":
    import sys
    from Collection_Preprocess.new_data import Stock_Data, Crypto_Data, Data
    from Models import arima_test
    from Analysis import default_analysis
    from Email.email_user import Email
    import read_config
    sys.path.append("./Src/")
    asset_report = AssetReport()
    asset_report.user_data()
    asset_report.analysis()

    # If the user is not keeping track of crypto currencies
    if asset_report.crypto_go_ahead == False:
        try:
            # Stock buy = true
            Email.report3(asset_report)
        except Exception as e:
            # Stock buy = false
            Email.report4(asset_report)
    else:
        try:
            # stock buy and crypto buy = true
            Email.report(asset_report)
        # stock buy and crypto buy = false
        except Exception as e:
            Email.report2(asset_report)
        # Somehow I need to add a check for on or the other.
        # E.g Stock buy = true, crypto buy = false
