import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'

import { useCreateProjectMutation } from '../../../entities/project/api/useCreateProjectMutation'
import { uiText } from '../../../shared/constants/ui-text'
import { getUserErrorMessage } from '../../../shared/lib/get-user-error-message'
import { useToast } from '../../../shared/ui/toast/useToast'
import {
    createProjectSchema,
    type CreateProjectFormValues,
} from '../model/createProjectSchema'

export function CreateProjectForm() {
    const createProjectMutation = useCreateProjectMutation()
    const toast = useToast()

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
        try {
            await createProjectMutation.mutateAsync({
                name: values.name.trim(),
                description: values.description?.trim() ? values.description.trim() : null,
            })

            toast.success(uiText.toasts.projectCreated)
            reset()
        } catch (error) {
            toast.error(getUserErrorMessage(error))
        }
    })

    return (
        <div className="card">
            <h3 className="section-title">{uiText.projects.createTitle}</h3>

            <form className="project-form" onSubmit={onSubmit}>
                <div className="field">
                    <label className="label" htmlFor="project-name">
                        {uiText.projects.nameLabel}
                    </label>

                    <input
                        id="project-name"
                        className="input"
                        placeholder={uiText.projects.namePlaceholder}
                        {...register('name')}
                    />

                    {errors.name ? <p className="error-text">{errors.name.message}</p> : null}
                </div>

                <div className="field">
                    <label className="label" htmlFor="project-description">
                        {uiText.projects.descriptionLabel}
                    </label>

                    <textarea
                        id="project-description"
                        className="textarea"
                        rows={4}
                        placeholder={uiText.projects.descriptionPlaceholder}
                        {...register('description')}
                    />

                    {errors.description ? (
                        <p className="error-text">{errors.description.message}</p>
                    ) : null}
                </div>

                <div className="form-actions">
                    <button
                        className="button"
                        type="submit"
                        disabled={createProjectMutation.isPending}
                    >
                        {createProjectMutation.isPending
                            ? uiText.projects.creatingButton
                            : uiText.projects.createButton}
                    </button>
                </div>
            </form>
        </div>
    )
}