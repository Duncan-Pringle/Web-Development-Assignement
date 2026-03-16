from flask import g
import os
import psycopg2
import psycopg2.extras

#DATABASE = "database/database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(os.environ.get("INTERNAL_DATABASE_URL"),
        cursor_factory=psycopg2.extras.RealDictCursor)
    return db


#Function to handle read database queries (SELECT)
#(SQL QUERY, params like userID etc, false if fetching multiple items, commit if you want changes to be saved in the DB)
#Returns none if no data found
def query_db_read(query, params=None, fetchone=False):
    database = get_db()
    cur = database.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cur.execute(query, params)

        if fetchone:
            return cur.fetchone()

        return cur.fetchall()

    finally:
        cur.close()

#Function to handle read database queries (INSERT, UPDATE, DELETE)
def query_db_write(query, params=None):
    database = get_db()
    cur = database.cursor()

    try:
        cur.execute(query, params)
        database.commit()

    except Exception:
        database.rollback()
        raise

    finally:
        cur.close()


def close_connection(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()







    

