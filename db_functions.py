from db import get_db
from flask import jsonify

#--- User functions ---

def getUserFromID(userID):
    db = get_db()
    user = db.execute("SELECT * FROM userTable WHERE userID = ?",(userID)).fetchone()
    return dict(user) if user else None

def getAllUsers():
    db = get_db()
    users = db.execute("SELECT * FROM userTable").fetchone()
    return jsonify([dict(user) for user in users])

def getUserFromEmail(email):
    db = get_db()
    user = db.execute("SELECT * FROM userTable WHERE email = ?",(email)).fetchone()
    return dict(user) if user else None

