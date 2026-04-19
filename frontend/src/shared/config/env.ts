const rawApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim()

export const API_BASE_URL =
    rawApiBaseUrl && rawApiBaseUrl.length > 0
        ? rawApiBaseUrl
        : 'http://127.0.0.1:8000'