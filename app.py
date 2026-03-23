from flask import Flask
from flask import jsonify
import db_functions
import db as database
import os
import api

app = Flask(__name__)

#This if statement is try to fix an issue when deploying where the page infinite loads until restart
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) #Default to 8000 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=False)

@app.route('/') #Base route for the home page "https://web-development-assignement.onrender.com/"
def hello_world():
    return 'Hello, World!'

@app.route('/test2') #Test route "https://web-development-assignement.onrender.com/test2"
def testselects():
        try:
            test = {
                "All users test": db_functions.getAllUsers(),
                "userid 1": db_functions.getUserFromID(1),
                "user from email": db_functions.getUserFromEmail("user2email@email.com"),
                "email from id": db_functions.getEmailFromID(2),
                "id from username": db_functions.getIDFromUsername("username3"),
                "all movies": db_functions.getAllMovies(),
                "user from id 2": db_functions.getUserFromID(2),
                "movie reviews 550": db_functions.getMovieReviews(550),
                "user reviews 4": db_functions.getUserReviews(4),
                "review id 2": db_functions.getReviewFromID(2)
            }
            return jsonify(test), 200
        except Exception as e:
             return jsonify({"error": str(e)}), 500

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

#Returns movie data from tmdb, but checks if we have it in the db first to instead use that
#caches the film in the DB for next time if we don't have it and stores the poster url as a suffix, use api.TMDB_poster_url() to build the full URL whenever we need it
@app.route('/movie/<int:movie_id>') 
def get_movie(movie_id):
    try:
        movie = db_functions.getMovieFromID(movie_id)
        if movie:
            return jsonify(dict(movie)), 200
 
        tmdb_data = api.TMDB_by_id(movie_id)
        if "error" in tmdb_data:
            return jsonify(tmdb_data), 502
 
        db_functions.createMovie(
            movieID=tmdb_data["id"],
            title=tmdb_data["title"],
            description=tmdb_data.get("overview"),
            poster_url=tmdb_data.get("poster_path"),
            year=tmdb_data.get("release_date", "")[:4] or None,
            genres=tmdb_data.get("genres", []), 
            rating=tmdb_data.get("vote_average")
        )
 
        return jsonify({
            "movieID": tmdb_data["id"],
            "title": tmdb_data["title"],
            "description": tmdb_data.get("overview"),
            "poster_url": tmdb.get_poster_url(tmdb_data.get("poster_path")),
            "year": tmdb_data.get("release_date", "")[:4] or None,
            "rating": tmdb_data.get("vote_average"),
            "genres": tmdb_data.get("genres", [])
        }), 200
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
