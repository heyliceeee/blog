import json
import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for
from email.message import EmailMessage
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp
from flask_login import login_user, LoginManager, UserMixin, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

smtp_host = os.getenv("SMTP_HOST")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_pass = os.getenv("SMTP_PASSWORD")
smtp_email = os.getenv("SMTP_EMAIL")

db = SQLAlchemy() # Create an instance of the SQLAlchemy class

with open('blog-data.txt', 'r') as file:  # Open the blog data file
    all_posts = json.load(file)  # Load the JSON data into a Python dictionary

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Regexp(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$", message="The password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")])
    submit = SubmitField("Login")
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # Primary key column
    email = db.Column(db.String(100), unique=True) # Unique email column
    password = db.Column(db.String(200)) # Password column

app = Flask(__name__)
app.config["SECRET_KEY"] = "uma_chave_segura_qualquer" # Set the secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db" # Set the database URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Disable tracking modifications

db.init_app(app) # Initialize the SQLAlchemy instance with the Flask application

login_manager = LoginManager() # Create an instance of the LoginManager class
login_manager.init_app(app) # Initialize the LoginManager with the Flask application
login_manager.login_view = "login_page"
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "warning"

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # Load the user from the database based on the user_id
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if current_user.is_authenticated: # Check if the user is already logged in
        return redirect(url_for("posts_crud")) # Redirect to the dashboard

    if form.validate_on_submit(): # Check if the form is submitted
        user = User.query.filter_by(email=form.email.data).first() # Get the user from the database

        if not user: # Check if the user exists
            form.email.errors.append("Email not found.") # Add an error message
            return render_template("login.html", form=form) # Render the login page with the form

        if not check_password_hash(user.password, form.password.data): # Check if the password is correct
            form.password.errors.append("Incorrect password.") # Add an error message
            return render_template("login.html", form=form) # Render the login page with the form

        login_user(user) # Log in the user
        return redirect(url_for('posts_crud')) # Redirect to the dashboard

    return render_template('login.html', form=form) # Render the login page

@app.route("/logout")
@login_required
def logout():
    logout_user() # Log out the user
    return redirect(url_for("login_page")) # Redirect to the login page

@app.route("/blog-data.txt")
@login_required
def block_json():
    return "Access denied", 403

@app.route("/posts")
@login_required
def posts_crud():
    return render_template("posts.html", all_posts=all_posts) # Render the posts.html template
@app.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        new_post = {
            "id": len(all_posts) + 1,
            "title": request.form["title"],
            "subtitle": request.form["subtitle"],
            "image": request.form["image"],
            "body": request.form["body"],
            "published": request.form["published"],
            "reading_time": request.form["reading_time"] + "min read",
            "comments_count": 0,
            "comments": [
                {"author": "", "text": "", "date": ""}
            ]
        } # Create a new post

        all_posts.append(new_post) # Add the new post to the dictionary

        with open("blog-data.txt", "w") as file: # Open the blog data file in write mode
            json.dump(all_posts, file, indent=4) # Dump the dictionary to the file

        return redirect(url_for("posts_crud")) # Redirect to the dashboard
    return render_template("create_post.html") # Render the create_post.html template
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = next((p for p in all_posts if p["id"] == post_id), None) # Find the post with the given id

    if not post: # Check if the post exists
        return "Post not found", 404 # Return a 404 error if the post doesn't exist'

    if request.method == "POST": # Check if the request method is POST
        post["title"] = request.form["title"]
        post["subtitle"] = request.form["subtitle"]
        post["image"] = request.form["image"]
        post["body"] = request.form["body"]
        post["published"] = request.form["published"]
        post["reading_time"] = request.form["reading_time"]

        with open("blog-data.txt", "w") as file:
            json.dump(all_posts, file, indent=4)

        return redirect(url_for("posts_crud"))
    return render_template("edit_post.html", post=post)
@app.route("/delete-post/<int:post_id>")
@login_required
def delete_post(post_id):
    global all_posts
    all_posts = [p for p in all_posts if p["id"] != post_id] # Remove the post with the given id from the dictionary

    with open("blog-data.txt", "w") as file:
        json.dump(all_posts, file, indent=4)

    return redirect(url_for("posts_crud"))


with app.app_context(): # Create a context for the database
    db.create_all() # Create the database tables
    if not User.query.filter_by(email="alice@example.com").first(): # Check if the user doesn't exist in the database'
        hashed = generate_password_hash("Alic3StrongPass123") # Hash the password
        user = User(email="alice@example.com", password=hashed) # Create a new user instance
        db.session.add(user) # Add the user to the database
        db.session.commit() # Commit the changes to the database

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)