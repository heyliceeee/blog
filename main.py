import json
import os
import smtplib
from flask import Flask, render_template, request
from email.message import EmailMessage

smtp_host = os.getenv("SMTP_HOST")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_pass = os.getenv("SMTP_PASSWORD")
smtp_email = os.getenv("SMTP_EMAIL")

with open('blog-data.txt', 'r') as file:  # Open the blog data file
    all_posts = json.load(file)  # Load the JSON data into a Python dictionary

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=all_posts) # Pass the dictionary to the template

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None # Initialize the variable
    for blog_post in all_posts: # Iterate through the dictionary
        if blog_post["id"] == index: # Check if the index matches the id of the blog post
            requested_post = blog_post # If it does, assign the blog post to the variable
    return render_template("blog-post.html", post=requested_post)

@app.route('/about')
def about():
    return render_template("about.html") # Render the about.html template

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST': # Check if the request method is POST
        data = request.form # Get the form data
        send_email(data['name'], data['email'], data['message']) # Call the send_email function
        return render_template("contact.html", msg_sent=True) # Render the contact.html template with a success message
    return render_template("contact.html", msg_sent=False) # Render the contact.html template without a success message

def send_email(name, email, message):
    """
    Send an email using the SMTP protocol
    :param name: name of the sender
    :param email: email of the sender
    :param message: message of the sender
    """
    msg = EmailMessage()
    msg["Subject"] = "New Message From Your Blog"
    msg["From"] = smtp_email
    msg["To"] = smtp_email
    letter = f"Name: {name}\nEmail: {email}\n\nMessage: {message}"
    msg.set_content(letter, charset="utf-8")

    with smtplib.SMTP(smtp_host, smtp_port) as conn:  # Create an SMTP connection
        conn.starttls()  # Enable TLS encryption
        conn.login(user=smtp_email, password=smtp_pass)  # Log in to the SMTP server
        conn.send_message(msg)  # Send the email

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)