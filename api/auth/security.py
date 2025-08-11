"""
Система аутентификации и авторизации для AI SEO Architects API
JWT токены с Redis хранением, роли пользователей, database интеграция
"""

try:
    import jwt
except ImportError:
    # Пытаемся импортировать из python-jose
    try:
        from jose import jwt
    except ImportError:
        # Fallback mock для тестирования
        class MockJWT:
            @staticmethod
            def encode(payload, key, algorithm="HS256"):
                import base64, json
                return base64.b64encode(json.dumps(payload).encode()).decode()
            
            @staticmethod  
            def decode(token, key, algorithms=None):
                import base64, json
                try:
                    return json.loads(base64.b64decode(token).decode())
                except:
                    raise Exception("Invalid token")
        
        jwt = MockJWT()
import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
try:
    from passlib.context import CryptContext
except ImportError:
    # Fallback для passlib
    import hashlib
    
    class MockCryptContext:
        def __init__(self, schemes=None, deprecated="auto"):
            pass
        
        def hash(self, password: str) -> str:
            """Простое хеширование с солью"""
            salt = "ai_seo_salt"
            return hashlib.sha256((password + salt).encode()).hexdigest()
        
        def verify(self, password: str, hashed: str) -> bool:
            """Проверка пароля"""
            return self.hash(password) == hashed
    
    CryptContext = MockCryptContext
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


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить пароль"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хешировать пароль"""
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str) -> Optional[UserModel]:
    """
    Аутентификация пользователя через PostgreSQL
    
    Args:
        username: Имя пользователя
        password: Пароль
        
    Returns:
        Модель пользователя или None если аутентификация не удалась
    """
    try:
        from api.database.connection import get_db_connection
        
        async with get_db_connection() as db:
            # Поиск пользователя в базе
            result = await db.execute(
                select(UserModel).where(UserModel.username == username)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                logger.debug(f"Пользователь не найден: {username}")
                return None
                
            # Проверяем пароль
            if not verify_password(password, user.password_hash):
                logger.debug(f"Неверный пароль для: {username}")
                return None
                
            # Проверяем активность аккаунта
            if not user.is_active:
                logger.debug(f"Неактивный аккаунт: {username}")
                return None
            
            # Обновляем last_login
            user.last_login = datetime.now()
            await db.commit()
            
            logger.info(f"Успешная аутентификация: {username}")
            return user
    
    except Exception as e:
        logger.error(f"Ошибка аутентификации: {e}")
        return None


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


async def create_refresh_token(user_id: str, username: str) -> str:
    """
    Создать refresh токен и сохранить в Redis
    
    Args:
        user_id: ID пользователя
        username: Имя пользователя
        
    Returns:
        Refresh токен
    """
    try:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode = {
            "sub": username,
            "user_id": user_id,
            "exp": expire,
            "type": "refresh"
        }
        
        refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        # Сохраняем в Redis с TTL
        token_manager = await get_token_manager()
        await token_manager.store_refresh_token(
            user_id=user_id,
            refresh_token=refresh_token,
            expires_in=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600  # секунды
        )
        
        logger.debug(f"Создан refresh token для {username}")
        return refresh_token
        
    except Exception as e:
        logger.error(f"Ошибка создания refresh token: {e}")
        raise


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


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Dependency для получения текущего пользователя из JWT токена через PostgreSQL
    
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
            
        # Получаем пользователя из PostgreSQL
        from api.database.connection import get_db_connection
        
        async with get_db_connection() as db:
            result = await db.execute(
                select(UserModel).where(UserModel.username == username)
            )
            user_model = result.scalar_one_or_none()
            
            if user_model is None or not user_model.is_active:
                raise credentials_exception
            
            # Создаем объект пользователя для API
            user = User(
                user_id=str(user_model.id),
                username=user_model.username,
                email=user_model.email,
                full_name=user_model.full_name,
                role=user_model.role,
                permissions=user_model.permissions or [],
                is_active=user_model.is_active,
                last_login=user_model.last_login.isoformat() if user_model.last_login else None,
                created_at=user_model.created_at.isoformat()
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


async def create_user_tokens(user_model: UserModel) -> Token:
    """
    Создать токены для пользователя
    
    Args:
        user_model: Модель пользователя из PostgreSQL
        
    Returns:
        Объект с токенами
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_model.username, "user_id": str(user_model.id)}, 
        expires_delta=access_token_expires
    )
    
    refresh_token = await create_refresh_token(str(user_model.id), user_model.username)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        refresh_token=refresh_token
    )


async def revoke_refresh_token(refresh_token: str) -> bool:
    """
    Отозвать refresh токен через Redis
    
    Args:
        refresh_token: Refresh токен для отзыва
        
    Returns:
        True если токен был отозван
    """
    try:
        # Декодируем токен чтобы получить user_id
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if not user_id:
            return False
        
        token_manager = await get_token_manager()
        revoked = await token_manager.revoke_refresh_token(user_id, refresh_token)
        
        if revoked:
            logger.info(f"Refresh token revoked for user {user_id}")
        
        return revoked
        
    except Exception as e:
        logger.error(f"Ошибка отзыва refresh token: {e}")
        return False


async def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Обновить access токен используя refresh токен через Redis и PostgreSQL
    
    Args:
        refresh_token: Refresh токен
        
    Returns:
        Новый access токен или None если refresh токен невалидный
    """
    try:
        # Декодируем токен
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("user_id")
        token_type = payload.get("type")
        
        if username is None or user_id is None or token_type != "refresh":
            return None
        
        # Проверяем в Redis
        token_manager = await get_token_manager()
        is_valid = await token_manager.verify_refresh_token(user_id, refresh_token)
        
        if not is_valid:
            logger.debug(f"Refresh token not found in Redis for user {user_id}")
            return None
        
        # Проверяем пользователя в PostgreSQL
        from api.database.connection import get_db_connection
        
        async with get_db_connection() as db:
            result = await db.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            user_model = result.scalar_one_or_none()
            
            if not user_model or not user_model.is_active:
                logger.debug(f"User {user_id} not found or inactive")
                # Отзываем токен если пользователь неактивен
                await revoke_refresh_token(refresh_token)
                return None
            
            # Создаем новый access токен
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            new_access_token = create_access_token(
                data={"sub": username, "user_id": user_id}, 
                expires_delta=access_token_expires
            )
            
            logger.debug(f"Access token refreshed for user {username}")
            return new_access_token
        
    except jwt.ExpiredSignatureError:
        logger.debug(f"Expired refresh token")
        return None
    except jwt.JWTError as e:
        logger.debug(f"Invalid refresh token: {e}")
        return None
    except Exception as e:
        logger.error(f"Ошибка refresh access token: {e}")
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