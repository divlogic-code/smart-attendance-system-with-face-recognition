from flask import Flask, render_template, request
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.sheets_api import get_attendance_for_student

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    roll_number = request.form['roll_number']

    # ✅ Use the Sheets API instead of CSV
    records = get_attendance_for_student(roll_number)

    return render_template('dashboard.html', roll_number=roll_number, records=records)

if __name__ == '__main__':
    app.run(debug=True)
