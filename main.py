import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf

#Import from ./src
from src.functions import normalize_data
from src.functions import roll_returns

# Streamlit interface elements
st.title('Stock Portfolio Analysis')

# Input tickers and weights
tickers_input = st.text_input("Enter tickers (comma separated)", "SPEA.BE,MSTR")
tickers = [ticker.strip() for ticker in tickers_input.split(",")]

weights_input = st.text_input("Enter weights (comma separated)", "0.4,0.6")
try:
    pesi = [float(x.strip()) for x in weights_input.split(",")]
except ValueError:
    st.error("Invalid weight format. Please enter numbers separated by commas.")
    st.stop()

# Validate tickers
tickers_validi = []
for ticker in tickers:
    info = yf.Ticker(ticker).history(period="1mo")
    if not info.empty:
        tickers_validi.append(ticker)
    else:
        st.warning(f"⚠️ Ticker '{ticker}' not found or has no data. It will be ignored.")

if not tickers_validi:
    st.error("❌ No valid tickers found. Please enter at least one valid ticker.")
    st.stop()

# Validate weights sum
if len(pesi) != len(tickers_validi):
    st.error("❌ Number of weights does not match the number of valid tickers. Please adjust.")
    st.stop()

if sum(pesi) != 1:
    st.error(f"❌ The sum of weights must be 1. Current sum: {sum(pesi)}. Please adjust your weights.")
    st.stop()


dati = yf.download(tickers_validi, interval='1mo')["Close"]
dati = dati.reindex(tickers_validi, axis=1)
dati.fillna(method="ffill", limit=1, inplace=True)
# Apply data normalization
dati_normaliz = normalize_data(dati)
# Display normalized data + line chart
dati_normaliz
st.line_chart(dati_normaliz)

#rolling ret
portafogli=pd.DataFrame()
portafogli=roll_returns(portafogli,8,dati, tickers,pesi)
portafogli
#todo: add "data between xxx e yyyy"
st.line_chart(portafogli.dropna())

# Streamlit app title
#st.title("Stock Portfolio Performance App")

# Initialize session state for tickers and weights
#if "tickers" not in st.session_state:
#     st.session_state.tickers = []
# if "weights" not in st.session_state:
#     st.session_state.weights = []

# # User input for ticker symbol
# #ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):").upper()
# #weight = st.number_input("Enter Weight (0-1):", min_value=0.0, max_value=1.0, value=0.1)

# # Button to add ticker and weight
# if st.button("Add Ticker"):
#     if ticker and weight > 0:
#         st.session_state.tickers.append(ticker)
#         st.session_state.weights.append(weight)

# # Display the current tickers and weights
# st.subheader("Current Portfolio")
# if st.session_state.tickers:
#     portfolio_df = pd.DataFrame({"Ticker": st.session_state.tickers, "Weight": st.session_state.weights})
#     st.dataframe(portfolio_df)

# # Calculate portfolio when button is pressed
# if st.button("Calculate Portfolio"):
#     if not st.session_state.tickers:
#         st.warning("Please add at least one ticker before calculating.")
#     else:
#         # Normalize weights to sum to 1
#         pesi = np.array(st.session_state.weights, dtype=float)
#         pesi /= pesi.sum()  # Ensure weights sum to 1

#         # Download stock data
#         stocks = yf.download(st.session_state.tickers, start="2018-01-01")["Close"]

#         # Ensure stocks data is numeric
#         componenti = stocks.dropna()
#         performance = (componenti.shift(-12*5) / componenti) ** (1/5) - 1
#         performance = performance.astype(float)  # Convert to numeric

#         # Compute weighted performance index
#         performance_indice = pd.DataFrame(np.dot(performance, pesi), index=performance.index, columns=["Portfolio Return"])
#         portafogli = pd.DataFrame(index=stocks.index)
#         portafogli["Portfolio Return"] = performance_indice.dropna()

#         # Display results
#         st.subheader("Portfolio Performance Chart")
#         st.line_chart(portafogli)
        
#         hist_values = np.histogram(
#             portafogli["Portfolio Return"].dropna(), bins=30)

# #        st.bar_chart(hist_values)
# #        
# #        st.subheader("Portfolio Data")
# #        st.dataframe(portafogli)
#