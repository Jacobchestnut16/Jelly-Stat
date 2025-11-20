from fastapi import APIRouter, Query, HTTPException
from app.services import trakt_api, tmdb_api
from app.utils.session_manager import get_session

router = APIRouter()

@router.get("/history")
def sync_history(session_id: str = Query(...)):
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

    # Call sync_history with tokens
    ret = trakt_api.sync_history(trakt_token, trakt_client_id)

    # Add images using tmdb token
    for item in ret:
        if item['type'] == 'movie':
            tmdb_id = item['movie']['ids']['tmdb']
            item['images'] = tmdb_api.get_movie_image(tmdb_id, tmdb_token)
        elif item['type'] == 'episode':
            show_tmdb_id = item['show']['ids']['tmdb']
            season = item['episode']['season']
            number = item['episode']['number']
            item['images'] = tmdb_api.get_episode_image(show_tmdb_id, season, number, tmdb_token)

    return ret
