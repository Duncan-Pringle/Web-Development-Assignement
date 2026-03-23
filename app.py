from flask import Flask, redirect, request, render_template, session

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
    return render_template('index.html', username=username, featured_movie=popular_movies.get(0), popular_movies=popular_movies)
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
