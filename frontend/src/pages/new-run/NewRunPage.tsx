import { Link, useParams } from 'react-router-dom'

import { uiText } from '../../shared/constants/ui-text'
import { StartRegressionRunForm } from '../../features/start-regression-run/ui/StartRegressionRunForm'

function parseProjectId(value: string | undefined): number {
    if (!value) {
        return NaN
    }

    return Number(value)
}

export function NewRunPage() {
    const { projectId: rawProjectId } = useParams()
    const projectId = parseProjectId(rawProjectId)

    if (!Number.isFinite(projectId) || projectId <= 0) {
        return (
            <section className="page">
                <div className="card">
                    <p className="error-text">Некорректный идентификатор проекта.</p>
                </div>
            </section>
        )
    }

    return (
        <section className="page">
            <div className="page__header">
                <div>
                    <h2 className="page__title">{uiText.newRun.title}</h2>
                    <p className="page__description">{uiText.newRun.description}</p>
                </div>

                <Link className="button button--secondary" to={`/projects/${projectId}/runs`}>
                    {uiText.newRun.backButton}
                </Link>
            </div>

            <StartRegressionRunForm projectId={projectId} />
        </section>
    )
}