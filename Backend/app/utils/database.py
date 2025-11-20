import datetime
from sqlalchemy import create_engine, text
from app.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_connection():
    return engine.connect()

# -----------------------
# Helper: row conversion
# -----------------------
def rows_to_dicts(result):
    return [dict(row._mapping) for row in result]

def row_to_dict(row):
    return dict(row._mapping) if row else None


# -----------------------
# Users (Trakt identity)
# -----------------------

def create_user(username, password, trakt_client_id="", trakt_client_secret=""):
    with engine.begin() as conn:
        r = conn.execute(
            text("""
                INSERT INTO users (username, pass, trakt_client_id, trakt_client_secret)
                VALUES (:username, :pass, :trakt_client_id, :trakt_client_secret)
                RETURNING id
            """),
            {
                "username": username,
                "pass": password,
                "trakt_client_id": trakt_client_id,
                "trakt_client_secret": trakt_client_secret
            },
        )
        return r.scalar()

def get_user_by_id(user_id):
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
        return row_to_dict(r.fetchone())

def authUser(username):
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username})
        return row_to_dict(r.fetchone())

def get_user_by_trakt_id(trakt_id):
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM users WHERE trakt_id = :trakt_id"), {"trakt_id": trakt_id})
        return row_to_dict(r.fetchone())

