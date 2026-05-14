# QA Regression Assistant

**QA Regression Assistant** — интеллектуальный ассистент QA-инженера для автоматического формирования регрессионного набора тест-кейсов по описанию изменений.

Система помогает загрузить тестовую базу, проиндексировать тест-кейсы, найти релевантные проверки по текстовому описанию изменения и сформировать набор кандидатов для регрессионного тестирования. В MVP поддерживаются лексический поиск, семантический поиск по эмбеддингам и дополнительное объяснение с помощью LLM.

> Проект разработан в рамках выпускной квалификационной работы: **«Разработка интеллектуального ассистента для автоматического формирования регрессионного набора тест-кейсов на основе больших языковых моделей»**.

---

## Содержание

- [Возможности](#возможности)
- [Архитектура](#архитектура)
- [Технологический стек](#технологический-стек)
- [Требования для запуска](#требования-для-запуска)
- [Подготовка Ollama](#подготовка-ollama)
- [Настройка переменных окружения](#настройка-переменных-окружения)
- [Запуск через Docker Compose](#запуск-через-docker-compose)
- [Проверка работоспособности](#проверка-работоспособности)
- [Как пользоваться приложением](#как-пользоваться-приложением)
- [Формат файла с тест-кейсами](#формат-файла-с-тест-кейсами)
- [Типовые проблемы](#типовые-проблемы)
- [Структура проекта](#структура-проекта)

---

## Возможности

- регистрация и вход пользователя;
- создание проектов;
- загрузка тест-кейсов из JSON-файла;
- индексирование тест-кейсов с построением эмбеддингов;
- лексический поиск по тестовой базе;
- семантический поиск через PostgreSQL + pgvector;
- LLM-объяснение найденных кандидатов;
- отображение результата анализа с оценками релевантности и пояснениями;
- поддержка OpenAI и локальной Ollama через настройки окружения.

---

## Архитектура

Проект построен как набор сервисов, запускаемых через Docker Compose.

### Компоненты

| Компонент | Назначение |
|---|---|
| `frontend` | Web-интерфейс для работы с проектами, тест-кейсами и результатами анализа |
| `user_service` | Центральный backend-сервис: пользователи, проекты, запуски анализа, координация сценариев |
| `data_service` | Импорт, хранение, индексирование и поиск тест-кейсов |
| `llm_service` | Взаимодействие с LLM-провайдерами и ранжирование кандидатов |
| `postgres` | PostgreSQL с расширением `pgvector` для хранения данных и эмбеддингов |

---

## Технологический стек

### Backend

- Python
- FastAPI
- SQLAlchemy Async
- Pydantic
- PostgreSQL
- pgvector
- httpx

### Frontend

- React
- TypeScript
- Vite
- React Router
- CSS

### Инфраструктура

- Docker
- Docker Compose
- Caddy
- nginx
- Ollama
- OpenAI API, опционально

---

## Требования для запуска

### Обязательно

- Windows 10/11, macOS или Linux;
- Docker Desktop с поддержкой Docker Compose;
- Git;
- Ollama, если используется локальный LLM/embedding-провайдер.
- Ключ OpenAI API, опционально

## Подготовка Ollama

Ollama запускается **на компьютере**, а контейнеры обращаются к ней через адрес:

```env
host.docker.internal:11434
```

### 1. Установить Ollama

Скачайте и установите Ollama:

```text
https://ollama.com/download
```

Проект использует OpenAI-compatible endpoint `/v1/responses` для LLM-запросов, поэтому рекомендуется использовать актуальную версию Ollama.

### 2. Скачать модели

Для локального режима нужны две модели:

```powershell
ollama pull nomic-embed-text
ollama pull llama3.1
```

Назначение моделей:

| Модель | Для чего используется                            |
|---|--------------------------------------------------|
| `nomic-embed-text` | построение эмбеддингов для семантического поиска |
| `llama3.1` | LLM-обработка найденных тест-кейсов              |

## Настройка переменных окружения

Все переменные для локального Docker Compose-запуска лежат в папке `deploy`.

В репозиторий добавляется только пример:

```text
deploy/.env.example
```

Создайте файл окружения:

```powershell
Copy-Item deploy\.env.example deploy\.env
```

### Вариант 1. Полностью локальный запуск через Ollama

Подходит, если не хотите использовать OpenAI API.

```env
COMPOSE_PROJECT_NAME=qa-regression-assistant

OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_LLM_MODEL=gpt-4.1-mini

OLLAMA_EMBEDDING_BASE_URL=http://host.docker.internal:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_LLM_BASE_URL=http://host.docker.internal:11434/v1
OLLAMA_LLM_MODEL=llama3.1

DEFAULT_EMBEDDING_PROVIDER=ollama
DEFAULT_LLM_PROVIDER=ollama
OPENAI_ENABLED=false
OLLAMA_ENABLED=true
```

### Вариант 2. Запуск через OpenAI

Подходит, если хотите использовать облачные модели OpenAI.

```env
COMPOSE_PROJECT_NAME=qa-regression-assistant

OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_LLM_MODEL=gpt-4.1-mini

OLLAMA_EMBEDDING_BASE_URL=http://host.docker.internal:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_LLM_BASE_URL=http://host.docker.internal:11434/v1
OLLAMA_LLM_MODEL=llama3.1

DEFAULT_EMBEDDING_PROVIDER=openai
DEFAULT_LLM_PROVIDER=openai
OPENAI_ENABLED=true
OLLAMA_ENABLED=false
```

### Вариант 3. Смешанный режим

```env
DEFAULT_EMBEDDING_PROVIDER=ollama
DEFAULT_LLM_PROVIDER=openai
OPENAI_ENABLED=true
OLLAMA_ENABLED=true
```

---

## Запуск через Docker Compose

Все команды выполняются из корневой папки репозитория.

Для Windows путь может выглядеть так:

```powershell
cd D:\GitHub\qa-regression-assistant
```

### Первый запуск

```powershell
docker compose --env-file deploy\.env -f deploy\docker-compose.yml up --build
```

После успешного запуска приложение будет доступно по адресу:

```text
http://localhost:8080
```

### Остановка

```powershell
docker compose --env-file deploy\.env -f deploy\docker-compose.yml down
```

### Остановка с удалением локальной базы данных

```powershell
docker compose --env-file deploy\.env -f deploy\docker-compose.yml down -v
```

Команда с `-v` удаляет Docker volume с PostgreSQL. Используйте ее только если нужно полностью сбросить локальные данные.

---

## Проверка работоспособности

После запуска доступны следующие адреса:

| Сервис | URL |
|---|---|
| Web-приложение | `http://localhost:8080` |
| user_service Swagger UI | `http://localhost:8000/docs` |
| data_service Swagger UI | `http://localhost:8001/docs` |
| llm_service Swagger UI | `http://localhost:8002/docs` |
| user_service health | `http://localhost:8000/health` |
| data_service health | `http://localhost:8001/health` |

---

## Как пользоваться приложением

1. Откройте приложение:

```text
http://localhost:8080
```

2. Зарегистрируйте пользователя.
3. Войдите в систему.
4. Создайте проект.
5. Перейдите в проект.
6. Импортируйте JSON-файл с тест-кейсами.
7. Запустите индексирование тестовой базы.
8. Перейдите к запуску анализа.
9. Введите описание изменения.
10. Выберите режим анализа:

| Режим | Что делает |
|---|---|
| `lexical` | ищет тест-кейсы по совпадениям слов и фраз |
| `semantic` | ищет тест-кейсы по смысловой близости через эмбеддинги |
| `semantic_llm` | сначала выполняет семантический поиск, затем уточняет результат через LLM |

11. Запустите анализ.
12. Откройте страницу результата и проверьте предложенный регрессионный набор.

---

## Формат файла с тест-кейсами

Импорт выполняется из JSON-файла.

Поля:

| Поле | Обязательное | Описание |
|---|---:|---|
| `items` | да | массив тест-кейсов |
| `external_id` | нет | идентификатор из внешней TMS или другого источника |
| `title` | да | название тест-кейса |
| `preconditions` | нет | предусловия |
| `steps` | нет | шаги выполнения |
| `expected_result` | нет | ожидаемый результат |
| `tags` | нет | список тегов |
| `priority` | нет | приоритет |
| `raw_text` | нет | готовое текстовое представление; если не передано, сервис соберет его автоматически |

---

## Типовые проблемы

### Контейнер не видит Ollama

Проверка на компьютере:

```powershell
curl.exe http://localhost:11434/api/tags
```

Проверка из контейнера:

```powershell
docker compose --env-file deploy\.env -f deploy\docker-compose.yml exec llm_service curl http://host.docker.internal:11434/api/tags
```

Если на компьютере работает, а из контейнера нет:

```powershell
setx OLLAMA_HOST "0.0.0.0:11434"
```

После этого перезапустите Ollama.

## Структура проекта

```text
qa-regression-assistant/
├── backend/
│   ├── services/
│   │   ├── user_service/       # пользователи, проекты, запуски анализа
│   │   ├── data_service/       # тест-кейсы, индексирование, поиск
│   │   └── llm_service/        # LLM
│   ├── shared/                 # общие настройки и инфраструктурные модули
│   ├── tests/                  # тесты backend-логики
│   └── requirements.txt
│
├── frontend/
│   ├── src/                    # React-приложение
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── deploy/
│   ├── docker-compose.yml      # локальный запуск всего проекта
│   ├── .env.example            # пример переменных окружения
│   ├── caddy/                  # конфигурация Caddy
│   ├── nginx/                  # конфигурация nginx для frontend
│   └── dockerfiles/            # Dockerfile-ы сервисов
│
└── README.md
```

---