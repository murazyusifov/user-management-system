from flask import Flask, render_template, request, redirect, url_for, flash
import bcrypt
import mysql.connector
from mysql.connector import Error
import re

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

@app.after_request
def apply_csp(response):
    # Setting a basic CSP that only allows scripts and styles from the same origin
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
    return response

# Database connection configuration
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Use your MySQL username
        password="root",  # Use your MySQL password
        database="chatroomFinal"  # Use your database name
    )

# Validation functions
def is_valid_username(username):
    return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

def is_valid_password(password):
    return bool(re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@$!%*?&]).{8,}$', password))

def is_valid_full_name(full_name):
    return re.match(r'^[a-zA-Z\s]{3,50}$', full_name) is not None

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']

        # Validate inputs
        if not is_valid_username(username):
            flash('Username must be between 3 and 20 characters, and can only contain letters, numbers, and underscores.', 'danger')
            return redirect(url_for('register'))

        if not is_valid_password(password):
            flash('Password must be at least 8 characters long and contain an uppercase letter, a lowercase letter, a number, and a special character.', 'danger')
            return redirect(url_for('register'))

        if not is_valid_full_name(full_name):
            flash('Full name must be between 3 and 50 characters and can only contain alphabetic characters and spaces.', 'danger')
            return redirect(url_for('register'))

        # Check if passwords match
        if password != password_confirmation:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register'))

        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user in the database
        try:
            # Establish a database connection
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username already exists. Please choose a different one.', 'danger')
                return redirect(url_for('register'))

            # Insert the new user into the database
            cursor.execute(
                "INSERT INTO users (username, full_name, password_hash) VALUES (%s, %s, %s)",
                (username, full_name, password_hash)
            )

            conn.commit()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))  # Redirect to login page after registration

        except Error as e:
            print(f"Error: {e}")
            flash('Something went wrong. Please try again.', 'danger')
            return redirect(url_for('register'))

        finally:
            # Ensure that cursor and connection are closed properly
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('register.html')

# Login route (example, you'll need to implement the actual login logic)
@app.route('/login')
def login():
    return render_template('login.html')  # Replace with your actual login page

if __name__ == '__main__':
    app.run(debug=True)
