from flask import g
import sqlite3

DATABASE = 'database\database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
    return db

def close_connection(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()



    

