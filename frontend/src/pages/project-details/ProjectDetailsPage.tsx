import { Link, useParams } from 'react-router-dom'

import { useProjectQuery } from '../../entities/project/api/useProjectQuery'
import { useRegressionRunsQuery } from '../../entities/regression-run/api/useRegressionRunsQuery'
import { ProjectOverviewCard } from '../../widgets/project-overview/ProjectOverviewCard'
import { RunsPreview } from '../../widgets/runs-preview/RunsPreview'

function parseProjectId(value: string | undefined): number {
    if (!value) {
        return NaN
    }

    return Number(value)
}

export function ProjectDetailsPage() {
    const { projectId: rawProjectId } = useParams()
    const projectId = parseProjectId(rawProjectId)

    const projectQuery = useProjectQuery({ projectId })
    const runsQuery = useRegressionRunsQuery({ projectId })

    if (!Number.isFinite(projectId) || projectId <= 0) {
        return (
            <section className="page">
                <div className="card">
                    <p className="error-text">Некорректный projectId в URL.</p>
                </div>
            </section>
        )
    }

    return (
        <section className="page">
            <div className="page__header">
                <div>
                    <h2 className="page__title">Project Details</h2>
                    <p className="page__description">
                        Обзор проекта, быстрые действия и последние запуски анализа.
                    </p>
                </div>
            </div>

            <div className="quick-actions">
                <Link className="button" to={`/projects/${projectId}/runs/new`}>
                    Новый запуск
                </Link>

                <Link className="button button--secondary" to={`/projects/${projectId}/test-cases`}>
                    Test Cases
                </Link>

                <Link className="button button--secondary" to={`/projects/${projectId}/runs`}>
                    Runs
                </Link>
            </div>

            {projectQuery.isLoading ? (
                <div className="card">
                    <p className="muted-text">Загрузка проекта...</p>
                </div>
            ) : null}

            {projectQuery.isError ? (
                <div className="card">
                    <p className="error-text">
                        Не удалось загрузить проект. Проверь user_service и корректность projectId.
                    </p>
                </div>
            ) : null}

            {projectQuery.data ? <ProjectOverviewCard project={projectQuery.data} /> : null}

            {runsQuery.isLoading ? (
                <div className="card">
                    <p className="muted-text">Загрузка запусков...</p>
                </div>
            ) : null}

            {runsQuery.isError ? (
                <div className="card">
                    <p className="error-text">
                        Не удалось загрузить список запусков проекта.
                    </p>
                </div>
            ) : null}

            {!runsQuery.isLoading && !runsQuery.isError ? (
                <RunsPreview projectId={projectId} runs={runsQuery.data ?? []} />
            ) : null}
        </section>
    )
}