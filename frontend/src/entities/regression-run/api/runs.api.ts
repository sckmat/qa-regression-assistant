import { httpClient } from '../../../shared/api/http-client'
import type {
    CreateRegressionRunRequest,
    RegressionRun,
    RegressionRunDetails,
} from '../model/types'

export async function listRegressionRuns(projectId: number): Promise<RegressionRun[]> {
    const response = await httpClient.get<RegressionRun[]>(
        `/api/v1/projects/${projectId}/regression-runs`,
    )

    return response.data
}

export async function getRegressionRun(runId: number): Promise<RegressionRunDetails> {
    const response = await httpClient.get<RegressionRunDetails>(
        `/api/v1/regression-runs/${runId}`,
    )

    return response.data
}

export async function createRegressionRun(
    projectId: number,
    payload: CreateRegressionRunRequest,
): Promise<RegressionRun> {
    const response = await httpClient.post<RegressionRun>(
        `/api/v1/projects/${projectId}/regression-runs`,
        payload,
    )

    return response.data
}