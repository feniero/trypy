import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf

tickets=["AAPL"]
stocks=yf.download(tickets,start="2018-01-01")["Close"]
stocks.plot(figsize=(20,10))
st.write(stocks.plot(figsize=(20,10)))




#st.write("Here's our first attempt at using data to create a table:")
#st.write(pd.DataFrame({
#    'first column': [1, 2, 3, 4],
#    'second column': [10, 20, 30, 40]
#}))