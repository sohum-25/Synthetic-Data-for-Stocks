import sqlite3
import pandas as pd

def analyze_tick_data(database_path, symbol_list,i):
    conn = sqlite3.connect(database_path)
    try:
        query = "SELECT * FROM tick_data ORDER BY Datetime DESC LIMIT 50"
        df = pd.read_sql_query(query, conn)
        df.set_index('Datetime', inplace=True)
        selected_columns = df[[symbol_list[i],symbol_list[i+1]]]
        df['Ratio'] = selected_columns.iloc[:, 0] / selected_columns.iloc[:, 1]
        df['EMA'] = df['Ratio'].rolling(20).mean()
        df['StdDown'] = df['EMA'] - df['EMA'].rolling(20).std()
        df['StdUp'] = df['EMA'] + df['EMA'].rolling(20).std()
        return df.iloc[-1]
    except Exception as e:
        print(f"Error analyzing tick data: {e}")
        return None
    finally:
        conn.close()



file_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\symbolz.txt'
Symbolz = []
with open(file_path, 'r') as file:
    for line in file:
        symbol = line.strip()
        Symbolz.append(symbol)





symbol_list=Symbolz
# Connect to the SQLite database
database_path = 'tick_data2.db'
analyze_tick_data(database_path,Symbolz,1)