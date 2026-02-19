from flask import Flask, jsonify
import os
from mailer import send_bulk_mail

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Python Inbox Mailer Running"

@app.route("/send")
def send_mail():
    result = send_bulk_mail()
    return jsonify({"status": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
