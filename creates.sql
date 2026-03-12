CREATE TABLE "userTable" (
	"userID"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"userLevel"	INTEGER NOT NULL DEFAULT 1,
	"hashedPass"	TEXT NOT NULL,
	PRIMARY KEY("userID" AUTOINCREMENT)
)

CREATE TABLE "movie" (
	"movieID"	INTEGER NOT NULL UNIQUE,
	"title"	TEXT NOT NULL,
	"description"	TEXT,
	"posterLink"	TEXT,
	PRIMARY KEY("movieID")
)

CREATE TABLE "review" (
	"reviewID"	INTEGER NOT NULL UNIQUE,
	"reviewText"	TEXT NOT NULL,
	"userID"	INTEGER NOT NULL,
	"movieID"	INTEGER NOT NULL,
	PRIMARY KEY("reviewID" AUTOINCREMENT)
)

CREATE TABLE "likedMovies" (
	"movieID"	INTEGER NOT NULL,
	"userID"	INTEGER NOT NULL,
	PRIMARY KEY("movieID","userID"),
	FOREIGN KEY("movieID") REFERENCES "movie"("movieID"),
	FOREIGN KEY("userID") REFERENCES "userTable"("userID")
)