//
// Created by Jacob on 9/5/25.
//

#ifndef BACKEND_TRAKT_API_H
#define BACKEND_TRAKT_API_H
#include <QJsonArray>
#include <config.h>
#include "json.hpp"


std::string const TRAKT_BASE = "https://api.trakt.tv";

nlohmann::json makeRequestNoAuth(const std::string &endpoint, const TraktConfig &config);
void getCode(const TraktConfig &config);
void getTokens(const TraktConfig &config);
void authorize(const TraktConfig &config);

// TraktAPI trakt(cfg);

// todo: configure the TraktAPI constructor that sets everything in the class

#endif //BACKEND_TRAKT_API_H