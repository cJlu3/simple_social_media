# Simple Social Media (X/Twitter Clone)

Проект представляет собой микросервисную социальную сеть, похожую на X (Twitter).

## Архитектура проекта

Проект использует микросервисную архитектуру:

- **auth_db_api** - API для работы с токенами и аутентификацией
- **posts_db_api** - API для работы с постами
- **users_db_api** - API для работы с пользователями
- **auth_service** - Сервис аутентификации (JWT, регистрация, вход)
- **posts_service** - Бизнес-логика для постов
- **users_service** - Бизнес-логика для пользователей

## План разработки

### ✅ 1. Инфраструктура и база данных

#### ✅ 1.1. Структура проекта

- [x] Создание структуры папок для микросервисов
- [x] Настройка Docker для auth_db_api
- [x] Настройка Docker для posts_db_api
- [x] Настройка Docker для users_db_api
- [x] Настройка Docker для всех сервисов
- [x] Полная настройка docker-compose.yml

#### ✅ 1.2. Модели данных

- [x] Модель Users (id, username, email, avatar_url, created_at, is_verified, is_admin, password_hash)
- [x] Модель Posts (id, author_id, parent_post_id, header, content, tags, media, created_at, is_deleted, is_visible)
- [x] Модель Tokens (id, user_id, refresh_token_hash, issued_at, expires_at, ip_address, user_agent, is_reboked)
- [x] Модель Likes (user_id, post_id)
- [x] Модель Reposts (user_id, post_id)
- [x] Модель Follows (follower_id, following_id)

### ✅ 2. Database APIs (CRUD операции)

#### ✅ 2.1. Auth DB API

- [x] Репозиторий TokensRepository (add, get, list, count, delete, delete_all)
- [x] Сервис TokenService
- [x] Эндпоинты для токенов (POST, GET, DELETE)
- [x] Схемы TokenSchema, TokenCreateSchema

#### ✅ 2.2. Posts DB API

- [x] Репозиторий PostsRepository (add, get, list, count, delete, delete_all, get_comments)
- [x] Сервис PostService
- [x] Эндпоинты для постов (POST, GET, DELETE, GET comments)
- [x] Схемы PostSchema

#### ✅ 2.3. Users DB API

- [x] Репозиторий UsersRepository (add, get, list, count, delete, delete_all)
- [x] Сервис UserService
- [x] Эндпоинты для пользователей (POST, GET, DELETE)
- [x] Схемы UserSchema

### ⏳ 3. Бизнес-логика сервисов

#### ✅ 3.1. Auth Service

- [x] Реализация JWT токенов (access + refresh)
- [x] Хеширование паролей (bcrypt)
- [x] Регистрация пользователя (POST /register)
- [x] Вход пользователя (POST /login)
- [x] Обновление токена (POST /refresh)
- [x] Выход пользователя (POST /logout)
- [x] Валидация токенов
- [x] Middleware для проверки аутентификации
- [x] Интеграция с auth_db_api и users_db_api

#### ✅ 3.2. Posts Service

- [x] Создание поста (POST /posts)
- [x] Получение поста по ID (GET /posts/{id})
- [x] Получение ленты постов (GET /posts)
- [x] Получение постов пользователя (GET /users/{id}/posts)
- [x] Редактирование поста (PUT /posts/{id})
- [x] Удаление поста (DELETE /posts/{id})
- [x] Получение комментариев к посту (GET /posts/{id}/comments)
- [x] Создание комментария (POST /posts/{id}/comments)
- [ ] Лайк поста (POST /posts/{id}/like) - модель создана, API нужно добавить
- [ ] Удаление лайка (DELETE /posts/{id}/like) - модель создана, API нужно добавить
- [ ] Репост (POST /posts/{id}/repost) - модель создана, API нужно добавить
- [ ] Удаление репоста (DELETE /posts/{id}/repost) - модель создана, API нужно добавить
- [ ] Поиск постов (GET /posts/search)
- [x] Интеграция с posts_db_api

#### ✅ 3.3. Users Service

- [x] Получение профиля пользователя (GET /users/{id})
- [x] Обновление профиля (PUT /users/{id})
- [ ] Подписка на пользователя (POST /users/{id}/follow) - модель создана, API нужно добавить
- [ ] Отписка от пользователя (DELETE /users/{id}/follow) - модель создана, API нужно добавить
- [ ] Получение подписчиков (GET /users/{id}/followers) - модель создана, API нужно добавить
- [ ] Получение подписок (GET /users/{id}/following) - модель создана, API нужно добавить
- [x] Поиск пользователей (GET /users/search)
- [x] Интеграция с users_db_api

### ⏳ 4. Взаимодействия (Interactions)

#### ⏳ 4.1. Лайки

- [ ] Модель Likes в базе данных
- [ ] API для лайков в posts_db_api
- [ ] Логика лайков в posts_service
- [ ] Подсчет лайков для постов

#### ⏳ 4.2. Репосты

- [ ] Модель Reposts в базе данных
- [ ] API для репостов в posts_db_api
- [ ] Логика репостов в posts_service
- [ ] Подсчет репостов для постов

#### ⏳ 4.3. Подписки

- [ ] Модель Follows в базе данных
- [ ] API для подписок в users_db_api
- [ ] Логика подписок в users_service
- [ ] Лента постов от подписок

