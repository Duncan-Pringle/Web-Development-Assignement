from flask import Flask, redirect, request, render_template, session, jsonify
import db_functions
import db as database
import api
import hashlib
import os
from urllib.parse import unquote
from flasgger import Swagger

app = Flask(__name__)
app.secret_key = 'super_secret_key'
swagger = Swagger(app, template={"info": {
    "title": "Moviehub API",
    "version": "1.0.0"
}})



def get_username():
    if 'id' not in session:
        return None
    result = db_functions.getUsernameFromID(session.get('id'))
    return result.get('username') if result else None

def check_admin():
    session['is_admin'] = (user.get('userlevel') == 2)
    return

#  HOME

@app.route("/")
def home():
    check_admin()
    """
    Home page - displays popular movies
    ---
    tags:
      - Pages
    responses:
      200:
        description: Home page rendered with popular movies
    """
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
    """
    Login page and authentication
    ---
    tags:
      - Auth
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: The user's username
      - name: password
        in: formData
        type: string
        required: true
        description: The user's password (plaintext, hashed server-side)
    responses:
      302:
        description: Redirect to home on successful login
      200:
        description: Login page returned with error message on failure
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password = hashlib.pbkdf2_hmac('sha256', password.encode(), os.environ.get("SALT").encode(), 260000).hex()
        user = db_functions.getUserFromUsername(username)
        if not user:
            return render_template('login.html', error="Invalid username or password")
        if password != user['hashedpass']:
            return render_template('login.html', error="Invalid username or password")
        session['id']       = user['userid']
        session['is_admin'] = (user.get('userlevel') == 2)
        return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    Logs the current user out and clears their session
    ---
    tags:
      - Auth
    responses:
      302:
        description: Redirect to home page
    """
    session.clear()
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Signup page and new user registration
    ---
    tags:
      - Auth
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Desired username (must be unique)
      - name: email
        in: formData
        type: string
        required: true
        description: User's email address (must be unique)
      - name: password
        in: formData
        type: string
        required: true
        description: Desired password (plaintext, hashed server-side)
    responses:
      302:
        description: Redirect to home on successful signup, user is logged in automatically
      200:
        description: Signup page returned with error if username or email already taken
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email    = request.form.get('email')
        password = request.form.get('password')
        if db_functions.getUserFromUsername(username):
            return render_template('signup.html', error="Username already taken")
        if db_functions.getUserFromEmail(email):
            return render_template('signup.html', error = "Email already in use")

        password = hashlib.pbkdf2_hmac('sha256', password.encode(), os.environ.get("SALT").encode(), 260000).hex()
        db_functions.createUser(username, email, password)

        result = db_functions.getIDFromUsername(username)
        session['id']       = result.get('userid') if result else None
        session['is_admin'] = False        
        return redirect('/')        

    return render_template('signup.html')



#  PROFILE & SETTINGS

@app.route('/profile')
def profile():
    """
    Current user's profile page
    ---
    tags:
      - Users
    responses:
      200:
        description: Profile page with watchlist and user details
      302:
        description: Redirect to login if not authenticated
    """
    if 'id' not in session:
        return redirect('/login')
     # Check terminal/logs for this!
    user_id = session.get('id')
    activity = db_functions.getRecentActivity(user_id)
    print(f"DEBUG ACTIVITY: {activity}")
    name_result = db_functions.getUsernameFromID(user_id)
    email_result = db_functions.getEmailFromID(user_id)
    
    username = name_result.get('username') if name_result else None
    email = email_result.get('email') if email_result else None
    watchlist = db_functions.getWatchlistMovieDetails(user_id) or []

    for m in watchlist:
        if m.get('poster_url') and not m['poster_url'].startswith('http'):
            m['poster_url'] = api.TMDB_poster_url(m['poster_url'])

    return render_template(
    'profile_overview.html',
    profile_owner=username,     # The name shown on the profile
    current_user=username,      # The name of the person logged in
    email=email,                # Only passed here because it's the user's own profile
    watchlist=watchlist,        # The list of movie posters
    activity=activity,          # The UNION ALL feed we built
    is_own_profile=True,        # Enables the "Settings" link in the sidebar
    active_page='overview'      # Highlights 'Overview' in the sidebar
)


