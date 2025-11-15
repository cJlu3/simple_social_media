from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.authenticator.service import AuthService
from src.authenticator.schemas import UserInfo


# Создаем экземпляр HTTPBearer для извлечения токена из заголовка Authorization
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = None
) -> UserInfo:
    """
    Dependency для получения текущего аутентифицированного пользователя
    
    Используется в эндпоинтах, которые требуют аутентификации.
    Извлекает токен из заголовка Authorization и проверяет его.
    
    Args:
        request: FastAPI Request объект
        credentials: Автоматически извлеченные credentials из HTTPBearer
    
    Returns:
        UserInfo с данными пользователя
    
    Raises:
        HTTPException: Если токен отсутствует или невалиден
    """
    # Пытаемся получить токен из HTTPBearer
    token = None
    if credentials:
        token = credentials.credentials
    else:
        # Если HTTPBearer не сработал, пытаемся получить из заголовка напрямую
        authorization = request.headers.get("Authorization")
        if authorization:
            try:
                scheme, token = authorization.split()
                if scheme.lower() != "bearer":
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Неверная схема аутентификации",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный формат заголовка Authorization",
                    headers={"WWW-Authenticate": "Bearer"},
                )
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен доступа не предоставлен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Проверяем токен
    user_info = AuthService.verify_access_token(token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или истекший токен доступа",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_info


async def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = None
) -> Optional[UserInfo]:
    """
    Dependency для получения текущего пользователя (опционально)
    
    Используется в эндпоинтах, где аутентификация не обязательна,
    но если пользователь аутентифицирован, мы можем использовать его данные.
    
    Args:
        request: FastAPI Request объект
        credentials: Автоматически извлеченные credentials из HTTPBearer
    
    Returns:
        UserInfo или None, если пользователь не аутентифицирован
    """
    try:
        return await get_current_user(request, credentials)
    except HTTPException:
        return None

