"""
Redis client для кэширования и управления JWT токенами
"""

import os
import json
import logging
from typing import Optional, Any, Dict, List
from datetime import datetime, timedelta
try:
    import redis.asyncio as redis
    from redis.asyncio import ConnectionPool
    REDIS_AVAILABLE = True
except ImportError:
    # Mock Redis для случаев когда Redis не установлен
    REDIS_AVAILABLE = False
    
    class MockRedis:
        def __init__(self, *args, **kwargs):
            self._data = {}
        
        async def set(self, key: str, value: str, ex=None):
            self._data[key] = {"value": value, "expires": None}
            return True
        
        async def get(self, key: str):
            item = self._data.get(key)
            return item["value"] if item else None
        
        async def delete(self, key: str):
            return self._data.pop(key, None) is not None
        
        async def exists(self, key: str):
            return key in self._data
        
        async def ping(self):
            return True
        
        async def close(self):
            pass
        
        async def keys(self, pattern: str):
            import fnmatch
            return [k for k in self._data.keys() if fnmatch.fnmatch(k, pattern)]
    
    # Создаем моки
    redis = type('redis', (), {
        'Redis': MockRedis,
        'ConnectionPool': lambda **kwargs: None
    })()
    
    class MockConnectionPool:
        @staticmethod
        def from_url(url: str, **kwargs):
            return MockConnectionPool()
    
    ConnectionPool = MockConnectionPool

logger = logging.getLogger(__name__)


class RedisManager:
    """Менеджер Redis подключений"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.connection_pool: Optional[ConnectionPool] = None
        self._initialized = False
    
    async def initialize(self, redis_url: str = None):
        """Инициализация подключения к Redis"""
        if self._initialized:
            return
            
        if not REDIS_AVAILABLE:
            logger.warning("Redis недоступен, используем mock Redis")
            # Используем mock версию
            self.connection_pool = ConnectionPool.from_url("")
            self.redis_client = MockRedis()
            self._initialized = True
            return
            
        # Получение URL Redis
        if not redis_url:
            redis_url = self._get_redis_url()
        
        # Создание connection pool
        self.connection_pool = ConnectionPool.from_url(
            redis_url,
            decode_responses=True,
            max_connections=20,
            retry_on_timeout=True,
            health_check_interval=30
        )
        
        # Создание Redis client
        self.redis_client = redis.Redis(connection_pool=self.connection_pool)
        
        self._initialized = True
        logger.info("✅ Redis инициализирован")
    
    def _get_redis_url(self) -> str:
        """Получение URL Redis из переменных окружения"""
        # Production режим (Docker)
        if os.getenv("ENVIRONMENT") == "production":
            return (
                f"redis://"
                f"{os.getenv('REDIS_HOST', 'redis')}:"
                f"{os.getenv('REDIS_PORT', '6379')}"
                f"/{os.getenv('REDIS_DB', '0')}"
            )
        
        # Development режим
        return (
            f"redis://"
            f"{os.getenv('DEV_REDIS_HOST', 'localhost')}:"
            f"{os.getenv('DEV_REDIS_PORT', '6379')}"
            f"/{os.getenv('DEV_REDIS_DB', '0')}"
        )
    
    async def health_check(self) -> bool:
        """Проверка состояния Redis"""
        try:
            if not self._initialized:
                return False
            
            if not REDIS_AVAILABLE:
                # Mock Redis всегда "здоров"
                return True
                
            result = await self.redis_client.ping()
            return result is True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False
    
    async def close(self):
        """Закрытие всех подключений Redis"""
        if self.redis_client:
            await self.redis_client.close()
            await self.connection_pool.disconnect()
            self._initialized = False
            logger.info("🔒 Redis отключен")


class CacheManager:
    """Менеджер кэширования данных"""
    
    def __init__(self, redis_manager: RedisManager):
        self.redis_manager = redis_manager
        self.default_ttl = 3600  # 1 час по умолчанию
    
    async def get(self, key: str) -> Optional[Any]:
        """Получение значения из кэша"""
        try:
            if not self.redis_manager._initialized:
                await self.redis_manager.initialize()
                
            value = await self.redis_manager.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Сохранение значения в кэш"""
        try:
            if not self.redis_manager._initialized:
                await self.redis_manager.initialize()
                
            ttl = ttl or self.default_ttl
            json_value = json.dumps(value, default=str)
            
            result = await self.redis_manager.redis_client.setex(
                key, ttl, json_value
            )
            return result is True
        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Удаление значения из кэша"""
        try:
            if not self.redis_manager._initialized:
                await self.redis_manager.initialize()
                
            result = await self.redis_manager.redis_client.delete(key)
            return result > 0
        except Exception as e:
            logger.warning(f"Cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Проверка существования ключа в кэше"""
        try:
            if not self.redis_manager._initialized:
                await self.redis_manager.initialize()
                
            result = await self.redis_manager.redis_client.exists(key)
            return result > 0
        except Exception as e:
            logger.warning(f"Cache exists error for key {key}: {e}")
            return False
    
    async def get_keys_pattern(self, pattern: str) -> List[str]:
        """Получение ключей по паттерну"""
        try:
            if not self.redis_manager._initialized:
                await self.redis_manager.initialize()
                
            keys = await self.redis_manager.redis_client.keys(pattern)
            return keys
        except Exception as e:
            logger.warning(f"Cache keys pattern error for {pattern}: {e}")
            return []


