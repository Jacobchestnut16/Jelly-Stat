var API_BASE = import.meta.env.VITE_API_BASE;

if (API_BASE == null)
    API_BASE = "http://localhost:3001";

const BASE = API_BASE+"/jellyseerr";//"http://localhost:3001/jellyseerr";

console.log("Base found at "+API_BASE);

function withSession(url, sessionId) {
    if (!sessionId) return url;
    const sep = url.includes("?") ? "&" : "?";
    return `${url}${sep}session_id=${sessionId}`;
}

export async function getJellyseerr(params = {}, archived = false, sessionId) {
    const q = new URLSearchParams(params).toString();
    const base = archived ? `${BASE}/archived` : `${BASE}/`;

    const url = withSession(
        q ? `${base}?${q}` : base,
        sessionId
    );

    const r = await fetch(url);
    if (!r.ok) throw new Error("Jellyseerr fetch failed");
    return r.json();
}

export async function getJellyseerrRaw(tmdbId, sessionId) {
    const url = withSession(
        `${BASE}/raw/${tmdbId}`,
        sessionId
    );

    const r = await fetch(url);
    if (!r.ok) throw new Error("Not found");
    return r.json();
}
