-- Users authenticated via Trakt
-- permissions table
-- {
--    disabled-user      :   0, (user id created, but cannot login)
--    normal-user        :   2, (can login, edit their profile, make requests)
--    admin              :   5, (can view users, disabled users, can login, edit their profile, make requests)
--    no-trakt-admin     :   8, (semi-login, can view users, disabled users, cannot make requests, cannot edit a trakt profile)
-- }
CREATE TABLE users (
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

-- TMDB API keys
CREATE TABLE tmdb_api (
    id SERIAL PRIMARY KEY,
    api_key TEXT NOT NULL UNIQUE,
    active BOOLEAN DEFAULT FALSE
);

-- User’s selected TMDB key
CREATE TABLE user_tmdb_key (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    tmdb_api_id INTEGER REFERENCES tmdb_api(id) ON DELETE CASCADE,
    UNIQUE (user_id, selected) WHERE selected = TRUE
);

-- Jellyseerr API keys
CREATE TABLE jellyseerr_api (
    id SERIAL PRIMARY KEY,
    api_key TEXT NOT NULL UNIQUE,
    active BOOLEAN DEFAULT FALSE
);

-- User’s selected Jellyseerr key
CREATE TABLE user_jellyseerr_key (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    jellyseerr_api_id INTEGER REFERENCES jellyseerr_api(id) ON DELETE CASCADE,
    UNIQUE (user_id, selected) WHERE selected = TRUE
);

-- Films
CREATE TABLE films (
    tmdb_id INTEGER PRIMARY KEY,
    slug VARCHAR(150) UNIQUE,
    jellyfin_id VARCHAR(200) UNIQUE,
    jellyseerr_id VARCHAR(200) UNIQUE
);

CREATE TABLE film_images (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER REFERENCES films(tmdb_id) ON DELETE CASCADE,
    entry_date DATE,
    poster_url TEXT,
    logo_url TEXT,
    backdrop_url TEXT

);

CREATE TABLE jellyseerr(
    jellyseerr_id VARCHAR(200) UNIQUE,
    cost DOUBLE,
    sell_back DOUBLE
)

-- Ratings and history stay tied to user + film
CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER REFERENCES films(tmdb_id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating BETWEEN 0 AND 10),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted BOOLEAN DEFAULT FALSE
);

CREATE TABLE history (
    id SERIAL PRIMARY KEY,
    tmdb_id INTEGER REFERENCES films(tmdb_id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted BOOLEAN DEFAULT FALSE
);
