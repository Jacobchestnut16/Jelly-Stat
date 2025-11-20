from fastapi import APIRouter, Query, HTTPException
from app.services import trakt_api
from app.utils.database import get_user_by_id
from app.utils.session_manager import get_session

router = APIRouter()

@router.get("/details")
def user_details(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    trakt_token = session.get("TRAKT_TOKEN")
    trakt_client_id = session.get("TRAKT_CLIENT_ID")

    if not (trakt_token and trakt_client_id):
        raise HTTPException(401, "Missing Trakt credentials in session")

    return trakt_api.retrieve_settings(trakt_token, trakt_client_id)

@router.get("/trakt_login_info")
def trakt_login_info(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    uid = session.get("UID")
    if not uid:
        raise HTTPException(401, "Missing user ID in session")

    ret = get_user_by_id(uid)
    if ret and 'pass' in ret:
        ret['pass'] = "*" * (len(ret['pass']) * 3)

    if ret and 'access_token' in ret:
        ret['access_token'] = "*" * (len(ret['access_token']) * 3)

    if ret and 'refresh_token' in ret:
        ret['refresh_token'] = "*" * (len(ret['refresh_token']) * 3)

    if ret and 'trakt_client_secret' in ret:
        ret['trakt_client_secret'] = "*" * (len(ret['trakt_client_secret']) * 3)

    return ret
