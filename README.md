# MovieHub – Web Development Assignment

## Overview

MovieHub is a full-stack web application that allows users to browse movies and TV shows, search content using the TMDb API, manage personal watchlists, and interact through user profiles and reviews.



## Features

* User authentication (signup/login with password hashing)
* Movie and TV show browsing using the TMDb API
* Search functionality
* Watchlist system (movies and TV shows)
* User profiles and settings
* Review system (movies and TV shows)
* Admin panel for managing users and content



## Technologies Used

* Frontend: HTML, CSS, JavaScript
* Backend: Python (Flask)
* Database: PostgreSQL
* External API: TMDb API
* Optional Deployment: Render



## Running the Project Locally

1. Clone the repository

git clone 

cd Web-Development-Assignment


2. Install dependencies

pip install -r requirements.txt


3. Set Environment Variables

The following environment variables are required to run the project:

TMDB_API=your_tmdb_api_key
INTERNAL_DATABASE_URL=your_database_connection_string
SALT=your_random_secure_string

Note: These values are not included in the repository for security reasons.


4. Database Setup

The database schema is provided in two SQL files:

creates.sql
tv_tables.sql

You must run BOTH files in your database before running the application.

These scripts will create all required tables including:

* usertable
* movie
* review
* watchlist
* genre
* movieGenres
* tvshow
* tv_watchlist

Running only one of these files may result in missing functionality or errors.


5. Run the application

python app.py


6. Open in browser

http://127.0.0.1:5000



## Running on Render (Optional)

The application can also be deployed using Render.

Required configuration:

Build Command:
pip install -r requirements.txt

Start Command:
python app.py

Environment Variables (must be set manually in Render):

TMDB_API
INTERNAL_DATABASE_URL
SALT



## API Documentation

Swagger UI is available when running the application and provides documentation for available API endpoints.

http://127.0.0.1:5000/apidocs


## Security Note

Sensitive credentials such as API keys, database URLs, and SALT values are not stored in this repository.

These must be configured manually when running the project.



## Walkthrough Video

A walkthrough video demonstrating the functionality of the application is included as part of the submission.



## Contributors

(Team D)
* Deen
* Declan
* Andrew
* Duncan


## Notes for Marker

* The project can be tested locally using the instructions above.
* Deployment is optional and may be demonstrated in the video.
* All required coursework features have been implemented.


