import db as database

#==========User Functions==========

#Inserts a new user into the database, username & email must be unique in the database
def createUser(username, email, hashedPass):
    database.query_db_write(
        "INSERT INTO usertable (username, email, hashedPass) values (%s, %s, %s)",
        (username,email,hashedPass,)
    )

#Gets
def getUserFromID(userID):
    return database.query_db_read(
        "SELECT * FROM usertable WHERE userID = %s",
        (userID,),
        fetchone = True
    )

def getAllUsers():
    return database.query_db_read("SELECT * FROM usertable",)

def getUserFromEmail(email):
    return database.query_db_read(
        "SELECT * FROM usertable WHERE email = %s",
        (email,),
        fetchone = True
    )

def getEmailFromID(userID):
    return database.query_db_read(
        "SELECT email FROM usertable WHERE userID = %s",
        (userID,),
        fetchone = True
    )

def getUsernameFromID(userID):
    return database.query_db_read(
        "SELECT username FROM usertable WHERE userID = %s",
        (userID,),
        fetchone = True
    )

def getIDFromUsername(username):
    return database.query_db_read(
        "SELECT userID FROM usertable WHERE username = %s",
        (username,),
        fetchone = True
    )

def getUserFromUsername(username):
    return database.query_db_read(
        "SELECT * FROM usertable WHERE username = %s",
        (username,),
        fetchone = True
    )

#A function that returns all reviews made by a user is further down vvvvv

#Sets
def setUsername(userID, username):
    database.query_db_write(
        "UPDATE usertable SET username = %s where userID = %s",
        (username, userID)
    )

def setEmail(userID, email):
    database.query_db_write(
        "UPDATE usertable SET email = %s where userID = %s",
        (email, userID)
    )

def setLevel(userID, userLevel): #Used to update userlevel (default 1 = regular user)

    database.query_db_write(
        "UPDATE usertable SET userLevel = %s where userID = %s",
        (userLevel, userID)
    )

def setPassword(userID, hashedPass):
    database.query_db_write(
        "UPDATE usertable SET hashedPass = %s where userID = %s",
        (hashedPass, userID)
    )

#Removes a user from the database, database will cascade reviews and likedMovies
def deleteUser(userID):
    database.query_db_write(
        "DELETE FROM usertable where userID = %s",
        (userID,)
    )

#==========Movie Functions==========

#Inserts a movie into the movie table, and uses the genres json to insert the genres
#(movieID - int, title - text/string, description - text/string, poster_url - text/string)
#(year - int, genres - json, rating - decimal)
def createMovie(movieID, title, description, poster_url, year, genres, rating):

    database.query_db_write( #Inserts everything except for the genres   
        "INSERT INTO movie (movieID, title, description, poster_url, year, rating) values (%s, %s, %s, %s, %s, %s)",
        (movieID, title, description, poster_url, year, rating)
    )                

# Genre Format example from TMDB ----- [{"id": 18,"name": "Drama"}, {"id": 53,"name": "Thriller"}]
    for genre in genres:
        genreID = genre["id"]
        genreName = genre["name"]
        #Insert into genre table
        database.query_db_write(
            "INSERT INTO genre (genreID, name) values (%s, %s) ON CONFLICT DO NOTHING", 
            (genreID, genreName)
        )
        #Insert into movieGenres join table
        database.query_db_write(
            "INSERT INTO movieGenres (movieID, genreID) values (%s, %s) ON CONFLICT DO NOTHING", 
            (movieID, genreID)
        )
    db = database.get_db()
    db.commit() #Commit once after all genres are inserted
    
def createLikedMovie(userID, movieID):
    database.query_db_write(
        "INSERT INTO likedmovies (userID, movieID) values (%s, %s)", 
        (userID, movieID)
    )
                
#Gets
def getMovieFromID(movieID): #Returns 1 movie from its movieID

    return database.query_db_read(
        "SELECT * FROM movie WHERE movieID = %s",
        (movieID,),
        fetchone = True
    )

def getAllMovies(): #Returns dictionary of all movies in the database
    return database.query_db_read("SELECT * FROM movie")

#==========Review Functions==========

