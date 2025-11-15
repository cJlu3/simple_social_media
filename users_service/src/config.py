import os


class Settings:
    # URL других микросервисов
    USERS_DB_API_URL = os.getenv("USERS_DB_API_URL", "http://users_db_api:8000")

    # JWT настройки для проверки токенов
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
