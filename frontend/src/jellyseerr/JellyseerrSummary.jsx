export default function JellyseerrSummary({ summary }) {
    if (!summary) return null;

    return (
        <div className="jellyseerr-summary">
            <span>Shows: {summary.tv}</span>
            <span>Movies: {summary.movies}</span>
            {/*<span>Owned: {summary.owned}</span>*/}
            {/*<span>Unowned: {summary.unowned}</span>*/}
        </div>
    );
}
