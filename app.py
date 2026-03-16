from flask import Flask
from flask import jsonify
import db_functions
import db as database

app = Flask(__name__)

@app.route('/') #Base route for the home page "https://web-development-assignement.onrender.com/"
def hello_world():
    return 'Hello, World!'

@app.route('/test1') 
def testinserts():
    try:
        db_functions.createUser("username1","user1email@email.com","hashedpass1")
        db_functions.createUser("username2","user2email@email.com","hashedpass2")
        db_functions.createUser("username3","user3email@email.com","hashedpass3")
        db_functions.createMovie(550, "test title", "test description", "test_url", 2000, 
        [{"id": 18,"name": "Drama"},{"id": 53,"name": "Thriller"}], 8.9)
        db_functions.createLikedMovie(2, 550)
        db_functions.createReview("reviewText", 1, 550)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test2') 
def testselects():
        test = db_functions.getAllUsers()
        test.append(db_functions.getUserFromID(1))
        test.append(db_functions.getUserFromEmail("user2email@email.com"))
        test.append(db_functions.getEmailFromID(2))
        test.append(db_functions.getIDFromUsername("username3"))
        test.append(db_functions.getAllMovies())
        test.append(db_functions.getUserFromID(2))
        test.append(db_functions.getMovieReviews(550))
        test.append(db_functions.getUserReviews(1))
        test.append(db_functions.getReviewFromID(1))

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)


