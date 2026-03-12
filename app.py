from flask import Flask
import db_functions
import db as database
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/test")
def test_display():
    try: 
        return db_functions.getAllUsers()
    except Exception as e:
        return str(e)

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

