import { useState } from "react";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    async function handleLogin(e) {
        e.preventDefault();
        try {
            const res = await fetch(
                `http://localhost:3001/auth/signin?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
            );

            const data = await res.json();

            if (!res.ok) throw new Error(data.detail || "Login failed");

            // store ID or token locally
            localStorage.setItem("user_id", data.id);

            if (data.redirect) {
                window.location.href = data.redirect; // go to Trakt login
                return;
            }

            setMessage("Login successful!");


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
