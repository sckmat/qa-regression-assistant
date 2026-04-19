import { Outlet } from 'react-router-dom'

import { Sidebar } from '../sidebar/Sidebar'
import { Topbar } from '../topbar/Topbar'

export function AppShell() {
    return (
        <div className="app-shell">
            <Sidebar />

            <div className="app-shell__content">
                <Topbar />

                <main className="app-shell__main">
                    <Outlet />
                </main>
            </div>
        </div>
    )
}