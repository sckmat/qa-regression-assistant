import { httpClient } from '../../../shared/api/http-client'
import type {
    ImportTestCasesFileResponse,
    ReindexResponse,
    TestCase,
} from '../model/types'

export async function listTestCases(projectId: number): Promise<TestCase[]> {
    const response = await httpClient.get<TestCase[]>(
        `/api/v1/projects/${projectId}/test-cases`,
    )

    return response.data
}

export async function importTestCasesFile(
    projectId: number,
    file: File,
): Promise<ImportTestCasesFileResponse> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await httpClient.post<ImportTestCasesFileResponse>(
        `/api/v1/projects/${projectId}/test-cases/import-file`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            timeout: 120000,
        },
    )

    return response.data
}

export async function reindexProject(projectId: number): Promise<ReindexResponse> {
    const response = await httpClient.post<ReindexResponse>(
        `/api/v1/projects/${projectId}/test-cases/reindex`,
    )

    return response.data
}