def portfolio_value_over_time(price_data, holdings):
    """
    price_data: dict like {"AAPL": price_dataframe, "TSLA": price_dataframe}
    holdings: dict like {"AAPL": 10, "TSLA": 5}  (number of shares)
    Returns: a single Series representing total portfolio value per day
    """
    total_value = None
    for ticker, shares in holdings.items():
        if ticker in price_data:
            stock_value = price_data[ticker]["Close"] * shares
            if total_value is None:
                total_value = stock_value
            else:
                total_value = total_value.add(stock_value, fill_value=0)
    return total_value


def portfolio_allocation(price_data, holdings):
    latest_values = {}
    for ticker, shares in holdings.items():
        if ticker in price_data:
            latest_price = price_data[ticker]["Close"].iloc[-1]
            latest_values[ticker] = latest_price * shares

    total = sum(latest_values.values())
    if total == 0:
        return {}
    allocation = {
        ticker: (value / total) * 100
        for ticker, value in latest_values.items()
    }
    return allocation


if __name__ == "__main__":
    from data_utils import fetch_price_data

    holdings = {"AAPL": 10, "TSLA": 5}
    price_data = {
        ticker: fetch_price_data(ticker, "2024-01-01", "2024-02-01")
        for ticker in holdings
    }

    # Portfolio value over time
    value_series = portfolio_value_over_time(price_data, holdings)
    print("Portfolio value over time (last 5 days):")
    print(value_series.tail())

    # Portfolio allocation (latest day)
    allocation = portfolio_allocation(price_data, holdings)
    print("\nPortfolio allocation (%):")
    print(allocation)

    # Diagnostic checks (replaces the `python3 -c ...` call)
    df = fetch_price_data("AAPL", "2024-01-01", "2024-01-10")
    print("\nDiagnostic for AAPL:")
    print("Columns:", df.columns.tolist())
    print("Type of df['Close']:", type(df["Close"]))
    print("Last close price:", df["Close"].iloc[-1])