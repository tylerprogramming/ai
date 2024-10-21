from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checklist: {title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        ul {{ padding-left: 20px; }}
        .footer {{ margin-top: 20px; font-size: 0.8em; color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Checklist: {title}</h1>
        {final_email_body}
        <div class="footer">
            <p>This email was sent by ChecklistAI. To unsubscribe, <a href="http://example.com/unsubscribe">click here</a>.</p>
        </div>
    </div>
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
