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

def exchange_code_for_token(code, client_id, client_secret, redirect_uri):
    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    r = requests.post(TOKEN_URL, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()
