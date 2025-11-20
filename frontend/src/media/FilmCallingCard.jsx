import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const TMDB_IMG = "https://image.tmdb.org/t/p/w500";

export default function FilmCallingCard({ sessionId }) {
    const { tmdb_id } = useParams();
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

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

    useEffect(() => {
        async function load() {
            const appendSessionId = (url) => {
                if (!url) return null;
                if (!localSessionId) return url; // no auth needed or no sessionId
                return url.includes("?") ? `${url}&session_id=${localSessionId}` : `${url}?session_id=${localSessionId}`;
            };

            try {
                const res = await fetch(appendSessionId(`http://localhost:3001/media/movie/${tmdb_id}`));
                if (!res.ok) {
                    throw new Error("Request failed");
                }
                const json = await res.json();
                setData(json);
            } catch (err) {
                setError(err.message);
            }
        }
        load();
    }, [tmdb_id]);

    if (error) return <div>Error: {error}</div>;
    if (!data) return <div>Loading...</div>;

    const poster = data.poster_path ? TMDB_IMG + data.poster_path : null;
    const backdrop = data.backdrop_path ? TMDB_IMG + data.backdrop_path : null;
    const year = data.release_date ? data.release_date.slice(0, 4) : "";

    return (
        <div className="film-card">

            {backdrop && (
                <div
                    className="film-backdrop"
                    style={{
                        backgroundImage: `url(${backdrop})`,
                        backgroundSize: "cover",
                        backgroundPosition: "center",
                        width: "100%",
                        height: "300px",
                        borderRadius: "8px",
                    }}
                />
            )}

            <div className="film-content" style={{ display: "flex", gap: "20px", marginTop: "20px" }}>

                {poster && (
                    <img
                        src={poster}
                        alt={data.title}
                        style={{ width: "200px", borderRadius: "8px" }}
                    />
                )}

                <div>
                    <h1>{data.title} {year && `(${year})`}</h1>

                    {data.tagline && (
                        <h3 style={{ fontStyle: "italic", opacity: 0.8 }}>
                            {data.tagline}
                        </h3>
                    )}

                    <p>{data.overview}</p>

                    <div style={{ marginTop: "10px" }}>
                        <div>Runtime: {data.runtime} min</div>
                        <div>Status: {data.status}</div>
                        {data.vote_average && <div>Rating: {data.vote_average}</div>}
                    </div>

                    <div style={{ marginTop: "10px", display: "flex", gap: "8px", flexWrap: "wrap" }}>
                        {data.genres?.map(g => (
                            <span key={g.id} style={{
                                background: "#eee",
                                padding: "4px 8px",
                                borderRadius: "6px",
                                fontSize: "0.9rem"
                            }}>
                                {g.name}
                            </span>
                        ))}
                    </div>
                </div>

            </div>
        </div>
    );
}
