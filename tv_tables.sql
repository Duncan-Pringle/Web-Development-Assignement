CREATE TABLE tvshow (
    showID INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    poster_url TEXT,
    first_air_date TEXT,
    rating DECIMAL
);

CREATE TABLE tv_watchlist (
    userID INTEGER REFERENCES usertable(userID) ON DELETE CASCADE,
    showID INTEGER REFERENCES tvshow(showID) ON DELETE CASCADE,
    PRIMARY KEY (userID, showID)
);