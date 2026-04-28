import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { register } from '../../entities/user/api/auth.api'
import { useToast } from '../../shared/ui/toast/useToast'
import { Link } from 'react-router-dom'

export function RegisterPage() {
    const navigate = useNavigate()
    const toast = useToast()

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [name, setName] = useState('')

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        try {
            await register({ email, password, full_name: name })
            toast.success('Аккаунт создан')
            navigate('/login')
        } catch {
            toast.error('Ошибка регистрации')
        }
    }

    return (
        <div className="auth-page">
            <form onSubmit={handleSubmit} className="auth-card">
                <h2>Регистрация</h2>

                <input
                    className="input"
                    placeholder="Имя"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />

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

                <button className="button">Создать</button>
                <p style={{ marginTop: 12, textAlign: 'center' }}>
                    Уже есть аккаунт? <Link to="/login">Войти</Link>
                </p>
            </form>
        </div>
    )
}