from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from src.config import Settings


class JWTService:
    """Service for working with JWT tokens"""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
        """
        Creates a JWT access token
        
        Args:
            data: Data to embed in the token (user_id, username, email, etc.)
            expires_delta: Token lifetime. Defaults to the settings value.
        
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """
        Creates a JWT refresh token with a longer lifetime
        
        Args:
            data: Data to embed in the token
        
        Returns:
            Encoded JWT refresh token
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=Settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """
        Verifies and decodes a JWT token
        
        Args:
            token: JWT token to verify
            token_type: Token type ("access" or "refresh")
        
        Returns:
            Decoded payload or None if the token is invalid
        """
        try:
            payload = jwt.decode(token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM])
            
            # Ensure token type matches
            if payload.get("type") != token_type:
                return None
            
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def get_user_id_from_token(token: str) -> Optional[int]:
        """
        Extracts user_id from a token
        
        Args:
            token: JWT token
        
        Returns:
            user_id or None if the token is invalid
        """
        payload = JWTService.verify_token(token)
        if payload:
            return payload.get("user_id")
        return None

