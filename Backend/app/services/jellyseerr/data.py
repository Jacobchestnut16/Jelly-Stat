import requests

REQUESTING = [
    "http://jellyser.chestnutsprogramming.local/api/v1/request",
    "http://jellyser.chestnutsprogramming.local/api/v1/media",
]
SEARCH = {
    'movie':"http://jellyser.chestnutsprogramming.local/api/v1/movie/",
    'show':"http://jellyser.chestnutsprogramming.local/api/v1/tv/"
}
headers = {
    'Content-Type': 'application/json',
    'X-Api-Key': None
}

def SET_URL(URL):
    global REQUESTING, SEARCH
    if URL[-1] == '/':
        URL = URL[:-1]

    REQUESTING = [
        f"{URL}/api/v1/request",
        f"{URL}/api/v1/media",
    ]
    SEARCH = {
        'movie': f"{URL}/api/v1/movie/",
        'show': f"{URL}/api/v1/tv/"
    }
    pass

def SET_HEADERS(API_KEY):
    global headers
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': API_KEY
    }


def search(tmdb_id, type):
    url_search = f"{SEARCH[type]}{tmdb_id}"

    response = requests.get(url_search, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    name = response.json()['originalTitle'] if 'originalTitle' in response.json() else response.json()['originalName']

    return (name, response.json())


def get_page(url, key, page=1,take=20,requesting=0):
    SET_URL(url)
    SET_HEADERS(key)
    skip=take*page
    # print(f"SEARCHING:{REQUESTING[requesting]} or requesting:{requesting}")
    url_search=f"{REQUESTING[requesting]}?take={take}&skip={skip}"

    response = requests.get(url_search, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    data = []

    for item in response.json()['results']:
        type = item['type'] if 'type' in item else item['mediaType']
        tmdb_id = item['media']['tmdbId'] if 'media' in item else item['tmdbId']
        jellyfin_media_id = item['media']['jellyfinMediaId'] if 'media' in item else item['jellyfinMediaId']
        if type == 'movie':
            title_data = search(tmdb_id, 'movie')
        else:
            title_data = search(tmdb_id, 'show')
        blob = {
            'title': title_data[0],
            'type': type,
            'tmdb_id': tmdb_id,
            'jellyfin_media_id': jellyfin_media_id,
            'raw-data': item,
            'raw-title-data': title_data[1],
        }
        if (requesting == 0 and blob['jellyfin_media_id'])\
                or (requesting == 1 and blob['jellyfin_media_id'] is None):
            continue

        data.append(blob)

    return data

def get_pages_len(url, key, requesting=0):
    SET_URL(url)
    SET_HEADERS(key)
    url_search=f"{REQUESTING[requesting]}?take=20"
    response = requests.get(url_search, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    return response.json()['pageInfo']['pages']

