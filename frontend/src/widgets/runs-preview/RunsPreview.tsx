import { Link } from 'react-router-dom'

import type { RegressionRun } from '../../entities/regression-run/model/types'
import { uiText } from '../../shared/constants/ui-text'

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
                    <h3 className="section-title">{uiText.projectDetails.latestRunsTitle}</h3>
                    <p className="muted-text">{uiText.projectDetails.latestRunsDescription}</p>
                </div>

                <Link className="button button--secondary" to={`/projects/${projectId}/runs`}>
                    {uiText.projectDetails.allRunsButton}
                </Link>
            </div>

            {latestRuns.length === 0 ? (
                <div className="empty-state">
                    <p className="empty-state__title">{uiText.projectDetails.noRunsTitle}</p>
                    <p className="empty-state__description">
                        {uiText.projectDetails.noRunsDescription}
                    </p>
                </div>
            ) : (
                <div className="runs-list">
                    {latestRuns.map((run) => (
                        <Link key={run.id} to={`/runs/${run.id}`} className="run-card">
                            <div className="run-card__header">
                                <div className="run-card__title-wrap">
                                    <h4 className="run-card__title">Запуск #{run.id}</h4>
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