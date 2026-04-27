import type { TestCase } from '../../entities/test-case/model/types'
import { uiText } from '../../shared/constants/ui-text'

type TestCasesListProps = {
    testCases: TestCase[]
}

export function TestCasesList({ testCases }: TestCasesListProps) {
    if (testCases.length === 0) {
        return (
            <div className="card empty-state">
                <p className="empty-state__title">{uiText.testCases.emptyTitle}</p>
                <p className="empty-state__description">
                    {uiText.testCases.emptyDescription}
                </p>
            </div>
        )
    }

    return (
        <div className="test-cases-list">
            {testCases.map((testCase) => (
                <div key={testCase.id} className="test-case-card">
                    <div className="test-case-card__header">
                        <div className="test-case-card__title-wrap">
                            <h4 className="test-case-card__title">{testCase.title}</h4>

                            <div className="test-case-card__badges">
                                <span className="test-case-card__badge">TC #{testCase.id}</span>

                                {testCase.external_id ? (
                                    <span className="test-case-card__badge test-case-card__badge--secondary">
                    {testCase.external_id}
                  </span>
                                ) : null}

                                {testCase.priority ? (
                                    <span className="test-case-card__badge test-case-card__badge--priority">
                    {testCase.priority}
                  </span>
                                ) : null}
                            </div>
                        </div>
                    </div>

                    {testCase.expected_result ? (
                        <div className="test-case-card__section">
                            <p className="test-case-card__label">{uiText.testCases.expectedResult}</p>
                            <p className="test-case-card__text">{testCase.expected_result}</p>
                        </div>
                    ) : null}

                    {testCase.tags?.length ? (
                        <div className="test-case-card__section">
                            <p className="test-case-card__label">{uiText.testCases.tags}</p>
                            <div className="test-case-card__tags">
                                {testCase.tags.map((tag) => (
                                    <span key={tag} className="test-case-card__tag">
                    {tag}
                  </span>
                                ))}
                            </div>
                        </div>
                    ) : null}
                </div>
            ))}
        </div>
    )
}