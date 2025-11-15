import httpx
from typing import Optional, Dict, Any, List
from src.config import Settings


class PostsDBClient:
    """HTTP клиент для работы с posts_db_api"""

    BASE_URL = Settings.POSTS_DB_API_URL

    @staticmethod
    async def create_post(post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создает новый пост"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PostsDBClient.BASE_URL}/api/v1/posts", json=post_data, timeout=10.0
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_post(post_id: int) -> Optional[Dict[str, Any]]:
        """Получает пост по ID"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{PostsDBClient.BASE_URL}/api/v1/posts/{post_id}", timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data") if data.get("success") else None
            except httpx.HTTPStatusError:
                return None

    @staticmethod
    async def get_posts(
        author_id: Optional[int] = None,
        parent_post_id: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Получает список постов с фильтрацией"""
        async with httpx.AsyncClient() as client:
            params = {}
            if author_id:
                params["author_id"] = author_id
            if parent_post_id:
                params["parent_post_id"] = parent_post_id
            if limit:
                params["limit"] = limit
            if offset:
                params["offset"] = offset
            params["is_deleted"] = False
            params["is_visible"] = True

            response = await client.get(
                f"{PostsDBClient.BASE_URL}/api/v1/posts", params=params, timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", []) if data.get("success") else []

    @staticmethod
    async def get_comments(post_id: int) -> List[Dict[str, Any]]:
        """Получает комментарии к посту"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{PostsDBClient.BASE_URL}/api/v1/posts/{post_id}/comments",
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", []) if data.get("success") else []
            except httpx.HTTPStatusError:
                return []

    @staticmethod
    async def delete_post(post_id: int) -> bool:
        """Удаляет пост (помечает как is_deleted=True)"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    f"{PostsDBClient.BASE_URL}/api/v1/posts/{post_id}", timeout=10.0
                )
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError:
                return False


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
