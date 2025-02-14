import streamlit as st
import numpy as np
import pandas as pd

#normalized data: start from '100'
def normalize_data(dati):
    return 100 * dati.dropna() / dati.dropna().iloc[0]

#rolling returns with sliding window
def roll_returns(anni,dati, tickers,pesi):
    componenti = dati[tickers].dropna()
    performance = (componenti.shift(-12*anni)/componenti)**(1/anni)-1
    performance_indice = pd.DataFrame( np.dot(performance,pesi), index=performance.index, columns=["All Seasons"] )
    portafogli["ptf"] = performance_indice.dropna()
    
    return (portafogli.dropna(how="all"))

