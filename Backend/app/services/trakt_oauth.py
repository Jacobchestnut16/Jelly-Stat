# import time
# import requests
# from typing import Optional
# from app.utils import config
# from app.services.token_store import TokenStore
#
# BASE = "https://api.trakt.tv"
# AUTH_URL = "https://trakt.tv/oauth/authorize"
#
# store = TokenStore()
#
# def build_auth_url(state: str):
#     redirect = f"{config.APP_HOST}/auth/callback"
#     return (f"{AUTH_URL}?response_type=code&client_id={config.TRAKT_CLIENT_ID}"
#             f"&redirect_uri={redirect}&state={state}")
#
# def exchange_code_for_token(code: str) -> dict:
#     url = f"{BASE}/oauth/token"
#     payload = {
#         "code": code,
#         "client_id": config.TRAKT_CLIENT_ID,
#         "client_secret": config.TRAKT_CLIENT_SECRET,
#         "redirect_uri": f"{config.APP_HOST}/auth/callback",
#         "grant_type": "authorization_code"
#     }
#     resp = requests.post(url, json=payload, timeout=10)
#     resp.raise_for_status()
#     data = resp.json()
#     data["obtained_at"] = int(time.time())
#     store.save_token(data)
#     return data
#
# def refresh_token_if_needed() -> dict:
#     token = store.get_token()
#     if not token:
#         raise RuntimeError("no token")
#     expires_in = token.get("expires_in", 0)
#     obtained = token.get("obtained_at", 0)
#     if int(time.time()) < obtained + expires_in - 60:
#         return token
#     # refresh
#     url = f"{BASE}/oauth/token"
#     payload = {
#         "refresh_token": token["refresh_token"],
#         "client_id": config.TRAKT_CLIENT_ID,
#         "client_secret": config.TRAKT_CLIENT_SECRET,
#         "redirect_uri": f"{config.APP_HOST}/auth/callback",
#         "grant_type": "refresh_token"
#     }
#     resp = requests.post(url, json=payload, timeout=10)
#     resp.raise_for_status()
#     data = resp.json()
#     data["obtained_at"] = int(time.time())
#     store.save_token(data)
#     return data

import requests
import datetime
from app.utils import config
from app.utils import database as db

BASE_URL = "https://api.trakt.tv"
AUTH_URL = "https://trakt.tv/oauth/authorize"
TOKEN_URL = "https://api.trakt.tv/oauth/token"

def build_auth_url(state: str):
    return (
        f"{AUTH_URL}?response_type=code"
        f"&client_id={config.TRAKT_CLIENT_ID}"
        f"&redirect_uri={config.TRAKT_REDIRECT_URI}"
        f"&state={state}"
    )

def exchange_code_for_token(code: str):
    payload = {
        "code": code,
        "client_id": config.TRAKT_CLIENT_ID,
        "client_secret": config.TRAKT_CLIENT_SECRET,
        "redirect_uri": config.TRAKT_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    r = requests.post(TOKEN_URL, json=payload, timeout=10)
    r.raise_for_status()
    token_data = r.json()

    # trakt_id = get_trakt_user_id(token_data["access_token"])
    # user = db.get_user_by_trakt_id(trakt_id)



    # if user:
    db.update_user_tokens(
        config.UID,
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        token_expires=datetime.datetime.utcnow()
        + datetime.timedelta(seconds=token_data["expires_in"]),
    )
    # else:
    #     db.create_user(
    #         trakt_id=trakt_id,
    #         trakt_client_id=config.TRAKT_CLIENT_ID,
    #         trakt_client_secret=config.TRAKT_CLIENT_SECRET,
    #         access_token=token_data["access_token"],
    #         refresh_token=token_data.get("refresh_token"),
    #         token_expires=datetime.datetime.utcnow()
    #         + datetime.timedelta(seconds=token_data["expires_in"]),
    #     )
    return token_data

# def get_trakt_user_id(access_token: str):
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "trakt-api-version": "2",
#         "trakt-api-key": config.TRAKT_CLIENT_ID,
#     }
#     r = requests.get(f"{BASE_URL}/users/me", headers=headers, timeout=10)
#     r.raise_for_status()
#     return r.json()["ids"]["slug"]
