from __future__ import annotations
from app.utils.database import create_user, authUser, get_selected_tmdb_key

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.services import trakt_oauth
from app.utils.session_manager import get_session, update_session, delete_session
from app.utils import database as db

from app.utils.session_manager import create_session

from app.utils import config

router = APIRouter()

@router.get("/signin")
def signin(username: str, password: str):
    p = authUser(username)
    if not p or password != p['pass']:
        raise HTTPException(status_code=401, detail="Username or password is incorrect")

    session_data = {
        "TRAKT_CLIENT_ID": p["trakt_client_id"],
        "TRAKT_CLIENT_SECRET": p["trakt_client_secret"],
        "TRAKT_TOKEN": p["access_token"],
        "TMDB_TOKEN": get_selected_tmdb_key(p["id"])["api_key"] if get_selected_tmdb_key(p["id"]) else None,
        "JELLYSEERR_TOKEN": p.get("jellyseerr_token"),
        "USERNAME": username,
        "UID": p["id"],
    }

    session_id = create_session(session_data)
    needs_trakt_login = session_data["TRAKT_TOKEN"] is None

    return {
        "session_id": session_id,
        "needs_trakt_login": needs_trakt_login,
        "redirect": f"http://localhost:3001/auth/login?session_id={session_id}" if needs_trakt_login else None
    }

@router.get("/validate")
def validate(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "invalid session")
    return {"valid": True}


@router.get("/register")
def register(username,password,client_id,client_secret):
    create_user(username=username,password=password,trakt_client_id=client_id,trakt_client_secret=client_secret)

@router.get("/logout")
def logout(session_id: str):
    # Delete the session from in-memory store
    delete_session(session_id)
    return {"message": "Logged out successfully"}

@router.get("/login")
def login(session_id: str, state: str = "state"):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "invalid session")

    auth_url = trakt_oauth.build_auth_url(
        client_id=session["TRAKT_CLIENT_ID"],
        redirect_uri="http://localhost:3001/auth/callback",
        state=session_id  # carry session here
    )
    return RedirectResponse(auth_url)



@router.get("/callback")
def callback(code: str, state: str):
    session = get_session(state)
    if not session:
        raise HTTPException(401, "invalid session")

    token_data = trakt_oauth.exchange_code_for_token(
        code,
        client_id=session["TRAKT_CLIENT_ID"],
        client_secret=session["TRAKT_CLIENT_SECRET"],
        redirect_uri="http://localhost:3001/auth/callback",
    )

    update_session(state, {"TRAKT_TOKEN": token_data["access_token"]})

    from datetime import datetime

    expires_ts = token_data["expires_at"]  # numeric
    expires_dt = datetime.fromtimestamp(expires_ts)  # real timestamp

    db.update_user_tokens(
        session["UID"],
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        token_expires=expires_dt,
    )

    return RedirectResponse("http://localhost:3000/")
