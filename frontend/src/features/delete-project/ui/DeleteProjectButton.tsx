import { useNavigate } from 'react-router-dom'

import { useDeleteProjectMutation } from '../../../entities/project/api/useDeleteProjectMutation'
import { getUserErrorMessage } from '../../../shared/lib/get-user-error-message'
import { useToast } from '../../../shared/ui/toast/useToast'

type DeleteProjectButtonProps = {
    projectId: number
    projectName?: string
}

export function DeleteProjectButton({
                                        projectId,
                                        projectName,
                                    }: DeleteProjectButtonProps) {
    const navigate = useNavigate()
    const toast = useToast()
    const deleteMutation = useDeleteProjectMutation({ projectId })

    const handleDelete = async () => {
        const confirmed = window.confirm(
            projectName
                ? `Удалить проект «${projectName}»? Это действие нельзя отменить.`
                : 'Удалить проект? Это действие нельзя отменить.',
        )

        if (!confirmed) {
            return
        }

        try {
            await deleteMutation.mutateAsync()
            toast.success('Проект успешно удален.')
            navigate('/projects')
        } catch (error) {
            toast.error(getUserErrorMessage(error))
        }
    }

    return (
        <button
            className="button button--danger"
            type="button"
            disabled={deleteMutation.isPending}
            onClick={handleDelete}
        >
            {deleteMutation.isPending ? 'Удаление...' : 'Удалить проект'}
        </button>
    )
}