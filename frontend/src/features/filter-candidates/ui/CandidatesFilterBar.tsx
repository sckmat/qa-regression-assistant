import type { CandidateFilters, CandidateSortMode } from '../model/types'
import { uiText } from '../../../shared/constants/ui-text'

type CandidatesFilterBarProps = {
    value: CandidateFilters
    onChange: (next: CandidateFilters) => void
}

export function CandidatesFilterBar({
                                        value,
                                        onChange,
                                    }: CandidatesFilterBarProps) {
    const handleSortChange = (sortMode: string) => {
        onChange({
            ...value,
            sortMode: sortMode as CandidateSortMode,
        })
    }

    return (
        <div className="card">
            <div className="section-header">
                <h3 className="section-title">{uiText.runDetails.filtersTitle}</h3>
            </div>

            <div className="filters-grid">
                <div className="field">
                    <label className="label" htmlFor="candidate-query">
                        {uiText.runDetails.searchByTitle}
                    </label>
                    <input
                        id="candidate-query"
                        className="input"
                        value={value.query}
                        onChange={(event) =>
                            onChange({
                                ...value,
                                query: event.target.value,
                            })
                        }
                        placeholder={uiText.runDetails.searchByTitlePlaceholder}
                    />
                </div>

                <div className="field">
                    <label className="label" htmlFor="candidate-sort">
                        {uiText.runDetails.sortLabel}
                    </label>
                    <select
                        id="candidate-sort"
                        className="input"
                        value={value.sortMode}
                        onChange={(event) => handleSortChange(event.target.value)}
                    >
                        <option value="score_desc">
                            {uiText.runDetails.sortOptions.scoreDesc}
                        </option>
                        <option value="score_asc">
                            {uiText.runDetails.sortOptions.scoreAsc}
                        </option>
                        <option value="title_asc">
                            {uiText.runDetails.sortOptions.titleAsc}
                        </option>
                        <option value="title_desc">
                            {uiText.runDetails.sortOptions.titleDesc}
                        </option>
                    </select>
                </div>
            </div>

            <div className="checkbox-row">
                <label className="checkbox-label">
                    <input
                        type="checkbox"
                        checked={value.onlyWithExplanation}
                        onChange={(event) =>
                            onChange({
                                ...value,
                                onlyWithExplanation: event.target.checked,
                            })
                        }
                    />
                    <span>{uiText.runDetails.onlyWithExplanation}</span>
                </label>

                <label className="checkbox-label">
                    <input
                        type="checkbox"
                        checked={value.onlyWithMatchedTerms}
                        onChange={(event) =>
                            onChange({
                                ...value,
                                onlyWithMatchedTerms: event.target.checked,
                            })
                        }
                    />
                    <span>{uiText.runDetails.onlyWithMatchedTerms}</span>
                </label>
            </div>
        </div>
    )
}