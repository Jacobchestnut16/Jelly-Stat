import {TrendingMovies} from "./media/Trending";
import {RecommendedMovies} from "./media/Recommended.jsx";
import {useEffect, useState} from "react";

export default function Movies({ sessionId }) {
    const [localSessionId, setLocalSessionId] = useState(sessionId);

    useEffect(() => {
        setLocalSessionId(sessionId);
    }, [sessionId]);

    useEffect(() => {
        const handler = () => {
            setLocalSessionId(localStorage.getItem("session_id"));
        };
        window.addEventListener("storage", handler);
        return () => window.removeEventListener("storage", handler);
    }, []);

    return (
        <div>
            <TrendingMovies sessionId={localSessionId}/>
            <RecommendedMovies sessionId={localSessionId}/>
            <div className="credit">
                <p>Images powered by <a href="https://tmdb.org">TMDB</a></p>
            </div>
        </div>
    );
}