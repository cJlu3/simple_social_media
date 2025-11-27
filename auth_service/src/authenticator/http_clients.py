import httpx
from typing import Optional, Dict, Any, List
from src.config import Settings


class UsersDBClient:
    """HTTP client for interacting with users_db_api"""

    BASE_URL = Settings.USERS_DB_API_URL

    @staticmethod
    async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new user

        Args:
            user_data: User payload (username, email, password_hash, etc.)

        Returns:
            API response containing the created user
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
        Retrieves a user by ID

        Args:
            user_id: User ID

        Returns:
            User data or None if not found
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
        Retrieves a user by email

        Args:
            email: User email

        Returns:
            User data or None if not found
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
        Retrieves a user by username

        Args:
            username: Username

        Returns:
            User data or None if not found
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
        Updates user data (e.g., password_hash)

        Args:
            user_id: User ID
            user_data: New data

        Returns:
            True if the update succeeded
        """
        async with httpx.AsyncClient() as client:
            try:
                # users_db_api has no PUT endpoint yet,
                # so we need to extend the API or reuse existing methods later
                # Returning False for now
                return False
            except httpx.HTTPStatusError:
                return False


class AuthDBClient:
    """HTTP client for interacting with auth_db_api"""

    BASE_URL = Settings.AUTH_DB_API_URL

    @staticmethod
    async def create_token(token_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Persists a refresh token in the database

        Args:
            token_data: Token payload (user_id, refresh_token_hash, ip_address, user_agent)

        Returns:
            API response
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
        Retrieves all tokens for a user

        Args:
            user_id: User ID

        Returns:
            List of token records
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
        Revokes a token (marks it as is_revoked=True)

        Args:
            token_id: Token ID

        Returns:
            True if the operation succeeded
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
        Finds a token by its refresh token hash

        Args:
            refresh_token_hash: Refresh token hash

        Returns:
            Token data or None
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
