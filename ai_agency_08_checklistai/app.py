from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TimeField, FieldList, FormField, HiddenField
from wtforms.validators import DataRequired, Email, Optional
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time
from pydantic import BaseModel
from utils.email_utils import send_email
from utils.constants import EXAMPLE_CHECKLISTS
from utils.email_utils import HTML_TEMPLATE

from checklist_flow.src.checklist_flow.main import main

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import logging
from openai import OpenAI
from config import Config

from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checklists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    schedule_time = db.Column(db.Time, nullable=True)  # Change this line
    recipients = db.Column(db.Text, nullable=False)
    items = db.relationship('ChecklistItem', back_populates='checklist', lazy=True, cascade='all, delete-orphan')

class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    checklist = db.relationship('Checklist', back_populates='items')

class ChecklistItemForm(FlaskForm):
    id = HiddenField('ID')
    item = StringField('Item', validators=[DataRequired()])

class ChecklistForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    schedule_time = TimeField('Schedule Time', validators=[Optional()])  # Change this line
    recipients = StringField('Recipients (comma-separated emails)', validators=[DataRequired()])
    items = FieldList(FormField(ChecklistItemForm), min_entries=1)

# Add this new route after the other route definitions
@app.route('/')
def index():
    checklists = Checklist.query.all()
    form = ChecklistForm()  # This is for the CSRF token in the update title form
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
            db.session.flush()  # This assigns an ID to the checklist

            for item_form in form.items:
                item = ChecklistItem(content=item_form.item.data, checklist_id=checklist.id)
                db.session.add(item)

            db.session.commit()
            
            # Schedule the new checklist only if schedule_time is provided
            if checklist.schedule_time:
                schedule_checklist(checklist.id)
            
            flash('Checklist created successfully!', 'success')
            return redirect(url_for('view_checklist', id=checklist.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating checklist: {str(e)}', 'danger')
            app.logger.error(f'Error creating checklist: {str(e)}')
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
            item_id = request.form['delete_item_id']
            item = ChecklistItem.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                # flash('Item deleted successfully', 'success')
        elif 'add_item' in request.form:
            new_item_content = request.form['add_item']
            if new_item_content.strip():
                new_item = ChecklistItem(content=new_item_content, checklist_id=checklist.id)
                db.session.add(new_item)
                db.session.commit()
                # flash('New item added successfully', 'success')
        elif 'item_id' in request.form and 'item' in request.form:
            item_id = request.form['item_id']
            content = request.form['item']
            item = ChecklistItem.query.get(item_id)
            if item:
                item.content = content
                db.session.commit()
                # flash('Item updated successfully', 'success')
        
        # Handle other form submissions (title, schedule, recipients)
        checklist.title = request.form.get('title', checklist.title)
        new_schedule_time = request.form.get('schedule_time')
        
        # Check if schedule time has changed
        if new_schedule_time != checklist.schedule_time:
            checklist.schedule_time = datetime.strptime(new_schedule_time, '%H:%M').time() if new_schedule_time else None
            db.session.commit()
            
            # Reschedule the checklist
            reschedule_checklist(checklist.id)
            # flash('Checklist rescheduled successfully', 'success')
        
        checklist.recipients = request.form.get('recipients', checklist.recipients)
        db.session.commit()
        
        return redirect(url_for('view_checklist', id=checklist.id))
    
    return render_template('view_checklist.html', form=form, checklist=checklist)

def reschedule_checklist(checklist_id):
    # Remove existing job if it exists
    job_id = f"checklist_{checklist_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
    
    # Schedule the checklist
    schedule_checklist(checklist_id)

@app.route('/delete/<int:id>')
def delete_checklist(id):
    checklist = Checklist.query.get_or_404(id)
    try:
        # Delete all related checklist items first
        ChecklistItem.query.filter_by(checklist_id=id).delete()
        
        # Now delete the checklist
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

def send_checklist_email(checklist_id):
    with app.app_context():
        logger.info(f"Attempting to send email for checklist ID: {checklist_id}")
        try:
            checklist = Checklist.query.get(checklist_id)
            
            if checklist:
                logger.info(f"Checklist found: {checklist.title}")
                recipients = [email.strip() for email in checklist.recipients.split(',')]
                logger.info(f"Recipients: {recipients}")

                items_text = "\n".join([f"- {item.content}" for item in checklist.items])
                email_body = main(items_text)

                formatted_html = HTML_TEMPLATE.format(
                    title=checklist.title,
                    final_email_body=email_body
                )

                send_email(
                    subject=f"Checklist: {checklist.title}",
                    body=formatted_html,
                    sender=app.config['MAIL_USERNAME'],
                    recipients=recipients,
                    smtp_server=app.config['MAIL_SERVER'],
                    smtp_port=app.config['MAIL_PORT'],
                    username=app.config['MAIL_USERNAME'],
                    password=app.config['MAIL_PASSWORD']
                )

                logger.info("Email sent successfully")
            else:
                logger.error(f"Checklist with ID {checklist_id} not found")
        except Exception as e:
            logger.error(f"Error sending email for checklist {checklist_id}: {str(e)}")

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_checklist(checklist_id):
    checklist = Checklist.query.get(checklist_id)
    if checklist:
        if checklist.schedule_time:
            logger.info(f"Scheduling checklist: {checklist.title} (ID: {checklist_id}) for {checklist.schedule_time}")
            scheduler.add_job(
                send_checklist_email,
                'cron',
                hour=checklist.schedule_time.hour,
                minute=checklist.schedule_time.minute,
                args=[checklist_id],
                id=f"checklist_{checklist_id}"
            )
            logger.info(f"Checklist scheduled successfully")
        else:
            logger.info(f"Checklist: {checklist.title} (ID: {checklist_id}) has no schedule time set. Skipping scheduling.")
    else:
        logger.error(f"Failed to schedule checklist. Checklist with ID {checklist_id} not found")

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

@app.route('/init-scheduler')
def initialize_scheduler():
    init_scheduler()
    return "Scheduler initialized"

# Add this new route after the other route definitions
@app.route('/add_item', methods=['POST'])
@csrf.exempt
def add_item():
    return jsonify({'status': 'success'})

@app.route('/test-email/<int:checklist_id>')
def test_email(checklist_id):
    logger.info(f"Testing email for checklist ID: {checklist_id}")
    send_checklist_email(checklist_id)
    return "Email test triggered. Check logs for details."

@app.route('/create-example/<example>')
def create_example_checklist(example):
    example_checklists = EXAMPLE_CHECKLISTS

    if example in example_checklists:
        checklist_data = example_checklists[example]
        checklist = Checklist(
            title=checklist_data['title'],
            schedule_time=None,  # Remove default schedule
            recipients='example@example.com'  # Default recipient
        )
        db.session.add(checklist)
        db.session.flush()  # This assigns an ID to the checklist

        for item_content in checklist_data['items']:
            item = ChecklistItem(content=item_content, checklist_id=checklist.id)
            db.session.add(item)

        db.session.commit()
        flash(f'Example checklist "{checklist_data["title"]}" created successfully!', 'success')
        return redirect(url_for('edit_checklist', id=checklist.id))  # Redirect to edit page instead of view
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
        class MyChecklist(BaseModel):
            title: str
            items: list[str]

        # Generate checklist using OpenAI
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Extract the checklist information."},
                {"role": "user", "content": f"Create a checklist for: {prompt}. Give a fun title for the description of the checklist they provided."},
            ],
            response_format=MyChecklist,
        )

        # Parse the AI response
        ai_checklist = completion.choices[0].message.parsed

        print("AI CHECKLIST")
        print(ai_checklist)

        # Create a new Checklist
        new_checklist = Checklist(
            title=ai_checklist.title,
            schedule_time=None,
            recipients='example@example.com'  # Default recipient
        )
        db.session.add(new_checklist)
        db.session.flush()  # This assigns an ID to the checklist

        print("NEW CHECKLIST")
        print(new_checklist)

        # Add items to the checklist
        for item_content in ai_checklist.items:
            item = ChecklistItem(content=item_content, checklist_id=new_checklist.id)
            db.session.add(item)

        db.session.commit()
        flash(f'AI-generated checklist "{new_checklist.title}" created successfully!', 'success')
        return redirect(url_for('view_checklist', id=new_checklist.id))

    except Exception as e:
        flash(f'Error generating AI checklist: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        init_scheduler()
    logger.info("Starting Flask application")
    app.run(debug=True, port=5052)
