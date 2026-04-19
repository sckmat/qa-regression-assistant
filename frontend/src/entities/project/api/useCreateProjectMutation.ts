import { useMutation, useQueryClient } from '@tanstack/react-query'

import { createProject } from './projects.api'

export function useCreateProjectMutation() {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: createProject,
        onSuccess: async () => {
            await queryClient.invalidateQueries({
                queryKey: ['projects'],
            })
        },
    })
}