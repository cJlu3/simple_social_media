import os


class Settings:
    # URLs of other microservices
    POSTS_DB_API_URL = os.getenv("POSTS_DB_API_URL", "http://posts_db_api:8000")
    USERS_DB_API_URL = os.getenv("USERS_DB_API_URL", "http://users_db_api:8000")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8000")

    # JWT settings for token validation
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
