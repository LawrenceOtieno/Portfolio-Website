import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── Email configuration ──────────────────────────────────────────────────────
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
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

# Case studies — each has an interactive HTML "view" page (view_url, rendered by
# Flask so it can use url_for for its own asset links) and a static PDF download.
case_studies = [
    {
        "title": "Turning Messy HR Data Into a Simple, Useful Dashboard",
        "summary": "Cleaned conflicting HR records for 500+ employees across 4 cities, then built an executive dashboard from scratch that shows leaders where staff are leaving and why.",
        "tags": ["Python", "Streamlit", "Plotly", "Pandas", "Data Cleaning"],
        "image": "images/dashboard.png",
        "view_url": "/case-study/hrm-dashboard",
        "pdf_file": "files/hrm_case_study.pdf",
    },
]

# FAQ — shown in the "Frequently Asked Questions" section on the homepage.
faqs = [
    {
        "question": "What is your primary technical stack?",
        "answer": "I specialise in Python (its libraries and frameworks), Excel, Power BI, SQL, and automation & integration tools.",
    },
    {
        "question": "Are you open to contract or full-time remote opportunities?",
        "answer": "Yes, I am fully equipped for full-time, remote, hybrid, and on-site roles, as well as project-based consultancies.",
    },
]

# Testimonials — named entries use a dark-skin-tone person emoji matched to
# gender for the avatar; anonymized entries render an "incognito" icon instead.
testimonials = [
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
        "name": "Newton Mbugua",
        "role": "Software Engineer",
        "company": "Aesops ke",
        "quote": "Working alongside as a Business Analyst at Aesops ke has been an absolute game-changer for our development workflow. Lawrence possess a rare ability to bridge the gap between complex business needs and technical execution.\nHis standout achievement was automating our requirements' gathering pipeline. This innovation completely transformed how we receive project scopes—making the entire business analysis process incredibly smooth, efficient, and crystal clear. Because of their expertise in business process optimization, our engineering team spends less time decoding requirements and more time building high-impact software. I highly recommend them to any team looking to optimize operations and drive technical efficiency.",
        "rating": 3.5,
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
        "name": "Norbert Oduor",
        "role": "Data Product Officer",
        "company": "ICEA Lion Group",
        "quote": "When we needed to chart a complex data and business solution, we brought Lawrence onboard as a freelancer, and it was one of the best decisions we made. In the insurance space, translating massive, legacy data into actionable business strategies is a huge hurdle. They stepped in and simplified the complex, mapping out a clear blueprint that bridged our data architecture with actual business value. Lawrence has a brilliant mind for optimization and a natural ability to make data-driven decision-making look easy. we are grateful!",
        "rating": 4.0,
        "emoji": "\U0001F468\U0001F3FF",
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
        "name": "Lynn Ajema",
        "role": "Data Analyst",
        "company": "Aesops ke",
        "quote": "An exceptional analytical thinker who bridges the gap perfectly between technical system requirements and business processes. From managing complex workflows to optimizing SAP modules, their documentation and reporting are top-tier.",
        "rating": 5,
        "emoji": "\U0001F469\U0001F3FF",
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
    return render_template(
        "index.html",
        projects=projects,
        testimonials=testimonials,
        case_studies=case_studies,
        faqs=faqs,
    )


@app.route("/case-study/hrm-dashboard", methods=["GET"])
def case_study_hrm():
    """Interactive, self-contained version of the HRM dashboard case study.
    Opened from the Case Studies section's 'View Case Study' button. The
    downloadable PDF version lives at /static/files/hrm_case_study.pdf and is
    linked directly from both this page and the homepage card."""
    return render_template("case_study_hrm.html")


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
