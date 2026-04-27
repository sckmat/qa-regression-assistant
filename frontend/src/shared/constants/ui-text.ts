export const uiText = {
    app: {
        title: 'QA Regression Assistant',
        subtitle: 'Интеллектуальный помощник для формирования регрессионного набора',
    },

    navigation: {
        projects: 'Проекты',
    },

    common: {
        loading: 'Загрузка...',
        retryLater: 'Попробуйте еще раз позже.',
        noDescription: 'Описание пока не указано.',
        createdAt: 'Создан',
        score: 'Оценка',
    },

    projects: {
        title: 'Проекты',
        description: 'Создавай проекты и переходи к анализу изменений.',
        createTitle: 'Создать проект',
        createButton: 'Создать проект',
        creatingButton: 'Создание...',
        listTitle: 'Список проектов',
        emptyTitle: 'Проектов пока нет',
        emptyDescription: 'Создай первый проект, чтобы начать работу.',
        nameLabel: 'Название',
        descriptionLabel: 'Описание',
        namePlaceholder: 'Например, Мобильное банковское приложение',
        descriptionPlaceholder: 'Коротко опиши проект',
    },

    projectDetails: {
        title: 'Проект',
        description: 'Обзор проекта, быстрые действия и последние запуски.',
        latestRunsTitle: 'Последние запуски',
        latestRunsDescription: 'Последние результаты анализа по проекту.',
        noRunsTitle: 'Запусков пока нет',
        noRunsDescription: 'Создай первый запуск, чтобы увидеть результаты анализа.',
        newRunButton: 'Новый запуск',
        testCasesButton: 'Тест-кейсы',
        runsButton: 'Запуски',
        allRunsButton: 'Все запуски',
    },

    runs: {
        title: 'Запуски',
        description: 'История запусков анализа по проекту.',
        noRunsTitle: 'Запусков пока нет',
        noRunsDescription: 'Создай первый запуск, чтобы получить набор кандидатов.',
        newRunButton: 'Новый запуск',
        summaryAvailable: 'Доступно итоговое summary',
    },

    newRun: {
        title: 'Новый запуск анализа',
        description: 'Запусти анализ изменений и получи регрессионный набор тест-кейсов.',
        backButton: 'К списку запусков',
        formTitle: 'Параметры запуска',
        changeSummaryLabel: 'Описание изменений',
        changeSummaryPlaceholder:
            'Например: Изменен экран логина, добавлена валидация email и обработка ошибки 401...',
        candidateLimitLabel: 'Количество кандидатов',
        searchModeLabel: 'Режим анализа',
        submitButton: 'Запустить анализ',
        submittingButton: 'Запуск...',
        modes: {
            lexical: {
                label: 'Лексический',
                description: 'Поиск по словам и совпадающим формулировкам.',
            },
            semantic: {
                label: 'Семантический',
                description: 'Поиск по смысловой близости между изменениями и тест-кейсами.',
            },
            semanticLlm: {
                label: 'Семантический + LLM',
                description: 'Сначала выполняется смысловой поиск, затем модель уточняет результаты и добавляет пояснение.',
            },
        },
    },

    testCases: {
        title: 'Тест-кейсы',
        description: 'Загрузка, просмотр и переиндексация тест-кейсов проекта.',
        backButton: 'К проекту',
        importTitle: 'Импорт тест-кейсов',
        importButton: 'Импортировать файл',
        importingButton: 'Импорт...',
        reindexTitle: 'Переиндексация',
        reindexButton: 'Запустить переиндексацию',
        reindexingButton: 'Переиндексация...',
        listTitle: 'Список тест-кейсов',
        emptyTitle: 'Тест-кейсов пока нет',
        emptyDescription: 'Загрузи JSON-файл, чтобы добавить тест-кейсы в проект.',
        expectedResult: 'Ожидаемый результат',
        tags: 'Теги',
        selectedFilePrefix: 'Выбран файл:',
        importHint: "Поддерживается JSON-файл с корневым полем 'items'.",
        reindexHint:
            'Переиндексация нужна после загрузки или обновления тест-кейсов, чтобы они участвовали в смысловом поиске и анализе с моделью.',
    },

    runDetails: {
        title: 'Результаты запуска',
        description: 'Итоги анализа, список кандидатов и пояснения.',
        backButton: 'К списку запусков',
        changeSummaryLabel: 'Описание изменений',
        resultSummaryLabel: 'Итог анализа',
        candidatesTitle: 'Кандидаты',
        candidatesEmptyTitle: 'Кандидаты не найдены',
        candidatesEmptyDescription: 'Для этого запуска релевантные тест-кейсы не были найдены.',
        matchedTermsLabel: 'Совпавшие термины',
        explanationLabel: 'Пояснение',
        noExplanation: 'Для этого режима пояснение недоступно.',
        noMatchedTerms: 'Совпавшие термины отсутствуют.',
        filtersTitle: 'Фильтрация кандидатов',
        searchByTitle: 'Поиск по названию',
        searchByTitlePlaceholder: 'Например: логин, 401, email',
        sortLabel: 'Сортировка',
        onlyWithExplanation: 'Только с пояснением',
        onlyWithMatchedTerms: 'Только с совпавшими терминами',
        sortOptions: {
            scoreDesc: 'Сначала высокий score',
            scoreAsc: 'Сначала низкий score',
            titleAsc: 'Название А-Я',
            titleDesc: 'Название Я-А',
        },
    },

    toasts: {
        projectCreated: 'Проект успешно создан.',
        fileImported: 'Файл успешно импортирован.',
        reindexCompleted: 'Переиндексация завершена успешно.',
        runStarted: 'Запуск анализа успешно создан.',
    },
} as const