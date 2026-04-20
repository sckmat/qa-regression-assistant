import { useMutation, useQueryClient } from '@tanstack/react-query'

import { createRegressionRun } from './runs.api'
import type { CreateRegressionRunRequest } from '../model/types'

type CreateRegressionRunMutationParams = {
    projectId: number
}

export function useCreateRegressionRunMutation({
                                                   projectId,
                                               }: CreateRegressionRunMutationParams) {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: (payload: CreateRegressionRunRequest) =>
            createRegressionRun(projectId, payload),

        onSuccess: async () => {
            await queryClient.invalidateQueries({
                queryKey: ['regression-runs', projectId],
            })
        },
    })
}