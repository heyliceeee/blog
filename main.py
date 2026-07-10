import json
import os
import smtplib
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, abort
from email.message import EmailMessage
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Regexp, EqualTo, Length
from flask_login import login_user, LoginManager, UserMixin, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

smtp_host = os.getenv("SMTP_HOST")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_pass = os.getenv("SMTP_PASSWORD")
smtp_email = os.getenv("SMTP_EMAIL")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") # Set the secret key
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") # Set the database URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Disable tracking modifications
Bootstrap5(app) # Initialize Bootstrap5

ckeditor = CKEditor(app) # Initialize CKEditor

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
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
    comments: Mapped[str] = mapped_column(Text, nullable=False) # Comments column
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key column
    text = db.Column(db.Text, nullable=False) # Text column
    author_id = db.Column(db.Integer, db.ForeignKey("user.id")) # Foreign key column
    post_id = db.Column(db.Integer, db.ForeignKey("blog_post.id")) # Foreign key column
    date = db.Column(db.String(50)) # Date column
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Regexp(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$", message="The password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create Account")
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Regexp(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$", message="The password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")])
    submit = SubmitField("Login")
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # Primary key column
    role = db.Column(db.String(20), nullable=False, default="user") # Role column
    username = db.Column(db.String(100), unique=True, nullable=False) # Unique username column
    email = db.Column(db.String(100), unique=True, nullable=False) # Unique email column
    password = db.Column(db.String(200), nullable=False) # Password column
class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()]) # Title field
    subtitle = StringField("Subtitle", validators=[DataRequired()]) # Subtitle field
    image = StringField("Image URL", validators=[DataRequired(), URL()]) # Image URL field
    body = CKEditorField("Content", validators=[DataRequired()]) # Content field
    submit = SubmitField("Publish") # Submit button
class EditPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    image = StringField("Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Content", validators=[DataRequired()])
    published = StringField("Published Date", validators=[DataRequired()])
    submit = SubmitField("Update")
class EditAboutForm(FlaskForm):
    intro = CKEditorField("Intro", validators=[DataRequired()])
    experience = CKEditorField("Experience", validators=[DataRequired()])
    education = CKEditorField("Education", validators=[DataRequired()])
    portfolio = CKEditorField("Portfolio", validators=[DataRequired()])
    newsletter_title = StringField("Newsletter Title", validators=[DataRequired()])
    newsletter_text = CKEditorField("Newsletter Text", validators=[DataRequired()])
    submit = SubmitField("Save Changes")
class EditContactForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    name_label = StringField("Name Label", validators=[DataRequired()])
    name_placeholder = StringField("Name Placeholder", validators=[DataRequired()])
    email_label = StringField("Email Label", validators=[DataRequired()])
    email_placeholder = StringField("Email Placeholder", validators=[DataRequired()])
    message_label = StringField("Message Label", validators=[DataRequired()])
    message_placeholder = StringField("Message Placeholder", validators=[DataRequired()])
    button_text = StringField("Button Text", validators=[DataRequired()])
    footer_text = StringField("Footer Text", validators=[DataRequired()])
    footer_link_text = StringField("Footer Link Text", validators=[DataRequired()])
    footer_link_url = StringField("Footer Link URL", validators=[DataRequired()])
    submit = SubmitField("Save Changes")
class CommentForm(FlaskForm):
    comment = StringField("Comment", validators=[DataRequired()])

with app.app_context(): # Create a context for the database
    db.create_all() # Create the database tables

login_manager = LoginManager() # Create an instance of the LoginManager class
login_manager.init_app(app) # Initialize the LoginManager with the Flask application
login_manager.login_view = "login_page"
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "warning"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs): # Decorate the function with the admin_required decorator
        if not current_user.is_authenticated or current_user.role != "admin": # Check if the user is authenticated and if the user is not an admin
            return abort(403) # Return a 403 Forbidden error
        return f(*args, **kwargs) # Call the decorated function
    return decorated_function # Return the decorated function

