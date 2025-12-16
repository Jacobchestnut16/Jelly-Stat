DROP TABLE IF EXISTS user_jellyseerr_url CASCADE;
DROP TABLE IF EXISTS jellyseerr_url CASCADE;

DROP TABLE IF EXISTS user_jellyfin_url CASCADE;
DROP TABLE IF EXISTS jellyfin_url CASCADE;

DROP TABLE IF EXISTS user_jellyfin_key CASCADE;
DROP TABLE IF EXISTS jellyfin_key CASCADE;


-- adds jellyseer and jellyfin support

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