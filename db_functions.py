import db as database

#==========User Functions==========

#Basic function for creating a user in the database
def createUser(username, email, hashedPass):
    database.query_db(
        "INSERT INTO usertable (username, email, hashedPass) values (%s, %s, %s)",
        (username,email, hashedPass,),
        commit = True
    )

#Gets
def getUserFromID(userID):
    database.query_db(
        "SELECT * FROM usertable WHERE userID = %s",
        (userID,),
        fetchone = True
    )

def getAllUsers():
    database.query_db("SELECT * FROM usertable",)

def getUserFromEmail(email):
    database.query_db(
        "SELECT * FROM usertable WHERE email = %s",
        (email,),
        fetchone = True
    )


def getEmailFromID(userID):
    database.query_db(
        "SELECT email FROM usertable WHERE userID = %s",
        (userID,),
        fetchone = True
    )

def getUsernameFromID(userID):
    database.query_db(
        "SELECT username FROM usertable WHERE userID = %s",
        (userID,),
        fetchone = True
    )

def getIDFromUsername(username):
    database.query_db(
        "SELECT userID FROM usertable WHERE username = %s",
        (username,),
        fetchone = True
    )

#function to get all user reviews is in review section further down vvvvv

#Sets
def setUsername(userID, username):
    database.query_db(
        "UPDATE usertable SET username = %s where userID = %s",
        (username, userID),
        commit = True
    )

def setEmail(userID, email):
    database.query_db(
        "UPDATE usertable SET email = %s where userID = %s",
        (email, userID),
        commit = True
    )
   

def setLevel(userID, userLevel): #Used to update userlevel (default 1 = regular user)

    database.query_db(
        "UPDATE usertable SET userLevel = %s where userID = %s",
        (userLevel, userID),
        commit = True
    )

def setPassword(userID, hashedPass):
    database.query_db(
        "UPDATE usertable SET hashedPass = %s where userID = %s",
        (hashedPass, userID),
        commit = True
    )

#Removes a user from the database
def deleteUser(userID):
    database.query_db(
        "DELETE FROM usertable where userID = %s",
        (userID),
        commit = True)

#==========Movie Functions==========

#Inserts a movie into the movie table, and uses the genres json to insert the genres
def createMovie(movieID, title, description, poster_url, year, genres, rating):

    database.query_db( #Inserts everything except for the genres   
        "INSERT INTO movie (movieID, title, description, poster_url, year, rating) values (%s, %s, %s, %s, %s, %s)",
        (movieID, title, description, poster_url, year, rating),
        commit = True
    )                
    

# Genre Format example from TMDB ----- [{"id": 18,"name": "Drama"}, {"id": 53,"name": "Thriller"}]
    for genre in genres:
        genreID = genre["id"]
        genreName = genre["name"]
        #Insert into genre table
        database.query_db(
            "INSERT INTO genre (genreID, name) values (%s, %s) ON CONFLICT DO NOTHING", 
            (genreID, genreName),
        )
        #Insert into movieGenres join table
        database.query_db(
            "INSERT INTO movieGenres (movieID, genreID) values (%s, %s) ON CONFLICT DO NOTHING", 
            (movieID, genreID),
        )
    db = database.get_db()
    db.commit() #Commit once after all genres are inserted
    

def createLikedMovie(userID, movieID):
    database.query_db(
        "INSERT INTO likedmovies (userID, movieID) values (%s, %s)", 
        (userID, movieID),
        commit = True
    )

                      
#Gets
def getMovieFromID(movieID): #Returns 1 movie from its movieID

    database.query_db(
        "SELECT * FROM movie WHERE movieID = %s",
        (movieID,),
        fetchone = True
    )


def getAllMovies(): #Returns json of all movies in the database
    database.query_db("SELECT * FROM movie")

#==========Review Functions==========

def createReview(reviewText, userID, movieID):
    database.query_db(
        "INSERT INTO review (reviewText, userID, movieID) values (%s, %s, %s)",
        (reviewText,userID, movieID,),
        commit = True
    )

def deleteReview(reviewID):
    database.query_db(
        "DELETE FROM review WHERE reviewID = %s",
        (reviewID),
        commit = True
    )
    
#Sets
def setReviewText(reviewID, text):
    database.query_db(
        "UPDATE review SET reviewText = %s where reviewID = %s", 
        (text, reviewID),
        commit = True
    )


#Gets
def getUserReviews(userID): #Returns all reviews created by a user
    database.query_db(
        "SELECT * FROM review WHERE userID = %s",
        (userID,)
    )


def getMovieReviews(movieID): #Returns all reviews created by a user
    database.query_db(
        "SELECT * FROM review WHERE movieID = %s",
        (movieID,)
    )

def getReviewFromID(reviewID): #Returns a review from a reviewID
    database.query_db(
        "SELECT * FROM review WHERE reviewID = %s",
        (reviewID,),
        fetchone = True
    )




