import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── Email configuration ──────────────────────────────────────────────────────
MAIL_USER = os.environ.get("MAIL_USER", "lawrenceit38@gmail.com")
MAIL_PASS = os.environ.get("MAIL_PASS", "gudinyaidebzxmvl")
MAIL_TO   = "lawrenceit38@gmail.com"

# Updated projects list
projects = [
    {"name": "Movies Rating Dashboard", "image": "images/moviesr.png", "tags": ["Python", "HTML", "Streamlit"], "link": "https://github.com/LawrenceOtieno/MovieRatingsDashboard"},
    {"name": "Gazebo Indoor Environment Generator for PX4 Autopilot", "image": "images/gazebo.png", "tags": ["Python", "Shell", "PX4 Autopilot","Gazebo Simulator"], "link": "https://github.com/LawrenceOtieno/gazebo-indoor-gen"},
    {"name": "KRA Nil Automator", "image": "images/automator.png", "tags": ["Python", "HTML", "Playwright", "Waitress"], "link": "https://github.com/LawrenceOtieno/kra-nil-automator"},
    {"name": "HRM Executive Dashboard", "image": "images/dashboard.png", "tags": ["Python", "Pandas", "Numpy", "Plotly", "Streamlit"], "link": "https://github.com/LawrenceOtieno/hrm-executive-dashboard"},
    {"name": "Statistical Review and A/B Testing for New York City TLC Project", "image": "images/AB_Test.png", "tags": ["Python", "SKLearn", "BigQuery"], "link": "#"},
    {"name": "Customer Churn Turnover- ML", "image": "images/churn_rate.png", "tags": ["Python", "Keras"], "link": "#"},
    {"name": "Blog on using PACE as an analytical framework", "image": "images/pace.png", "tags": ["WordPress"], "link": "#"},
    {"name": "COVID-19 fatalities and risk of conflicts - Youth Bulge", "image": "images/COVID-19_youth.jpg", "tags": ["Excel", "R", "Research"], "link": "#"},
    {"name": "Human Resource Management (HRM)- Executive Dashboard", "image": "images/HRM.png", "tags": ["Tableau"], "link": "#"},
]

# Testimonials — named entries use a dark-skin-tone person emoji matched to
# gender for the avatar; anonymized entries render an "incognito" icon instead.
testimonials = [
    {
        "name": "Lynn Ajema",
        "role": "Data Analyst",
        "company": "Aesops ke",
        "quote": "An exceptional analytical thinker who bridges the gap perfectly between technical system requirements and business processes. From managing complex workflows to optimizing SAP modules, their documentation and reporting are top-tier.",
        "rating": 5,
        "emoji": "\U0001F469\U0001F3FF",
        "anonymous": False,
    },
    {
        "name": "John Kamau",
        "role": "Data Team Lead",
        "company": "L-IFT",
        "quote": "Was incredibly reliable in handling critical system support and optimizing our daily data flows. Their dedication to maintaining flawless ICT infrastructure ensured our operations always ran smoothly.",
        "rating": 5,
        "emoji": "\U0001F468\U0001F3FF",
        "anonymous": False,
    },
    {
        "name": "Purity Cherono",
        "role": "Communications Specialist",
        "company": "Lilt AI",
        "quote": "Demonstrated outstanding technical precision while documenting complex guidelines for our indigenous language AI models. A highly collaborative engineer who excelled at translating nuanced local variations into structured technical logic.",
        "rating": 5,
        "emoji": "\U0001F469\U0001F3FF",
        "anonymous": False,
    },
    {
        "name": "Kelly Otieno",
        "role": "Peer / Technical Collaborator",
        "company": "",
        "quote": "A master at structuring backend workflows and building highly organized engineering documentation in Jira and Confluence. Their systematic approach to mapping end-to-end operational processes brought absolute clarity to cross-functional teams.",
        "rating": 4.5,
        "emoji": "\U0001F468\U0001F3FF",
        "anonymous": False,
    },
    {
        "name": "Anonymous",
        "role": "Senior Business Analyst",
        "company": "Private",
        "quote": "A brilliant strategist with a sharp eye for workflow bottlenecks. They excelled at gathering stakeholders' chaotic requirements and transforming them into beautifully structured, actionable technical solutions.",
        "rating": 5,
        "emoji": "",
        "anonymous": True,
    },
    {
        "name": "Anonymous",
        "role": "DevOps & Automation Engineer",
        "company": "Private",
        "quote": "Transformed our slow, manual data entries into automated, highly efficient pipelines. They possessed a deep understanding of software integrations, significantly cutting down our daily operational friction.",
        "rating": 4.5,
        "emoji": "",
        "anonymous": True,
    },
    {
        "name": "Anonymous",
        "role": "Product Manager",
        "company": "Private",
        "quote": "The perfect cross-functional collaborator for systems optimization. Their unique blend of analytical data parsing and automated process mapping completely revitalized our operational efficiency models.",
        "rating": 3.5,
        "emoji": "",
        "anonymous": True,
    },
]


def send_email(name: str, email: str, phone: str, message: str) -> None:
    """Send a contact-form notification to MAIL_TO via Gmail SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"]  = f"Portfolio Contact: {name}"
    msg["From"]     = MAIL_USER
    msg["To"]       = MAIL_TO
    msg["Reply-To"] = email

    html_body = f"""
    <html><body style="font-family:Arial,sans-serif;color:#06283D;">
      <h2 style="color:#F5820D;">New message from your portfolio</h2>
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
    return render_template("index.html", projects=projects, testimonials=testimonials)


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
        app.logger.warning("MAIL_PASS not set.")
        return jsonify({"ok": False, "error": "Server mail not configured."}), 500

    try:
        send_email(name, email, phone, message)
        return jsonify({"ok": True, "message": "Message sent!"})
    except Exception as exc:
        app.logger.exception("Failed to send email: %s", exc)
        return jsonify({"ok": False, "error": "Failed to send email."}), 500


if __name__ == "__main__":
    app.run(debug=False)
