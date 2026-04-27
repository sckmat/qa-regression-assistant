export type TestCase = {
    id: number
    project_id: number
    external_id?: string | null
    title: string
    preconditions?: string | null
    steps?: string | null
    expected_result?: string | null
    tags?: string[] | null
    priority?: string | null
    raw_text?: string | null
    created_at?: string
}

export type ReindexResponse = {
    project_id: number
    embedding_provider: string
    embedding_model: string
    embedding_dim: number
    processed_test_cases: number
    indexed_test_cases: number
    status: string
}

export type ImportTestCasesFileResponse = {
    status: 'completed' | 'partial_success'
    message: string
    import_result: unknown
    reindex_result?: ReindexResponse
    reindex_error?: string
}