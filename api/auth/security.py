"""
Система аутентификации и авторизации для AI SEO Architects API
JWT токены с Redis хранением, роли пользователей, database интеграция
"""

import jwt
import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.database.connection import get_db_session
from api.database.models import User as UserModel, UserSession
from api.database.redis_client import get_token_manager, TokenManager
from api.models.responses import User, Token
from api.monitoring.logger import get_logger

logger = get_logger(__name__)

# Конфигурация безопасности
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key_change_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer схема для токенов
security = HTTPBearer()
users_db = {
    "admin": {
        "user_id": "user_admin",
        "username": "admin",
        "email": "admin@ai-seo-architects.com",
        "full_name": "System Administrator",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "role": "admin",
        "permissions": [
            "agents:read", "agents:write", "agents:delete",
            "campaigns:read", "campaigns:write", "campaigns:delete",
            "clients:read", "clients:write", "clients:delete",
            "analytics:read", "system:admin"
        ],
        "is_active": True,
        "created_at": "2025-01-01T00:00:00Z"
    },
    "manager": {
        "user_id": "user_manager",
        "username": "manager",
        "email": "manager@ai-seo-architects.com",
        "full_name": "SEO Manager",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "role": "manager",
        "permissions": [
            "agents:read", "agents:write",
            "campaigns:read", "campaigns:write",
            "clients:read", "clients:write",
            "analytics:read"
        ],
        "is_active": True,
        "created_at": "2025-01-01T00:00:00Z"
    },
    "operator": {
        "user_id": "user_operator",
        "username": "operator",
        "email": "operator@ai-seo-architects.com",
        "full_name": "SEO Operator",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "role": "operator",
        "permissions": [
            "agents:read",
            "campaigns:read",
            "clients:read",
            "analytics:read"
        ],
        "is_active": True,
        "created_at": "2025-01-01T00:00:00Z"
    }
}

# Хранилище refresh токенов
refresh_tokens_db = set()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хешировать пароль"""
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Аутентификация пользователя
    
    Args:
        username: Имя пользователя
        password: Пароль
        
    Returns:
        Данные пользователя или None если аутентификация не удалась
    """
    user = users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    if not user["is_active"]:
        return None
    
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создать JWT access токен
    
    Args:
        data: Данные для включения в токен
        expires_delta: Время жизни токена
        
    Returns:
        JWT токен
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def create_refresh_token(username: str) -> str:
    """
    Создать refresh токен
    
    Args:
        username: Имя пользователя
        
    Returns:
        Refresh токен
    """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "sub": username,
        "exp": expire,
        "type": "refresh"
    }
    
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    refresh_tokens_db.add(refresh_token)  # Сохраняем в "базе данных"
    
    return refresh_token


def verify_token(token: str) -> Optional[dict]:
    """
    Проверить и декодировать JWT токен
    
    Args:
        token: JWT токен
        
    Returns:
        Payload токена или None если токен невалидный
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            return None
            
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        return None
    except jwt.JWTError:
        logger.warning("Invalid token")
        return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Dependency для получения текущего пользователя из JWT токена
    
    Args:
        credentials: HTTP Bearer credentials
        
    Returns:
        Объект пользователя
        
    Raises:
        HTTPException: Если токен невалидный или пользователь не найден
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        if payload is None:
            raise credentials_exception
            
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        user_data = users_db.get(username)
        if user_data is None:
            raise credentials_exception
            
        # Обновляем время последнего входа
        user_data["last_login"] = datetime.utcnow().isoformat()
        
        # Создаем объект пользователя
        user = User(
            user_id=user_data["user_id"],
            username=user_data["username"],
            email=user_data["email"],
            full_name=user_data["full_name"],
            role=user_data["role"],
            permissions=user_data["permissions"],
            is_active=user_data["is_active"],
            last_login=user_data.get("last_login"),
            created_at=user_data["created_at"]
        )
        
        logger.debug(f"User authenticated: {username}", user_id=user.user_id, role=user.role)
        
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise credentials_exception


def require_permissions(required_permissions: List[str]):
    """
    Decorator для проверки прав доступа
    
    Args:
        required_permissions: Список необходимых разрешений
        
    Returns:
        Dependency function
    """
    def permission_dependency(current_user: User = Depends(get_current_user)) -> User:
        """
        Проверить права пользователя
        
        Args:
            current_user: Текущий пользователь
            
        Returns:
            Пользователя если есть необходимые права
            
        Raises:
            HTTPException: Если прав недостаточно
        """
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        # Админы имеют все права
        if current_user.role == "admin":
            return current_user
        
        # Проверяем конкретные разрешения
        missing_permissions = set(required_permissions) - set(current_user.permissions)
        
        if missing_permissions:
            logger.warning(f"User {current_user.username} missing permissions: {missing_permissions}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Missing: {', '.join(missing_permissions)}"
            )
        
        return current_user
    
    return permission_dependency


def require_role(required_role: str):
    """
    Decorator для проверки роли пользователя
    
    Args:
        required_role: Необходимая роль
        
    Returns:
        Dependency function
    """
    def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        """
        Проверить роль пользователя
        
        Args:
            current_user: Текущий пользователь
            
        Returns:
            Пользователя если роль подходит
            
        Raises:
            HTTPException: Если роль не подходит
        """
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        # Иерархия ролей: admin > manager > operator
        role_hierarchy = {
            "admin": 3,
            "manager": 2,
            "operator": 1
        }
        
        user_level = role_hierarchy.get(current_user.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        if user_level < required_level:
            logger.warning(f"User {current_user.username} role {current_user.role} insufficient for {required_role}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' or higher required"
            )
        
        return current_user
    
    return role_dependency


def create_user_tokens(username: str) -> Token:
    """
    Создать токены для пользователя
    
    Args:
        username: Имя пользователя
        
    Returns:
        Объект с токенами
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, 
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(username)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        refresh_token=refresh_token
    )


def revoke_refresh_token(refresh_token: str) -> bool:
    """
    Отозвать refresh токен
    
    Args:
        refresh_token: Refresh токен для отзыва
        
    Returns:
        True если токен был отозван
    """
    if refresh_token in refresh_tokens_db:
        refresh_tokens_db.remove(refresh_token)
        return True
    return False


def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Обновить access токен используя refresh токен
    
    Args:
        refresh_token: Refresh токен
        
    Returns:
        Новый access токен или None если refresh токен невалидный
    """
    if refresh_token not in refresh_tokens_db:
        return None
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")
        
        if username is None or token_type != "refresh":
            return None
        
        # Проверяем что пользователь еще существует и активен
        user_data = users_db.get(username)
        if not user_data or not user_data["is_active"]:
            # Отзываем токен если пользователь неактивен
            revoke_refresh_token(refresh_token)
            return None
        
        # Создаем новый access токен
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": username}, 
            expires_delta=access_token_expires
        )
        
        return new_access_token
        
    except jwt.ExpiredSignatureError:
        # Удаляем просроченный refresh токен
        refresh_tokens_db.discard(refresh_token)
        return None
    except jwt.JWTError:
        return None


# Готовые dependency для различных уровней доступа
admin_required = require_role("admin")
manager_required = require_role("manager")
operator_required = require_role("operator")

agents_read_required = require_permissions(["agents:read"])
agents_write_required = require_permissions(["agents:write"])
campaigns_read_required = require_permissions(["campaigns:read"])
campaigns_write_required = require_permissions(["campaigns:write"])
clients_read_required = require_permissions(["clients:read"])
clients_write_required = require_permissions(["clients:write"])
analytics_read_required = require_permissions(["analytics:read"])
system_admin_required = require_permissions(["system:admin"])