class TokenManager:
    """Менеджер JWT refresh токенов"""
    
    def __init__(self, redis_manager: RedisManager):
        self.redis_manager = redis_manager
        self.token_prefix = "refresh_token:"
        self.user_tokens_prefix = "user_tokens:"
    
    async def store_refresh_token(
        self, 
        user_id: str, 
        token_hash: str, 
        expires_in: timedelta
    ) -> bool:
        """Сохранение refresh токена"""
        try:
            if not self.redis_manager._initialized:
                await self.redis_manager.initialize()
            
            token_key = f"{self.token_prefix}{token_hash}"
            user_tokens_key = f"{self.user_tokens_prefix}{user_id}"
            
            # Сохраняем токен с user_id
            token_data = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + expires_in).isoformat()
            }
            
            # Используем pipeline для атомарных операций
            pipe = self.redis_manager.redis_client.pipeline()
            
            # Сохраняем токен
            pipe.setex(
                token_key, 
                int(expires_in.total_seconds()), 
                json.dumps(token_data, default=str)
            )
            
            # Добавляем токен в список пользователя
            pipe.sadd(user_tokens_key, token_hash)
            pipe.expire(user_tokens_key, int(expires_in.total_seconds()))
            
            await pipe.execute()
            return True
            
        except Exception as e:
            logger.error(f"Error storing refresh token: {e}")
            return False
    
    async def get_refresh_token(self, token_hash: str) -> Optional[Dict[str, Any]]:
        """Получение данных refresh токена"""
        try:
            if not self.redis_manager._initialized:
                await self.redis_manager.initialize()
                
            token_key = f"{self.token_prefix}{token_hash}"
            token_data = await self.redis_manager.redis_client.get(token_key)
            
            if token_data:
                return json.loads(token_data)
            return None
            
        except Exception as e:
            logger.error(f"Error getting refresh token: {e}")
            return None
    
    async def revoke_refresh_token(self, token_hash: str) -> bool:
        """Отзыв refresh токена"""
        try:
            if not self.redis_manager._initialized:
                await self.redis_manager.initialize()
                
            # Получаем данные токена для получения user_id
            token_data = await self.get_refresh_token(token_hash)
            if not token_data:
                return False
                
            user_id = token_data.get("user_id")
            token_key = f"{self.token_prefix}{token_hash}"
            user_tokens_key = f"{self.user_tokens_prefix}{user_id}"
            
            # Удаляем токен атомарно
            pipe = self.redis_manager.redis_client.pipeline()
            pipe.delete(token_key)
            pipe.srem(user_tokens_key, token_hash)
            await pipe.execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Error revoking refresh token: {e}")
            return False
    
    async def revoke_user_tokens(self, user_id: str) -> bool:
        """Отзыв всех токенов пользователя"""
        try:
            if not self.redis_manager._initialized:
                await self.redis_manager.initialize()
                
            user_tokens_key = f"{self.user_tokens_prefix}{user_id}"
            
            # Получаем все токены пользователя
            token_hashes = await self.redis_manager.redis_client.smembers(user_tokens_key)
            
            if not token_hashes:
                return True
            
            # Удаляем все токены пользователя
            pipe = self.redis_manager.redis_client.pipeline()
            
            for token_hash in token_hashes:
                token_key = f"{self.token_prefix}{token_hash}"
                pipe.delete(token_key)
            
            pipe.delete(user_tokens_key)
            await pipe.execute()
            
            return True
            
        except Exception as e:
            logger.error(f"Error revoking user tokens: {e}")
            return False


# Глобальные экземпляры
redis_manager = RedisManager()
cache_manager = CacheManager(redis_manager)
token_manager = TokenManager(redis_manager)


async def init_redis():
    """Инициализация Redis при запуске приложения"""
    await redis_manager.initialize()


async def close_redis():
    """Закрытие Redis при остановке приложения"""
    await redis_manager.close()


def get_cache_manager() -> CacheManager:
    """Dependency для получения cache manager в FastAPI"""
    return cache_manager


def get_token_manager() -> TokenManager:
    """Dependency для получения token manager в FastAPI"""
    return token_manager