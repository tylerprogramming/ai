from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    schedule_time = db.Column(db.Time, nullable=True)
    recipients = db.Column(db.Text, nullable=False)
    items = db.relationship('ChecklistItem', back_populates='checklist', lazy=True, cascade='all, delete-orphan')

class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist.id'), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    checklist = db.relationship('Checklist', back_populates='items')
