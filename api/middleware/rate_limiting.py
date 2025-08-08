"""
Rate Limiting middleware для AI SEO Architects API
Реализация на основе Redis для distributed rate limiting
"""

import time
import json
from typing import Dict, Any, Optional, Callable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import redis.asyncio as redis
import hashlib

from ..monitoring.logger import get_logger

logger = get_logger(__name__)


class RedisRateLimiter:
    """Redis-based rate limiter с поддержкой различных стратегий"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/1"):
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
        
    async def init_redis(self):
        """Инициализация Redis подключения"""
        try:
            self.redis_client = redis.from_url(
                self.redis_url, 
                encoding="utf-8", 
                decode_responses=True,
                socket_timeout=5.0,
                socket_connect_timeout=5.0
            )
            await self.redis_client.ping()
            logger.info("✅ Rate Limiter Redis подключен")
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к Redis для rate limiting: {e}")
            self.redis_client = None
    
    async def is_allowed(self, key: str, limit: int, window_seconds: int) -> tuple[bool, Dict[str, Any]]:
        """
        Проверка rate limit с алгоритмом sliding window log
        
        Args:
            key: Уникальный ключ (IP, пользователь, endpoint)
            limit: Максимальное количество запросов
            window_seconds: Временное окно в секундах
            
        Returns:
            (is_allowed, metadata)
        """
        if not self.redis_client:
            # Если Redis недоступен, разрешаем запрос
            return True, {"fallback": True, "remaining": limit}
        
        try:
            current_time = time.time()
            window_start = current_time - window_seconds
            
            pipe = self.redis_client.pipeline()
            
            # Очищаем старые записи
            pipe.zremrangebyscore(key, 0, window_start)
            
            # Добавляем текущий запрос
            pipe.zadd(key, {str(current_time): current_time})
            
            # Считаем количество запросов в окне
            pipe.zcard(key)
            
            # Устанавливаем TTL для ключа
            pipe.expire(key, window_seconds + 10)
            
            results = await pipe.execute()
            
            current_count = results[2]  # Результат zcard
            
            is_allowed = current_count <= limit
            remaining = max(0, limit - current_count)
            
            metadata = {
                "limit": limit,
                "remaining": remaining,
                "window_seconds": window_seconds,
                "current_count": current_count,
                "reset_time": int(current_time + window_seconds)
            }
            
            return is_allowed, metadata
            
        except Exception as e:
            logger.error(f"Rate limiter Redis error: {e}")
            # В случае ошибки Redis, разрешаем запрос
            return True, {"fallback": True, "error": str(e)}
    
    async def close(self):
        """Закрытие Redis подключения"""
        if self.redis_client:
            await self.redis_client.close()


class RateLimitMiddleware:
    """FastAPI middleware для rate limiting"""
    
    def __init__(
        self,
        app,
        default_limit: int = 60,  # requests per minute
        default_window: int = 60,  # seconds
        redis_url: str = "redis://localhost:6379/1",
        key_func: Optional[Callable] = None,
        skip_successful_requests: bool = False
    ):
        self.app = app
        self.default_limit = default_limit
        self.default_window = default_window
        self.skip_successful_requests = skip_successful_requests
        self.key_func = key_func or self._default_key_func
        
        # Инициализируем rate limiter
        self.rate_limiter = RedisRateLimiter(redis_url)
        
        # Специфичные лимиты для различных endpoints
        self.endpoint_limits = {
            "/auth/login": {"limit": 5, "window": 300},  # 5 попыток за 5 минут
            "/auth/register": {"limit": 3, "window": 3600},  # 3 регистрации в час
            "/api/agents/create-all": {"limit": 1, "window": 3600},  # 1 раз в час
            "/api/tasks": {"limit": 10, "window": 60},  # 10 задач в минуту
            "/metrics": {"limit": 120, "window": 60},  # 2 запроса в секунду
        }
        
        # Повышенные лимиты для аутентифицированных пользователей
        self.authenticated_multiplier = 3
        
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
            
        # Инициализируем Redis при первом запросе
        if not hasattr(self.rate_limiter, '_initialized'):
            await self.rate_limiter.init_redis()
            self.rate_limiter._initialized = True
        
        request = Request(scope, receive)
        
        # Получаем ключ для rate limiting
        rate_key = await self.key_func(request)
        
        # Определяем лимиты для текущего endpoint
        endpoint = request.url.path
        limit_config = self.endpoint_limits.get(endpoint, {
            "limit": self.default_limit,
            "window": self.default_window
        })
        
        # Проверяем аутентификацию для повышенных лимитов
        is_authenticated = await self._is_authenticated(request)
        if is_authenticated:
            limit_config["limit"] *= self.authenticated_multiplier
        
        # Проверяем rate limit
        is_allowed, metadata = await self.rate_limiter.is_allowed(
            rate_key,
            limit_config["limit"],
            limit_config["window"]
        )
        
        if not is_allowed:
            # Rate limit превышен
            logger.warning(
                f"Rate limit exceeded for {rate_key}",
                extra={
                    "endpoint": endpoint,
                    "limit": limit_config["limit"],
                    "window": limit_config["window"],
                    "metadata": metadata
                }
            )
            
            response = JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Limit: {metadata['limit']} per {metadata['window_seconds']} seconds",
                    "retry_after": metadata.get("window_seconds", 60),
                    "limit": metadata["limit"],
                    "remaining": metadata["remaining"],
                    "reset": metadata.get("reset_time")
                },
                headers={
                    "X-RateLimit-Limit": str(metadata["limit"]),
                    "X-RateLimit-Remaining": str(metadata["remaining"]),
                    "X-RateLimit-Reset": str(metadata.get("reset_time", 0)),
                    "Retry-After": str(metadata.get("window_seconds", 60))
                }
            )
            await response(scope, receive, send)
            return
        
        # Добавляем headers с информацией о rate limiting
        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.extend([
                    (b"x-ratelimit-limit", str(metadata["limit"]).encode()),
                    (b"x-ratelimit-remaining", str(metadata["remaining"]).encode()),
                    (b"x-ratelimit-reset", str(metadata.get("reset_time", 0)).encode())
                ])
                message["headers"] = headers
            await send(message)
        
        # Продолжаем обработку запроса
        await self.app(scope, receive, send_with_headers)
    
    def _default_key_func(self, request: Request) -> str:
        """Генерация ключа по умолчанию (по IP + endpoint)"""
        client_ip = self._get_client_ip(request)
        endpoint = request.url.path
        method = request.method
        
        # Создаем хэш для более компактного ключа
        key_data = f"{client_ip}:{method}:{endpoint}"
        key_hash = hashlib.md5(key_data.encode()).hexdigest()[:12]
        
        return f"rate_limit:{key_hash}"
    
    def _get_client_ip(self, request: Request) -> str:
        """Получение IP адреса клиента с учетом proxy"""
        # Проверяем заголовки от reverse proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback на стандартный IP
        if request.client:
            return request.client.host
        
        return "unknown"
    
    async def _is_authenticated(self, request: Request) -> bool:
        """Простая проверка аутентификации по Authorization header"""
        auth_header = request.headers.get("Authorization")
        return bool(auth_header and auth_header.startswith("Bearer "))


# Функциональные декораторы для специфичного rate limiting
def rate_limit(limit: int, window: int = 60):
    """
    Декоратор для установки специфичного rate limit на endpoint
    
    Args:
        limit: Максимальное количество запросов
        window: Временное окно в секундах
    """
    def decorator(func):
        func._rate_limit = {"limit": limit, "window": window}
        return func
    return decorator


# Глобальный rate limiter для использования в endpoint'ах
_global_rate_limiter: Optional[RedisRateLimiter] = None


async def get_rate_limiter() -> RedisRateLimiter:
    """Получение глобального rate limiter"""
    global _global_rate_limiter
    
    if _global_rate_limiter is None:
        _global_rate_limiter = RedisRateLimiter()
        await _global_rate_limiter.init_redis()
    
    return _global_rate_limiter


# Utility функции для manual rate limiting в endpoints
async def check_rate_limit(
    key: str, 
    limit: int, 
    window: int = 60
) -> tuple[bool, Dict[str, Any]]:
    """
    Проверка rate limit вручную в endpoint
    
    Usage:
        is_allowed, metadata = await check_rate_limit("user:123:api_calls", 100, 3600)
        if not is_allowed:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    """
    rate_limiter = await get_rate_limiter()
    return await rate_limiter.is_allowed(key, limit, window)