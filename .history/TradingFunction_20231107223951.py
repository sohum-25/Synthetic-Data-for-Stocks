import pandas as pd
import numpy as np
import sqlite3 

database_path = 'tick_data2.db'
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# SQL query to select the latest 50 rows from the "tick_data" table
query = "SELECT * FROM tick_data ORDER BY Datetime DESC LIMIT 50"

# Execute the query
cursor.execute(query)

# Fetch the results
latest_50_rows = cursor.fetchall()

# Close the database connection
conn.close()
print(latest_50_rows)