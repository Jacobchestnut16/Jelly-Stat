from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Body
from app.utils.database import (
    get_tmdb_key,
    get_tmdb_keys,
    add_tmdb_key,
    select_tmdb_key,
    get_selected_tmdb_key,
    get_jellyseerr_key,
    get_jellyseerr_keys,
    add_jellyseerr_key,
    select_jellyseerr_key,
    get_selected_jellyseerr_key,
)
from app.utils.session_manager import get_session, update_session

router = APIRouter()

# ------------
#  TMDB
# ------------

@router.get("/tmdb/get")
def api_get_tmdb_key(id: int | None = Query(None)):
    if id is not None:
        data = get_tmdb_key(id)
        if not data:
            raise HTTPException(status_code=404, detail="TMDB key not found")
        return data
    return get_tmdb_keys()

@router.get("/tmdb/get/selected")
def api_get_selected_tmdb_key(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    uid = session["UID"]
    data = get_selected_tmdb_key(uid)
    if not data:
        raise HTTPException(status_code=404, detail="No selected TMDB key")
    return data

@router.post("/tmdb/add")
def api_add_tmdb_key(api_key: str = Body(..., embed=True)):
    add_tmdb_key(api_key)
    return {"message": "TMDB key added"}

@router.post("/tmdb/select")
def api_select_tmdb_key(api_key_id: int = Body(..., embed=True), session_id: str = Body(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    uid = session["UID"]
    select_tmdb_key(uid, api_key_id)
    update_session(state, {"TMDB_TOKEN": get_selected_tmdb_key(uid)["api_key"]})
    return {"message": "TMDB key selected"}

# ------------
#  Jellyseerr
# ------------

@router.get("/jellyseerr/get")
def api_get_jellyseerr_key(id: int | None = Query(None)):
    if id is not None:
        data = get_jellyseerr_key(id)
        if not data:
            raise HTTPException(status_code=404, detail="Jellyseerr key not found")
        return data
    return get_jellyseerr_keys()

@router.get("/jellyseerr/get/selected")
def api_get_selected_jellyseerr_key(session_id: str = Query(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    uid = session["UID"]
    data = get_selected_jellyseerr_key(uid)
    if not data:
        raise HTTPException(status_code=404, detail="No selected Jellyseerr key")
    return data

@router.post("/jellyseerr/add")
def api_add_jellyseerr_key(api_key: str = Body(..., embed=True)):
    add_jellyseerr_key(api_key)
    return {"message": "Jellyseerr key added"}

@router.post("/jellyseerr/select")
def api_select_jellyseerr_key(api_key_id: int = Body(..., embed=True), session_id: str = Body(...)):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    uid = session["UID"]
    select_jellyseerr_key(uid, api_key_id)
    update_session(state, {"JELLYSEERR_TOKEN": get_selected_jellyseerr_key(uid)["api_key"]})
    return {"message": "Jellyseerr key selected"}
