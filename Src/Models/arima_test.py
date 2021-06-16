#!/usr/bin/python

import sys
import warnings
from sklearn.metrics import mean_squared_error
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
import datetime
from pprint import pprint
from statsmodels.tsa.arima_model import ARIMA
sys.path.append("../")
warnings.filterwarnings('ignore')

######################## GETTING DATA ################################
# Creating the initial dataframe with a bunch of information

# TODO This will inherit from an original df stock or crypto

# TODO Split this up into Train Test Predict


class arima():

    def get_optimal_order(self, close_df, test_percent=0.8):

        ######################## SPLITTING THE DATA ##########################
        original_close_df = close_df
        close_df = close_df.pct_change().dropna()
        # Creating a train test split
        observances = len(close_df)
        # Train consists of the first 80% of the close df
        train = close_df.iloc[:math.ceil(
            observances * test_percent), :]
        # Test Consists of last 20% of the close df
        test = close_df.iloc[math.ceil(
            observances * test_percent):, :]

        ######################## OPTIMAL ORDER FOR TRAINING DATA #############
        best_order = []

        for d in range(0, 3):
            for q in range(1, 5):
                for p in range(1, 5):
                    order = (p, d, q)
                    # Using the Training data in this case to find the best order
                    model = ARIMA(
                        np.array(train), order=order)
                    try:

                        # Fit the model and assign it to a variable called results
                        results = model.fit(disp=0)
                    except Exception as e:
                        print(e)
                    # This is one of the performance indicators.
                    # The other one is MSE
                    aic = results.aic
                    order_results = (aic, order)
                    best_order.append(order_results)

        print("Done Training")
        # Sort the orders by AIC and give me
        best_order = sorted(best_order)
        optimal_order = best_order[0][1]
        second_best_order = best_order[1][1]
        self.optimal_order = optimal_order
        self.second_best_order = second_best_order
        self.train = train
        self.test = test
        self.original_close = original_close_df

        return best_order

        ########################## TRAINING DATA ################################

    def train_model(self):
        # TODO Try one. If it doesn't work, try the other
        train_model = ARIMA(self.train, order=self.optimal_order)

        train_results = train_model.fit(disp=0)
        train_score = train_results.summary()
        train_forecast = pd.DataFrame(
            train_results.forecast(len(self.test))[0],
            columns=['Close']
        )

        # Add the predicted returns to the actual returns dataframe
        train_predictions = self.train.append(train_forecast)
        train_predictions['Predicted Returns'] = train_predictions['Close']
        # train_predictions.drop(columns='Close', inplace=True)
        # Create a cumulative returns column
        all_actual_prices_df = pd.DataFrame(self.original_close[1:])
        train_predictions['Predicted Price'] = (
            1 + train_predictions['Predicted Returns']).cumprod() * all_actual_prices_df.Close.values[0]
        # Getting the actual prices to compare to the predicted prices
        train_predictions['Actual Price'] = all_actual_prices_df.Close.values
        # Cutting down the predictions to only 5 days
        train_prediction_5_day = train_predictions[:-95].dropna()
        train_prediction_5_day = train_prediction_5_day[[
            'Actual Price', 'Predicted Price']]
        ######################### COMPARE TRAINING TO ACTUAL DATA #################
        # Finding the MSE of those predictions
        train_rmse = np.sqrt(mean_squared_error(
            train_prediction_5_day['Actual Price'],
            train_prediction_5_day['Predicted Price'])
        )
        self.train_rmse = train_rmse
        return train_prediction_5_day
      # ########################### TESTING DATA #################################

    def test_model(self):
        print("Starting Test")
        try:
            test_model = ARIMA(self.test, order=self.optimal_order)
            test_results = test_model.fit(disp=0)
        except Exception as e:
            print(e)
        finally:
            test_model = ARIMA(self.test, order=self.second_best_order)
            test_results = test_model.fit(disp=0)

        test_forecast = pd.DataFrame(
            test_results.forecast(5)[0],
            columns=['Close'],
            index=pd.date_range(
                start=pd.to_datetime(
                    self.test.index[-1]) + datetime.timedelta(1),
                periods=5,
                freq="D"
            )
        )

        # Add the predicted returns to the actual returns dataframe
        test_predictions = self.original_close.append(test_forecast)
        print(test_forecast)
        # Create a cumulative returns column
        # TODO This part probably wouldn't work with multiple data columns
        print(self.original_close.Close[1])

        # TODO Returns an odd number.
        test_predictions['Close'] = (
            1 + test_predictions['Close']
        ).cumprod() * self.original_close.Close[1]

        # Getting the actual prices to compare to the predicted prices
        ######################### COMPARE TRAINING TO ACTUAL DATA #################
        return test_predictions


if __name__ == '__main__':
    from Collection_Preprocess.new_data import Stock_Data, Crypto_Data

    ticker = 'AAPL'

    stock_df = Stock_Data(ticker)

    close_df = pd.DataFrame(stock_df.get_long_period_raw_df().Close)
    print(close_df)

    model = arima()
    model.get_optimal_order(close_df)
    model.train_model()
    test_prediction = model.test_model()
    print(test_prediction)

    # # print('\n\n\n\nCrypto Data')
    # ticker = 'BTC'

    # end = datetime.date.today()
    # start = end - datetime.timedelta(days=505)

    # import read_config
    # env_location = '../../Data/.env'
    # user_name, password, crypto_api = read_config.export_variables(
    #     env_location)
    # crypto_df = get_close_data(ticker, start, end, crypto_api)

    # arima_prediction(crypto_df)
