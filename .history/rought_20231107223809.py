import sqlite3
import time
from datetime import datetime
import multiprocessing
from RelevantPairs import GetRelevantPairs,ListCorrection,FillerDataFrames
from historic_data import UpdateHistoricData

def fetch_ltp_for_symbol(args):
    database_path, fetch_table, symbol = args  # Unpack the arguments
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
        current_second=current_time.tm_sec
        if (
            current_minute % 2 == 1
            and current_second == 0
            
        ):
            pool = multiprocessing.Pool(processes=1)
            ltp_results = pool.map(fetch_ltp_for_symbol, [(database_path, fetch_table, symbol) for symbol in symbols])
            pool.close()
            pool.join()

            latest_ltp_values = {symbol: ltp for symbol, ltp in ltp_results if ltp is not None}

            if latest_ltp_values:
                current_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
                current_time2= (datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")
                data_dict = {'Datetime': current_time2, **latest_ltp_values}

                try:
                    conn = sqlite3.connect(database_path)
                    cursor = conn.cursor()

                    # Prepare the SQL query with placeholders and double quotes around column names
                    placeholders = ', '.join(['?' for _ in data_dict])
                    columns = ', '.join([f'"{key}"' for key in data_dict.keys()])
                    insert_query = f"INSERT INTO {insert_table} ({columns}) VALUES ({placeholders})"

                    insertion_time = datetime.now()
                    insertion_timestamp = insertion_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                    print(insertion_timestamp)

                    # Execute the query with a tuple of values
                    cursor.execute(insert_query, tuple(data_dict.values()))
                    conn.commit()

                    current_timestamp2 = time.strftime("%Y-%m-%d %H:%M:%S.%f")
                    print("Added to db at:", current_timestamp2)
                except Exception as e:
                    insertion_time=datetime.now()
                    insertion_timestamp=insertion_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                    print(insertion_timestamp)
                    print(f"Error inserting data into the database: {e}")
                    print(data_dict)
                    print(insert_query)
                finally:
                    conn.close()
            else:
                print("No data found for any symbol at this time")

        time.sleep(0.01) 

if __name__ == '__main__':
    path='ind_nifty100list (1).csv'
    file_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\symbolz.txt'
    Symbolz = []
    with open(file_path, 'r') as file:
        for line in file:
            symbol = line.strip()
            Symbolz.append(symbol)
    symbol_list=Symbolz

    list_of_symbols =Symbolz
    symbols = list_of_symbols  # Replace with your list of stock symbols
    database_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\tick_data2.db'
    insert_table = 'tick_data'      # Replace with your historic data table name
    fetch_table = 'tick_data2'          # Replace with your tick data table name

    fetch_latest_ltp(symbols, database_path, insert_table, fetch_table)
