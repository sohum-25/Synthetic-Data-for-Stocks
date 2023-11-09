import pandas as pd
import numpy as np
import yfinance as yf
import sqlite3
from RelevantPairs import GetRelevantPairs,FillerDataFrames,ListCorrection


path='ind_nifty100list (1).csv'
ValidPairs,correlation=FillerDataFrames(path)

symbol_list=(ListCorrection(GetRelevantPairs(correlation,0.05,ValidPairs)))
print(symbol_list)
