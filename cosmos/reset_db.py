import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('hotfix_inputs.db')
cursor = conn.cursor()

# Drop the table if it exists
cursor.execute('DROP TABLE IF EXISTS hotfix_inputs')

# Close the connection
conn.commit()
conn.close()

print("Table dropped. You can now run your application to recreate it.")
