import { useMutation, useQueryClient } from '@tanstack/react-query'

import { importTestCasesFile } from './test-cases.api'

type UseImportTestCasesFileMutationParams = {
    projectId: number
}

export function useImportTestCasesFileMutation({
                                                   projectId,
                                               }: UseImportTestCasesFileMutationParams) {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: (file: File) => importTestCasesFile(projectId, file),
        onSuccess: async () => {
            await queryClient.invalidateQueries({
                queryKey: ['test-cases', projectId],
            })
        },
    })
}