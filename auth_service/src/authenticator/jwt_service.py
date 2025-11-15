from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from src.config import Settings


class JWTService:
    """Сервис для работы с JWT токенами"""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Создает JWT access token
        
        Args:
            data: Данные для включения в токен (обычно user_id, username, email)
            expires_delta: Время жизни токена. Если не указано, используется значение из настроек
        
        Returns:
            Закодированный JWT токен
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
        Создает JWT refresh token с более длительным сроком жизни
        
        Args:
            data: Данные для включения в токен
        
        Returns:
            Закодированный JWT refresh token
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=Settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """
        Проверяет и декодирует JWT токен
        
        Args:
            token: JWT токен для проверки
            token_type: Тип токена ("access" или "refresh")
        
        Returns:
            Декодированные данные токена или None, если токен невалиден
        """
        try:
            payload = jwt.decode(token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM])
            
            # Проверяем тип токена
            if payload.get("type") != token_type:
                return None
            
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def get_user_id_from_token(token: str) -> Optional[int]:
        """
        Извлекает user_id из токена
        
        Args:
            token: JWT токен
        
        Returns:
            user_id или None, если токен невалиден
        """
        payload = JWTService.verify_token(token)
        if payload:
            return payload.get("user_id")
        return None

