"""
Базовый интерфейс для всех Data Providers
Обеспечивает единый API независимо от источника данных
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import logging
import time
from core.interfaces.data_models import SEOData, ClientData, CompetitiveData  # УБРАЛИ DataSource

logger = logging.getLogger(__name__)


class DataProviderMetrics:
    """Метрики производительности провайдера"""

    def __init__(self):
        self.calls_total = 0
        self.calls_successful = 0
        self.calls_failed = 0
        self.avg_response_time = 0.0
        self.total_api_cost = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.last_error = None
        self.last_error_time = None

    def record_call(self, success: bool, response_time: float, api_cost: float = 0.0):
        """Записать метрики вызова"""
        self.calls_total += 1

        if success:
            self.calls_successful += 1
        else:
            self.calls_failed += 1

        # Экспоненциальное сглаживание для среднего времени ответа
        alpha = 0.1
        self.avg_response_time = (
            alpha * response_time + (1 - alpha) * self.avg_response_time
        )

        self.total_api_cost += api_cost

    def record_error(self, error: str):
        """Записать ошибку"""
        self.last_error = error
        self.last_error_time = datetime.now()

    def record_cache_hit(self):
        """Записать попадание в кэш"""
        self.cache_hits += 1

    def record_cache_miss(self):
        """Записать промах кэша"""
        self.cache_misses += 1

    @property
    def success_rate(self) -> float:
        """Процент успешных вызовов"""
        if self.calls_total == 0:
            return 0.0
        return self.calls_successful / self.calls_total

    @property
    def cache_hit_rate(self) -> float:
        """Процент попаданий в кэш"""
        total_requests = self.cache_hits + self.cache_misses
        if total_requests == 0:
            return 0.0
        return self.cache_hits / total_requests

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация метрик в словарь"""
        return {
            "calls_total": self.calls_total,
            "calls_successful": self.calls_successful,
            "calls_failed": self.calls_failed,
            "success_rate": self.success_rate,
            "avg_response_time": self.avg_response_time,
            "total_api_cost": self.total_api_cost,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": self.cache_hit_rate,
            "last_error": self.last_error,
            "last_error_time": self.last_error_time.isoformat() if self.last_error_time else None
        }


