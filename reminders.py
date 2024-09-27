from flask import current_app
from models import Client
from app import db
from datetime import datetime, date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_reminder_email(client):
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')

    message = MIMEMultipart("alternative")
    message["Subject"] = "Reminder: Follow-up with " + client.company_name
    message["From"] = sender_email
    message["To"] = client.email

    text = f"""
    Dear {client.contact_name},

    This is a friendly reminder about your upcoming follow-up with {client.company_name}.

    Message: {client.reminder_message}

    Best regards,
    Your CRM Team
    """

    html = f"""
    <html>
      <body>
        <p>Dear {client.contact_name},</p>
        <p>This is a friendly reminder about your upcoming follow-up with {client.company_name}.</p>
        <p><strong>Message:</strong> {client.reminder_message}</p>
        <p>Best regards,<br>Your CRM Team</p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, client.email, message.as_string())
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False

def check_and_send_reminders():
    today = date.today()
    clients_to_remind = Client.query.filter(
        Client.reminder_date == today,
        (Client.last_reminder_sent == None) | (Client.last_reminder_sent.cast(db.Date) < today)
    ).all()

    for client in clients_to_remind:
        if send_reminder_email(client):
            client.last_reminder_sent = datetime.now()
            db.session.commit()

if __name__ == "__main__":
    check_and_send_reminders()
