const ACCESS_TOKEN_KEY = 'access_token'

export const authStorage = {
    get: () => localStorage.getItem(ACCESS_TOKEN_KEY),

    set: (token: string) => {
        localStorage.setItem(ACCESS_TOKEN_KEY, token)
    },

    clear: () => {
        localStorage.removeItem(ACCESS_TOKEN_KEY)
    },

    hasToken: () => {
        return Boolean(localStorage.getItem(ACCESS_TOKEN_KEY))
    },
}