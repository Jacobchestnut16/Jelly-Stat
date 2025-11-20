//
// Created by Jacob on 9/5/25.
//

#include "tmdb_api.h"
#include <curl/curl.h>
#include <config.h>
#include <iostream>
#include "json.hpp"


// callback to write response data into a std::string
static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}



nlohmann::json makeTMDBRequest(const std::string &endpoint, const TraktConfig &config) {
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
        headers = curl_slist_append(headers, "accept: application/json");
        std::string authHeader = "Authorization: Bearer " + config.tmdb_bearer;
        headers = curl_slist_append(headers, authHeader.c_str());

        //apply the headers
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);


        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << "\n" << std::flush;
        } else {
            long http_code = 0;
            curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
            std::cerr << "HTTP status: " << http_code << "\n" << std::flush;
        }

        // curl_slist_free_all(headers);
    }else {
        std::cerr << "Curl either could not be initialized or is not installed." << "\n" << std::flush;
    }

    // Now parse JSON
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


// QJsonArray makeTMDBRequest(const QString &endpoint, const TraktConfig &config) {
//     QNetworkAccessManager manager;
//     QNetworkRequest request(QUrl(endpoint.toUtf8()));
//     request.setRawHeader("Accept", "application/json");
//     QString token = config.tmdb_bearer.trimmed();
//     QByteArray authHeader = "Bearer " + token.toUtf8();
//     request.setRawHeader("Authorization", authHeader);
//
//     QEventLoop loop;
//     QJsonArray result; // this will hold the "results" array
//
//     QObject::connect(&manager, &QNetworkAccessManager::finished,
//         [&](QNetworkReply *reply) {
//             int statusCode = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
//             QString reason = reply->attribute(QNetworkRequest::HttpReasonPhraseAttribute).toString();
//             std::cout << "Calling TMDB" << std::endl;
//             qDebug() << "HTTP status:" << statusCode << reason;
//
//             QByteArray data = reply->readAll();
//
//             if (reply->error() != QNetworkReply::NoError) {
//                 qWarning() << "Error:" << reply->errorString();
//                 qWarning() << "Body:" << data;
//             } else {
//                 qDebug() << "Raw response:" << data.left(500);
//
//                 // Parse the JSON
//                 QJsonParseError parseError;
//                 QJsonDocument doc = QJsonDocument::fromJson(data, &parseError);
//                 if (parseError.error != QJsonParseError::NoError) {
//                     qWarning() << "JSON parse error:" << parseError.errorString();
//                 } else if (doc.isObject()) {
//                     QJsonObject obj = doc.object();
//                     if (obj.contains("results") && obj.value("results").isArray()) {
//                         result = obj.value("results").toArray(); // assign the results array
//                     } else {
//                         qWarning() << "Response JSON has no 'results' array.";
//                     }
//                 } else {
//                     qWarning() << "Response JSON is not an object.";
//                 }
//             }
//
//             reply->deleteLater();
//             loop.quit();
//         });
//
//     manager.get(request);
//     loop.exec(); // Wait for request to finish
//
//     return result;
// }
//
//
//
