import httpx
from typing import Optional, Dict, Any, List
from src.config import Settings


class UsersDBClient:
    """HTTP клиент для работы с users_db_api"""

    BASE_URL = Settings.USERS_DB_API_URL

    @staticmethod
    async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
        """Получает пользователя по ID"""
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
    async def update_user(user_id: int, user_data: Dict[str, Any]) -> bool:
        """Обновляет данные пользователя"""
        # Пока что users_db_api не имеет PUT эндпоинта
        # Нужно будет добавить его позже
        return False

    @staticmethod
    async def search_users(
        query: str, limit: int = 20, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Поиск пользователей по username или email"""
        async with httpx.AsyncClient() as client:
            try:
                # Поиск по username
                response = await client.get(
                    f"{UsersDBClient.BASE_URL}/api/v1/users",
                    params={"username": query, "limit": limit, "offset": offset},
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", []) if data.get("success") else []
            except httpx.HTTPStatusError:
                return []
