import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

file_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\symbolz.txt'
Symbolz = []
with open(file_path, 'r') as file:
    for line in file:
        symbol = line.strip()
        Symbolz.append(symbol)
symbol_list=Symbolz





# Connect to the SQLite database
database_path = 'tick_data2.db'
conn = sqlite3.connect(database_path)

# Define the SQL query to select the latest 50 rows
query = "SELECT * FROM tick_data ORDER BY Datetime DESC LIMIT 50"

# Use Pandas to read the query result into a DataFrame
df = pd.read_sql_query(query, conn)
df.set_index('Datetime',inplace=True)
df=df[[symbol_list[2],symbol_list[3]]]
df['Ratio']=df.iloc[:, 0]/df.iloc[:,1]
df['EMA']=df['Ratio'].rolling(20).mean()
df['StdDown']=df['EMA']-df['EMA'].rolling(20).std()
df['StdUp']=df['EMA']+df['EMA'].rolling(20).std()

# Close the database connection
conn.close()

print(df)