import pandas as pd

def normalize_data(dati):
    if(dati is None):
        return False
    else:
        return 100 * dati.dropna() / dati.dropna().iloc[0]

