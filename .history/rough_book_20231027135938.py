import sqlite3

conn = sqlite3.connect(r'C:\Users\Sohum\Desktop\Synthetic Data for Stocks\tick_data2.db')
cursor = conn.cursor()

# Query to retrieve the list of tables in the database
cursor.execute("SELECT name FROM tick_data2 WHERE type='table';")
tables = cursor.fetchall()
print(5+6)
# Extract and print the table names
print(len(tables))