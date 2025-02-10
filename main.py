import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf

import streamlit as st
import yfinance as yf
import pandas as pd

# Streamlit app title
st.title("Stock Price App")

# User input for ticker symbol
#ticker = st.text_input("Enter Stock Ticker:", "AAPL")

# Fetch data from yfinance
ticker=["AAPL","ENI.MI","F","MSFT","T","NIO","EPD","GME","GGB","BB"]
if ticker:
    stocks=yf.download(ticker,start="2018-01-01")["Close"]

    # Display stock information
    #st.write(f"## {stock.info['shortName']}")
    #st.write(f"**Industry:** {stock.info.get('industry', 'N/A')}")
    #st.write(f"**Market Cap:** {stock.info.get('marketCap', 'N/A'):,}")

    # Plot stock closing price
    st.subheader("Stocks Price Chart")
    st.line_chart(stocks["Close"])

    # Display raw data
    st.subheader("Historical Data (Last 1 Month)")
    st.dataframe(stocks)

