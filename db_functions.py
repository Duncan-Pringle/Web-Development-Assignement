import db as database

# User Functions

def createUser(username, email, hashedPass):
    database.query_db_write(
        "INSERT INTO usertable (username, email, hashedPass) values (%s, %s, %s)",
        (username, email, hashedPass,)
    )

def getUserFromID(userID):
    return database.query_db_read(
        "SELECT * FROM usertable WHERE userID = %s",
        (userID,), fetchone=True
    )

def getAllUsers():
    return database.query_db_read("SELECT * FROM usertable",)

def getUserFromEmail(email):
    return database.query_db_read(
        "SELECT * FROM usertable WHERE email = %s",
        (email,), fetchone=True
    )

def getEmailFromID(userID):
    return database.query_db_read(
        "SELECT email FROM usertable WHERE userID = %s",
        (userID,), fetchone=True
    )

def getUsernameFromID(userID):
    return database.query_db_read(
        "SELECT username FROM usertable WHERE userID = %s",
        (userID,), fetchone=True
    )

def getIDFromUsername(username):
    return database.query_db_read(
        "SELECT userID FROM usertable WHERE username = %s",
        (username,), fetchone=True
    )

def getUserFromUsername(username):
    return database.query_db_read(
        "SELECT * FROM usertable WHERE username = %s",
        (username,), fetchone=True
    )

def setUsername(userID, username):
    database.query_db_write(
        "UPDATE usertable SET username = %s where userID = %s", (username, userID))

def setEmail(userID, email):
    database.query_db_write(
        "UPDATE usertable SET email = %s where userID = %s", (email, userID))

def setLevel(userID, userLevel):
    database.query_db_write(
        "UPDATE usertable SET userLevel = %s where userID = %s", (userLevel, userID))

def setPassword(userID, hashedPass):
    database.query_db_write(
        "UPDATE usertable SET hashedPass = %s where userID = %s", (hashedPass, userID))

def deleteUser(userID):
    database.query_db_write(
        "DELETE FROM usertable where userID = %s", (userID,))


# Movie Functions

def createMovie(movieID, title, description, poster_url, year, genres, rating):
    try:
        database.query_db_write(
            "INSERT INTO movie (movieID, title, description, poster_url, year, rating) values (%s, %s, %s, %s, %s, %s)",
            (movieID, title, description, poster_url, year, rating)
        )
    except Exception:
        pass  # already exists, skip

    for genre in genres:
        if isinstance(genre, dict):
            genreID   = genre["id"]
            genreName = genre["name"]
        else:
            continue
        database.query_db_write(
            "INSERT INTO genre (genreID, name) values (%s, %s) ON CONFLICT DO NOTHING",
            (genreID, genreName)
        )
        database.query_db_write(
            "INSERT INTO movieGenres (movieID, genreID) values (%s, %s) ON CONFLICT DO NOTHING",
            (movieID, genreID)
        )

def createLikedMovie(userID, movieID):
    database.query_db_write(
        "INSERT INTO likedmovies (userID, movieID) values (%s, %s)", (userID, movieID))

def getMovieFromID(movieID):
    return database.query_db_read(
        "SELECT * FROM movie WHERE movieID = %s", (movieID,), fetchone=True)

def getAllMovies():
    return database.query_db_read("SELECT * FROM movie")

def getMovieByTitle(title):
    return database.query_db_read(
        "SELECT * FROM movie WHERE title = %s", (title,), fetchone=True)

def getGenresForMovie(movieID):
    results = database.query_db_read("""
        SELECT g.name FROM genre g
        JOIN movieGenres mg ON g.genreID = mg.genreID
        WHERE mg.movieID = %s
    """, (movieID,))
    return [row['name'] for row in results] if results else []


# Movie Watchlist Functions

def createWatchlistMovie(userID, movieID):
    database.query_db_write(
        "INSERT INTO watchlist (userID, movieID) values (%s, %s)", (userID, movieID))

