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

        value_series = portfolio_value_over_time(price_data, shares)

        st.subheader("Portfolio Value Over Time")

        import plotly.graph_objects as go

        value_df = value_series.reset_index()
        value_df.columns = ["Date", "Portfolio Value"]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=value_df["Date"],
                y=value_df["Portfolio Value"],
                mode="lines",
                name="Portfolio Value",
                line=dict(width=2),
                hovertemplate="%{x|%b %d, %Y}<br>$%{y:,.2f}<extra></extra>",
            )
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=450,
            hovermode="x unified",
            xaxis_title=None,
            yaxis_title="Value ($)",
            dragmode="zoom",  # click-and-drag box zoom
        )
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=[
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(step="all", label="All"),
                ]
            ),
        )
        # Scroll wheel is left off on purpose (too twitchy) - drag-to-zoom,
        # double-click to reset, and the range slider/buttons above do the rest.
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": False})


        st.subheader("Current Allocation")
        allocation = portfolio_allocation(price_data, shares)

        import pandas as pd
        allocation_df = pd.DataFrame({
            "Ticker": list(allocation.keys()),
            "Allocation %": list(allocation.values())
        })
        st.bar_chart(allocation_df.set_index("Ticker"))

        st.subheader("Risk Metrics per Stock")
        metrics_rows = []
        for ticker in tickers:
               returns = compute_daily_returns(price_data[ticker])
               vol = calculate_volatility(returns)
               sharpe = calculate_sharpe_ratio(returns)
               metrics_rows.append({
                  "Ticker": ticker,
                  "Annualized Volatility": f"{vol*100:.2f}%",
                  "Sharpe Ratio": f"{sharpe:.2f}"
              })

        st.table(metrics_rows)