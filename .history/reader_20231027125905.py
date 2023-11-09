import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("tick_data2.db")

# Create a cursor
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)