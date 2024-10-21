import os
import logging
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_mail import Mail

from apscheduler.schedulers.background import BackgroundScheduler

from openai import OpenAI
from dotenv import load_dotenv

from db.models import db, Checklist, ChecklistItem
from utils.form_classes import ChecklistForm
from utils.email_utils import send_checklist_email, HTML_TEMPLATE

from utils.constants import EXAMPLE_CHECKLISTS
from agents.checklist_agent import ChecklistAgent
from checklist_flow.src.checklist_flow.main import main

# Add this import at the top of the file
from utils.db_helper import (
    delete_checklist_item,
    add_checklist_item,
    update_checklist_item,
    update_checklist,
    create_checklist_from_data
)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app and configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checklists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize extensions
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Initialize OpenAI client and ChecklistAgent
client = OpenAI()
checklist_agent = ChecklistAgent(client)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Route handlers
@app.route('/')
def index():
    checklists = Checklist.query.all()
    form = ChecklistForm()
    return render_template('index.html', checklists=checklists, form=form)

@app.route('/create', methods=['GET', 'POST'])
def create_checklist():
    form = ChecklistForm()
    if form.validate_on_submit():
        try:
            checklist = Checklist(
                title=form.title.data,
                schedule_time=form.schedule_time.data if form.schedule_time.data else None,
                recipients=form.recipients.data
            )
            db.session.add(checklist)
            db.session.flush()

            for item_form in form.items:
                item = ChecklistItem(content=item_form.item.data, checklist_id=checklist.id)
                db.session.add(item)

            db.session.commit()
            
            if checklist.schedule_time:
                schedule_checklist(checklist.id)
            
            flash('Checklist created successfully!', 'success')
            return redirect(url_for('view_checklist', id=checklist.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating checklist: {str(e)}', 'danger')
            logger.error(f'Error creating checklist: {str(e)}')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'danger')

    return render_template('create_checklist.html', form=form)

@app.route('/checklist/<int:id>', methods=['GET', 'POST'])
def view_checklist(id):
    checklist = Checklist.query.get_or_404(id)
    form = ChecklistForm(obj=checklist)
    
    if request.method == 'POST':
        if 'delete_item_id' in request.form:
            delete_checklist_item(request.form['delete_item_id'])
        elif 'add_item' in request.form:
            add_checklist_item(checklist.id, request.form['add_item'])
        elif 'item_id' in request.form and 'item' in request.form:
            update_checklist_item(request.form['item_id'], request.form['item'])
        
        update_checklist(checklist, request.form, reschedule_checklist)
        
        return redirect(url_for('view_checklist', id=checklist.id))
    
    return render_template('view_checklist.html', form=form, checklist=checklist)

def reschedule_checklist(checklist_id):
    job_id = f"checklist_{checklist_id}"

    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    
    schedule_checklist(checklist_id)

@app.route('/delete/<int:id>')
def delete_checklist(id):
    checklist = Checklist.query.get_or_404(id)
    try:
        ChecklistItem.query.filter_by(checklist_id=id).delete()
        db.session.delete(checklist)
        db.session.commit()
        flash('Checklist and all its items deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting checklist: {str(e)}', 'danger')
        logger.error(f'Error deleting checklist: {str(e)}')
    return redirect(url_for('index'))

@app.route('/update_title/<int:id>', methods=['POST'])
def update_title(id):
    checklist = Checklist.query.get_or_404(id)
    new_title = request.form.get('title')
    if new_title:
        checklist.title = new_title
        db.session.commit()
        flash('Checklist title updated successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/create-example/<example>')
def create_example_checklist(example):
    if example in EXAMPLE_CHECKLISTS:
        checklist_data = EXAMPLE_CHECKLISTS[example]
        checklist = create_checklist_from_data(checklist_data)
        flash(f'Example checklist "{checklist_data["title"]}" created successfully!', 'success')
        return redirect(url_for('view_checklist', id=checklist.id))
    else:
        flash('Invalid example checklist selected.', 'danger')
        return redirect(url_for('index'))

@app.route('/generate-ai-checklist', methods=['POST'])
def generate_ai_checklist():
    prompt = request.form.get('ai_prompt')
    if not prompt:
        flash('Please provide a prompt for the AI.', 'warning')
        return redirect(url_for('index'))

    try:
        ai_checklist = checklist_agent.generate_checklist(prompt)
        new_checklist = create_checklist_from_data({
            'title': ai_checklist.title,
            'items': ai_checklist.items
        })
        flash(f'AI-generated checklist "{new_checklist.title}" created successfully!', 'success')
        return redirect(url_for('view_checklist', id=new_checklist.id))
    except Exception as e:
        flash(f'Error generating AI checklist: {str(e)}', 'danger')
        return redirect(url_for('index'))

def init_scheduler():
    with app.app_context():
        logger.info("Initializing scheduler")
        checklists = Checklist.query.all()
        scheduled_count = 0
        for checklist in checklists:
            if checklist.schedule_time:
                schedule_checklist(checklist.id)
                scheduled_count += 1
            else:
                logger.info(f"Checklist: {checklist.title} (ID: {checklist.id}) has no schedule time set. Skipping scheduling.")
        logger.info(f"Scheduled {scheduled_count} out of {len(checklists)} checklists")

# Add this function after the other helper functions

def schedule_checklist(checklist_id):
    checklist = Checklist.query.get(checklist_id)
    if checklist:
        if checklist.schedule_time:
            logger.info(f"Scheduling checklist: {checklist.title} (ID: {checklist_id}) for {checklist.schedule_time}")
            try:    
                scheduler.add_job(
                    send_checklist_email,
                    'cron',
                    hour=checklist.schedule_time.hour,
                    minute=checklist.schedule_time.minute,
                    args=[checklist_id, app],  # Pass the app instance here
                    id=f"checklist_{checklist_id}"
                )
                logger.info(f"Checklist scheduled successfully")
            except Exception as e:
                logger.error(f"Error scheduling checklist: {str(e)}")
        else:
            logger.info(f"Checklist: {checklist.title} (ID: {checklist_id}) has no schedule time set. Skipping scheduling.")
    else:
        logger.error(f"Failed to schedule checklist. Checklist with ID {checklist_id} not found")

if __name__ == '__main__':
    with app.app_context():
        init_scheduler()
    logger.info("Starting Flask application")
    app.run(debug=os.getenv('CHECKLIST_AI_FLASK_DEBUG'), port=os.getenv('CHECKLIST_AI_FLASK_PORT'))
