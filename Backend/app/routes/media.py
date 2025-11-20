from fastapi import APIRouter, Query, HTTPException
from app.services import trakt_api, tmdb_api
from app.services.image_resolver import resolve_images
from app.utils.session_manager import get_session

router = APIRouter()

@router.get("/trending/shows")
def trending_shows(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    trakt_token = session.get("TRAKT_TOKEN")
    trakt_client_id = session.get("TRAKT_CLIENT_ID")
    tmdb_token = session.get("TMDB_TOKEN")

    if not trakt_client_id:
        raise HTTPException(401, "Missing Trakt credentials in session")
    if not tmdb_token:
        raise HTTPException(401, "Missing TMDB token in session")

    shows = trakt_api.get_shows_noAuth('trending', trakt_client_id)
    for film in shows:
        try:
            tmdb_id = film["show"]["ids"]["tmdb"]
        except KeyError:
            print(f"ERROR NO KEY show: {film}")
            continue
        film["images"] = resolve_images(tmdb_id, "show", tmdb_token, trakt_token, trakt_client_id)
    return shows

@router.get("/trending/movies")
def trending_movies(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    trakt_token = session.get("TRAKT_TOKEN")
    trakt_client_id = session.get("TRAKT_CLIENT_ID")
    tmdb_token = session.get("TMDB_TOKEN")

    if not trakt_client_id:
        raise HTTPException(401, "Missing Trakt credentials in session")
    if not tmdb_token:
        raise HTTPException(401, "Missing TMDB token in session")

    movies = trakt_api.get_movies_noAuth('trending', trakt_client_id)
    for film in movies:
        try:
            tmdb_id = film["movie"]["ids"]["tmdb"]
        except KeyError:
            print(f"ERROR NO KEY movie: {film}")
            continue
        film["images"] = resolve_images(tmdb_id, "movie", tmdb_token, trakt_token, trakt_client_id)

    return movies

@router.get("/trending")
def trending_all(session_id: str = Query(...)):
    shows = trending_shows(session_id)
    movies = trending_movies(session_id)
    return {"shows": shows, "movies": movies}

@router.get("/recommended/shows")
def recommended_shows(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    trakt_token = session.get("TRAKT_TOKEN")
    trakt_client_id = session.get("TRAKT_CLIENT_ID")
    tmdb_token = session.get("TMDB_TOKEN")

    if not (trakt_token and trakt_client_id):
        raise HTTPException(401, "Missing Trakt credentials in session")
    if not tmdb_token:
        raise HTTPException(401, "Missing TMDB token in session")

    shows = trakt_api.get_endpoint_oAuth('recommendations/shows', trakt_token, trakt_client_id)
    for film in shows:
        tmdb_id = film["ids"]["tmdb"]
        film["images"] = resolve_images(tmdb_id, "show", tmdb_token, trakt_token, trakt_client_id)

    return shows

@router.get("/recommended/movies")
def recommended_movies(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    trakt_token = session.get("TRAKT_TOKEN")
    trakt_client_id = session.get("TRAKT_CLIENT_ID")
    tmdb_token = session.get("TMDB_TOKEN")

    if not (trakt_token and trakt_client_id):
        raise HTTPException(401, "Missing Trakt credentials in session")
    if not tmdb_token:
        raise HTTPException(401, "Missing TMDB token in session")

    movies = trakt_api.get_endpoint_oAuth('recommendations/movies', trakt_token, trakt_client_id)
    for film in movies:
        tmdb_id = film["ids"]["tmdb"]
        film["images"] = resolve_images(tmdb_id, "movie", tmdb_token, trakt_token, trakt_client_id)

    return movies

@router.get("/recommended")
def recommended_all(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    trakt_token = session.get("TRAKT_TOKEN")
    trakt_client_id = session.get("TRAKT_CLIENT_ID")
    tmdb_token = session.get("TMDB_TOKEN")

    if not (trakt_token and trakt_client_id):
        raise HTTPException(401, "Missing Trakt credentials in session")
    if not tmdb_token:
        raise HTTPException(401, "Missing TMDB token in session")

    movies = trakt_api.get_endpoint_oAuth('recommendations/movies', trakt_token, trakt_client_id)
    for film in movies:
        tmdb_id = film["ids"]["tmdb"]
        film["images"] = resolve_images(tmdb_id, "movie", tmdb_token, trakt_token, trakt_client_id)

    shows = trakt_api.get_endpoint_oAuth('recommendations/shows', trakt_token, trakt_client_id)
    for film in shows:
        tmdb_id = film["ids"]["tmdb"]
        film["images"] = resolve_images(tmdb_id, "show", tmdb_token, trakt_token, trakt_client_id)

    return {"shows": shows, "movies": movies}

@router.get("/movie/{tmdb_id}")
def movie_info(tmdb_id: int, session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")
    tmdb_token = session.get("TMDB_TOKEN")
    if not tmdb_token:
        raise HTTPException(401, "Missing TMDB token in session")
    return tmdb_api.get_movie(tmdb_id, tmdb_token)

@router.get("/show/{tmdb_id}")
def show_info(tmdb_id: int, session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")
    tmdb_token = session.get("TMDB_TOKEN")
    if not tmdb_token:
        raise HTTPException(401, "Missing TMDB token in session")
    return tmdb_api.get_show(tmdb_id, tmdb_token)
