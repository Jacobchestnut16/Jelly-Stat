from fastapi import HTTPException
import requests

BASE_URL = "https://api.themoviedb.org/3"

def get_movie(movie_id: int, tmdb_token: str):
    if not tmdb_token:
        raise HTTPException(401, "No TMDB Key provided")
    url = f"{BASE_URL}/movie/{movie_id}"
    headers = {"Authorization": f"Bearer {tmdb_token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TMDB SAYS: {resp.text}")
    return resp.json()

def get_show(movie_id: int, tmdb_token: str):
    if not tmdb_token:
        raise HTTPException(401, "No TMDB Key provided")
    url = f"{BASE_URL}/tv/{movie_id}"
    headers = {"Authorization": f"Bearer {tmdb_token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TMDB SAYS: {resp.text}")
    return resp.json()

def get_show_image(movie_id: int, tmdb_token: str, trakt_token: str, trakt_client_id: str):
    if not tmdb_token:
        raise HTTPException(401, "No TMDB Key provided")
    url = f"{BASE_URL}/tv/{movie_id}/images"
    headers = {"Authorization": f"Bearer {tmdb_token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        if resp.status_code == 401:
            print("tmdb_token is invalid")
        if resp.status_code == 429:
            print("Too many requests")
        print(resp.text+". Trying a different Endpoint")
        from app.services.trakt_api import get_show_image_by_tmdb
        trakt = get_show_image_by_tmdb(movie_id, trakt_token, trakt_client_id)
        if trakt:
            return trakt
        raise HTTPException(resp.status_code, f"{resp.text}. Trying a different Endpoint")
    return resp.json()

def get_movie_image(movie_id: int, tmdb_token: str, trakt_token: str, trakt_client_id: str):
    if not tmdb_token:
        raise HTTPException(401, "No TMDB Key provided")
    url = f"{BASE_URL}/movie/{movie_id}/images"
    headers = {"Authorization": f"Bearer {tmdb_token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        if resp.status_code == 401:
            print("tmdb_token is invalid")
        if resp.status_code == 429:
            print("Too many requests")
        print(resp.text+". Trying a different Endpoint")
        from app.services.trakt_api import get_movie_image_by_tmdb
        trakt = get_movie_image_by_tmdb(movie_id, trakt_token, trakt_client_id)
        if trakt:
            return trakt
        raise HTTPException(resp.status_code, f"{resp.text}. Trying a different Endpoint")
    return resp.json()

def get_episode_image(series_id: int, season_number: int, episode_number: int, tmdb_token: str):
    if not tmdb_token:
        raise HTTPException(401, "No TMDB Key provided")
    url = f"{BASE_URL}/tv/{series_id}/season/{season_number}/episode/{episode_number}/images"
    headers = {"Authorization": f"Bearer {tmdb_token}"}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(resp.status_code, f"TMDB SAYS: {resp.text}")
        return resp.json()
    except Exception as e:
        print(e)
        return {}
