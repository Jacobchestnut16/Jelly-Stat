import { useEffect, useState } from "react";

export default function UserDetails({ sessionId }) {
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


    const [userInfo, setUserInfo] = useState(null);
    const [userTraktInfo, setUserTraktInfo] = useState(null);
    const [loading, setLoading] = useState(true);

    // Fetch user details
    useEffect(() => {
        async function load() {
                        const appendSessionId = (url) => {
                if (!url) return null;
                if (!localSessionId) return url; // no auth needed or no sessionId
                return url.includes("?") ? `${url}&session_id=${localSessionId}` : `${url}?session_id=${localSessionId}`;
            };
            try {
                const res = await fetch(appendSessionId("http://localhost:3001/user/details"));
                if (!res.ok) throw new Error("Failed");
                const data = await res.json();
                setUserInfo(data);
            } catch (_) {}
        }
        load();
    }, []);

    // Fetch trakt login info
    useEffect(() => {
        async function load() {
                        const appendSessionId = (url) => {
                if (!url) return null;
                if (!localSessionId) return url; // no auth needed or no sessionId
                return url.includes("?") ? `${url}&session_id=${localSessionId}` : `${url}?session_id=${localSessionId}`;
            };
            try {
                const res = await fetch(appendSessionId("http://localhost:3001/user/trakt_login_info"));
                if (!res.ok) throw new Error("Failed");
                const data = await res.json();
                setUserTraktInfo(data);
            } catch (_) {}
        }
        load();
    }, []);

    // Combine loading logic
    useEffect(() => {
        if (userInfo !== null && userTraktInfo !== null) {
            setLoading(false);
        }
    }, [userInfo, userTraktInfo]);

    if (loading) return <h1>Loading...</h1>;

    return (
        <div>
            <h1>{userInfo.user.name}</h1>
            <div style={{display: "flex", flexDirection: "column", maxWidth: "500px", gap: "10px"}}>
                <h2>Trakt Info</h2>
                <div>
                    <table>
                        <tr>
                            <td>
                                <h3>Client ID</h3>
                            </td>
                            <td>
                                <input
                                    type="text"
                                    readOnly
                                    value={userTraktInfo.trakt_client_id || ""}
                                    style={{width: "350px"}}
                                />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <h3>Client Secret</h3>
                            </td>
                            <td>
                                <input
                                    type="password"
                                    readOnly
                                    value={userTraktInfo.trakt_client_secret || ""}
                                    style={{width: "350px"}}

                                />
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
            {userInfo.user.vip ? <h3>Trakt VIP User</h3> : null}

        </div>
    );
}
