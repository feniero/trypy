import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from pyscript import document

arr=np.arange(4)

#send python output to html div
output_div = document.querySelector("#output")
output_div.innerText = arr