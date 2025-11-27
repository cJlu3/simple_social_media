# Simple Social Media (X/Twitter Clone)

This project is a microservice-based social network inspired by X (Twitter).

## Project Architecture

The system is composed of multiple services:

- **auth_db_api** – token storage API (refresh tokens, metadata)
- **posts_db_api** – CRUD API for posts
- **users_db_api** – CRUD API for user profiles
- **auth_service** – authentication service (JWT, registration, login)
- **posts_service** – post-related business logic
- **users_service** – user-related business logic

## Roadmap

### ✅ 1. Infrastructure & Databases

#### ✅ 1.1. Project structure

- [x] Create the microservice folder layout
- [x] Configure Docker for auth_db_api
- [x] Configure Docker for posts_db_api
- [x] Configure Docker for users_db_api
- [x] Provide Dockerfiles for every service
- [x] Fully configure `docker-compose.yml`

#### ✅ 1.2. Data models

- [x] Users model (id, username, email, avatar_url, created_at, is_verified, is_admin, password_hash)
- [x] Posts model (id, author_id, parent_post_id, header, content, tags, media, created_at, is_deleted, is_visible)
- [x] Tokens model (id, user_id, refresh_token_hash, issued_at, expires_at, ip_address, user_agent, is_reboked)
- [x] Likes model (user_id, post_id)
- [x] Reposts model (user_id, post_id)
- [x] Follows model (follower_id, following_id)

### ✅ 2. Database APIs (CRUD)

#### ✅ 2.1. Auth DB API

- [x] TokensRepository (add, get, list, count, delete, delete_all)
- [x] TokenService
- [x] Token endpoints (POST, GET, DELETE)
- [x] TokenSchema & TokenCreateSchema

#### ✅ 2.2. Posts DB API

- [x] PostsRepository (add, get, list, count, delete, delete_all, get_comments)
- [x] PostService
- [x] Post endpoints (POST, GET, DELETE, GET comments)
- [x] PostSchema

#### ✅ 2.3. Users DB API

- [x] UsersRepository (add, get, list, count, delete, delete_all)
- [x] UserService
- [x] User endpoints (POST, GET, DELETE)
- [x] UserSchema

### ⏳ 3. Service Business Logic

#### ✅ 3.1. Auth Service

- [x] JWT tokens (access + refresh)
- [x] Password hashing (bcrypt)
- [x] Registration (POST /register)
- [x] Login (POST /login)
- [x] Token refresh (POST /refresh)
- [x] Logout (POST /logout)
- [x] Token validation
- [x] Authentication middleware
- [x] Integration with auth_db_api & users_db_api

#### ✅ 3.2. Posts Service

- [x] Create post (POST /posts)
- [x] Get post by ID (GET /posts/{id})
- [x] Fetch feed (GET /posts)
- [x] Get posts by user (GET /users/{id}/posts)
- [x] Update post (PUT /posts/{id})
- [x] Delete post (DELETE /posts/{id})
- [x] Fetch comments (GET /posts/{id}/comments)
- [x] Create comment (POST /posts/{id}/comments)
- [ ] Like post (POST /posts/{id}/like) – model exists, API pending
- [ ] Remove like (DELETE /posts/{id}/like) – model exists, API pending
- [ ] Repost (POST /posts/{id}/repost) – model exists, API pending
- [ ] Remove repost (DELETE /posts/{id}/repost) – model exists, API pending
- [ ] Search posts (GET /posts/search)
- [x] Integration with posts_db_api

#### ✅ 3.3. Users Service

- [x] Get user profile (GET /users/{id})
- [x] Update profile (PUT /users/{id})
- [ ] Follow user (POST /users/{id}/follow) – model exists, API pending
- [ ] Unfollow user (DELETE /users/{id}/follow) – model exists, API pending
- [ ] Fetch followers (GET /users/{id}/followers) – model exists, API pending
- [ ] Fetch following (GET /users/{id}/following) – model exists, API pending
- [x] Search users (GET /users/search)
- [x] Integration with users_db_api

