import { httpClient } from '../../../shared/api/http-client'
import type {
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    User,
} from '../model/types'

export const login = async (payload: LoginRequest) => {
    const { data } = await httpClient.post<AuthResponse>(
        '/api/v1/auth/login',
        payload,
    )
    return data
}

export const register = async (payload: RegisterRequest) => {
    const { data } = await httpClient.post<User>(
        '/api/v1/auth/register',
        payload,
    )
    return data
}

export const getMe = async () => {
    const { data } = await httpClient.get<User>('/api/v1/auth/me')
    return data
}