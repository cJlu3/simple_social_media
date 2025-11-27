from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserUpdateSchema(BaseModel):
    """Schema for updating a user profile"""

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    avatar_url: str | None = None
    birth_date: datetime | None = None


class UserSchema(BaseModel):
    """User schema for responses"""

    id: int
    username: str
    avatar_url: str | None = None
    email: str
    created_at: datetime
    disactivated_at: datetime | None = None
    birth_date: datetime | None = None
    is_verified: bool
    is_admin: bool
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    is_following: bool = False


class FollowSchema(BaseModel):
    """Follow schema"""

    follower_id: int
    following_id: int
    created_at: datetime
