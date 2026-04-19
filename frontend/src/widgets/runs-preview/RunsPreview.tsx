import { Link } from 'react-router-dom'

import type { RegressionRun } from '../../entities/regression-run/model/types'

type RunsPreviewProps = {
    projectId: number
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

export function RunsPreview({ projectId, runs }: RunsPreviewProps) {
    const latestRuns = runs.slice(0, 5)

    return (
        <div className="card">
            <div className="section-header">
                <div>
                    <h3 className="section-title">Последние запуски</h3>
                    <p className="muted-text">
                        Краткая история запусков анализа по проекту.
                    </p>
                </div>

                <Link className="button button--secondary" to={`/projects/${projectId}/runs`}>
                    Все запуски
                </Link>
            </div>

            {latestRuns.length === 0 ? (
                <div className="empty-state">
                    <p className="empty-state__title">Запусков пока нет</p>
                    <p className="empty-state__description">
                        Создай первый run, чтобы увидеть результаты отбора тест-кейсов.
                    </p>
                </div>
            ) : (
                <div className="runs-list">
                    {latestRuns.map((run) => (
                        <Link key={run.id} to={`/runs/${run.id}`} className="run-card">
                            <div className="run-card__header">
                                <div className="run-card__title-wrap">
                                    <h4 className="run-card__title">Run #{run.id}</h4>
                                    <span className="run-card__status">{run.status}</span>
                                </div>

                                <span className="run-card__date">{formatDate(run.created_at)}</span>
                            </div>

                            <p className="run-card__summary">{run.change_summary}</p>
                        </Link>
                    ))}
                </div>
            )}
        </div>
    )
}