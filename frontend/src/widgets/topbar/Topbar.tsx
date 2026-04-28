import { useNavigate } from 'react-router-dom'
import { useQueryClient } from '@tanstack/react-query'

import { useMeQuery } from '../../entities/user/api/useMeQuery'
import { authStorage } from '../../features/auth/model/authStorage'
import { uiText } from '../../shared/constants/ui-text'

export function Topbar() {
    const navigate = useNavigate()
    const queryClient = useQueryClient()
    const meQuery = useMeQuery()

    const handleLogout = async () => {
        authStorage.clear()
        queryClient.clear()
        navigate('/login')
    }

    return (
        <header className="topbar">
            <div className="topbar__left">
                <h1 className="topbar__title">{uiText.app.title}</h1>
                <p className="topbar__subtitle">{uiText.app.subtitle}</p>
            </div>

            <div className="topbar__right">
                {meQuery.data && (
                    <div className="topbar__user-card">
                        <div className="topbar__avatar">
                            {meQuery.data.full_name.charAt(0).toUpperCase()}
                        </div>

                        <div className="topbar__user-info">
              <span className="topbar__user-name">
                {meQuery.data.full_name}
              </span>
                            <span className="topbar__user-email">
                {meQuery.data.email}
              </span>
                        </div>
                    </div>
                )}

                <button
                    className="button button--secondary topbar__logout"
                    type="button"
                    onClick={handleLogout}
                >
                    Выйти
                </button>
            </div>
        </header>
    )
}