@app.route('/profile/<username>')
def view_profile(username):
    user = db_functions.getUserFromUsername(username)
    if not user:
        return render_template('404.html'), 404

    # The person currently logged in
    current_user_name = None
    is_own_profile = False
    
    if 'id' in session:
        current_user_data = db_functions.getUsernameFromID(session.get('id'))
        if current_user_data:
            current_user_name = current_user_data.get('username')
            if current_user_name == username:
                is_own_profile = True

    # Fetch activity and watchlist for the PROFILE OWNER (user['userid'])
    activity = db_functions.getRecentActivity(user['userid']) or []
    watchlist = db_functions.getWatchlistMovieDetails(user['userid']) or []

    return render_template('profile_overview.html',
                           profile_owner=user['username'],  # The profile we are looking at
                           current_user=current_user_name, # The person logged in
                           email=user['email'] if is_own_profile else None,
                           watchlist=watchlist,
                           activity=activity,
                           is_own_profile=is_own_profile)


@app.route('/settings')
def settings():
    """
    Settings page
    ---
    tags:
      - Users
    responses:
      200:
        description: Profile settings page
      302:
        description: Redirect to login if not authenticated
    """
    if 'id' not in session:
        return redirect('/login')

    user_id = session.get('id')
    user_data = db_functions.getUsernameFromID(user_id)
    email_data = db_functions.getEmailFromID(user_id)

    return render_template('profile_settings.html',
                           username=user_data.get('username'),
                           email=email_data.get('email'),
                           is_own_profile=True)



#  MOVIE WATCHLIST PAGE

@app.route('/watchlist')
def watchlist():
    """
    Current user's movie watchlist page
    ---
    tags:
      - Watchlist
    responses:
      200:
        description: Watchlist page with all saved movies
      302:
        description: Redirect to login if not authenticated
    """
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



#  TV WATCHLIST PAGE

@app.route('/tv-watchlist')
def tv_watchlist():
    """
    Current user's TV show watchlist page
    ---
    tags:
      - Watchlist
    responses:
      200:
        description: TV watchlist page with all saved shows
      302:
        description: Redirect to login if not authenticated
    """
    if 'id' not in session:
        return redirect('/login')
    user_id  = session.get('id')
    result   = db_functions.getUsernameFromID(user_id)
    username = result.get('username') if result else None
    wl = db_functions.getTVWatchlistDetails(user_id) or []
    for s in wl:
        if s.get('poster_url') and not s['poster_url'].startswith('http'):
            s['poster_url'] = api.TMDB_poster_url(s['poster_url'])
    return render_template('tv_watchlist.html', username=username, watchlist=wl)



#  TOGGLE MOVIE WATCHLIST 

@app.route('/toggle-watchlist/<int:movie_id>', methods=['POST'])
def toggle_watchlist(movie_id):
    """
    Add or remove a movie from the current user's watchlist
    ---
    tags:
      - Watchlist
    parameters:
      - name: movie_id
        in: path
        type: integer
        required: true
        description: TMDB movie ID to add or remove
    responses:
      200:
        description: JSON with status 'added' or 'removed'
        schema:
          properties:
            status:
              type: string
              example: added
      401:
        description: Not logged in
      500:
        description: Server error
    """
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
        print(f"Movie watchlist toggle error: {e}")
        return jsonify(status='error'), 500



#  TOGGLE TV WATCHLIST (AJAX)

@app.route('/toggle-tv-watchlist/<int:show_id>', methods=['POST'])
def toggle_tv_watchlist(show_id):
    """
    Add or remove a TV show from the current user's watchlist
    ---
    tags:
      - Watchlist
    parameters:
      - name: show_id
        in: path
        type: integer
        required: true
        description: TMDB show ID to add or remove
    responses:
      200:
        description: JSON with status 'added' or 'removed'
        schema:
          properties:
            status:
              type: string
              example: added
      401:
        description: Not logged in
      500:
        description: Server error
    """
    if 'id' not in session:
        return jsonify(status='error', message='Not logged in'), 401
    user_id = session.get('id')
    try:
        if db_functions.checkTVWatchlist(user_id, show_id):
            db_functions.deleteTVWatchlist(user_id, show_id)
            return jsonify(status='removed')
        else:
            db_functions.createTVWatchlist(user_id, show_id)
            return jsonify(status='added')
    except Exception as e:
        print(f"TV watchlist toggle error: {e}")
        return jsonify(status='error'), 500



#  MOVIE DETAILS

@app.route('/movie/<path:movie_name>')
def movie_details_page(movie_name):
    """
    Movie details page - checks local DB first, falls back to TMDB search
    ---
    tags:
      - Movies
    parameters:
      - name: movie_name
        in: path
        type: string
        required: true
        description: Movie title (URL encoded)
    responses:
      200:
        description: Movie details page
      404:
        description: Movie not found in DB or TMDB
    """
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
            movieID=movie_info["movieID"], title=movie_info["title"],
            description=movie_info["description"],
            poster_url=full_details.get("poster_path"),
            year=movie_info["year"], genres=movie_info["genres"],
            rating=movie_info["rating"]
        )
        movie_info['genres'] = [g['name'] for g in movie_info['genres']]
        return movie_info
    except Exception as e:
        print(f"fetch_movie_by_name_logic error: {e}")
        return None



#  TV SHOW DETAILS

@app.route('/tv/show/<int:show_id>')
def tv_details_page(show_id):
    """
    TV show details page - checks local DB first, falls back to TMDB
    ---
    tags:
      - TV Shows
    parameters:
      - name: show_id
        in: path
        type: integer
        required: true
        description: TMDB TV show ID
    responses:
      200:
        description: TV show details page
      404:
        description: Show not found
    """
    data = fetch_tv_by_id_logic(show_id)
    if not data:
        return render_template('404.html'), 404
    is_in_watchlist = False
    if session.get('id'):
        is_in_watchlist = db_functions.checkTVWatchlist(session.get('id'), show_id)
    return render_template('tvDetails.html',
                           show=data,
                           is_in_watchlist=is_in_watchlist,
                           username=get_username())



def fetch_tv_by_id_logic(show_id):
    try:
        cached = db_functions.getTVShowByID(show_id)
        if cached:
            data = dict(cached)
            if data.get('poster_url') and not data['poster_url'].startswith('http'):
                data['poster_url'] = api.TMDB_poster_url(data['poster_url'])
            return data
        full = api.TMDB_tv_by_id(show_id)
        if "error" in full:
            return None
        show_info = {
            "showid":         full.get("id"),
            "showID":         full.get("id"),
            "title":          full.get("name") or full.get("original_name", "Unknown"),
            "description":    full.get("overview"),
            "poster_url":     api.TMDB_poster_url(full.get("poster_path")),
            "first_air_date": full.get("first_air_date", ""),
            "rating":         full.get("vote_average"),
            "genres":         [g['name'] for g in full.get("genres", [])],
        }
        db_functions.createTVShow(
            showID=show_info["showID"],
            name=show_info["title"],
            description=show_info["description"],
            poster_url=full.get("poster_path"),
            first_air_date=show_info["first_air_date"],
            genres=full.get("genres", []),
            number_of_seasons=full.get("number_of_seasons"),
            rating=show_info["rating"]
        )
        return show_info
    except Exception as e:
        print(f"fetch_tv_by_id_logic error: {e}")
        return None



#  SEARCH

@app.route('/search')
def search_movies():
    """
    Search for movies via TMDB
    ---
    tags:
      - Movies
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Search query string
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number of results
    responses:
      200:
        description: Search results page
      302:
        description: Redirect to home if query is empty
      502:
        description: TMDB API error
    """
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
        return render_template('search.html', movies=movies,
                               query=query, username=get_username())
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
        return {"results": movies, "total_results": results.get("total_results"),
                "total_pages": results.get("total_pages"), "page": results.get("page")}
    except Exception as e:
        print(f"popular_movies_logic error: {e}")
        return {"results": []}



#  TV SHOWS PAGE + POPULAR HELPER

def popular_tv_logic(page=1):
    try:
        results = api.TMDB_tv_popular(page=page)
        if "error" in results:
            return {"results": []}
        shows = []
        for s in results.get("results", []):
            shows.append({
                "id":             s["id"],
                "title":          s.get("name") or s.get("original_name", "Unknown"),
                "overview":       s.get("overview"),
                "poster_url":     api.TMDB_poster_url(s.get("poster_path")),
                "vote_average":   s.get("vote_average"),
                "first_air_date": s.get("first_air_date", ""),
            })
        return {"results": shows, "total_results": results.get("total_results"),
                "total_pages": results.get("total_pages"), "page": results.get("page")}
    except Exception as e:
        print(f"popular_tv_logic error: {e}")
        return {"results": []}


@app.route('/tv')
def tv():
    """
    TV shows home page - displays popular TV shows
    ---
    tags:
      - TV Shows
    responses:
      200:
        description: TV shows page with featured and popular shows
    """
    data  = popular_tv_logic()
    shows = data.get("results", [])
    return render_template('tv.html',
                           username=get_username(),
                           featured_show=shows[0] if shows else None,
                           popular_shows=shows)



#  PEOPLE

@app.route('/people')
def people():
    """
    People page - lists registered users
    ---
    tags:
      - Users
    responses:
      200:
        description: People page with list of up to 100 users
    """
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
    """
    Admin dashboard - lists all users and movies
    ---
    tags:
      - Admin
    responses:
      200:
        description: Admin panel rendered
      302:
        description: Redirect to login if not authenticated
      403:
        description: Access denied if not admin
    """
    if 'id' not in session:
        return redirect('/login')
    if not session.get('is_admin'):
        return render_template('404.html'), 403
    users  = db_functions.getAllUsers()
    movies = db_functions.getAllMovies()
    return render_template("admin.html", users=users, movies=movies, username=get_username())


@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    """
    Delete a user by ID (admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to delete
    responses:
      302:
        description: Redirect to admin panel
      403:
        description: Access denied if not admin
    """
    if not session.get('is_admin'):
        return render_template('404.html'), 403
    db_functions.deleteUser(user_id)
    return redirect('/admin')


@app.route('/admin/promote/<int:user_id>'  )
def promote(user_id):
    """
    Promote a user to admin (admin only)
    ---
    tags:
      - Admin
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to promote
    responses:
      302:
        description: Redirect to admin panel
      403:
        description: Access denied if not admin
    """
    if not session.get('is_admin'):
        return render_template('404.html'), 403
    db_functions.setLevel(user_id, 2)
    return redirect('/admin')


@app.route('/make_admin')
def make_admin():
    """
    Promote the currently logged in user to admin
    ---
    tags:
      - Admin
    responses:
      302:
        description: Redirect to admin panel, or login if not authenticated
    """
    if 'id' not in session:
        return redirect('/login')
    db_functions.setLevel(session['id'], 2)
    session['is_admin'] = True
    return redirect('/admin')

@app.route('/update-username', methods=['POST'])
def update_username():
    if 'id' not in session:
        return redirect('/login')
    
    new_username = request.form.get('new_username')
    user_id = session.get('id')
    
    if new_username:
        # Update DB
        db_functions.setUsername(user_id, new_username)
        # Sync session so the UI updates
        session['username'] = new_username
        
    return redirect('/settings')

@app.route('/update-password', methods=['POST'])
def update_password():
    if 'id' not in session:
        return redirect('/login')
    
    new_password = request.form.get('new_password')
    user_id = session.get('id')
    
    if new_password:
        # Use your specific hashing logic
        salt = os.environ.get("SALT").encode()
        hashed_pw = hashlib.pbkdf2_hmac(
            'sha256', 
            new_password.encode(), 
            salt, 
            260000
        ).hex()
        
        db_functions.setPassword(user_id, hashed_pw)
        
    return redirect('/settings')

@app.route('/delete-account', methods=['POST'])
def delete_account():
    if 'id' not in session:
        return redirect('/login')
    
    user_id = session.get('id')
    db_functions.deleteUser(user_id)
    
    session.clear()
    return redirect('/')

#  MISC

@app.route('/userdetails')
def userdetails():
    """
    Debug route - returns entire database contents as JSON
    ---
    tags:
      - Debug
    responses:
      200:
        description: All database tables as JSON
      500:
        description: Server error
    """
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


@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)


if __name__ == '__main__':
    app.run(debug=True)


### Routes for creating reviews, getting reviews and frontend deletion of reviews
### by the session user or an administrator

@app.route('/movie/<int:movie_id>/reviews', methods=['GET'])
def get_movie_reviews(movie_id):
    """
    Get all reviews for a movie
    ---
    tags:
      - Reviews
    parameters:
      - name: movie_id
        in: path
        type: integer
        required: true
        description: ID of the movie to get reviews for
    responses:
      200:
        description: List of reviews as JSON
    """
    reviews = db_functions.getMovieReviews(movie_id)
    return jsonify(reviews)

