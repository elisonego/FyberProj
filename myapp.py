from flask import Flask, render_template, request
import requests
import os
import mysql.connector
import json
from datetime import datetime  # Add this line

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    title = request.form.get("movie_title")
    print(f"Searching for movie: {title}")
    data = search_movie(title)
    return render_template("result.html", data=data)

def search_movie(title):
    # Replace YOUR_API_KEY with your actual API key
    api_key = os.getenv("OMDB_API_KEY")
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Parse the release date
        release_date = None
        if 'Released' in data and data['Released']:
            release_date = datetime.strptime(data['Released'], "%d %b %Y").date()

        # Connect to the database
        cnx = mysql.connector.connect(
            host="dev-rds-instance.cq5fbtzsgyiw.us-east-1.rds.amazonaws.com",
            user="elisonego",
            password="adminADMIN123",
            database="applicationDB"
        )

        cursor = cnx.cursor()

        # Insert the data into the database
        sql = ("INSERT INTO movies_cache "
               "(title, year, rated, released, data) "
               "VALUES (%s, %s, %s, %s, %s)")

        cursor.execute(sql, (title, data.get('Year', None), data.get('Rated', None), release_date, json.dumps(data)))

        cnx.commit()

        cursor.close()
        cnx.close()
        
        return data
    else:
        # If there was an error with the API request, print the status code and response text
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise Exception("Unable to search movie")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port =5000)

