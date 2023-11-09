import sqlite3
import pandas as pd

# Connect to the SQLite database
database_path = 'tick_data2.db'
conn = sqlite3.connect(database_path)

# Define the SQL query to select the latest 50 rows
query = "SELECT * FROM tick_data ORDER BY Datetime DESC LIMIT 50"

# Use Pandas to read the query result into a DataFrame
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Now, the variable "df" contains the latest 50 rows from the "tick_data" table with column names intact.
