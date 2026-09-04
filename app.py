import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Portfolio Risk Analyzer", layout="wide")
st.title("Stock Portfolio Analyzer with Risk Metrics")

# Sidebar inputs
st.sidebar.header("Portfolio Setup")

tickers_input = st.sidebar.text_input(
    "Enter tickers (comma-separated)", value="AAPL,TSLA"
)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

start_date = st.sidebar.date_input("Start date", date.today() - timedelta(days=365))
end_date = st.sidebar.date_input("End date", date.today())

st.write("Tickers entered:", tickers)
st.write("Date range:", start_date, "to", end_date)


from data_utils import fetch_price_data, compute_daily_returns
from risk_metrics import calculate_volatility, calculate_sharpe_ratio
from portfolio_utils import portfolio_value_over_time, portfolio_allocation

st.sidebar.subheader("Shares per stock")
shares = {}
for ticker in tickers:
    shares[ticker] = st.sidebar.number_input(f"Shares of {ticker}", min_value=0, value=10)

run_button = st.sidebar.button("Analyze Portfolio")

if run_button:
    with st.spinner("Fetching data..."):
        price_data = {
            ticker: fetch_price_data(ticker, str(start_date), str(end_date))
            for ticker in tickers
        }

    st.success("Data fetched!")
    for ticker in tickers:
        st.write(f"{ticker} last close price:", price_data[ticker]["Close"].iloc[-1])

