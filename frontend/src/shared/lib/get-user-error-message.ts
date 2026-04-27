import axios from 'axios'

export function getUserErrorMessage(error: unknown): string {
    if (axios.isAxiosError(error)) {
        const status = error.response?.status

        if (status === 400) {
            return 'Не удалось выполнить операцию из-за некорректных данных.'
        }

        if (status === 404) {
            return 'Запрошенные данные не найдены.'
        }

        if (status === 409) {
            return 'Операция не выполнена из-за конфликта данных.'
        }

        if (status === 413) {
            return 'Файл слишком большой.'
        }

        if (status === 415) {
            return 'Неподдерживаемый формат файла.'
        }

        if (status === 500 || status === 502 || status === 503 || status === 504) {
            return 'Сервис временно недоступен. Попробуйте позже.'
        }

        if (error.code === 'ECONNABORTED') {
            return 'Превышено время ожидания ответа. Попробуйте еще раз.'
        }

        return 'Не удалось выполнить запрос. Попробуйте еще раз.'
    }

    return 'Произошла непредвиденная ошибка.'
}