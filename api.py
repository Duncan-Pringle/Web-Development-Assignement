import os
import httpx

TMDB = "https://api.themoviedb.org/3"
TMDB_IMAGE = "https://image.tmdb.org/t/p/"

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

def TMDB_poster_url(poster_path, size="w342"):
    if not poster_path:
        return None
    return f"{TMDB_IMAGE}{size}{poster_path}"


# Movies 
def get_genres():
    r = httpx.get(f"{TMDB}/genre/movie/list", headers=HEADERS)
    if r.status_code != 200:
        return {"error": f"Request failed with status {r.status_code}"}
    return r.json()

def TMDB_search(query: str, page: int = 1):
    r = httpx.get(f"{TMDB}/search/movie", headers=HEADERS,
                  params={"query": query, "page": page})
    if r.status_code != 200:
        return {"error": f"Request failed with status {r.status_code}"}
    return r.json()

def TMDB_popular(page: int = 1):
    r = httpx.get(f"{TMDB}/movie/popular", headers=HEADERS,
                  params={"page": page})
    if r.status_code != 200:
        return {"error": f"Request failed with status {r.status_code}"}
    return r.json()

def TMDB_by_id(movie_id):
    r = httpx.get(f"{TMDB}/movie/{movie_id}", headers=HEADERS)
    if r.status_code != 200:
        return {"error": "Movie not found"}
    return r.json()

def TMDB_search_first(title):
    r = httpx.get(f"{TMDB}/search/movie", headers=HEADERS,
                  params={"query": title, "page": 1})
    if r.status_code == 200:
        results = r.json().get("results")
        return results[0] if results else None
    return None


#  TV Shows 
def TMDB_tv_popular(page: int = 1):
    """Returns a page of popular TV shows from TMDB."""
    r = httpx.get(f"{TMDB}/tv/popular", headers=HEADERS,
                  params={"page": page})
    if r.status_code != 200:
        return {"error": f"Request failed with status {r.status_code}"}
    return r.json()

def TMDB_tv_search(query: str, page: int = 1):
    """Search TV shows by name."""
    r = httpx.get(f"{TMDB}/search/tv", headers=HEADERS,
                  params={"query": query, "page": page})
    if r.status_code != 200:
        return {"error": f"Request failed with status {r.status_code}"}
    return r.json()

def TMDB_tv_by_id(tv_id):
    """Get full details for a single TV show by its TMDB id."""
    r = httpx.get(f"{TMDB}/tv/{tv_id}", headers=HEADERS)
    if r.status_code != 200:
        return {"error": "TV show not found"}
    return r.json()
