import hashlib
from datetime import datetime, timezone
from typing import Optional, Tuple
from fastapi import HTTPException, status
from src.authenticator.schemas import RegisterSchema, LoginSchema, TokenResponse, UserInfo
from src.authenticator.jwt_service import JWTService
from src.authenticator.password_service import PasswordService
from src.authenticator.http_clients import UsersDBClient, AuthDBClient


class AuthService:
    """Primary authentication service"""
    
    @staticmethod
    def _hash_refresh_token(token: str) -> str:
        """
        Creates a hash from a refresh token for safe storage
        
        Args:
            token: Refresh token
        
        Returns:
            SHA256 hash of the token
        """
        return hashlib.sha256(token.encode()).hexdigest()
    
    @staticmethod
    async def register(user_data: RegisterSchema, ip_address: str | None = None, 
                      user_agent: str | None = None) -> TokenResponse:
        """
        Registers a new user and returns tokens
        
        Args:
            user_data: Registration payload (username, email, password)
            ip_address: Client IP address
            user_agent: Browser User-Agent
        
        Returns:
            TokenResponse with access and refresh tokens
        
        Raises:
            HTTPException: If the user already exists
        """
        # Ensure there is no existing user with this email
        existing_user_by_email = await UsersDBClient.get_user_by_email(user_data.email)
        if existing_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )
        
        # Ensure the username is unique
        existing_user_by_username = await UsersDBClient.get_user_by_username(user_data.username)
        if existing_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists"
            )
        
        # Hash the password
        password_hash = PasswordService.hash_password(user_data.password)
        
        # Create a user in the database
        user_dict = {
            "username": user_data.username,
            "email": user_data.email,
            "password_hash": password_hash,  # This field has to exist in the Users model
            "created_at": datetime.now(timezone.utc).isoformat(),
            "is_verified": False,
            "is_admin": False
        }
        
        try:
            result = await UsersDBClient.create_user(user_dict)
            # Fetch the newly created user by email to get its ID
            new_user = await UsersDBClient.get_user_by_email(user_data.email)
            if not new_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error while creating user"
                )
            
            user_id = new_user["id"]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error while creating user: {str(e)}"
            )
        
        # Issue tokens
        token_data = {
            "user_id": user_id,
            "username": user_data.username,
            "email": user_data.email,
            "is_admin": False,
            "is_verified": False
        }
        
        access_token = JWTService.create_access_token(token_data)
        refresh_token = JWTService.create_refresh_token(token_data)
        
        # Persist the refresh token in the database
        refresh_token_hash = AuthService._hash_refresh_token(refresh_token)
        token_db_data = {
            "user_id": user_id,
            "refresh_token_hash": refresh_token_hash,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "is_reboked": False
        }
        
        try:
            await AuthDBClient.create_token(token_db_data)
        except Exception as e:
            # Not critical if saving fails, but log it
            print(f"Warning: Failed to save refresh token: {str(e)}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    @staticmethod
    async def login(login_data: LoginSchema, ip_address: str | None = None,
                   user_agent: str | None = None) -> TokenResponse:
        """
        Authenticates a user and returns tokens
        
        Args:
            login_data: Login payload (email or username, password)
            ip_address: Client IP address
            user_agent: Browser User-Agent
        
        Returns:
            TokenResponse with access and refresh tokens
        
        Raises:
            HTTPException: If credentials are invalid
        """
        # Attempt to find the user by email or username
        user = None
        
        # Determine whether the login is an email (contains @)
        if "@" in login_data.login:
            user = await UsersDBClient.get_user_by_email(login_data.login)
        else:
            user = await UsersDBClient.get_user_by_username(login_data.login)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email/username or password"
            )
        
        # Validate the password
        # IMPORTANT: ensure password_hash exists in the Users model
        # For now, just check for the field
        password_hash = user.get("password_hash")
        if not password_hash:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Password is not set for this user"
            )
        
        if not PasswordService.verify_password(login_data.password, password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email/username or password"
            )
        
        # Issue tokens
        token_data = {
            "user_id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "is_admin": user.get("is_admin", False),
            "is_verified": user.get("is_verified", False)
        }
        
        access_token = JWTService.create_access_token(token_data)
        refresh_token = JWTService.create_refresh_token(token_data)
        
        # Persist the refresh token
        refresh_token_hash = AuthService._hash_refresh_token(refresh_token)
        token_db_data = {
            "user_id": user["id"],
            "refresh_token_hash": refresh_token_hash,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "is_reboked": False
        }
        
        try:
            await AuthDBClient.create_token(token_db_data)
        except Exception as e:
            print(f"Warning: Failed to save refresh token: {str(e)}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    @staticmethod
    async def refresh_token(refresh_token: str) -> TokenResponse:
        """
        Refreshes an access token using a refresh token
        
        Args:
            refresh_token: Refresh token
        
        Returns:
            TokenResponse with new tokens
        
        Raises:
            HTTPException: If the refresh token is invalid
        """
        # Validate the refresh token
        payload = JWTService.verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Ensure the token has not been revoked
        refresh_token_hash = AuthService._hash_refresh_token(refresh_token)
        token_in_db = await AuthDBClient.find_token_by_hash(refresh_token_hash)
        
        if not token_in_db or token_in_db.get("is_reboked", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked"
            )
        
        # Fetch up-to-date user data
        user = await UsersDBClient.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Issue new tokens
        token_data = {
            "user_id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "is_admin": user.get("is_admin", False),
            "is_verified": user.get("is_verified", False)
        }
        
        access_token = JWTService.create_access_token(token_data)
        new_refresh_token = JWTService.create_refresh_token(token_data)
        
        # Persist the new refresh token
        new_refresh_token_hash = AuthService._hash_refresh_token(new_refresh_token)
        token_db_data = {
            "user_id": user["id"],
            "refresh_token_hash": new_refresh_token_hash,
            "ip_address": token_in_db.get("ip_address"),
            "user_agent": token_in_db.get("user_agent"),
            "is_reboked": False
        }
        
        try:
            await AuthDBClient.create_token(token_db_data)
            # Revoke the previous token
            await AuthDBClient.revoke_token(token_in_db["id"])
        except Exception as e:
            print(f"Warning: Failed to update refresh token: {str(e)}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    
    @staticmethod
    async def logout(refresh_token: str) -> bool:
        """
        Logs a user out (revokes the refresh token)
        
        Args:
            refresh_token: Refresh token to revoke
        
        Returns:
            True if successful
        """
        refresh_token_hash = AuthService._hash_refresh_token(refresh_token)
        token_in_db = await AuthDBClient.find_token_by_hash(refresh_token_hash)
        
        if token_in_db:
            await AuthDBClient.revoke_token(token_in_db["id"])
        
        return True
    
    @staticmethod
    def verify_access_token(token: str) -> Optional[UserInfo]:
        """
        Validates an access token and returns user info
        
        Args:
            token: Access token
        
        Returns:
            UserInfo or None if the token is invalid
        """
        payload = JWTService.verify_token(token, token_type="access")
        if not payload:
            return None
        
        return UserInfo(
            user_id=payload.get("user_id"),
            username=payload.get("username"),
            email=payload.get("email"),
            is_admin=payload.get("is_admin", False),
            is_verified=payload.get("is_verified", False)
        )

