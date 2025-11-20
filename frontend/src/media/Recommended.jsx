import MediaFetcher from "./MediaFetcher.jsx";
import Row from "./components/Row.jsx";

export default function Recommended({ sessionId }) {
    return (
        <MediaFetcher
            sessionId={sessionId}
            endpointMovies="http://localhost:3001/media/recommended/movies"
            endpointShows="http://localhost:3001/media/recommended/shows"
            render={({ data, basePath }) => (
                <>
                    <Row title="Recommended Movies" items={data.movies} basePath={basePath} isMovie />
                    <Row title="Recommended Shows" items={data.shows} basePath={basePath} isMovie={false} />
                </>
            )}
        />
    );
}

export function RecommendedShows({ sessionId }) {
    return (
        <MediaFetcher
            sessionId={sessionId}
            endpointShows="http://localhost:3001/media/recommended/shows"
            render={({ data, basePath }) => (
                <>
                    <Row title="Recommended Shows" items={data.shows} basePath={basePath} isMovie={false} />
                </>
            )}
        />
    );
}

export function RecommendedMovies({ sessionId }) {
    return (
        <MediaFetcher
            sessionId={sessionId}
            endpointMovies="http://localhost:3001/media/recommended/movies"
            render={({ data, basePath }) => (
                <>
                    <Row title="Recommended Movies" items={data.movies} basePath={basePath} isMovie />
                </>
            )}
        />
    );
}
