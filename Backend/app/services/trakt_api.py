import urllib
from http.client import HTTPException

import requests
from app.utils import config
from app.routes.auth import token
from app.services import tmdb_api


BASE_URL = "https://api.trakt.tv"

try:
    token = token()
except RuntimeError:
    token = None


HEADERS = {
    "Content-Type": "application/json",
    "trakt-api-key": config.TRAKT_CLIENT_ID,
    "trakt-api-version": "2"
}

if token and token.get("access_token"):
    AUTH_HEADERS = {
        "Content-Type": "application/json",
        "trakt-api-key": config.TRAKT_CLIENT_ID,
        "trakt-api-version": "2",
        "Authorization": f"Bearer {token['access_token']}",
    }


def get_trending_shows():
    url = f"{BASE_URL}/shows/trending"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def get_shows_noAuth(endpoint=""):
    url = f"{BASE_URL}/shows/{endpoint}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    ret_val = resp.json()
    for film in ret_val:
        tmdb_id = film["show"]["ids"]["tmdb"]
        film["show"]["images"] = tmdb_api.get_show_image(tmdb_id)
    return ret_val


def get_shows_oAuth(endpoint=""):
    if not token or not token.get("access_token"):
        raise HTTPException(status_code=401, detail="Unauthorized: missing access token")
    url = f"{BASE_URL}/shows/{endpoint}"
    resp = requests.get(url, headers=AUTH_HEADERS)
    resp.raise_for_status()
    return resp.json()

def get_movies_noAuth(endpoint=""):
    url = f"{BASE_URL}/movies/{endpoint}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    ret_val = resp.json()
    for film in ret_val:
        tmdb_id = film["movie"]["ids"]["tmdb"]
        film["movie"]["images"] = tmdb_api.get_movie_image(tmdb_id)
    return ret_val


def get_movies_oAuth(endpoint=""):
    if not token or not token.get("access_token"):
        raise HTTPException(status_code=401, detail="Unauthorized: missing access token")
    url = f"{BASE_URL}/movies/{endpoint}"
    resp = requests.get(url, headers=AUTH_HEADERS)
    resp.raise_for_status()
    return resp.json()

def retrieve_settings():
    if not token or not token.get("access_token"):
        raise HTTPException(status_code=401, detail="Unauthorized: missing access token")
    url = f"{BASE_URL}/users/settings"
    resp = requests.get(url, headers=AUTH_HEADERS)
    resp.raise_for_status()
    return resp.json()

def sync_history():
    if not token or not token.get("access_token"):
        raise HTTPException(status_code=401, detail="Unauthroized: missing access token")
    settings = retrieve_settings()
    if not settings:
        raise HTTPException(status_code=404, detail="Not Found: could not retrive user setttings eithir there is no user or url provided was incorrect")
    url = f"{BASE_URL}/sync/history/{settings['user']['ids']['slug']}"
    resp = requests.get(url, headers=AUTH_HEADERS)
    resp.raise_for_status()
    return resp.json()