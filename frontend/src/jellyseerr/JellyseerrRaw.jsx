import { useEffect, useState } from "react";
import { getJellyseerrRaw } from "./api";

export default function JellyseerrRaw({ sessionId, tmdbId }) {
    const [data, setData] = useState(null);

    useEffect(() => {
        if (!tmdbId) return;
        getJellyseerrRaw(tmdbId, sessionId).then(setData);
    }, [tmdbId]);

    if (!data) return null;

    return (
        <div className="jellyseerr-raw">
            <h3>{data.title}</h3>

            <div style={{ display: "flex", gap: "1rem" }}>
                <img src={data.images.poster} style={{ height: 400 }} />

                <table>
                    <tbody>
                    {Object.entries(data.summary).map(([k, v]) => (
                        <tr key={k}>
                            <th>{k}</th>
                            <td>{String(v)}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>

            <div className="lookups">
                {Object.entries(data.lookups).map(([k, v]) => (
                    <a key={k} href={v}>{k}</a>
                ))}
            </div>
        </div>
    );
}
