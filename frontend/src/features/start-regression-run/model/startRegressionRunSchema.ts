import { z } from 'zod'

export const startRegressionRunSchema = z.object({
    change_summary: z
        .string()
        .trim()
        .min(10, 'Описание изменений должно содержать минимум 10 символов')
        .max(5000, 'Описание изменений не должно быть длиннее 5000 символов'),

    candidate_limit: z.coerce
        .number()
        .int('Количество кандидатов должно быть целым числом')
        .min(1, 'Минимум 1 кандидат')
        .max(20, 'Максимум 20 кандидатов'),

    search_mode: z.enum(['lexical', 'semantic', 'semantic_llm']),
})

export type StartRegressionRunFormInput = z.input<typeof startRegressionRunSchema>
export type StartRegressionRunFormValues = z.output<typeof startRegressionRunSchema>