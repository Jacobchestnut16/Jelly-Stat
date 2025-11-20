import { useState } from "react";

export default function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [clientId, setClientId] = useState("");
    const [clientSecret, setClientSecret] = useState("");
    const [showPass, setShowPass] = useState(false);
    const [showConfirm, setShowConfirm] = useState(false);
    const [showSecret, setShowSecret] = useState(false);
    const [message, setMessage] = useState("");

    async function handleRegister(e) {
        e.preventDefault();
        if (password !== confirm) {
            setMessage("Passwords do not match");
            return;
        }

        try {
            const res = await fetch(
                `http://localhost:3001/auth/register?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&client_id=${encodeURIComponent(clientId)}&client_secret=${encodeURIComponent(clientSecret)}`
            );

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || "Registration failed");
            }

            setMessage("User registered.");
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
            <form onSubmit={handleRegister} className="auth-card">
                <h2>Create Account</h2>

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

                <div className="pw-row">
                    <input
                        type={showConfirm ? "text" : "password"}
                        placeholder="Confirm Password"
                        value={confirm}
                        onChange={(e) => setConfirm(e.target.value)}
                    />
                    <button
                        type="button"
                        className="pw-toggle"
                        onClick={() => setShowConfirm(!showConfirm)}
                    >
                        {showConfirm ? "Hide" : "Show"}
                    </button>
                </div>

                <input
                    type="text"
                    placeholder="Trakt Client ID"
                    value={clientId}
                    onChange={(e) => setClientId(e.target.value)}
                />

                <div className="pw-row">
                    <input
                        type={showSecret ? "text" : "password"}
                        placeholder="Trakt Client Secret"
                        value={clientSecret}
                        onChange={(e) => setClientSecret(e.target.value)}
                    />
                    <button
                        type="button"
                        className="pw-toggle"
                        onClick={() => setShowSecret(!showSecret)}
                    >
                        {showSecret ? "Hide" : "Show"}
                    </button>
                </div>

                <button type="submit">Register</button>
                <a href="/login">Already have an account? Sign in</a>

                {message && <p>{message}</p>}
            </form>
        </div>
    );


}
