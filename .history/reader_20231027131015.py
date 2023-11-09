import sqlite3
import time
import pandas as pd
# Connect to the SQLite database
conn = sqlite3.connect(r'c:\Users\Sohum\tick_data2.db')

# Create a cursor
cursor = conn.cursor()
data_dict = {}

# Define the number of iterations or the duration you want to update the DataFrame
num_iterations = 10  # For example, update 10 times
update_interval = 120  # Update every 2 minutes

for _ in range(num_iterations):
    # Execute a query to fetch the latest LTP for each symbol
    cursor.execute("SELECT symbol, ltp FROM tick_data2 WHERE timestamp = (SELECT MAX(timestamp) FROM tick_data2 WHERE symbol = ?)", ("NSE:TCS-EQ",))

    # Fetch the data
    result = cursor.fetchone()
    if result:
        symbol, ltp = result

        # Update the dictionary with the latest data
        data_dict[symbol] = ltp

        # Wait for 2 minutes before the next update
        time.sleep(update_interval)

    else:
        print(f"No data found for symbol {symbol}")

# Convert the data dictionary to a DataFrame
df = pd.DataFrame(data_dict, index=[pd.Timestamp.now()])

# Print the DataFrame (or save it to a file)
print(df)