def createReview(reviewText, userID, movieID):
    database.query_db_write(
        "INSERT INTO review (reviewText, userID, movieID) values (%s, %s, %s)",
        (reviewText,userID, movieID,)
    )

def deleteReview(reviewID):
    database.query_db_write(
        "DELETE FROM review WHERE reviewID = %s",
        (reviewID)
    )
    
#Sets
def setReviewText(reviewID, text):
    database.query_db_write(
        "UPDATE review SET reviewText = %s where reviewID = %s", 
        (text, reviewID)
    )

#Gets
def getUserReviews(userID): #Returns all reviews created by a user
    return database.query_db_read(
        "SELECT * FROM review WHERE userID = %s",
        (userID,)
    )

def getMovieReviews(movieID): #Returns all reviews created by a user
    return database.query_db_read(
        "SELECT * FROM review WHERE movieID = %s",
        (movieID,)
    )

def getReviewFromID(reviewID): #Returns a review from a reviewID
    return database.query_db_read(
        "SELECT * FROM review WHERE reviewID = %s",
        (reviewID,),
        fetchone = True
    )




#======================================================
#GET EVERYTHING FROM THE DATABASE FUNCTION DELETE LATER
#======================================================

def getEverything():
    tables = ["usertable", "movie", "genre", "likedmovies", "moviegenres", "review", "watchlist", "userreports"]
    results = {}

    for table in tables:
        result = database.query_db_read(f"SELECT * FROM {table}")
        
        # Convert the list of RealDictRows into a list of regular dicts
        if result:
            results[table] = [dict(row) for row in result]
        else:
            results[table] = [] # Keep it as an empty list if no data

    return results

#=========watchlist functions===========

def createWatchlistMovie(userID, movieID): #Inserts a value into the watchlist, also has a timestamp
    database.query_db_write(
        "INSERT INTO watchlist (userID, movieID) values (%s, %s)", 
        (userID, movieID)
    )

def deleteWatchlistMovie(userID, movieID):
    database.query_db_write(
        "DELETE FROM watchlist WHERE userID = %s AND movieID = %s",
        (userID, movieID)
    )

def getUserWatchlist(userID):
    return database.query_db_read(
        "SELECT * FROM watchlist WHERE userID = %s",
        (userID,)
    )

#=========userreports functions===========

def createReportWithReview(reporter, reported, reviewID): #Creates a report from 2 userid's with a reviewID
    database.query_db_write(
        "INSERT INTO userreports (reporter, reported, reviewid) values (%s, %s, %s)", 
        (reporter, reported, reviewID)
    )

def createReport(reporter, reported): #Creates a report from 2 userid's
    database.query_db_write(
        "INSERT INTO userreports (reporter, reported) values (%s, %s)", 
        (reporter, reported)
    )

def deleteReportFromID(reportid):
    database.query_db_write(
        "DELETE FROM userreports WHERE reportid = %s",
        (reportid)
    )

def getAllUnhandledReports(): #Returns everything from the userreports table where handled = false
    return database.query_db_read(
        "SELECT * FROM userreports WHERE handled = false"
        )

def handleReport(reportid): #Changes the "handled" variable from false to true in a report
    database.query_db_write("UPDATE userreports SET handled = true WHERE reportid = %s", (reportid))

#declan db code (might break)]
# look up movies by name instead of ID
def getMovieByTitle(title):
    return database.query_db_read(
        "SELECT * FROM movie WHERE title = %s",
        (title,),
        fetchone=True
    )

# get the actual genre names for a movie
def getGenresForMovie(movieID):
    query = """
        SELECT g.name 
        FROM genre g
        JOIN movieGenres mg ON g.genreID = mg.genreID
        WHERE mg.movieID = %s
    """
    results = database.query_db_read(query, (movieID,))
    # Convert list of dicts/rows to a simple list of strings: ['Action', 'Comedy']
    return [row['name'] for row in results] if results else []
    
def checkWatchlist(userID, movieID):
#Returns True if the movie is in the user's watchlist, False otherwise
    result = database.query_db_read(
        "SELECT 1 FROM watchlist WHERE userID = %s AND movieID = %s",
        (userID, movieID),
        fetchone=True
    )
    return result is not None