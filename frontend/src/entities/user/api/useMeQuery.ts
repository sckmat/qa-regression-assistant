import { useQuery } from '@tanstack/react-query'
import { httpClient } from '../../../shared/api/http-client'

export type MeResponse = {
    id: number
    email: string
    full_name: string
}

export function useMeQuery() {
    return useQuery({
        queryKey: ['me'],
        queryFn: async () => {
            const { data } = await httpClient.get<MeResponse>('/api/v1/auth/me')
            return data
        },
        retry: false,
    })
}