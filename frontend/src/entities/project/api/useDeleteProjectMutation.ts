import { useMutation, useQueryClient } from '@tanstack/react-query'

import { deleteProject } from './projects.api'

type UseDeleteProjectMutationParams = {
    projectId: number
}

export function useDeleteProjectMutation({
                                             projectId,
                                         }: UseDeleteProjectMutationParams) {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: () => deleteProject(projectId),
        onSuccess: async () => {
            await queryClient.invalidateQueries({
                queryKey: ['projects'],
            })
        },
    })
}