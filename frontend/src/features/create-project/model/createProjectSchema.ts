import { z } from 'zod'

export const createProjectSchema = z.object({
    name: z
        .string()
        .trim()
        .min(2, 'Название проекта должно содержать минимум 2 символа')
        .max(100, 'Название проекта не должно быть длиннее 100 символов'),

    description: z
        .string()
        .max(500, 'Описание не должно быть длиннее 500 символов')
        .optional(),
})

export type CreateProjectFormValues = z.infer<typeof createProjectSchema>