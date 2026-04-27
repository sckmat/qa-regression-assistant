import { useReindexProjectMutation } from '../../../entities/test-case/api/useReindexProjectMutation'
import { uiText } from '../../../shared/constants/ui-text'
import { getUserErrorMessage } from '../../../shared/lib/get-user-error-message'
import { useToast } from '../../../shared/ui/toast/useToast'

type ReindexProjectCardProps = {
    projectId: number
}

export function ReindexProjectCard({ projectId }: ReindexProjectCardProps) {
    const reindexMutation = useReindexProjectMutation({ projectId })
    const toast = useToast()

    const handleReindex = async () => {
        try {
            await reindexMutation.mutateAsync()
            toast.success(uiText.toasts.reindexCompleted)
        } catch (error) {
            toast.error(getUserErrorMessage(error))
        }
    }

    return (
        <div className="card">
            <h3 className="section-title">{uiText.testCases.reindexTitle}</h3>

            <div className="reindex-panel">
                <p className="muted-text">{uiText.testCases.reindexHint}</p>

                {reindexMutation.isSuccess ? (
                    <div className="success-box">
                        <p className="success-text">Переиндексация завершена успешно.</p>
                        <p className="muted-text">
                            Обработано: {reindexMutation.data.processed_test_cases}, проиндексировано:{' '}
                            {reindexMutation.data.indexed_test_cases}
                        </p>
                    </div>
                ) : null}

                <div className="form-actions">
                    <button
                        className="button button--secondary"
                        type="button"
                        disabled={reindexMutation.isPending}
                        onClick={handleReindex}
                    >
                        {reindexMutation.isPending
                            ? uiText.testCases.reindexingButton
                            : uiText.testCases.reindexButton}
                    </button>
                </div>
            </div>
        </div>
    )
}