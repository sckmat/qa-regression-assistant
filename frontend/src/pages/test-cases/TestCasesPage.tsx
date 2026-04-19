import { useParams } from 'react-router-dom'

export function TestCasesPage() {
    const { projectId } = useParams()

    return (
        <section className="page">
            <h2 className="page__title">Test Cases</h2>
            <div className="card">
                <p>Project ID: {projectId}</p>
                <p>Здесь будет импорт test cases, список и reindex.</p>
            </div>
        </section>
    )
}