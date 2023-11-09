import sqlite3
import time

# Function to fetch the latest data for specific symbols every odd minute
def fetch_data_for_symbols(symbol1, symbol2, database_path, table_name):
    while True:
        current_minute = int(time.strftime('%M'))
        if current_minute % 2 == 1:
            try:
                conn = sqlite3.connect(database_path)
                cursor = conn.cursor()
                
                # Retrieve the latest data for the specified symbols
                cursor.execute(f"SELECT * FROM {table_name} WHERE symbol = ? ORDER BY timestamp DESC LIMIT 1", (symbol1,))
                data1 = cursor.fetchone()
                
                cursor.execute(f"SELECT * FROM {table_name} WHERE symbol = ? ORDER BY timestamp DESC LIMIT 1", (symbol2,))
                data2 = cursor.fetchone()
                
                
                # Process the retrieved data
                print(f"Latest data for {symbol1}: {data1}")
                print(f"Latest data for {symbol2}: {data2}")
                
            except Exception as e:
                print(f"Error: {e}")
        
        time.sleep(60)  # Sleep for 1 minute

# Example usage of the function
if __name__ == "__main__":
    symbol1 = 'NSE:TCS-EQ'  # Replace with the first stock symbol
    symbol2 = 'NSE"INFY-EQ'  # Replace with the second stock symbol
    database_path = 'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\tick_data2.db'  # Replace with the path to your SQLite database
    table_name = 'tick_data2'  # Replace with the name of your database table
    
    fetch_data_for_symbols(symbol1, symbol2, database_path, table_name)