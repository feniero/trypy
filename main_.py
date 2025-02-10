import streamlit as st
import yfinance as yf
import pandas as pd

import numpy.matlib
import numpy as np

# Streamlit app title
st.title("Stock Price App")

# List of predefined stock tickers
#tickers = ["AAPL", "ENI.MI", "F", "MSFT", "T", "NIO", "EPD", "GME", "GGB", "BB"]

# User input for ticker symbol
tickers = st.text_input("Enter stock tickers (pointcomma-separated):", "AAPL; MSFT; GME")
tickers = [ticker.strip().upper() for ticker in tickers.split(";") if ticker.strip()]

#percentage
pesi = st.text_input("Enter percentage (pointcomma-separated):", "0.33; 0.33; 0.33")
pesi = [perc.strip().upper() for perc in pesi.split(";") if perc.strip()]


# Download historical stock data
stocks = yf.download(tickers, start="2018-01-01")["Close"]
stocks=stocks.interpolate(method="time")
#####
######

# Plot stock closing prices
stocks=( stocks/stocks.iloc[0] )*100
st.subheader("Stock Price Chart")
st.line_chart(stocks)

# Display raw historical data
st.subheader("Describe")
#st.dataframe(stocks)
st.write(stocks.describe())


