import { httpClient } from '../../../shared/api/http-client'
import type { UserPreference } from '../model/types'

export const getPreferences = async () => {
    const { data } = await httpClient.get<UserPreference>(
        '/api/v1/me/preferences',
    )
    return data
}

export const updatePreferences = async (payload: Partial<UserPreference>) => {
    const { data } = await httpClient.patch<UserPreference>(
        '/api/v1/me/preferences',
        payload,
    )
    return data
}