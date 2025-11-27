from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class RegisterSchema(BaseModel):
    """Schema for registering a new user"""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password (minimum 8 characters)")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Ensure username only contains letters, digits, hyphens, or underscores"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username may only contain letters, digits, hyphens, and underscores')
        return v


class LoginSchema(BaseModel):
    """Schema for user login (email or username)"""
    login: str = Field(..., description="Email or username")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    """Response schema with access credentials"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class RefreshTokenSchema(BaseModel):
    """Schema for refreshing tokens"""
    refresh_token: str = Field(..., description="Refresh token to exchange")


class UserInfo(BaseModel):
    """User information extracted from a token"""
    user_id: int
    username: str
    email: str
    is_admin: bool = False
    is_verified: bool = False

