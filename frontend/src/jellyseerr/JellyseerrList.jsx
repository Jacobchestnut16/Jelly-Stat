import { useEffect, useState } from "react";
import { getJellyseerr } from "./api";
import JellyseerrSummary from "./JellyseerrSummary";

export default function JellyseerrList({ sessionId, archived = false, onSelect }) {
    const [items, setItems] = useState([]);
    const [summary, setSummary] = useState(null);
    const [filters, setFilters] = useState({ type: "", title: "" });

    useEffect(() => {
        getJellyseerr(filters, archived, sessionId).then(r => {
            setItems(r.results);
            setSummary(r.summary);
        });
    }, [filters, archived, sessionId]);

    return (
        <div className="settings-wrap">
            <div className="settings-card jellyseerr js-settings-width">

                <form
                    className="js-filters"
                    onSubmit={e => {
                        e.preventDefault();
                        setFilters({
                            type: e.target.type.value,
                            title: e.target.title.value,
                        });
                    }}
                >
                    <div>
                        <label>Type</label>
                        <select name="type">
                            <option value="">All</option>
                            <option value="movie">Movie</option>
                            <option value="tv">TV</option>
                        </select>
                    </div>

                    <div>
                        <label>Title</label>
                        <input name="title" placeholder="Search title" />
                    </div>

                    <button type="submit">Apply</button>
                </form>

                <JellyseerrSummary summary={summary} />

                <table className="js-table">
                    <thead>
                    <tr>
                        <th>Type</th>
                        <th>Owned</th>
                        <th>Title</th>
                        <th />
                        {!archived && <th>Lookups</th>}
                    </tr>
                    </thead>
                    <tbody>
                    {items.map(d => (
                        <tr key={d.tmdb_id}>
                            <td>{d.type}</td>
                            <td className={`owned ${d.jellyfin_media_id ? "yes" : "no"}`}>
                                {d.jellyfin_media_id ? "owned" : "unowned"}
                            </td>
                            <td>{d.title}</td>
                            <td className="actions">
                                <button
                                    className="view-btn"
                                    onClick={() => onSelect?.(d.tmdb_id)}
                                >
                                    View
                                </button>
                            </td>
                            {!archived && (
                                <td className="lookups">
                                    {Object.entries(d.lookups).map(([k, v]) => (
                                        <a
                                            key={k}
                                            className="lookup-link"
                                            href={v}
                                            target="_blank"
                                            rel="noreferrer"
                                        >
                                            {k}
                                        </a>
                                    ))}
                                </td>
                            )}
                        </tr>
                    ))}
                    </tbody>
                </table>

            </div>
        </div>
    );
}
