import yfinance as yf


def fetch_price_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


def compute_daily_returns(price_df):
    returns = price_df["Close"].pct_change().dropna()
    return returns
