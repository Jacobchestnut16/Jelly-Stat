from app.services.jellyseerr.data import get_page, get_pages_len
from enum import Enum

class RequestURL(Enum):
    request = 0
    media = 1

def getEverything(url, key,requesting=RequestURL.request):
    r = int(requesting.value)
    max_pages = get_pages_len(url=url,key=key,requesting=requesting.value)
    data = []
    for page in range(max_pages):
        page_data = get_page(url=url,key=key,page=page,requesting=requesting.value)
        data.extend(page_data)
    return data

def appendLast(url, key,data,requesting=RequestURL.request):
    last = get_page(url=url,key=key,take=1,requesting=requesting.value)
    known_ids =[]
    for d in data:
        known_ids.append(d['tmdb_id'])
    for f in last:
        if f['tmdb_id'] in known_ids:
            continue
        data.append(f)
    return data

def appendNew(url, key,data,requesting=RequestURL.request):
    r = int(requesting.value)
    last = get_page(url=url,key=key,page=1,requesting=requesting.value)
    known_ids =[]
    for d in data:
        known_ids.append(d['tmdb_id'])
    for f in last:
        if f['tmdb_id'] in known_ids:
            continue
        data.append(f)
    return data

def printFormat(data):
    retData = ""
    for d in data:
        own = "owned" if d['jellyfin_media_id'] else "unowned"
        retData += f"{d['type']}    {own}    {d['title']}\n"
    return retData