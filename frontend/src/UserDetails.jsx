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
        <div className="settings-wrap">
            <div className="settings-card">
                <h2>User Details</h2>
                <h3 style={{textAlign: "left", margin: 0}}>{userInfo.user.name}</h3>

                <table className="settings-table">
                    <tbody>
                    <tr>
                        <td className="settings-label">Username</td>
                        <td>
                            <input
                                className="settings-input"
                                type="text"
                                value={userTraktInfo.username || ""}
                                readOnly
                            />
                        </td>
                    </tr>

                    <tr>
                        <td className="settings-label">Password</td>
                        <td>
                            <input
                                className="settings-input"
                                type="password"
                                value={userTraktInfo.pass || ""}
                                readOnly
                            />
                        </td>
                    </tr>
                    </tbody>
                </table>

                <h2 className="settings-section-title">Trakt Info</h2>
                {userInfo.user.vip ? (
                    <h3 style={{textAlign: "left", marginTop: "10px"}}>
                        Trakt VIP User
                    </h3>
                ) : null}
                <table className="settings-table">
                    <tbody>
                    <tr>
                        <td className="settings-label">Client ID</td>
                        <td>
                            <input
                                className="settings-input"
                                type="text"
                                readOnly
                                value={userTraktInfo.trakt_client_id || ""}
                            />
                        </td>
                    </tr>

                    <tr>
                        <td className="settings-label">Client Secret</td>
                        <td>
                            <input
                                className="settings-input"
                                type="password"
                                readOnly
                                value={userTraktInfo.trakt_client_secret || ""}
                            />
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}
