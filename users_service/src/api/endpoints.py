from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.users.schemas import UserUpdateSchema, UserSchema
from src.users.service import UserService
from src.users.middleware import get_current_user_id

app = FastAPI(
    title="Users Service",
    description="Сервис для работы с пользователями",
    version="1.0.0"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/users/{user_id}", response_model=UserSchema)
async def get_user_profile(
    user_id: int,
    current_user_id: Optional[int] = Depends(get_current_user_id)
):
    """Получает профиль пользователя"""
    return await UserService.get_user_profile(user_id, current_user_id)


@app.put("/api/v1/users/{user_id}", response_model=UserSchema)
async def update_user_profile(
    user_id: int,
    user_data: UserUpdateSchema,
    current_user_id: int = Depends(get_current_user_id)
):
    """Обновляет профиль пользователя (только свой профиль)"""
    return await UserService.update_profile(user_id, current_user_id, user_data)


@app.get("/api/v1/users/search", response_model=List[UserSchema])
async def search_users(
    q: str,
    limit: int = 20,
    offset: int = 0
):
    """Поиск пользователей"""
    return await UserService.search_users(q, limit, offset)


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "service": "users-service"}