def extract_block_content(html):
    start = html.find("{% block content %}") + len("{% block content %}") # Find the start of the block content
    end = html.find("{% endblock %}", start) # Find the end of the block content
    return html[start:end].strip() # Return the block content
def replace_block_content(original_html, new_content):
    start = original_html.find("{% block content %}") + len("{% block content %}") # Find the start of the block content
    end = original_html.find("{% endblock %}", start) # Find the end of the block content
    return original_html[:start] + "\n" + new_content + "\n" + original_html[end:] # Return the original HTML with the new content inserted

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
    comments_list = db.session.query(Comment, User).join(User, Comment.author_id == User.id).filter(Comment.post_id == index).all() # Get all comments for the post

    form = CommentForm()

    return render_template("blog_post.html", post=requested_post, comments=comments_list, form=form) # Render the blog_post.html template with the post data

@app.route('/about')
def about():
    about_path = os.path.join(app.root_path, "instance", "about.json")
    with open(about_path, "r", encoding="utf-8") as f:
        about_data = json.load(f)
    return render_template("about.html", about=about_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_path = os.path.join(app.root_path, "instance", "contact.json")

    with open(contact_path, "r", encoding="utf-8") as f:
        contact_data = json.load(f)

    if request.method == 'POST':
        data = request.form
        send_email(data['name'], data['email'], data['message'])
        return render_template("contact.html", contact=contact_data, msg_sent=True)

    return render_template("contact.html", contact=contact_data, msg_sent=False)

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
        return redirect(url_for("get_all_posts")) # Redirect to the dashboard

    if form.validate_on_submit(): # Check if the form is submitted
        user = User.query.filter_by(username=form.username.data).first() # Get the user with the given username

        if not user: # Check if the user exists
            form.username.errors.append("Username not found.") # Add an error message
            return render_template("login.html", form=form) # Render the login page with the form

        if not check_password_hash(user.password, form.password.data): # Check if the password is correct
            form.password.errors.append("Incorrect password.") # Add an error message
            return render_template("login.html", form=form) # Render the login page with the form

        login_user(user) # Log in the user
        return redirect(url_for("get_all_posts")) # Redirect to the dashboard
    return render_template('login.html', form=form) # Render the login page

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if current_user.is_authenticated: # Check if the user is already logged in
        return redirect(url_for("get_all_posts")) # Redirect to the dashboard

    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            role="user",
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()

        logout_user() # Log out the user

        return redirect(url_for("login_page"))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user() # Log out the user
    return redirect(url_for("login_page")) # Redirect to the login page

@app.route("/posts")
@login_required
@admin_required
def posts_crud():
    " posts list "
    posts = BlogPost.query.all() # Get all posts from the database
    return render_template("posts.html", all_posts=posts) # Render the posts.html template

@app.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_required
def new_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            image=form.image.data,
            body=form.body.data,
            published=date.today().strftime("%B %d, %Y"),
            reading_time=f"{max(1, len(form.body.data.split()) // 150)} min read",
            comments_count=0,
            comments=json.dumps([])
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("get_all_posts"))
    return render_template("make_post.html", form=form)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_post(post_id):
    " Edit a post "
    post = BlogPost.query.get_or_404(post_id) # Get the post with the given id or return a 404 error
    form = EditPostForm(obj=post) # Create an EditPostForm instance with the post object

    if form.validate_on_submit(): # Check if the form is submitted
        post.title = form.title.data # Update the post title
        post.subtitle = form.subtitle.data # Update the post subtitle
        post.image = form.image.data # Update the post image
        post.body = form.body.data # Update the post body
        post.published = form.published.data # Update the post published date
        post.reading_time = f"{max(1, len(form.body.data.split()) // 200)} min read" # Update the post reading time

        db.session.commit() # Commit the changes to the database
        return redirect(url_for("get_all_posts")) # Redirect to the dashboard
    return render_template("edit_post.html", form=form, post=post) # Render the edit_post.html template with the form and post data

