export type CandidateSortMode =
    | 'score_desc'
    | 'score_asc'
    | 'title_asc'
    | 'title_desc'

export type CandidateFilters = {
    query: string
    onlyWithExplanation: boolean
    onlyWithMatchedTerms: boolean
    sortMode: CandidateSortMode
}