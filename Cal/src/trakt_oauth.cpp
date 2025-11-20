//
// Created by Jacob on 10/1/25.
//

#include "trakt_oauth.h"
#include <iostream>

std::mutex code_mutex;
std::condition_variable code_cv;
std::string oauth_code;

void registerTraktOAuthCallback(httplib::Server &svr) {
    svr.Get("/trakt/callback", [](const httplib::Request &req, httplib::Response &res) {
        if (req.has_param("code")) {
            {
                std::lock_guard<std::mutex> lock(code_mutex);
                oauth_code = req.get_param_value("code");
            }
            res.set_content("Authorization complete. You can close this tab.", "text/plain");
            code_cv.notify_one();
        } else {
            res.set_content("No code found in query parameters.", "text/plain");
        }
    });
}

std::string waitForOAuthCode() {
    std::unique_lock<std::mutex> lock(code_mutex);
    code_cv.wait(lock, [] { return !oauth_code.empty(); });
    return oauth_code;
}
#include <iomanip>
#include <sstream>
#include <string>

std::string encode_url(const std::string &value) {
    std::ostringstream escaped;
    escaped.fill('0');
    escaped << std::hex;

    for (unsigned char c : value) {
        // Alphanumeric and -_.~ are "safe" characters
        if (isalnum(c) || c == '-' || c == '_' || c == '.' || c == '~') {
            escaped << c;
        } else {
            escaped << '%' << std::setw(2) << int(c);
        }
    }

    return escaped.str();
}



std::string generateTraktAuthUrl(const TraktConfig &config) {
    return "https://api.trakt.tv/oauth/authorize?response_type=code"
           "&client_id=" + config.clientId +
           "&redirect_uri=" + encode_url(config.redirectUri) +
           "&state=xyz"; // optional random state
}

nlohmann::json fetchTraktTokens(const std::string &code, const TraktConfig &config) {
    httplib::Client cli("https://api.trakt.tv");

    nlohmann::json body = {
        {"code", code},
        {"client_id", config.clientId},
        {"client_secret", config.clientSecret},
        {"redirect_uri", config.redirectUri},
        {"grant_type", "authorization_code"}
    };

    auto res = cli.Post("/oauth/token", body.dump(), "application/json");
    if (!res || res->status != 200) {
        std::cerr << "Trakt token fetch failed: " << (res ? res->status : -1) << "\n";
        throw std::runtime_error("Failed to get Trakt token");
    }
    return nlohmann::json::parse(res->body);
}


