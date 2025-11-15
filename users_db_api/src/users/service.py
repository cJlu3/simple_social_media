from datetime import datetime
from typing import List
from src.users.repository import UsersRepository
from src.users.schemas import UserSchema

class UserService:
    @classmethod
    async def add (cls, new_user: UserSchema):
        user_dict = new_user.to_dict()
        await UsersRepository.add(user_dict)

    @classmethod
    async def get(cls, user_id: int):
        user = await UsersRepository.get(user_id)
        res = UserSchema.model_validate(user, from_attributes=True)
        return res

    @classmethod
    async def list(
        cls,
        username: str | None = None,
        email: str | None = None,
        avatar_url: str | None = None,
        created_at: datetime | None = None,
        disactivated_at: datetime | None = None,
        birth_date: datetime | None = None,
        is_verified: bool | None = None,
        is_admin: bool | None = None,
        limit: int | None = 5,
        offset: int | None = 0,

    ):
        filter = {
            k: v
            for k, v in {
                "username": username,
                "email": email,
                "avatar_url": avatar_url,
                "created_at": created_at,
                "disactivated_at": disactivated_at,
                "birth_date": birth_date,
                "is_verified": is_verified,
                "is_admin": is_admin,
            }.items()
            if v is not None
        }
        lst = await UsersRepository.list(filter, limit=limit, offset=offset)
        res = []
        for item in lst:
            user = UserSchema.model_validate(item, from_attributes=True)
            res.append(user)
        return res

    @classmethod
    async def count(cls):
        res = await UsersRepository.count()
        return res

    @classmethod
    async def delete(cls, user_id):
        await UsersRepository.delete(user_id)

    @classmethod
    async def delete_all(cls):
        await UsersRepository.delete_all()
