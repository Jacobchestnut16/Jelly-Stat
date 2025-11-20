cmake_minimum_required(VERSION 3.22)
project(Backend)

set(CMAKE_CXX_STANDARD 20)

find_package(Qt5 REQUIRED Core Network)

find_package(CURL REQUIRED)

include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${CMAKE_SOURCE_DIR}/src)


add_executable(Backend src/main.cpp
        src/config.cpp
        src/config.h
        src/trakt_api.cpp
        src/trakt_api.h
        src/data_store.cpp
        src/data_store.h
        src/routes.cpp
        src/routes.h
        src/tmdb_api.cpp
        src/tmdb_api.h
        src/trakt_oauth.cpp
        src/trakt_oauth.h)


target_link_libraries(Backend
        Qt5::Core
        Qt5::Network
        CURL::libcurl
)