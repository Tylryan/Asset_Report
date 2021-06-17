#!/usr/bin/python

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
import warnings
import sys
sys.path.append("../../Src/")

warnings.filterwarnings('ignore')

######################## GETTING DATA ################################
# Creating the initial dataframe with a bunch of information

# TODO This will inherit from an original df stock or crypto

# TODO Right now, the column must be called "Close". Make it to where a column with any name could be used.
# Also the column name coming in should be unaffected by the arima model.


class arima():
    """
    Takes in a dataframe of asset closing prices and returns a dataframe \n
    of that cointains the original closing prices in addition to a 5 day \n
    forecast.

    """

    def get_optimal_order(self, close_df, test_percent=0.8):
        """
        Takes in a dataframe of only closing prices. There can be as many \n
        columns as you'd like.

        Returns the optimal order for the ARIMA model.
        """

        print("Starting Training")

        ######################## SPLITTING THE DATA ##########################
        original_close_df = close_df
        print("\n\nDATA GOING IN")
        print(original_close_df)
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

        # Sort the orders by AIC and give me
        best_order = sorted(best_order)
        optimal_order = best_order[0][1]
        second_best_order = best_order[1][1]
        self.optimal_order = optimal_order
        self.second_best_order = second_best_order
        self.train = train
        self.test = test
        self.original_close = original_close_df
        self.percent_close = close_df

        return best_order

        ########################## TRAINING DATA ################################

    def train_model(self):
        # TODO Try one. If it doesn't work, try the other
        train_model = ARIMA(self.train, order=self.optimal_order)

        train_results = train_model.fit(disp=0)
        train_score = train_results.summary()
        train_forecast = pd.DataFrame(
            train_results.forecast(len(self.test))[0],
            columns=self.original_close.columns
        )

        # Add the predicted returns to the actual returns dataframe
        train_predictions = self.train.append(train_forecast)
        # This is taking information from the Close column
        train_predictions['Predicted Returns'] = train_predictions.iloc[:, 0]
        # train_predictions.drop(columns='Close', inplace=True)
        # Create a cumulative returns column
        all_actual_prices_df = pd.DataFrame(self.original_close[1:])
        train_predictions['Predicted Price'] = (
            1 + train_predictions['Predicted Returns']).cumprod() * all_actual_prices_df.iloc[:, 0].values[0]
        # Getting the actual prices to compare to the predicted prices
        train_predictions['Actual Price'] = all_actual_prices_df.iloc[:, 0].values
        # Cutting down the predictions to only 5 days
        train_prediction_5_day = train_predictions[:-95].dropna()
        train_prediction_5_day = train_prediction_5_day[[
            'Actual Price', 'Predicted Price']]
        ######################### COMPARE TRAINING TO ACTUAL DATA #################
        # Finding the MSE of that 5 day prediction
        train_rmse = np.sqrt(mean_squared_error(
            train_prediction_5_day['Actual Price'],
            train_prediction_5_day['Predicted Price'])
        )
        self.train_results = train_prediction_5_day
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
        # finally:
        #     test_model = ARIMA(self.test, order=self.second_best_order)
        #     test_results = test_model.fit(disp=0)

        test_forecast = pd.DataFrame(
            test_results.forecast(5)[0],
            columns=self.original_close.columns,
            index=pd.date_range(
                # Start = last actual day plus 1
                start=pd.to_datetime(
                    self.test.index[-1]) + datetime.timedelta(1),
                periods=5,
                freq="D"
            )
        )

        # Add the predicted returns to the actual returns dataframe
        test_predictions = self.percent_close.append(test_forecast)
        # Create a cumulative returns column
        # TODO This part probably wouldn't work with multiple data columns

        # TODO Returns an odd number.
        test_predictions[self.original_close.columns] = (
            1 + test_predictions[self.original_close.columns]
        ).cumprod() * self.original_close.iloc[1, 0]

        # Getting the actual prices to compare to the predicted prices
        ######################### COMPARE TRAINING TO ACTUAL DATA #################
        print("DATA COMMING OUT OF ARIMA")
        print(test_predictions)
        return test_predictions


class arima_predictions():
    """
    This class is easier to use as a user.
    """

    def run_one_time(self, closing_df):
        """ 
        Takes in a dataframe containing the closing price of a single stock.
        Returns the same dataframe with predictions appended to each column.
        """
        # 1. Find the closing price of the first stock in the dataframe.
        first_stock = pd.DataFrame(closing_df.iloc[:, 0])
        # 2. Run the entire arima model on it.
        model = arima()
        model.get_optimal_order(first_stock)
        model.train_model()
        # 3. Return the predictions
        test_predictions = model.test_model()
        return test_predictions

    def run_multiple_tests(self, closing_df):
        """
        Takes in a dataframe containing the closing prices of more than on stock
        Returns the same dataframe with predictions appended to each column.
        """
        # 1. Find the closing price of the first stock in the dataframe.
        first_stock = pd.DataFrame(closing_df.iloc[:, 0])
        # 2. Run the entire arima model on it.
        model = arima()
        model.get_optimal_order(first_stock)
        model.train_model()
        # 3. Return the predictions
        test_predictions = model.test_model()

        # We are going to do the same with the rest of the dataframe.
        # We are going to append the others to the test_predictions dataframe
        for ticker in tickers[1:]:
            # Reinitialize the Stock_data class.
            # Harder to override the original. Easier to just do this.
            stock_df = Stock_Data(ticker)

            # Get a long period of only close information
            close_df = pd.DataFrame(stock_df.get_long_period_raw_df().Close)

            # Also need to reinstantiate the arima model
            model = arima()
            model.get_optimal_order(close_df)
            model.train_model()
            test_prediction = model.test_model()
            print(model.train_rmse)
            test_predictions[ticker] = test_prediction.iloc[:, 0]
        return test_predictions


if __name__ == '__main__':
    import sys
    sys.path.append("../../Src/")

    from Collection_Preprocess.new_data import Stock_Data, Crypto_Data

##################### WORKING STOCK EXAMPLE ##################################
    # Use this in main.py

    tickers = ["AAPL", "GOOGL", "AMZN"]

    # Get in all the stock data
    stocks_df = pd.DataFrame(Stock_Data(
        tickers).get_long_period_raw_df().Close)
    print("STOCK DATA GOING IN")
    print(stocks_df)

    stock_predictions = arima_predictions()
    stock_predictions = stock_predictions.run_multiple_tests(stocks_df)
    print("STOCK DATA COMING OUT")
    print(stock_predictions)


##################### Crypto EXAMPLE ###################################

    # print('\n\n\n\nCrypto Data')
    # tickers = ["BTC", "ETH"]

    # end = datetime.date.today()
    # start = end - datetime.timedelta(days=505)

    # import read_config
    # env_location = '../../Data/.env'
    # user_name, password, crypto_api = read_config.export_variables(
    #     env_location)
    # crypto_data_df = Crypto_Data(crypto_api)
    # crypto_data_df = crypto_data_df.get_multiple_close_df(tickers)
    # print(crypto_data_df)

    # arima_prediction(crypto_df)
