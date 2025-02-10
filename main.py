import streamlit as st
import yfinance as yf
import pandas as pd

# Streamlit app title
st.title("Stock Price App")

# User input for ticker symbol
tickers = st.text_input("Enter stock tickers (pointcomma-separated):", "AAPL; MSFT; GME")
tickers = [ticker.strip().upper() for ticker in tickers.split(";") if ticker.strip()]

# List of predefined stock tickers
#tickers = ["AAPL", "ENI.MI", "F", "MSFT", "T", "NIO", "EPD", "GME", "GGB", "BB"]

# Download historical stock data
stocks = yf.download(tickers, start="2018-01-01")["Close"]
stocks=stocks.interpolate(method="time")
stocks=( stocks/stocks.iloc[0] )*100

# Plot stock closing prices
st.subheader("Stock Price Chart")
st.line_chart(stocks)

# Display raw historical data
st.subheader("Historical Data")
#st.dataframe(stocks)
st.write(stocks.describe())


