import { create } from 'zustand'

export type ToastType = 'success' | 'error' | 'info'

export type ToastItem = {
    id: string
    type: ToastType
    message: string
}

type ToastStore = {
    items: ToastItem[]
    push: (toast: Omit<ToastItem, 'id'>) => void
    remove: (id: string) => void
}

export const useToastStore = create<ToastStore>((set) => ({
    items: [],
    push: (toast) =>
        set((state) => ({
            items: [
                ...state.items,
                {
                    ...toast,
                    id: crypto.randomUUID(),
                },
            ],
        })),
    remove: (id) =>
        set((state) => ({
            items: state.items.filter((item) => item.id !== id),
        })),
}))