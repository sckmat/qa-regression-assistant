export type SearchMode = 'lexical' | 'semantic' | 'semantic_llm'

export type RegressionRun = {
    id: number
    project_id: number
    change_summary: string
    status: string
    result_summary: string | null
    created_at: string
}

export type RegressionRunCandidate = {
    id: number
    regression_run_id: number
    source_test_case_id: number
    title: string
    relevance_score: number
    matched_terms: string[]
    explanation: string | null
    created_at: string
}

export type RegressionRunDetails = RegressionRun & {
    candidates: RegressionRunCandidate[]
}

export type CreateRegressionRunRequest = {
    change_summary: string
    candidate_limit: number
    search_mode: SearchMode
}