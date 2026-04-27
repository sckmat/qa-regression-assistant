import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'

import { useCreateRegressionRunMutation } from '../../../entities/regression-run/api/useCreateRegressionRunMutation'
import { uiText } from '../../../shared/constants/ui-text'
import { getUserErrorMessage } from '../../../shared/lib/get-user-error-message'
import { useToast } from '../../../shared/ui/toast/useToast'
import {
    startRegressionRunSchema,
    type StartRegressionRunFormValues, type StartRegressionRunFormInput,
} from '../model/startRegressionRunSchema'

type StartRegressionRunFormProps = {
    projectId: number
}

const modeOptions = [
    {
        value: 'lexical',
        label: uiText.newRun.modes.lexical.label,
        description: uiText.newRun.modes.lexical.description,
    },
    {
        value: 'semantic',
        label: uiText.newRun.modes.semantic.label,
        description: uiText.newRun.modes.semantic.description,
    },
    {
        value: 'semantic_llm',
        label: uiText.newRun.modes.semanticLlm.label,
        description: uiText.newRun.modes.semanticLlm.description,
    },
] as const

export function StartRegressionRunForm({
                                           projectId,
                                       }: StartRegressionRunFormProps) {
    const navigate = useNavigate()
    const createRegressionRunMutation = useCreateRegressionRunMutation({ projectId })
    const toast = useToast()

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<StartRegressionRunFormInput, unknown, StartRegressionRunFormValues>({
        resolver: zodResolver(startRegressionRunSchema),
        defaultValues: {
            change_summary: '',
            candidate_limit: 5,
            search_mode: 'semantic_llm',
        },
    })

    const onSubmit = handleSubmit(async (values) => {
        try {
            const createdRun = await createRegressionRunMutation.mutateAsync({
                change_summary: values.change_summary.trim(),
                candidate_limit: values.candidate_limit,
                search_mode: values.search_mode,
            })

            toast.success(uiText.toasts.runStarted)
            navigate(`/runs/${createdRun.id}`)
        } catch (error) {
            toast.error(getUserErrorMessage(error))
        }
    })

    return (
        <div className="card">
            <h3 className="section-title">{uiText.newRun.formTitle}</h3>

            <form className="project-form" onSubmit={onSubmit}>
                <div className="field">
                    <label className="label" htmlFor="change-summary">
                        {uiText.newRun.changeSummaryLabel}
                    </label>

                    <textarea
                        id="change-summary"
                        className="textarea textarea--large"
                        rows={8}
                        placeholder={uiText.newRun.changeSummaryPlaceholder}
                        {...register('change_summary')}
                    />

                    {errors.change_summary ? (
                        <p className="error-text">{errors.change_summary.message}</p>
                    ) : null}
                </div>

                <div className="form-grid">
                    <div className="field">
                        <label className="label" htmlFor="candidate-limit">
                            {uiText.newRun.candidateLimitLabel}
                        </label>

                        <input
                            id="candidate-limit"
                            className="input"
                            type="number"
                            min={1}
                            max={20}
                            {...register('candidate_limit')}
                        />

                        {errors.candidate_limit ? (
                            <p className="error-text">{errors.candidate_limit.message}</p>
                        ) : null}
                    </div>

                    <div className="field">
                        <label className="label" htmlFor="search-mode">
                            {uiText.newRun.searchModeLabel}
                        </label>

                        <select
                            id="search-mode"
                            className="input"
                            {...register('search_mode')}
                        >
                            {modeOptions.map((option) => (
                                <option key={option.value} value={option.value}>
                                    {option.label}
                                </option>
                            ))}
                        </select>

                        {errors.search_mode ? (
                            <p className="error-text">{errors.search_mode.message}</p>
                        ) : null}
                    </div>
                </div>

                <div className="mode-hints">
                    {modeOptions.map((option) => (
                        <div key={option.value} className="mode-hint">
                            <p className="mode-hint__title">{option.label}</p>
                            <p className="mode-hint__description">{option.description}</p>
                        </div>
                    ))}
                </div>

                <div className="form-actions">
                    <button
                        className="button"
                        type="submit"
                        disabled={createRegressionRunMutation.isPending}
                    >
                        {createRegressionRunMutation.isPending
                            ? uiText.newRun.submittingButton
                            : uiText.newRun.submitButton}
                    </button>
                </div>
            </form>
        </div>
    )
}