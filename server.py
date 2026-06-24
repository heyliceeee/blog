import json
from flask import Flask, render_template
import random
import datetime
import requests

app = Flask(__name__)


@app.route('/')
def home():
    random_number = random.randint(1, 10) # Generate a random number between 1 and 10
    current_year = datetime.datetime.now().year # Get the current year

    return render_template("index.html", num=random_number, year=current_year) # Pass the random number and current year to the template

@app.route('/guess/<name>')
def guess(name):
    genderize_url = f'https://api.genderize.io/?name={name}'
    genderize_response = requests.get(genderize_url) # Make a GET request to the genderize API
    gender_data = genderize_response.json() # Parse the JSON response
    gender = gender_data['gender'] # Get the gender from the response

    age_url = f'https://api.agify.io/?name={name}'
    age_response = requests.get(age_url) # Make a GET request to the agify API
    age_data = age_response.json() # Parse the JSON response
    age = age_data['age'] # Get the age from the response

    return render_template("guess.html", person_name=name, person_gender=gender, person_age=age) # Pass the person data to the template

@app.route('/blog')
def blog():
    with open('blog-data.txt', 'r') as file: # Open the blog data file
        all_posts = json.load(file) # Load the JSON data into a Python dictionary

    return render_template('blog.html', posts=all_posts) # Pass the blog posts to the template

if __name__ == "__main__":
    app.run(debug=True)


