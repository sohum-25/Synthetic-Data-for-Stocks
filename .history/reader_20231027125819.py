import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("tick_data2.db")

# Create a cursor
cursor = conn.cursor()

# Execute a SQL query to fetch data
cursor.execute("SELECT * FROM tick_data2")

