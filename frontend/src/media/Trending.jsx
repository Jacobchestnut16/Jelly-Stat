import MediaFetcher from "./MediaFetcher.jsx";
import Row from "./components/Row.jsx";

export default function Trending({ sessionId }) {
    return (
        <MediaFetcher
            sessionId={sessionId}
            endpointMovies="http://localhost:3001/media/trending/movies"
            endpointShows="http://localhost:3001/media/trending/shows"
            render={({ data, basePath }) => (
                <>
                    <Row title="Trending Movies" items={data.movies} basePath={basePath} isMovie />
                    <Row title="Trending Shows" items={data.shows} basePath={basePath} isMovie={false} />
                </>
            )}
        />
    );
}
export function TrendingShows({ sessionId }){
    return (
        <MediaFetcher
            sessionId={sessionId}
            endpointShows="http://localhost:3001/media/trending/shows"
            render={({ data, basePath }) => (
                <>
                    <Row title="Trending Shows" items={data.shows} basePath={basePath} isMovie={false} />
                </>
            )}
        />
    );
}

export function TrendingMovies({ sessionId }){
    return (
        <MediaFetcher
            sessionId={sessionId}
            endpointMovies="http://localhost:3001/media/trending/movies"
            render={({ data, basePath }) => (
                <>
                    <Row title="Trending Movies" items={data.movies} basePath={basePath} isMovie />
                </>
            )}
        />
    );
}