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
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

load_dotenv()

smtp_host = os.getenv("SMTP_HOST")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_pass = os.getenv("SMTP_PASSWORD")
smtp_email = os.getenv("SMTP_EMAIL")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") # Set the secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db" # Set the database URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Disable tracking modifications
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db' # Set the database URI
db = SQLAlchemy(model_class=Base) # Create an instance of the SQLAlchemy class
db.init_app(app) # Initialize the SQLAlchemy instance with the Flask application

# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True) # Primary key column
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False) # Unique title column
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False) # Subtitle column
    image: Mapped[str] = mapped_column(String(250), nullable=False) # Image column
    published: Mapped[str] = mapped_column(String(250), nullable=False) # Date column
    body: Mapped[str] = mapped_column(Text, nullable=False) # Body column
    reading_time: Mapped[str] = mapped_column(String(250), nullable=False) # Reading time column
    comments_count: Mapped[int] = mapped_column(Integer, nullable=False) # Comments count column
    comments: Mapped[list] = mapped_column(Text, nullable=False) # Comments column
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Regexp(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$", message="The password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")])
    submit = SubmitField("Login")
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # Primary key column
    email = db.Column(db.String(100), unique=True) # Unique email column
    password = db.Column(db.String(200)) # Password column

with app.app_context(): # Create a context for the database
    db.create_all() # Create the database tables

    if BlogPost.query.count() == 0:
        sample_posts = [
            BlogPost(
                title="How I Built My First Flask App",
                subtitle="A beginner-friendly journey into backend development",
                image="https://images.unsplash.com/photo-1518770660436-463b3625b3ac",
                published="2026-06-12",
                body=(
                    "I started this project with zero experience in Flask. "
                    "What surprised me the most was how quickly everything clicked once I understood routing, "
                    "templates and SQLAlchemy. In this post, I walk through the exact steps I took, "
                    "the mistakes I made, and the moment everything finally worked."
                ),
                reading_time="6 min read",
                comments_count=0,
                comments=json.dumps([
    {
        "author": "Miguel Ferreira",
        "text": "Adorei a forma como explicaste o processo. Senti exatamente o mesmo quando comecei com Flask!",
        "date": "2026-07-04"
    },
    {
        "author": "Rita Marques",
        "text": "A parte dos erros silenciosos… tão real. Obrigada por partilhares a tua experiência.",
        "date": "2026-07-04"
    },
    {
        "author": "João Cardoso",
        "text": "Este post motivou-me a finalmente começar o meu próprio projeto. Obrigado Alice!",
        "date": "2026-07-05"
    }
]
)
            ),
            BlogPost(
                title="Why Backend Developers Should Learn Automation",
                subtitle="Small scripts, big impact",
                image="https://images.unsplash.com/photo-1555066931-4365d14bab8c",
                published="2026-06-20",
                body=(
                    "Automation is not just about saving time — it's about reducing cognitive load. "
                    "From cleaning datasets to sending scheduled emails, automation has transformed the way "
                    "I approach daily tasks. Here are the tools I rely on and the automations that made the biggest difference."
                ),
                reading_time="5 min read",
                comments_count=0,
                comments=json.dumps([
    {
        "author": "Carolina Lopes",
        "text": "Automação mudou completamente o meu workflow também. Scripts pequenos fazem milagres!",
        "date": "2026-07-06"
    },
    {
        "author": "Pedro Nunes",
        "text": "Excelente explicação. Gostava de ver um post só sobre automação com Python.",
        "date": "2026-07-06"
    },
    {
        "author": "Sofia Almeida",
        "text": "Concordo totalmente — reduzir carga mental é tão importante quanto poupar tempo.",
        "date": "2026-07-07"
    }
]
)
            ),
            BlogPost(
                title="The Day I Finally Understood SQLAlchemy",
                subtitle="ORMs don’t have to be scary",
                image="https://images.unsplash.com/photo-1526378722484-cc6c0c9a4f87",
                published="2026-07-01",
                body=(
                    "SQLAlchemy felt overwhelming at first — models, sessions, queries, relationships… "
                    "But once I grasped how the ORM maps Python classes to database tables, everything changed. "
                    "In this post, I break down the concepts in a simple way and share the cheatsheet I wish I had earlier."
                ),
                reading_time="7 min read",
                comments_count=0,
                comments=json.dumps([
    {
        "author": "Tiago Santos",
        "text": "SQLAlchemy parecia magia negra até ler isto. Obrigado por simplificares tudo!",
        "date": "2026-07-08"
    },
    {
        "author": "Beatriz Correia",
        "text": "A tua explicação sobre ORM vs SQL direto foi a melhor que já vi.",
        "date": "2026-07-08"
    },
    {
        "author": "Hugo Martins",
        "text": "Finalmente percebi sessions e commits. Este post salvou-me horas de frustração.",
        "date": "2026-07-09"
    }
]
)
            ),
        ]

        db.session.add_all(sample_posts)
        db.session.commit()

login_manager = LoginManager() # Create an instance of the LoginManager class
login_manager.init_app(app) # Initialize the LoginManager with the Flask application
login_manager.login_view = "login_page"
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "warning"

@app.route('/')
def get_all_posts():
    " Get all posts from the database "
    result = db.session.execute(db.select(BlogPost)) # Execute the SQL query
    posts = result.scalars().all() # Get the results as a list of dictionaries
    return render_template("index.html", all_posts=posts) # Pass the dictionary to the template

@app.route("/post/<int:index>")
def show_post(index):
    " Show a single post from the database "
    requested_post = db.get_or_404(BlogPost, index) # Get the post with the given id or return a 404 error
    comments_list = json.loads(requested_post.comments) # Convert the comments string to a list of dictionaries

    return render_template("blog-post.html", post=requested_post, comments=comments_list) # Render the blog-post.html template with the post data

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
    return db.session.get(User, int(user_id)) # Get the user with the given id from the database
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

@app.route("/posts")
@login_required
def posts_crud():
    " posts list "
    posts = BlogPost.query.all() # Get all posts from the database
    return render_template("posts.html", all_posts=posts) # Render the posts.html template
@app.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    " Create a new post "
    if request.method == "POST": # Check if the request method is POST
        new_post = BlogPost(
            title=request.form["title"],
            subtitle=request.form["subtitle"],
            image=request.form["image"],
            body=request.form["body"],
            published=request.form["published"],
            reading_time=request.form["reading_time"] + "min read",
            comments_count=0,
            comments=json.dumps([{"author": "", "text": "", "date": ""}])
        ) # Create a new post instance with the form data

        db.session.add(new_post) # Add the new post to the database
        db.session.commit() # Commit the changes to the database

        return redirect(url_for("posts_crud")) # Redirect to the dashboard
    return render_template("create_post.html") # Render the create_post.html template

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    " Edit a post "
    post = BlogPost.query.get_or_404(post_id) # Get the post with the given id or return a 404 error

    if request.method == "POST": # Check if the request method is POST
        post.title = request.form["title"] # Update the post title with the form data
        post.subtitle = request.form["subtitle"] # Update the post subtitle with the form data
        post.image = request.form["image"] # Update the post image with the form data
        post.body = request.form["body"] # Update the post body with the form data
        post.published = request.form["published"] # Update the post published date with the form data
        post.reading_time = request.form["reading_time"] # Update the post reading time with the form data

        db.session.commit() # Commit the changes to the database
        return redirect(url_for("posts_crud")) # Redirect to the dashboard
    return render_template("edit_post.html", post=post) # Render the edit_post.html template with the post data

@app.route("/delete-post/<int:post_id>")
@login_required
def delete_post(post_id):
    " Delete a post "
    post = BlogPost.query.get_or_404(post_id) # Get the post with the given id or return a 404 error

    db.session.delete(post) # Delete the post from the database
    db.session.commit() # Commit the changes to the database

    return redirect(url_for("posts_crud")) # Redirect to the dashboard


with app.app_context(): # Create a context for the database
    db.create_all() # Create the database tables
    if not User.query.filter_by(email="alice@example.com").first(): # Check if the user doesn't exist in the database'
        hashed = generate_password_hash("Alic3StrongPass123") # Hash the password
        user = User(email="alice@example.com", password=hashed) # Create a new user instance
        db.session.add(user) # Add the user to the database
        db.session.commit() # Commit the changes to the database

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)