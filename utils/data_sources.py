import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web


def retrieve_us_yield_data() -> pd.DataFrame:
    _start = "1990-01-01"
    _tickers = ["GS30", "GS10", "GS5", "GS3", "GS2", "GS1", "GS6m", "GS3m", "GS1m"]
    df = pdr.get_data_fred(_tickers, _start)
    df.columns = [
        "30-year",
        "10-year",
        "5-year",
        "3-year",
        "2-year",
        "1-year",
        "6-month",
        "3-month",
        "1-month",
    ]
    df.index = df.index + pd.offsets.MonthEnd(0)
    df.to_csv("../data/fed_yc.csv", header=True, index=True)
    return df


def get_us_yield_data() -> pd.DataFrame:
    df = pd.read_csv("data/fed_yc.csv", index_col=0)
    df.index = pd.to_datetime(df.index)
    return df


def get_uk_yield_curve_data() -> pd.DataFrame:
    df = pd.read_csv("data/boe_yc.csv", index_col = 0)
    df.index = pd.to_datetime(df.index)
    return df
