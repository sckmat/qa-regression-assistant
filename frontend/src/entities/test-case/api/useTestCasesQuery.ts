import { useQuery } from '@tanstack/react-query'

import { listTestCases } from './test-cases.api'

type UseTestCasesQueryParams = {
    projectId: number
}

export function useTestCasesQuery({ projectId }: UseTestCasesQueryParams) {
    return useQuery({
        queryKey: ['test-cases', projectId],
        queryFn: () => listTestCases(projectId),
        enabled: Number.isFinite(projectId) && projectId > 0,
    })
}