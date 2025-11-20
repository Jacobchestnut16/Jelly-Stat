//
// Created by Jacob on 9/5/25.
//

#include "config.h"

#include <fstream>
#include <iostream>
#include "json.hpp"


TraktConfig loadConfig(const std::string& path) {
    TraktConfig config;

    // open file
    std::ifstream file(path);
    if (!file.is_open()) {
        std::cerr << "Cannot open config file: " << path << "\n";
        return config;
    }

    try {
        nlohmann::json j;
        file >> j;

        if (!j.is_object()) {
            std::cerr << "Invalid JSON in config file: " << path << "\n";
            return config;
        }

        // extract values safely
        if (j.contains("client_id"))     config.clientId     = j["client_id"].get<std::string>();
        if (j.contains("client_secret")) config.clientSecret = j["client_secret"].get<std::string>();
        if (j.contains("tmdb_bearer"))   config.tmdb_bearer  = j["tmdb_bearer"].get<std::string>();
        if (j.contains("accessToken"))   config.accessToken= j["accessToken"].get<std::string>();
        if (j.contains("redirect_uri"))   config.redirectUri= j["redirect_uri"].get<std::string>();
    } catch (const std::exception& e) {
        std::cerr << "Error parsing config file: " << e.what() << "\n";
    }

    return config;
}

void saveConfig(const std::string &path, const TraktConfig &config) {
    nlohmann::json j;
    j["client_id"]       = config.clientId;
    j["client_secret"]   = config.clientSecret;
    j["redirect_uri"]    = config.redirectUri;
    j["access_token_data"] = config.accessToken;  // store the full token JSON

    std::ofstream outFile(path);
    if (!outFile.is_open()) {
        std::cerr << "Failed to open config for writing: " << path << "\n";
        return;
    }

    outFile << j.dump(4); // pretty-print with 4-space indentation
}