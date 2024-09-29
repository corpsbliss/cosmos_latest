import sqlite3
import sys

# Database setup
DATABASE = 'hotfix_inputs.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def store_command(command, status='Pending', rollback_build_url=None, rollback_cl=None, action=None):
    conn = get_db_connection()
    try:
        # Insert the command along with additional fields into the database
        conn.execute('''
            INSERT INTO hotfix_inputs (command, status, rollback_build_url, rollback_cl, action)
            VALUES (?, ?, ?, ?, ?)
        ''', (command, status, rollback_build_url, rollback_cl, action))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Command '{command}' already exists in the database.")
    finally:
        conn.close()

if __name__ == "__main__":
    # Assuming input comes from command line arguments
    if len(sys.argv) < 2:
        print("Please provide a command.")
    else:
        command_input = sys.argv[1]
        # Call the function with the provided command and optional default values
        store_command(command_input)

