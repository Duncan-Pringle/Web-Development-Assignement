import os
import httpx

TMDB = "https://api.themoviedb.org/3"

#this is slightly different to what's on my local machine so it might be broke. This should get the api 
#read token from render and return results to us as a json, though that might be redundant as tmdb sends 
#everything as a json anyway
HEADERS = {
    "Authorization": f"Bearer {os.environ.get('TMDB_API')}",
    "accept": "application/json"
    }

#basic methods to call for api functionallity, I'll add more as needed

#getter methods

#these return a json with the following fields:
#poster_path - IMPORTANT - ONLY GIVES THE SUFFIX OF THE PATH, we can append this to https://image.tmdb.org/t/p/[size], where size is any of w92, w154, w185, w342, w500 or w700
#adult - a bool that tells you if the movie is pornographic or not
#overview 
#release_date
#genre_ids - notably these are just the internal tmdb id numbers for the genres, they're not descriptive but get_genres lets us update these 
#id
#original_title
#original_language
#title
#backdrop_path
#popularity
#vote count
#video#vote_average

#use this to get any movie by its id
#note to self - should be easy enough to make work with the database if we have things in local storage
async def TMDB_by_id(movie_id: int):
    async with httpx.AsyncClient() as client:
        movie = await client.get(f"{TMDB}/movie/{movie_id}", headers=HEADERS)
    if movie.status_code != 200:
        return {"error": f"Request failed with status {movie.status_code}"}
    return movie.json()


#other methods

#use this to get the key for translating the genre ids to english, it'll return us a very large list formatted like {"id": x, "name": "y"}, ...
async def get_genres():
    async with httpx.AsyncClient() as client:
        genrenames = await client.get(f"{TMDB}/genre/movie/list", headers=HEADERS)
    if genrenames.status_code != 200:
        return {"error": f"Request failed with status {genrenames.status_code}"}
    return genrenames.json()  

#use this to run a search on tmdb, need to explore this a bit more myself, but it returns a list of search results, the total hits and pages, and which page of search results we're on 
async def TMDB_search(query: str):
    async with httpx.AsyncClient() as client:
        search = await client.get(f"{TMDB}/search/movie", headers = HEADERS, params={"query": query})
    return search.json()


