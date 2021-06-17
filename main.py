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


######################### GLOBAL VARIABLES ##################################
# Tickers to watch
stock_tickers = ["AMD", "AAPL"]
crypto_tickers = ["BTC", "ETH"]

# Can be changed to a more desired location
env_location = '../Data/.env'


def main():
    sys.path.append(
        './Src/')
    ####################### CUSTOM IMPORTS ##########################################
    from Collection_Preprocess.new_data import Stock_Data, Crypto_Data

    ###################### BRING IN DATA #####################################

    long_term_stock_data = Stock_Data(stock_tickers)

    long_term_stock_data = long_term_stock_data.get_long_period_raw_df()

    ################# STOCKS ###############################
    ldf_close = pd.DataFrame(long_term_stock_data.Close)

    ###################### FEED IT TO ARIMA #################################

    # SENDING THE ACTUAL EMAIL
    # send_email(email, password)

    # print(f'\nPredicted Prices and Moving Averages for {stock_ticker}\n')
    # print(stock_analysis_df.tail(10))
    # print("---------------------------------------------------------")
    # print(f"\nRandom Walk RMSE: {stock_prediction_benchmark_mse}")
    # print(f"ARIMA Train RMSE: {stock_train_prediction_mse}")


if __name__ == "__main__":
    main()
