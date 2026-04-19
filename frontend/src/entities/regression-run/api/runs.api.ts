import { httpClient } from '../../../shared/api/http-client'
import type { RegressionRun } from '../model/types'

export async function listRegressionRuns(projectId: number): Promise<RegressionRun[]> {
    const response = await httpClient.get<RegressionRun[]>(
        `/api/v1/projects/${projectId}/regression-runs`,
    )

    return response.data
}