#!/usr/bin/python3

from Functions import stock_sources
import pandas as pd
# You will need to create something that works for only one stock
# I made it a set to remove duplicates

# TODO Here i would like to add a path to a csv file to use for tickers


def stock_report(ticker):
    try:
        long_period = stock_sources.long_period_df(ticker)

        short_period = stock_sources.short_period_df(ticker)

        # Find the current price

        current_price = stock_sources.only_close(short_period)[ticker][-1:]
    except Exception as e:
        print(f"Error: {e}")
    # print(current_price)

    # # Find the 200 day moving average.

    two_hundred_day_ma = stock_sources.only_close(
        long_period
    ).rolling(window=200).mean().iloc[-1:, :]

    # If a stock's 200ma > it's current price, then print true
    for stock, price in two_hundred_day_ma.items():
        report = pd.DataFrame(
            {
                'Current': [1],
                '200 ma': [1]
            }, index=ticker
        )
        # Print statements test to make sure the values are correct
        # print(price.values)
        # print(current_price[stock].values)

        # If the 200 ma is greater than the current price add it to the list to email.
        if price.values > current_price[stock].values:
            # print(f'{stock}\'s Current Price is BELOW its\'s 200 ma')
            report.loc[stock, 'Current'] = round(
                current_price[stock].values[0], 2)
            report.loc[stock, '200 ma'] = round(price.values[0], 2)
            # Give me only the stocks that have a lower current value than the 200ma
            mask = report['Current'] != 1

            report_to_email = report[mask]
            report_to_email.sort_index(inplace=True)
            report_to_email = report_to_email.to_html(
                notebook=True)
            return report_to_email

        else:
            pass
            # print(f'{stock}\'s Current Price is ABOVE its\'s 200 ma')
    # print(y.values)


if __name__ == '__main__':
    ticker = 'AAPL'
    ticker = {'AAPL', 'TSLA', 'PLUG', 'AMZN', 'AMZN', "LSD", "WPG"}
    print(stock_report(ticker))
