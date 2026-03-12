from flask import Flask
import db_functions
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/test")
def test_display():
    db_functions.getAllUsers()