def deleteWatchlistMovie(userID, movieID):
    database.query_db_write(
        "DELETE FROM watchlist WHERE userID = %s AND movieID = %s", (userID, movieID))

def getUserWatchlist(userID):
    return database.query_db_read(
        "SELECT * FROM watchlist WHERE userID = %s", (userID,))

def checkWatchlist(userID, movieID):
    result = database.query_db_read(
        "SELECT 1 FROM watchlist WHERE userID = %s AND movieID = %s",
        (userID, movieID), fetchone=True
    )
    return result is not None

def getWatchlistMovieDetails(userID):
    return database.query_db_read(
        "SELECT m.* FROM movie m JOIN watchlist w ON m.movieID = w.movieID WHERE w.userID = %s",
        (userID,)
    )


# TV Show Functions

def getTVShowByID(showID):
    return database.query_db_read(
        "SELECT * FROM tvshow WHERE showID = %s", (showID,), fetchone=True)

def getTVShowByTitle(name):
    return database.query_db_read(
        "SELECT * FROM tvshow WHERE name = %s", (name,), fetchone=True)


# TV Watchlist Functions

def createTVWatchlist(userID, showID):
    database.query_db_write(
        "INSERT INTO tv_watchlist (userID, showID) values (%s, %s)", (userID, showID))

def deleteTVWatchlist(userID, showID):
    database.query_db_write(
        "DELETE FROM tv_watchlist WHERE userID = %s AND showID = %s", (userID, showID))

def checkTVWatchlist(userID, showID):
    result = database.query_db_read(
        "SELECT 1 FROM tv_watchlist WHERE userID = %s AND showID = %s",
        (userID, showID), fetchone=True
    )
    return result is not None

def getTVWatchlistDetails(userID):
    """Returns full tvshow rows for everything in a user's TV watchlist."""
    return database.query_db_read(
        "SELECT t.* FROM tvshow t JOIN tv_watchlist tw ON t.showID = tw.showID WHERE tw.userID = %s",
        (userID,)
    )


# Review Functions
def createMovieReview(reviewText, userID, movieID, rating):
    database.query_db_write(
        "INSERT INTO review (reviewText, userID, movieID, rating) values (%s, %s, %s, %s)",
        (reviewText,userID, movieID, rating)
    )
        

def deleteReview(reviewID):
    database.query_db_write(
        "DELETE FROM review WHERE reviewID = %s", (reviewID,))

def setReviewText(reviewID, text):
    database.query_db_write(
        "UPDATE review SET reviewText = %s where reviewID = %s", (text, reviewID))

def getUserReviews(userID):
    return database.query_db_read(
        "SELECT * FROM review WHERE userID = %s", (userID,))

def getMovieReviews(movieID):
    return database.query_db_read(
        "SELECT * FROM review WHERE movieID = %s", (movieID,))

def getReviewFromID(reviewID):
    return database.query_db_read(
        "SELECT * FROM review WHERE reviewID = %s", (reviewID,), fetchone=True)


# UserReports Functions

def createReportWithReview(reporter, reported, reviewID):
    database.query_db_write(
        "INSERT INTO userreports (reporter, reported, reviewid) values (%s, %s, %s)",
        (reporter, reported, reviewID))

def createReport(reporter, reported):
    database.query_db_write(
        "INSERT INTO userreports (reporter, reported) values (%s, %s)",
        (reporter, reported))

def deleteReportFromID(reportid):
    database.query_db_write(
        "DELETE FROM userreports WHERE reportid = %s", (reportid,))

def getAllUnhandledReports():
    return database.query_db_read(
        "SELECT * FROM userreports WHERE handled = false")

def handleReport(reportid):
    database.query_db_write(
        "UPDATE userreports SET handled = true WHERE reportid = %s", (reportid,))


# Debug / Dev Tools

def getEverything():
    tables = ["usertable", "movie", "genre", "likedmovies", "moviegenres",
              "review", "watchlist", "tv_watchlist", "tvshow", "userreports"]
    results = {}
    for table in tables:
        result = database.query_db_read(f"SELECT * FROM {table}")
        results[table] = [dict(row) for row in result] if result else []
    return results


