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
import multiprocessing

# Define the fetch_latest_ltp function (as provided in the previous responses)

# Create a list of different symbol sets, each containing two symbols
symbol_sets = [
    ['NSE:HDFCBANK-EQ', 'NSE:ICICIBANK-EQ'],
    ['NSE:TCS-EQ', 'NSE:INFY-EQ'],
    ['NSE:RELIANCE-EQ', 'NSE:HDFCBANK-EQ'],
    ['NSE:KOTAKBANK-EQ', 'NSE:LT-EQ'],
    ['NSE:AXISBANK-EQ', 'NSE:ITC-EQ'],
    ['NSE:SBIN-EQ', 'NSE:HCLTECH-EQ'],
    ['NSE:WIPRO-EQ', 'NSE:BAJAJFINSV-EQ'],
    ['NSE:BAJFINANCE-EQ', 'NSE:ASIANPAINT-EQ'],
    ['NSE:MARUTI-EQ', 'NSE:TECHM-EQ'],
    ['NSE:NTPC-EQ', 'NSE:TITAN-EQ']
    ]

if __name__ == "__main__":
    database_path = r'C:\Users\Sohum\tick_data2.db'  # Replace with the path to your SQLite database
    table_name = 'tick_data2'  # Replace with the name of your database table

    # Define a list to store the processes
    processes = []

    # Number of instances to run (10 in this case)
    num_instances = 10

    # Start multiple instances of the function using multiprocessing
    for i in range(num_instances):
        # Pass the appropriate symbol set to each process
        symbol_set = symbol_sets[i % len(symbol_sets)]
        process = multiprocessing.Process(target=fetch_latest_ltp, args=(symbol_set, database_path, table_name))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()
