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

    config.TRAKT_TOKEN = token_data["access_token"]

    # if user:
    db.update_user_tokens(
        config.UID,
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        token_expires=datetime.datetime.utcnow()
        + datetime.timedelta(seconds=token_data["expires_in"]),
    )
    return token_data
