# Import necessary modules
from flask import Flask, render_template, request, redirect
import sqlite3

# Create Flask application
app = Flask(__name__)

# Set up SQLite database connection
conn = sqlite3.connect('feedback.db')
cursor = conn.cursor()

# Create table for feedback records if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        experience TEXT
    )
''')
conn.commit()


# Route for the feedback form
@app.route('/', methods=['GET', 'POST'])
def feedback_form():
    if request.method == 'POST':
        # Get the feedback from the form
        experience = request.form['experience']

        # Insert the feedback into the database
        cursor.execute('INSERT INTO feedback (experience) VALUES (?)', (experience,))
        conn.commit()

        # Redirect to the thank-you page
        return redirect('/thankyou')

    # Render the feedback form template
    return render_template('index.html')


# Route for the thank-you page
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


# Route for the admin page
@app.route('/admin')
def admin():
    # Retrieve all feedback records from the database
    cursor.execute('SELECT * FROM feedback')
    feedback_records = cursor.fetchall()

    # Render the admin page template with the feedback records
    return render_template('admin.html', feedback_records=feedback_records)


# Run the Flask application
if __name__ == '__main__':
    app.run()
