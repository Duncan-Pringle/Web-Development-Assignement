from flask import g
import os
import psycopg2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database", "database.db")
#DATABASE = "database/database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(os.environ.get("postgresql://webdevdb_6c33_user:dgC92LpOoSVQIQfpxH2kO3MHaVExmx1q@dpg-d6ru1t4hg0os73es0a90-a/webdevdb_6c33"),
        cursor_factory=psycopg2.extras.RealDictCursor)
    return db

def close_connection(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()







    

