import { useProjectsQuery } from '../../entities/project/api/useProjectsQuery'
import { CreateProjectForm } from '../../features/create-project/ui/CreateProjectForm'
import { ProjectList } from '../../widgets/project-list/ProjectList'

export function ProjectsPage() {
    const { data, isLoading, isError } = useProjectsQuery()

    return (
        <section className="page">
            <div className="page__header">
                <div>
                    <h2 className="page__title">Projects</h2>
                    <p className="page__description">
                        Точка входа в продукт. Здесь создаются и открываются проекты.
                    </p>
                </div>
            </div>

            <div className="page-stack">
                <CreateProjectForm />

                <div className="card">
                    <div className="section-header">
                        <h3 className="section-title">Список проектов</h3>
                    </div>

                    {isLoading ? <p className="muted-text">Загрузка проектов...</p> : null}

                    {isError ? (
                        <p className="error-text">
                            Не удалось загрузить проекты. Проверь доступность user_service и CORS.
                        </p>
                    ) : null}

                    {!isLoading && !isError ? <ProjectList projects={data ?? []} /> : null}
                </div>
            </div>
        </section>
    )
}