from flask import Flask, render_template, request, redirect, session, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "super_secret_key_2026"

# Fixed Login Credentials
LOGIN_ID = "2026"
LOGIN_PASS = "2026"


# ======================
# LOGIN PAGE
# ======================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == LOGIN_ID and password == LOGIN_PASS:
            session["logged_in"] = True
            return redirect("/launcher")
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ======================
# LAUNCHER PAGE
# ======================
@app.route("/launcher")
def launcher():
    if not session.get("logged_in"):
        return redirect("/")
    return render_template("launcher.html")


# ======================
# SEND MAIL API
# ======================
@app.route("/send", methods=["POST"])
def send_mail():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json

    sender_name = data.get("senderName")
    email = data.get("email")
    password = data.get("password")
    subject = data.get("subject")
    message_body = data.get("message")
    recipients = data.get("recipients")

    if not all([sender_name, email, password, subject, message_body, recipients]):
        return jsonify({"error": "All fields required"})

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)

        for recipient in recipients:
            msg = MIMEMultipart()
            msg["From"] = f"{sender_name} <{email}>"
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(message_body, "plain"))
            server.sendmail(email, recipient, msg.as_string())

        server.quit()
        return jsonify({"status": "Emails Sent Successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})


# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False)
