import requests
from fastapi import HTTPException

BASE_URL = "https://api.trakt.tv"

def get_headers(trakt_token: str, trakt_client_id: str):
    if not trakt_client_id or not trakt_token:
        return None
    return {
        "Content-Type": "application/json",
        "trakt-api-key": trakt_client_id,
        "trakt-api-version": "2",
        "Authorization": f"Bearer {trakt_token}",
    }

def get_uath_headers(trakt_client_id: str):
    if not trakt_client_id:
        return None
    return {
        "Content-Type": "application/json",
        "trakt-api-key": trakt_client_id,
        "trakt-api-version": "2",
    }

def get_shows_noAuth(endpoint: str,trakt_client_id: str):
    headers = get_uath_headers(trakt_client_id)
    if not headers:
        raise HTTPException(401, "Unauthorized: missing access token or client ID")
    url = f"{BASE_URL}/shows/{endpoint}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(401, "Unauthorized: invalid trakt token")
    return resp.json()

def get_movies_noAuth(endpoint: str,trakt_client_id: str):
    headers = get_uath_headers(trakt_client_id)
    if not headers:
        raise HTTPException(401, "Unauthorized: missing access token or client ID")
    url = f"{BASE_URL}/movies/{endpoint}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(401, "Unauthorized: invalid trakt token")
    return resp.json()

def get_shows_oAuth(endpoint: str, trakt_token: str, trakt_client_id: str):
    headers = get_headers(trakt_token, trakt_client_id)
    if not headers:
        raise HTTPException(401, "Unauthorized: missing access token or client ID")
    url = f"{BASE_URL}/shows/{endpoint}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TRAKT SAYS: {resp.text}")
    return resp.json()

def get_movies_oAuth(endpoint: str, trakt_token: str, trakt_client_id: str):
    headers = get_headers(trakt_token, trakt_client_id)
    if not headers:
        raise HTTPException(401, "Unauthorized: missing access token or client ID")
    url = f"{BASE_URL}/movies/{endpoint}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TRAKT SAYS: {resp.text}")
    return resp.json()

def get_endpoint_oAuth(endpoint: str, trakt_token: str, trakt_client_id: str):
    if endpoint.startswith('/'):
        endpoint = endpoint[1:]
    headers = get_headers(trakt_token, trakt_client_id)
    if not headers:
        raise HTTPException(401, "Unauthorized: missing access token or client ID")
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TRAKT SAYS: {resp.text}")
    return resp.json()

def get_show_image_by_tmdb(tmdb_id: int, trakt_token: str, trakt_client_id: str):
    # https: // api.trakt.tv / search / id_type / id?type = movie
    url = f"{BASE_URL}/search/tmdb/{tmdb_id}?type=show"
    headers = get_headers(trakt_token, trakt_client_id)
    if not headers:
        raise HTTPException(401, "Unauthorized: no user signed in")
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TRAKT SAYS: {resp.text}")
    film_slug = resp.json()[0]['show']['ids']['slug']

    url = f"{BASE_URL}/shows/{film_slug}?extended=images"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TRAKT SAYS: {resp.text}")
    film_details = resp.json()

    images = {
        'backdrops': [{"file_path":film_details['images']['fanart'][0] if film_details['images']['fanart'][0] else None}],
        'posters': [{"file_path":film_details['images']['poster'][0] if film_details['images']['poster'][0] else None}],
        'logos': [{"file_path":film_details['images']['logo'][0] if film_details['images']['logo'][0] else None}]
    }

    # fanart -> backdrops
    # poster -> posters
    # logo -> logos
    return images

def get_movie_image_by_tmdb(tmdb_id: int, trakt_token: str, trakt_client_id: str):
    url = f"{BASE_URL}/search/tmdb/{tmdb_id}?type=movie"
    headers = get_headers(trakt_token, trakt_client_id)
    if not headers:
        raise HTTPException(401, "Unauthorized: no user signed in")
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TRAKT SAYS: {resp.text}")
    film_slug = resp.json()[0]['movie']['ids']['slug']

    url = f"{BASE_URL}/movies/{film_slug}?extended=images"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TRAKT SAYS: {resp.text}")
    film_details = resp.json()

    images = {
        'backdrops': [{"file_path":film_details['images']['fanart'][0] if film_details['images']['fanart'][0] else None}],
        'posters': [{"file_path":film_details['images']['poster'][0] if film_details['images']['poster'][0] else None}],
        'logos': [{"file_path":film_details['images']['logo'][0] if film_details['images']['logo'][0] else None}]
    }
    # fanart -> backdrops
    # poster -> posters
    # logo -> logos
    return images

def retrieve_settings(trakt_token: str, trakt_client_id: str):
    headers = get_headers(trakt_token, trakt_client_id)
    if not headers:
        raise HTTPException(401, "Unauthorized: missing access token or client ID")
    url = f"{BASE_URL}/users/settings"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TRAKT SAYS: {resp.text}")
    return resp.json()

def sync_history(trakt_token: str, trakt_client_id: str):
    settings = retrieve_settings(trakt_token, trakt_client_id)
    if not settings:
        raise HTTPException(404, "Not Found: could not retrieve user settings")
    url = f"{BASE_URL}/sync/history/{settings['user']['ids']['slug']}"
    headers = get_headers(trakt_token, trakt_client_id)
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"TRAKT SAYS: {resp.text}")
    return resp.json()
