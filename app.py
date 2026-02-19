import asyncio
import aiosmtplib
import re
from email.message import EmailMessage
from config import *
from dotenv import load_dotenv
import os

load_dotenv()

# ===== USER INPUT =====
SENDER_EMAIL = input("Enter Gmail: ").strip()
APP_PASSWORD = input("Enter App Password: ").strip()
SENDER_NAME = input("Sender Name: ").strip()
SUBJECT = input("Subject: ").strip()
MESSAGE_BODY = input("Message: ").strip()

# ===== VALIDATION =====
if len(SUBJECT) > MAX_SUBJECT_LENGTH:
    raise ValueError("Subject too long")

if len(MESSAGE_BODY) > MAX_MESSAGE_LENGTH:
    raise ValueError("Message too long")

# Basic spam word filter
SPAM_WORDS = ["free money", "earn cash", "urgent offer", "100% guaranteed"]

def clean_message(text):
    lower = text.lower()
    for word in SPAM_WORDS:
        if word in lower:
            raise ValueError(f"Spam-like phrase detected: {word}")
    return text

MESSAGE_BODY = clean_message(MESSAGE_BODY)

# Load recipients
with open("recipients.txt") as f:
    recipients = [line.strip() for line in f if line.strip()]

if len(recipients) > MAX_EMAILS_PER_BATCH:
    raise ValueError("Too many recipients in one batch")

async def send_email(to_email):
    message = EmailMessage()
    message["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    message["To"] = to_email
    message["Subject"] = SUBJECT
    message.set_content(MESSAGE_BODY)

    await aiosmtplib.send(
        message,
        hostname=SMTP_SERVER,
        port=SMTP_PORT,
        start_tls=True,
        username=SENDER_EMAIL,
        password=APP_PASSWORD,
    )

async def main():
    sent = 0
    for email in recipients:
        try:
            await send_email(email)
            sent += 1
            print(f"Sent: {email}")
            await asyncio.sleep(DELAY_BETWEEN_EMAILS)
        except Exception as e:
            print(f"Failed: {email} - {e}")

    print(f"\nDone ✅ Total Sent: {sent}")

if __name__ == "__main__":
    asyncio.run(main())
