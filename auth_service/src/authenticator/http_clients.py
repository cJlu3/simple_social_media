import httpx
from typing import Optional, Dict, Any, List
from src.config import Settings


class UsersDBClient:
    """HTTP клиент для работы с users_db_api"""

    BASE_URL = Settings.USERS_DB_API_URL

    @staticmethod
    async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создает нового пользователя

        Args:
            user_data: Данные пользователя (username, email, password_hash и т.д.)

        Returns:
            Ответ от API с данными созданного пользователя
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{UsersDBClient.BASE_URL}/api/v1/users", json=user_data, timeout=10.0
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Получает пользователя по ID

        Args:
            user_id: ID пользователя

        Returns:
            Данные пользователя или None, если не найден
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{UsersDBClient.BASE_URL}/api/v1/users/{user_id}", timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data") if data.get("success") else None
            except httpx.HTTPStatusError:
                return None

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Получает пользователя по email

        Args:
            email: Email пользователя

        Returns:
            Данные пользователя или None, если не найден
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{UsersDBClient.BASE_URL}/api/v1/users",
                    params={"email": email, "limit": 1},
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()
                if data.get("success") and data.get("data"):
                    users = data["data"]
                    return users[0] if users else None
                return None
            except httpx.HTTPStatusError:
                return None

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """
        Получает пользователя по username

        Args:
            username: Имя пользователя

        Returns:
            Данные пользователя или None, если не найден
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{UsersDBClient.BASE_URL}/api/v1/users",
                    params={"username": username, "limit": 1},
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()
                if data.get("success") and data.get("data"):
                    users = data["data"]
                    return users[0] if users else None
                return None
            except httpx.HTTPStatusError:
                return None

    @staticmethod
    async def update_user(user_id: int, user_data: Dict[str, Any]) -> bool:
        """
        Обновляет данные пользователя (например, password_hash)

        Args:
            user_id: ID пользователя
            user_data: Новые данные

        Returns:
            True, если обновление успешно
        """
        async with httpx.AsyncClient() as client:
            try:
                # Поскольку в users_db_api нет PUT эндпоинта,
                # мы можем использовать существующие методы или добавить его позже
                # Пока что возвращаем False
                return False
            except httpx.HTTPStatusError:
                return False


class AuthDBClient:
    """HTTP клиент для работы с auth_db_api"""

    BASE_URL = Settings.AUTH_DB_API_URL

    @staticmethod
    async def create_token(token_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Сохраняет refresh token в базе данных

        Args:
            token_data: Данные токена (user_id, refresh_token_hash, ip_address, user_agent)

        Returns:
            Ответ от API
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AuthDBClient.BASE_URL}/api/v1/tokens", json=token_data, timeout=10.0
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_tokens_by_user_id(user_id: int) -> List[Dict[str, Any]]:
        """
        Получает все токены пользователя

        Args:
            user_id: ID пользователя

        Returns:
            Список токенов
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{AuthDBClient.BASE_URL}/api/v1/tokens",
                    params={"user_id": user_id},
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", []) if data.get("success") else []
            except httpx.HTTPStatusError:
                return []

    @staticmethod
    async def revoke_token(token_id: int) -> bool:
        """
        Отзывает токен (помечает как is_reboked=True)

        Args:
            token_id: ID токена

        Returns:
            True, если успешно
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    f"{AuthDBClient.BASE_URL}/api/v1/tokens/{token_id}", timeout=10.0
                )
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError:
                return False

    @staticmethod
    async def find_token_by_hash(refresh_token_hash: str) -> Optional[Dict[str, Any]]:
        """
        Находит токен по хешу refresh token

        Args:
            refresh_token_hash: Хеш refresh token

        Returns:
            Данные токена или None
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{AuthDBClient.BASE_URL}/api/v1/tokens",
                    params={"refresh_token_hash": refresh_token_hash, "limit": 1},
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()
                if data.get("success") and data.get("data"):
                    tokens = data["data"]
                    return tokens[0] if tokens else None
                return None
            except httpx.HTTPStatusError:
                return None
