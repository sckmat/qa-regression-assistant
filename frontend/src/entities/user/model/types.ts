export type User = {
    id: number
    email: string
    full_name: string
}

export type LoginRequest = {
    email: string
    password: string
}

export type RegisterRequest = {
    email: string
    password: string
    full_name: string
}

export type AuthResponse = {
    access_token: string
    token_type: 'bearer'
    user: User
}

export type UserPreference = {
    default_search_mode: 'lexical' | 'semantic' | 'semantic_llm'
    preferred_llm_provider: string
}

export type LlmProviderCapability = {
    code: string
    label: string
    enabled: boolean
    reason: string | null
}

export type AppCapabilities = {
    llm_providers: LlmProviderCapability[]
}