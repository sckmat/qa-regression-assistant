import { useQuery } from '@tanstack/react-query'

import { listRegressionRuns } from './runs.api'

type UseRegressionRunsQueryParams = {
    projectId: number
}

export function useRegressionRunsQuery({ projectId }: UseRegressionRunsQueryParams) {
    return useQuery({
        queryKey: ['regression-runs', projectId],
        queryFn: () => listRegressionRuns(projectId),
        enabled: Number.isFinite(projectId) && projectId > 0,
    })
}