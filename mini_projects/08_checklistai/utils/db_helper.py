from datetime import datetime
from db.models import db, Checklist, ChecklistItem

def delete_checklist_item(item_id):
    item = ChecklistItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()

def add_checklist_item(checklist_id, content):
    if content.strip():
        new_item = ChecklistItem(content=content, checklist_id=checklist_id)
        db.session.add(new_item)
        db.session.commit()

def update_checklist_item(item_id, content):
    item = ChecklistItem.query.get(item_id)
    if item:
        item.content = content
        db.session.commit()

def update_checklist(checklist, form_data, reschedule_function):
    checklist.title = form_data.get('title', checklist.title)
    new_schedule_time = form_data.get('schedule_time')
    
    if new_schedule_time != checklist.schedule_time:
        checklist.schedule_time = datetime.strptime(new_schedule_time, '%H:%M').time() if new_schedule_time else None
        reschedule_function(checklist.id)
    
    checklist.recipients = form_data.get('recipients', checklist.recipients)
    db.session.commit()

def create_checklist_from_data(checklist_data):
    checklist = Checklist(
        title=checklist_data['title'],
        schedule_time=None,
        recipients='example@example.com'
    )
    db.session.add(checklist)
    db.session.flush()

    for item_content in checklist_data['items']:
        item = ChecklistItem(content=item_content, checklist_id=checklist.id)
        db.session.add(item)

    db.session.commit()
    return checklist
