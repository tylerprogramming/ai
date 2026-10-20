import asyncio
import os

from flask import Flask, render_template, request, Response

import agents

app = Flask(__name__)

doc = ""


@app.route('/download_text_file')
def download_text_file():
    return Response(
        doc,
        mimetype='application/msword',
        headers={'Content-disposition': 'attachment; filename=workout.doc'})


@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""
    if request.method == 'POST':
        days_option = request.form.getlist('days')
        selected_options = request.form.getlist('option')
        level_option = request.form.getlist('level')

        # AutoGen v0.7 is async, so run the agent with asyncio.run inside the route
        response_text = asyncio.run(
            agents.create_workout_plan(days_option, selected_options, level_option)
        )

        global doc
        doc = response_text

    return render_template('index.html', response_text=response_text)


if __name__ == '__main__':
    # Debug mode is off by default; set FLASK_DEBUG=1 to turn it on while developing
    app.run(debug=os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true"), port=5001)
