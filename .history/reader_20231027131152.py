import sqlite3
import time
import pandas as pd
# Connect to the SQLite database
conn = sqlite3.connect(r'c:\Users\Sohum\tick_data2.db')

# Create a cursor
cursor = conn.cursor()
data_dict = {}

while True:
    # Check if the current minute is an odd number (1st, 3rd, 5th minute, etc.)
    current_minute = time.localtime().tm_min
    if current_minute % 2 == 1:
        # Execute a query to fetch the latest LTP for each symbol
        cursor.execute("SELECT symbol, ltp FROM tick_data2 WHERE timestamp = (SELECT MAX(timestamp) FROM tick_data2 WHERE symbol = ?)", ("NSE:TCS-EQ",))

        # Fetch the data
        result = cursor.fetchone()
        if result:
            symbol, ltp = result

            # Update the dictionary with the latest data
            data_dict[symbol] = ltp

            # Print the DataFrame (or save it to a file)
            df = pd.DataFrame(data_dict, index=[pd.Timestamp.now()])
            print(df)

    # Wait for 1 minute before checking the odd minute condition again
    time.sleep(60)  