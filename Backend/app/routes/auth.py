# from __future__ import annotations
#
# from idlelib.query import Query
#
# from fastapi import APIRouter, Request, HTTPException
# from fastapi.responses import RedirectResponse
# from app.services import trakt_oauth
#
# router = APIRouter()
#
# @router.get("/login")
# def login(state: str = "state"):
#     url = trakt_oauth.build_auth_url(state)
#     return RedirectResponse(url)
#
# @router.get("/callback")
# def callback(request: Request, code: str = None, state: str = None):
#     if not code:
#         raise HTTPException(status_code=400, detail="missing code")
#     try:
#         token = trakt_oauth.exchange_code_for_token(code)
#     except Exception as exc:
#         raise HTTPException(status_code=502, detail=str(exc))
#     return {"status": "ok", "token": token}
#
# @router.get("/token")
# # def token():
#     # token = trakt_oauth.refresh_token_if_needed()
#     # return token
# def token(trakt_id: str | None = Query(None, description="Trakt id or slug of the user")):
#     try:
#         token = trakt_oauth.get_token_for_user_or_first(trakt_id)
#     except LookupError as exc:
#         raise HTTPException(status_code=404, detail=str(exc))
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=str(exc))
#     return token
from __future__ import annotations

from datetime import time, datetime

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.services import trakt_oauth
from app.utils.database import create_user, authUser

from app.utils import config

router = APIRouter()

@router.get("/signin")
def signin(username: str, password: str):
    p = authUser(username)
    print(p)
    if not p or password != p['pass']:
        raise HTTPException(status_code=401, detail="Username or password is incorrect")

    config.TRAKT_CLIENT_ID = p['trakt_client_id']
    config.TRAKT_CLIENT_SECRET = p['trakt_client_secret']

    config.TRAKT_TOKEN = p['access_token']

    config.USERNAME = username
    config.UID = p['id']

    needs_refreshed_or_login = False if config.TRAKT_TOKEN else True

    # if datetime.now() >= p['token_expires']:
    #     needs_refreshed_or_login = True

    if needs_refreshed_or_login:
        return {"id": p['id'], "redirect": f"http://localhost:3001/auth/login"}

    return {"id": p['id']}

@router.get("/register")
def register(username,password,client_id,client_secret):
    create_user(username=username,password=password,trakt_client_id=client_id,trakt_client_secret=client_secret)

@router.get("/login")
def login(state: str = "state"):
    return RedirectResponse(trakt_oauth.build_auth_url(state))

@router.get("/callback")
def callback(code: str | None = None, state: str | None = None):
    if not code:
        raise HTTPException(status_code=400, detail="missing code")
    try:
        trakt_oauth.exchange_code_for_token(code)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return RedirectResponse("/")
