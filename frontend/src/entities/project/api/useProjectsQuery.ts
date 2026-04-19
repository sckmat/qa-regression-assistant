import { useQuery } from '@tanstack/react-query'

import { listProjects } from './projects.api'

export function useProjectsQuery() {
    return useQuery({
        queryKey: ['projects'],
        queryFn: listProjects,
    })
}