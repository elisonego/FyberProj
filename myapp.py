from flask import Flask, render_template, request
import requests
import os
import mysql.connector
import json
from datetime import datetime

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
    cnx = mysql.connector.connect(
        host="dev-rds-instance.cq5fbtzsgyiw.us-east-1.rds.amazonaws.com",
        user="elisonego",
        password="adminADMIN123",
        database="applicationDB"
    )

    cursor = cnx.cursor()

    # Try to get the movie from the database
    sql = ("SELECT data FROM movie_cache WHERE title = %s")
    cursor.execute(sql, (title,))
    result = cursor.fetchone()

    if result:
        print("Movie found in cache")
        data = json.loads(result[0])
    else:
        # Movie not in cache, get it from the OMDB API
        print("Movie not found in cache, fetching from API")
        api_key = os.getenv("OMDB_API_KEY")
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Store the movie in the database
            sql = ("INSERT INTO movie_cache (title, year, runtime, genre, data) "
                   "VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(sql, (title, data.get('Year', None), data.get('Runtime', None), data.get('Genre', None), json.dumps(data)))

            cnx.commit()
        else:
            print(f"Status code: {response.status_code}")
            print(f"Response text: {response.text}")
            raise Exception("Unable to search movie")

    cursor.close()
    cnx.close()
    
    return data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port =5000)
