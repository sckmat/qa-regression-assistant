import { useEffect } from 'react'
import { useForm } from 'react-hook-form'

import { usePreferencesQuery } from '../../../entities/user/api/usePreferencesQuery'
import { useCapabilitiesQuery } from '../../../entities/user/api/useCapabilitiesQuery'

type StartRegressionRunFormValues = {
    change_summary: string
    candidate_limit: number
    search_mode: 'lexical' | 'semantic' | 'semantic_llm'
}

type Props = {
    onSubmit: (values: StartRegressionRunFormValues) => Promise<void>
    isLoading?: boolean
}

export function StartRegressionRunForm({ onSubmit, isLoading }: Props) {
    const preferencesQuery = usePreferencesQuery()
    const capabilitiesQuery = useCapabilitiesQuery()

    const {
        register,
        handleSubmit,
        setValue,
        watch,
        formState: { errors },
    } = useForm<StartRegressionRunFormValues>({
        defaultValues: {
            change_summary: '',
            candidate_limit: 5,
            search_mode: 'semantic_llm',
        },
    })

    useEffect(() => {
        if (preferencesQuery.data?.default_search_mode) {
            setValue('search_mode', preferencesQuery.data.default_search_mode)
        }
    }, [preferencesQuery.data?.default_search_mode, setValue])

    const currentMode = watch('search_mode')

    const isLlmAvailable = capabilitiesQuery.data?.llm_providers
        ?.find((p) => p.code === 'openai')
        ?.enabled ?? false

    const submitHandler = handleSubmit(async (values) => {
        await onSubmit(values)
    })

    return (
        <form className="card project-form" onSubmit={submitHandler}>
            <h3 className="section-title">Запуск анализа</h3>

            {/* Описание изменений */}
            <div className="field">
                <label className="label">Описание изменений</label>

                <textarea
                    className="textarea"
                    placeholder="Например: Изменен экран логина, добавлена валидация email..."
                    {...register('change_summary', {
                        required: 'Введите описание изменений',
                    })}
                />

                {errors.change_summary && (
                    <p className="error-text">{errors.change_summary.message}</p>
                )}
            </div>

            {/* Количество кандидатов */}
            <div className="field">
                <label className="label">Количество кандидатов</label>

                <input
                    type="number"
                    className="input"
                    {...register('candidate_limit', {
                        valueAsNumber: true,
                        min: 1,
                        max: 20,
                    })}
                />
            </div>

            {/* Режим */}
            <div className="field">
                <label className="label">Режим анализа</label>

                <select className="input" {...register('search_mode')}>
                    <option value="lexical">Лексический</option>
                    <option value="semantic">Семантический</option>
                    <option value="semantic_llm" disabled={!isLlmAvailable}>
                        Семантический + модель {!isLlmAvailable ? '(недоступно)' : ''}
                    </option>
                </select>

                {/* 🔥 Подсказки UX */}
                {currentMode === 'semantic_llm' && (
                    <p className="hint">
                        Будет выполнен семантический поиск с дополнительной фильтрацией через модель.
                    </p>
                )}

                {currentMode === 'semantic_llm' && !isLlmAvailable && (
                    <p className="error-text">
                        Модель недоступна. Будет использован только семантический поиск.
                    </p>
                )}
            </div>

            {/* Кнопка */}
            <button className="button" disabled={isLoading}>
                {isLoading ? 'Запуск...' : 'Запустить анализ'}
            </button>
        </form>
    )
}