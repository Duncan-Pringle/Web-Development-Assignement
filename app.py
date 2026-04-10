from flask import Flask, redirect, request, render_template, session, jsonify
import db_functions
import db as database
import api
import hashlib
from urllib.parse import unquote

app = Flask(__name__)
app.secret_key = 'super_secret_key'



def get_username():
    if 'id' not in session:
        return None
    result = db_functions.getUsernameFromID(session.get('id'))
    return result.get('username') if result else None

#  HOME
@app.route("/")
def home():
    data       = popular_movies_logic()
    movie_list = data.get("results", [])

    return render_template(
        "index.html",
        username=get_username(),
        featured_movie=movie_list[0] if movie_list else None,
        popular_movies=movie_list
    )



#  AUTH

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db_functions.getUserFromUsername(username)
        if not user:
            return render_template('login.html', error="Invalid username or password")

        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        stored_pass  = user.get('hashedpass') or user.get('hashedPass') or ''

        if hashed_input != stored_pass:
            return render_template('login.html', error="Invalid username or password")

        session['id']       = user['userid']
        session['is_admin'] = (user.get('userlevel') == 2)
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
        email    = request.form.get('email')
        password = request.form.get('password')

        if db_functions.getUserFromUsername(username):
            return render_template('signup.html', error="Username already taken")

        if db_functions.getUserFromEmail(email):
            return render_template('signup.html', error="Email already registered")

        hashed = hashlib.sha256(password.encode()).hexdigest()
        db_functions.createUser(username, email, hashed)

        result = db_functions.getIDFromUsername(username)
        session['id']       = result.get('userid') if result else None
        session['is_admin'] = False
        return redirect('/')

    return render_template('signup.html')



#  PROFILE & SETTINGS

@app.route('/profile')
def profile():
    if 'id' not in session:
        return redirect('/login')

    user_id      = session.get('id')
    name_result  = db_functions.getUsernameFromID(user_id)
    email_result = db_functions.getEmailFromID(user_id)
    username     = name_result.get('username')  if name_result  else None
    email        = email_result.get('email')    if email_result else None

    watchlist = db_functions.getWatchlistMovieDetails(user_id) or []
    for m in watchlist:
        if m.get('poster_url') and not m['poster_url'].startswith('http'):
            m['poster_url'] = api.TMDB_poster_url(m['poster_url'])

    return render_template('profile.html',
                           username=username,
                           email=email,
                           watchlist=watchlist,
                           show_nav=False)


@app.route('/settings')
def settings():
    if 'id' not in session:
    return redirect('/login')
    return redirect('/profile')
    

#  WATCHLIST

@app.route('/watchlist')
def watchlist():
    if 'id' not in session:
        return redirect('/login')

    user_id  = session.get('id')
    result   = db_functions.getUsernameFromID(user_id)
    username = result.get('username') if result else None

    wl = db_functions.getWatchlistMovieDetails(user_id) or []
    for m in wl:
        if m.get('poster_url') and not m['poster_url'].startswith('http'):
            m['poster_url'] = api.TMDB_poster_url(m['poster_url'])

    return render_template('watchlist.html', username=username, watchlist=wl)



#  TOGGLE WATCHLIST  

@app.route('/toggle-watchlist/<int:movie_id>', methods=['POST'])
def toggle_watchlist(movie_id):
    if 'id' not in session:
        return jsonify(status='error', message='Not logged in'), 401

    user_id = session.get('id')
    try:
        if db_functions.checkWatchlist(user_id, movie_id):
            db_functions.deleteWatchlistMovie(user_id, movie_id)
            return jsonify(status='removed')
        else:
            db_functions.createWatchlistMovie(user_id, movie_id)
            return jsonify(status='added')
    except Exception as e:
        print(f"Watchlist toggle error: {e}")
        return jsonify(status='error'), 500



#  MOVIE DETAILS

@app.route('/movie/<path:movie_name>')
def movie_details_page(movie_name):
    clean_name = unquote(movie_name)
    data = fetch_movie_by_name_logic(clean_name)
    if not data:
        return render_template('404.html'), 404

    is_in_watchlist = False
    if session.get('id'):
        movie_id = data.get('movieid') or data.get('movieID')
        is_in_watchlist = db_functions.checkWatchlist(session.get('id'), movie_id)

    return render_template('movieDetails.html',
                           movie=data,
                           is_in_watchlist=is_in_watchlist,
                           username=get_username())


def fetch_movie_by_name_logic(movie_name):
    try:
        movie = db_functions.getMovieByTitle(movie_name)
        if movie:
            movie_data = dict(movie)
            movie_data['genres'] = db_functions.getGenresForMovie(movie['movieid'])
            if movie_data.get('poster_url') and not movie_data['poster_url'].startswith('http'):
                movie_data['poster_url'] = api.TMDB_poster_url(movie_data['poster_url'])
            return movie_data

        tmdb_data = api.TMDB_search_first(movie_name)
        if not tmdb_data:
            return None

        full_details = api.TMDB_by_id(tmdb_data['id'])
        if "error" in full_details:
            return None

        movie_info = {
            "movieid":     full_details.get("id"),
            "movieID":     full_details.get("id"),
            "title":       full_details.get("title"),
            "description": full_details.get("overview"),
            "poster_url":  api.TMDB_poster_url(full_details.get("poster_path")),
            "year":        full_details.get("release_date", "")[:4] or "N/A",
            "rating":      full_details.get("vote_average"),
            "genres":      full_details.get("genres", [])
        }

        db_functions.createMovie(
            movieID=movie_info["movieID"],
            title=movie_info["title"],
            description=movie_info["description"],
            poster_url=full_details.get("poster_path"),
            year=movie_info["year"],
            genres=movie_info["genres"],
            rating=movie_info["rating"]
        )

        movie_info['genres'] = [g['name'] for g in movie_info['genres']]
        return movie_info

    except Exception as e:
        print(f"fetch_movie_by_name_logic error: {e}")
        return None