### ⏳ 4. Interactions

#### ⏳ 4.1. Likes

- [ ] Database model
- [ ] posts_db_api endpoints
- [ ] posts_service logic
- [ ] Post like counters

#### ⏳ 4.2. Reposts

- [ ] Database model
- [ ] posts_db_api endpoints
- [ ] posts_service logic
- [ ] Post repost counters

#### ⏳ 4.3. Follows

- [ ] Database model
- [ ] users_db_api endpoints
- [ ] users_service logic
- [ ] Feed filtered by follows

### ✅ 5. Security & Validation

- [x] Input validation (Pydantic)
- [x] Error handling (HTTP exceptions)
- [ ] Rate limiting
- [x] CORS configuration
- [x] Email & username validation
- [x] Access checks (only authors can edit/delete posts)
- [x] SQL injection protection (parameterized queries)
- [x] Password hashing
- [x] Secure token storage

### ⏳ 6. API Gateway / Frontend

#### ⏳ 6.1. API Gateway (optional)

- [ ] Configure gateway (Kong, Traefik, or FastAPI router)
- [ ] Route requests to services
- [ ] Aggregate data from multiple services
- [ ] Provide a single entry point

#### ⏳ 6.2. Frontend (optional)

- [ ] Choose technology (React, Vue, or plain HTML/JS)
- [ ] Registration page
- [ ] Login page
- [ ] Home feed
- [ ] Profile page
- [ ] Post composer
- [ ] Components for likes, reposts, comments

### ⏳ 7. Additional Features

- [ ] Pagination for all lists
- [ ] Post sorting (by date, popularity)
- [ ] Post filtering (by tags, author)
- [ ] Media uploads (images, video)
- [ ] Notifications (followers, likes, comments)
- [ ] Hashtags & hashtag search
- [ ] User mentions (@username)
- [ ] Threaded replies

### ⏳ 8. Testing

- [ ] Unit tests for repositories
- [ ] Unit tests for services
- [ ] API integration tests
- [ ] Authentication tests
- [ ] Security tests

### ⏳ 9. Documentation

- [ ] README with project overview
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Runbook / setup guide
- [ ] Architecture description
- [ ] API usage examples

### ✅ 10. DevOps & Deployment

- [x] Complete `docker-compose.yml`
- [x] Environment variables (`.env`)
- [x] Health checks for all services
- [ ] Basic logging
- [ ] Monitoring (optional)
- [ ] CI/CD pipeline (optional)

## Current Status

### Completed ✅

- Base project structure
- Data models (Users, Posts, Tokens)
- Repositories for all entities
- Services for all entities
- API endpoints for every db_api
- Initial Docker setup (partial)

### In progress ⏳

- docker-compose orchestration
- Business logic implementation in services

### Not started ⏳

- Additional auth hardening (JWT, password flows)
- Interaction features (likes, reposts, follows)
- Frontend
- Testing
- Documentation polish

## Getting Started

### Requirements
- Docker & Docker Compose
- Python 3.13+ (for local development)

### Setup

1. Create a `.env` file in the project root (copy from `.env.example` if needed):
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

2. Start every service:
```bash
# Launch stack
docker-compose up -d

# Check status
docker-compose ps

# Tail logs
docker-compose logs -f

# Stop everything
docker-compose down
```

### API Endpoints

Available services after startup:

