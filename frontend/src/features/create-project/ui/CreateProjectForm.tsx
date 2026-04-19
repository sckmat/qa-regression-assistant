import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'

import { useCreateProjectMutation } from '../../../entities/project/api/useCreateProjectMutation'
import {
    createProjectSchema,
    type CreateProjectFormValues,
} from '../model/createProjectSchema'

export function CreateProjectForm() {
    const createProjectMutation = useCreateProjectMutation()

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm<CreateProjectFormValues>({
        resolver: zodResolver(createProjectSchema),
        defaultValues: {
            name: '',
            description: '',
        },
    })

    const onSubmit = handleSubmit(async (values) => {
        await createProjectMutation.mutateAsync({
            name: values.name.trim(),
            description: values.description?.trim() ? values.description.trim() : null,
        })

        reset()
    })

    return (
        <div className="card">
            <h3 className="section-title">Создать проект</h3>

            <form className="project-form" onSubmit={onSubmit}>
                <div className="field">
                    <label className="label" htmlFor="project-name">
                        Название
                    </label>

                    <input
                        id="project-name"
                        className="input"
                        placeholder="Например, Mobile Banking QA"
                        {...register('name')}
                    />

                    {errors.name ? <p className="error-text">{errors.name.message}</p> : null}
                </div>

                <div className="field">
                    <label className="label" htmlFor="project-description">
                        Описание
                    </label>

                    <textarea
                        id="project-description"
                        className="textarea"
                        rows={4}
                        placeholder="Коротко опиши проект"
                        {...register('description')}
                    />

                    {errors.description ? (
                        <p className="error-text">{errors.description.message}</p>
                    ) : null}
                </div>

                {createProjectMutation.isError ? (
                    <p className="error-text">
                        Не удалось создать проект. Проверь доступность backend.
                    </p>
                ) : null}

                <div className="form-actions">
                    <button
                        className="button"
                        type="submit"
                        disabled={createProjectMutation.isPending}
                    >
                        {createProjectMutation.isPending ? 'Создание...' : 'Создать проект'}
                    </button>
                </div>
            </form>
        </div>
    )
}