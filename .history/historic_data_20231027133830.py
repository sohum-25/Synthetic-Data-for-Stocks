import pandas as pd
import numpy as np
import yfinance as yf

df=yf.download(tickers=['ICICIBANK.NS','HDFCBANK.NS'],interval='2m',period='4d')['Close']
columns_to_rename = ['HDFCBANK.NS', 'ICICIBANK.NS']

# Rename the columns
for old_column_name in columns_to_rename:
    symbol = old_column_name.replace('.NS', '')  # Extract the symbol
    new_column_name = f'NSE:{symbol}-EQ'
    df = df.rename(columns={old_column_name: new_column_name})

print(len(df),df.columns)