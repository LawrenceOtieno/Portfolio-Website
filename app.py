from flask import Flask, render_template, request

app = Flask(__name__, static_url_path="/static")

projects = [
    {
        "name": "Optical character Recognitio",
        "image": "images/churn.png",
        "tags": ["Python", "Decision Tree", "xgboost"],
    },
    {
        "name": "Twitter Bot for Product Monitoring",
        "image": "images/twitter.png",
        "tags": ["Python", "Keras", "Tweepy"],
    },
    {
        "name": "Opinion vs. Claim Classifier: Enhancing Content Moderation at TikTok",
        "image": "images/tiktok2.PNG",
        "tags": ["Python", "sklearn", "RandomForestClassifier"],
    },
    {
        "name": "Plant Disease Detection- Mahindy Project",
        "image": "images/plant.PNG",
        "tags": ["Python", "Keras", "CNN", "RCNN"],
    },
    {
        "name": "Statistical Review and A/B Testing for New York City TLC Project",
        "image": "images/AB_Test.png",
        "tags": ["Python", "SKLearn", "BigQuery"],
    },
    {
        "name": "Customer Churn Turnover- ML",
        "image": "images/churn_rate.png",
        "tags": ["Python", "Keras"],
    },
    {
        "name": "Blog on using PACE as an analytical framework",
        "image": "images/pace.png",
        "tags": ["WordPress"],
    },
    {
        "name": "COVID-19 fatalities and risk of conflicts - Youth Bulge",
        "image": "images/COVID-19_youth.jpg",
        "tags": ["Excel", "R", "Research"],
    },
    {
        "name": "Human Resource Management (HRM)- Executive Dashboard",
        "image": "images/HRM.png",
        "tags": [
            "Tableau",
        ],
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

        # Validate form data (you can add more validation as needed)

        # Handle the form data (you can replace this with your preferred method)
        # For simplicity, we'll just print the data to the console
        print(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")

        # You can add additional logic here, such as sending an email or saving to a database

    return render_template(
        "index.html", projects=projects
    )  # Assuming your HTML file is named 'index.html'


if __name__ == "__main__":
    app.run(debug=True)
