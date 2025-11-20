//
// Created by Jacob on 9/5/25.
//

#ifndef BACKEND_CONFIG_H
#define BACKEND_CONFIG_H

#pragma once
#include "json.hpp"
#include "routes.h"

struct TraktConfig {
    std::string redirectUri;
    std::string clientId;
    std::string clientSecret;
    std::string tmdb_bearer;
    json accessToken; // future: store/retrieve access token
};

// Load configuration from JSON file
TraktConfig loadConfig(const std::string &path);
void saveConfig(const std::string &path, const TraktConfig &config);

#endif //BACKEND_CONFIG_H