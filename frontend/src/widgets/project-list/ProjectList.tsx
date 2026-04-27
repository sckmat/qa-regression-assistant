import { Link } from 'react-router-dom'

import type { Project } from '../../entities/project/model/types'
import { uiText } from '../../shared/constants/ui-text'

type ProjectListProps = {
    projects: Project[]
}

export function ProjectList({ projects }: ProjectListProps) {
    if (projects.length === 0) {
        return (
            <div className="card empty-state">
                <p className="empty-state__title">{uiText.projects.emptyTitle}</p>
                <p className="empty-state__description">
                    {uiText.projects.emptyDescription}
                </p>
            </div>
        )
    }

    return (
        <div className="projects-grid">
            {projects.map((project) => (
                <Link key={project.id} to={`/projects/${project.id}`} className="project-card">
                    <div className="project-card__header">
                        <h3 className="project-card__title">{project.name}</h3>
                        <span className="project-card__badge">#{project.id}</span>
                    </div>

                    <p className="project-card__description">
                        {project.description?.trim()
                            ? project.description
                            : uiText.common.noDescription}
                    </p>
                </Link>
            ))}
        </div>
    )
}