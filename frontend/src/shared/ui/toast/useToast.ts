import { useToastStore } from './useToastStore'

export function useToast() {
    const push = useToastStore((state) => state.push)

    return {
        success: (message: string) => push({ type: 'success', message }),
        error: (message: string) => push({ type: 'error', message }),
        info: (message: string) => push({ type: 'info', message }),
    }
}