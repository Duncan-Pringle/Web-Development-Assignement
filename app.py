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
        db_functions.createReview("reviewText", 4, 550)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test2') 
def testselects():
        test = db_functions.getAllUsers()
        try:
            test.append(db_functions.getUserFromID(1))
        except Exception as e:
             print("Error getting user by ID:", e)
        test.append(db_functions.getUserFromEmail("user2email@email.com"))
        test.append(db_functions.getEmailFromID(2))
        test.append(db_functions.getIDFromUsername("username3"))
        test.append(db_functions.getAllMovies())
        test.append(db_functions.getUserFromID(2))
        test.append(db_functions.getMovieReviews(550))
        test.append(db_functions.getUserReviews(4))
        test.append(db_functions.getReviewFromID(1))

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)


