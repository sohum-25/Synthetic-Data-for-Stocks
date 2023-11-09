import sqlite3
import multiprocessing
import time
from datetime import datetime
def fetch_latest_ltp(symbols, database_path, insert_table, fetch_table):
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
                    # Retrieve the existing row for the same Datetime and symbol
                    cursor.execute(f"SELECT * FROM {insert_table} WHERE Datetime = (SELECT MAX(Datetime) FROM {insert_table} WHERE symbol = ?) AND symbol = ?", (symbol, symbol))
                    existing_row = cursor.fetchone()

                    if existing_row:
                        # Retrieve the latest LTP for the specified symbol from the fetch_table
                        cursor.execute(f"SELECT ltp FROM {fetch_table} WHERE symbol = ? AND Datetime = (SELECT MAX(Datetime) FROM {fetch_table} WHERE symbol = ?)", (symbol, symbol))
                        latest_ltp = cursor.fetchone()

                        if latest_ltp:
                            # Compute the intersection and update the row
                            new_ltp = latest_ltp[0]
                            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            intersection_value = min(float(existing_row[1]), new_ltp)
                            cursor.execute(f"UPDATE {insert_table} SET {symbol} = ? WHERE Datetime = ? AND symbol = ?", (intersection_value, existing_row[0], symbol))
                            conn.commit()
                        else:
                            print(f"No data found for {symbol} at this time.")

                    else:
                        print(f"No existing data found for {symbol}.")

            except Exception as e:
                print(f"Error: {e}")
            finally:
                conn.close()

        time.sleep(1)


symbol_sets = [
    ['APOLLOHOSP', 'BANKBARODA'],
    ['BPCL', 'BRITANNIA'],
    ['CANBK', 'DIVISLAB'],
    ['GRASIM', 'HEROMOTOCO'],
    ['HINDALCO', 'INDUSINDBK'],
    ['IOC', 'JSWSTEEL'],
    ['ONGC', 'RELIANCE'],
    ['SBILIFE', 'SBIN'],
    ['SHREECEM', 'SHRIRAMFIN'],
    ['TATACONSUM', 'TATAMOTORS']
]


if __name__ == "__main__":
    database_path= "C:\\Users\\Sohum\\Desktop\\Synthetic Data for Stocks\\tick_data2.db"
    insert_table = 'tick_data'
    fetch_table = 'tick_data2'  # Replace with the name of your database table

    # Define a list to store the processes
    processes = []

    # Number of instances to run (10 in this case)
    num_instances = 10

    # Start multiple instances of the function using multiprocessing
    for i in range(num_instances):
        # Pass the appropriate symbol set to each process
        symbol_set = symbol_sets[i % len(symbol_sets)]
        process = multiprocessing.Process(target=fetch_latest_ltp, args=(symbol_set, database_path, insert_table,fetch_table))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()
