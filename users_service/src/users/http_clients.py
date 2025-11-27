import httpx
from typing import Optional, Dict, Any, List
from src.config import Settings


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

    @staticmethod
    async def update_user(user_id: int, user_data: Dict[str, Any]) -> bool:
        """Updates user data"""
        # users_db_api does not expose a PUT endpoint yet
        # Need to add it later
        return False

    @staticmethod
    async def search_users(
        query: str, limit: int = 20, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Searches users by username or email"""
        async with httpx.AsyncClient() as client:
            try:
                # Search by username
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
