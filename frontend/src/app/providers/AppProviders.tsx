import { type PropsWithChildren, useState } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

import { ToastViewport } from '../../shared/ui/toast/ToastViewport'

export function AppProviders({ children }: PropsWithChildren) {
    const [queryClient] = useState(
        () =>
            new QueryClient({
                defaultOptions: {
                    queries: {
                        retry: 1,
                        refetchOnWindowFocus: false,
                    },
                    mutations: {
                        retry: 0,
                    },
                },
            }),
    )

    return (
        <QueryClientProvider client={queryClient}>
            {children}
            <ToastViewport />
        </QueryClientProvider>
    )
}