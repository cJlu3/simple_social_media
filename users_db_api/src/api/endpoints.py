from datetime import datetime
from fastapi import FastAPI
from src.users.schemas import UserSchema
from src.users.service import UserService
from src.api.schemas import ResponseData, ResponseOK

app = FastAPI()


@app.post("/api/v1/users", response_model=ResponseOK)
async def add_user(new_user: UserSchema) -> dict:
    await UserService.add(new_user)
    return {"success": True}

@app.get("/api/v1/users", response_model=ResponseData)
async def get_all_users(
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
) -> dict:
    data = await UserService.list(
        username = username,
        email = email,
        avatar_url = avatar_url,
        created_at = created_at,
        disactivated_at = disactivated_at,
        birth_date = birth_date,
        is_verified = is_verified,
        is_admin = is_admin,
        limit = limit,
        offset = offset
    )
    return {"success": True, "data": data}

@app.get("/api/v1/users/count", response_model=ResponseData)
async def count_all_users() -> dict:
    count = await UserService.count()
    return {"success": True, "data": count}


@app.get("/api/v1/users/{user_id}", response_model=ResponseData)
async def get_users_by_id(user_id: int) -> dict:
    data = await UserService.get(user_id)
    return {"success": True, "data": data}

@app.delete("/api/v1/users", response_model=ResponseOK)
async def delete_all_users() -> dict:
    await UserService.delete_all()
    return {"success": True}

@app.delete("/api/v1/users/{user_id}", response_model=ResponseOK)
async def delete_user_by_id(user_id: int) -> dict:
    await UserService.delete(user_id=user_id)
    return {"success": True}
