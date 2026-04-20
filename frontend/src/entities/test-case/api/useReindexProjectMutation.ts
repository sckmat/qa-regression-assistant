import { useMutation, useQueryClient } from '@tanstack/react-query'

import { reindexProject } from './test-cases.api'

type UseReindexProjectMutationParams = {
    projectId: number
}

export function useReindexProjectMutation({
                                              projectId,
                                          }: UseReindexProjectMutationParams) {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: () => reindexProject(projectId),
        onSuccess: async () => {
            await queryClient.invalidateQueries({
                queryKey: ['test-cases', projectId],
            })
        },
    })
}