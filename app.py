from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Validate form data (you can add more validation as needed)

        # Handle the form data (you can replace this with your preferred method)
        # For simplicity, we'll just print the data to the console
        print(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")

        # You can add additional logic here, such as sending an email or saving to a database

    return render_template('index.html')  # Assuming your HTML file is named 'index.html'

if __name__ == '__main__':
    app.run(debug=True)
