import sqlite3
from datetime import datetime

# List of symbols for which you want to append data
symbols_to_insert = ["NSE:HDFCBANK-EQ","NSE:ICICIBANK-EQ","NSE:TCS-EQ","NSE:INFY-EQ","NSE:RELIANCE-EQ","NSE:HDFC-EQ", "NSE:KOTAKBANK-EQ", "NSE:LT-EQ", "NSE:AXISBANK-EQ", "NSE:ITC-EQ", "NSE:SBIN-EQ", "NSE:HCLTECH-EQ", "NSE:WIPRO-EQ", "NSE:BAJAJFINSV-EQ", "NSE:BAJFINANCE-EQ", "NSE:ASIANPAINT-EQ", "NSE:MARUTI-EQ", "NSE:TECHM-EQ", "NSE:NTPC-EQ", "NSE:TITAN-EQ"]

# Connect to the database
conn = sqlite3.connect("tick_data2.db")
cursor = conn.cursor()

# Get the current timestamp in the desired format
current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Iterate over the list of symbols
for symbol in symbols_to_insert:
    # Get the latest tick data for the current symbol
    query = f"SELECT ltp FROM tick_data2 WHERE symbol = ? ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(query, (symbol,))
    latest_tick = cursor.fetchone()

    if latest_tick:
        ltp = latest_tick[0]

        # Generate the INSERT statement to append data to the 'tick_data' table
        insert_query = f"INSERT INTO tick_data (Datetime, symbol, {symbol}) VALUES (?, ?, ?)"
        
        # Execute the INSERT statement with current_timestamp, symbol, and ltp
        cursor.execute(insert_query, (current_timestamp, symbol, ltp))
        conn.commit()

# Close the connection
conn.close()
