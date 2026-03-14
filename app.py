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
        test=db_functions.getAllUsers()
        test.append(db_functions.getUserFromID(1))
        test.append(db_functions.getUserFromEmail("username3@email.com"))
        test.append(db_functions.getEmailFromID(2))
        test.append(db_functions.getIDFromUsername("username1"))
        return jsonify(test)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)


