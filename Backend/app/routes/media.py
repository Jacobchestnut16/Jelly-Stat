import os

from fastapi import APIRouter
from fastapi.routing import APIRoute
from app.services import trakt_api, tmdb_api

router = APIRouter()

@router.get("/trending")
def trending_all():
    shows = trakt_api.get_shows_noAuth('trending')
    movies = trending_movies()
    return {"shows": shows, "movies": movies}
@router.get("/trending/shows")
def trending_shows():
    return trakt_api.get_shows_noAuth('trending')
@router.get("/trending/movies")
def trending_movies():
    return trakt_api.get_movies_noAuth('trending')

@router.get("/movie/{tmdb_id}")
def movie_info(tmdb_id: int):
    return tmdb_api.get_movie(tmdb_id)

@router.get("/__routes", include_in_schema=False)
def media_routes():
    # if os.getenv("ENV", "development") != "development":
    #     return {"error": "not available in production"}
    routes = []
    for r in router.routes:
        if isinstance(r, APIRoute):
            routes.append({
                "path": r.path,              # router-local path
                "methods": sorted(list(r.methods or [])),
                "name": r.name,
                "status": "deprecated" if r.include_in_schema is False else "active"
            })
    return {"router": "media", "routes": routes}