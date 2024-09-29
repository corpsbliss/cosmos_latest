import sqlite3

# Database setup
DATABASE = 'hotfix_inputs.db'

def print_schema():
    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Query to get the schema of the hotfix_inputs table
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='hotfix_inputs';")
    schema = cursor.fetchone()
    
    if schema:
        print("Schema for 'hotfix_inputs' table:")
        print(schema[0])
    else:
        print("Table 'hotfix_inputs' does not exist.")
    
    # Close the connection
    conn.close()

if __name__ == '__main__':
    print_schema()
