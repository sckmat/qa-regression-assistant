import axios from 'axios'

import { authStorage } from '../../features/auth/model/authStorage'
import { API_BASE_URL } from '../config/env'

export const httpClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
})

httpClient.interceptors.request.use((config) => {
    const token = authStorage.get()

    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
})