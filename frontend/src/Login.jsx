import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login({ setSessionId, setPendingTrakt, setPendingRedirect }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
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
        } catch (err) {
            setMessage(err.message);
        }
    }

    return (
        <form onSubmit={handleLogin} className="flex flex-col gap-2 max-w-xs">
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="border p-2 rounded"
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="border p-2 rounded"
            />
            <button type="submit" className="bg-blue-500 text-white p-2 rounded">
                Sign In
            </button>
            {message && <p>{message}</p>}
        </form>
    );
}
