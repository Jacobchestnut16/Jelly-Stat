import urllib.parse


IMAGE_PATHS = {'tmdb':'https://image.tmdb.org/t/p/w500'}


def format_genres(item_genres):
    genres = []
    for genre in item_genres:
        genres.append(genre["name"])
    return genres

def format_imagePaths(location="tmdb", ep="/"):
    return IMAGE_PATHS[location]+ep

def format_runtime(runtime):
    if not runtime or not isinstance(runtime, (int, float)):
        return "00:00"
    hours = runtime // 60
    minutes = runtime % 60
    return f"{hours:02}:{minutes:02}"


def summarize_raw(item, item2):
    media = item.get("media", {})
    requester = item.get("requestedBy", {})
    genres = item2.get("genres", [])
    runtime = item2.get("runtime", 0)
    overview = item2.get("overview", {})

    backdrop = item2.get("backdropPath", {})
    poster = item2.get("posterPath", {})

    summary = {
        "ID": item.get("id"),
        "Type": item.get("type"),
        "Status": "Approved" if item.get("status") == 1 else "Pending",
        # "Is 4K": item.get("is4k"),
        "Created": item.get("createdAt"),
        "Owned": bool(media.get("jellyfinMediaId")),
        "TMDB ID": media.get("tmdbId"),
        "Requester": requester.get("displayName") or requester.get("email"),
        # "Request Count (User)": requester.get("requestCount"),
        # "User Type": requester.get("userType"),
        "Last Updated": item.get("updatedAt"),
        "Genres": format_genres(genres),
        "Runtime": format_runtime (runtime),
        "Overview": overview,
    }

    # Filter out None values for readability
    return (
        {k: v for k, v in summary.items() if v is not None},
        format_imagePaths(ep=backdrop),
        format_imagePaths(ep=poster)
    )


def generate_lookup_links(title):
    encoded = urllib.parse.quote_plus(title)
    return {
        "The Exchange": f"https://theexchange.com/search?q={encoded}",
        "Amazon": f"https://www.amazon.com/s?k={encoded}",
        "Best Buy": f"https://www.bestbuy.com/site/searchpage.jsp?st={encoded}",
        "Walmart": f"https://www.walmart.com/search?q={encoded}",
    }