#  SEARCH

@app.route('/search')
def search_movies():
    query = request.args.get('q', '').strip()
    page  = request.args.get('page', 1, type=int)

    if not query:
        return redirect('/')

    try:
        results = api.TMDB_search(query, page=page)
        if "error" in results:
            return render_template('404.html'), 502

        movies = []
        for m in results.get("results", []):
            movies.append({
                "id":           m["id"],
                "title":        m["title"],
                "overview":     m.get("overview"),
                "release_date": m.get("release_date"),
                "poster_url":   api.TMDB_poster_url(m.get("poster_path")),
                "vote_average": m.get("vote_average"),
                "genre_ids":    m.get("genre_ids", [])
            })

        return render_template('search.html',
                               movies=movies,
                               query=query,
                               username=get_username())

    except Exception as e:
        print(f"Search error: {e}")
        return render_template('404.html'), 500



#  POPULAR MOVIES HELPER

def popular_movies_logic(page=1):
    try:
        results = api.TMDB_popular(page=page)
        if "error" in results:
            return {"results": []}

        movies = []
        for m in results.get("results", []):
            movies.append({
                "id":           m["id"],
                "title":        m["title"],
                "overview":     m.get("overview"),
                "release_date": m.get("release_date"),
                "poster_url":   api.TMDB_poster_url(m.get("poster_path")),
                "vote_average": m.get("vote_average"),
                "genre_ids":    m.get("genre_ids", [])
            })

        return {
            "results":       movies,
            "total_results": results.get("total_results"),
            "total_pages":   results.get("total_pages"),
            "page":          results.get("page")
        }
    except Exception as e:
        print(f"popular_movies_logic error: {e}")
        return {"results": []}



#  TV SHOWS

def popular_tv_logic(page=1):
    """Fetch popular TV shows from TMDB and normalise into the same shape as movies."""
    try:
        results = api.TMDB_tv_popular(page=page)
        if "error" in results:
            return {"results": []}

        shows = []
        for s in results.get("results", []):
            shows.append({
                "id":         s["id"],
                # TV shows use 'name' not 'title' in TMDB — normalise to 'title' so poster.html works
                "title":      s.get("name") or s.get("original_name", "Unknown"),
                "overview":   s.get("overview"),
                "poster_url": api.TMDB_poster_url(s.get("poster_path")),
                "vote_average": s.get("vote_average"),
                "first_air_date": s.get("first_air_date", ""),
            })

        return {
            "results":       shows,
            "total_results": results.get("total_results"),
            "total_pages":   results.get("total_pages"),
            "page":          results.get("page")
        }
    except Exception as e:
        print(f"popular_tv_logic error: {e}")
        return {"results": []}


@app.route('/tv')
def tv():
    data     = popular_tv_logic()
    shows    = data.get("results", [])
    featured = shows[0] if shows else None

    return render_template('tv.html',
                           username=get_username(),
                           featured_show=featured,
                           popular_shows=shows)



#  PEOPLE

@app.route('/people')
def people():
    try:
        user_list = db_functions.getAllUsers() or []
        user_list = user_list[:100]
    except Exception as e:
        print(f"People page error: {e}")
        user_list = []

    return render_template('people.html', people=user_list, username=get_username())



#  ADMIN

@app.route('/admin')
def admin():
    if 'id' not in session:
        return redirect('/login')
    if not session.get('is_admin'):
        return render_template('404.html'), 403

    users  = db_functions.getAllUsers()
    movies = db_functions.getAllMovies()

    return render_template("admin.html", users=users, movies=movies, username=get_username())


@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if not session.get('is_admin'):
        return render_template('404.html'), 403
    db_functions.deleteUser(user_id)
    return redirect('/admin')


@app.route('/admin/promote/<int:user_id>')
def promote(user_id):
    if not session.get('is_admin'):
        return render_template('404.html'), 403
    db_functions.setLevel(user_id, 2)
    return redirect('/admin')


@app.route('/make_admin')
def make_admin():
    if 'id' not in session:
        return redirect('/login')
    db_functions.setLevel(session['id'], 2)
    session['is_admin'] = True
    return redirect('/admin')


#  MISC
@app.route('/userdetails')
def userdetails():
    try:
        return jsonify({"Details": db_functions.getEverything()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



#  UTILITIES

def get_user_color(username):
    hash_hex = hashlib.md5(username.encode()).hexdigest()
    hue = int(hash_hex[:4], 16) % 360
    return f"hsl({hue}, 60%, 50%)"


@app.context_processor
def utility_processor():
    return dict(get_user_color=get_user_color)



#  DB TEARDOWN

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)


if __name__ == '__main__':
    app.run(debug=True)
