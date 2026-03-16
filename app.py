from flask import Flask
from flask import jsonify
import db_functions
import db as database

app = Flask(__name__)

@app.route('/') #Base route for the home page "https://web-development-assignement.onrender.com/"
def hello_world():
    return 'Hello, World!'

@app.route('/test2') 
def testselects():

        try:
            test = db_functions.getAllUsers()
            test.append(db_functions.getUserFromID(1))
            test.append(db_functions.getUserFromEmail("user2email@email.com"))
            test.append(db_functions.getEmailFromID(2))
            test.append(db_functions.getIDFromUsername("username3"))
            test.append(db_functions.getAllMovies())
            test.append(db_functions.getUserFromID(2))
            test.append(db_functions.getMovieReviews(550))
            test.append(db_functions.getUserReviews(4))
            test.append(db_functions.getReviewFromID(1))
            return jsonify(test), 200
        except Exception as e:
             return jsonify({"error": str(e)}), 500

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)


