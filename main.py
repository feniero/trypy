import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.express as px
import matplotlib.pyplot as plt

#Import from ./src
from src.functions import normalize_data
from src.functions import roll_returns


st.title('Stock :blue[_Portfolio_] Analysis')

# Input tickers, weights, years, and risk-free return
try:
    # Tickers Input
    tickers_input = st.text_input("Enter tickers (comma separated)", "SPEA.BE, MSTR")
    tickers = [ticker.strip() for ticker in tickers_input.split(",")]

    # Weights Input
    weights_input = st.text_input("Enter weights (comma separated)", "40, 60")
    try:
        pesi = [(float(x.strip())/100) for x in weights_input.split(",")]
    except ValueError:
        st.error("Invalid weight format. Please enter numbers separated by commas.")
        st.stop()

    # Rolling Return Windows Size Input
    anni_input = st.text_input("Enter the rolling return windows size", "8")
    try:
        if anni_input is None or anni_input == '':
            anni_input = 1
        else:
            anni_input = int(anni_input)
        if anni_input < 1 or anni_input > 999:
            st.error("C'mon! Please enter a value between 1 and 999.")
            st.stop()
    except ValueError:
        st.error("Ouch! Invalid input. Please enter a valid number.")
        st.stop()

    # Risk-Free Return Input
    rf_input = st.text_input("Enter the risk-free return (%)", "2")
    try:
        if rf_input is None or rf_input.strip() == '':
            rf_input = 0.0
        else:
            rf_input = float(rf_input)
        if rf_input < 0 or rf_input > 100:
            st.error("Risk-free return must be between 0 and 100%.")
            st.stop()
    except ValueError:
        st.error("Invalid input for risk-free return. Please enter a valid number.")
        st.stop()

    # Validate Tickers
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

    # Validate Weights
    if len(pesi) != len(tickers_validi):
        st.error("❌ Number of weights does not match the number of valid tickers. Please adjust.")
        st.stop()

    if sum(pesi) != 1:
        st.error(f"❌ The sum of weights must be 100%. Current sum: {(round(sum(pesi), 2)) * 100}%. Please adjust your weights.")
        st.stop()

except Exception as e:
    st.error(":scream: Unexpected exception...")
    # st.error(f"Error: {e}")
    st.stop()


try:
    st.divider()
    dati = yf.download(tickers_validi, interval='1mo')["Close"]
    dati = dati.reindex(tickers_validi, axis=1)
    dati.fillna(method="ffill", limit=1, inplace=True)
    st.write(f"Cool!:sunglasses: We got data from {dati.dropna().index[0].strftime("%Y-%m-%d")} and {dati.dropna().index[-1].strftime("%Y-%m-%d")} ")

except Exception as e:
    st.error(":scream: Failed retrieve tickers data...")
    #st.error(f"Error: {e}")
    st.stop()

## normalized data
try:
    st.subheader(":pushpin: Display price normalized data")
    dati_normaliz = normalize_data(dati)
    dati_normaliz

    ## normalized data - chart
    st.write("Now... price chart! You can compare how assets were going through the years.")
    dn_chart=px.line(dati_normaliz, title='Price normalization chart')
    dn_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified"
    )
    st.plotly_chart(dn_chart, use_container_width=True)
except Exception as e:
    st.error(":scream: Failed normalized data...")
    #st.error(f"Error: {e}")
    st.stop()

## rolling ret
try:
    portafogli=pd.DataFrame()
    anni=anni_input
    #return each period
    portafogli=roll_returns(portafogli,anni,dati, tickers,pesi)

    st.subheader(f":pushpin: Display portfolio :green[annualized return] over {anni} years")
    st.write("A series of annualized returns by month: Imagine you bought on *start date* and sold on blue[*end period date*, **which annualized return did you get?**")
    st.write("*the 'annualized returns' are already a % value*")
    start_dates = portafogli.index
    end_dates = start_dates + pd.DateOffset(years=anni)
    returns = (portafogli*100)

    results = pd.DataFrame({
        #"start date": start_dates,
        "end period date": end_dates,
        "% annualized return over period ": returns
    })
    st.dataframe(results)

except Exception as e:
    st.error(":scream: Failed generate rolling returns on data...")
    #st.error(f"Error: {e}")
    st.stop()

## rolling ret - line chart
try:
    rollretlinechart=px.line(portafogli.dropna(), title="Rolling return chart")
    rollretlinechart.update_layout(
        xaxis_title="Date",
        yaxis_title="Return %",
        hovermode="x unified"
    )
    rollretlinechart.add_hline(y=0, line_dash="dash", line_color="red", line_width=2)
    rollretlinechart.layout.yaxis.tickformat = ',.0%'
    st.plotly_chart(rollretlinechart, use_container_width=True)
    
    st.write(f":face_with_monocle: How to read it: on X axis we have the date when we start investing, on Y axis we have the annualized return reached")


    #rolling ret - hist chart
    hist = px.histogram(portafogli.dropna(), 
        opacity=0.4, nbins=80, 
        title="Histogram of Portfolio Returns"
    )
    hist.update_layout(
        xaxis_title="Return",
        yaxis_title="# of times",
        hovermode="x unified"
    )
    hist.add_vline(x=0, line_dash="dash", line_color="red", line_width=2)
    hist.layout.xaxis.tickformat = ',.0%'
    st.plotly_chart(hist, use_container_width=True)

    st.write(f":face_with_monocle: How to read it: On the X axis we have the % return, on the Y axis we have the number of times it happened.")

except Exception as e:
    st.error(":scream: Failed create rolling charts...")
    #st.error(f"Error: {e}")
    st.stop()

## Portfolio Statistics
try:
    st.subheader(f":pushpin: Juicy portfolio statistics over {anni} years")
    st.write(":yum: Some yummy statistics:")
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
except Exception as e:
    st.error(":scream: Failed create portfolio statistics...")
    #st.error(f"Error: {e}")
    st.stop()

## Drawdown
try:
    st.subheader(":pushpin: :red[Drawdown] Statistics")
    st.write(":worried: The painful side...")
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

    st.write(f":face_with_monocle: How to read it: we have the worst case (max drawdown), the 10% of worst cases (10% quantile), the 5% of worst cases (5% quantile) and the mean return in that case (mean return on quantile) ")
except Exception as e:
    st.error(":scream: Failed calculate drawdown statistics...")
    #st.error(f"Error: {e}")
    st.stop()

## sharpRatio
try:
    st.subheader(":pushpin: Sharpe Ratio")
    st.subheader(f"Sharpe Ratio over period with risk-free rate of return of {rf_input}")
    st.write(
        round(  (portafogli.dropna().mean()-rf_input)/portafogli.dropna().std() , 3)
    )
except Exception as e:
    st.error(":scream: Failed create sharp ratio...")
    #st.error(f"Error: {e}")
    st.stop()
