import { httpClient } from '../../../shared/api/http-client'
import type { AppCapabilities } from '../model/types'

export const getCapabilities = async () => {
    const { data } = await httpClient.get<AppCapabilities>(
        '/api/v1/app/capabilities',
    )
    return data
}