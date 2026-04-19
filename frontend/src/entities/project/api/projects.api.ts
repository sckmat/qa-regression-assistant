import { httpClient } from '../../../shared/api/http-client'
import type { CreateProjectRequest, Project } from '../model/types'

export async function listProjects(): Promise<Project[]> {
    const response = await httpClient.get<Project[]>('/api/v1/projects')
    return response.data
}

export async function getProject(projectId: number): Promise<Project> {
    const response = await httpClient.get<Project>(`/api/v1/projects/${projectId}`)
    return response.data
}

export async function createProject(payload: CreateProjectRequest): Promise<Project> {
    const response = await httpClient.post<Project>('/api/v1/projects', payload)
    return response.data
}