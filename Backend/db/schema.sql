CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    permissions INT DEFAULT 2,
    username VARCHAR(150) UNIQUE NOT NULL,
    pass VARCHAR(150) NOT NULL,
    trakt_client_id VARCHAR(250) NOT NULL,
    trakt_client_secret VARCHAR(250) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    token_expires TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tmdb_api (
    id SERIAL PRIMARY KEY,
    api_key TEXT NOT NULL UNIQUE,
    active BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS user_tmdb_key (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    tmdb_api_id INTEGER REFERENCES tmdb_api(id) ON DELETE CASCADE,
    selected BOOLEAN DEFAULT FALSE
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_user_tmdb_selected
ON user_tmdb_key (user_id)
WHERE selected = TRUE;

CREATE TABLE IF NOT EXISTS jellyseerr_api (
    id SERIAL PRIMARY KEY,
    api_key TEXT NOT NULL UNIQUE,
    active BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS user_jellyseerr_key (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    jellyseerr_api_id INTEGER REFERENCES jellyseerr_api(id) ON DELETE CASCADE,
    selected BOOLEAN DEFAULT FALSE
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_user_jellyseerr_selected
ON user_jellyseerr_key (user_id)
WHERE selected = TRUE;

CREATE TABLE IF NOT EXISTS films (
    tmdb_id INTEGER PRIMARY KEY,
    slug VARCHAR(150) UNIQUE,
    jellyfin_id VARCHAR(200) UNIQUE,
    jellyseerr_id VARCHAR(200) UNIQUE
);

CREATE TABLE IF NOT EXISTS film_images (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER REFERENCES films(tmdb_id) ON DELETE CASCADE,
    entry_date DATE,
    poster_url TEXT,
    logo_url TEXT,
    backdrop_url TEXT
);

CREATE TABLE IF NOT EXISTS jellyseerr (
    jellyseerr_id VARCHAR(200) UNIQUE,
    cost DOUBLE PRECISION,
    sell_back DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS ratings (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER REFERENCES films(tmdb_id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating BETWEEN 0 AND 10),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS history (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER REFERENCES films(tmdb_id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted BOOLEAN DEFAULT FALSE
);

-- updates and alters

CREATE TABLE IF NOT EXISTS jellyseerr_url (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    active BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS user_jellyseerr_url(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url INTEGER REFERENCES jellyseerr_url(id) ON DELETE CASCADE,
    selected BOOLEAN DEFAULT FALSE
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_user_jellyseerr_url
ON user_jellyseerr_url (user_id)
WHERE selected = TRUE;


CREATE TABLE IF NOT EXISTS jellyfin_url (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    active BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS user_jellyfin_url(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    url INTEGER REFERENCES jellyfin_url(id) ON DELETE CASCADE,
    selected BOOLEAN DEFAULT FALSE
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_user_jellyfin_url
ON user_jellyfin_url (user_id)
WHERE selected = TRUE;

CREATE TABLE IF NOT EXISTS jellyfin_key (
    id SERIAL PRIMARY KEY,
    jellyfin_key TEXT NOT NULL UNIQUE,
    active BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS user_jellyfin_key(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    jellyfin_key INTEGER REFERENCES jellyfin_key(id) ON DELETE CASCADE,
    selected BOOLEAN DEFAULT FALSE
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_user_jellyfin_key
ON user_jellyfin_key (user_id)
WHERE selected = TRUE;