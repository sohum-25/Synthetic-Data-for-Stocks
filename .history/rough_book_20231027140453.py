import sqlite3

conn = sqlite3.connect(r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\tick_data.db')
cursor = conn.cursor()

# Query to retrieve the list of tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Extract and print the table names
for table in tables:
    print("Table Name:", table[0])