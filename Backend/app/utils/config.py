import logging
from dotenv import load_dotenv
import os


load_dotenv()

logger = logging.getLogger("app.config")

APP_HOST = os.getenv("APP_HOST", "http://localhost:3001")
DATABASE_URL = os.getenv("DATABASE_URL")

TRAKT_REDIRECT_URI = APP_HOST+'/auth/callback'


required = {
    "APP_HOST": APP_HOST,
}

missing = [k for k, v in required.items() if not v]
if missing:
    logger.warning("Missing config items: %s", ", ".join(missing))

if not DATABASE_URL:
    logger.warning("DATABASE_URL not set. Database operations will fail until this is provided.")