### ✅ 5. Безопасность и валидация

- [x] Валидация входных данных (Pydantic)
- [x] Обработка ошибок (HTTP exceptions)
- [ ] Rate limiting
- [x] CORS настройки
- [x] Валидация email и username
- [x] Проверка прав доступа (только автор может редактировать/удалять пост)
- [x] Защита от SQL injection (использование параметризованных запросов)
- [x] Хеширование паролей
- [x] Безопасное хранение токенов

### ⏳ 6. API Gateway / Frontend

#### ⏳ 6.1. API Gateway (опционально)

- [ ] Настройка API Gateway (Kong, Traefik, или простой FastAPI роутер)
- [ ] Маршрутизация запросов к микросервисам
- [ ] Агрегация данных из нескольких сервисов
- [ ] Единая точка входа для клиентов

#### ⏳ 6.2. Frontend (опционально)

- [ ] Выбор технологии (React, Vue, или простой HTML/JS)
- [ ] Страница регистрации
- [ ] Страница входа
- [ ] Главная страница (лента постов)
- [ ] Страница профиля
- [ ] Страница создания поста
- [ ] Компоненты для лайков, репостов, комментариев

### ⏳ 7. Дополнительные функции

- [ ] Пагинация для всех списков
- [ ] Сортировка постов (по дате, популярности)
- [ ] Фильтрация постов (по тегам, автору)
- [ ] Загрузка медиа файлов (изображения, видео)
- [ ] Уведомления (новые подписчики, лайки, комментарии)
- [ ] Хештеги и поиск по хештегам
- [ ] Упоминания пользователей (@username)
- [ ] Ответы на посты (threads)

### ⏳ 8. Тестирование

- [ ] Unit тесты для репозиториев
- [ ] Unit тесты для сервисов
- [ ] Integration тесты для API
- [ ] Тесты аутентификации
- [ ] Тесты безопасности

### ⏳ 9. Документация

- [ ] README с описанием проекта
- [ ] API документация (Swagger/OpenAPI)
- [ ] Инструкции по запуску
- [ ] Описание архитектуры
- [ ] Примеры использования API

### ✅ 10. DevOps и деплой

- [x] Полная настройка docker-compose.yml
- [x] Переменные окружения (.env файл)
- [x] Health checks для всех сервисов
- [ ] Логирование (базовое)
- [ ] Мониторинг (опционально)
- [ ] CI/CD pipeline (опционально)

## Текущий статус

### Выполнено ✅

- Базовая структура проекта
- Модели данных (Users, Posts, Tokens)
- Репозитории для всех сущностей
- Сервисы для всех сущностей
- API эндпоинты для всех db_apis
- Базовая настройка Docker (частично)

### В процессе ⏳

- Настройка docker-compose.yml
- Реализация бизнес-логики в сервисах

### Не начато ⏳

- Аутентификация (JWT, пароли)
- Взаимодействия (лайки, репосты, подписки)
- Frontend
- Тестирование
- Документация

## Как запустить

### Требования
- Docker и Docker Compose
- Python 3.13+ (для локальной разработки)

### Настройка

1. Создайте файл `.env` в корне проекта (можно скопировать из `.env.example`):
```bash
# Database credentials
DB_USER=postgres
DB_PASSWORD=postgres

# Database names
AUTH_DB_NAME=auth_db
POSTS_DB_NAME=posts_db
USERS_DB_NAME=users_db

# JWT settings
JWT_SECRET_KEY=your-secret-key-change-in-production-minimum-32-characters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
```

2. Запустите все сервисы:
```bash
# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f

# Остановка всех сервисов
docker-compose down
```

### API Endpoints

После запуска доступны следующие сервисы:

**Auth Service (http://localhost:8004)**
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `POST /api/v1/auth/refresh` - Обновление токена
- `POST /api/v1/auth/logout` - Выход
- `GET /api/v1/auth/me` - Информация о текущем пользователе

**Posts Service (http://localhost:8005)**
- `POST /api/v1/posts` - Создание поста
- `GET /api/v1/posts/{id}` - Получение поста
- `GET /api/v1/posts` - Лента постов
- `GET /api/v1/users/{id}/posts` - Посты пользователя
- `PUT /api/v1/posts/{id}` - Обновление поста
- `DELETE /api/v1/posts/{id}` - Удаление поста
- `GET /api/v1/posts/{id}/comments` - Комментарии к посту
- `POST /api/v1/posts/{id}/comments` - Создание комментария

**Users Service (http://localhost:8006)**
- `GET /api/v1/users/{id}` - Профиль пользователя
- `PUT /api/v1/users/{id}` - Обновление профиля
- `GET /api/v1/users/search?q=query` - Поиск пользователей

Все эндпоинты имеют автоматическую документацию Swagger UI:
- http://localhost:8004/docs - Auth Service
- http://localhost:8005/docs - Posts Service
- http://localhost:8006/docs - Users Service

## Порты

- auth_db_api: 8001
- posts_db_api: 8002
- users_db_api: 8003
- auth_service: 8004
- posts_service: 8005
- users_service: 8006

## Технологии

- Python 3.13+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Docker & Docker Compose
- Pydantic (валидация)
