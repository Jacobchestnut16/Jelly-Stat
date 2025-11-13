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
from app.utils import config

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
def api_get_selected_tmdb_key():
    data = get_selected_tmdb_key(config.UID)
    if not data:
        raise HTTPException(status_code=404, detail="No selected TMDB key")
    return data

@router.post("/tmdb/add")
def api_add_tmdb_key(api_key: str = Body(..., embed=True)):
    add_tmdb_key(api_key)
    return {"message": "TMDB key added"}

@router.post("/tmdb/select")
def api_select_tmdb_key(uid: int = Body(..., embed=True), api_key_id: int = Body(..., embed=True)):
    select_tmdb_key(uid, api_key_id)
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
def api_get_selected_jellyseerr_key():
    data = get_selected_jellyseerr_key(config.UID)
    if not data:
        raise HTTPException(status_code=404, detail="No selected Jellyseerr key")
    return data

@router.post("/jellyseerr/add")
def api_add_jellyseerr_key(api_key: str = Body(..., embed=True)):
    add_jellyseerr_key(api_key)
    return {"message": "Jellyseerr key added"}

@router.post("/jellyseerr/select")
def api_select_jellyseerr_key(uid: int = Body(..., embed=True), api_key_id: int = Body(..., embed=True)):
    select_jellyseerr_key(uid, api_key_id)
    return {"message": "Jellyseerr key selected"}
