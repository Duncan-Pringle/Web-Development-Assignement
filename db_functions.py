import db as database

#==========User Functions==========

#Basic function for creating a user in the database
def createUser(username, email, hashedPass):
    db = database.get_db()
    cursor = db.execute("INSERT INTO userTable (username, email, hashedPass) values (?, ?, ?)",(username,email, hashedPass,))
    db.commit
    return cursor.lastrowid #Returns lastrowid so that you can create a user, and then immediately use their information without another select

#Gets
def getUserFromID(userID):
    db = database.get_db()
    user = db.execute("SELECT * FROM userTable WHERE userID = ?",(userID,)).fetchone()
    return dict(user) if user else None

def getAllUsers():
    db = database.get_db()
    users = db.execute("SELECT * FROM userTable").fetchall()
    return [dict(user) for user in users]

def getUserFromEmail(email):
    db = database.get_db()
    user = db.execute("SELECT * FROM userTable WHERE email = ?",(email,)).fetchone()
    return dict(user) if user else None

def getEmailFromID(userID):
    db = database.get_db()
    email = db.execute("SELECT email FROM userTable WHERE userID = ?",(userID,)).fetchone()
    return dict(email) if email else None

def getUsernameFromID(userID):
    db = database.get_db()
    username = db.execute("SELECT username FROM userTable WHERE userID = ?",(userID,)).fetchone()
    return dict(username) if username else None

def getIDFromUsername(username):
    db = database.get_db()
    userID = db.execute("SELECT userID FROM userTable WHERE username = ?",(username,)).fetchone()
    return dict(userID) if userID else None

#Sets
def setUsername(userID, username):
    db = database.get_db()
    db.execute("UPDATE userTable SET username = ? where userID = ?", (username, userID))
    db.commit

def setEmail(userID, email):
    db = database.get_db()
    db.execute("UPDATE userTable SET email = ? where userID = ?", (email, userID))
    db.commit

def setLevel(userID, userLevel): #Used to update userlevel (default 1 = regular user)
    db = database.get_db()
    db.execute("UPDATE userTable SET userLevel = ? where userID = ?", (userLevel, userID))
    db.commit

def setPassword(userID, hashedPass):
    db = database.get_db()
    db.execute("UPDATE userTable SET hashedPass = ? where userID = ?", (hashedPass, userID))
    db.commit

#Removes a user from the database
def deleteUser(userID):
    db = database.get_db()
    db.execute("DELETE FROM userTable where userID = ?", (userID))

#==========Movie Functions==========

#Inserts a movie into the movie table, and uses the genres json to insert the genres
def createMovie(movieID, title, description, poster_url, year, genres, rating):
    db = database.get_db()
    cursor = db.execute("INSERT INTO movie (movieID, title, description, poster_url, year, rating) values (?, ?, ?, ?, ?, ?)",
    (movieID, title, description, poster_url, year, rating)) #Inserts everything except for the genres                
    
    movieID = cursor.lastrowid
# Genre Format example from TMDB ----- [{"id": 18,"name": "Drama"}, {"id": 53,"name": "Thriller"}]
    for genre in genres:
        genreID = genre["id"]
        genreName = genre["name"]
        #Insert into genre table
        db.execute("INSERT OR IGNORE INTO genre (genreID, name) values (?, ?)", (genreID, genreName))
        #Insert into movieGenres join table
        db.execute("INSERT OR IGNORE INTO movieGenres (movieID, genreID) values (?, ?)", (movieID, genreID))
    db.commit

def createLikedMovie(userID, movieID):
    db = database.get_db()
    cursor = db.execute("INSERT INTO likedMovies (userID, movieID) values (?, ?)", (userID, movieID))
    db.commit
    return cursor.lastrowid
                      
#Gets
def getMovieFromID(movieID): #Returns 1 movie from its movieID
    db = database.get_db()
    movie = db.execute("SELECT * FROM movie WHERE movieID = ?",(movieID,)).fetchone()
    return dict(movie) if movie else None

def getAllMovies(): #Returns json of all movies in the database
    db = database.get_db()
    movies = db.execute("SELECT * FROM movie").fetchall()
    return [dict(movie) for movie in movies]


#==========Review Functions==========

def createReview(reviewText, userID, movieID):
    db = database.get_db()
    cursor = db.execute("INSERT INTO review (reviewText, userID, movieID) values (?, ?, ?)",(reviewText,userID, movieID,))
    db.commit
    return cursor.lastrowid

def deleteReview(reviewID):
    db = database.get_db()
    db.execute("DELETE FROM review WHERE reviewID = ?",(reviewID))
    db.commit
    
#Sets
def setReviewText(reviewID, text):
    db = database.get_db()
    cursor = db.execute("UPDATE review SET reviewText = ? where reviewID = ?", (text, reviewID))
    db.commit
    return cursor.lastrowid

    