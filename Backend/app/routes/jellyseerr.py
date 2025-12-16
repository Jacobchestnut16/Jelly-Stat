from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Literal
from app.services.jellyseerr.util import getEverything, appendNew, RequestURL
from app.services.jellyseerr.formatter import summarize_raw, generate_lookup_links
from app.utils.session_manager import get_session

router = APIRouter()

DATA_CACHE = None
ARCHIVED_DATA_CACHE = None


def get_data(url, key):
    global DATA_CACHE
    if DATA_CACHE is None:
        DATA_CACHE = getEverything(url,key)
    else:
        DATA_CACHE = appendNew(url,key,DATA_CACHE)
    return DATA_CACHE


def get_data_archived(url, key):
    global ARCHIVED_DATA_CACHE
    if ARCHIVED_DATA_CACHE is None:
        ARCHIVED_DATA_CACHE = getEverything(url,key,RequestURL.media)
    else:
        ARCHIVED_DATA_CACHE = appendNew(url,key,ARCHIVED_DATA_CACHE, RequestURL.media)
    return ARCHIVED_DATA_CACHE


def apply_filters(
    data,
    type_filter: Optional[str],
    owned_filter: Optional[str],
    title_filter: Optional[str],
    sort_key: Optional[str],
    order: str,
):
    for d in data:
        d["lookups"] = generate_lookup_links(d["title"])

    filtered = data

    if type_filter:
        filtered = [d for d in filtered if d["type"] == type_filter]

    if owned_filter:
        if owned_filter == "owned":
            filtered = [d for d in filtered if d["jellyfin_media_id"]]
        elif owned_filter == "unowned":
            filtered = [d for d in filtered if not d["jellyfin_media_id"]]

    if title_filter:
        title_filter = title_filter.lower()
        filtered = [d for d in filtered if title_filter in d["title"].lower()]

    if sort_key:
        reverse = order == "desc"
        if sort_key == "title":
            filtered = sorted(filtered, key=lambda d: d["title"].lower(), reverse=reverse)
        elif sort_key == "type":
            filtered = sorted(filtered, key=lambda d: d["type"], reverse=reverse)
        elif sort_key == "owned":
            filtered = sorted(filtered, key=lambda d: bool(d["jellyfin_media_id"]), reverse=reverse)

    summary = {
        "tv": len([d for d in data if d["type"] == "tv"]),
        "movies": len([d for d in data if d["type"] == "movie"]),
        "owned": len([d for d in data if d["jellyfin_media_id"]]),
        "unowned": len([d for d in data if not d["jellyfin_media_id"]]),
    }

    return filtered, summary

@router.get("/")
def list_media(
    session_id: str = Query(...),
    type: Optional[str] = Query(None),
    owned: Optional[Literal["owned", "unowned"]] = Query(None),
    title: Optional[str] = Query(None),
    sort: Optional[Literal["title", "type", "owned"]] = Query(None),
    order: Literal["asc", "desc"] = Query("asc"),
):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    jellyseerr_url = session.get("JELLYSEERR_URL")
    jellyseerr_key = session.get("JELLYSEERR_TOKEN")

    if not jellyseerr_url:
        raise HTTPException(401, "No URL provided")
    if not jellyseerr_key:
        raise HTTPException(401, "No token provided")

    data = get_data(jellyseerr_url, jellyseerr_key)
    filtered, summary = apply_filters(data, type, owned, title, sort, order)

    return {
        "count": len(filtered),
        "summary": summary,
        "results": filtered,
    }

@router.get("/archived")
def list_archived_media(
    session_id: str = Query(...),
    type: Optional[str] = Query(None),
    owned: Optional[Literal["owned", "unowned"]] = Query(None),
    title: Optional[str] = Query(None),
    sort: Optional[Literal["title", "type", "owned"]] = Query(None),
    order: Literal["asc", "desc"] = Query("asc"),
):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    jellyseerr_url = session.get("JELLYSEERR_URL")
    jellyseerr_key = session.get("JELLYSEERR_TOKEN")

    if not jellyseerr_url:
        raise HTTPException(401, "No URL provided")
    if not jellyseerr_key:
        raise HTTPException(401, "No token provided")

    data = get_data_archived(jellyseerr_url, jellyseerr_key)
    filtered, summary = apply_filters(data, type, owned, title, sort, order)

    return {
        "count": len(filtered),
        "summary": summary,
        "results": filtered,
    }

@router.get("/detail/{tmdb_id}")
def media_detail(
    tmdb_id: int,
    session_id: str = Query(...)
):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    jellyseerr_url = session.get("JELLYSEERR_URL")
    jellyseerr_key = session.get("JELLYSEERR_TOKEN")

    if not jellyseerr_url:
        raise HTTPException(401, "No URL provided")
    if not jellyseerr_key:
        raise HTTPException(401, "No token provided")

    data = get_data(jellyseerr_url, jellyseerr_key)
    match = next((d for d in data if d["tmdb_id"] == tmdb_id), None)

    if not match:
        raise HTTPException(status_code=404, detail="Not found")

    return match

@router.get("/raw/{tmdb_id}")
def view_raw(
    tmdb_id: int,
    session_id: str = Query(...)
):
    session = get_session(session_id)
    if not session:
        raise HTTPException(401, "Invalid session")

    jellyseerr_url = session.get("JELLYSEERR_URL")
    jellyseerr_key = session.get("JELLYSEERR_TOKEN")

    if not jellyseerr_url:
        raise HTTPException(401, "No URL provided")
    if not jellyseerr_key:
        raise HTTPException(401, "No token provided")

    data = get_data(jellyseerr_url, jellyseerr_key)
    match = next((d for d in data if d["tmdb_id"] == tmdb_id), None)

    if not match:
        data = get_data_archived(jellyseerr_url, jellyseerr_key)
        match = next((d for d in data if d["tmdb_id"] == tmdb_id), None)

    if not match:
        raise HTTPException(status_code=404, detail="Not found")

    summary, backdrop, poster = summarize_raw(
        match["raw-data"],
        match["raw-title-data"],
    )

    return {
        "tmdb_id": tmdb_id,
        "title": match["title"],
        "summary": summary,
        "images": {
            "poster": poster,
            "backdrop": backdrop,
        },
        "lookups": generate_lookup_links(match["title"]),
        "raw": match["raw-data"],
    }
