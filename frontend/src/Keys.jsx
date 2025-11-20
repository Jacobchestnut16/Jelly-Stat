import { useEffect, useState } from "react";

const API_BASE = "http://localhost:3001";

export default function Keys({ sessionId }) {
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

    // Append ?session_id=... safely
    const appendSessionId = (url) => {
        if (!url) return null;
        const strUrl = String(url);
        if (!localSessionId) return strUrl;
        return strUrl.includes("?")
            ? `${strUrl}&session_id=${localSessionId}`
            : `${strUrl}?session_id=${localSessionId}`;
    };

    const [tmdbKeys, setTmdbKeys] = useState([]);
    const [tmdbSelectedId, setTmdbSelectedId] = useState(null);
    const [tmdbNewKey, setTmdbNewKey] = useState("");
    const [tmdbLoading, setTmdbLoading] = useState(false);

    const [jellyKeys, setJellyKeys] = useState([]);
    const [jellySelectedId, setJellySelectedId] = useState(null);
    const [jellyNewKey, setJellyNewKey] = useState("");
    const [jellyLoading, setJellyLoading] = useState(false);

    // Fetch TMDB keys
    useEffect(() => {
        async function fetchTmdb() {
            try {
                const [allRes, selRes] = await Promise.all([
                    fetch(appendSessionId(`${API_BASE}/keys/tmdb/get`)),
                    fetch(appendSessionId(`${API_BASE}/keys/tmdb/get/selected`)),
                ]);
                if (allRes.ok) {
                    const all = await allRes.json();
                    setTmdbKeys(all);
                }
                if (selRes.ok) {
                    const sel = await selRes.json();
                    setTmdbSelectedId(sel.id);
                }
            } catch (e) {
                console.error("Failed fetching TMDB keys", e);
            }
        }
        fetchTmdb();
    }, [localSessionId]);

    // Fetch Jellyseerr keys
    useEffect(() => {
        async function fetchJelly() {
            try {
                const [allRes, selRes] = await Promise.all([
                    fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/get`)),
                    fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/get/selected`)),
                ]);
                if (allRes.ok) {
                    const all = await allRes.json();
                    setJellyKeys(all);
                }
                if (selRes.ok) {
                    const sel = await selRes.json();
                    setJellySelectedId(sel.id);
                }
            } catch (e) {
                console.error("Failed fetching Jellyseerr keys", e);
            }
        }
        fetchJelly();
    }, [localSessionId]);

    //
    // TMDB
    //
    async function addAndSelectTmdbKey() {
        if (!tmdbNewKey) return;
        setTmdbLoading(true);
        try {
            const addRes = await fetch(appendSessionId(`${API_BASE}/keys/tmdb/add`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ api_key: tmdbNewKey }),
            });
            if (!addRes.ok) throw new Error("Failed to add TMDB key");

            const allRes = await fetch(appendSessionId(`${API_BASE}/keys/tmdb/get`));
            const all = await allRes.json();

            const newKeyObj = all.find((k) => k.api_key === tmdbNewKey);
            if (!newKeyObj) throw new Error("New key not found after adding");

            // FIXED: include session_id
            const selectRes = await fetch(appendSessionId(`${API_BASE}/keys/tmdb/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: newKeyObj.id,
                    session_id: localSessionId,
                }),
            });
            if (!selectRes.ok) throw new Error("Failed to select TMDB key");

            setTmdbSelectedId(newKeyObj.id);
            setTmdbKeys(all);
            setTmdbNewKey("");
        } catch (e) {
            alert(e.message);
        } finally {
            setTmdbLoading(false);
        }
    }

    async function selectTmdbKey(id) {
        setTmdbLoading(true);
        try {
            const res = await fetch(appendSessionId(`${API_BASE}/keys/tmdb/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: id,
                    session_id: localSessionId,  // FIXED
                }),
            });
            if (!res.ok) throw new Error("Failed to select TMDB key");
            setTmdbSelectedId(id);
        } catch (e) {
            alert(e.message);
        } finally {
            setTmdbLoading(false);
        }
    }

    //
    // JELLYSEERR
    //
    async function addAndSelectJellyKey() {
        if (!jellyNewKey) return;
        setJellyLoading(true);
        try {
            const addRes = await fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/add`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ api_key: jellyNewKey }),
            });
            if (!addRes.ok) throw new Error("Failed to add Jellyseerr key");

            const allRes = await fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/get`));
            const all = await allRes.json();

            const newKeyObj = all.find((k) => k.api_key === jellyNewKey);
            if (!newKeyObj) throw new Error("New key not found after adding");

            // FIXED: include session_id
            const selectRes = await fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: newKeyObj.id,
                    session_id: localSessionId,
                }),
            });
            if (!selectRes.ok) throw new Error("Failed to select Jellyseerr key");

            setJellySelectedId(newKeyObj.id);
            setJellyKeys(all);
            setJellyNewKey("");
        } catch (e) {
            alert(e.message);
        } finally {
            setJellyLoading(false);
        }
    }

    async function selectJellyKey(id) {
        setJellyLoading(true);
        try {
            const res = await fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: id,
                    session_id: localSessionId, // FIXED
                }),
            });
            if (!res.ok) throw new Error("Failed to select Jellyseerr key");
            setJellySelectedId(id);
        } catch (e) {
            alert(e.message);
        } finally {
            setJellyLoading(false);
        }
    }

    return (
        <div className="settings-wrap">
            <div className="settings-card">
                <h2>TMDB Keys</h2>

                <select
                    disabled={tmdbLoading}
                    value={tmdbSelectedId || ""}
                    onChange={(e) => selectTmdbKey(Number(e.target.value))}
                >
                    <option value="" disabled>Select TMDB Key</option>
                    {tmdbKeys.map(({ id, api_key }) => (
                        <option key={id} value={id}>
                            {api_key}
                        </option>
                    ))}
                </select>

                <div className="settings-row">
                    <input
                        type="text"
                        placeholder="Add new TMDB key"
                        value={tmdbNewKey}
                        onChange={(e) => setTmdbNewKey(e.target.value)}
                        disabled={tmdbLoading}
                    />
                    <button onClick={addAndSelectTmdbKey} disabled={tmdbLoading || !tmdbNewKey}>
                        Add
                    </button>
                </div>

                <h2>Jellyseerr Keys</h2>

                <select
                    disabled={jellyLoading}
                    value={jellySelectedId || ""}
                    onChange={(e) => selectJellyKey(Number(e.target.value))}
                >
                    <option value="" disabled>Select Jellyseerr Key</option>
                    {jellyKeys.map(({ id, api_key }) => (
                        <option key={id} value={id}>
                            {api_key}
                        </option>
                    ))}
                </select>

                <div className="settings-row">
                    <input
                        type="text"
                        placeholder="Add new Jellyseerr key"
                        value={jellyNewKey}
                        onChange={(e) => setJellyNewKey(e.target.value)}
                        disabled={jellyLoading}
                    />
                    <button onClick={addAndSelectJellyKey} disabled={jellyLoading || !jellyNewKey}>
                        Add
                    </button>
                </div>
            </div>
        </div>
    );

}
