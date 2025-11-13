import logging
from dotenv import load_dotenv
import os


load_dotenv()

logger = logging.getLogger("app.config")

TRAKT_CLIENT_ID = os.getenv("TRAKT_CLIENT_ID")
TRAKT_CLIENT_SECRET = os.getenv("TRAKT_CLIENT_SECRET")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
APP_HOST = os.getenv("APP_HOST", "http://localhost:8000")
DATABASE_URL = os.getenv("DATABASE_URL")

TRAKT_REDIRECT_URI = APP_HOST+'/auth/callback'

TRAKT_TOKEN      = None
TMDB_TOKEN       = TMDB_API_KEY #Master Key
JELLYSEERR_TOKEN = None

USERNAME = None
UID      = None

required = {
    "APP_HOST": APP_HOST,
}

missing = [k for k, v in required.items() if not v]
if missing:
    logger.warning("Missing config items: %s", ", ".join(missing))

if not DATABASE_URL:
    logger.warning("DATABASE_URL not set. Database operations will fail until this is provided.")

