import db as database
from flask import jsonify

#--- User functions ---

def getUserFromID(userID):
    db = database.get_db()
    user = db.execute("SELECT * FROM userTable WHERE userID = ?",(userID,)).fetchone()
    return dict(user) if user else None

def getAllUsers():
    db = database.get_db()
    users = db.execute("SELECT * FROM userTable").fetchall()
    return jsonify([dict(user) for user in users])

def getUserFromEmail(email):
    db = database.get_db()
    user = db.execute("SELECT * FROM userTable WHERE email = ?",(email,)).fetchone()
    return dict(user) if user else None

