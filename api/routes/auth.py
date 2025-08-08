"""
API роуты для аутентификации и авторизации
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from typing import Dict, Any
from datetime import datetime

from api.models.responses import APIResponse, Token, User, LoginRequest
from api.auth.security import (
    authenticate_user, create_user_tokens, refresh_access_token,
    revoke_refresh_token, get_current_user
)
from api.monitoring.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()
security = HTTPBearer()


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """
    Авторизация пользователя
    
    Возвращает JWT access token и refresh token
    """
    try:
        # Аутентифицируем пользователя через PostgreSQL
        user_model = await authenticate_user(login_data.username, login_data.password)
        
        if not user_model:
            logger.warning(f"Failed login attempt for user: {login_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        # Создаем токены с сохранением в Redis
        tokens = await create_user_tokens(user_model)
        
        logger.info(f"User logged in successfully: {login_data.username}")
        
        return tokens
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=Dict[str, str])
async def refresh_token(refresh_data: Dict[str, str]):
    """
    Обновление access token с использованием refresh token
    """
    try:
        refresh_token = refresh_data.get("refresh_token")
        
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is required"
            )
        
        # Получаем новый access токен через Redis и PostgreSQL
        new_access_token = await refresh_access_token(refresh_token)
        
        if not new_access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        logger.debug("Access token refreshed successfully")
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout(
    logout_data: Dict[str, str],
    current_user: User = Depends(get_current_user)
):
    """
    Выход пользователя (отзыв refresh token)
    """
    try:
        refresh_token = logout_data.get("refresh_token")
        
        if refresh_token:
            revoked = await revoke_refresh_token(refresh_token)
            if revoked:
                logger.info(f"User logged out successfully: {current_user.username}")
            else:
                logger.warning(f"Logout attempt with invalid refresh token: {current_user.username}")
        
        return APIResponse(
            status="success",
            message="Logout successful"
        )
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Получить информацию о текущем пользователе
    """
    return current_user


@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_user)):
    """
    Проверить валидность токена
    """
    return APIResponse(
        status="success",
        message="Token is valid",
        data={
            "user_id": current_user.user_id,
            "username": current_user.username,
            "role": current_user.role,
            "is_active": current_user.is_active
        }
    )


@router.get("/health")
async def auth_health_check():
    """
    Health check для authentication системы
    Проверяет PostgreSQL и Redis connectivity
    """
    try:
        from api.database.connection import get_db_connection
        from api.database.redis_client import get_token_manager
        from sqlalchemy import select, func
        from api.database.models import User as UserModel
        
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        # Проверяем PostgreSQL
        try:
            async with get_db_connection() as db:
                users_count = await db.execute(select(func.count(UserModel.id)))
                total_users = users_count.scalar()
                
                active_users = await db.execute(
                    select(func.count(UserModel.id))
                    .where(UserModel.is_active == True)
                )
                
                health_status["components"]["postgresql"] = {
                    "status": "healthy",
                    "total_users": total_users,
                    "active_users": active_users.scalar()
                }
        except Exception as e:
            health_status["components"]["postgresql"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "degraded"
        
        # Проверяем Redis
        try:
            token_manager = await get_token_manager()
            redis_info = await token_manager.health_check()
            health_status["components"]["redis"] = {
                "status": "healthy",
                "info": redis_info
            }
        except Exception as e:
            health_status["components"]["redis"] = {
                "status": "unhealthy", 
                "error": str(e)
            }
            health_status["status"] = "degraded"
        
        # Общий статус
        if all(comp.get("status") == "healthy" for comp in health_status["components"].values()):
            health_status["status"] = "healthy"
        elif any(comp.get("status") == "unhealthy" for comp in health_status["components"].values()):
            health_status["status"] = "unhealthy"
        
        return health_status
        
    except Exception as e:
        logger.error(f"Auth health check error: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }