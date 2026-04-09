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


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = api.TMDB_by_id(movie_id)

    if "error" in movie:
        return render_template("404.html"), 404

    movie["poster_url"] = api.TMDB_poster_url(movie.get("poster_path"))

    return render_template('movieDetails.html', movie=movie)


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


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()

    if not query:
        return render_template('index.html', popular_movies=[])

    results = api.TMDB_search(query)

    movies = []
    for m in results.get("results", []):
        movies.append({
            "id": m["id"],
            "title": m["title"],
            "poster_url": api.TMDB_poster_url(m.get("poster_path")),
            "description": m.get("overview"),
        })

    return render_template("index.html", popular_movies=movies)


@app.route('/tv')
def tv():
    return "TV Shows coming soon"


@app.route('/people')
def people():
    return "People page coming soon"


@app.route('/admin')
def admin():
    if 'id' not in session:
        return redirect('/login')

    if not session.get('is_admin'):
        return "Access denied", 403

    users = db_functions.getAllUsers()
    movies = db_functions.getAllMovies()

    return render_template("admin.html", users=users, movies=movies)


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


@app.route('/POPMOVIESNEEDSEDITED/popular')
def popular_movies():
    results = api.TMDB_popular()

    movies = []
    for m in results.get("results", []):
        movies.append({
            "id": m["id"],
            "title": m["title"],
            "poster_url": api.TMDB_poster_url(m.get("poster_path")),
        })

    return {"results": movies}


if __name__ == '__main__':
    app.run(debug=True)