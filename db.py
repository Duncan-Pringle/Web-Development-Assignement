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


#Function to handle all database queries 
#(SQL QUERY, params like userID etc, false if fetching multiple items, commit if you want changes to be saved in the DB)
#Returns none if no data found
def query_db(query, params=None, fetchone=False, commit=False):
    database = get_db()
    cur = database.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cur.execute(query, params)
        result = None

        if query.strip().lower().startswith("select"):
            if fetchone:
                result = cur.fetchone()
            else:
                result = cur.fetchall()

        if commit:
            database.commit()

        return result
    
    except Exception as e:
        database.rollback()
        raise e

    finally:
        cur.close()


def close_connection(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()







    

