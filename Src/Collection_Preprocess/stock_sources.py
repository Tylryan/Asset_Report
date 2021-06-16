#!/usr/bin/python3

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
import numpy as np


def save_image(df, title):
    df.plot(
        title=title,
        figsize=(15, 7)
    ).get_figure()

    plt.savefig('./Email/stock_image.png')


if __name__ == "__main__":
    # ticker = ['AAPL', 'TSLA']
    ticker = 'AAPL'

    # long_df = long_period_df(ticker)
    # long_close = only_close(long_df)
    # short_df = short_period_df(ticker)
    # short_close = only_close(short_df)
    # save_image(long_close, title='heller')

    cp = current_price(ticker)
    print(cp)
    # print(len(long_close))
    # print(f"\nThis is {ticker}'s 2y historical data\n")
    # print(long_df)
    # print(f"\nThis is {ticker}'s 2y historical data only close\n")
    # print(long_close)
    # print(f"\nThis is {ticker}'s 60d historical data\n")
    # print(short_df)
    # print(f"\nThis is {ticker}'s 60d historical data only close\n")
    # print(short_close)
