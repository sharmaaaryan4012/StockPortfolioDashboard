from flask import *
from flask_bcrypt import Bcrypt
import sqlite3
import os
from datetime import timedelta, datetime
import random

app = Flask(__name__)
bcrypt = Bcrypt(app)

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
    with sqlite3.connect('credentials.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT UNIQUE NOT NULL,
                            hashed_password TEXT NOT NULL)''')
        conn.commit()

init_db()

@app.before_request
def session_management():
    session.permanent = True
    if 'user_id' in session:
        last_activity = session.get('last_activity')
        if last_activity:
            last_activity_time = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')
            if (datetime.now() - last_activity_time) > app.permanent_session_lifetime:
                session.pop('user_id', None)  # Log out the user
                session.pop('last_activity', None)
                flash("Session timed out. Please log in again.")
                return redirect(url_for('login'))
        session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif request.endpoint not in ['login']:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        with sqlite3.connect('credentials.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT hashed_password FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()

            if result and bcrypt.check_password_hash(result[0], password):
                session['user_id'] = user_id
                session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Initialize last activity
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials. Please try again.")
                return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        session_timeout_ms = app.permanent_session_lifetime.total_seconds() * 1000

        # Select a random greeting
        greeting = random.choice(GREETINGS)

        return render_template(
            'dashboard.html',
            user_id=session['user_id'],
            greeting_word=greeting["word"],
            greeting_language=greeting["language"],
            session_timeout_ms=session_timeout_ms
        )
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('last_activity', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route("/")
def connect():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)