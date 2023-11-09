import sqlite3
import time
import multiprocessing
from fyers_apiv3 import fyersModel
import pandas as pd
from fyers_apiv3.FyersWebsocket import data_ws
from RelevantPairs import FillerDataFrames, ListCorrection, GetRelevantPairs
from historic_data import UpdateHistoricData
import datetime
from datetime import datetime
from datetime import datetime
from TradingFunction import CalculateParameters

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
    current_time = time.localtime()
    

    if (
        1
    ):
        pool = multiprocessing.Pool(processes=1)
        ltp_results = pool.map(fetch_ltp_for_symbol, [(database_path, fetch_table, symbol) for symbol in symbols])
        pool.close()
        pool.join()

        latest_ltp_values = {symbol: ltp for symbol, ltp in ltp_results if ltp is not None}

        if latest_ltp_values:
            current_timestamp = time.strftime("%Y-%m-d %H:%M:%S", current_time)
            current_time2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
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
                insertion_time = datetime.now()
                insertion_timestamp = insertion_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                print(insertion_timestamp)
                print(f"Error inserting data into the database: {e}")
                print(data_dict)
                
            finally:
                conn.close()
        else:
            print("No data found for any symbol at this time")
            

if __name__ == '__main__':
        
    conn = sqlite3.connect('tick_data2.db')
    cursor = conn.cursor()
    table_names = ['tick_data2']
    for table_name in table_names:
        truncate_query = f'DELETE FROM {table_name}'
        cursor.execute(truncate_query)
    conn.commit()
    conn.close()


    conn = sqlite3.connect("tick_data2.db")
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tick_data2 (
    Datetime REAL,
    symbol TEXT,
    ltp REAL
    );
    """
    cursor.execute(create_table_sql)










    client_id='MRXTWL7TF2-100'
    tokenpath = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\token.txt'
    with open(tokenpath, 'r') as file:
        tk = file.read().strip()
    
    fyers=fyersModel.FyersModel(client_id=client_id,is_async=False,token=tk,log_path="")
    


    def onmessage(message):
        try:
            data = message
            symbol = data['symbol'].replace('NSE:', '').replace('-EQ', '') 
            ltp = data['ltp']
            Datetime = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

            # Establish a connection to the SQLite database in this thread
            db_connection = sqlite3.connect('tick_data2.db')
            cursor = db_connection.cursor()

            # Insert the data into the database
            cursor.execute("INSERT INTO tick_data2 (Datetime, symbol, ltp) VALUES (?, ?, ?)", (Datetime, symbol, ltp))
            db_connection.commit()
            db_connection.close()  # Close the connection in the same thread

            #print("Stored data in the database - Datetime: {}, Symbol: {}, LTP: {}".format(Datetime, symbol, ltp))

        except Exception as e:
            print("Error:", e)
        
  
    def onerror(message):
        print("Error",message)
        

    def onopen():
        data_type="SymbolUpdate"
        
        symbols=list_of_symbols
        fyers.subscribe(symbols=symbols,data_type=data_type)
        
        fyers.keep_running()
        
    


    csv_path = 'ind_nifty100list (1).csv'
    Symbolz = UpdateHistoricData(csv_path)
   # Specify the file path
    file_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\symbolz.txt'

    # Save the 'Symbolz' list as a text file
    with open(file_path, 'w') as file:
        for symbol in Symbolz:
            file.write(symbol + '\n')



    file_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\symbolz.txt'
    Symbolz = []
    with open(file_path, 'r') as file:
        for line in file:
            symbol = line.strip()
            Symbolz.append(symbol)
    symbol_list=Symbolz
    print(symbol_list)
    
    symbol_list = Symbolz
    list_of_symbols=[f'NSE:{item}-EQ' for item in symbol_list]
    list_of_symbols=list(set(list_of_symbols))
    symbols = symbol_list  # Replace with your list of stock symbols
    database_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\tick_data2.db'
    insert_table = 'tick_data'  # Replace with your historic data table name
    fetch_table = 'tick_data2'  # Replace with your tick data table name
    w_access_token=client_id+":"+tk

    fyers = data_ws.FyersDataSocket(
            access_token=w_access_token,       # Access token in the format "appid:accesstoken"
            log_path="",                     # Path to save logs. Leave empty to auto-create logs in the current directory.
            litemode=True,                  # Lite mode disabled. Set to True if you want a lite response.
            write_to_file=False,              # Save response in a log file instead of printing it.
            reconnect=True,                  # Enable auto-reconnection to WebSocket on disconnection.
            on_connect=onopen,               # Callback function to subscribe to data upon connection.
                    # Callback function to handle WebSocket connection close events.
            on_error=onerror,                # Callback function to handle WebSocket errors.
            on_message=onmessage             # Callback function to handle incoming messages from the WebSocket.
        )

        # Establish a connection to the Fyers WebSocket
    fyers.connect()
    
    # Main loop to run the function
    while True:
        
        current_time = datetime.now().time()
        current_hour = current_time.hour
        current_minute = current_time.minute
        current_second = current_time.second

        if (
    current_minute % 2 == 1
    and current_second == 0
    and (
        (current_hour > 9 or (current_hour == 9 and current_minute >= 15))
        and (current_hour < 15 or (current_hour == 15 and current_minute <= 20))
    )
):
            fetch_latest_ltp(symbols, database_path, insert_table, fetch_table)
            fyers=fyersModel.FyersModel(client_id=client_id,is_async=False,token=tk,log_path="")
            TotalCapital=5000
            inTrade=0
            activeLongPosition=0
            activeShortPosition=0
            TotalCapital, inTrade, activeLongPosition, activeShortPosition=CalculateParameters(database_path, symbol_list, 0, TotalCapital, fyers, inTrade, activeLongPosition, activeShortPosition,client_id,tk)

 
 
        time.sleep(1)  # Check every second
