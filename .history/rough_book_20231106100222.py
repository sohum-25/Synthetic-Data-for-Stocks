from rought import fetch_ltp_for_symbol


database_path = r'C:\Users\Sohum\tick_data2.db'  # Replace with your database file path
fetch_table = 'tick_data2'

fetch_ltp_for_symbol(database_path,fetch_table,'BPCL')
