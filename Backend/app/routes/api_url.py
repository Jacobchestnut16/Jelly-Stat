from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Body
from app.utils.database import (
    get_jellyseerr_url,
    get_jellyseerr_urls,
    add_jellyseerr_url,
    select_jellyseerr_url,
    get_selected_jellyseerr_url,

    get_jellyfin_url,
    get_jellyfin_urls,
    add_jellyfin_url,
    select_jellyfin_url,
    get_selected_jellyfin_url,
)
from app.utils.session_manager import get_session, update_session

router = APIRouter()


# ------------
#  Jellyseerr
# ------------

@router.get("/jellyseerr/get")
def url_get_jellyseerr(id: int | None = Query(None)):
    if id is not None:
        data = get_jellyseerr_url(id)
        if not data:
            raise HTTPException(status_code=404, detail="Jellyseerr url not found")
        return data
    return get_jellyseerr_urls()

@router.get("/jellyseerr/get/selected")
def url_get_selected_jellyseerr(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    uid = session["UID"]
    data = get_selected_jellyseerr_url(uid)
    if not data:
        raise HTTPException(status_code=404, detail="No selected Jellyseerr url")
    return data

@router.post("/jellyseerr/add")
def url_add_jellyseerr(url: str = Body(..., embed=True)):
    add_jellyseerr_url(url)
    return {"message": "Jellyseerr key added"}

@router.post("/jellyseerr/select")
def url_select_jellyseerr(url_id: int = Body(..., embed=True), session_id: str = Body(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    uid = session["UID"]
    select_jellyseerr_url(uid, url_id)
    update_session(session_id, {"JELLYSEERR_URL": get_selected_jellyseerr_url(uid)["url"]})
    return {"message": "Jellyseerr URL selected"}


# ------------
#  Jellyfin
# ------------

@router.get("/jellyfin/get")
def url_get_jellyfin(id: int | None = Query(None)):
    if id is not None:
        data = get_jellyfin_url(id)
        if not data:
            raise HTTPException(status_code=404, detail="Jellyfin url not found")
        return data
    return get_jellyfin_urls()

@router.get("/jellyfin/get/selected")
def url_get_selected_jellyfin(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    uid = session["UID"]
    data = get_selected_jellyfin_url(uid)
    if not data:
        raise HTTPException(status_code=404, detail="No selected Jellyfin url")
    return data

@router.post("/jellyfin/add")
def url_add_jellyfin(url: str = Body(..., embed=True)):
    add_jellyfin_url(url)
    return {"message": "Jellyfin key added"}

@router.post("/jellyfin/select")
def url_select_jellyfin(url_id: int = Body(..., embed=True), session_id: str = Body(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    uid = session["UID"]
    select_jellyfin_url(uid, url_id)
    update_session(session_id, {"JELLYFIN_URL": get_selected_jellyfin_url(uid)["url"]})
    return {"message": "Jellyfin URL selected"}