def update_user_tokens(user_id, access_token, refresh_token=None, token_expires=None):
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE users
                SET access_token = :access_token,
                    refresh_token = :refresh_token,
                    token_expires = :token_expires
                WHERE id = :user_id
            """),
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_expires": token_expires,
                "user_id": user_id,
            },
        )
        return True

def delete_user(user_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM users WHERE id = :id"), {"id": user_id})
        return True


# -----------------------
# TMDB API keys
# -----------------------

def get_tmdb_keys():
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM tmdb_api ORDER BY id"))
        return rows_to_dicts(r)

def get_tmdb_key(key_id):
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM tmdb_api WHERE id = :id"), {"id": key_id})
        return row_to_dict(r.fetchone())

def add_tmdb_key(api_key, active=False):
    with engine.begin() as conn:
        r = conn.execute(
            text("INSERT INTO tmdb_api (api_key, active) VALUES (:api_key, :active) RETURNING id"),
            {"api_key": api_key, "active": active},
        )
        return r.scalar()

def update_tmdb_key(key_id, api_key=None, active=None):
    parts = []
    params = {"id": key_id}
    if api_key is not None:
        parts.append("api_key = :api_key")
        params["api_key"] = api_key
    if active is not None:
        parts.append("active = :active")
        params["active"] = active
    if not parts:
        return False
    stmt = f"UPDATE tmdb_api SET {', '.join(parts)} WHERE id = :id"
    with engine.begin() as conn:
        conn.execute(text(stmt), params)
        return True

def delete_tmdb_key(key_id=None, api_key=None):
    if key_id is None and api_key is None:
        return False
    with engine.begin() as conn:
        if key_id is not None:
            conn.execute(text("DELETE FROM tmdb_api WHERE id = :id"), {"id": key_id})
        if api_key is not None:
            conn.execute(text("DELETE FROM tmdb_api WHERE api_key = :api_key"), {"api_key": api_key})
        return True


# -----------------------
# User's selected TMDB key
# -----------------------

def get_selected_tmdb_key(user_id):
    with get_connection() as conn:
        r = conn.execute(
            text("SELECT tmdb_api_id FROM user_tmdb_key WHERE user_id = :user_id AND selected = TRUE"),
            {"user_id": user_id})
        row = r.fetchone()
        if not row:
            return None
        key = get_tmdb_key(row[0])
        return {"id": row[0], "api_key": key["api_key"] if key else None}

def select_tmdb_key(user_id, tmdb_api_id):
    with engine.begin() as conn:
        conn.execute(text("UPDATE user_tmdb_key SET selected = FALSE WHERE user_id = :user_id"),
                     {"user_id": user_id})
        res = conn.execute(
            text("""
                UPDATE user_tmdb_key
                SET tmdb_api_id = :tmdb_api_id, selected = TRUE
                WHERE user_id = :user_id
                RETURNING id
            """),
            {"tmdb_api_id": tmdb_api_id, "user_id": user_id},
        )
        updated_id = res.scalar()
        if updated_id:
            return updated_id
        r = conn.execute(
            text("""
                INSERT INTO user_tmdb_key (user_id, tmdb_api_id, selected)
                VALUES (:user_id, :tmdb_api_id, TRUE)
                RETURNING id
            """),
            {"user_id": user_id, "tmdb_api_id": tmdb_api_id},
        )
        return r.scalar()

def update_selected_tmdb_key(user_id, tmdb_api_id):
    return select_tmdb_key(user_id, tmdb_api_id)

def remove_selected_tmdb_key(user_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM user_tmdb_key WHERE user_id = :user_id"), {"user_id": user_id})
        return True


# -----------------------
# Jellyseerr API keys
# -----------------------

def get_jellyseerr_keys():
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM jellyseerr_api ORDER BY id"))
        return rows_to_dicts(r)

def get_jellyseerr_key(key_id):
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM jellyseerr_api WHERE id = :id"), {"id": key_id})
        return row_to_dict(r.fetchone())

def add_jellyseerr_key(api_key, active=False):
    with engine.begin() as conn:
        r = conn.execute(
            text("INSERT INTO jellyseerr_api (api_key, active) VALUES (:api_key, :active) RETURNING id"),
            {"api_key": api_key, "active": active},
        )
        return r.scalar()

def update_jellyseerr_key(key_id, api_key=None, active=None):
    parts = []
    params = {"id": key_id}
    if api_key is not None:
        parts.append("api_key = :api_key")
        params["api_key"] = api_key
    if active is not None:
        parts.append("active = :active")
        params["active"] = active
    if not parts:
        return False
    stmt = f"UPDATE jellyseerr_api SET {', '.join(parts)} WHERE id = :id"
    with engine.begin() as conn:
        conn.execute(text(stmt), params)
        return True

def delete_jellyseerr_key(key_id=None, api_key=None):
    if key_id is None and api_key is None:
        return False
    with engine.begin() as conn:
        if key_id is not None:
            conn.execute(text("DELETE FROM jellyseerr_api WHERE id = :id"), {"id": key_id})
        if api_key is not None:
            conn.execute(text("DELETE FROM jellyseerr_api WHERE api_key = :api_key"), {"api_key": api_key})
        return True

# Jellyseerr url

def get_jellyseerr_urls():
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM jellyseerr_url ORDER BY id"))
        return rows_to_dicts(r)

def get_jellyseerr_url(url_id):
    with get_connection() as conn:
        r = conn.execute(
            text("SELECT * FROM jellyseerr_url WHERE id = :id"),
            {"id": url_id}
        )
        return row_to_dict(r.fetchone())

def add_jellyseerr_url(url, active=False):
    with engine.begin() as conn:
        r = conn.execute(
            text("INSERT INTO jellyseerr_url (url, active) VALUES (:url, :active) RETURNING id"),
            {"url": url, "active": active},
        )
        return r.scalar()

def update_jellyseerr_url(url_id, url_key=None, active=None):
    parts = []
    params = {"id": url_id}
    if url_key is not None:
        parts.append("url = :url_key")
        params["url_key"] = url_key
    if active is not None:
        parts.append("active = :active")
        params["active"] = active
    if not parts:
        return False
    stmt = f"UPDATE jellyseerr_url SET {', '.join(parts)} WHERE id = :id"
    with engine.begin() as conn:
        conn.execute(text(stmt), params)
        return True

def delete_jellyseerr_url(url_id=None, url_key=None):
    if url_id is None and url_key is None:
        return False
    with engine.begin() as conn:
        if url_id is not None:
            conn.execute(text("DELETE FROM jellyseerr_url WHERE id = :id"), {"id": url_id})
        if url_key is not None:
            conn.execute(text("DELETE FROM jellyseerr_url WHERE url = :url_key"), {"url_key": url_key})
        return True


# -----------------------
# User's selected Jellyseerr key
# -----------------------

def get_selected_jellyseerr_key(user_id):
    with get_connection() as conn:
        r = conn.execute(
            text("SELECT jellyseerr_api_id FROM user_jellyseerr_key WHERE user_id = :user_id AND selected = TRUE"),
            {"user_id": user_id})
        row = r.fetchone()
        if not row:
            return None
        key = get_jellyseerr_key(row[0])
        return {"id": row[0], "api_key": key["api_key"] if key else None}

def select_jellyseerr_key(user_id, jellyseerr_api_id):
    with engine.begin() as conn:
        conn.execute(text("UPDATE user_jellyseerr_key SET selected = FALSE WHERE user_id = :user_id"),
                     {"user_id": user_id})
        res = conn.execute(
            text("""
                UPDATE user_jellyseerr_key
                SET jellyseerr_api_id = :jellyseerr_api_id, selected = TRUE
                WHERE user_id = :user_id
                RETURNING id
            """),
            {"jellyseerr_api_id": jellyseerr_api_id, "user_id": user_id},
        )
        updated_id = res.scalar()
        if updated_id:
            return updated_id
        r = conn.execute(
            text("""
                INSERT INTO user_jellyseerr_key (user_id, jellyseerr_api_id, selected)
                VALUES (:user_id, :jellyseerr_api_id, TRUE)
                RETURNING id
            """),
            {"user_id": user_id, "jellyseerr_api_id": jellyseerr_api_id},
        )
        return r.scalar()

def update_selected_jellyseerr_key(user_id, jellyseerr_api_id):
    return select_jellyseerr_key(user_id, jellyseerr_api_id)

def remove_selected_jellyseerr_key(user_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM user_jellyseerr_key WHERE user_id = :user_id"), {"user_id": user_id})
        return True

# Jellyseerr URL

def get_selected_jellyseerr_url(user_id):
    with get_connection() as conn:
        r = conn.execute(
            text("SELECT url FROM user_jellyseerr_url WHERE user_id = :user_id AND selected = TRUE"),
            {"user_id": user_id},
        )
        row = r.fetchone()
        if not row:
            return None

        url_id = row[0]
        url = get_jellyseerr_url(url_id)  # expects row_to_dict(...) or None
        return {"id": url_id, "url": url["url"] if url else None}



def select_jellyseerr_url(user_id, jellyseerr_url_id):
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE user_jellyseerr_url SET selected = FALSE WHERE user_id = :user_id"),
            {"user_id": user_id}
        )

        res = conn.execute(
            text("""
                UPDATE user_jellyseerr_url
                SET url = :url_id, selected = TRUE
                WHERE user_id = :user_id
                RETURNING id
            """),
            {"url_id": jellyseerr_url_id, "user_id": user_id}
        )
        updated_id = res.scalar()

        if updated_id:
            return updated_id

        r = conn.execute(
            text("""
                INSERT INTO user_jellyseerr_url (user_id, url, selected)
                VALUES (:user_id, :url_id, TRUE)
                RETURNING id
            """),
            {"user_id": user_id, "url_id": jellyseerr_url_id}
        )
        return r.scalar()


def update_selected_jellyseerr_url(user_id, jellyseerr_url_id):
    return select_jellyseerr_url(user_id, jellyseerr_url_id)

def remove_selected_jellyseerr_url(user_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM user_jellyseerr_url WHERE user_id = :user_id"), {"user_id": user_id})
        return True

# -----------------------
# Films and film_images
# -----------------------

def add_film(tmdb_id, slug=None, jellyfin_id=None, jellyseerr_id=None):
    with engine.begin() as conn:
        r = conn.execute(
            text("""
                INSERT INTO films (tmdb_id, slug, jellyfin_id, jellyseerr_id)
                VALUES (:tmdb_id, :slug, :jellyfin, :jellyseerr)
                ON CONFLICT (tmdb_id) DO UPDATE
                SET slug = EXCLUDED.slug,
                    jellyfin_id = EXCLUDED.jellyfin_id,
                    jellyseerr_id = EXCLUDED.jellyseerr_id
                RETURNING tmdb_id
            """),
            {"tmdb_id": tmdb_id, "slug": slug, "jellyfin": jellyfin_id, "jellyseerr": jellyseerr_id},
        )
        return r.scalar()

def get_film(tmdb_id):
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM films WHERE tmdb_id = :tmdb_id"), {"tmdb_id": tmdb_id})
        return row_to_dict(r.fetchone())

def delete_film(tmdb_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM films WHERE tmdb_id = :tmdb_id"), {"tmdb_id": tmdb_id})
        return True

def lookup_film_image(tmdb_id):
    with get_connection() as conn:
        r = conn.execute(text(
            "SELECT poster_url, logo_url, backdrop_url, entry_date FROM film_images WHERE tmdb_id = :tmdb_id ORDER BY entry_date DESC LIMIT 1"),
                         {"tmdb_id": tmdb_id})
        return row_to_dict(r.fetchone())

def add_film_image(tmdb_id, poster_url=None, logo_url=None, backdrop_url=None):
    with engine.begin() as conn:
        r = conn.execute(
            text("""
                INSERT INTO film_images (tmdb_id, entry_date, poster_url, logo_url, backdrop_url)
                VALUES (:tmdb_id, :entry_date, :poster, :logo, :backdrop)
                RETURNING id
            """),
            {
                "tmdb_id": tmdb_id,
                "entry_date": datetime.datetime.now(),
                "poster": poster_url,
                "logo": logo_url,
                "backdrop": backdrop_url,
            },
        )
        return r.scalar()

def delete_film_image(film_image_id=None, tmdb_id=None):
    if film_image_id is None and tmdb_id is None:
        return False
    with engine.begin() as conn:
        if film_image_id is not None:
            conn.execute(text("DELETE FROM film_images WHERE id = :id"), {"id": film_image_id})
        if tmdb_id is not None:
            conn.execute(text("DELETE FROM film_images WHERE tmdb_id = :tmdb_id"), {"tmdb_id": tmdb_id})
        return True


# -----------------------
# Ratings
# -----------------------

def add_rating(tmdb_id, user_id, rating, submitted=False):
    with engine.begin() as conn:
        r = conn.execute(
            text("""
                INSERT INTO ratings (tmdb_id, user_id, rating, date, submitted)
                VALUES (:tmdb_id, :user_id, :rating, :date, :submitted)
                RETURNING id
            """),
            {"tmdb_id": tmdb_id, "user_id": user_id, "rating": rating, "date": datetime.datetime.now(), "submitted": submitted},
        )
        return r.scalar()

def get_rating(tmdb_id, user_id):
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM ratings WHERE tmdb_id = :tmdb_id AND user_id = :user_id"),
                         {"tmdb_id": tmdb_id, "user_id": user_id})
        return row_to_dict(r.fetchone())

def update_rating(tmdb_id, user_id, rating=None, submitted=None):
    parts = []
    params = {"tmdb_id": tmdb_id, "user_id": user_id}
    if rating is not None:
        parts.append("rating = :rating")
        params["rating"] = rating
    if submitted is not None:
        parts.append("submitted = :submitted")
        params["submitted"] = submitted
    if not parts:
        return False
    stmt = f"UPDATE ratings SET {', '.join(parts)} WHERE tmdb_id = :tmdb_id AND user_id = :user_id"
    with engine.begin() as conn:
        conn.execute(text(stmt), params)
        return True

def delete_rating(tmdb_id, user_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM ratings WHERE tmdb_id = :tmdb_id AND user_id = :user_id"),
                     {"tmdb_id": tmdb_id, "user_id": user_id})
        return True


# -----------------------
# History
# -----------------------

def add_history(tmdb_id, user_id, submitted=False):
    with engine.begin() as conn:
        r = conn.execute(
            text("""
                INSERT INTO history (tmdb_id, user_id, date, submitted)
                VALUES (:tmdb_id, :user_id, :date, :submitted)
                RETURNING id
            """),
            {"tmdb_id": tmdb_id, "user_id": user_id, "date": datetime.datetime.now(), "submitted": submitted},
        )
        return r.scalar()

def get_history_for_user(user_id, limit=100):
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM history WHERE user_id = :user_id ORDER BY date DESC LIMIT :limit"),
                         {"user_id": user_id, "limit": limit})
        return rows_to_dicts(r)

def delete_history(tmdb_id, user_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM history WHERE tmdb_id = :tmdb_id AND user_id = :user_id"),
                     {"tmdb_id": tmdb_id, "user_id": user_id})
        return True

# -----------------------
# Jellyfin URLs
# -----------------------

def get_jellyfin_urls():
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM jellyfin_url ORDER BY id"))
        return rows_to_dicts(r)


def get_jellyfin_url(url_id):
    with get_connection() as conn:
        r = conn.execute(
            text("SELECT * FROM jellyfin_url WHERE id = :id"),
            {"id": url_id}
        )
        return row_to_dict(r.fetchone())


def add_jellyfin_url(url, active=False):
    with engine.begin() as conn:
        r = conn.execute(
            text("INSERT INTO jellyfin_url (url, active) VALUES (:url, :active) RETURNING id"),
            {"url": url, "active": active},
        )
        return r.scalar()


def update_jellyfin_url(url_id, url_value=None, active=None):
    parts = []
    params = {"id": url_id}

    if url_value is not None:
        parts.append("url = :url_value")
        params["url_value"] = url_value

    if active is not None:
        parts.append("active = :active")
        params["active"] = active

    if not parts:
        return False

    stmt = f"UPDATE jellyfin_url SET {', '.join(parts)} WHERE id = :id"

    with engine.begin() as conn:
        conn.execute(text(stmt), params)
        return True


def delete_jellyfin_url(url_id=None, url_value=None):
    if url_id is None and url_value is None:
        return False

    with engine.begin() as conn:
        if url_id is not None:
            conn.execute(text("DELETE FROM jellyfin_url WHERE id = :id"), {"id": url_id})

        if url_value is not None:
            conn.execute(text("DELETE FROM jellyfin_url WHERE url = :url_value"), {"url_value": url_value})

        return True

# select

def get_selected_jellyfin_url(user_id):
    with get_connection() as conn:
        r = conn.execute(
            text("SELECT url FROM user_jellyfin_url WHERE user_id = :user_id AND selected = TRUE"),
            {"user_id": user_id},
        )
        row = r.fetchone()

        if not row:
            return None

        url_id = row[0]
        url = get_jellyfin_url(url_id)

        return {"id": url_id, "url": url["url"] if url else None}

def select_jellyfin_url(user_id, jellyfin_url_id):
    with engine.begin() as conn:

        conn.execute(
            text("UPDATE user_jellyfin_url SET selected = FALSE WHERE user_id = :user_id"),
            {"user_id": user_id}
        )

        res = conn.execute(
            text("""
                UPDATE user_jellyfin_url
                SET url = :url_id, selected = TRUE
                WHERE user_id = :user_id
                RETURNING id
            """),
            {"url_id": jellyfin_url_id, "user_id": user_id},
        )

        updated_id = res.scalar()

        if updated_id:
            return updated_id

        r = conn.execute(
            text("""
                INSERT INTO user_jellyfin_url (user_id, url, selected)
                VALUES (:user_id, :url_id, TRUE)
                RETURNING id
            """),
            {"user_id": user_id, "url_id": jellyfin_url_id}
        )

        return r.scalar()

def update_selected_jellyfin_url(user_id, jellyfin_url_id):
    return select_jellyfin_url(user_id, jellyfin_url_id)

def remove_selected_jellyfin_url(user_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM user_jellyfin_url WHERE user_id = :user_id"), {"user_id": user_id})
        return True

# -----------------------
# Jellyfin API Keys
# -----------------------

def get_jellyfin_keys():
    with get_connection() as conn:
        r = conn.execute(text("SELECT * FROM jellyfin_key ORDER BY id"))
        return rows_to_dicts(r)


def get_jellyfin_key(key_id):
    with get_connection() as conn:
        r = conn.execute(
            text("SELECT * FROM jellyfin_key WHERE id = :id"),
            {"id": key_id}
        )
        return row_to_dict(r.fetchone())

def add_jellyfin_key(jellyfin_key, active=False):
    with engine.begin() as conn:
        r = conn.execute(
            text("INSERT INTO jellyfin_key (jellyfin_key, active) VALUES (:jellyfin_key, :active) RETURNING id"),
            {"jellyfin_key": jellyfin_key, "active": active},
        )
        return r.scalar()

def update_jellyfin_key(key_id, jellyfin_key=None, active=None):
    parts = []
    params = {"id": key_id}

    if jellyfin_key is not None:
        parts.append("jellyfin_key = :jellyfin_key")
        params["jellyfin_key"] = jellyfin_key

    if active is not None:
        parts.append("active = :active")
        params["active"] = active

    if not parts:
        return False

    stmt = f"UPDATE jellyfin_key SET {', '.join(parts)} WHERE id = :id"

    with engine.begin() as conn:
        conn.execute(text(stmt), params)
        return True

def delete_jellyfin_key(key_id=None, jellyfin_key=None):
    if key_id is None and jellyfin_key is None:
        return False

    with engine.begin() as conn:
        if key_id is not None:
            conn.execute(text("DELETE FROM jellyfin_key WHERE id = :id"), {"id": key_id})

        if jellyfin_key is not None:
            conn.execute(text("DELETE FROM jellyfin_key WHERE jellyfin_key = :jellyfin_key"),
                         {"jellyfin_key": jellyfin_key})

        return True

# Select

def get_selected_jellyfin_key(user_id):
    with get_connection() as conn:
        r = conn.execute(
            text("SELECT jellyfin_key FROM user_jellyfin_key WHERE user_id = :user_id AND selected = TRUE"),
            {"user_id": user_id},
        )
        row = r.fetchone()

        if not row:
            return None

        key_id = row[0]
        key = get_jellyfin_key(key_id)

        return {"id": key_id, "jellyfin_key": key["jellyfin_key"] if key else None}

def select_jellyfin_key(user_id, jellyfin_key_id):
    with engine.begin() as conn:

        conn.execute(
            text("UPDATE user_jellyfin_key SET selected = FALSE WHERE user_id = :user_id"),
            {"user_id": user_id}
        )

        res = conn.execute(
            text("""
                UPDATE user_jellyfin_key
                SET jellyfin_key = :key_id, selected = TRUE
                WHERE user_id = :user_id
                RETURNING id
            """),
            {"key_id": jellyfin_key_id, "user_id": user_id},
        )

        updated_id = res.scalar()

        if updated_id:
            return updated_id

        r = conn.execute(
            text("""
                INSERT INTO user_jellyfin_key (user_id, jellyfin_key, selected)
                VALUES (:user_id, :key_id, TRUE)
                RETURNING id
            """),
            {"user_id": user_id, "key_id": jellyfin_key_id}
        )

        return r.scalar()

def update_selected_jellyfin_key(user_id, jellyfin_key_id):
    return select_jellyfin_key(user_id, jellyfin_key_id)


def remove_selected_jellyfin_key(user_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM user_jellyfin_key WHERE user_id = :user_id"), {"user_id": user_id})
        return True
