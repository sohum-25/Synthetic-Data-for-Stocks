import sqlite3
import time
import pandas as pd
# Connect to the SQLite database
conn = sqlite3.connect(r'c:\Users\Sohum\tick_data2.db')

# Create a cursor
cursor = conn.cursor()
data_dict = {}

# Wait until the next odd minute to start fetching data
current_minute = time.localtime().tm_min
if current_minute % 2 == 0:
    # If the current minute is even, wait for the next odd minute
    time_to_wait = 61 - current_minute  # Time until the next odd minute
    time.sleep(time_to_wait)

while True:
    # Execute a query to fetch the latest LTP for each symbol
    cursor.execute("SELECT symbol, ltp FROM tick_data2 WHERE timestamp = (SELECT MAX(timestamp) FROM tick_data2 WHERE symbol = ?)", ("NSE:TCS-EQ",))

    # Fetch the data
    result = cursor.fetchone()
    if result:
        symbol, ltp = result

        # Update the dictionary with the latest data
        data_dict[symbol] = ltp

        # Print the DataFrame (or save it to a file)
        df = pd.DataFrame(data_dict, index=[pd.Timestamp.now().time()])
        print(df)

    # Wait for 2 minutes before the next update
    time.sleep(120)  # 120 seconds = 2 minutes
