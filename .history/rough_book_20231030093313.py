from reader import fetch_latest_ltp
database_path = r'C:\Users\Sohum\tick_data2.db'
table_name = 'tick_data2'
fetch_latest_ltp(['BPCL.NS','IOC.NS'],database_path,table_name)