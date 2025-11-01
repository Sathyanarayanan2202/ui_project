from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# ------------------ MySQL Connection Setup ------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",        
        user="root",             
        password="@Sathya@2202",
        database="logindb"       
    )

# ------------------ Home Route ------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ------------------ Register Route ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        # Create table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')

        # Check if email already exists
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash('Email already registered. Please login.', 'error')
            conn.close()
            return redirect(url_for('login'))

        # Insert new user
        cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                    (username, email, hashed_password))
        conn.commit()
        conn.close()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# ------------------ Login Route ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            flash(f'Welcome, {user[1]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# ------------------ Dashboard Route ------------------
@app.route('/dashboard')
def dashboard():
    return "<h2>Welcome to your dashboard!</h2><p>Login successful.</p>"

# ------------------ Run App ------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
