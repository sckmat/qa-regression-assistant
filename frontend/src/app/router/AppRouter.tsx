import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { AppShell } from '../../widgets/app-shell/AppShell'
import { NewRunPage } from '../../pages/new-run/NewRunPage'
import { ProjectDetailsPage } from '../../pages/project-details/ProjectDetailsPage'
import { ProjectsPage } from '../../pages/projects/ProjectsPage'
import { RunDetailsPage } from '../../pages/run-details/RunDetailsPage'
import { RunsPage } from '../../pages/runs/RunsPage'
import { TestCasesPage } from '../../pages/test-cases/TestCasesPage'

export function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/projects" replace />} />

                <Route element={<AppShell />}>
                    <Route path="/projects" element={<ProjectsPage />} />
                    <Route path="/projects/:projectId" element={<ProjectDetailsPage />} />
                    <Route path="/projects/:projectId/test-cases" element={<TestCasesPage />} />
                    <Route path="/projects/:projectId/runs" element={<RunsPage />} />
                    <Route path="/projects/:projectId/runs/new" element={<NewRunPage />} />
                    <Route path="/runs/:runId" element={<RunDetailsPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}