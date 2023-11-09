import pandas as pd
import numpy as np
import yfinance as yf

df=yf.download(tickers=['ICICIBANK.NS','HDFCBANK.NS'],interval='2m',period='4d')['Close']
df