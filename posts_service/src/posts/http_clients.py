import httpx
from typing import Optional, Dict, Any, List
from src.config import Settings


class PostsDBClient:
    """HTTP client for interacting with posts_db_api"""

    BASE_URL = Settings.POSTS_DB_API_URL

    @staticmethod
    async def create_post(post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new post"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PostsDBClient.BASE_URL}/api/v1/posts", json=post_data, timeout=10.0
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_post(post_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a post by ID"""
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
        author_id: int | None = None,
        parent_post_id: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves a filtered list of posts"""
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
        """Retrieves comments for a post"""
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
        """Deletes a post (marks it as is_deleted=True)"""
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
    """HTTP client for interacting with users_db_api"""

    BASE_URL = Settings.USERS_DB_API_URL

    @staticmethod
    async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a user by ID"""
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
