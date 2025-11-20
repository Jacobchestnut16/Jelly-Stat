//
// Created by Jacob on 10/1/25.
//

#ifndef BACKEND_TRAKT_OAUTH_H
#define BACKEND_TRAKT_OAUTH_H


#pragma once
#include <httplib.h>
#include "json.hpp"
#include "config.h"
#include <mutex>
#include <condition_variable>

extern std::mutex code_mutex;
extern std::condition_variable code_cv;
extern std::string oauth_code;

void registerTraktOAuthCallback(httplib::Server &svr);

std::string waitForOAuthCode();

std::string generateTraktAuthUrl(const TraktConfig &config);

nlohmann::json fetchTraktTokens(const std::string &code, const TraktConfig &config);

std::string encode_url(const std::string &value);

#endif //BACKEND_TRAKT_OAUTH_H