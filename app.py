from flask import Flask, redirect, request, render_template, session, jsonify
import db_functions
import db as database
import api

app = Flask(__name__)
app.secret_key = 'super_secret_key'


@app.route("/")
def home():
    if 'id' in session:
        username = db_functions.getUsernameFromID(session.get('id')).get("username")
    else:
        username = None

    data = popular_movies()
    movie_list = data.get("results", [])

    return render_template(
        "index.html",
        username=username,
        featured_movie=movie_list[0] if movie_list else None,
        popular_movies=movie_list
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db_functions.getUserFromUsername(username)

        if not user:
            return render_template('login.html', error="Invalid login")

        if password != user.get('hashedpass') and password != user.get('hashedPass'):
            return render_template('login.html', error="Invalid login")

        session['id'] = user['userid']
        session['is_admin'] = (user['userlevel'] == 2)

        return redirect('/')
   
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if db_functions.getUserFromUsername(username):
            return render_template('signup.html', error="Username exists")

        db_functions.createUser(username, email, password)

        session['id'] = db_functions.getIDFromUsername(username).get("userid")
        return redirect('/')

    return render_template('signup.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/profile')
def profile():
    return render_template('profile.html', username=db_functions.getUsernameFromID(session.get('id')).get("username"), show_nav=False, email=db_functions.getEmailFromID(session.get('id')).get("email"))

@app.route('/watchlist')
def watchlist():
    #shouldn't be possible to get here without being logged in but just in case, redirect to login if we don't have a user id in the session
    if 'id' not in session:
        return redirect('/login')
    watchlist = db_functions.getUserWatchlist(session.get('id'))
    return render_template('watchlist.html', username=db_functions.getUsernameFromID(session.get('id')).get("username"), watchlist=watchlist)

@app.route('/userdetails')
def userdetails():
    try:
        test = {
            "Details": db_functions.getEverything()
            }
        return jsonify(test), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

# Updated fetch movie
def fetch_movie_by_name_logic(movie_name):
    print(f"DEBUG: Starting fetch for movie: '{movie_name}'")
    try:
        # check DB by Title 
        movie = db_functions.getMovieByTitle(movie_name) 
        if movie:
            print(f"DEBUG: Found '{movie_name}' in Database.")
            movie_data = dict(movie)
            movie_data['genres'] = db_functions.getGenresForMovie(movie['movieid'])
            # ensure poster_url is a full URL 
            if movie_data['poster_url'] and not movie_data['poster_url'].startswith('http'):
                 movie_data['poster_url'] = api.TMDB_poster_url(movie_data['poster_url'])
            return movie_data
        print(f"DEBUG: '{movie_name}' not in DB. Searching TMDB...")
        #search TMDB by string
        tmdb_data = api.TMDB_search_first(movie_name)
        if not tmdb_data:
            print(f"DEBUG: TMDB Search returned ZERO results for '{movie_name}'")
            return None
        print(f"DEBUG: TMDB found a match: {tmdb_data.get('title')} (ID: {tmdb_data.get('id')})")
        # format
        
        full_details = api.TMDB_by_id(tmdb_data['id'])
        if "error" in full_details:
            print(f"DEBUG: TMDB Detail call failed: {full_details['error']}")
            return None

        movie_info = {
            "movieID": full_details.get("id"),
            "title": full_details.get("title"),
            "description": full_details.get("overview"),
            "poster_url": api.TMDB_poster_url(full_details.get("poster_path")),
            "year": full_details.get("release_date", "")[:4] or "N/A",
            "rating": full_details.get("vote_average"),
            "genres": full_details.get("genres", []) 
        }
        # save to DB
        print(f"DEBUG: Attempting to save '{movie_info['title']}' to DB...")
        db_functions.createMovie(
            movieID=movie_info["movieID"],
            title=movie_info["title"],
            description=movie_info["description"],
            poster_url=full_details.get("poster_path"), # Save suffix only
            year=movie_info["year"],
            genres=movie_info["genres"],
            rating=movie_info["rating"]
        )

        movie_info['genres'] = [g['name'] for g in movie_info['genres']]
        print(f"DEBUG: Successfully saved to DB.")
        return movie_info

    except Exception as e:
        print(f"Error: {e}")
        return None

#updated route
@app.route('/movie/<path:movie_name>')
def movie_details_page(movie_name):
    
    # handle URL-encoded spaces (%20)
    from urllib.parse import unquote
    clean_name = unquote(movie_name)
    
    data = fetch_movie_by_name_logic(clean_name)
    if not data:
        return "Movie not found", 404
    is_in_watchlist = False
    if session.get('id'):
    # Check if this specific movie is in this user's list
        is_in_watchlist = db_functions.checkWatchlist(session.get('id'), data['movieid'])
    return render_template('movieDetails.html', movie=data, is_in_watchlist=is_in_watchlist, username = db_functions.getUsernameFromID(session.get('id')).get("username") if 'id' in session else None)

#Think we can delete this despite all the refactoring I did 😭
#Returns movie data from tmdb, but checks if we have it in the db first to instead use that
#caches the film in the DB for next time if we don't have it and stores the poster url as a suffix, use api.TMDB_poster_url() to build the full URL whenever we need it
def fetch_movie_logic(movie_id):
    try:
        # check local database first
        movie = db_functions.getMovieFromID(movie_id)
        if movie:
            return dict(movie)

        # not found, call TMDB
        tmdb_data = api.TMDB_by_id(movie_id)
        if "error" in tmdb_data:
            return None

        # clean up the data for our use
        movie_info = {
            "movieID": tmdb_data.get("id"),
            "title": tmdb_data.get("title"),
            "description": tmdb_data.get("overview"),
            "poster_url": api.TMDB_poster_url(tmdb_data.get("poster_path")),
            "year": tmdb_data.get("release_date", "")[:4] or "N/A",
            "rating": tmdb_data.get("vote_average"),
            "genres": [g['name'] for g in tmdb_data.get("genres", [])] # Extract names
        }

        # cache it in our DB for later
        db_functions.createMovie(
            movieID=movie_info["movieID"],
            title=movie_info["title"],
            description=movie_info["description"],
            poster_url=tmdb_data.get("poster_path"), 
            year=movie_info["year"],
            genres=movie_info["genres"],
            rating=movie_info["rating"]
        )

        return movie_info

    except Exception as e:
        print(f"Server-side error: {e}")
        return None
#don't think I'm using this anymore so we can probably delete
#changed name to pag


#Search for movies thru TMDB, uses my method from api.py so you can do this with or without pages like ?q=shrek or ?q=shrek&page=2
@app.route('/search') #To fix, added await and removed error
async def search_movies():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({"error": "Missing search query. Use ?q=your+search+term"}), 400
 
    try:
        results = await api.TMDB_search(query, page=page)
        if "error" in results:
            return results, 502
 
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
 
        return {
            "results": movies,
            "total_results": results.get("total_results"),
            "total_pages": results.get("total_pages"),
            "page": results.get("page")
        }
 
    except Exception as e:
        return {"error": str(e)}, 500

#Returns a list of popular movies from tmdb, also has the option for us to grab more pages of popular films just like the search method above
@app.route('/POPMOVIESNEEDSEDITED/popular') #To fix, added await and removed error 
def popular_movies():
    page = request.args.get('page', 1, type=int)
    try:
        results = api.TMDB_popular(page=page)
        if "error" in results:
            print(f"Error fetching popular movies: {results['error']}")
            return results, 502
 
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
        print("Fetched popular movies from TMDB")
        return {
            "results": movies,
            "total_results": results.get("total_results"),
            "total_pages": results.get("total_pages"),
            "page": results.get("page")
        }
 
    except Exception as e:
        print(f"Error fetching popular movies: {e}")
        return {"error": str(e)}, 500

#very simple method that gives us just a plaintext of the full tmdb genres list. could be useful for translating genre ids
#might be useless, but it was very simple to add regardless so figured why not, can just delete later
@app.route('/GENRESNEEDSEDITED') 
async def genres():
    try:
        result = await api.get_genres()
        if "error" in result:
            return jsonify(result), 502
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tv')
def tv():
    return render_template('404.html')


@app.route('/people')
def people():
    return render_template('404.html')


@app.route('/admin')
def admin():
    if 'id' not in session:
        return redirect('/login')

    if not session.get('is_admin'):
        return "Access denied", 403

    users = db_functions.getAllUsers()
    movies = db_functions.getAllMovies()

    return render_template("admin.html", users=users, movies=movies, username=db_functions.getUsernameFromID(session.get('id')).get("username"))


@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if not session.get('is_admin'):
        return "Access denied", 403

    db_functions.deleteUser(user_id)
    return redirect('/admin')


@app.route('/admin/promote/<int:user_id>')
def promote(user_id):
    if not session.get('is_admin'):
        return "Access denied", 403

    db_functions.setLevel(user_id, 2)
    return redirect('/admin')


@app.route('/make_admin')
def make_admin():
    db_functions.setLevel(session['id'], 2)
    session['is_admin'] = True
    return "Now admin"


@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

@app.route('/toggle-watchlist/<int:movie_id>', methods=['POST'])
def toggle_watchlist(movie_id):
    print(f"DEBUG: Toggling watchlist for movie_id={movie_id} and user_id={session.get('id')}")
    try:
        if db_functions.checkWatchlist(session.get('id'), movie_id):
            print(f"DEBUG: Movie {movie_id} is currently in watchlist, removing...")
            db_functions.deleteWatchlistMovie(session.get('id'), movie_id)
            return jsonify(status='removed')
        else:
            print(f"DEBUG: Movie {movie_id} is not in watchlist, adding...")
            db_functions.createWatchlistMovie(session.get('id'), movie_id)
            return jsonify(status='added')

    except Exception as e:
        print(f"DEBUG: Error occurred while toggling watchlist for movie_id={movie_id}: {e}")
        return jsonify(status='error'), 500

if __name__ == '__main__':
    app.run(debug=True)

