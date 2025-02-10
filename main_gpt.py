import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf

# Streamlit app title
st.title("Stock Portfolio Performance App")

# User input for stock tickers
tickers = st.text_input("Enter stock tickers (comma-separated):", "AAPL, MSFT, GME")

# Convert input string to a list
tickers = [ticker.strip().upper() for ticker in tickers.split(",") if ticker.strip()]

if tickers:
    # Download stock data
    stocks = yf.download(tickers, start="2018-01-01")["Close"]

    # User input for weights
    st.subheader("Set Portfolio Weights")
    pesi = []
    for ticker in tickers:
        weight = st.number_input(f"Weight for {ticker} (0-1)", min_value=0.0, max_value=1.0, value=1/len(tickers))
        pesi.append(weight)

    # Normalize weights to sum to 1
    pesi = np.array(pesi, dtype=float)
    pesi /= pesi.sum()  # Ensure weights sum to 1

    # Ensure stocks data is numeric
    componenti = stocks.dropna()
    performance = (componenti.shift(-12*5) / componenti) ** (1/5) - 1
    performance = performance.astype(float)  # Convert to numeric

    # Compute weighted performance index
    performance_indice = pd.DataFrame(np.dot(performance, pesi), index=performance.index, columns=["Portfolio Return"])
    portafogli = pd.DataFrame(index=stocks.index)
    portafogli["Portfolio Return"] = performance_indice.dropna()

    # Display results
    st.subheader("Portfolio Performance Chart")
    st.line_chart(portafogli)

    st.subheader("Portfolio Data")
    st.dataframe(portafogli)

else:
    st.warning("Please enter at least one stock ticker.")
