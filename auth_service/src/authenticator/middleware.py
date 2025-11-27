from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.authenticator.service import AuthService
from src.authenticator.schemas import UserInfo


# Create an HTTPBearer instance to extract tokens from the Authorization header
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = None
) -> UserInfo:
    """
    Dependency that returns the currently authenticated user.

    Used in endpoints that require authentication. Extracts the token from
    the Authorization header and validates it.

    Args:
        request: FastAPI Request object
        credentials: Automatically extracted credentials from HTTPBearer

    Returns:
        UserInfo with user data

    Raises:
        HTTPException: If the token is missing or invalid
    """
    # Try to read the token from HTTPBearer
    token = None
    if credentials:
        token = credentials.credentials
    else:
        # If HTTPBearer failed, parse the header manually
        authorization = request.headers.get("Authorization")
        if authorization:
            try:
                scheme, token = authorization.split()
                if scheme.lower() != "bearer":
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication scheme",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Authorization header format",
                    headers={"WWW-Authenticate": "Bearer"},
                )
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Validate the token
    user_info = AuthService.verify_access_token(token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_info


async def get_current_user_optional(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = None
) -> Optional[UserInfo]:
    """
    Dependency that returns the current user when available.

    Useful for endpoints where authentication is optional but user data is
    desirable if present.

    Args:
        request: FastAPI Request object
        credentials: Automatically extracted credentials from HTTPBearer

    Returns:
        UserInfo or None if the user is not authenticated
    """
    try:
        return await get_current_user(request, credentials)
    except HTTPException:
        return None

