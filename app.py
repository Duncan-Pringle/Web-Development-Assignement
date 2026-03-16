from flask import Flask
from flask import jsonify
import db_functions
import db as database
import os

app = Flask(__name__)

#This if statement is try to fix an issue when deploying where the page infinite loads until restart
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) #Default to 8000 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=False)

@app.route('/') #Base route for the home page "https://web-development-assignement.onrender.com/"
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