**Auth Service (http://localhost:8004)**
- `POST /api/v1/auth/register` – register a user
- `POST /api/v1/auth/login` – log in
- `POST /api/v1/auth/refresh` – refresh tokens
- `POST /api/v1/auth/logout` – log out
- `GET /api/v1/auth/me` – current user info

**Posts Service (http://localhost:8005)**
- `POST /api/v1/posts` – create a post
- `GET /api/v1/posts/{id}` – fetch a post
- `GET /api/v1/posts` – get the feed
- `GET /api/v1/users/{id}/posts` – posts by user
- `PUT /api/v1/posts/{id}` – update a post
- `DELETE /api/v1/posts/{id}` – delete a post
- `GET /api/v1/posts/{id}/comments` – fetch comments
- `POST /api/v1/posts/{id}/comments` – create comment

**Users Service (http://localhost:8006)**
- `GET /api/v1/users/{id}` – user profile
- `PUT /api/v1/users/{id}` – update profile
- `GET /api/v1/users/search?q=query` – search users

Swagger UI is available for every service:
- http://localhost:8004/docs – Auth Service
- http://localhost:8005/docs – Posts Service
- http://localhost:8006/docs – Users Service

## Ports

- auth_db_api: 8001
- posts_db_api: 8002
- users_db_api: 8003
- auth_service: 8004
- posts_service: 8005
- users_service: 8006

## Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Docker & Docker Compose
- Pydantic (validation)

## Remote-style training environment

To practice deploying the databases and services onto “separate servers”, spin up the lightweight SSH-ready hosts defined in `docker-compose.remote.yml`.

1. Build and start the hosts:
   ```bash
   docker compose -f docker-compose.remote.yml up -d
   ```
   You will get seven containers:
   - `auth_db_host`, `posts_db_host`, `users_db_host` – empty Debian boxes for database work
   - `auth_service_host`, `posts_service_host`, `users_service_host` – empty Debian boxes intended for the FastAPI services
   - `bastion` – helper box that is connected to the services network

2. Each host exposes SSH on a different local port (2222–2228). Example:
   ```bash
   ssh dev@localhost -p 2226    # connects to auth_service_host
   ```
   Default credentials: `dev` / `dev`. The user has passwordless sudo rights so you can install PostgreSQL, uvicorn, etc. exactly like on a remote VM.

3. Containers start empty. Use the helper scripts under `scripts/` to copy code or database dumps into a host once you decide it is ready:
   ```bash
   # Copy the auth service code into /srv/app/auth_service on auth_service_host (port 2226)
   scripts/push-service.sh ./auth_service 2226 /srv/app

   # Upload a SQL dump to auth_db_host (port 2223) and run it through psql
   scripts/push-sql.sh ./seed.sql 2223 "postgresql://postgres:postgres@localhost:5432/postgres"
   ```

4. Bring databases/services up manually inside the target host (e.g., `sudo apt-get install postgresql`, `python -m venv /srv/app/venv`, `uv run uvicorn src.main:app --host 0.0.0.0 --port 8000`). Because there are no bind mounts, nothing is shared automatically with your local tree—the workflow mimics copying artifacts onto a completely separate server.

5. When you are done experimenting, tear everything down:
   ```bash
   docker compose -f docker-compose.remote.yml down -v
   ```

This remote-style topology keeps the original `docker-compose.yml` (fully managed stack) intact while giving you an isolated lab for learning how to push code and data to independent servers.

### Автоматизация деплоя сервисов

Чтобы не выполнять все шаги вручную, можно воспользоваться скриптом `scripts/deploy-service.sh`. Он заходит на выбранный “сервер”, устанавливает Python-зависимости, синхронизирует исходники и запускает uvicorn в отдельной tmux-сессии.

```bash
# Деплой auth_service на хост, слушающий порт 2226
scripts/deploy-service.sh ./auth_service 2226 /srv/services 8000 ./auth_service/.env

# Проверить логи
ssh dev@localhost -p 2226 'tmux attach -t auth_service'
```

Скрипт:
1. Ставит на удалённую машину `python3-venv`, `pipx`, `tmux`, `uv`.
2. Копирует проект через `rsync` и при необходимости `.env`.
3. Создаёт виртуальное окружение, ставит зависимости через `uv pip install -e .`.
4. Перезапускает сервис в tmux-сессии `<имя_папки>`.

Аналогично можно дописать скрипты для деплоя БД (например, запуск `push-sql.sh`) или вынести всё в Ansible-плейбук, если захочется полноценной оркестрации.
