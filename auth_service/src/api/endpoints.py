from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.authenticator.schemas import RegisterSchema, LoginSchema, RefreshTokenSchema, TokenResponse, UserInfo
from src.authenticator.service import AuthService
from src.authenticator.middleware import get_current_user, get_current_user_optional

app = FastAPI(
    title="Auth Service",
    description="Сервис аутентификации для социальной сети",
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


def get_client_ip(request: Request) -> str:
    """Извлекает IP адрес клиента из запроса"""
    # Проверяем заголовки прокси
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Если нет заголовков прокси, используем прямой IP
    if request.client:
        return request.client.host
    
    return "unknown"


def get_user_agent(request: Request) -> str:
    """Извлекает User-Agent из запроса"""
    return request.headers.get("User-Agent", "unknown")


@app.post("/api/v1/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterSchema,
    request: Request
):
    """
    Регистрация нового пользователя
    
    Создает нового пользователя в системе и возвращает токены доступа.
    Пароль хешируется с использованием bcrypt перед сохранением.
    
    Args:
        user_data: Данные для регистрации (username, email, password)
        request: FastAPI Request для получения IP и User-Agent
    
    Returns:
        TokenResponse с access и refresh токенами
    
    Raises:
        HTTPException: Если пользователь уже существует
    """
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    try:
        tokens = await AuthService.register(user_data, ip_address, user_agent)
        return tokens
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при регистрации: {str(e)}"
        )


@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(
    login_data: LoginSchema,
    request: Request
):
    """
    Вход пользователя в систему
    
    Проверяет учетные данные пользователя и возвращает токены доступа.
    Можно использовать email или username для входа.
    
    Args:
        login_data: Данные для входа (login - email или username, password)
        request: FastAPI Request для получения IP и User-Agent
    
    Returns:
        TokenResponse с access и refresh токенами
    
    Raises:
        HTTPException: Если неверные учетные данные
    """
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    try:
        tokens = await AuthService.login(login_data, ip_address, user_agent)
        return tokens
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при входе: {str(e)}"
        )


@app.post("/api/v1/auth/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: RefreshTokenSchema
):
    """
    Обновление access token
    
    Использует refresh token для получения новых access и refresh токенов.
    Старый refresh token отзывается.
    
    Args:
        token_data: Refresh token для обновления
    
    Returns:
        TokenResponse с новыми access и refresh токенами
    
    Raises:
        HTTPException: Если refresh token невалиден или отозван
    """
    try:
        tokens = await AuthService.refresh_token(token_data.refresh_token)
        return tokens
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении токена: {str(e)}"
        )


@app.post("/api/v1/auth/logout", status_code=status.HTTP_200_OK)
async def logout(
    token_data: RefreshTokenSchema
):
    """
    Выход пользователя из системы
    
    Отзывает refresh token, делая его недействительным.
    Access token остается валидным до истечения срока действия.
    
    Args:
        token_data: Refresh token для отзыва
    
    Returns:
        Сообщение об успешном выходе
    """
    try:
        await AuthService.logout(token_data.refresh_token)
        return {"success": True, "message": "Выход выполнен успешно"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при выходе: {str(e)}"
        )


@app.get("/api/v1/auth/me")
async def get_current_user_info(
    current_user: UserInfo = Depends(get_current_user)
):
    """
    Получение информации о текущем пользователе
    
    Возвращает информацию о пользователе на основе access token.
    Требует аутентификации.
    
    Args:
        current_user: Текущий пользователь (из middleware)
    
    Returns:
        Информация о пользователе
    """
    return {
        "success": True,
        "data": {
            "user_id": current_user.user_id,
            "username": current_user.username,
            "email": current_user.email,
            "is_admin": current_user.is_admin,
            "is_verified": current_user.is_verified
        }
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "service": "auth-service"}

