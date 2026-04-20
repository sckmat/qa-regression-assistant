import { Link, useParams } from 'react-router-dom'

import { useRegressionRunQuery } from '../../entities/regression-run/api/useRegressionRunQuery'
import { CandidatesList } from '../../widgets/candidates-list/CandidatesList'
import { RunOverviewCard } from '../../widgets/run-overview/RunOverviewCard'

function parseRunId(value: string | undefined): number {
    if (!value) {
        return NaN
    }

    return Number(value)
}

export function RunDetailsPage() {
    const { runId: rawRunId } = useParams()
    const runId = parseRunId(rawRunId)

    const runQuery = useRegressionRunQuery({ runId })

    if (!Number.isFinite(runId) || runId <= 0) {
        return (
            <section className="page">
                <div className="card">
                    <p className="error-text">Некорректный runId в URL.</p>
                </div>
            </section>
        )
    }

    return (
        <section className="page">
            <div className="page__header">
                <div>
                    <h2 className="page__title">Run Details</h2>
                    <p className="page__description">
                        Детали запуска, итоговый summary и список кандидатов.
                    </p>
                </div>

                {runQuery.data ? (
                    <Link
                        className="button button--secondary"
                        to={`/projects/${runQuery.data.project_id}/runs`}
                    >
                        К списку запусков
                    </Link>
                ) : null}
            </div>

            {runQuery.isLoading ? (
                <div className="card">
                    <p className="muted-text">Загрузка деталей запуска...</p>
                </div>
            ) : null}

            {runQuery.isError ? (
                <div className="card">
                    <p className="error-text">
                        Не удалось загрузить детали запуска. Проверь user_service и корректность runId.
                    </p>
                </div>
            ) : null}

            {runQuery.data ? (
                <>
                    <RunOverviewCard run={runQuery.data} />
                    <CandidatesList candidates={runQuery.data.candidates} />
                </>
            ) : null}
        </section>
    )
}