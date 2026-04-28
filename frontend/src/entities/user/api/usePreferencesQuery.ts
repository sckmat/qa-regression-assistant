import { useQuery } from '@tanstack/react-query'
import { getPreferences } from './preferences.api'

export function usePreferencesQuery() {
    return useQuery({
        queryKey: ['user-preferences'],
        queryFn: getPreferences,
    })
}