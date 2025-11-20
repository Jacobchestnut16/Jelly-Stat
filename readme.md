# Jelly-Stat
Jelly-Stat is an extension app designed to improve the Trakt experience by enhancing recommendations and analytics. It integrates TMDB to counterbalance Trakt’s tendency to deliver repetitive or poorly rated recommendations. Instead of the common "flat curve" where the same shows or movies are repeated, Film Finder diversifies and plans to personalizes content discovery.

## Features
* Recommended → Personalized picks tailored to the user.
* Trending → Movies and shows trending.
## Planned Enhancements
* Improved recommendation filters with rating and watch-count thresholds.
* Combined multi-watchlist recommendations with rating-based prioritization.
* Jellyfin + Jellyseerr intigration
* ADR (Automatic Disc Ripper) intigration
___
# Setup
Create a .env or copy the example.env to .env file at:`config/.env`
Add your credentials:
```
#
# Your trakt api `https://trakt.tv/oauth/applications` may require the following:
#
# -----Redirect uri------
# http://localhost:3001/auth/callback
# urn:ietf:wg:oauth:2.0:oob
#
# refere line 1 of redirects to `APP_HOST`
# and docker-compose.yml services.backend.ports
# if you change the ports
#

# TMDB
# In order to view where to watch locations and posters this api is required
# This should be the API Read Access Token not the API Key
# This key is not required but this will act as a master key for all users
TMDB_API_KEY        = ""

# App info
APP_HOST            = "http://localhost:3001" #same address as docker-compose.yml services.backend.ports
```
* An example.env is preloaded as a base template.
* Neither api requires a purchase but Trakt VIP is recommended
    * [trakt website](https://www.trakt.tv)
    * [tmdb website](https://www.themoviedb.org)
___
# Running the App

### Install docker

Docker Desktop:

* [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
* [Windoes](https://docs.docker.com/desktop/setup/install/windows-install/)
* [Linux](https://docs.docker.com/desktop/setup/install/linux/)

[Docker Engin (For Linux instead of Docker Desktop)](https://docs.docker.com/engine/install/)

### Run docker

 Warning you may want to change the postgress user and password before running docker see below [configuring the compose file](configuring%20the%20compose%20file])

From the root of the apps directory there is a `docker-compose` file cd to the direcotry containning this file and run:
```
docker compose up -d
```
older versions of docker
```
docker-compose up -d
```

# configuring the compose file
```
services:
  db:
    image: postgres:16
    container_name: traktplus_db
    restart: always
    environment:
      POSTGRES_USER: [your-username]
      POSTGRES_PASSWORD: [your-password]
      POSTGRES_DB: traktplus
    volumes:
      - trakt_db_data:/var/lib/postgresql/data
      - ./Backend/db/schema.sql:/docker-entrypoint-initdb.d/schema.sql:ro
    ports:
      - "5432:5432"

  backend:
    build: ./backend #Backend project dircotry

    container_name: backend
    depends_on:
      - db
    environment:
      - ENV=production
      - CONFIG_PATH=/app/config/config.json #The location of the configfile for the backend to lookup
      - DATABASE_URL=postgresql://traktuser:traktpass@db:5432/traktplus
    ports:
      - "3001:8080" #The backend uses port 8080, 3001 is the port the frontend looks up
    volumes:
      - ./config/.env:/app/.env #The config file

  frontend:
    build: ./frontend
    container_name: frontend
    depends_on:
      - backend
    ports:
      - "3000:80" #NGINX runs 80 for the frontend change 3000 if you need a different port on your host


volumes:
  trakt_db_data:
```

# API documentation

openAPI docs can be found on your instance at:
```
http://localhost:3001/docs
```