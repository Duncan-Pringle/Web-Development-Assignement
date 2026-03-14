from flask import Flask
from flask import jsonify
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
        users =  db_functions.getAllUsers()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

