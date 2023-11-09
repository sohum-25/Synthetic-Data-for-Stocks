import os

database_path = r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\tick_data2.db'

if os.path.exists(database_path):
    print("Database file exists.")
else:
    print("Database file does not exist.")
