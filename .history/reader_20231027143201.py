import sqlite3
import time

# Function to fetch the latest data for specific symbols every odd minute
import sqlite3
import time

# Function to fetch the latest data for specific symbols every odd minute
def fetch_latest_ltp(symbols, database_path, table_name):
    while True:
        current_time = time.localtime()
        current_minute = current_time.tm_min
        current_second = current_time.tm_sec

        # Check if the minute is odd and the seconds are 00
        if current_minute % 2 == 1 and current_second == 0:
            try:
                conn = sqlite3.connect(database_path)
                cursor = conn.cursor()

                for symbol in symbols:
                    # Retrieve the latest LTP for each specified symbol based on the maximum timestamp
                    cursor.execute(f"SELECT ltp FROM {table_name} WHERE symbol = ? AND timestamp = (SELECT MAX(timestamp) FROM {table_name} WHERE symbol = ?)", (symbol, symbol))
                    latest_ltp = cursor.fetchone()

                    if latest_ltp:
                        print(f"Latest LTP for {symbol}: {latest_ltp[0]} at {time.strftime('%H:%M:%S', current_time)}")
                    else:
                        print(f"No data found for {symbol} at this time.")

            except Exception as e:
                print(f"Error: {e}")
            finally:
                conn.close()

        time.sleep(1)  # Sleep for 2 seconds to avoid continuous checking

# Example usage
if __name__ == "__main__":
    symbols_to_fetch = ['NSE:TCS-EQ', 'NSE:INFY-EQ']  # Replace with the symbols you want to monitor
    database_path = r'C:\Users\Sohum\tick_data2.db'  # Replace with the path to your SQLite database
    table_name = 'tick_data2'  # Replace with the name of your database table

    fetch_latest_ltp(symbols_to_fetch, database_path, table_name)