import tmdbsimple as tmdb
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

load_dotenv()
tmdb.API_KEY = os.getenv("TMDB_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/movies")
def movies():
    return render_template("movies.html")

@app.route("/tv")
def tv():
    return render_template("tv.html")

@app.route("/movieplayer/<format>/<media_id>")
def movieplayer(format, media_id):
    return render_template("movieplayer.html", format=format, media_id=media_id)

@app.route("/tvplayer/<format>/<media_id>")
def tvplayer(format, media_id):
    return render_template("tvplayer.html", format=format, media_id=media_id)

@app.route("/api/search/movie", methods=["GET"])
def search_movie_route():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    results = search_movie(query)
    return jsonify(results)

@app.route("/api/movies/popular")
def popular_movies():
    movies = tmdb.Movies()
    response = movies.popular()
    return jsonify(response['results'])

@app.route("/api/search/tv", methods=["GET"])
def search_tv_route():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
    results = search_tv_show(query)
    return jsonify(results)

@app.route("/api/movies/discover")
def discover_movies():
    genre = request.args.get('genre', '')
    decade = request.args.get('decade', '')
    rating_min = request.args.get('rating_min', '0')
    rating_max = request.args.get('rating_max', '10')

    discover = tmdb.Discover()
    params = {
        'vote_average.gte': rating_min,
        'vote_average.lte': rating_max,
        'vote_count.gte': 10  # avoids movies with 1 vote rated 10
    }

    if genre:
        params['with_genres'] = genre
    if decade:
        params['primary_release_date.gte'] = f'{decade}-01-01'
        params['primary_release_date.lte'] = f'{int(decade)+9}-12-31'

    results = []
    for page in range(1, 4):
        params['page'] = page
        response = discover.movie(**params)
        results.extend(response['results'])

    return jsonify(results)



def search_movie(query):
    search = tmdb.Search()
    response = search.movie(query=query)
    return response['results']

def search_tv_show(query):
    search = tmdb.Search()
    response = search.tv(query=query)
    return response['results']

def get_movie_details(movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.info()
    return response

def get_popular_movies():
    movies = tmdb.Movies()
    response = movies.popular()
    return response['results']



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))