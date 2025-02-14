import pandas as pd

def normalize_data(dati):
        return 100 * dati.dropna() / dati.dropna().iloc[0]

