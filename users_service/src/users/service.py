from typing import Optional, List
from fastapi import HTTPException, status
from src.users.schemas import UserUpdateSchema, UserSchema
from src.users.http_clients import UsersDBClient


class UserService:
    """Service for working with users"""
    
    @staticmethod
    async def get_user_profile(user_id: int, current_user_id: int | None = None) -> UserSchema:
        """Retrieves a user profile"""
        user = await UsersDBClient.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check whether the current user is following the profile owner
        is_following = False
        # TODO: Implement follow check via the Follows model
        
        return UserSchema(
            id=user["id"],
            username=user["username"],
            avatar_url=user.get("avatar_url"),
            email=user["email"],
            created_at=user["created_at"],
            disactivated_at=user.get("disactivated_at"),
            birth_date=user.get("birth_date"),
            is_verified=user.get("is_verified", False),
            is_admin=user.get("is_admin", False),
            is_following=is_following
        )
    
    @staticmethod
    async def update_profile(user_id: int, current_user_id: int, user_data: UserUpdateSchema) -> UserSchema:
        """Updates a user profile (only their own profile)"""
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to edit this profile"
            )
        
        # Profile update (need to add a method in UsersDBClient)
        # For now, return the existing profile
        return await UserService.get_user_profile(user_id, current_user_id)
    
    @staticmethod
    async def search_users(query: str, limit: int = 20, offset: int = 0) -> List[UserSchema]:
        """Searches users"""
        users = await UsersDBClient.search_users(query, limit, offset)
        result = []
        for user in users:
            result.append(UserSchema(
                id=user["id"],
                username=user["username"],
                avatar_url=user.get("avatar_url"),
                email=user["email"],
                created_at=user["created_at"],
                disactivated_at=user.get("disactivated_at"),
                birth_date=user.get("birth_date"),
                is_verified=user.get("is_verified", False),
                is_admin=user.get("is_admin", False)
            ))
        return result

