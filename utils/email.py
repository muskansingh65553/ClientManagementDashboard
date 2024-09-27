import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_otp_email(to_email, otp):
    # Note: In a production environment, you would use environment variables for these credentials
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your OTP for CRM Login"
    message["From"] = sender_email
    message["To"] = to_email

    text = f"Your OTP is: {otp}"
    html = f"""\
    <html>
      <body>
        <p>Your OTP is: <strong>{otp}</strong></p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
