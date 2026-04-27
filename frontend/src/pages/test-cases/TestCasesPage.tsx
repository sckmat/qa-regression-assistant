import { Link, useParams } from 'react-router-dom'

import { useTestCasesQuery } from '../../entities/test-case/api/useTestCasesQuery'
import { uiText } from '../../shared/constants/ui-text'
import { ImportTestCasesCard } from '../../features/import-test-cases/ui/ImportTestCasesCard'
import { ReindexProjectCard } from '../../features/reindex-project/ui/ReindexProjectCard'
import { TestCasesList } from '../../widgets/test-cases-list/TestCasesList'

function parseProjectId(value: string | undefined): number {
    if (!value) {
        return NaN
    }

    return Number(value)
}

export function TestCasesPage() {
    const { projectId: rawProjectId } = useParams()
    const projectId = parseProjectId(rawProjectId)

    const testCasesQuery = useTestCasesQuery({ projectId })

    if (!Number.isFinite(projectId) || projectId <= 0) {
        return (
            <section className="page">
                <div className="card">
                    <p className="error-text">Некорректный идентификатор проекта.</p>
                </div>
            </section>
        )
    }

    return (
        <section className="page">
            <div className="page__header">
                <div>
                    <h2 className="page__title">{uiText.testCases.title}</h2>
                    <p className="page__description">{uiText.testCases.description}</p>
                </div>

                <Link className="button button--secondary" to={`/projects/${projectId}`}>
                    {uiText.testCases.backButton}
                </Link>
            </div>

            <div className="two-column-layout">
                <ImportTestCasesCard projectId={projectId} />
                <ReindexProjectCard projectId={projectId} />
            </div>

            <div className="card">
                <div className="section-header">
                    <h3 className="section-title">{uiText.testCases.listTitle}</h3>
                </div>

                {testCasesQuery.isLoading ? (
                    <p className="muted-text">Загрузка тест-кейсов...</p>
                ) : null}

                {testCasesQuery.isError ? (
                    <p className="error-text">
                        Не удалось загрузить список тест-кейсов. Попробуйте позже.
                    </p>
                ) : null}

                {!testCasesQuery.isLoading && !testCasesQuery.isError ? (
                    <TestCasesList testCases={testCasesQuery.data ?? []} />
                ) : null}
            </div>
        </section>
    )
}