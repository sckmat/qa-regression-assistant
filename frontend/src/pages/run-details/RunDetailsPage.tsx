import { useParams } from 'react-router-dom'

export function RunDetailsPage() {
    const { runId } = useParams()

    return (
        <section className="page">
            <h2 className="page__title">Run Details</h2>
            <div className="card">
                <p>Run ID: {runId}</p>
                <p>Здесь будут candidates, scores, matched terms и explanation.</p>
            </div>
        </section>
    )
}