@app.route('/post-review/<int:movie_id>', methods=['POST'])
def post_review(movie_id):
    """
    Create a review for a movie
    ---
    tags:
      - Reviews
    parameters:
      - name: movie_id
        in: path
        type: integer
        required: true
        description: ID of the movie to review
      - name: reviewText
        in: formData
        type: string
        required: true
        description: The review text content
      - name: rating
        in: formData
        type: integer
        required: true
        description: Rating out of 10
    responses:
      200:
        description: Review created successfully
      400:
        description: Missing review text or rating
      401:
        description: Not logged in
      500:
        description: Server error
    """
    user_id = session.get('id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json()
    text = data.get('reviewText', '').strip()
    rating = data.get('rating')

    if not text or not rating:
        return jsonify({"status": "error", "message": "Review and rating are required"}), 400

    try:
        db_functions.createMovieReview(text, user_id, movie_id, int(rating))
        return jsonify({"status": "success", "message": "Review added!"})
    except Exception as e:
        print(f"DEBUG: Review Error - {e}")
        return jsonify({"status": "error", "message": "Failed to post review"}), 500

@app.route('/review/<int:review_id>/delete', methods=['POST'])
def delete_review_user(review_id):
    """
    Delete a review - users can only delete their own, admins can delete any
    ---
    tags:
      - Reviews
    parameters:
      - name: review_id
        in: path
        type: integer
        required: true
        description: ID of the review to delete
    responses:
      200:
        description: Review deleted successfully
      401:
        description: Not logged in
      403:
        description: Review belongs to another user and requester is not admin
      404:
        description: Review not found
    """
    if 'id' not in session:
        return jsonify({"error": "You must be logged in to delete a review."}), 401
 
    review = db_functions.getReviewFromID(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
 
    if review['userid'] != session['id'] and not session.get('is_admin'):
        return jsonify({"error": "You can only delete your own reviews"}), 403
 
    db_functions.deleteReview(review_id)
    return jsonify({"message": "Review deleted successfully"}), 200

###TV show review routes

@app.route('/tv/show/<int:show_id>/reviews', methods=['GET'])
def get_tv_reviews(show_id):
    """
    Get all reviews for a TV show
    ---
    tags:
      - Reviews
    parameters:
      - name: show_id
        in: path
        type: integer
        required: true
        description: ID of the show to get reviews for
    responses:
      200:
        description: List of reviews as JSON
    """
    reviews = db_functions.getTvReviews(show_id)
    return jsonify(reviews)

@app.route('/tv/show/<int:show_id>/reviews', methods=['POST'])
def post_tv_review(show_id):
    """
    Create a review for a TV show
    ---
    tags:
      - Reviews
    parameters:
      - name: show_id
        in: path
        type: integer
        required: true
        description: ID of the show to review
      - name: reviewText
        in: formData
        type: string
        required: true
        description: The review text content
      - name: rating
        in: formData
        type: integer
        required: true
        description: Rating out of 10
    responses:
      200:
        description: Review created successfully
      400:
        description: Missing review text or rating
      401:
        description: Not logged in
      500:
        description: Server error
    """
    user_id = session.get('id')
    if not user_id:
      return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json()
    text = data.get('reviewText', '').strip()
    rating = data.get('rating')

    if not text or not rating:
        return jsonify({"status": "error", "message": "Review and rating are required"}), 400

    try:
        db_functions.createTvReview(text, user_id, show_id, int(rating))
        return jsonify({"status": "success", "message": "Review added!"})
    except Exception as e:
        print(f"TV Review Error: {e}")
        return jsonify({"status": "error", "message": "Failed to post review"}), 500

@app.route('/tv/review/<int:review_id>/delete', methods=['POST'])
def delete_tv_review(review_id):
    """
    Delete a TV show review - users can only delete their own, admins can delete any
    ---
    tags:
      - Reviews
    parameters:
      - name: review_id
        in: path
        type: integer
        required: true
        description: ID of the review to delete
    responses:
      200:
        description: Review deleted successfully
      401:
        description: Not logged in
      403:
        description: Review belongs to another user and requester is not admin
      404:
        description: Review not found
    """
    if 'id' not in session:
        return jsonify({"error": "You must be logged in to delete a review."}), 401

    review = db_functions.getTvReviewFromID(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    if review['userid'] != session['id'] and not session.get('is_admin'):
        return jsonify({"error": "You can only delete your own reviews"}), 403

    db_functions.deleteTvReview(review_id)
    return jsonify({"message": "Review deleted successfully"}), 200