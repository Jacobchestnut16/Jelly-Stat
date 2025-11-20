//
// Created by Jacob on 9/5/25.
//

#include "trakt_api.h"
#include <curl/curl.h>
#include <config.h>
#include <iostream>
#include "json.hpp"

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}



nlohmann::json makeRequestNoAuth(const std::string &endpoint, const TraktConfig &config) {
    std::cout << "Make a Request to: " << endpoint << "\n" << std::flush;
    CURL *curl;
    CURLcode res;
    std::string readBuffer;

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, endpoint.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

        curl_slist *headers = NULL;

        headers = curl_slist_append(headers, "Content-Type: application/json");
        headers = curl_slist_append(headers, "trakt-api-version: 2");
        std::string authHeader = "trakt-api-key: " + config.clientId;
        headers = curl_slist_append(headers, authHeader.c_str());
        headers = curl_slist_append(headers, "User-Agent: BetterWatchlist/1.0.0"); //technically needed

        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);


        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);


        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << "\n" << std::flush;
        } else {
            long http_code = 0;
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
            std::cerr << "HTTP status: " << http_code << "\n" << std::flush;
            if (http_code == 401) {
                std::cerr
                << "Trakt API Keys attempted \n { \n"
                << " \"client_id\" : \""
                <<config.clientId
                << "\"\n } \n"
                << std::flush;
            }
        }
    }else {
        std::cerr << "Curl either could not be initialized or is not installed." << "\n" << std::flush;
    }

    // std::cout << "response: " << readBuffer << "\n" << std::flush;
    try {
        nlohmann::json response = nlohmann::json::parse(readBuffer);
        if (response.contains("results")) {
            return response["results"];  // just the array
        } else {
            return response;             // fallback: return full JSON if "results" missing
        }
    } catch (const std::exception& e) {
        std::cerr << "JSON parse error: " << e.what() << "\n" << std::flush;
        return nlohmann::json{};
    }
}

void getCode(const TraktConfig &config) {
    // https://api.trakt.tv/oauth/authorize?response_type=code&client_id=%20&redirect_uri=%20&state=%20
    /*
     * set config.accessToken = {'code': TheReturnedCode }
     */
}
void getTokens(const TraktConfig &config) {
    /*
     * if config.accessToken["refresh_token"] does not exist:
     */

    //     curl --include \
    //      --request POST \
    //      --header "Content-Type: application/json" \
    //      --data-binary "{
    //     \"code\": \"fd0847dbb559752d932dd3c1ac34ff98d27b11fe2fea5a864f44740cd7919ad0\",          <--  config.accessToken["code"]
    //     \"client_id\": \"9b36d8c0db59eff5038aea7a417d73e69aea75b41aac771816d2ef1b3109cc2f\",     <--  config.clientId
    //     \"client_secret\": \"d6ea27703957b69939b8104ed4524595e210cd2e79af587744a7eb6e58f5b3d2\", <--  config.client_secret
    //     \"redirect_uri\": \"urn:ietf:wg:oauth:2.0:oob\",                                         <-- not sure what this should be
    //     \"grant_type\": \"authorization_code\"
    // }" \
    // 'https://api.trakt.tv/oauth/token'

    /*
     * else :
     */

//     curl --include \
//      --request POST \
//      --header "Content-Type: application/json" \
//      --data-binary "{
//     \"refresh_token\": \"fd0847dbb559752d932dd3c1ac34ff98d27b11fe2fea5a864f44740cd7919ad0\",  <--  config.accessToken["code"]
//     \"client_id\": \"9b36d8c0db59eff5038aea7a417d73e69aea75b41aac771816d2ef1b3109cc2f\",      <--  config.clientId
//     \"client_secret\": \"d6ea27703957b69939b8104ed4524595e210cd2e79af587744a7eb6e58f5b3d2\",  <--  config.client_secret
//     \"redirect_uri\": \"urn:ietf:wg:oauth:2.0:oob\",                                          <-- not sure what this should be
//     \"grant_type\": \"refresh_token\"
// }" \
// 'https://api.trakt.tv/oauth/token'

    /*
     * update config.accessToken = {
          "access_token" : access_token-retuned,
          "token_type"   : token_type-returned,
          "expires_in"   : expires_in-returned,
          "refresh_token": refresh_token-returned,
          "scope"        : scope-returned,
          "created_at"   : created_at-returned
        }
     */
}
void authorize(const TraktConfig &config) {
    if (/*config.accessToken is null ||*/config.accessToken.empty()) {
        getCode(config);
        getTokens(config);
    }else {
        getTokens(config);
    }
}

