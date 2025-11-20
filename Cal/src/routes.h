//
// Created by Jacob on 9/5/25.
//

#ifndef BACKEND_ROUTES_H
#define BACKEND_ROUTES_H

// registerRoutes(svr, trakt, store);

// todo: set a function that registers all found routes from the TraktAPI

#pragma once
#include "httplib.h"
#include "json.hpp"
#include <functional>
#include <string>
#include <unordered_map>
#include <QJsonArray>

using json = nlohmann::json;
using EndpointHandler = std::function<json(const httplib::Request&)>;



class Routes {
public:
    void registerEndpoint(const std::string& path, const json& staticData);
    void registerEndpoint(const std::string& path, const json& staticData, const std::string& type);
    void setUnregisteredRout(const std::string& path, const json& staticData);
    void bindToServer(httplib::Server& svr);
    json api_routes_available();
private:
    std::unordered_map<std::string, EndpointHandler> handlers;
};


void registerThreeRoutes(Routes& routes, const std::string& path, const json& movieData, const json& showData);


#endif //BACKEND_ROUTES_H