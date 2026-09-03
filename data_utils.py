import yfinance as yf
import pandas as pd


def fetch_price_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Flatten multi-level columns if present (newer yfinance versions do this)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    return data

def compute_daily_returns(price_df):
    returns = price_df["Close"].pct_change().dropna()
    return returns
