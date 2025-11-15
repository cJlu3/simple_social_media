from typing import Optional, List
from fastapi import HTTPException, status
from src.users.schemas import UserUpdateSchema, UserSchema
from src.users.http_clients import UsersDBClient


class UserService:
    """Сервис для работы с пользователями"""
    
    @staticmethod
    async def get_user_profile(user_id: int, current_user_id: Optional[int] = None) -> UserSchema:
        """Получает профиль пользователя"""
        user = await UsersDBClient.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        # Проверяем, подписан ли текущий пользователь
        is_following = False
        # TODO: Реализовать проверку подписки через Follows модель
        
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
        """Обновляет профиль пользователя (только свой профиль)"""
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет прав на редактирование этого профиля"
            )
        
        # Обновление профиля (нужно добавить метод в UsersDBClient)
        # Пока что возвращаем существующий профиль
        return await UserService.get_user_profile(user_id, current_user_id)
    
    @staticmethod
    async def search_users(query: str, limit: int = 20, offset: int = 0) -> List[UserSchema]:
        """Поиск пользователей"""
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

