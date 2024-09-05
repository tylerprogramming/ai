from flask import Flask, render_template, request, redirect, url_for, session
from workout_agents import WorkoutPlannerSystem  # Import the class
import json
import ast
import pdfkit
from flask import send_file
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

@app.route('/', methods=['GET', 'POST'])
def screen1():
    if request.method == 'POST':
        session['age'] = request.form['age']
        session['gender'] = request.form['gender']
        session['fitness_level'] = request.form['fitness_level']
        session['goals'] = request.form.getlist('goals')
        return redirect(url_for('screen2'))
    return render_template('screen1.html', active_step=1, active_screen='screen1')

@app.route('/screen2', methods=['GET', 'POST'])
def screen2():
    if request.method == 'POST':
        session['workout_duration'] = request.form['workout_duration']
        session['workout_type'] = request.form['workout_type']
        session['equipment'] = request.form.getlist('equipment')
        return redirect(url_for('screen3'))
    return render_template('screen2.html', active_step=2, active_screen='screen2')

@app.route('/screen3', methods=['GET', 'POST'])
def screen3():
    if request.method == 'POST':
        session['workout_days'] = request.form['workout_days']
        session['intensity'] = request.form['intensity']
        session['workout_time'] = request.form['workout_time']
        return redirect(url_for('screen4'))
    return render_template('screen3.html', active_step=3, active_screen='screen3')

@app.route('/screen4', methods=['GET', 'POST'])
def screen4():
    if request.method == 'POST':
        session['warmup_cooldown'] = request.form.get('warmup_cooldown', 'No')
        session['focus_areas'] = request.form.getlist('focus_areas')
        return redirect(url_for('workout_plan'))
    return render_template('screen4.html', active_step=4, active_screen='screen4')

@app.route('/workout_plan')
def workout_plan():
    # Generate the workout plan using the collected data
    user_data = {
        'age': session['age'],
        'gender': session['gender'],
        'fitness_level': session['fitness_level'],
        'goals': session['goals'],
        'workout_duration': session['workout_duration'],
        'workout_type': session['workout_type'],
        'equipment': session['equipment'],
        'workout_days': session['workout_days'],
        'intensity': session['intensity'],
        'workout_time': session['workout_time'],
        'warmup_cooldown': session['warmup_cooldown'],
        'focus_areas': session['focus_areas']
    }

    plan = WorkoutPlannerSystem().generate_plan(user_data)

    cleaned_plan = plan
    if "```json" in cleaned_plan:
        cleaned_plan = cleaned_plan.replace("```json", "")
    if "```" in cleaned_plan:
        cleaned_plan = cleaned_plan.replace("```", "")
    if "TERMINATE" in cleaned_plan:
        cleaned_plan = cleaned_plan.replace("TERMINATE", "")

    json_plan = json.loads(cleaned_plan)

    try:
        return render_template('workout_plan.html', active_step=5, active_screen='workout_plan', plan=json_plan)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return render_template('error.html', error_message="Failed to generate workout plan. Please try again.")


@app.route('/export_pdf')
def export_pdf():
    # Path to your markdown file
    path_to_md_file = 'workout_plan.md'
    
    # Send the file as a download to the user
    return send_file(path_to_md_file, as_attachment=True, download_name='workout_plan.md')



if __name__ == '__main__':
    app.run(debug=True)