from flask import Flask, render_template, request
import requests

# ==============================
# CREATE FLASK APP
# ==============================
app = Flask(__name__)

# ==============================
# TMDB CONFIG
# ==============================
TMDB_API_KEY = "1f149116d178767b4a14df2f7330c202"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

# ==============================
# HOME PAGE
# ==============================


@app.route("/")
def home():
    return render_template("index.html")

# ==============================
# MOVIE RECOMMENDATION
# ==============================


@app.route("/recommend", methods=["POST"])
def recommend():
    movie_name = request.form.get("movie")
    genre_id = request.form.get("genre")

    if not movie_name or not genre_id:
        return render_template("index.html", error="Please enter a movie and select a genre!")

    try:
        genre_id = int(genre_id)  # Convert genre to integer
    except ValueError:
        return render_template("index.html", error="Invalid genre selected!")

    recommended_movies = []

    # 1. SEARCH MOVIE BY NAME
    search_response = requests.get(
        f"{TMDB_BASE_URL}/search/movie",
        params={"api_key": TMDB_API_KEY, "query": movie_name}
    ).json()

    if not search_response.get("results"):
        return render_template("index.html", error="Movie not found 😢")

    movie_id = search_response["results"][0]["id"]

    # 2. GET SIMILAR MOVIES
    similar_response = requests.get(
        f"{TMDB_BASE_URL}/movie/{movie_id}/similar",
        params={"api_key": TMDB_API_KEY}
    ).json()

    # 3. FILTER MOVIES BY GENRE
    for movie in similar_response.get("results", []):
        if genre_id in movie.get("genre_ids", []):
            recommended_movies.append({
                "title": movie.get("title"),
                "overview": movie.get("overview"),
                "rating": movie.get("vote_average"),
                "poster": POSTER_BASE_URL + movie.get("poster_path") if movie.get("poster_path") else ""
            })

    recommended_movies = recommended_movies[:6]  # limit to 6

    if not recommended_movies:
        return render_template("index.html", error="No recommended movies found for this genre 😢")

    return render_template("index.html", movies=recommended_movies)


# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    app.run(port=5001, debug=True)
