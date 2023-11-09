import sqlite3

# Replace 'tick_data2.db' with the actual name of your SQLite database file.
database_path = 'tick_data2.db'

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Fetch the table names from the SQLite master table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()

conn.close()

if table_names:
    print("Existing tables in the database:")
    for table_name in table_names:
        print(table_name[0])
else:
    print("No tables found in the database.")
