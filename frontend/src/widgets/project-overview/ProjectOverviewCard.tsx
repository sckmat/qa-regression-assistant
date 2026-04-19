import type { Project } from '../../entities/project/model/types'

type ProjectOverviewCardProps = {
    project: Project
}

export function ProjectOverviewCard({ project }: ProjectOverviewCardProps) {
    return (
        <div className="card">
            <div className="project-overview">
                <div className="project-overview__meta">
                    <span className="project-overview__badge">Project #{project.id}</span>
                </div>

                <div className="project-overview__content">
                    <h3 className="project-overview__title">{project.name}</h3>
                    <p className="project-overview__description">
                        {project.description?.trim()
                            ? project.description
                            : 'Описание проекта пока не указано'}
                    </p>
                </div>
            </div>
        </div>
    )
}