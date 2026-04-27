import { useEffect } from 'react'

import { useToastStore } from './useToastStore'

export function ToastViewport() {
    const items = useToastStore((state) => state.items)
    const remove = useToastStore((state) => state.remove)

    useEffect(() => {
        if (items.length === 0) {
            return
        }

        const timers = items.map((item) =>
            window.setTimeout(() => {
                remove(item.id)
            }, 3500),
        )

        return () => {
            timers.forEach((timer) => window.clearTimeout(timer))
        }
    }, [items, remove])

    return (
        <div className="toast-viewport">
            {items.map((item) => (
                <div key={item.id} className={`toast toast--${item.type}`} role="status">
                    {item.message}
                </div>
            ))}
        </div>
    )
}