import db as database

#==========User Functions==========

#Basic function for creating a user in the database
def createUser(username, email, hashedPass):
    db = database.get_db()
    cursor = db.execute("INSERT INTO userTable (username, email, hashedPass) values (%s, %s, %s)",(username,email, hashedPass,))
    db.commit()
    return cursor.lastrowid #Returns lastrowid so that you can create a user, and then immediately use their information without another select

#Gets
def getUserFromID(userID):
    db = database.get_db()
    user = db.execute("SELECT * FROM userTable WHERE userID = %s",(userID,)).fetchone()
    return dict(user) if user else None

def getAllUsers():
    db = database.get_db()
    users = db.execute("SELECT * FROM userTable").fetchall()
    return [dict(user) for user in users]

def getUserFromEmail(email):
    db = database.get_db()
    user = db.execute("SELECT * FROM userTable WHERE email = %s",(email,)).fetchone()
    return dict(user) if user else None

def getEmailFromID(userID):
    db = database.get_db()
    email = db.execute("SELECT email FROM userTable WHERE userID = %s",(userID,)).fetchone()
    return dict(email) if email else None

def getUsernameFromID(userID):
    db = database.get_db()
    username = db.execute("SELECT username FROM userTable WHERE userID = %s",(userID,)).fetchone()
    return dict(username) if username else None

def getIDFromUsername(username):
    db = database.get_db()
    userID = db.execute("SELECT userID FROM userTable WHERE username = %s",(username,)).fetchone()
    return dict(userID) if userID else None
#function to get all user reviews is in review section further down vvvvv

#Sets
def setUsername(userID, username):
    db = database.get_db()
    db.execute("UPDATE userTable SET username = %s where userID = %s", (username, userID))
    db.commit()

def setEmail(userID, email):
    db = database.get_db()
    db.execute("UPDATE userTable SET email = %s where userID = %s", (email, userID))
    db.commit()

def setLevel(userID, userLevel): #Used to update userlevel (default 1 = regular user)
    db = database.get_db()
    db.execute("UPDATE userTable SET userLevel = %s where userID = %s", (userLevel, userID))
    db.commit()

def setPassword(userID, hashedPass):
    db = database.get_db()
    db.execute("UPDATE userTable SET hashedPass = %s where userID = %s", (hashedPass, userID))
    db.commit()

#Removes a user from the database
def deleteUser(userID):
    db = database.get_db()
    db.execute("DELETE FROM userTable where userID = %s", (userID))
    db.commit()
#==========Movie Functions==========

#Inserts a movie into the movie table, and uses the genres json to insert the genres
def createMovie(movieID, title, description, poster_url, year, genres, rating):
    db = database.get_db()
    cursor = db.execute("INSERT INTO movie (movieID, title, description, poster_url, year, rating) values (%s, %s, %s, %s, %s, %s)",
    (movieID, title, description, poster_url, year, rating)) #Inserts everything except for the genres                
    
# Genre Format example from TMDB ----- [{"id": 18,"name": "Drama"}, {"id": 53,"name": "Thriller"}]
    for genre in genres:
        genreID = genre["id"]
        genreName = genre["name"]
        #Insert into genre table
        db.execute("INSERT OR IGNORE INTO genre (genreID, name) values (%s, %s)", (genreID, genreName))
        #Insert into movieGenres join table
        db.execute("INSERT OR IGNORE INTO movieGenres (movieID, genreID) values (%s, %s)", (movieID, genreID))
    db.commit()

def createLikedMovie(userID, movieID):
    db = database.get_db()
    cursor = db.execute("INSERT INTO likedMovies (userID, movieID) values (%s, %s)", (userID, movieID))
    db.commit()
    return cursor.lastrowid
                      
#Gets
def getMovieFromID(movieID): #Returns 1 movie from its movieID
    db = database.get_db()
    movie = db.execute("SELECT * FROM movie WHERE movieID = %s",(movieID,)).fetchone()
    return dict(movie) if movie else None

def getAllMovies(): #Returns json of all movies in the database
    db = database.get_db()
    movies = db.execute("SELECT * FROM movie").fetchall()
    return [dict(movie) for movie in movies]


#==========Review Functions==========

def createReview(reviewText, userID, movieID):
    db = database.get_db()
    cursor = db.execute("INSERT INTO review (reviewText, userID, movieID) values (%s, %s, %s)",(reviewText,userID, movieID,))
    db.commit()
    return cursor.lastrowid

def deleteReview(reviewID):
    db = database.get_db()
    db.execute("DELETE FROM review WHERE reviewID = %s",(reviewID))
    db.commit()
    
#Sets
def setReviewText(reviewID, text):
    db = database.get_db()
    cursor = db.execute("UPDATE review SET reviewText = %s where reviewID = %s", (text, reviewID))
    db.commit()
    return cursor.lastrowid

#Gets
def getUserReviews(userID): #Returns all reviews created by a user
    db = database.get_db()
    reviews = db.execute("SELECT * FROM review WHERE userID = %s",(userID,)).fetchall()
    return [dict(review) for review in reviews]

def getMovieReviews(movieID): #Returns all reviews created by a user
    db = database.get_db()
    reviews = db.execute("SELECT * FROM review WHERE userID = %s",(userID,)).fetchall()
    return [dict(review) for review in reviews]

def getReviewFromID(reviewID): #Returns a review from a reviewID
    db = database.get_db()
    review = db.execute("SELECT * FROM review WHERE reviewID = %s",(reviewID,)).fetchone()
    return dict(review) if review else None



