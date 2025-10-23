# Film Finder
Film Finder is an extension app designed to improve the Trakt experience by enhancing recommendations and analytics. It integrates TMDB to counterbalance Trakt’s tendency to deliver repetitive or poorly rated recommendations. Instead of the common "flat curve" where the same shows or movies are repeated, Film Finder diversifies and plans to personalizes content discovery.

## Features
* Recommended → Personalized picks tailored to the user.
* Upcoming → Movies and shows scheduled but not yet released.
* Underrated → Highly rated titles with low watch counts.
* Similar → Content related to a given movie or show.
* History → Full watch log tracking via trakt.
* Analytics → Aggregated statistics (average ratings, completion %, * binge patterns).
* Curated → Pulls recommendations across all watchlists (3–6 per film * based on ratings).
## Planned Enhancements
* Fetch top-rated films for each user.
* Improved recommendation filters with rating and watch-count thresholds.
* Fallback logic for short lists (random drops if <10 items).
* Combined multi-watchlist recommendations with rating-based prioritization.
* Considerations for list shortening (e.g., newest, most popular, oldest).
* Docker setup to simplify configuration and deployment.
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

# Trakt info
TRAKT_CLIENT_ID     = ""
TRAKT_CLIENT_SECRET = ""

# The Moive Database info
# This should be the API Read Access Token not the API Key
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
  backend:
    build: ./backend #Backend project dircotry
    container_name: trakt_backend
    ports:
      - "3001:8080" #The backend uses port 8080, 3001 is the port the frontend looks up. recomended to not change
    volumes:
      - ./backend/config:/app/config:ro #The config file
    environment:
      - ENV=production
      - CONFIG_PATH=/app/config/config.json #The location of the configfile for the backend to lookup


  frontend:
    build: ./frontend
    container_name: trakt_frontend
    ports:
      - "3000:80" #NGINX runs 80 for the frontend change 3000 if you need a different port on your host
    depends_on:
      - backend
```

# API documentation

openAPI docs can be found on your instance at:
```
http://localhost:3001/docs
```

Current routes include

    Users - trakt user data
    Auth - trakt barer auth
    Media - media item json objects
    Sync - sync with trakt

# What is trakt

Trakt TV is a source that will help organize your collections, create multi watchlist playlists, and even scrobble your media. Scrobbling is a method to grab data about your currently watching on your devices. Trakt VIP will scrobble most main stream streaming services.