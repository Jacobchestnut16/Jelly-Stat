// src/components/Row.jsx
import { useRef } from "react";
import { Link } from "react-router-dom";
import "./Row.css";

function formatTitle(str) {
    return str
        .replace(/_/g, " ")            // replace underscores with spaces
        .replace(/-/g," ")
        .replace(/\b\w/g, c => c.toUpperCase()); // capitalize each word
}
function Row({ title, items, basePath, isMovie = true }) {
    const scrollRef = useRef(null);

    const scroll = (direction) => {
        if (scrollRef.current) {
            const { scrollLeft, clientWidth } = scrollRef.current;
            const newScroll =
                direction === "left" ? scrollLeft - clientWidth : scrollLeft + clientWidth;
            scrollRef.current.scrollTo({ left: newScroll, behavior: "smooth" });
        }
    };

    return (
        <div style={{ marginBottom: "2rem" }}>
            <h2 style={{ marginLeft: "1rem" }}>{formatTitle(title)}</h2>
            <div style={{ position: "relative" }} className="cards-container">
                {/* Scroll buttons */}
                <button
                    onClick={() => scroll("left")}
                    style={{
                        position: "absolute",
                        left: 0,
                        top: "40%",
                        zIndex: 10,
                        background: "rgba(0,0,0,0.5)",
                        color: "white",
                        border: "none",
                        cursor: "pointer",
                    }}
                >
                    ◀
                </button>

                <div
                    ref={scrollRef}
                    style={{
                        display: "flex",
                        overflowX: "auto",
                        scrollBehavior: "smooth",
                        padding: "1rem",
                        gap: "1rem",
                    }}
                >
                    {items.map((item, idx) => (
                        //
                        //
                        // <div
                        //     key={idx}
                        //     className="card"
                        // >
                        //     {item.poster_path ? (
                        //         <img
                        //             src={basePath + item.poster_path}
                        //             alt={isMovie ? item.title : item.name}
                        //             style={{
                        //                 width: "150px",
                        //                 height: "225px",
                        //                 objectFit: "cover",
                        //                 borderRadius: "8px",
                        //                 boxShadow: "0 2px 8px rgba(0,0,0,0.5)",
                        //             }}
                        //         />
                        //     ) : (
                        //         <div
                        //             style={{
                        //                 width: "150px",
                        //                 height: "225px",
                        //                 background: "#333",
                        //                 color: "white",
                        //                 display: "flex",
                        //                 alignItems: "center",
                        //                 justifyContent: "center",
                        //                 borderRadius: "8px",
                        //             }}
                        //         >
                        //             No Image
                        //         </div>
                        //     )}
                        //     <p className="card-title">{isMovie ? item.title : item.name}</p>
                        // </div>

                        <Link
                            to={`/${isMovie ? "movie" : "show"}/${item.tmdb_id}`}
                            style={{ textDecoration: "none", color: "inherit" }}
                        >
                            <div
                                key={idx}
                                className="card"
                            >
                                {item.poster_path ? (
                                    <img
                                        src={item.poster_path}
                                        alt={isMovie ? item.title : item.name}
                                        style={{
                                            width: "150px",
                                            height: "225px",
                                            objectFit: "cover",
                                            borderRadius: "8px",
                                            boxShadow: "0 2px 8px rgba(0,0,0,0.5)",
                                        }}
                                    />
                                ) : (
                                    <div
                                        style={{
                                            width: "150px",
                                            height: "225px",
                                            background: "#333",
                                            color: "white",
                                            display: "flex",
                                            alignItems: "center",
                                            justifyContent: "center",
                                            borderRadius: "8px",
                                        }}
                                    >
                                        No Image
                                    </div>
                                )}
                                <p className="card-title">{isMovie ? item.title : item.name}</p>
                            </div>
                        </Link>

                    ))}
                </div>

                <button
                    onClick={() => scroll("right")}
                    style={{
                        position: "absolute",
                        right: 0,
                        top: "40%",
                        zIndex: 10,
                        background: "rgba(0,0,0,0.5)",
                        color: "white",
                        border: "none",
                        cursor: "pointer",
                    }}
                >
                    ▶
                </button>
            </div>
        </div>
    );
}

export default Row;
