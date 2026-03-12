from flask import Flask
import db_functions
import db as database
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/test")
def test_display():
    return db_functions.getAllUsers()

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

