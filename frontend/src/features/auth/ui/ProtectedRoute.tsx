import { type PropsWithChildren } from 'react'
import { Navigate } from 'react-router-dom'

import { authStorage } from '../model/authStorage'

export function ProtectedRoute({ children }: PropsWithChildren) {
    if (!authStorage.hasToken()) {
        return <Navigate to="/login" replace />
    }

    return children
}