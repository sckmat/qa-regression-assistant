import { useQuery } from '@tanstack/react-query'

import { getRegressionRun } from './runs.api'

type UseRegressionRunQueryParams = {
    runId: number
}

export function useRegressionRunQuery({ runId }: UseRegressionRunQueryParams) {
    return useQuery({
        queryKey: ['regression-run', runId],
        queryFn: () => getRegressionRun(runId),
        enabled: Number.isFinite(runId) && runId > 0,
    })
}