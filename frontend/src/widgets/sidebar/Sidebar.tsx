import { NavLink } from 'react-router-dom'

import { uiText } from '../../shared/constants/ui-text'

export function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="sidebar__logo">{uiText.app.title}</div>

            <nav className="sidebar__nav">
                <NavLink
                    to="/projects"
                    className={({ isActive }) =>
                        isActive ? 'sidebar__link sidebar__link--active' : 'sidebar__link'
                    }
                >
                    {uiText.navigation.projects}
                </NavLink>
            </nav>
        </aside>
    )
}