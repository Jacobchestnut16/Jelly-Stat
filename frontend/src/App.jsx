import { useState, useEffect, useRef } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import MediaPage from "./MediaPage.jsx";
import Login from "./Login.jsx";
import Register from "./Register.jsx";
import Keys from "./Keys.jsx";
import UserDetails from "./UserDetails.jsx";
import Movies from "./Movies.jsx";
import Shows from "./Shows.jsx";
import FilmCallingCard from "./media/FilmCallingCard.jsx";

export default function App() {
    // Store sessionId from localStorage (was user_id before)
    const [sessionId, setSessionId] = useState(() => localStorage.getItem("session_id"));
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [pendingTrakt, setPendingTrakt] = useState(
        localStorage.getItem("pending_trakt") === "1"
    );
    const [pendingRedirect, setPendingRedirect] = useState(
        localStorage.getItem("pending_redirect") || ""
    );
    const [userInfo, setUserInfo] = useState(null);
    const dropdownRef = useRef(null);

    async function logout() {
        try {
            await fetch(`http://localhost:3001/auth/logout?session_id=${sessionId}`, { method: "GET" });
        } catch (_) {}

        localStorage.removeItem("session_id");
        localStorage.removeItem("pending_trakt");
        localStorage.removeItem("pending_redirect");

        setSessionId(null);
        setPendingTrakt(false);
        setPendingRedirect("");
        setUserInfo(null);

        window.location.href = "/";
    }


    useEffect(() => {
        // Update sessionId when localStorage changes (ex. login from other tabs)
        const handler = () => setSessionId(localStorage.getItem("session_id"));
        window.addEventListener("storage", handler);
        return () => window.removeEventListener("storage", handler);
    }, []);

    // If a Trakt OAuth redirect is pending, run it
// Validate session + run pending redirect
    useEffect(() => {
        async function validateAndRedirect() {
            if (!sessionId) return;

            try {
                const res = await fetch(
                    `http://localhost:3001/auth/validate?session_id=${sessionId}`
                );
                if (res.status === 401) {
                    await logout();
                    return;
                }
            } catch (_) {
                await logout();
                return;
            }

            if (pendingTrakt && pendingRedirect) {
                window.location.href = pendingRedirect;
            }
        }

        validateAndRedirect();
    }, [sessionId, pendingTrakt, pendingRedirect]);


    // Load user details whenever sessionId changes
    useEffect(() => {
        if (!sessionId) {
            setUserInfo(null);
            return;
        }

        if (pendingTrakt) return;

        async function loadUser() {
            try {
                const res = await fetch(
                    `http://localhost:3001/user/details?session_id=${sessionId}`
                );

                if (res.status === 401) {
                    console.warn("Could not retrieve User Details, Trakt may not be logged in")
                    const res = await fetch(
                        `http://localhost:3001/auth/validate?session_id=${sessionId}`
                    );
                    if (res.status === 200){
                        console.warn("Session is Valid trying to log into Trakt")
                        if (pendingRedirect) {
                            var pndRdrt = pendingRedirect
                            localStorage.removeItem("pending_trakt");
                            localStorage.removeItem("pending_redirect");
                            setPendingTrakt(false);
                            setPendingRedirect("");
                            window.location.href = pndRdrt;
                        }else{
                            console.error("No Trakt URL")
                            await logout();
                            return;
                        }
                    }else{
                        console.error("INVALID SESSION logging out")
                        await logout();
                        return;
                    }
                }

                const data = await res.json();
                setUserInfo(data);
            } catch (_) {
                await logout();
            }
        }

        loadUser();
    }, [sessionId, pendingTrakt]);


    // Close dropdown when clicking outside
    useEffect(() => {
        function handleClickOutside(e) {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
                setDropdownOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    return (
        <BrowserRouter>
            <div style={{display: "flex", flexDirection: "column", minHeight: "100vh"}}>
                <nav>
                    <ul>
                        <li><Link to="/">Jelly-Stat</Link></li>
                        <li><Link to="/movies">Movies</Link></li>
                        <li><Link to="/shows">Shows</Link></li>
                    </ul>

                    <ul>
                        {sessionId ? (
                            <>
                                {/*<li><a href="#ADR">ADR</a></li>*/}
                                <li ref={dropdownRef} style={{position: "relative", listStyle: "none"}}>
                                    {userInfo?.user?.images?.avatar?.full ? (
                                        <div
                                            style={{
                                                cursor: "pointer",
                                                display: "inline-flex",
                                                alignItems: "center",
                                                padding: "0 6px",
                                            }}
                                            onClick={() => setDropdownOpen((open) => !open)}
                                            tabIndex={0}
                                        >
                                            <img
                                                src={userInfo.user.images.avatar.full}
                                                alt="User avatar"
                                                style={{width: "35px", borderRadius: "5%"}}
                                            />
                                        </div>
                                    ) : (
                                        <div
                                            style={{
                                                color: "#eee",
                                                padding: "0 8px",
                                                cursor: "pointer",
                                                display: "inline-flex",
                                                alignItems: "center",
                                            }}
                                            onClick={() => setDropdownOpen((open) => !open)}
                                            tabIndex={0}
                                        >
                                            Settings
                                        </div>
                                    )}

                                    {dropdownOpen && (
                                        <ul
                                            style={{
                                                position: "absolute",
                                                top: "100%",
                                                right: 0,
                                                background: "#1a1a1a",
                                                padding: "8px 0",
                                                margin: 0,
                                                listStyle: "none",
                                                borderRadius: "4px",
                                                boxShadow: "0 2px 6px rgba(0,0,0,0.5)",
                                                minWidth: "150px",
                                                zIndex: 1000,
                                                display: "block",
                                            }}
                                        >
                                            <li style={{padding: "8px 16px"}}>
                                                <Link
                                                    to="/user-details"
                                                    style={{color: "#eee", textDecoration: "none"}}
                                                    onClick={() => setDropdownOpen(false)}
                                                >
                                                    User Details
                                                </Link>
                                            </li>

                                            <li style={{padding: "8px 16px"}}>
                                                <Link
                                                    to="/keys"
                                                    style={{color: "#eee", textDecoration: "none"}}
                                                    onClick={() => setDropdownOpen(false)}
                                                >
                                                    API-Settings
                                                </Link>
                                            </li>

                                            <li style={{padding: "8px 16px"}}>
                                                <button
                                                    onClick={() => {
                                                        setDropdownOpen(false);
                                                        logout();
                                                    }}
                                                    style={{
                                                        background: "none",
                                                        border: "none",
                                                        color: "#eee",
                                                        width: "100%",
                                                        textAlign: "left",
                                                        cursor: "pointer",
                                                        fontSize: "inherit",
                                                        padding: 0,
                                                    }}
                                                >
                                                    Logout
                                                </button>
                                            </li>
                                        </ul>
                                    )}
                                </li>
                            </>
                        ) : (
                            <>
                                <li><Link to="/login">Login</Link></li>
                                <li><Link to="/register">Register</Link></li>
                            </>
                        )}
                    </ul>
                </nav>
                <div style={{flexGrow: 1}}>
                    <Routes>
                        <Route path="/" element={<MediaPage sessionId={sessionId}/>}/>
                        <Route path="/movies" element={<Movies sessionId={sessionId}/>}/>
                        <Route path="/shows" element={<Shows sessionId={sessionId}/>}/>
                        <Route path="/keys" element={<Keys sessionId={sessionId}/>}/>
                        <Route path="/user-details" element={<UserDetails sessionId={sessionId}/>}/>
                        <Route path="/login" element={<Login setSessionId={setSessionId}
                                                             setPendingTrakt={setPendingTrakt}
                                                             setPendingRedirect={setPendingRedirect}/>}/>
                        <Route path="/register" element={<Register setSessionId={setSessionId}/>}/>
                        <Route path="/movie/:tmdb_id" element={<FilmCallingCard sessionId={sessionId}/>}/>
                        <Route path="/show/:tmdb_id" element={<FilmCallingCard type="show" sessionId={sessionId}/>}/>
                    </Routes>
                </div>
            </div>
        </BrowserRouter>
);
}
