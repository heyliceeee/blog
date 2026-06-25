import json
from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True)


