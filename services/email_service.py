import smtplib
from email.mime.text import MIMEText

def send_email(to_email, message):
    try:
        sender = "carparkhub25@gmail.com"
        app_password = "xpxmkoxwmnbajlut"

        msg = MIMEText(message)
        msg["Subject"] = "Parking Reminder"
        msg["From"] = sender
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, app_password)
            server.sendmail(sender, to_email, msg.as_string())

        print("Email sent!")
    except Exception as e:
        print("Email error:", e)
