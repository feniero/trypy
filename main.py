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
ticker = st.text_input("Enter Stock Ticker:", "AAPL")

# Fetch data from yfinance
if ticker:
    stock = yf.Ticker(ticker)
    
    # Get historical market data
    hist = stock.history(period="1mo")

    # Display stock information
    st.write(f"## {stock.info['shortName']}")
    st.write(f"**Industry:** {stock.info.get('industry', 'N/A')}")
    st.write(f"**Market Cap:** {stock.info.get('marketCap', 'N/A'):,}")

    # Plot stock closing price
    st.subheader("Stock Price Chart (Last 1 Month)")
    st.line_chart(hist["Close"])

    # Display raw data
    st.subheader("Historical Data (Last 1 Month)")
    st.dataframe(hist)