@app.route("/delete-post/<int:post_id>", methods=["POST"])
@login_required
@admin_required
def delete_post(post_id):
    " Delete a post "
    post = BlogPost.query.get_or_404(post_id) # Get the post with the given id or return a 404 error

    db.session.delete(post) # Delete the post from the database
    db.session.commit() # Commit the changes to the database

    return redirect(url_for("get_all_posts")) # Redirect to the dashboard

@app.route("/post/<int:post_id>/comment", methods=["POST"])
@login_required
def add_comment(post_id):
    text = request.form.get("comment") # Get the comment text from the form

    if not text: # Check if the comment text is empty
        return redirect(url_for("show_post", index=post_id)) # Redirect to the post page if the comment text is empty

    new_comment = Comment(
        text=text,
        author_id=current_user.id,
        post_id=post_id,
        date=date.today().strftime("%B %d, %Y")
    ) # Create a new Comment instance

    db.session.add(new_comment) # Add the new Comment instance to the database
    db.session.commit() # Commit the changes to the database

    post = BlogPost.query.get(post_id) # Get the post with the given id
    post.comments_count = Comment.query.filter_by(post_id=post_id).count() # Update the comments_count field in the post
    db.session.commit() # Commit the changes to the database

    return redirect(url_for("show_post", index=post_id)) # Redirect to the post page

@app.route("/comment/<int:comment_id>/edit", methods=["POST"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id) # Get the comment with the given id or return a 404 error

    if comment.author_id != current_user.id: # Check if the current user is the author of the comment
        return abort(403) # Return a 403 Forbidden error

    new_text = request.form.get("comment") # Get the new comment text from the form
    comment.text = new_text # Update the comment text
    db.session.commit() # Commit the changes to the database

    return redirect(url_for("show_post", index=comment.post_id)) # Redirect to the post page

@app.route("/comment/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id) # Get the comment with the given id or return a 404 error

    if current_user.role == "admin": # Check if the current user is an admin
        db.session.delete(comment) # Delete the comment from the database
        db.session.commit() # Commit the changes to the database
        return redirect(url_for("show_post", index=comment.post_id)) # Redirect to the post page

    if comment.author_id != current_user.id: # Check if the current user is the author of the comment
        return abort(403) # Return a 403 Forbidden error

    db.session.delete(comment) # Delete the comment from the database
    db.session.commit() # Commit the changes to the database

    post = BlogPost.query.get(comment.post_id) # Get the post with the given id
    post.comments_count = Comment.query.filter_by(post_id=comment.post_id).count() # Update the comments_count field in the post
    db.session.commit() # Commit the changes to the database

    return redirect(url_for("show_post", index=comment.post_id)) # Redirect to the post page

@app.route("/edit-about", methods=["GET", "POST"])
@login_required
@admin_required
def edit_about():
    about_path = os.path.join(app.root_path, "instance", "about.json")

    with open(about_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    form = EditAboutForm(data=data)

    if form.validate_on_submit():
        updated = {
            "intro": form.intro.data,
            "experience": form.experience.data,
            "education": form.education.data,
            "portfolio": form.portfolio.data,
            "newsletter_title": form.newsletter_title.data,
            "newsletter_text": form.newsletter_text.data
        }

        with open(about_path, "w", encoding="utf-8") as f:
            json.dump(updated, f, indent=4)

        return redirect(url_for("about"))
    return render_template("edit_about.html", form=form)

@app.route("/edit-contact", methods=["GET", "POST"])
@login_required
@admin_required
def edit_contact():
    contact_path = os.path.join(app.root_path, "instance", "contact.json")

    with open(contact_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    form = EditContactForm(data=data)

    if form.validate_on_submit():
        updated = {
            "title": form.title.data,
            "description": form.description.data,
            "name_label": form.name_label.data,
            "name_placeholder": form.name_placeholder.data,
            "email_label": form.email_label.data,
            "email_placeholder": form.email_placeholder.data,
            "message_label": form.message_label.data,
            "message_placeholder": form.message_placeholder.data,
            "button_text": form.button_text.data
        }

        with open(contact_path, "w", encoding="utf-8") as f:
            json.dump(updated, f, indent=4)

        return redirect(url_for("contact"))
    return render_template("edit_contact.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)