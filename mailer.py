import smtplib
import ssl
from email.message import EmailMessage
from config import EMAIL, PASSWORD
import time

LIMIT_PER_RUN = 50  # Safe limit per run

def send_bulk_mail():
    try:
        context = ssl.create_default_context()

        with open("recipients.txt", "r") as file:
            recipients = file.read().splitlines()

        recipients = recipients[:LIMIT_PER_RUN]

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL, PASSWORD)

            for email in recipients:
                msg = EmailMessage()
                msg["From"] = EMAIL
                msg["To"] = email
                msg["Subject"] = "Hello from Python Mailer"

                msg.set_content("This is a test email sent safely.")

                server.send_message(msg)
                time.sleep(2)  # delay to reduce spam risk

        return "Emails Sent Successfully"

    except Exception as e:
        return str(e)
