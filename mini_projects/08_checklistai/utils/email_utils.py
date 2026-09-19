from flask import current_app
from flask_mail import Message
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from checklist_flow.src.checklist_flow.main import main
from db.models import Checklist

logger = logging.getLogger(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    {final_email_body}
</body>
</html>
"""

def send_email(subject, body, sender, recipients, smtp_server, smtp_port, username, password):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

def send_checklist_email(checklist_id, app):
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
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=recipients,
                    smtp_server=current_app.config['MAIL_SERVER'],
                    smtp_port=current_app.config['MAIL_PORT'],
                    username=current_app.config['MAIL_USERNAME'],
                    password=current_app.config['MAIL_PASSWORD']
                )

                logger.info("Email sent successfully")
            else:
                logger.error(f"Checklist with ID {checklist_id} not found")
        except Exception as e:
            logger.error(f"Error sending email for checklist {checklist_id}: {str(e)}")
