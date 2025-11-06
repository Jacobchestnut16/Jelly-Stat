from fastapi import APIRouter, HTTPException
from app.utils.ID import ID_TYPE
from app.services.tmdb_api import get_movie_image, get_show_image
from app.utils.config import DATABASE_URL
import datetime

router = APIRouter()

# Placeholder DB handler (replace later with SQLAlchemy/asyncpg)
def db_active():
    return bool(DATABASE_URL and DATABASE_URL.strip())

def get_cached_image(film_id, image_type):
    # TODO: implement real DB lookup
    pass

def cache_image(film_id):
    # TODO: implement DB insert/update
    pass

def id_type(id):
    try:
        int(id)
        return ID_TYPE.TMDB
    except ValueError:
        return ID_TYPE.Slug


def fetch_tmdb_image(content_type: str, film_id: int, image_key: str):
    """Grabs TMDB images directly from API."""
    if content_type == "movie":
        images = get_movie_image(film_id)
    elif content_type == "show":
        images = get_show_image(film_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid content type")

    if image_key not in images or not images[image_key]:
        raise HTTPException(status_code=404, detail=f"No {image_key} found for {content_type}")
    return images[image_key][0]["file_path"]


@router.get("/{image_type}")
def get_image(content_type: str, film_id: str, image_type: str):
    """
    Endpoint for retrieving images.
    Supports image_type: all, backdrop, logo, poster.
    """
    if id_type(film_id) != ID_TYPE.TMDB:
        raise HTTPException(status_code=402, detail="Invalid TMDB ID")

    film_id = int(film_id)

    # Attempt database lookup if DB active
    if db_active():
        cached = get_cached_image(film_id, image_type)
        if cached:
            age = datetime.datetime.now() - cached["timestamp"]
            if age.days < 45:
                return {"source": "cache", "url": cached["url"]}

    # DB inactive or cache expired → fall back to API
    if image_type == "all":
        result = get_movie_image(film_id) if content_type == "movie" else get_show_image(film_id)
        if db_active():
            cache_image(film_id, result)
        return {"source": "api", "data": result}

    url = fetch_tmdb_image(content_type, film_id, image_type + "s")

    if db_active():
        cache_image(film_id, image_type, url)

    return {"source": "api", "url": url}
