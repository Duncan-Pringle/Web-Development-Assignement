from flask import Flask
from flask import jsonify
import db_functions
import db as database

app = Flask(__name__)

@app.route('/') #Base route for the home page "https://web-development-assignement.onrender.com/"
def hello_world():
    return 'Hello, World!'

@app.route("/test") #Route for test route "https://web-development-assignement.onrender.com/test"
def test_display():
    try: 
        test =  db_functions.getAllUsers()
        test.append(db_functions.getUserFromID(1))
        test.append(db_functions.getUserFromEmail("username3@email.com"))
        test.append(db_functions.getEmailFromID(2))
        test.append(db_functions.getIDFromUsername("username1"))
        db_functions.setUsername(2, "newusername2")
        db_functions.setEmail(2, "newemail2@email.com")
        db_functions.setLevel(2, 2)
        db_functions.setPassword(2, "newuserpassword2")
        db_functions.createMovie(550, "test title", "test description", "test_url", 2000, 
        [{"id": 18,"name": "Drama"},{"id": 53,"name": "Thriller"}], 8.9)
        db_functions.createLikedMovie(2, 550)
        test.append(db_functions.getAllMovies())
        db_functions.createReview("reviewText", 1, 550)
        return jsonify(test)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)


