from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, FieldList, FormField, HiddenField
from wtforms.validators import DataRequired, Optional

class ChecklistItemForm(FlaskForm):
    id = HiddenField('ID')
    item = StringField('Item', validators=[DataRequired()])

class ChecklistForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    schedule_time = TimeField('Schedule Time', validators=[Optional()])
    recipients = StringField('Recipients (comma-separated emails)', validators=[DataRequired()])
    items = FieldList(FormField(ChecklistItemForm), min_entries=1)
