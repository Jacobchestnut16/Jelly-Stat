//
// Created by Jacob on 9/5/25.
//

#include "routes.h"

#include <QJsonArray>
#include <QJsonDocument>
#include <QCoreApplication>
#include "json.hpp"

json routes_available = {};

template <typename T>
void push_back_unique(json &loc, const T &data) {
    for (const auto& el : loc) {
        if (el == data) {
            return; // already exists
        }
    }
    loc.push_back(data);
}

std::vector<std::string> split_by_delimiter(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    size_t start = 0;
    size_t end = str.find(delimiter);

    while (end != std::string::npos) {
        tokens.push_back(str.substr(start, end - start));
        start = end + 1;
        end = str.find(delimiter, start);
    }
    tokens.push_back(str.substr(start)); // Add the last token
    return tokens;
}

void Routes::setUnregisteredRout(const std::string& path, const json& staticData) {
    handlers["/api"] = [staticData](const httplib::Request&) {
        return staticData;
    };
}
 // Writes a path endpoint /trending/moives and stores the json blob
void Routes::registerEndpoint(const std::string& path, const json& staticData) {
    if (path != "/api") {
        auto tokens = split_by_delimiter(path, '/');

        // build full path
        std::string full_path = "/api/" + tokens[1];

        if (tokens.size() == 2) {
            // check if already exists
            if (!routes_available.contains(full_path)) {
                if (!routes_available[full_path].contains("content-type")) {
                    routes_available[full_path]["content-type"] = json::array();
                }
                routes_available[full_path]["content-type"].push_back(tokens[1]);
                // only insert "self" if no sub endpoints were registered
                routes_available[full_path]["name"] = tokens[1];
            }else {
                routes_available[full_path][full_path] = "both";
                routes_available[full_path]["name"] = tokens[1];
            }
        } else if (tokens.size() == 3) {
            std::string last_element = tokens[2];
            if (!routes_available[full_path].contains("content-type")) {
                routes_available[full_path]["content-type"] = json::array();
            }
            push_back_unique(routes_available[full_path]["content-type"], last_element);
            routes_available[full_path][full_path+"/"+last_element] = last_element;
        }

        handlers["/api"+path] = [staticData](const httplib::Request&) {
            return staticData;
        };
    }else {
        handlers["/api"] = [staticData](const httplib::Request&) {
            return staticData;
        };
    }
}

void Routes::registerEndpoint(const std::string& path, const json& staticData, const std::string& type) {
    if (path != "/api") {
        auto tokens = split_by_delimiter(path, '/');

        // build full path
        std::string full_path = "/api/" + tokens[1];

        if (tokens.size() == 2) {
            // check if already exists
            if (!routes_available.contains(full_path)) {
                if (!routes_available[full_path].contains("content-type")) {
                    routes_available[full_path]["content-type"] = json::array();
                }
                push_back_unique(routes_available[full_path]["content-type"], type);
                // only insert "self" if no sub endpoints were registered
                routes_available[full_path]["name"] = tokens[1];
            }else {
                if (!routes_available[full_path].contains("content-type")) {
                    routes_available[full_path]["content-type"] = json::array();
                }
                push_back_unique(routes_available[full_path]["content-type"], type);
                routes_available[full_path][full_path] = "both";
                routes_available[full_path]["name"] = tokens[1];
            }
        } else if (tokens.size() == 3) {
            std::string last_element = tokens[2];
            if (!routes_available[full_path].contains("content-type")) {
                routes_available[full_path]["content-type"] = json::array();
            }
            push_back_unique(routes_available[full_path]["content-type"], type);
            routes_available[full_path][full_path+"/"+last_element] = last_element;
        }

        handlers["/api"+path] = [staticData](const httplib::Request&) {
            return staticData;
        };
    }else {
        handlers["/api"] = [staticData](const httplib::Request&) {
            return staticData;
        };
    }
}

 // binds the endpoints to the server to be reached by GET headers
void Routes::bindToServer(httplib::Server& svr) {
    for (auto& [path, handler] : handlers) {
        svr.Get(path.c_str(), [handler](const httplib::Request& req, httplib::Response& res) {
            json result = handler(req);
            res.set_content(result.dump(), "application/json");
        });
    }
}

json Routes::api_routes_available() {
    return routes_available;
}


 // Register three types of routes at once
void registerThreeRoutes(Routes& routes, const std::string& path, const json& movieData, const json& showData) {
    routes.registerEndpoint(path + "/movies", movieData);
    routes.registerEndpoint(path + "/shows", showData);

    routes.registerEndpoint(path, json{
    {"movies", movieData},
    {"shows",  showData}
    });
}