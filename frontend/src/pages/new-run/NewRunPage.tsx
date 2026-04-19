import { useParams } from 'react-router-dom'

export function NewRunPage() {
    const { projectId } = useParams()

    return (
        <section className="page">
            <h2 className="page__title">New Regression Run</h2>
            <div className="card">
                <p>Project ID: {projectId}</p>
                <p>Здесь будет форма запуска анализа: change_summary, mode, candidate_limit.</p>
            </div>
        </section>
    )
}