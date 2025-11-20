import {TrendingShows} from "./media/Trending";
import {RecommendedShows} from "./media/Recommended.jsx";
import {useEffect, useState} from "react";

export default function Shows({ sessionId }) {
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
            <TrendingShows sessionId={localSessionId}/>
            <RecommendedShows sessionId={localSessionId}/>
            <div className="credit">
                <p>Images powered by <a href="https://tmdb.org">TMDB</a></p>
            </div>
        </div>
    );
}