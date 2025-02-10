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
pesi= [0.33,0.33,0.33]


# Download historical stock data
stocks = yf.download(tickers, start="2018-01-01")["Close"]
stocks=stocks.interpolate(method="time")
#####
portafogli = pd.DataFrame(index=stocks.index)
componenti = stocks[tickers].dropna()
performance = (componenti.shift(-12*5)/componenti)**(1/5)-1
performance_indice = pd.DataFrame(np.dot(performance, pesi), index=performance.index, columns=["aa"])
portafogli["aa"]=performance_indice.dropna()

#plot portafolgio
st.line_chart(portafogli)
st.write(portafogli.describe())
######

# Plot stock closing prices
stocks=( stocks/stocks.iloc[0] )*100
st.subheader("Stock Price Chart")
st.line_chart(stocks)

# Display raw historical data
st.subheader("Describe")
#st.dataframe(stocks)
st.write(stocks.describe())


