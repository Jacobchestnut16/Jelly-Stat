import requests
import datetime

BASE_URL = "https://api.trakt.tv"
AUTH_URL = "https://trakt.tv/oauth/authorize"
TOKEN_URL = "https://api.trakt.tv/oauth/token"


def build_auth_url(client_id: str, redirect_uri: str, state: str):
    return (
        f"{AUTH_URL}?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
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

    r = requests.post(TOKEN_URL, json=payload)
    r.raise_for_status()

    data = r.json()
    data["expires_at"] = datetime.datetime.utcnow().timestamp() + data["expires_in"]
    return data
