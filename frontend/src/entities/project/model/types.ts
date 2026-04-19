export type Project = {
    id: number
    name: string
    description: string | null
}

export type CreateProjectRequest = {
    name: string
    description: string | null
}