#==========Tv Show Functions==========

#Inserts a show into the tvshow table, and uses the genres json to insert the genres
def createTVShow(showID, name, description, poster_url, first_air_date, genres, number_of_seasons, rating):


    database.query_db_write( #Inserts everything except for the genres   
        "INSERT INTO tvshow (showID, name, description, poster_url, first_air_date, number_of_seasons, rating) values (%s, %s, %s, %s, %s, %s, %s)",
        (showID, name, description, poster_url, first_air_date, number_of_seasons, rating)
    )                

# Genre Format example from TMDB ----- [{"id": 18,"name": "Drama"}, {"id": 53,"name": "Thriller"}]
    for genre in genres:
        genreID = genre["id"]
        genreName = genre["name"]
        #Insert into genre table
        database.query_db_write(
            "INSERT INTO tvgenre (tvgenreid, name) values (%s, %s) ON CONFLICT DO NOTHING", 
            (genreID, genreName)
        )
        #Insert into tvgenres join table
        database.query_db_write(
            "INSERT INTO tvgenres (showid, tvgenreid) values (%s, %s) ON CONFLICT DO NOTHING", 
            (showID, genreID)
        )
    db = database.get_db()
    db.commit() #Commit once after all genres are inserted

def getShowFromID(showID): #Returns 1 show from its showID

    return database.query_db_read(
        "SELECT * FROM tvshow WHERE showid = %s",
        (showID,),
        fetchone = True
    )

def getAllShows(): #Returns dictionary of all shows in the database
    return database.query_db_read("SELECT * FROM tvshow")

def getShowGenres(showID): #Returns dictionary of all genres for a tv show
    return database.query_db_read("SELECT * FROM tvgenres WHERE showid = %s", (showID,), fetchone = True)
    
# TV Review Functions
def createTvReview(reviewText, userID, showID, rating):
    database.query_db_write(
        "INSERT INTO showreview (reviewText, userID, showID, rating) values (%s, %s, %s, %s)",
        (reviewText, userID, showID, rating))

def deleteTvReview(reviewID):
    database.query_db_write(
        "DELETE FROM showreview WHERE reviewID = %s", (reviewID,))

def setTvReviewText(reviewID, text):
    database.query_db_write(
        "UPDATE showreview SET reviewText = %s where reviewID = %s", (text, reviewID))

def getUserTvReviews(userID):
    return database.query_db_read(
        "SELECT * FROM showreview WHERE userID = %s", (userID,))

def getTvReviews(showID):
    return database.query_db_read(
        "SELECT * FROM showreview WHERE showID = %s", (showID,))

def getTvReviewFromID(reviewID):
    return database.query_db_read(
        "SELECT * FROM showreview WHERE reviewID = %s", (reviewID,), fetchone=True)

def getRecentActivity(userID):
    return database.query_db_read(
        """
        /* 1. Movie Reviews */
        SELECT 
            r.timestamp, r.rating, r.reviewText, 'movie_review' AS type,
            m.title AS content_name, m.movieID AS content_id
        FROM review r
        JOIN movie m ON r.movieID = m.movieID
        WHERE r.userID = %s

        UNION ALL

        /* 2. Show Reviews */
        SELECT 
            sr.timestamp, sr.rating, sr.reviewText, 'show_review' AS type,
            s.title AS content_name, s.showID AS content_id
        FROM showreview sr
        JOIN show s ON sr.showID = s.showID
        WHERE sr.userID = %s

        UNION ALL

        /* 3. Watchlist Additions */
        SELECT 
            w.timestamp, NULL AS rating, NULL AS reviewText, 'watchlist' AS type,
            m.title AS content_name, m.movieID AS content_id
        FROM watchlist w
        JOIN movie m ON w.movieID = m.movieID
        WHERE w.userID = %s

        ORDER BY timestamp DESC LIMIT 3
        """,
        (userID, userID, userID)
    )