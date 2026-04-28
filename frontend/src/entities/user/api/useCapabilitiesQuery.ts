import { useQuery } from '@tanstack/react-query'
import { getCapabilities } from './capabilities.api'

export function useCapabilitiesQuery() {
    return useQuery({
        queryKey: ['capabilities'],
        queryFn: getCapabilities,
    })
}