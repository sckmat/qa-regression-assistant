import { NavLink } from 'react-router-dom'

export function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="sidebar__logo">QA Assistant</div>

            <nav className="sidebar__nav">
                <NavLink
                    to="/projects"
                    className={({ isActive }) =>
                        isActive ? 'sidebar__link sidebar__link--active' : 'sidebar__link'
                    }
                >
                    Projects
                </NavLink>
            </nav>
        </aside>
    )
}