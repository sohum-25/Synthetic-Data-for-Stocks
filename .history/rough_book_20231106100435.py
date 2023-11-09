from rought import fetch_ltp_for_symbol


database_path = r'C:\Users\Sohum\tick_data2.db'  # Replace with your database file path
fetch_table = 'tick_data'
symbol='BPCL'
args=(database_path,fetch_table,symbol)
fetch_ltp_for_symbol(args)
