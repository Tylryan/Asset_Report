#!/usr/bin/python

import sys
import os
from time import sleep
import pandas as pd
import yfinance as yf
import datetime
from time import sleep
import warnings
warnings.filterwarnings('ignore')


def main():
    sys.path.append(
        './Src/')
    ####################### CUSTOM IMPORTS #####################################
    from Collection_Preprocess.new_data import Stock_Data, Crypto_Data
    from Models import arima_test
    import read_config

    ###################### Customizable Variables ##############################
    # Tickers to watch
    stock_tickers = ["AMD", "AAPL"]
    crypto_tickers = ["BTC", "ETH"]

    # Can be changed to a more desired location
    env_location = 'Data/.env'
    user_name, password, crypto_api = read_config.export_variables(
        env_location)

    ###################### BRING IN DATA #####################################

    stocks_df = pd.DataFrame(Stock_Data(
        stock_tickers).get_long_period_raw_df().Close)

    # Getting a dataframe with 2 closing columns
    # Note: the 2 paramater means years of data to collect.
    try:
        crypto_closing_df = Crypto_Data(crypto_api).get_multiple_close_df(
            crypto_tickers, 2)
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
        crypto_go_ahead = False
    ################# STOCKS ###############################

    ###################### FEED IT TO ARIMA #################################

    stock_predictions = arima_test.arima_predictions()
    stock_predictions = stock_predictions.run_multiple_tests(stocks_df)

    stock_predictions.to_csv("Src/stock_predictions.csv")

    # If the user hasn't exhausted their api calls ...
    if crypto_go_ahead:
        # Instantiating the arima model
        crypto_predictions = arima_test.arima_predictions()
        # Running the model on 2 columns
        crypto_predictions = crypto_predictions.run_multiple_tests(crypto_closing_df,
                                                                   crypto_api,
                                                                   )
        crypto_predictions.to_csv("Src/crypto_predictions.csv")
        print(crypto_predictions)
    print(stock_predictions)
    #################### Basic Analysis ######################################

    # SENDING THE ACTUAL EMAIL
    # send_email(email, password)

    # print(f'\nPredicted Prices and Moving Averages for {stock_ticker}\n')
    # print(stock_analysis_df.tail(10))
    # print("---------------------------------------------------------")
    # print(f"\nRandom Walk RMSE: {stock_prediction_benchmark_mse}")
    # print(f"ARIMA Train RMSE: {stock_train_prediction_mse}")

    # Get in all the stock data


if __name__ == "__main__":
    main()
