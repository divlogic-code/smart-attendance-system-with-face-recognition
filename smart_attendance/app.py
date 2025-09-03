from flask import Flask, render_template, request, redirect, session, url_for
import json
import os
from backend.sheets_api import fetch_attendance  # you already use this

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # for session management

# Load users from JSON
def load_users():
    path = os.path.join(os.path.dirname(__file__), 'users.json')
    with open(path, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    error = None

    if request.method == 'POST':
        roll = request.form['roll_number']
        password = request.form['password']

        user = users.get(roll)
        if user and user['password'] == password:
            session['roll_number'] = roll
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid roll number or password."

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'roll_number' not in session:
        return redirect('/login')

    roll = session['roll_number']
    records = fetch_attendance(roll)  # assuming it returns a list of tuples [(date, status), ...]

    return render_template('dashboard.html', roll_number=roll, records=records)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
