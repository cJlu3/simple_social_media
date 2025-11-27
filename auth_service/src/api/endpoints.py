from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.authenticator.schemas import RegisterSchema, LoginSchema, RefreshTokenSchema, TokenResponse, UserInfo
from src.authenticator.service import AuthService
from src.authenticator.middleware import get_current_user, get_current_user_optional

app = FastAPI(
    title="Auth Service",
    description="Authentication service for the social network",
    version="1.0.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify explicit domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_client_ip(request: Request) -> str:
    """Extracts the client's IP address from the request"""
    # Check proxy headers
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to the direct client IP
    if request.client:
        return request.client.host
    
    return "unknown"


def get_user_agent(request: Request) -> str:
    """Extracts the User-Agent from the request"""
    return request.headers.get("User-Agent", "unknown")


@app.post("/api/v1/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterSchema,
    request: Request
):
    """
    Register a new user.

    Creates a user account and returns access credentials.
    The password is hashed with bcrypt before persistence.

    Args:
        user_data: Registration payload (username, email, password)
        request: FastAPI Request to capture IP and User-Agent

    Returns:
        TokenResponse with access and refresh tokens

    Raises:
        HTTPException: If the user already exists
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
            detail=f"Registration error: {str(e)}"
        )


@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(
    login_data: LoginSchema,
    request: Request
):
    """
    User login endpoint.

    Validates credentials and issues tokens.
    Users can provide either email or username.

    Args:
        login_data: Login payload (email/username and password)
        request: FastAPI Request to capture IP and User-Agent

    Returns:
        TokenResponse with access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
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
            detail=f"Login error: {str(e)}"
        )


@app.post("/api/v1/auth/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: RefreshTokenSchema
):
    """
    Refresh an access token.

    Exchanges a refresh token for new access/refresh token pair.
    The old refresh token is revoked.

    Args:
        token_data: Refresh token payload

    Returns:
        TokenResponse containing new tokens

    Raises:
        HTTPException: If the refresh token is invalid or revoked
    """
    try:
        tokens = await AuthService.refresh_token(token_data.refresh_token)
        return tokens
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh error: {str(e)}"
        )


@app.post("/api/v1/auth/logout", status_code=status.HTTP_200_OK)
async def logout(
    token_data: RefreshTokenSchema
):
    """
    Log a user out.

    Revokes the refresh token, rendering it invalid.
    The access token remains valid until expiry.

    Args:
        token_data: Refresh token to revoke

    Returns:
        Success message
    """
    try:
        await AuthService.logout(token_data.refresh_token)
        return {"success": True, "message": "Logout completed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout error: {str(e)}"
        )


@app.get("/api/v1/auth/me")
async def get_current_user_info(
    current_user: UserInfo = Depends(get_current_user)
):
    """
    Retrieve information about the current user.

    Requires authentication via access token.

    Args:
        current_user: UserInfo provided by middleware

    Returns:
        User data payload
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
    """Service health check"""
    return {"status": "healthy", "service": "auth-service"}

