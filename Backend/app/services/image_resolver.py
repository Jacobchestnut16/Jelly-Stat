import datetime
from app.utils.database import (
    get_film,
    add_film,
    lookup_film_image,
    add_film_image
)
from app.services.tmdb_api import (
    get_movie_image,
    get_show_image
)

TTL_DAYS = 45

def resolve_images(tmdb_id: int, content_type: str, tmdb_token: str, trakt_token: str, trakt_client_id: str):
    """
    One-call resolver. Ensures film exists.
    Reads cache.
    Refreshes if needed.
    Saves fresh values.
    Returns single poster/logo/backdrop set.
    """

    # Ensure film exists in DB
    film = get_film(tmdb_id)
    if not film:
        add_film(tmdb_id=tmdb_id)

    # Check cache
    cached = lookup_film_image(tmdb_id)
    if cached:
        age = datetime.datetime.now().date() - cached["entry_date"]
        if age.days < TTL_DAYS:
            return {
                "poster": cached["poster_url"],
                "logo": cached["logo_url"],
                "backdrop": cached["backdrop_url"]
            }

    # Fetch from TMDB
    if content_type == "movie":
        data = get_movie_image(tmdb_id, tmdb_token, trakt_token, trakt_client_id)
    else:
        data = get_show_image(tmdb_id, tmdb_token, trakt_token, trakt_client_id)

    posters = data.get("posters", [])
    logos = data.get("logos", [])
    backdrops = data.get("backdrops", [])

    poster = posters[0]["file_path"] if posters else None
    logo = logos[0]["file_path"] if logos else None
    backdrop = backdrops[0]["file_path"] if backdrops else None

    if poster[0] == "/":
        poster = poster

    # Save to DB (refresh)
    add_film_image(
        tmdb_id,
        poster_url=poster,
        logo_url=logo,
        backdrop_url=backdrop
    )

    return {
        "poster": poster,
        "logo": logo,
        "backdrop": backdrop
    }
