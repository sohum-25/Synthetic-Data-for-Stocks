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

 
def fetch_latest_ltp_and_insert(symbols, database_path, insert_table, fetch_table):
    try:
        current_time = time.localtime()

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Retrieve the latest LTP values for all symbols
        latest_ltp_values = {}
        for symbol in symbols:
            cursor.execute(f"SELECT LTP FROM {fetch_table} WHERE Symbol = ? ORDER BY Datetime DESC LIMIT 1", (symbol,))
            latest_ltp = cursor.fetchone()
            if latest_ltp:
                latest_ltp_values[symbol] = latest_ltp[0]

        conn.close()

        if latest_ltp_values:
            current_time2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            data_dict = {'Datetime': current_time2, **latest_ltp_values}

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

            conn.close()
        else:
            print("No data found for any symbol at this time")

    except Exception as e:
        insertion_time = datetime.now()
        insertion_timestamp = insertion_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        print(insertion_timestamp)
        print(f"Error: {e}")
        print(data_dict)






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
            cursor.execute("CREATE INDEX IF NOT EXISTS datetime_index ON tick_data2 (Datetime)")
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
        fyers2.subscribe(symbols=symbols,data_type=data_type)
        
        fyers2.keep_running()
        
    


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

    fyers2 = data_ws.FyersDataSocket(
            access_token=w_access_token,      
            log_path="",                    
            litemode=True,                  
            write_to_file=False,              
            reconnect=True,                  
            on_connect=onopen,               
                    
            on_error=onerror,               
            on_message=onmessage            
        )

        # Establish a connection to the Fyers WebSocket
    fyers2.connect()
    
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
            fetch_latest_ltp_and_insert(symbols, database_path, insert_table, fetch_table)
            response=fyers.get_profile()
            print(response['data']['name'])
            TotalCapital = 5000  # Initial total capital
            inTrade = 0  # Assume not in trade initially
            activeLongPosition = 0
            activeShortPosition = 0
            TotalCapital,inTrade,activeLongPosition,activeShortPosition= CalculateParameters(database_path, symbol_list, 1, TotalCapital, fyers, inTrade, activeLongPosition, activeShortPosition)
            





        time.sleep(1)  # Check every second
