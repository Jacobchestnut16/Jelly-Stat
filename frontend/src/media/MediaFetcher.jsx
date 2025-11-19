import { useEffect, useState } from "react";

const basePath = "https://image.tmdb.org/t/p/w500";

// ----------------------------------------------------
// 1. Bulletproof Media Extractor (no changes)
// ----------------------------------------------------
function extractMedia(raw, type) {
    const obj =
        raw?.movie ||
        raw?.movies ||
        raw?.show ||
        raw?.shows ||
        raw ||
        {};

    const id =
        obj?.ids?.trakt ||
        obj?.ids?.tmdb ||
        obj?.id ||
        obj?.slug ||
        obj?.title ||
        obj?.name ||
        Math.random().toString(36).slice(2);

    const tmdb_id =
        obj?.ids?.tmdb ||
        Math.random().toString(36).slice(2);

    const title = obj?.title || obj?.name || "Unknown";

    let poster =
        obj?.images?.poster ||
        obj?.poster_path ||
        obj?.image ||
        null;

    poster = String(poster); // force to string

    if (poster.startsWith("/")) {
        poster = basePath + poster;
    }else if (poster.startsWith("m")){
        poster = "https://"+poster;
    } else if (poster === "null" || poster === "undefined" || poster === "") {
        poster = null; // or handle as no image
    }

    return {
        id,
        tmdb_id,
        title,
        name: title,
        poster_path: poster,
        type
    };
}


// ----------------------------------------------------
// 2. MediaFetcher Component with session_id support
// ----------------------------------------------------
export default function MediaFetcher({
                                         endpointMovies, // string or null
                                         endpointShows,  // string or null
                                         render,         // function({ data, basePath })
                                         sessionId       // NEW: pass sessionId here
                                     }) {
    const [data, setData] = useState({
        movies: [],
        shows: []
    });

    useEffect(() => {
        const fetchData = async () => {
            // Helper to append session_id query param if present
            const appendSessionId = (url) => {
                if (!url) return null;
                if (!sessionId) return url; // no auth needed or no sessionId
                return url.includes("?") ? `${url}&session_id=${sessionId}` : `${url}?session_id=${sessionId}`;
            };

            const promises = [
                endpointMovies ? fetch(appendSessionId(endpointMovies)) : Promise.resolve(null),
                endpointShows ? fetch(appendSessionId(endpointShows)) : Promise.resolve(null)
            ];

            const [moviesRes, showsRes] = await Promise.all(promises);

            const movies = moviesRes ? await moviesRes.json() : [];
            const shows = showsRes ? await showsRes.json() : [];

            const normMovies = Array.isArray(movies)
                ? movies.map(m => extractMedia(m, "movie"))
                : [];

            const normShows = Array.isArray(shows)
                ? shows.map(s => extractMedia(s, "show"))
                : [];

            setData({
                movies: normMovies,
                shows: normShows
            });
        };

        fetchData();
    }, [endpointMovies, endpointShows, sessionId]);

    return render({ data, basePath });
}
