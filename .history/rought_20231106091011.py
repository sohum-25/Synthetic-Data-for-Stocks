import sqlite3
import time
from datetime import datetime
import multiprocessing

def fetch_latest_ltp(symbols, database_path, insert_table, fetch_table):
    def fetch_ltp_for_symbol(symbol):
        try:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()

            # Retrieve the latest LTP for the specified symbol based on the maximum Datetime
            cursor.execute(f"SELECT LTP FROM {fetch_table} WHERE Symbol = ? AND Datetime = (SELECT MAX(Datetime) FROM {fetch_table} WHERE Symbol = ?)", (symbol, symbol))
            latest_ltp = cursor.fetchone()
            conn.close()

            return symbol, latest_ltp[0] if latest_ltp else None
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return symbol, None

    while True:
        current_time = time.localtime()
        current_minute = current_time.tm_min  # Extract the minute part

        if current_minute % 2 == 0:
            pool = multiprocessing.Pool(processes=1)
            ltp_results = pool.map(fetch_ltp_for_symbol, symbols)
            pool.close()
            pool.join()

            latest_ltp_values = {symbol: ltp for symbol, ltp in ltp_results if ltp is not None}

            if latest_ltp_values:
                current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
                data_dict = {'Datetime': current_timestamp, **latest_ltp_values}

                try:
                    conn = sqlite3.connect(database_path)
                    cursor = conn.cursor()

                    columns = ', '.join(data_dict.keys())
                    placeholders = ', '.join(['?'] * len(data_dict))
                    values = list(data_dict.values())

                    insert_query = f"INSERT INTO {insert_table} ({columns}) VALUES ({placeholders})"
                    cursor.execute(insert_query, values)
                    conn.commit()

                    current_timestamp2 = time.strftime("%Y-%m-%d %H:%M:%S.%f")
                    print("Added to db at:", current_timestamp2)
                except Exception as e:
                    print(f"Error inserting data into the database: {e}")
                finally:
                    conn.close()
            else:
                print("No data found for any symbol at this time.")

        time.sleep(60)  # Check every minute

# Example usage:
symbols = ['SBIN', 'AAPL', 'GOOGL']  # Replace with your list of stock symbols
database_path = 'your_database.db'  # Replace with your database file path
insert_table = 'historic_data'      # Replace with your historic data table name
fetch_table = 'tick_data'          # Replace with your tick data table name

fetch_latest_ltp(symbols, database_path, insert_table, fetch_table)
