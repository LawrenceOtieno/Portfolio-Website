from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__, static_url_path="/static")

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'lawrenceit38@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'ejttzqpykbwxnauf'  # Your email password or app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'lawrenceit38@gmail.com'  # Default sender email address

mail = Mail(app)

projects = [
    {
        "name": "Movies Rating Dashboard",
        "image": "images/movies_rating_dashboard.png",
        "tags": ["Python", "HTML", "Streamlit"],
        "link": "https://github.com/LawrenceOtieno/MovieRatingsDashboard",  # <-- Add actual GitHub link here
    },
    {
        "name": "Twitter Bot for Product Monitoring",
        "image": "images/twitter.png",
        "tags": ["Python", "Keras", "Tweepy"],
        "link": "https://github.com/yourusername/twitter-bot",  # <-- Add actual GitHub link here
    },
    {
        "name": "Opinion vs. Claim Classifier: Enhancing Content Moderation at TikTok",
        "image": "images/tiktok2.PNG",
        "tags": ["Python", "sklearn", "RandomForestClassifier"],
        "link": "https://github.com/yourusername/tiktok-classifier",  # <-- Add actual GitHub link here
    },
    {
        "name": "Plant Disease Detection- Mahindy Project",
        "image": "images/plant.PNG",
        "tags": ["Python", "Keras", "CNN", "RCNN"],
        "link": "#",  # Placeholder link until you add it
    },
    {
        "name": "Statistical Review and A/B Testing for New York City TLC Project",
        "image": "images/AB_Test.png",
        "tags": ["Python", "SKLearn", "BigQuery"],
        "link": "#",
    },
    {
        "name": "Customer Churn Turnover- ML",
        "image": "images/churn_rate.png",
        "tags": ["Python", "Keras"],
        "link": "#",
    },
    {
        "name": "Blog on using PACE as an analytical framework",
        "image": "images/pace.png",
        "tags": ["WordPress"],
        "link": "#",
    },
    {
        "name": "COVID-19 fatalities and risk of conflicts - Youth Bulge",
        "image": "images/COVID-19_youth.jpg",
        "tags": ["Excel", "R", "Research"],
        "link": "#",
    },
    {
        "name": "Human Resource Management (HRM)- Executive Dashboard",
        "image": "images/HRM.png",
        "tags": ["Tableau"],
        "link": "#",
    },
]

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        # Validate form data
        if not name or not email or not phone or not message:
            return "Please fill all fields", 400

        # Create the email message
        msg = Message(
            subject="New Contact Form Submission",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=['lawrenceit38@gmail.com'],
            body=f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        )

        # Send the email
        mail.send(msg)

    return render_template("index.html", projects=projects)

if __name__ == "__main__":
    app.run(debug=True)