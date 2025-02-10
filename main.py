import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf

# Streamlit app title
st.title("Stock Portfolio Performance App")

# Initialize session state for tickers and weights
if "tickers" not in st.session_state:
    st.session_state.tickers = []
if "weights" not in st.session_state:
    st.session_state.weights = []

# User input for ticker symbol
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):").upper()
weight = st.number_input("Enter Weight (0-1):", min_value=0.0, max_value=1.0, value=0.1)

# Button to add ticker and weight
if st.button("Add Ticker"):
    if ticker and weight > 0:
        st.session_state.tickers.append(ticker)
        st.session_state.weights.append(weight)

# Display the current tickers and weights
st.subheader("Current Portfolio")
if st.session_state.tickers:
    portfolio_df = pd.DataFrame({"Ticker": st.session_state.tickers, "Weight": st.session_state.weights})
    st.dataframe(portfolio_df)

# Calculate portfolio when button is pressed
if st.button("Calculate Portfolio"):
    if not st.session_state.tickers:
        st.warning("Please add at least one ticker before calculating.")
    else:
        # Normalize weights to sum to 1
        pesi = np.array(st.session_state.weights, dtype=float)
        pesi /= pesi.sum()  # Ensure weights sum to 1

        # Download stock data
        stocks = yf.download(st.session_state.tickers, start="2018-01-01")["Close"]

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
