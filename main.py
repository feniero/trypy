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

## normalized data
dati_normaliz = normalize_data(dati)
st.subheader("Display price normalized data")
dati_normaliz

## normalized data - chart
dn_chart=px.line(dati_normaliz, title='normalization data chart')
dn_chart.update_layout(hovermode="x unified")
st.plotly_chart(dn_chart, use_container_width=True)

## rolling ret
portafogli=pd.DataFrame()
anni=8
#return each period
portafogli=roll_returns(portafogli,anni,dati, tickers,pesi)

st.subheader(f"Display portfolio :green[annualized return] on {anni} years")
st.info('The column "annualized return over period %" are alerady a % value', icon="ℹ️")
start_dates = portafogli.index
end_dates = start_dates + pd.DateOffset(years=anni)
returns = portafogli

results = pd.DataFrame({
    #"start date": start_dates,
    "end period date": end_dates,
    "annualized return over period %": returns*100
})
st.dataframe(results)

## rolling ret - line chart
rollretlinechart=px.line(portafogli.dropna(), title='rolling return')
rollretlinechart.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
rollretlinechart.update_layout(hovermode="x unified")
rollretlinechart.layout.yaxis.tickformat = ',.0%'
st.plotly_chart(rollretlinechart, use_container_width=True)



#rolling ret - hist chart
hist = px.histogram(portafogli.dropna(), 
    opacity=0.4, nbins=80, 
    title="Histogram of Portfolio Returns"
)
hist.update_layout(hovermode="x unified")
hist.add_vline(x=0, line_dash="dash", line_color="red", line_width=2)
hist.layout.xaxis.tickformat = ',.0%'
st.plotly_chart(hist, use_container_width=True)


## Portfolio Statistics
st.write("### Portfolio Statistics")
#st.write(portafogli.dropna().describe())
st.write(
    pd.DataFrame(
        [
            {"Data over period": "number of periods" , "value": portafogli.dropna().describe().iloc[0] },
            {"Data over period": "mean of return", "value": (portafogli.dropna().describe().iloc[1])*100 },
            {"Data over period": "median of return", "value": (portafogli.dropna().describe().iloc[5])*100 },
            {"Data over period": "standard deviation", "value": (portafogli.dropna().describe().iloc[2])*100 },
            {"Data over period": "Max return", "value": (portafogli.dropna().describe().iloc[7])*100 },
            {"Data over period": "Min return", "value": (portafogli.dropna().describe().iloc[3])*100 }
        ]
    )
)

## Drawdown
st.subheader(":red[Drawdown] Statistics")
#round(portafogli.dropna().quantile([0.0,0.1])*100,2)
st.write(
    pd.DataFrame(
        [
            {"Data over period": "max drawdown" , "value": ( round(portafogli.dropna().quantile(0.0)*100,2) ) },
            {"Data over period": "10% quantile", "value": round(portafogli.dropna().quantile(0.1)*100,2)  },
            {"Data over period": "mean return on 10% quantile", "value": round(portafogli.dropna()[portafogli.dropna()<=portafogli.dropna().quantile(0.1)].mean()*100,2)  },
            {"Data over period": "5% quantile", "value": round(portafogli.dropna().quantile(0.05)*100,2)  },
            {"Data over period": "mean return on 5% quantile", "value": round(portafogli.dropna()[portafogli.dropna()<=portafogli.dropna().quantile(0.05)].mean()*100,2)  }
        ]
    )
)


## sharpRatio
st.subheader("Sharp Ratio")
rendimento_bond_a_n_anni=0.045
st.write(
    round(  (portafogli.dropna().mean()-rendimento_bond_a_n_anni)/portafogli.dropna().std() , 3)
)
