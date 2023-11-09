import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("tick_data2.db")

# Create a cursor
cursor = conn.cursor()

# Execute a SQL query to fetch data
cursor.execute("SELECT * FROM tick_data2")

# Fetch all the data from the query
data = cursor.fetchall()

# Close the cursor and the connection
cursor.close()
conn.close()

# Print the retrieved data
for row in data:
    print(row)
