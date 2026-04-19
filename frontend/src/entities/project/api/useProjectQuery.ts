import { useQuery } from '@tanstack/react-query'

import { getProject } from './projects.api'

type UseProjectQueryParams = {
    projectId: number
}

export function useProjectQuery({ projectId }: UseProjectQueryParams) {
    return useQuery({
        queryKey: ['project', projectId],
        queryFn: () => getProject(projectId),
        enabled: Number.isFinite(projectId) && projectId > 0,
    })
}