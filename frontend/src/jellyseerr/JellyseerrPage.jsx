import { useEffect, useState } from "react";
import JellyseerrList from "./JellyseerrList";
import JellyseerrRaw from "./JellyseerrRaw";

export default function JellyseerrPage({ sessionId, archived = false }) {
    const [localSessionId, setLocalSessionId] = useState(sessionId);
    const [selected, setSelected] = useState(null);

    useEffect(() => {
        setLocalSessionId(sessionId);
    }, [sessionId]);

    useEffect(() => {
        const handler = () =>
            setLocalSessionId(localStorage.getItem("session_id"));

        window.addEventListener("storage", handler);
        return () => window.removeEventListener("storage", handler);
    }, []);

    return (
        <>
            <JellyseerrList
                archived={archived}
                sessionId={localSessionId}
                onSelect={setSelected}
            />
            <JellyseerrRaw
                tmdbId={selected}
                sessionId={localSessionId}
            />
        </>
    );
}
