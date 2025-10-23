import requests
from app.utils import config

BASE_URL = "https://api.themoviedb.org/3"

def get_movie(movie_id: int):
    url = f"{BASE_URL}/movie/{movie_id}"
    headers = {"Authorization": f"Bearer {config.TMDB_API_KEY}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


# /tv/{series_id}/images
def get_show_image(movie_id: int):
    url = f"{BASE_URL}/tv/{movie_id}/images"
    headers = {"Authorization": f"Bearer {config.TMDB_API_KEY}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

# /movie/{series_id}/images
def get_movie_image(movie_id: int):
    url = f"{BASE_URL}/movie/{movie_id}/images"
    headers = {"Authorization": f"Bearer {config.TMDB_API_KEY}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()