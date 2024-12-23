'''
    Author: Aaryan Sharma
    Date: December 2024
    Project: Stock Portfolio Dashboard
    File: app.py
'''

from flask import *
from flask_bcrypt import Bcrypt
import sqlite3
from datetime import timedelta, datetime
import random
import csv

# Initialize Flask app and Flask-Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Set secret key and session lifetime
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=15)

# List of greetings in different languages
GREETINGS = [
    {"word": "Hello", "language": "English"},
    {"word": "Hola", "language": "Spanish"},
    {"word": "Bonjour", "language": "French"},
    {"word": "Hallo", "language": "German"},
    {"word": "Ciao", "language": "Italian"},
    {"word": "Namaste", "language": "Hindi"},
    {"word": "Salaam", "language": "Persian"},
    {"word": "Zdravstvuyte", "language": "Russian"},
    {"word": "Nǐ hǎo", "language": "Chinese"},
    {"word": "Konnichiwa", "language": "Japanese"},
    {"word": "Annyeonghaseyo", "language": "Korean"},
    {"word": "Merhaba", "language": "Turkish"},
    {"word": "Sawasdee", "language": "Thai"},
    {"word": "Xin chào", "language": "Vietnamese"},
    {"word": "Olá", "language": "Portuguese"}
]


def init_db():
    """Initialize the database and create the credentials table if it doesn't exist."""
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT UNIQUE NOT NULL,
                            hashed_password TEXT NOT NULL)''')
        conn.commit()


# Initialize the database on app start
init_db()


@app.before_request
def session_management():
    """Manage session timeout and update session activity."""
    session.permanent = True
    if 'user_id' in session:
        last_activity = session.get('last_activity')
        if last_activity:
            last_activity_time = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')
            elapsed_time = (datetime.now() - last_activity_time).total_seconds()
            remaining_time = app.permanent_session_lifetime.total_seconds() - elapsed_time

            # Handle session expiration
            if remaining_time <= 0:
                session.pop('user_id', None)
                session.pop('last_activity', None)
                flash("Session timed out. Please log in again.")
                return redirect(url_for('login'))

            # Update session activity
            session['remaining_time'] = remaining_time
        session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif request.endpoint not in ['login']:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        # Verify user credentials
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT hashed_password FROM credentials WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()

            if result and bcrypt.check_password_hash(result[0], password):
                # Initialize session for successful login
                session['user_id'] = user_id
                session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials. Please try again.")
                return redirect(url_for('login'))

    # Render login page
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Render the dashboard and handle data filtering."""
    if 'user_id' in session:
        greeting = random.choice(GREETINGS)

        # Read data from CSV file
        file_path = 'order_history.csv'
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            all_data = list(reader)

        # Generate a list of distinct users
        user_list = sorted(set(row['ouser'] for row in all_data))

        # Initialize variables for filtered data
        data = None
        selected_date = None
        selected_user = None

        if request.method == 'POST':
            selected_date = request.form.get('inp_date', datetime.now().strftime('%Y-%m-%d'))
            selected_user = request.form.get('inp_user', user_list[0])

            # Filter rows by selected user and date
            filtered_data = [
                row for row in all_data
                if row['ouser'] == selected_user and row['odate'] < selected_date
            ]

            # Format filtered data
            formatted_data = []
            for row in filtered_data:
                profit_loss = float(row['oltp']) - float(row['obp'])
                profit_loss_percent = (profit_loss / float(row['obp'])) * 100

                # Insert profit/loss details and highlight classes
                formatted_row = list(row.values())
                ltp_index = list(row.keys()).index('oltp') + 1
                formatted_row.insert(ltp_index, f"+{profit_loss:.2f}" if profit_loss > 0 else f"{profit_loss:.2f}")
                formatted_row.insert(ltp_index + 1, f"+{profit_loss_percent:.2f}%" if profit_loss_percent > 0 else f"{profit_loss_percent:.2f}%")

                if profit_loss_percent >= 5:
                    formatted_row.append('green-highlight')
                elif profit_loss_percent <= -5:
                    formatted_row.append('red-highlight')
                else:
                    formatted_row.append('')
                formatted_data.append(formatted_row)

            data = formatted_data

        # Pass remaining session time to the front-end
        remaining_time = session.get('remaining_time', app.permanent_session_lifetime.total_seconds())

        return render_template(
            'dashboard.html',
            greeting_word=greeting["word"],
            greeting_language=greeting["language"],
            user_id=session['user_id'],
            user_list=user_list,
            selected_date=selected_date,
            selected_user=selected_user,
            data=data,
            session_timeout_ms=remaining_time * 1000
        )

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('user_id', None)
    session.pop('last_activity', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route("/")
def connect():
    """Redirect to login page."""
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
