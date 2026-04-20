import type { RegressionRunCandidate } from '../../entities/regression-run/model/types'

type CandidatesListProps = {
    candidates: RegressionRunCandidate[]
}

export function CandidatesList({ candidates }: CandidatesListProps) {
    if (candidates.length === 0) {
        return (
            <div className="card empty-state">
                <p className="empty-state__title">Кандидаты не найдены</p>
                <p className="empty-state__description">
                    Для этого запуска не было найдено релевантных тест-кейсов.
                </p>
            </div>
        )
    }

    return (
        <div className="candidates-list">
            {candidates.map((candidate) => (
                <div key={candidate.id} className="candidate-card">
                    <div className="candidate-card__header">
                        <div className="candidate-card__title-wrap">
                            <h4 className="candidate-card__title">{candidate.title}</h4>
                            <span className="candidate-card__id">
                TC #{candidate.source_test_case_id}
              </span>
                        </div>

                        <span className="candidate-card__score">
              Score: {candidate.relevance_score}
            </span>
                    </div>

                    <div className="candidate-card__sections">
                        <div className="candidate-card__section">
                            <p className="candidate-card__label">Matched terms</p>

                            {candidate.matched_terms.length > 0 ? (
                                <div className="candidate-card__tags">
                                    {candidate.matched_terms.map((term) => (
                                        <span key={term} className="candidate-card__tag">
                      {term}
                    </span>
                                    ))}
                                </div>
                            ) : (
                                <p className="candidate-card__empty">Нет matched terms</p>
                            )}
                        </div>

                        <div className="candidate-card__section">
                            <p className="candidate-card__label">Explanation</p>
                            <p className="candidate-card__text">
                                {candidate.explanation?.trim()
                                    ? candidate.explanation
                                    : 'Explanation отсутствует для этого режима запуска'}
                            </p>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}