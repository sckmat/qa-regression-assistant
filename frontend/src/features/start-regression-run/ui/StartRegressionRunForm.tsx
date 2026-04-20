import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'

import { useCreateRegressionRunMutation } from '../../../entities/regression-run/api/useCreateRegressionRunMutation'
import {
    startRegressionRunSchema,
    type StartRegressionRunFormInput,
    type StartRegressionRunFormValues,
} from '../model/startRegressionRunSchema'

type StartRegressionRunFormProps = {
    projectId: number
}

const modeOptions = [
    {
        value: 'lexical',
        label: 'Lexical',
        description: 'Базовый поиск по ключевым словам и matched terms.',
    },
    {
        value: 'semantic',
        label: 'Semantic',
        description: 'Семантический поиск по embeddings и pgvector.',
    },
    {
        value: 'semantic_llm',
        label: 'Semantic + LLM',
        description: 'Семантический поиск с последующим rerank и explanation от LLM.',
    },
] as const

export function StartRegressionRunForm({
                                           projectId,
                                       }: StartRegressionRunFormProps) {
    const navigate = useNavigate()
    const createRegressionRunMutation = useCreateRegressionRunMutation({ projectId })

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
        const createdRun = await createRegressionRunMutation.mutateAsync({
            change_summary: values.change_summary.trim(),
            candidate_limit: values.candidate_limit,
            search_mode: values.search_mode,
        })

        navigate(`/runs/${createdRun.id}`)
    })

    return (
        <div className="card">
            <h3 className="section-title">Новый запуск анализа</h3>

            <form className="project-form" onSubmit={onSubmit}>
                <div className="field">
                    <label className="label" htmlFor="change-summary">
                        Описание изменений
                    </label>

                    <textarea
                        id="change-summary"
                        className="textarea textarea--large"
                        rows={8}
                        placeholder="Например: Изменен экран логина, добавлена валидация email и обработка ошибки 401..."
                        {...register('change_summary')}
                    />

                    {errors.change_summary ? (
                        <p className="error-text">{errors.change_summary.message}</p>
                    ) : null}
                </div>

                <div className="form-grid">
                    <div className="field">
                        <label className="label" htmlFor="candidate-limit">
                            Candidate limit
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
                            Режим поиска
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

                {createRegressionRunMutation.isError ? (
                    <p className="error-text">
                        Не удалось создать запуск. Проверь доступность user_service, data_service и llm_service.
                    </p>
                ) : null}

                <div className="form-actions">
                    <button
                        className="button"
                        type="submit"
                        disabled={createRegressionRunMutation.isPending}
                    >
                        {createRegressionRunMutation.isPending
                            ? 'Запуск...'
                            : 'Запустить анализ'}
                    </button>
                </div>
            </form>
        </div>
    )
}