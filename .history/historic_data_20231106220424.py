import pandas as pd
import numpy as np
import yfinance as yf
import sqlite3
from RelevantPairs import GetRelevantPairs,FillerDataFrames,ListCorrection


path='ind_nifty100list (1).csv'
ValidPairs,correlation=FillerDataFrames(path)

symbol_list=(ListCorrection(GetRelevantPairs(correlation,0.05,ValidPairs)))
modified_list=[item + ".NS" for item in symbol_list]




df=yf.download(tickers=modified_list,interval='2m',period='4d')['Close']
columns_to_rename = modified_list
# Rename the columns
for old_column_name in columns_to_rename:
    symbol = old_column_name.replace('.NS', '')  # Extract the symbol
    new_column_name = f'{symbol}'
    df = df.rename(columns={old_column_name: new_column_name})

print(len(df),df.columns)
df=df.tz_localize(None)
df=df.reset_index()
df=df.tail(100)
conn = sqlite3.connect("tick_data2.db")

df.to_sql("tick_data", conn, if_exists="replace", index=False)