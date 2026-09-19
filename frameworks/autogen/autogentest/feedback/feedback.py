from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('feedback.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  experience TEXT)''')
    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        experience = request.form['experience']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO feedback (experience) VALUES (?)", (experience,))
        conn.commit()
        conn.close()
        return redirect('/thankyou')
    return render_template('index.html')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@app.route('/admin')
def admin():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM feedback")
    feedback = c.fetchall()
    return render_template('admin.html', feedback=feedback)


if __name__ == '__main__':
    create_table()
    app.run()
