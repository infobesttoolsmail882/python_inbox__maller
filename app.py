from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Home Route (Important - warna Not Found aata hai)
@app.route("/")
def home():
    return "Inbox Mailer Running Successfully ✅"

# Send Mail Route
@app.route("/send", methods=["POST"])
def send_mail():
    try:
        data = request.json

        sender_email = os.environ.get("EMAIL")
        sender_password = os.environ.get("PASSWORD")

        receiver_email = data.get("to")
        subject = data.get("subject")
        body = data.get("message")

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return jsonify({"status": "Email Sent Successfully ✅"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
