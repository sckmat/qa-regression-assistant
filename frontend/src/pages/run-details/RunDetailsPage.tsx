import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { useRegressionRunQuery } from '../../entities/regression-run/api/useRegressionRunQuery'
import type { RegressionRunCandidate } from '../../entities/regression-run/model/types'
import { uiText } from '../../shared/constants/ui-text'
import { CandidatesFilterBar } from '../../features/filter-candidates/ui/CandidatesFilterBar'
import type { CandidateFilters } from '../../features/filter-candidates/model/types'
import { CandidatesList } from '../../widgets/candidates-list/CandidatesList'
import RunOverviewCard from '../../widgets/run-overview/RunOverviewCard'

function parseRunId(value: string | undefined): number {
    if (!value) {
        return NaN
    }

    return Number(value)
}

const defaultFilters: CandidateFilters = {
    query: '',
    onlyWithExplanation: false,
    onlyWithMatchedTerms: false,
    sortMode: 'score_desc',
}

function sortCandidates(
    candidates: RegressionRunCandidate[],
    sortMode: CandidateFilters['sortMode'],
) {
    const next = [...candidates]

    if (sortMode === 'score_desc') {
        next.sort((a, b) => b.relevance_score - a.relevance_score)
        return next
    }

    if (sortMode === 'score_asc') {
        next.sort((a, b) => a.relevance_score - b.relevance_score)
        return next
    }

    if (sortMode === 'title_asc') {
        next.sort((a, b) => a.title.localeCompare(b.title, 'ru'))
        return next
    }

    next.sort((a, b) => b.title.localeCompare(a.title, 'ru'))
    return next
}

export function RunDetailsPage() {
    const { runId: rawRunId } = useParams()
    const runId = parseRunId(rawRunId)

    const runQuery = useRegressionRunQuery({ runId })
    const [filters, setFilters] = useState<CandidateFilters>(defaultFilters)

    const filteredCandidates = useMemo(() => {
        const candidates = runQuery.data?.candidates ?? []

        const normalizedQuery = filters.query.trim().toLowerCase()

        const next = candidates.filter((candidate) => {
            if (
                normalizedQuery &&
                !candidate.title.toLowerCase().includes(normalizedQuery)
            ) {
                return false
            }

            if (filters.onlyWithExplanation && !candidate.explanation?.trim()) {
                return false
            }

            if (
                filters.onlyWithMatchedTerms &&
                (!candidate.matched_terms || candidate.matched_terms.length === 0)
            ) {
                return false
            }

            return true
        })

        return sortCandidates(next, filters.sortMode)
    }, [filters, runQuery.data?.candidates])

    if (!Number.isFinite(runId) || runId <= 0) {
        return (
            <section className="page">
                <div className="card">
                    <p className="error-text">Некорректный идентификатор запуска.</p>
                </div>
            </section>
        )
    }

    return (
        <section className="page">
            <div className="page__header">
                <div>
                    <h2 className="page__title">{uiText.runDetails.title}</h2>
                    <p className="page__description">{uiText.runDetails.description}</p>
                </div>

                {runQuery.data ? (
                    <Link
                        className="button button--secondary"
                        to={`/projects/${runQuery.data.project_id}/runs`}
                    >
                        {uiText.runDetails.backButton}
                    </Link>
                ) : null}
            </div>

            {runQuery.isLoading ? (
                <div className="card">
                    <p className="muted-text">Загрузка результатов запуска...</p>
                </div>
            ) : null}

            {runQuery.isError ? (
                <div className="card">
                    <p className="error-text">
                        Не удалось загрузить результаты запуска. Попробуйте позже.
                    </p>
                </div>
            ) : null}

            {runQuery.data ? (
                <>
                    <RunOverviewCard run={runQuery.data} />
                    <CandidatesFilterBar value={filters} onChange={setFilters} />
                    <CandidatesList candidates={filteredCandidates} />
                </>
            ) : null}
        </section>
    )
}