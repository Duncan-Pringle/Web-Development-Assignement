CREATE TABLE usertable (
    userID SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    userLevel INTEGER DEFAULT 1,
    hashedPass TEXT NOT NULL
);

CREATE TABLE movie (
    movieID INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    poster_url TEXT,
    year INTEGER,
    rating DECIMAL
);

CREATE TABLE review (
    reviewID SERIAL PRIMARY KEY,
    reviewText TEXT NOT NULL,
    userID INTEGER REFERENCES usertable(userID) ON DELETE CASCADE,
    movieID INTEGER REFERENCES movie(movieID) ON DELETE CASCADE
);

CREATE TABLE likedmovies (
    userID INTEGER REFERENCES usertable(userID) ON DELETE CASCADE,
    movieID INTEGER REFERENCES movie(movieID) ON DELETE CASCADE,
    PRIMARY KEY (userID, movieID)
);

CREATE TABLE watchlist (
    userID INTEGER REFERENCES usertable(userID) ON DELETE CASCADE,
    movieID INTEGER REFERENCES movie(movieID) ON DELETE CASCADE,
    PRIMARY KEY (userID, movieID)
);

CREATE TABLE genre (
    genreID INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE movieGenres (
    movieID INTEGER REFERENCES movie(movieID) ON DELETE CASCADE,
    genreID INTEGER REFERENCES genre(genreID) ON DELETE CASCADE,
    PRIMARY KEY (movieID, genreID)
);

CREATE TABLE userreports (
    reportID SERIAL PRIMARY KEY,
    reporter INTEGER REFERENCES usertable(userID),
    reported INTEGER REFERENCES usertable(userID),
    reviewID INTEGER REFERENCES review(reviewID),
    handled BOOLEAN DEFAULT FALSE
);