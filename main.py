import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.express as px
import matplotlib.pyplot as plt

#Import from ./src
from src.functions import normalize_data
from src.functions import roll_returns

# Streamlit interface elements
st.title('Stock :blue[_Portfolio_] Analysis')

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

st.write(f"We got data from {dati.dropna().index[0].strftime("%Y-%m-%d")} and {dati.dropna().index[-1].strftime("%Y-%m-%d")} ")

#normalized data
dati_normaliz = normalize_data(dati)
st.subheader("Display price normalized data")
dati_normaliz

#normalized data - chart
st.subheader("Data price normalization graph")
dn_chart=px.line(dati_normaliz, title='normalization data')
dn_chart.update_layout(hovermode="x unified")
st.plotly_chart(dn_chart, use_container_width=True)

#rolling ret
portafogli=pd.DataFrame()
anni=8
portafogli=roll_returns(portafogli,anni,dati, tickers,pesi)
st.subheader("Display portfolio annualized return on {anni} years")
portafogli
st.write(
    pd.DataFrame(
        [
            {"start date": portafogli.index ,"end date":1, "return": portafogli.dropna().iloc[0] },
           # {"option": "mean of return", "value": (portafogli.dropna().describe().iloc[1])*100 },
           # {"option": "standard deviation", "value": (portafogli.dropna().describe().iloc[2])*100 },
        ]
    )
)

#rolling ret - line chart
st.subheader("Rolling return graph on {anni} years")
rollretlinechart=px.line(portafogli.dropna(), title='rolling ret')
rollretlinechart.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
rollretlinechart.update_layout(hovermode="x unified")
rollretlinechart.layout.yaxis.tickformat = ',.0%'
st.plotly_chart(rollretlinechart, use_container_width=True)



#rolling ret - hist chart
st.subheader("Rolling return :green[histogram] on {anni} years")
hist = px.histogram(portafogli.dropna(), 
    opacity=0.4, nbins=80, 
    title="Histogram of Portfolio Returns"
)
hist.update_layout(hovermode="x unified")
hist.add_vline(x=0, line_dash="dash", line_color="red", line_width=2)
hist.layout.xaxis.tickformat = ',.0%'
st.plotly_chart(hist, use_container_width=True)


#describe portfogli
st.write("### Portfolio Statistics")
#st.write(portafogli.dropna().describe())
st.write(
    pd.DataFrame(
        [
            {"option": "number of periods" , "value": portafogli.dropna().describe().iloc[0] },
            {"option": "mean of return", "value": (portafogli.dropna().describe().iloc[1])*100 },
            {"option": "standard deviation", "value": (portafogli.dropna().describe().iloc[2])*100 },
        ]
    )
)

st.subheader(" max Drawdown")
#st.write( round(portafogli.dropna().quantile([0.0])*100,2).iloc[1,1] ) 

st.write(round(portafogli.dropna().quantile([0.0])*100,2))

###############
#value = dataframe.iloc[2, 1]  # get valueo in Row index 2, Column index 1


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