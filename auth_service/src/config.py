import os

class Settings:
    # JWT настройки
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    
    # URL других микросервисов
    AUTH_DB_API_URL = os.getenv("AUTH_DB_API_URL", "http://auth_db_api:8000")
    USERS_DB_API_URL = os.getenv("USERS_DB_API_URL", "http://users_db_api:8000")
    
    # Настройки для работы с паролями
    PASSWORD_HASH_ALGORITHM = "bcrypt"
