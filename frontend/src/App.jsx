import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import MediaPage from "./MediaPage.jsx";
import Login from "./Login.jsx";
import Register from "./Register.jsx";

export default function App() {
    return (
        <BrowserRouter>
            <nav>
                <ul>
                    <li><Link to="/">Trakt Plus</Link></li>
                    <li><a href="#movies">Movies</a></li>
                    <li><a href="#shows">Shows</a></li>
                </ul>
                <ul>
                    <li><Link to="/login">Login</Link></li>
                    <li><Link to="/register">Register</Link></li>
                </ul>
            </nav>

            <Routes>
                <Route path="/" element={<MediaPage/>}/>
                <Route path="/login" element={<Login/>}/>
                <Route path="/register" element={<Register />} />
            </Routes>
        </BrowserRouter>
    );
}
