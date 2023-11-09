import sqlite3
import time
from datetime import datetime
import multiprocessing

def fetch_ltp_for_symbol(database_path, symbol):
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

def fetch_latest_ltp(symbols, database_path, insert_table, fetch_table):
    while True:
        current_time = time.localtime()
        current_minute = current_time.tm_min  # Extract the minute part

        if current_minute % 2 == 0:
            pool = multiprocessing.Pool(processes=len(symbols))
            ltp_results = pool.map(fetch_ltp_for_symbol, [(database_path, symbol) for symbol in symbols])
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

        time.sleep(60)

list_of_symbols=['NSE:APOLLOHOSP-EQ', 'NSE:BANKBARODA-EQ', 'NSE:BPCL-EQ',
       'NSE:BRITANNIA-EQ', 'NSE:CANBK-EQ', 'NSE:DIVISLAB-EQ', 'NSE:GRASIM-EQ',
       'NSE:HEROMOTOCO-EQ', 'NSE:HINDALCO-EQ', 'NSE:INDUSINDBK-EQ',
       'NSE:IOC-EQ', 'NSE:JSWSTEEL-EQ', 'NSE:ONGC-EQ', 'NSE:RELIANCE-EQ',
       'NSE:SBILIFE-EQ', 'NSE:SBIN-EQ', 'NSE:SHREECEM-EQ', 'NSE:SHRIRAMFIN-EQ',
       'NSE:TATACONSUM-EQ', 'NSE:TATAMOTORS-EQ']


list_of_symbols=[value.replace('NSE:', '').replace('-EQ', '') for value in list_of_symbols]

symbols = list_of_symbols  # Replace with your list of stock symbols
database_path = r'C:\Users\Sohum\tick_data2.db'  # Replace with your database file path
insert_table = 'tick_data'      # Replace with your historic data table name
fetch_table = 'tick_data2'          # Replace with your tick data table name

fetch_latest_ltp(symbols, database_path, insert_table, fetch_table)
