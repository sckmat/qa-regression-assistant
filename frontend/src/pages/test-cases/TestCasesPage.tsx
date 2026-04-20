import { Link, useParams } from 'react-router-dom'

import { useTestCasesQuery } from '../../entities/test-case/api/useTestCasesQuery'
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
                    <p className="error-text">Некорректный projectId в URL.</p>
                </div>
            </section>
        )
    }

    return (
        <section className="page">
            <div className="page__header">
                <div>
                    <h2 className="page__title">Test Cases</h2>
                    <p className="page__description">
                        Загрузка тест-кейсов проекта, просмотр списка и запуск переиндексации.
                    </p>
                </div>

                <Link className="button button--secondary" to={`/projects/${projectId}`}>
                    К проекту
                </Link>
            </div>

            <div className="two-column-layout">
                <ImportTestCasesCard projectId={projectId} />
                <ReindexProjectCard projectId={projectId} />
            </div>

            <div className="card">
                <div className="section-header">
                    <h3 className="section-title">Список test cases</h3>
                </div>

                {testCasesQuery.isLoading ? (
                    <p className="muted-text">Загрузка test cases...</p>
                ) : null}

                {testCasesQuery.isError ? (
                    <p className="error-text">
                        Не удалось загрузить test cases. Проверь user_service и доступность gateway-ручек.
                    </p>
                ) : null}

                {!testCasesQuery.isLoading && !testCasesQuery.isError ? (
                    <TestCasesList testCases={testCasesQuery.data ?? []} />
                ) : null}
            </div>
        </section>
    )
}