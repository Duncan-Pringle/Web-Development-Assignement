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

def createTVShow(showID, title, description, poster_url, first_air_date, rating):
    """Save a TV show to the tvshow table. Silently skips if it already exists."""
    try:
        database.query_db_write(
            "INSERT INTO tvshow (showID, title, description, poster_url, first_air_date, rating) values (%s, %s, %s, %s, %s, %s)",
            (showID, title, description, poster_url, first_air_date, rating)
        )
    except Exception:
        pass  # already exists, skip

def getTVShowByID(showID):
    return database.query_db_read(
        "SELECT * FROM tvshow WHERE showID = %s", (showID,), fetchone=True)

def getTVShowByTitle(title):
    return database.query_db_read(
        "SELECT * FROM tvshow WHERE title = %s", (title,), fetchone=True)


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
def createReview(reviewText, userID, movieID):
    database.query_db_write(
        "INSERT INTO review (reviewText, userID, movieID) values (%s, %s, %s)",
        (reviewText, userID, movieID,))

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
