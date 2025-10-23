import { useEffect, useState } from "react";
import Row from "./components/Row";

const basePath = "https://image.tmdb.org/t/p/w500";

export default function MediaPage() {
    const [data, setData] = useState({
        trendingMovies: [],
        trendingShows: []
    });

    useEffect(() => {
        const fetchData = async () => {
            const [moviesRes, showsRes] = await Promise.all([
                fetch("http://localhost:3001/media/trending/movies"),
                fetch("http://localhost:3001/media/trending/shows")
            ]);
            const [movies, shows] = await Promise.all([moviesRes.json(), showsRes.json()]);

            // normalize trakt format
            const normMovies = movies.map(m => ({
                title: m.movie?.title,
                poster_path: m.movie?.images?.posters?.[0]?.file_path || null
            }));

            const normShows = shows.map(s => ({
                name: s.show?.title || s.show?.name,
                poster_path: s.show?.images?.posters?.[0]?.file_path || null
            }));

            setData({
                trendingMovies: normMovies,
                trendingShows: normShows
            });
        };

        fetchData();
    }, []);

    return (
        <div>
            <nav>
                <ul>
                    <li><a href="#">Trakt Plus</a></li>
                    <li><a href="#movies">Movies</a></li>
                    <li><a href="#shows">Shows</a></li>
                </ul>
            </nav>

            <Row
                title="Trending Movies"
                items={data.trendingMovies}
                basePath={basePath}
                isMovie={true}
            />
            <Row
                title="Trending Shows"
                items={data.trendingShows}
                basePath={basePath}
                isMovie={false}
            />
            <div className={'credit'}>
                <p>Images powered by <a href="https://tmdb.org">TMDB</a></p>
            </div>
        </div>
    );
}
