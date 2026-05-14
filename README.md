## Дополнительные репозитории
Добавил дополнительные репозитории для демонстрации своего опыта во фронтенд разработке

### Список контактов
Находится по пути extra/webclient.
Страница для отображения списка контактов.
Использовались redux, daisyUI, tailwindCSS.
Не имеет бэкенда, используется mock api.

### RAG ассистент
Находится по пути extra/tulahack. 
Предоставлена только часть с проектом на NextJS, с которой я непосредственно работал. 
Решение было разработано в рамках хакатона tulahack2026.
Решение представляет собой RAG ассистента для технической поддержки.
Использвались daisyUI, tailwindCSS, clsx. ORM - Drizzle, БД - postgreSQL


## Описание
Это репозиторий с тестовым задание для компании YADRO импульс. 
### Формулировка задачи:
Необходимо разработать сервис для асинхронной отправки уведомлений (email, telegram, sms – заглушки). Результат – публичный репозиторий на GitHub.
Функциональные требования - backend на flask, REST API:
· POST /api/v1/notifications → тело: type, recipient, subject(opt), message, channel_data(opt) → ответ: 201, id, status=queued  
· GET /api/v1/notifications/ → ответ: id, status (pending/sent/failed), error  
· GET /api/v1/notifications?status=&limit=&offset= → список с пагинацией и фильтром (опционально)
Валидация: обязательные поля, корректность email/телефона в зависимости от типа.
При создании уведомления задача помещается в очередь (брокер сообщений).  
Воркер (отдельный процесс) забирает задачу, имитирует отправку (лог), обновляет статус в БД. При ошибке – статус failed с текстом ошибки.
Хранение данных – реляционная БД. Модель: id (UUID), type, recipient, subject, message, status, created_at, updated_at, error_text.
Контейнеризация – сервис, воркер, брокер, БД должны подниматься одной командой. Переменные окружения вынести в .env.example.
Логирование – структурированный вывод в stdout (приём запроса, постановка в очередь, обработка, успех/ошибка).
Тестирование – минимум 3–5 юнит-тестов на ключевую логику (валидация, создание, обновление статуса).
Документация – README.md: запуск, примеры curl-запросов, архитектура.

## Запуск
1. Создать файл .env в корне
2. Скопировать содержимое .env.example в .env
3. Написать docker compose up -d

## Примеры curl запросов
1. Запрос на создание уведомления(Sms)
`curl -X POST http://127.0.0.1:5000/api/v1/notifications -H "Content-Type: application/json" -d "{\"type\": \"sms\", \"recipient\": \"+79001234567\", \"message\": \"Код: 1234\"}"`
2. Запрос на создание уведомления(Email)
`curl -X POST http://127.0.0.1:5000/api/v1/notifications -H "Content-Type: application/json" -d "{\"type\": \"email\", \"recipient\": \"user@mail.com\", \"subject\": \"Инфо\", \"message\": \"Текст письма\"}"`
3. Запрос на создание уведомления(Telegram)
`curl -X POST http://127.0.0.1:5000/api/v1/notifications -H "Content-Type: application/json" -d "{\"type\": \"telegram\", \"recipient\": \"@username\", \"message\": \"Сообщение в бот\"}"`

4. Запрос на получение уведомления по id
`curl -X GET http://127.0.0.1:5000/api/v1/notifications/%id%`

5. Запрос на получение уведомлений с фильтрацией и пагинацией со стандартными параметрами
`curl -X GET http://127.0.0.1:5000/api/v1/notifications`
6. Запрос на получение уведомлений с фильтрацией и пагинацией
`curl -X GET "http://127.0.0.1:5000/api/v1/notifications?status=sent&limit=4&offset=1"`

## Архитектура 
Архитектура представляет собой распределенную систему по паттерну Producer-Consumer

1. Flask приложение. Producer, принимает HTTP запросы клиентов, валидирует данные и создает записи в БД и помещает задачи в очередь.
2. Celery worker. Consumer, ищет задачи в Redis, при получении задачи имитирует отправку уведомления и обновляет запись в БД.
3. PostgreSQL. База данных, используется для хранения данных об уведомлениях.
4. Redis. Используется как очередь задач.

Каждому архитектурному компоненту соответствует свой docker контейнер.

## Используемые технологии:
Flask
SQLAlchemy
Pscycopg
Pytest
Alembic
Celery
Flask-Injector

##  Структура проекта
├── docker-compose.yaml
├── Readme.md
├── app/
│   ├── DTO/
│   │   └── notificationDTO.py
│   ├── migrations/
│   │   ├── versions/
│   │   │   ├── 3394cdfd1fb7_fix.py
│   │   │   └── 48a1a8508b87_notifications_table.py
│   │   ├── env.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── __init__.py
│   ├── tests/
│   │   ├── test_create_notification_api.py
│   │   ├── test_get_notification_api.py
│   │   ├── test_list_notification_api.py
│   │   └── test_validation.py
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── init.py
│   ├── main.py
│   ├── model.py
│   ├── notification_repository.py
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── tasks.py
│   └── validators.py
└── venv/

