import { useReindexProjectMutation } from '../../../entities/test-case/api/useReindexProjectMutation.ts'

type ReindexProjectCardProps = {
    projectId: number
}

export function ReindexProjectCard({ projectId }: ReindexProjectCardProps) {
    const reindexMutation = useReindexProjectMutation({ projectId })

    return (
        <div className="card">
            <h3 className="section-title">Reindex</h3>

            <div className="reindex-panel">
                <p className="muted-text">
                    Переиндексация нужна для semantic и semantic_llm режимов после загрузки или обновления тест-кейсов.
                </p>

                {reindexMutation.isError ? (
                    <p className="error-text">
                        Не удалось запустить reindex. Проверь доступность user_service и data_service.
                    </p>
                ) : null}

                {reindexMutation.isSuccess ? (
                    <div className="success-box">
                        <p className="success-text">
                            Reindex завершен успешно.
                        </p>
                        <p className="muted-text">
                            Indexed: {reindexMutation.data.indexed_test_cases} / Processed: {reindexMutation.data.processed_test_cases}
                        </p>
                    </div>
                ) : null}

                <div className="form-actions">
                    <button
                        className="button button--secondary"
                        type="button"
                        disabled={reindexMutation.isPending}
                        onClick={() => reindexMutation.mutate()}
                    >
                        {reindexMutation.isPending ? 'Reindex...' : 'Запустить reindex'}
                    </button>
                </div>
            </div>
        </div>
    )
}