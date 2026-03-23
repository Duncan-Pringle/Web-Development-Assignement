from flask import Flask, redirect, request, render_template, session, jsonify
import db_functions
import db as database
import os
import api

app = Flask(__name__)
app.secret_key = 'super_secret_key'
popular_movies = {
    0: {"title": "Inception", "year": 2010, "genre": "Sci-Fi", "rating": 8.8, "poster_url": "https://m.media-amazon.com/images/I/51s+qjv9ZlL._AC_.jpg", "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO."},
    1: {"title": "The Shawshank Redemption", "year": 1994, "genre": "Drama", "rating": 9.3, "poster_url": "https://m.media-amazon.com/images/I/51NiGlapXlL._AC_.jpg", "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."},
    2: {"title": "The Godfather", "year": 1972, "genre": "Crime", "rating": 9.2, "poster_url": "https://m.media-amazon.com/images/I/41+eK8zBwQL._AC_.jpg", "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."},
    3: {"title": "The Dark Knight", "year": 2008, "genre": "Action", "rating": 9.0, "poster_url": "https://m.media-amazon.com/images/I/51EbJjlLJ-L._AC_.jpg", "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."},
    4: {"title": "Pulp Fiction", "year": 1994, "genre": "Crime", "rating": 8.9, "poster_url": "https://m.media-amazon.com/images/I/51V5ZpFyaFL._AC_.jpg", "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."},
    5: {"title": "Forrest Gump", "year": 1994, "genre": "Drama", "rating": 8.8, "poster_url": "https://m.media-amazon.com/images/I/41c9r+eH7-L._AC_.jpg", "description": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold through the perspective of an Alabama man with an IQ of 75."}
}

@app.route('/')
def home():
    username = session.get('username') 
    return render_template('/templates/index.html', username=username, featured_movie=popular_movies.get(0), popular_movies=popular_movies)
USER_DB = {
    "admin": "password123"
}

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = popular_movies.get(movie_id)
    return render_template('movieDetails.html', movie=movie)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        
        if username in USER_DB and USER_DB[username] == password:
            session['username'] = username  
            return redirect('/')
        else:
            return "Invalid username or password", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/search')
def search():
    term = request.args.get('term', 'nothing')
    return f'Searching for: {term}'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/profile')
def profile():
    return render_template('profile.html', username=session['username'], show_nav=False)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
    


app = Flask(__name__)

#This if statement is try to fix an issue when deploying where the page infinite loads until restart
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) #Default to 8000 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=False)

@app.route('/HELLOWORLD') #Base route for the home page "https://web-development-assignement.onrender.com/"
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
@app.route('/MOVIENEEDSEDITED/<int:movie_id>') 
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
        
#Search for movies thru TMDB, uses my method from api.py so you can do this with or without pages like /search?q=shrek or /search?q=shrek&page=2
@app.route('/SEARCHNEEDSEDITED') 
def search_movies():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
 
    if not query:
        return jsonify({"error": "Missing search query. Use ?q=your+search+term"}), 400
 
    try:
        results = api.TMDB_search(query, page=page)
        if "error" in results:
            return jsonify(results), 502
 
        movies = []
        for m in results.get("results", []):
            movies.append({
                "id": m["id"],
                "title": m["title"],
                "overview": m.get("overview"),
                "release_date": m.get("release_date"),
                "poster_url": api.TMDB_poster_url(m.get("poster_path")),
                "vote_average": m.get("vote_average"),
                "genre_ids": m.get("genre_ids", [])
            })
 
        return jsonify({
            "results": movies,
            "total_results": results.get("total_results"),
            "total_pages": results.get("total_pages"),
            "page": results.get("page")
        }), 200
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Returns a list of popular movies from tmdb, also has the option for us to grab more pages of popular films just like the search method above
@app.route('/POPMOVIESNEEDSEDITED/popular') 
def popular_movies():
    page = request.args.get('page', 1, type=int)
    try:
        results = api.TMDB_popular(page=page)
        if "error" in results:
            return jsonify(results), 502
 
        movies = []
        for m in results.get("results", []):
            movies.append({
                "id": m["id"],
                "title": m["title"],
                "overview": m.get("overview"),
                "release_date": m.get("release_date"),
                "poster_url": api.TMDB_poster_url(m.get("poster_path")),
                "vote_average": m.get("vote_average"),
                "genre_ids": m.get("genre_ids", [])
            })
 
        return jsonify({
            "results": movies,
            "total_results": results.get("total_results"),
            "total_pages": results.get("total_pages"),
            "page": results.get("page")
        }), 200
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#very simple method that gives us just a plaintext of the full tmdb genres list. could be useful for translating genre ids
#might be useless, but it was very simple to add regardless so figured why not, can just delete later
@app.route('/GENRESNEEDSEDITED') 
async def genres():
    try:
        result = await api.get_genres()
        if "error" in result:
            return jsonify(result), 502
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
