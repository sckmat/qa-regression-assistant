import { useParams } from 'react-router-dom'

export function RunsPage() {
    const { projectId } = useParams()

    return (
        <section className="page">
            <h2 className="page__title">Runs</h2>
            <div className="card">
                <p>Project ID: {projectId}</p>
                <p>Здесь будет список запусков анализа по проекту.</p>
            </div>
        </section>
    )
}