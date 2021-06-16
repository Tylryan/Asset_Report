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


# Tickers to watch
stock_ticker = ["AMD", "AAPL"]
crypto_ticker = 'BTC'

# Can be changed to a more desired location
env_location = '../Data/.env'


def main():
    sys.path.append(
        './Src/')
    ####################### IMPORTS ##########################################

    # Personal Modules
    # from read_config import export_variables
    # from Email.email_test import send_email
    # from data_analysis import stock_report
    # from crypto_data_collection import get_close_data
    # from arima_test import arima_prediction
    # import Collection_Preprocess.stock_sources
    # from Analysis.random_walk import random_walk_benchmark
    # from Analysis.default_analysis import default_analysis, plot_dataframe, plot_dataframe
    from Collection_Preprocess.new_data import Stock_Data, Crypto_Data

    # Personal information to be used in the program
    # email, password, crypto_api = read_config.export_variables(
    #     env_location)

    ####################### Stock Data ######################################
    only_close_stock_df = pd.DataFrame(Stock_Data(
        stock_ticker).get_long_period_raw_df(period="2y").Close)
    print(only_close_stock_df)
    # stock_df = stock_sources.long_period_df(stock_ticker)
    # stock_close_df = stock_sources.only_close(stock_df)

    ####################### Stock Predictions ###############################
    # print("Training the Model")
    # stock_train_prediction_mse, stock_prediction_df = arima_prediction(
    #     stock_close_df)

    ###################### Stock Benchmark #################################

    # stock_prediction_benchmark_mse = random_walk_benchmark(stock_close_df)

    # stock_report = stock_report(stock_ticker)
    ####################### Crypto Data ####################################

    # end = datetime.date.today()
    # 2 Years according to stock data
    # start = end - datetime.timedelta(days=505)
    # crypto_close_df = get_close_data(crypto_ticker, start, end, crypto_api)

    ####################### Crypto Predictions ###############################

    # crypto_train_prediction_mse, crypto_prediction = arima_prediction(
    #     crypto_close_df
    # )
    # crypto_prediction_mse, crypto_prediction = arima_prediction(
    #     crypto_close_df)

    ###################### Crypto Prediction Benchmark #######################

    # crypto_prediction_benchmark_mse = random_walk_benchmark(crypto_close_df)

    # good_stock_prediction = False
    # good_crypto_prediction = False

    # good_stock_prediction = True if stock_train_prediction_mse < stock_prediction_benchmark_mse else False
    # good_crypto_prediction = True if crypto_train_prediction_mse < crypto_prediction_benchmark_mse else False

    # print('\n\n\n')
    # print(f"Good Stock Prediction: {good_stock_prediction}")

    # print(f"Good Crypto Prediction: {good_crypto_prediction}")

    # If stock_train_prediction_mse IS LESS than random_walk_benchmark, then use it.
    # Else Don't and only email the user moving averages graph

    ####################### Default Analysis ################################

    # current_stock_price = stock_sources.current_price(stock_ticker)

    # DEFAULT
    # stock_analysis_df = default_analysis(
    # stock_prediction_df, current_stock_price).copy()

#     crypto_default_analysis = default_analysis(
#         crypto_prediction, current_crypto_price)

    # Crypto Data probably will only show daily results
    # current_crypto_price = pd.DataFrame(crypto_close_df[-1])
    # print(current_crypto_price)
    # print(crypto_close_df)
    # crypto_default_analysis = default_analysis(
    #     crypto_close_df['Close'], current_crypto_price)
    # print(f"Default Crypto Analysis Says: {crypto_default_analysis}")

    ####################### STRATEGY #######################################

    # If this is True, email them everything

    ####################### EMAIL ##########################################

    # Should contain: MSEs, Predictions, Current Price, Moving Average Chart
    # If no move to be made, moving averaage chart should be sent regardless along with a different title
    # If the predicted price is close to the 50 day or 100 ma, then email.
    # conditions = [
    # good_stock_prediction == True and stock_default_analysis_response == True
    # crypto_default_analysis == True
    # ]

    # Stock Graphs
    # plot_dataframe(stock_ticker, stock_analysis_df)
    # plot_dataframe_zoomed(stock_ticker, stock_analysis_df)

    # Crypto Graphs
    # plot_dataframe(crypto_ticker, crypto_prediction)
    # plot_dataframe_zoomed(crypto_ticker, crypto_prediction)

    # SENDING THE ACTUAL EMAIL
    # send_email(email, password)

    # print(f'\nPredicted Prices and Moving Averages for {stock_ticker}\n')
    # print(stock_analysis_df.tail(10))
    # print("---------------------------------------------------------")
    # print(f"\nRandom Walk RMSE: {stock_prediction_benchmark_mse}")
    # print(f"ARIMA Train RMSE: {stock_train_prediction_mse}")


if __name__ == "__main__":
    main()
