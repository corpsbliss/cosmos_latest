from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('hotfix_input.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        username = request.form['username']
        password = request.form['password']
        # Check credentials (this is just a placeholder, implement your own logic)
        if username == 'admin' and password == 'password':
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

# Route for dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Route for hotfix monitoring
@app.route('/hotfix_monitoring', methods=['GET', 'POST'])
def hotfix_monitoring():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if request.method == 'POST':
        command = request.form['text_input']
        try:
            conn.execute('INSERT INTO hotfix_inputs (command, status) VALUES (?, ?)', (command, 'Pending'))
            conn.commit()
            flash('Command submitted successfully.', 'success')
        except sqlite3.IntegrityError:
            flash('Duplicate command detected.', 'danger')
    
    # Fetch all commands
    commands = conn.execute('SELECT * FROM hotfix_inputs ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('hotfix_monitoring.html', commands=commands)

# Route to remove a command from the database
@app.route('/remove_command/<int:command_id>', methods=['POST'])
def remove_command(command_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM hotfix_inputs WHERE id = ?', (command_id,))
        conn.commit()
        flash('Command removed successfully.', 'success')
    except Exception as e:
        flash(f'Error removing command: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('hotfix_monitoring'))

# Route for regular monitoring
@app.route('/regular_monitoring')
def regular_monitoring():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('regular_monitoring.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Run the application
if __name__ == '__main__':
    if not os.path.exists('hotfix_input.db'):
        conn = get_db_connection()
        conn.execute('CREATE TABLE hotfix_inputs (id INTEGER PRIMARY KEY, command TEXT UNIQUE, status TEXT, rollback_build_url TEXT, rollback_cl TEXT, action TEXT)')
        conn.commit()
        conn.close()
    app.run(debug=True)
