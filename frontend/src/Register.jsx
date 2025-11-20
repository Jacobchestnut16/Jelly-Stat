import { useState } from "react";

export default function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [clientId, setClientId] = useState("");
    const [clientSecret, setClientSecret] = useState("");
    const [message, setMessage] = useState("");

    async function handleRegister(e) {
        e.preventDefault();
        try {
            const res = await fetch(
                `http://localhost:3001/auth/register?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&client_id=${encodeURIComponent(clientId)}&client_secret=${encodeURIComponent(clientSecret)}`
            );

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || "Registration failed");
            }

            setMessage("User registered successfully.");
        } catch (err) {
            setMessage(err.message);
        }
    }

    return (
        <form onSubmit={handleRegister} className="flex flex-col gap-2 max-w-xs">
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
            <input
                type="text"
                placeholder="Trakt Client ID"
                value={clientId}
                onChange={(e) => setClientId(e.target.value)}
                className="border p-2 rounded"
            />
            <input
                type="text"
                placeholder="Trakt Client Secret"
                value={clientSecret}
                onChange={(e) => setClientSecret(e.target.value)}
                className="border p-2 rounded"
            />
            <button type="submit" className="bg-green-500 text-white p-2 rounded">
                Register
            </button>
            {message && <p>{message}</p>}
        </form>
    );
}
