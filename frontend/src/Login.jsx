import { useState } from "react";
import {redirect, useNavigate} from "react-router-dom";

export default function Login({ setSessionId, setPendingTrakt, setPendingRedirect }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const [showPass, setShowPass] = useState(false);
    const navigate = useNavigate();

    async function handleLogin(e) {
        e.preventDefault();
        setMessage("");

        try {
            console.log("Start")

            const res = await fetch(
                `http://localhost:3001/auth/signin?username=${encodeURIComponent(
                    username
                )}&password=${encodeURIComponent(password)}`
            );

            const data = await res.json();

            if (!res.ok) throw new Error(data.detail || "Login failed");

            console.log(data)

            // Save to localStorage + update App state
            localStorage.setItem("session_id", data.session_id);
            localStorage.setItem("pending_trakt", data.needs_trakt_login ? "1" : "0");
            localStorage.setItem("pending_redirect", data.redirect || "");

            setSessionId(data.session_id);
            + setPendingTrakt(data.needs_trakt_login);
            + setPendingRedirect(data.redirect || "");

            navigate("/")
        } catch (err) {
            setMessage(err.message);
        }
    }

    return (
        <div
            className="auth-wrap"
            style={{
                height: "calc(100vh - 60px)",
                background: "#242424"
            }}
        >
            <form onSubmit={handleLogin} className="auth-card">
                <h2>Login</h2>

                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />

                <div className="pw-row">
                    <input
                        type={showPass ? "text" : "password"}
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <button
                        type="button"
                        className="pw-toggle"
                        onClick={() => setShowPass(!showPass)}
                    >
                        {showPass ? "Hide" : "Show"}
                    </button>
                </div>

                <button type="submit">Login</button>
                <a href={'/register'}>Create an account</a>

                {message && <p>{message}</p>}
            </form>
        </div>
    );
}
