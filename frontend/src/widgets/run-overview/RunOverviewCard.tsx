import type { RegressionRunDetails } from '../../entities/regression-run/model/types'

type RunOverviewCardProps = {
    run: RegressionRunDetails
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

export function RunOverviewCard({ run }: RunOverviewCardProps) {
    return (
        <div className="card">
            <div className="run-overview">
                <div className="run-overview__header">
                    <div className="run-overview__title-wrap">
                        <h3 className="run-overview__title">Run #{run.id}</h3>
                        <span className="run-overview__status">{run.status}</span>
                    </div>

                    <span className="run-overview__date">{formatDate(run.created_at)}</span>
                </div>

                <div className="run-overview__meta">
                    <span className="run-overview__badge">Project #{run.project_id}</span>
                    <span className="run-overview__badge">
            Candidates: {run.candidates.length}
          </span>
                </div>

                <div className="run-overview__section">
                    <p className="run-overview__label">Change summary</p>
                    <p className="run-overview__text">{run.change_summary}</p>
                </div>

                <div className="run-overview__section">
                    <p className="run-overview__label">Result summary</p>
                    <pre className="run-overview__summary">
            {run.result_summary?.trim()
                ? run.result_summary
                : 'Result summary пока отсутствует'}
          </pre>
                </div>
            </div>
        </div>
    )
}