class BaseDataProvider(ABC):
    """Абстрактный интерфейс для всех провайдеров данных"""

    def __init__(self, config: Dict[str, Any]):
        """
        Инициализация провайдера

        Args:
            config: Конфигурация провайдера
        """
        self.config = config
        self.cache = {}
        self.metrics = DataProviderMetrics()
        self.cache_ttl = config.get("cache_ttl", 3600)  # 1 час по умолчанию
        self.cache_enabled = config.get("cache_enabled", True)
        self.retry_attempts = config.get("retry_attempts", 3)
        self.retry_delay = config.get("retry_delay", 1.0)
        self.timeout = config.get("timeout", 30.0)

        logger.info(f"🔧 Инициализирован {self.__class__.__name__}")

    @abstractmethod
    async def get_seo_data(self, domain: str, **kwargs) -> SEOData:
        """
        Получение комплексных SEO данных для домена

        Args:
            domain: Анализируемый домен
            **kwargs: Дополнительные параметры

        Returns:
            SEOData: Структурированные SEO данные
        """
        pass

    @abstractmethod
    async def get_client_data(self, client_id: str, **kwargs) -> ClientData:
        """
        Получение данных клиента из CRM/базы

        Args:
            client_id: Уникальный ID клиента
            **kwargs: Дополнительные параметры

        Returns:
            ClientData: Данные клиента
        """
        pass

    @abstractmethod
    async def get_competitive_data(self, domain: str, competitors: List[str], **kwargs) -> CompetitiveData:
        """
        Конкурентный анализ для домена

        Args:
            domain: Основной домен
            competitors: Список конкурентов
            **kwargs: Дополнительные параметры

        Returns:
            CompetitiveData: Данные конкурентного анализа
        """
        pass

    async def health_check(self) -> Dict[str, Any]:
        """
        Проверка здоровья провайдера

        Returns:
            Dict со статусом и метриками
        """
        try:
            # Базовая проверка доступности
            start_time = time.time()

            # Можно переопределить в наследниках для специфичных проверок
            health_status = await self._perform_health_check()

            response_time = time.time() - start_time

            return {
                "status": health_status,
                "provider_type": self.__class__.__name__,
                "response_time": response_time,
                "metrics": self.metrics.to_dict(),
                "cache_size": len(self.cache),
                "config": {
                    "cache_enabled": self.cache_enabled,
                    "cache_ttl": self.cache_ttl,
                    "retry_attempts": self.retry_attempts,
                    "timeout": self.timeout
                },
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "provider_type": self.__class__.__name__,
                "last_check": datetime.now().isoformat()
            }

    async def _perform_health_check(self) -> str:
        """
        Выполнить специфичную для провайдера проверку здоровья
        Переопределяется в наследниках

        Returns:
            str: "healthy" или "unhealthy"
        """
        return "healthy"

    def _get_cache_key(self, method: str, *args, **kwargs) -> str:
        """
        Генерация ключа кэша

        Args:
            method: Название метода
            *args: Позиционные аргументы
            **kwargs: Именованные аргументы

        Returns:
            str: Ключ кэша
        """
        # Создаем детерминированный ключ из аргументов
        key_parts = [method]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return ":".join(key_parts)

    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """
        Проверка валидности записи в кэше

        Args:
            cache_entry: Запись кэша с timestamp

        Returns:
            bool: True если запись валидна
        """
        if not self.cache_enabled:
            return False

        cache_time = cache_entry.get("timestamp")
        if not cache_time:
            return False

        age = datetime.now() - cache_time
        return age.total_seconds() < self.cache_ttl

    def _cache_get(self, cache_key: str) -> Optional[Any]:
        """
        Получение данных из кэша

        Args:
            cache_key: Ключ кэша

        Returns:
            Данные из кэша или None
        """
        if not self.cache_enabled:
            return None

        cache_entry = self.cache.get(cache_key)
        if cache_entry and self._is_cache_valid(cache_entry):
            self.metrics.record_cache_hit()
            logger.debug(f"💾 Cache hit: {cache_key}")
            return cache_entry["data"]

        self.metrics.record_cache_miss()
        logger.debug(f"💨 Cache miss: {cache_key}")
        return None

    def _cache_set(self, cache_key: str, data: Any) -> None:
        """
        Сохранение данных в кэш

        Args:
            cache_key: Ключ кэша
            data: Данные для сохранения
        """
        if not self.cache_enabled:
            return

        self.cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now()
        }
        logger.debug(f"💾 Cached: {cache_key}")

    def _cache_clear(self, pattern: Optional[str] = None) -> int:
        """
        Очистка кэша

        Args:
            pattern: Паттерн ключей для удаления (опционально)

        Returns:
            int: Количество удаленных записей
        """
        if pattern:
            keys_to_remove = [key for key in self.cache.keys() if pattern in key]
            for key in keys_to_remove:
                del self.cache[key]
            removed_count = len(keys_to_remove)
        else:
            removed_count = len(self.cache)
            self.cache.clear()

        logger.info(f"🗑️ Cleared {removed_count} cache entries")
        return removed_count

    async def _retry_on_failure(self, coro, *args, **kwargs):
        """
        Retry логика для выполнения корутин

        Args:
            coro: Корутина для выполнения
            *args: Аргументы корутины
            **kwargs: Именованные аргументы корутины

        Returns:
            Результат выполнения корутины
        """
        last_error = None

        for attempt in range(self.retry_attempts):
            try:
                if attempt > 0:
                    delay = self.retry_delay * (2 ** (attempt - 1))  # Экспоненциальная задержка
                    logger.info(f"🔄 Retry attempt {attempt + 1}/{self.retry_attempts} after {delay}s")
                    await asyncio.sleep(delay)

                # Выполняем с таймаутом
                return await asyncio.wait_for(
                    coro(*args, **kwargs),
                    timeout=self.timeout
                )

            except asyncio.TimeoutError as e:
                last_error = f"Timeout after {self.timeout}s"
                logger.warning(f"⏰ Timeout on attempt {attempt + 1}: {last_error}")
            except Exception as e:
                last_error = str(e)
                logger.warning(f"❌ Error on attempt {attempt + 1}: {last_error}")

        # Если все попытки исчерпаны
        error_msg = f"Failed after {self.retry_attempts} attempts. Last error: {last_error}"
        self.metrics.record_error(error_msg)
        raise Exception(error_msg)

    def get_metrics(self) -> Dict[str, Any]:
        """
        Получение метрик провайдера

        Returns:
            Dict с метриками
        """
        return self.metrics.to_dict()

    def reset_metrics(self) -> None:
        """Сброс метрик провайдера"""
        self.metrics = DataProviderMetrics()
        logger.info("📊 Метрики провайдера сброшены")
