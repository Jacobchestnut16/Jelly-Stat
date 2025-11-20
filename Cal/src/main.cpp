#include <QCoreApplication>
#include <QFile>

#include <config.h>
#include <trakt_api.h>
#include <tmdb_api.h>
#include <routes.h>
#include "trakt_oauth.h"
#include <data_store.h>

#include "json.hpp"

#include "httplib.h"

void add_cors_headers(httplib::Response &res) {
    res.set_header("Access-Control-Allow-Origin", "*");
    res.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    res.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization");
}


int main(int argc, char *argv[])
{
    httplib::Server svr;
    Routes routes;
    QCoreApplication app(argc, argv);


    // Initialize the config
    const char* configPath = std::getenv("CONFIG_PATH");
    TraktConfig config = loadConfig(configPath);

    registerTraktOAuthCallback(svr);

    std::thread server_thread([&svr]() {
        std::cout << "Server running on http://localhost:8080\n";
        svr.listen("0.0.0.0", 8080);
    });

    // Check if we have a saved access token
    if (config.accessToken.empty()) {
        std::string authUrl = generateTraktAuthUrl(config);
        std::cout << config.redirectUri<<"\n"<< std::flush;
        std::cout << "Go to this URL to authorize the app: " << authUrl << "\n" << std::flush;

        std::string code = waitForOAuthCode();

        nlohmann::json tokens = fetchTraktTokens(code, config);

        config.accessToken = tokens;
        saveConfig(configPath, config);
        std::cout << "Trakt authorization complete.\n"<< std::flush;
    }




    // https://api.themoviedb.org/3/{movie/tv}/popular
    registerThreeRoutes(routes, "/popular",
        makeTMDBRequest(TMDB_BASE+"/movie/popular", config),
        makeTMDBRequest(TMDB_BASE+"/tv/popular", config));


    // https://api.themoviedb.org/3/{movie/tv}/top_rated
    registerThreeRoutes(routes, "/top_rated",
    makeTMDBRequest(TMDB_BASE+"/movie/top_rated", config),
    makeTMDBRequest(TMDB_BASE+"/tv/top_rated", config));

    // https://api.themoviedb.org/3/movie/now_playing
    json in_theaters = makeTMDBRequest(TMDB_BASE+"/movie/now_playing", config);

    // https://api.themoviedb.org/3/movie/upcoming
    json unreleased = makeTMDBRequest(TMDB_BASE+"/movie/upcoming", config);


    //upcoming
    routes.registerEndpoint("/upcoming/in_theaters",in_theaters,"movies");
    routes.registerEndpoint("/upcoming/unreleased",unreleased,"movies");
    routes.registerEndpoint("/upcoming", json{
    {"in_theaters", in_theaters},
    {"unreleased",  unreleased}
    },"movies");


    // https://api.trakt.tv/lists/trending/[personal , official]

    json trending_official_list = makeRequestNoAuth(TRAKT_BASE+"/lists/trending", config);
    int start_index = 6;
    for (int list_i = start_index; list_i < 3+start_index; list_i++) {

        std::string list_slug = "";
        if (trending_official_list[list_i]["list"]["ids"].contains("slug")
            && !trending_official_list[list_i]["list"]["ids"]["slug"].is_null()
            ){
            list_slug = trending_official_list[list_i]["list"]["ids"]["slug"].get<std::string>();
        }

        std::string author = "";
        if (trending_official_list[list_i]["list"]["user"].contains("name")
            && !trending_official_list[list_i]["list"]["user"]["name"].is_null()
            ) {
            author = trending_official_list[list_i]["list"]["user"]["name"].get<std::string>();
        } else if (trending_official_list[list_i]["list"]["user"].contains("username")
            && !trending_official_list[list_i]["list"]["user"]["username"].is_null()
            ) {
            // fallback to username if display name missing
            author = trending_official_list[list_i]["list"]["user"]["username"].get<std::string>();
        } else {
            author = "Unknown";
        }
        // https://api.trakt.tv/lists/[id]/items/[movie , show , season , episode , person]
        int first_list_id = trending_official_list[list_i]["list"]["ids"]["trakt"].get<int>();
        json trending_official_list_items_movies = makeRequestNoAuth(
            TRAKT_BASE
            +"/lists/"
            +std::to_string(first_list_id)
            +"/items/movie?limit=15",
            config);

        json movies_tended_list = json::array();
        if (trending_official_list_items_movies.size() > 0) {
            for (auto &entry : trending_official_list_items_movies) {
                int tmdb_film_id = entry["movie"]["ids"]["tmdb"].get<int>();
                movies_tended_list.push_back( makeTMDBRequest(TMDB_BASE+"/movie/"+std::to_string(tmdb_film_id), config));
            }
        }

        json trending_official_list_items_shows = makeRequestNoAuth(
        TRAKT_BASE
            +"/lists/"
            +std::to_string(first_list_id)
            +"/items/show?limit=15",
            config);

        json shows_tended_list = json::array();
        if (trending_official_list_items_shows.size() > 0) {
            for (auto &entry : trending_official_list_items_shows) {
                int tmdb_film_id = entry["show"]["ids"]["tmdb"].get<int>();
                shows_tended_list.push_back( makeTMDBRequest(TMDB_BASE+"/tv/"+std::to_string(tmdb_film_id), config));
            }
        }
        registerThreeRoutes(routes,
            "/" + list_slug + "-by-" + author,
            movies_tended_list,
            shows_tended_list);
    }



    // https://api.trakt.tv/{movies/shows}/played/monthly
     json movies_played_trakt = makeRequestNoAuth(TRAKT_BASE+"/movies/played/monthly", config);
    json movies_played = json::array();
    for (auto &entry : movies_played_trakt) {
        int tmdb_film_id = entry["movie"]["ids"]["tmdb"].get<int>();
        movies_played.push_back( makeTMDBRequest(TMDB_BASE+"/movie/"+std::to_string(tmdb_film_id), config));
    }

     json shows_played_trakt = makeRequestNoAuth(TRAKT_BASE+"/shows/played/monthly", config);
    json shows_played = json::array();
    for (auto &entry : shows_played_trakt) {
        int tmdb_film_id = entry["show"]["ids"]["tmdb"].get<int>();
        shows_played.push_back( makeTMDBRequest(TMDB_BASE+"/tv/"+std::to_string(tmdb_film_id), config));
    }

    registerThreeRoutes(
        routes,
        "/most_played",
        movies_played,
        shows_played);



    // recommended → user-personalized picks.
    // upcoming → unreleased but scheduled.
    // underrated → high ratings but low watch counts.
    // todo: get films watched or get individuals top high rated film
    // todo: use to get recommended and grab high rated films
    // todo: add a threshold if there aren't enough low watch counts with high ratings drop (add to a drop json before dropping)
    // todo: finally if the list is under 10 films re-add random drops to fulfill this list
    // similar → items related to a given movie/show.
    // history → user’s watch log.
    // analytics → aggregated stats like avg rating, completion %, binge patterns.
    // curated → from all watch lists get 3-6 recommendations per film
    // todo: get a combined list of all watchlist' data
    // todo: get 3-6 recommendations per film based on rating 3 no rating 6 highest rating
    // todo: propose: considerations to shorten the list [newest films, most popular, oldest films]

    json routes_available = routes.api_routes_available();
    std::cerr << "/api found: " << routes_available.dump() << "\n" << std::flush;

    routes.registerEndpoint("/api",routes_available);

    routes.bindToServer(svr);

    svr.set_post_routing_handler([](const httplib::Request &, httplib::Response &res) {
        add_cors_headers(res);
    });

    std::cout << "Server running on http://localhost:" << 8080 << "\n" << std::flush;;
    svr.listen("0.0.0.0", 8080);

    return 0;
}
