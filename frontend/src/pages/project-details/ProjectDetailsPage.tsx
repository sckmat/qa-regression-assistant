import { useParams } from 'react-router-dom'

export function ProjectDetailsPage() {
    const { projectId } = useParams()

    return (
        <section className="page">
            <h2 className="page__title">Project Details</h2>
            <div className="card">
                <p>Project ID: {projectId}</p>
                <p>Здесь будет overview проекта, быстрые действия и последние прогоны.</p>
            </div>
        </section>
    )
}