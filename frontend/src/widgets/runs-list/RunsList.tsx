import { Link } from 'react-router-dom'

import type { RegressionRun } from '../../entities/regression-run/model/types'

type RunsListProps = {
    runs: RegressionRun[]
}

function formatDate(value: string) {
    const date = new Date(value)

    if (Number.isNaN(date.getTime())) {
        return value
    }

    return new Intl.DateTimeFormat('ru-RU', {
        dateStyle: 'medium',
        timeStyle: 'short',
    }).format(date)
}

export function RunsList({ runs }: RunsListProps) {
    if (runs.length === 0) {
        return (
            <div className="card empty-state">
                <p className="empty-state__title">Запусков пока нет</p>
                <p className="empty-state__description">
                    Создай первый run, чтобы увидеть результаты интеллектуального отбора тест-кейсов.
                </p>
            </div>
        )
    }

    return (
        <div className="runs-list">
            {runs.map((run) => (
                <Link key={run.id} to={`/runs/${run.id}`} className="run-card">
                    <div className="run-card__header">
                        <div className="run-card__title-wrap">
                            <h4 className="run-card__title">Run #{run.id}</h4>
                            <span className="run-card__status">{run.status}</span>
                        </div>

                        <span className="run-card__date">{formatDate(run.created_at)}</span>
                    </div>

                    <p className="run-card__summary">{run.change_summary}</p>

                    {run.result_summary ? (
                        <p className="run-card__meta">
                            Summary available
                        </p>
                    ) : null}
                </Link>
            ))}
        </div>
    )
}