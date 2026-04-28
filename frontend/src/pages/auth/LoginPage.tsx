import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'

import { login } from '../../entities/user/api/auth.api'
import { authStorage } from '../../features/auth/model/authStorage'
import { useToast } from '../../shared/ui/toast/useToast'

export function LoginPage() {
    const navigate = useNavigate()
    const toast = useToast()

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        try {
            const res = await login({ email, password })
            authStorage.set(res.access_token)

            toast.success('Вход выполнен')
            navigate('/projects')
        } catch {
            toast.error('Ошибка входа')
        }
    }

    return (
        <div className="auth-page">
            <form onSubmit={handleSubmit} className="auth-card">
                <h2>Вход</h2>

                <input
                    className="input"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />

                <input
                    className="input"
                    type="password"
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />

                <button className="button">Войти</button>

                <p>
                    Нет аккаунта? <Link to="/register">Регистрация</Link>
                </p>
            </form>
        </div>
    )
}