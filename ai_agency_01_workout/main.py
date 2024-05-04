from flask import Flask, render_template, request, Response

import agents
import system_messages

app = Flask(__name__)


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

        agents.user_proxy.initiate_chat(
            agents.fitness_expert,
            message=system_messages.get_initiate_message(days_option, selected_options, level_option),
        )

        last_message = agents.user_proxy.last_message()["content"]
        response_text = last_message

        global doc
        doc = response_text

    return render_template('index.html', response_text=response_text)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
