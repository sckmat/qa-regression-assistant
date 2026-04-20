import { Link, useParams } from 'react-router-dom'

import { useRegressionRunsQuery } from '../../entities/regression-run/api/useRegressionRunsQuery'
import { RunsList } from '../../widgets/runs-list/RunsList'

function parseProjectId(value: string | undefined): number {
    if (!value) {
        return NaN
    }

    return Number(value)
}

export function RunsPage() {
    const { projectId: rawProjectId } = useParams()
    const projectId = parseProjectId(rawProjectId)

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
                    <h2 className="page__title">Runs</h2>
                    <p className="page__description">
                        История запусков анализа по проекту.
                    </p>
                </div>

                <Link className="button" to={`/projects/${projectId}/runs/new`}>
                    Новый запуск
                </Link>
            </div>

            {runsQuery.isLoading ? (
                <div className="card">
                    <p className="muted-text">Загрузка запусков...</p>
                </div>
            ) : null}

            {runsQuery.isError ? (
                <div className="card">
                    <p className="error-text">
                        Не удалось загрузить запуски проекта.
                    </p>
                </div>
            ) : null}

            {!runsQuery.isLoading && !runsQuery.isError ? (
                <RunsList runs={runsQuery.data ?? []} />
            ) : null}
        </section>
    )
}