import json
from pathlib import Path
from typing import Optional
from app.utils import config

file_path = Path("./data/token.json")

class TokenStore:
    def __init__(self):
        file_path.parent.mkdir(parents=True, exist_ok=True)

    def save_token(self, payload: dict):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)

    def get_token(self) -> Optional[dict]:
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
