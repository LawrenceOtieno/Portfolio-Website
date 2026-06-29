import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── Email configuration ──────────────────────────────────────────────────────
# Set these two environment variables on your server before running the app:
#
#   export MAIL_USER="lawrenceit38@gmail.com"
#   export MAIL_PASS="your_gmail_app_password"
#
# Generate an App Password at: https://myaccount.google.com/apppasswords
# (requires 2-Step Verification to be enabled on the Gmail account)
# ─────────────────────────────────────────────────────────────────────────────
MAIL_USER = os.environ.get("MAIL_USER", "lawrenceit38@gmail.com")
MAIL_PASS = os.environ.get("MAIL_PASS", "")          # App Password — never hard-code
MAIL_TO   = "lawrenceit38@gmail.com"

# Sample projects data — replace/extend as needed
projects = [
    {
        "name": "Data Pipeline Automation",
        "image": "images/project1.jpg",
        "link": "#",
        "tags": ["Python", "Airflow", "SQL"],
    },
    {
        "name": "Business Intelligence Dashboard",
        "image": "images/project2.jpg",
        "link": "#",
        "tags": ["Power BI", "Excel", "DAX"],
    },
    {
        "name": "IT Service Desk Analytics",
        "image": "images/project3.jpg",
        "link": "#",
        "tags": ["ServiceNow", "Python", "Tableau"],
    },
]


def send_email(name: str, email: str, phone: str, message: str) -> None:
    """Send a contact-form notification to MAIL_TO via Gmail SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Portfolio Contact: {name}"
    msg["From"]    = MAIL_USER
    msg["To"]      = MAIL_TO
    msg["Reply-To"] = email

    html_body = f"""
    <html><body style="font-family:Arial,sans-serif;color:#06283D;">
      <h2 style="color:#FFC107;">New message from your portfolio</h2>
      <table cellpadding="8" style="border-collapse:collapse;width:100%;max-width:600px;">
        <tr><td style="font-weight:bold;width:100px;">Name</td><td>{name}</td></tr>
        <tr style="background:#f4f8fb;"><td style="font-weight:bold;">Email</td><td><a href="mailto:{email}">{email}</a></td></tr>
        <tr><td style="font-weight:bold;">Phone</td><td>{phone}</td></tr>
        <tr style="background:#f4f8fb;"><td style="font-weight:bold;vertical-align:top;">Message</td>
            <td style="white-space:pre-wrap;">{message}</td></tr>
      </table>
      <p style="margin-top:20px;font-size:12px;color:#888;">Sent from lawrenceotieno.stredata.com</p>
    </body></html>
    """

    text_body = (
        f"New portfolio contact\n\n"
        f"Name:    {name}\n"
        f"Email:   {email}\n"
        f"Phone:   {phone}\n"
        f"Message:\n{message}\n"
    )

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(MAIL_USER, MAIL_PASS)
        server.sendmail(MAIL_USER, MAIL_TO, msg.as_string())


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", projects=projects)


@app.route("/contact", methods=["POST"])
def contact():
    """Handle contact-form submission and send an email notification."""
    data = request.get_json(silent=True) or request.form

    name    = (data.get("name")    or "").strip()
    email   = (data.get("email")   or "").strip()
    phone   = (data.get("phone")   or "").strip()
    message = (data.get("message") or "").strip()

    if not all([name, email, message]):
        return jsonify({"ok": False, "error": "Please fill in all required fields."}), 400

    if not MAIL_PASS:
        # Graceful fallback — log to console and tell the user
        app.logger.warning(
            "MAIL_PASS not set. Contact from %s <%s>: %s", name, email, message
        )
        return jsonify({"ok": False, "error": "Mail not configured on the server. Please email lawrenceit38@gmail.com directly."}), 500

    try:
        send_email(name, email, phone, message)
        return jsonify({"ok": True, "message": "Message sent! I'll be in touch within 24–48 hours."})
    except smtplib.SMTPAuthenticationError:
        app.logger.exception("SMTP auth failed")
        return jsonify({"ok": False, "error": "Server mail authentication failed. Please contact lawrenceit38@gmail.com directly."}), 500
    except Exception as exc:
        app.logger.exception("Failed to send email: %s", exc)
        return jsonify({"ok": False, "error": "Something went wrong. Please try again or email lawrenceit38@gmail.com."}), 500


if __name__ == "__main__":
    app.run(debug=False)