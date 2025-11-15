from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class RegisterSchema(BaseModel):
    """Схема для регистрации нового пользователя"""
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email адрес")
    password: str = Field(..., min_length=8, max_length=100, description="Пароль (минимум 8 символов)")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Проверка, что username содержит только буквы, цифры и подчеркивания"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username может содержать только буквы, цифры, дефисы и подчеркивания')
        return v


class LoginSchema(BaseModel):
    """Схема для входа пользователя (можно использовать email или username)"""
    login: str = Field(..., description="Email или username")
    password: str = Field(..., description="Пароль")


class TokenResponse(BaseModel):
    """Схема ответа с токенами доступа"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Тип токена")


class RefreshTokenSchema(BaseModel):
    """Схема для обновления токена"""
    refresh_token: str = Field(..., description="Refresh token для обновления")


class UserInfo(BaseModel):
    """Информация о пользователе из токена"""
    user_id: int
    username: str
    email: str
    is_admin: bool = False
    is_verified: bool = False

