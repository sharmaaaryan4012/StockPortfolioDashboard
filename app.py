from flask import *
from flask_bcrypt import Bcrypt
import sqlite3
from datetime import timedelta, datetime
import random

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=1)

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
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (
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
            elapsed_time = (datetime.now() - last_activity_time).total_seconds()
            remaining_time = app.permanent_session_lifetime.total_seconds() - elapsed_time

            # If session has expired
            if remaining_time <= 0:
                session.pop('user_id', None)
                session.pop('last_activity', None)
                flash("Session timed out. Please log in again.")
                return redirect(url_for('login'))

            # Update the session with remaining time
            session['remaining_time'] = remaining_time
        session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif request.endpoint not in ['login']:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT hashed_password FROM credentials WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()

            if result and bcrypt.check_password_hash(result[0], password):
                session['user_id'] = user_id
                session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Initialize last activity
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials. Please try again.")
                return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        greeting = random.choice(GREETINGS)
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()

            # Fetch all distinct users from the data table
            cursor.execute("SELECT DISTINCT ouser FROM order_history")
            user_list = [row[0] for row in cursor.fetchall()]

            # Initialize variables
            data = None  # No data on first load
            selected_date = None
            selected_user = None

            if request.method == 'POST':
                selected_date = request.form.get('inp_date', datetime.now().strftime('%Y-%m-%d'))
                selected_user = request.form.get('inp_user', user_list[0])

                # Fetch all orders before the selected date for the given user
                cursor.execute(
                    """
                    SELECT * FROM order_history
                    WHERE ouser = ? AND date(odate) < ?
                    ORDER BY odate DESC
                    """,
                    (selected_user, selected_date)
                )
                data = cursor.fetchall()

        # Pass remaining session time
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
    session.pop('user_id', None)
    session.pop('last_activity', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route("/")
def connect():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)