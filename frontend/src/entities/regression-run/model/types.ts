export type RegressionRun = {
    id: number
    project_id: number
    change_summary: string
    status: string
    result_summary: string | null
    created_at: string
}