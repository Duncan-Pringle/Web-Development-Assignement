from flask import Flask
import db_functions
import db as database
import os
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

