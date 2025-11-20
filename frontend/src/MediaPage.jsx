import Trending from "./media/Trending";
import Recommended from "./media/Recommended.jsx";
import { useEffect, useState } from "react";

export default function MediaPage({ sessionId }) {
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

    // Example: pass sessionId to Trending and Recommended if they need it in fetch calls
    return (
        <div>
            <Trending sessionId={localSessionId} />
            <Recommended sessionId={localSessionId} />
            <div className="credit">
                <p>Images powered by <a href="https://tmdb.org">TMDB</a></p>
            </div>
        </div>
    );
}
