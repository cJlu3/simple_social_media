import hashlib
from datetime import datetime, timezone
from typing import Optional, Tuple
from fastapi import HTTPException, status
from src.authenticator.schemas import RegisterSchema, LoginSchema, TokenResponse, UserInfo
from src.authenticator.jwt_service import JWTService
from src.authenticator.password_service import PasswordService
from src.authenticator.http_clients import UsersDBClient, AuthDBClient


class AuthService:
    """Основной сервис аутентификации"""
    
    @staticmethod
    def _hash_refresh_token(token: str) -> str:
        """
        Создает хеш из refresh token для безопасного хранения в БД
        
        Args:
            token: Refresh token
        
        Returns:
            SHA256 хеш токена
        """
        return hashlib.sha256(token.encode()).hexdigest()
    
    @staticmethod
    async def register(user_data: RegisterSchema, ip_address: Optional[str] = None, 
                      user_agent: Optional[str] = None) -> TokenResponse:
        """
        Регистрирует нового пользователя и возвращает токены
        
        Args:
            user_data: Данные для регистрации (username, email, password)
            ip_address: IP адрес клиента
            user_agent: User-Agent браузера
        
        Returns:
            TokenResponse с access и refresh токенами
        
        Raises:
            HTTPException: Если пользователь уже существует
        """
        # Проверяем, не существует ли уже пользователь с таким email
        existing_user_by_email = await UsersDBClient.get_user_by_email(user_data.email)
        if existing_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )
        
        # Проверяем, не существует ли уже пользователь с таким username
        existing_user_by_username = await UsersDBClient.get_user_by_username(user_data.username)
        if existing_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким username уже существует"
            )
        
        # Хешируем пароль
        password_hash = PasswordService.hash_password(user_data.password)
        
        # Создаем пользователя в базе данных
        # ВАЖНО: Нужно добавить поле password_hash в модель Users в users_db_api
        # Пока что создаем пользователя без пароля, пароль нужно будет добавить отдельно
        user_dict = {
            "username": user_data.username,
            "email": user_data.email,
            "password_hash": password_hash,  # Это поле нужно добавить в Users модель
            "created_at": datetime.now(timezone.utc).isoformat(),
            "is_verified": False,
            "is_admin": False
        }
        
        try:
            result = await UsersDBClient.create_user(user_dict)
            # Получаем созданного пользователя по email для получения ID
            new_user = await UsersDBClient.get_user_by_email(user_data.email)
            if not new_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Ошибка при создании пользователя"
                )
            
            user_id = new_user["id"]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при создании пользователя: {str(e)}"
            )
        
        # Создаем токены
        token_data = {
            "user_id": user_id,
            "username": user_data.username,
            "email": user_data.email,
            "is_admin": False,
            "is_verified": False
        }
        
        access_token = JWTService.create_access_token(token_data)
        refresh_token = JWTService.create_refresh_token(token_data)
        
        # Сохраняем refresh token в базе данных
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
            # Если не удалось сохранить токен, это не критично, но логируем
            print(f"Warning: Failed to save refresh token: {str(e)}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    @staticmethod
    async def login(login_data: LoginSchema, ip_address: Optional[str] = None,
                   user_agent: Optional[str] = None) -> TokenResponse:
        """
        Выполняет вход пользователя и возвращает токены
        
        Args:
            login_data: Данные для входа (login - email или username, password)
            ip_address: IP адрес клиента
            user_agent: User-Agent браузера
        
        Returns:
            TokenResponse с access и refresh токенами
        
        Raises:
            HTTPException: Если неверные учетные данные
        """
        # Пытаемся найти пользователя по email или username
        user = None
        
        # Проверяем, является ли login email (содержит @)
        if "@" in login_data.login:
            user = await UsersDBClient.get_user_by_email(login_data.login)
        else:
            user = await UsersDBClient.get_user_by_username(login_data.login)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email/username или пароль"
            )
        
        # Проверяем пароль
        # ВАЖНО: Нужно получить password_hash из модели Users
        # Пока что проверяем наличие поля password_hash
        password_hash = user.get("password_hash")
        if not password_hash:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Пароль не установлен для пользователя"
            )
        
        if not PasswordService.verify_password(login_data.password, password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email/username или пароль"
            )
        
        # Создаем токены
        token_data = {
            "user_id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "is_admin": user.get("is_admin", False),
            "is_verified": user.get("is_verified", False)
        }
        
        access_token = JWTService.create_access_token(token_data)
        refresh_token = JWTService.create_refresh_token(token_data)
        
        # Сохраняем refresh token в базе данных
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
        Обновляет access token используя refresh token
        
        Args:
            refresh_token: Refresh token
        
        Returns:
            TokenResponse с новыми токенами
        
        Raises:
            HTTPException: Если refresh token невалиден
        """
        # Проверяем refresh token
        payload = JWTService.verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный refresh token"
            )
        
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный refresh token"
            )
        
        # Проверяем, не отозван ли токен в базе данных
        refresh_token_hash = AuthService._hash_refresh_token(refresh_token)
        token_in_db = await AuthDBClient.find_token_by_hash(refresh_token_hash)
        
        if not token_in_db or token_in_db.get("is_reboked", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token был отозван"
            )
        
        # Получаем актуальные данные пользователя
        user = await UsersDBClient.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        # Создаем новые токены
        token_data = {
            "user_id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "is_admin": user.get("is_admin", False),
            "is_verified": user.get("is_verified", False)
        }
        
        access_token = JWTService.create_access_token(token_data)
        new_refresh_token = JWTService.create_refresh_token(token_data)
        
        # Сохраняем новый refresh token
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
            # Отзываем старый токен
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
        Выполняет выход пользователя (отзывает refresh token)
        
        Args:
            refresh_token: Refresh token для отзыва
        
        Returns:
            True, если выход успешен
        """
        refresh_token_hash = AuthService._hash_refresh_token(refresh_token)
        token_in_db = await AuthDBClient.find_token_by_hash(refresh_token_hash)
        
        if token_in_db:
            await AuthDBClient.revoke_token(token_in_db["id"])
        
        return True
    
    @staticmethod
    def verify_access_token(token: str) -> Optional[UserInfo]:
        """
        Проверяет access token и возвращает информацию о пользователе
        
        Args:
            token: Access token
        
        Returns:
            UserInfo или None, если токен невалиден
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

