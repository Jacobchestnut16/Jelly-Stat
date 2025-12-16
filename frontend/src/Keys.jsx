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

    // const appendSessionId = (url) => {
    //     if (!url) return null;
    //     const strUrl = String(url);
    //     if (!localSessionId) return strUrl;
    //     return strUrl.includes("?")
    //         ? `${strUrl}&session_id=${localSessionId}`
    //         : `${strUrl}?session_id=${localSessionId}`;
    // };

    const appendSessionId = (url) => {
        const sid = localSessionId || sessionId || localStorage.getItem("session_id");
        if (!sid) return url;
        return url.includes("?")
            ? `${url}&session_id=${sid}`
            : `${url}?session_id=${sid}`;
    };


    //
    // TMDB KEYS
    //
    const [tmdbKeys, setTmdbKeys] = useState([]);
    const [tmdbSelectedId, setTmdbSelectedId] = useState(null);
    const [tmdbNewKey, setTmdbNewKey] = useState("");
    const [tmdbLoading, setTmdbLoading] = useState(false);

    useEffect(() => {
        async function fetchTmdb() {
            try {
                const [allRes, selRes] = await Promise.all([
                    fetch(appendSessionId(`${API_BASE}/keys/tmdb/get`)),
                    fetch(appendSessionId(`${API_BASE}/keys/tmdb/get/selected`)),
                ]);

                if (allRes.ok) setTmdbKeys(await allRes.json());
                if (selRes.ok) {
                    const sel = await selRes.json();
                    setTmdbSelectedId(sel.id);
                }
            } catch (e) {}
        }
        fetchTmdb();
    }, [localSessionId]);

    async function addAndSelectTmdbKey() {
        if (!tmdbNewKey) return;
        setTmdbLoading(true);

        try {
            await fetch(appendSessionId(`${API_BASE}/keys/tmdb/add`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ api_key: tmdbNewKey }),
            });

            const all = await (await fetch(appendSessionId(`${API_BASE}/keys/tmdb/get`))).json();
            const newKeyObj = all.find((k) => k.api_key === tmdbNewKey);

            await fetch(appendSessionId(`${API_BASE}/keys/tmdb/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: newKeyObj.id,
                    session_id: localSessionId,
                }),
            });

            setTmdbKeys(all);
            setTmdbSelectedId(newKeyObj.id);
            setTmdbNewKey("");
        } finally {
            setTmdbLoading(false);
        }
    }

    async function selectTmdbKey(id) {
        setTmdbLoading(true);
        try {
            await fetch(appendSessionId(`${API_BASE}/keys/tmdb/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: id,
                    session_id: localSessionId,
                }),
            });
            setTmdbSelectedId(id);
        } finally {
            setTmdbLoading(false);
        }
    }

    //
    // JELLYSEERR KEYS
    //
    const [jellyKeys, setJellyKeys] = useState([]);
    const [jellySelectedId, setJellySelectedId] = useState(null);
    const [jellyNewKey, setJellyNewKey] = useState("");
    const [jellyLoading, setJellyLoading] = useState(false);

    useEffect(() => {
        async function fetchJelly() {
            try {
                const [allRes, selRes] = await Promise.all([
                    fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/get`)),
                    fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/get/selected`)),
                ]);

                if (allRes.ok) setJellyKeys(await allRes.json());
                if (selRes.ok) {
                    const sel = await selRes.json();
                    setJellySelectedId(sel.id);
                }
            } catch (e) {}
        }
        fetchJelly();
    }, [localSessionId]);

    async function addAndSelectJellyKey() {
        if (!jellyNewKey) return;
        setJellyLoading(true);

        try {
            await fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/add`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ api_key: jellyNewKey }),
            });

            const all = await (await fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/get`))).json();
            const newKeyObj = all.find((k) => k.api_key === jellyNewKey);

            await fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: newKeyObj.id,
                    session_id: localSessionId,
                }),
            });

            setJellyKeys(all);
            setJellySelectedId(newKeyObj.id);
            setJellyNewKey("");
        } finally {
            setJellyLoading(false);
        }
    }

    async function selectJellyKey(id) {
        setJellyLoading(true);

        try {
            await fetch(appendSessionId(`${API_BASE}/keys/jellyseerr/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: id,
                    session_id: localSessionId,
                }),
            });
            setJellySelectedId(id);
        } finally {
            setJellyLoading(false);
        }
    }

    //
    // JELLYSEERR URLS
    //
    const [jellyseerrUrls, setJellyseerrUrls] = useState([]);
    const [jellyseerrUrlSelectedId, setJellyseerrUrlSelectedId] = useState(null);
    const [jellyseerrNewUrl, setJellyseerrNewUrl] = useState("");
    const [jellyseerrUrlLoading, setJellyseerrUrlLoading] = useState(false);

    useEffect(() => {
        async function fetchUrls() {
            try {
                const [allRes, selRes] = await Promise.all([
                    fetch(appendSessionId(`${API_BASE}/urls/jellyseerr/get`)),
                    fetch(appendSessionId(`${API_BASE}/urls/jellyseerr/get/selected`)),
                ]);

                if (allRes.ok) setJellyseerrUrls(await allRes.json());
                if (selRes.ok) {
                    const sel = await selRes.json();
                    setJellyseerrUrlSelectedId(sel.url_id);
                }
            } catch (e) {}
        }
        fetchUrls();
    }, [localSessionId]);

    async function addAndSelectJellyseerrUrl() {
        if (!jellyseerrNewUrl) return;
        setJellyseerrUrlLoading(true);

        try {
            await fetch(appendSessionId(`${API_BASE}/urls/jellyseerr/add`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: jellyseerrNewUrl }),
            });

            const all = await (await fetch(appendSessionId(`${API_BASE}/urls/jellyseerr/get`))).json();
            const newObj = all.find((u) => u.url === jellyseerrNewUrl);

            await fetch(appendSessionId(`${API_BASE}/urls/jellyseerr/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url_id: newObj.id,
                    session_id: localSessionId,
                }),
            });

            setJellyseerrUrls(all);
            setJellyseerrUrlSelectedId(newObj.id);
            setJellyseerrNewUrl("");
        } finally {
            setJellyseerrUrlLoading(false);
        }
    }

    async function selectJellyseerrUrl(id) {
        setJellyseerrUrlLoading(true);

        try {
            await fetch(appendSessionId(`${API_BASE}/urls/jellyseerr/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url_id: id,
                    session_id: localSessionId,
                }),
            });
            setJellyseerrUrlSelectedId(id);
        } finally {
            setJellyseerrUrlLoading(false);
        }
    }

    //
    // JELLYFIN KEYS
    //
    const [jellyfinKeys, setJellyfinKeys] = useState([]);
    const [jellyfinKeySelectedId, setJellyfinKeySelectedId] = useState(null);
    const [jellyfinNewKey, setJellyfinNewKey] = useState("");
    const [jellyfinKeyLoading, setJellyfinKeyLoading] = useState(false);

    useEffect(() => {
        async function fetchFinKeys() {
            try {
                const [allRes, selRes] = await Promise.all([
                    fetch(appendSessionId(`${API_BASE}/keys/jellyfin/get`)),
                    fetch(appendSessionId(`${API_BASE}/keys/jellyfin/get/selected`)),
                ]);

                if (allRes.ok) {
                    const all = await allRes.json();
                    console.log(all)
                    setJellyfinKeys(all);
                }
                if (selRes.ok) {
                    const sel = await selRes.json();
                    setJellyfinKeySelectedId(sel.id);
                }
            } catch (e) {}
        }
        fetchFinKeys();

    }, [localSessionId]);

    async function addAndSelectJellyfinKey() {
        if (!jellyfinNewKey) return;
        setJellyfinKeyLoading(true);

        try {
            await fetch(appendSessionId(`${API_BASE}/keys/jellyfin/add`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ api_key: jellyfinNewKey }),
            });

            const all = await (await fetch(appendSessionId(`${API_BASE}/keys/jellyfin/get`))).json();
            const newObj = all.find((k) => k.api_key === jellyfinNewKey);

            await fetch(appendSessionId(`${API_BASE}/keys/jellyfin/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: newObj.id,
                    session_id: localSessionId,
                }),
            });

            setJellyfinKeys(all);
            setJellyfinKeySelectedId(newObj.id);
            setJellyfinNewKey("");
        } finally {
            setJellyfinKeyLoading(false);
        }
    }

    async function selectJellyfinKey(id) {
        setJellyfinKeyLoading(true);

        try {
            await fetch(appendSessionId(`${API_BASE}/keys/jellyfin/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    api_key_id: id,
                    session_id: localSessionId,
                }),
            });
            setJellyfinKeySelectedId(id);
        } finally {
            setJellyfinKeyLoading(false);
        }
    }

    //
    // JELLYFIN URLS
    //
    const [jellyfinUrls, setJellyfinUrls] = useState([]);
    const [jellyfinUrlSelectedId, setJellyfinUrlSelectedId] = useState(null);
    const [jellyfinNewUrl, setJellyfinNewUrl] = useState("");
    const [jellyfinUrlLoading, setJellyfinUrlLoading] = useState(false);

    useEffect(() => {
        async function fetchFinUrls() {
            try {
                const [allRes, selRes] = await Promise.all([
                    fetch(appendSessionId(`${API_BASE}/urls/jellyfin/get`)),
                    fetch(appendSessionId(`${API_BASE}/urls/jellyfin/get/selected`)),
                ]);

                if (allRes.ok) setJellyfinUrls(await allRes.json());
                if (selRes.ok) {
                    const sel = await selRes.json();
                    setJellyfinUrlSelectedId(sel.id);
                }
            } catch (e) {}
        }
        fetchFinUrls();
    }, [localSessionId]);

    async function addAndSelectJellyfinUrl() {
        if (!jellyfinNewUrl) return;
        setJellyfinUrlLoading(true);

        try {
            await fetch(appendSessionId(`${API_BASE}/urls/jellyfin/add`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: jellyfinNewUrl }),
            });

            const all = await (await fetch(appendSessionId(`${API_BASE}/urls/jellyfin/get`))).json();
            const newObj = all.find((u) => u.url === jellyfinNewUrl);

            await fetch(appendSessionId(`${API_BASE}/urls/jellyfin/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url_id: newObj.id,
                    session_id: localSessionId,
                }),
            });

            setJellyfinUrls(all);
            setJellyfinUrlSelectedId(newObj.id);
            setJellyfinNewUrl("");
        } finally {
            setJellyfinUrlLoading(false);
        }
    }

    async function selectJellyfinUrl(id) {
        setJellyfinUrlLoading(true);

        try {
            await fetch(appendSessionId(`${API_BASE}/urls/jellyfin/select`), {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url_id: id,
                    session_id: localSessionId,
                }),
            });
            setJellyfinUrlSelectedId(id);
        } finally {
            setJellyfinUrlLoading(false);
        }
    }

    return (
        <div className="settings-wrap">
            <div className="settings-card">
                <h2>TMDB</h2>

                <h4>TMDB Keys</h4>
                <select
                    disabled={tmdbLoading}
                    value={tmdbSelectedId || ""}
                    onChange={(e) => selectTmdbKey(Number(e.target.value))}
                >
                    <option value="" disabled>Select TMDB Key</option>
                    {tmdbKeys.map(({ id, api_key }) => (
                        <option key={id} value={id}>{api_key}</option>
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
                    <button onClick={addAndSelectTmdbKey} disabled={tmdbLoading || !tmdbNewKey}>Add</button>
                </div>

                <h2>Jellyseerr</h2>

                <h4>Jellyseerr Keys</h4>
                <select
                    disabled={jellyLoading}
                    value={jellySelectedId || ""}
                    onChange={(e) => selectJellyKey(Number(e.target.value))}
                >
                    <option value="" disabled>Select Jellyseerr Key</option>
                    {jellyKeys.map(({ id, api_key }) => (
                        <option key={id} value={id}>{api_key}</option>
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
                    <button onClick={addAndSelectJellyKey} disabled={jellyLoading || !jellyNewKey}>Add</button>
                </div>

                <h4>Jellyseerr URL</h4>
                <select
                    disabled={jellyseerrUrlLoading}
                    value={jellyseerrUrlSelectedId || ""}
                    onChange={(e) => selectJellyseerrUrl(Number(e.target.value))}
                >
                    <option value="" disabled>Select Jellyseerr URL</option>
                    {jellyseerrUrls.map(({ id, url }) => (
                        <option key={id} value={id}>{url}</option>
                    ))}
                </select>

                <div className="settings-row">
                    <input
                        type="text"
                        placeholder="Add new Jellyseerr URL"
                        value={jellyseerrNewUrl}
                        onChange={(e) => setJellyseerrNewUrl(e.target.value)}
                        disabled={jellyseerrUrlLoading}
                    />
                    <button onClick={addAndSelectJellyseerrUrl} disabled={jellyseerrUrlLoading || !jellyseerrNewUrl}>Add</button>
                </div>

                <h2>Jellyfin</h2>

                <h4>Jellyfin Keys</h4>
                <select
                    disabled={jellyfinKeyLoading}
                    value={jellyfinKeySelectedId || ""}
                    onChange={(e) => selectJellyfinKey(Number(e.target.value))}
                >
                    <option value="" disabled>Select Jellyfin Key</option>
                    {jellyfinKeys.map(({ id, jellyfin_key }) => (
                        <option key={id} value={id}>{jellyfin_key}</option>
                    ))}
                </select>

                <div className="settings-row">
                    <input
                        type="text"
                        placeholder="Add new Jellyfin key"
                        value={jellyfinNewKey}
                        onChange={(e) => setJellyfinNewKey(e.target.value)}
                        disabled={jellyfinKeyLoading}
                    />
                    <button onClick={addAndSelectJellyfinKey} disabled={jellyfinKeyLoading || !jellyfinNewKey}>Add</button>
                </div>

                <h4>Jellyfin URL</h4>
                <select
                    disabled={jellyfinUrlLoading}
                    value={jellyfinUrlSelectedId || ""}
                    onChange={(e) => selectJellyfinUrl(Number(e.target.value))}
                >
                    <option value="" disabled>Select Jellyfin URL</option>
                    {jellyfinUrls.map(({ id, url }) => (
                        <option key={id} value={id}>{url}</option>
                    ))}
                </select>

                <div className="settings-row">
                    <input
                        type="text"
                        placeholder="Add new Jellyfin URL"
                        value={jellyfinNewUrl}
                        onChange={(e) => setJellyfinNewUrl(e.target.value)}
                        disabled={jellyfinUrlLoading}
                    />
                    <button onClick={addAndSelectJellyfinUrl} disabled={jellyfinUrlLoading || !jellyfinNewUrl}>Add</button>
                </div>
            </div>
        </div>
    );
}
