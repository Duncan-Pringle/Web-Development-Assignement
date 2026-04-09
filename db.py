from flask import g
import os
import psycopg2
import psycopg2.extras

#DATABASE = "database/database.db"

#Function that returns a connection to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(os.environ.get("INTERNAL_DATABASE_URL"),
        cursor_factory=psycopg2.extras.RealDictCursor)
    return db


#Function to handle read database queries (SELECT)
#Inputs - (query - SQL query i.e "insert into ? where etc", params - what the ? in the sql query are i.e usertable)
#Inputs - (fetchone - tells the function if you want one row or all rows)
#Returns null if no rows are found
def query_db_read(query, params=None, fetchone=False):
    database = get_db() #Gets the db connection
    cur = database.cursor(cursor_factory=psycopg2.extras.RealDictCursor) 
    #gets the cursor "psycopg2.extras.RealDictCursor just returns the values in a dictionary rather than list"

    try:
        cur.execute(query, params) #Selects the data in query

        if fetchone: #Fetches the selected data
            return cur.fetchone()

        return cur.fetchall()

    finally: #Closes the cursor
        cur.close()

#Function to handle read database queries (INSERT, UPDATE, DELETE)
#Inputs - (query - SQL query i.e "insert into ? where etc", params - what the ? in the sql query are i.e usertable)
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


#This may surprise you but it closes the DB connection
def close_connection(exception):
    db = g.pop("_database", None)
    if db is not None:
        db.close()







    

