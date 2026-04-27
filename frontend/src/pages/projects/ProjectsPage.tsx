import { useProjectsQuery } from '../../entities/project/api/useProjectsQuery'
import { uiText } from '../../shared/constants/ui-text'
import { CreateProjectForm } from '../../features/create-project/ui/CreateProjectForm'
import { ProjectList } from '../../widgets/project-list/ProjectList'

export function ProjectsPage() {
    const { data, isLoading, isError } = useProjectsQuery()

    return (
        <section className="page">
            <div className="page__header">
                <div>
                    <h2 className="page__title">{uiText.projects.title}</h2>
                    <p className="page__description">{uiText.projects.description}</p>
                </div>
            </div>

            <div className="page-stack">
                <CreateProjectForm />

                <div className="card">
                    <div className="section-header">
                        <h3 className="section-title">{uiText.projects.listTitle}</h3>
                    </div>

                    {isLoading ? <p className="muted-text">{uiText.common.loading}</p> : null}

                    {isError ? (
                        <p className="error-text">
                            Не удалось загрузить проекты. Попробуйте обновить страницу.
                        </p>
                    ) : null}

                    {!isLoading && !isError ? <ProjectList projects={data ?? []} /> : null}
                </div>
            </div>
        </section>
    )
}