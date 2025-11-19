import secrets
import time
from typing import Optional

# Simple in-memory store
_sessions = {}

SESSION_TTL = 86400  # 24h

def create_session(data: dict) -> str:
    session_id = secrets.token_hex(32)
    _sessions[session_id] = {
        "data": data,
        "created": time.time(),
    }
    return session_id

def get_session(session_id: str) -> Optional[dict]:
    s = _sessions.get(session_id)
    if not s:
        return None
    if time.time() - s["created"] > SESSION_TTL:
        delete_session(session_id)
        return None
    return s["data"]

def update_session(session_id: str, updates: dict) -> bool:
    s = _sessions.get(session_id)
    if not s:
        return False
    s["data"].update(updates)
    return True

def delete_session(session_id: str) -> None:
    _sessions.pop(session_id, None)
