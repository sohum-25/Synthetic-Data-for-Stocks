import pandas as pd
import numpy as np
import yfinance as yf
import sqlite3
df=yf.download(tickers=['INDUSINDBK.NS', 'SBILIFE.NS', 'BPCL.NS', 'IOC.NS', 'HINDALCO.NS', 'JSWSTEEL.NS', 'APOLLOHOSP.NS', 'DIVISLAB.NS', 'ONGC.NS', 'RELIANCE.NS', 'BANKBARODA.NS', 'SBIN.NS', 'GRASIM.NS', 'SHREECEM.NS', 'BRITANNIA.NS', 'TATACONSUM.NS', 'HEROMOTOCO.NS', 'TATAMOTORS.NS', 'CANBK.NS', 'SHRIRAMFIN.NS'],interval='2m',period='4d')['Close']
columns_to_rename = ['INDUSINDBK.NS', 'SBILIFE.NS', 'BPCL.NS', 'IOC.NS', 'HINDALCO.NS', 'JSWSTEEL.NS', 'APOLLOHOSP.NS', 'DIVISLAB.NS', 'ONGC.NS', 'RELIANCE.NS', 'BANKBARODA.NS', 'SBIN.NS', 'GRASIM.NS', 'SHREECEM.NS', 'BRITANNIA.NS', 'TATACONSUM.NS', 'HEROMOTOCO.NS', 'TATAMOTORS.NS', 'CANBK.NS', 'SHRIRAMFIN.NS']
['INDUSINDBK.NS', 'SBILIFE.NS', 'BPCL.NS', 'IOC.NS', 'HINDALCO.NS', 'JSWSTEEL.NS', 'APOLLOHOSP.NS', 'DIVISLAB.NS', 'ONGC.NS', 'RELIANCE.NS', 'BANKBARODA.NS', 'SBIN.NS', 'GRASIM.NS', 'SHREECEM.NS', 'BRITANNIA.NS', 'TATACONSUM.NS', 'HEROMOTOCO.NS', 'TATAMOTORS.NS', 'CANBK.NS', 'SHRIRAMFIN.NS']
# Rename the columns
for old_column_name in columns_to_rename:
    symbol = old_column_name.replace('.NS', '')  # Extract the symbol
    new_column_name = f'NSE:{symbol}-EQ'
    df = df.rename(columns={old_column_name: new_column_name})

print(len(df),df.columns)
df=df.tz_localize(None)
df=df.reset_index()
df
conn = sqlite3.connect("tick_data2.db")

df.to_sql("tick_data", conn, if_exists="replace", index=False)
