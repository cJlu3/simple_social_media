from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserUpdateSchema(BaseModel):
    """Схема для обновления профиля пользователя"""

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    avatar_url: Optional[str] = None
    birth_date: Optional[datetime] = None


class UserSchema(BaseModel):
    """Схема пользователя для ответа"""

    id: int
    username: str
    avatar_url: Optional[str] = None
    email: str
    created_at: datetime
    disactivated_at: Optional[datetime] = None
    birth_date: Optional[datetime] = None
    is_verified: bool
    is_admin: bool
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    is_following: bool = False


class FollowSchema(BaseModel):
    """Схема подписки"""

    follower_id: int
    following_id: int
    created_at: datetime
