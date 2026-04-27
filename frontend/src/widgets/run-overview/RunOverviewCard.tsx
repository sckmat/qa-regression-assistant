import type { RegressionRunDetails } from '../../entities/regression-run/model/types'
import { uiText } from '../../shared/constants/ui-text'

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

function RunOverviewCard({ run }: RunOverviewCardProps) {
    return (
        <div className="card">
            <div className="run-overview">
                <div className="run-overview__header">
                    <div className="run-overview__title-wrap">
                        <h3 className="run-overview__title">Запуск #{run.id}</h3>
                        <span className="run-overview__status">{run.status}</span>
                    </div>

                    <span className="run-overview__date">{formatDate(run.created_at)}</span>
                </div>

                <div className="run-overview__meta">
                    <span className="run-overview__badge">Проект #{run.project_id}</span>
                    <span className="run-overview__badge">
            Кандидатов: {run.candidates.length}
          </span>
                </div>

                <div className="run-overview__section">
                    <p className="run-overview__label">{uiText.runDetails.changeSummaryLabel}</p>
                    <p className="run-overview__text">{run.change_summary}</p>
                </div>

                <div className="run-overview__section">
                    <p className="run-overview__label">{uiText.runDetails.resultSummaryLabel}</p>
                    <pre className="run-overview__summary">
            {run.result_summary?.trim()
                ? run.result_summary
                : 'Итоговый summary пока отсутствует'}
          </pre>
                </div>
            </div>
        </div>
    )
}

export default RunOverviewCard