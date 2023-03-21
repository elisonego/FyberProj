from flask import Flask, render_template, request
import requests

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
    api_key = "53ba70e1"
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    response = requests.get(url)
    if response.status_code == 200:
        # The API returns a JSON response, so we can use the built-in JSON parser
        return response.json()
    else:
        # If there was an error with the API request, raise an exception
        raise Exception("Unable to search movie")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port =5000)

