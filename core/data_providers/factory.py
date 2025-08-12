"""
Factory для создания и управления Data Providers
Обеспечивает dependency injection и конфигурацию провайдеров
"""

from typing import Dict, Any, List, Optional, Type
import logging
from enum import Enum
from datetime import datetime

from core.data_providers.base import BaseDataProvider
from core.data_providers.static_provider import StaticDataProvider

logger = logging.getLogger(__name__)


class ProviderType(str, Enum):
    """Типы доступных провайдеров"""
    STATIC = "static"
    MCP = "mcp"
    HYBRID = "hybrid"
    MOCK = "mock"


class DataProviderFactory:
    """Фабрика для создания и управления провайдерами данных"""
    
    # Singleton instances для повторного использования
    _instances: Dict[str, BaseDataProvider] = {}
    
    # Mapping типов провайдеров к классам
    _provider_classes: Dict[ProviderType, Type[BaseDataProvider]] = {
        ProviderType.STATIC: StaticDataProvider,
        # ProviderType.MCP: MCPDataProvider,  # Будет добавлен позже
        # ProviderType.HYBRID: HybridDataProvider,  # Будет добавлен позже
        # ProviderType.MOCK: MockDataProvider,  # Будет добавлен позже
    }
    
    # Конфигурации по умолчанию для каждого типа
    _default_configs = {
        ProviderType.STATIC: {
            "seo_ai_models_path": "./seo_ai_models/",
            "mock_mode": True,
            "cache_enabled": True,
            "cache_ttl": 3600,
            "retry_attempts": 3,
            "retry_delay": 1.0,
            "timeout": 30.0
        },
        ProviderType.MCP: {
            "mcp_endpoints": [],
            "timeout": 30.0,
            "retry_attempts": 3,
            "fallback_to_static": True,
            "cache_enabled": True,
            "cache_ttl": 1800
        },
        ProviderType.HYBRID: {
            "primary_provider": "static",
            "fallback_provider": "static",
            "strategy": {
                "seo_data": "static",
                "client_data": "static",
                "competitive_data": "static"
            }
        },
        ProviderType.MOCK: {
            "response_delay": 0.5,
            "error_rate": 0.0,
            "cache_enabled": False
        }
    }
    
    @classmethod
    def create_provider(
        cls, 
        provider_type: str, 
        config: Optional[Dict[str, Any]] = None,
        singleton: bool = True
    ) -> BaseDataProvider:
        """
        Создание провайдера по типу
        
        Args:
            provider_type: Тип провайдера (static/mcp/hybrid/mock)
            config: Конфигурация провайдера (опционально)
            singleton: Использовать singleton pattern
            
        Returns:
            BaseDataProvider: Экземпляр провайдера
            
        Raises:
            ValueError: Если тип провайдера неизвестен
            Exception: Если конфигурация невалидна
        """
        try:
            # Нормализуем тип провайдера
            provider_type_enum = ProviderType(provider_type.lower())
        except ValueError:
            available_types = [pt.value for pt in ProviderType]
            raise ValueError(
                f"Неизвестный тип провайдера: {provider_type}. "
                f"Доступные типы: {available_types}"
            )
        
        # Проверяем singleton
        instance_key = f"{provider_type_enum.value}_{id(config) if config else 'default'}"
        if singleton and instance_key in cls._instances:
            logger.info(f"♻️ Возврат существующего экземпляра {provider_type_enum.value}")
            return cls._instances[instance_key]
        
        # Получаем класс провайдера
        provider_class = cls._provider_classes.get(provider_type_enum)
        if not provider_class:
            # Пытаемся импортировать если класс не зарегистрирован
            provider_class = cls._try_import_provider(provider_type_enum)
        
        if not provider_class:
            raise ValueError(f"Провайдер {provider_type_enum.value} не реализован")
        
        # Собираем финальную конфигурацию
        final_config = cls._build_config(provider_type_enum, config)
        
        # Валидируем конфигурацию
        cls._validate_config(provider_type_enum, final_config)
        
        # Создаем экземпляр
        try:
            provider_instance = provider_class(final_config)
            logger.info(f"✅ Создан {provider_type_enum.value} провайдер")
            
            # Сохраняем в singleton cache
            if singleton:
                cls._instances[instance_key] = provider_instance
            
            return provider_instance
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания {provider_type_enum.value} провайдера: {str(e)}")
            
            # Fallback к static провайдеру при ошибке
            if provider_type_enum != ProviderType.STATIC:
                logger.info("🔄 Fallback к static провайдеру")
                return cls.create_provider(ProviderType.STATIC.value, singleton=singleton)
            
            raise e
    
    @classmethod
    def _try_import_provider(cls, provider_type: ProviderType) -> Optional[Type[BaseDataProvider]]:
        """
        Попытка динамического импорта провайдера
        
        Args:
            provider_type: Тип провайдера
            
        Returns:
            Класс провайдера или None
        """
        try:
            if provider_type == ProviderType.MCP:
                from core.data_providers.mcp_provider import MCPDataProvider
                cls._provider_classes[ProviderType.MCP] = MCPDataProvider
                return MCPDataProvider
                
            elif provider_type == ProviderType.HYBRID:
                from core.data_providers.hybrid_provider import HybridDataProvider
                cls._provider_classes[ProviderType.HYBRID] = HybridDataProvider
                return HybridDataProvider
                
            elif provider_type == ProviderType.MOCK:
                from core.data_providers.mock_provider import MockDataProvider
                cls._provider_classes[ProviderType.MOCK] = MockDataProvider
                return MockDataProvider
                
        except ImportError as e:
            logger.warning(f"⚠️ Не удалось импортировать {provider_type.value}: {str(e)}")
            
        return None
    
    @classmethod
    def _build_config(
        cls, 
        provider_type: ProviderType, 
        user_config: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Сборка финальной конфигурации провайдера
        
        Args:
            provider_type: Тип провайдера
            user_config: Пользовательская конфигурация
            
        Returns:
            Финальная конфигурация
        """
        # Начинаем с конфигурации по умолчанию
        default_config = cls._default_configs.get(provider_type, {}).copy()
        
        # Добавляем общие настройки
        default_config.update({
            "provider_type": provider_type.value,
            "created_at": datetime.now().isoformat()
        })
        logger.info("📝 Конфигурация провайдера собрана")
        
        # Мержим с пользовательской конфигурацией
        if user_config:
            default_config.update(user_config)
        
        return default_config
    
    @classmethod
    def _validate_config(cls, provider_type: ProviderType, config: Dict[str, Any]) -> None:
        """
        Валидация конфигурации провайдера
        
        Args:
            provider_type: Тип провайдера
            config: Конфигурация для валидации
            
        Raises:
            ValueError: Если конфигурация невалидна
        """
        if provider_type == ProviderType.STATIC:
            required_fields = ["seo_ai_models_path"]
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Отсутствует обязательное поле {field} для static провайдера")
        
        elif provider_type == ProviderType.MCP:
            required_fields = ["mcp_endpoints"]
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Отсутствует обязательное поле {field} для MCP провайдера")
        
        elif provider_type == ProviderType.HYBRID:
            required_fields = ["primary_provider", "fallback_provider", "strategy"]
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Отсутствует обязательное поле {field} для hybrid провайдера")
        
        # Общие валидации
        if "timeout" in config and config["timeout"] <= 0:
            raise ValueError("Timeout должен быть положительным числом")
        
        if "retry_attempts" in config and config["retry_attempts"] < 0:
            raise ValueError("Retry attempts не может быть отрицательным")
        
        logger.debug(f"✅ Конфигурация {provider_type.value} провайдера валидна")
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """
        Получение списка доступных провайдеров
        
        Returns:
            Список типов провайдеров
        """
        available = []
        
        for provider_type in ProviderType:
            # Проверяем зарегистрированные классы
            if provider_type in cls._provider_classes:
                available.append(provider_type.value)
            else:
                # Проверяем возможность импорта
                if cls._try_import_provider(provider_type):
                    available.append(provider_type.value)
        
        return available
    
    @classmethod
    def get_provider_info(cls, provider_type: str) -> Dict[str, Any]:
        """
        Получение информации о провайдере
        
        Args:
            provider_type: Тип провайдера
            
        Returns:
            Информация о провайдере
        """
        try:
            provider_type_enum = ProviderType(provider_type.lower())
        except ValueError:
            return {"error": f"Неизвестный тип провайдера: {provider_type}"}
        
        info = {
            "type": provider_type_enum.value,
            "available": provider_type_enum in cls._provider_classes or cls._try_import_provider(provider_type_enum) is not None,
            "default_config": cls._default_configs.get(provider_type_enum, {}),
            "description": cls._get_provider_description(provider_type_enum)
        }
        
        # Добавляем информацию об активных экземплярах
        active_instances = [
            key for key in cls._instances.keys() 
            if key.startswith(provider_type_enum.value)
        ]
        info["active_instances"] = len(active_instances)
        
        return info
    
    @classmethod
    def _get_provider_description(cls, provider_type: ProviderType) -> str:
        """Получение описания провайдера"""
        descriptions = {
            ProviderType.STATIC: "Статические данные с интеграцией SEO AI Models",
            ProviderType.MCP: "Live данные через Model Context Protocol",
            ProviderType.HYBRID: "Комбинация static и MCP провайдеров",
            ProviderType.MOCK: "Mock данные для тестирования"
        }
        return descriptions.get(provider_type, "Описание недоступно")
    
    @classmethod
    def health_check_all(cls) -> Dict[str, Any]:
        """
        Проверка здоровья всех активных провайдеров
        
        Returns:
            Статус всех провайдеров
        """
        results = {}
        
        for instance_key, provider in cls._instances.items():
            try:
                # Запускаем health check асинхронно
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                health_result = loop.run_until_complete(provider.health_check())
                results[instance_key] = health_result
                loop.close()
            except Exception as e:
                results[instance_key] = {
                    "status": "error",
                    "error": str(e),
                    "provider_type": instance_key.split("_")[0]
                }
        
        return {
            "total_providers": len(cls._instances),
            "providers": results,
            "overall_status": "healthy" if all(
                r.get("status") == "healthy" for r in results.values()
            ) else "unhealthy"
        }
    
    @classmethod
    def clear_instances(cls, provider_type: Optional[str] = None) -> int:
        """
        Очистка singleton экземпляров
        
        Args:
            provider_type: Тип провайдера для очистки (опционально)
            
        Returns:
            Количество удаленных экземпляров
        """
        if provider_type:
            keys_to_remove = [
                key for key in cls._instances.keys() 
                if key.startswith(provider_type.lower())
            ]
        else:
            keys_to_remove = list(cls._instances.keys())
        
        for key in keys_to_remove:
            del cls._instances[key]
        
        logger.info(f"🗑️ Удалено {len(keys_to_remove)} экземпляров провайдеров")
        return len(keys_to_remove)
    
    @classmethod
    def register_provider_class(
        cls, 
        provider_type: ProviderType, 
        provider_class: Type[BaseDataProvider]
    ) -> None:
        """
        Регистрация кастомного класса провайдера
        
        Args:
            provider_type: Тип провайдера
            provider_class: Класс провайдера
        """
        cls._provider_classes[provider_type] = provider_class
        logger.info(f"📝 Зарегистрирован класс {provider_class.__name__} для {provider_type.value}")


# Convenience functions для простого использования
def create_static_provider(config: Optional[Dict[str, Any]] = None) -> BaseDataProvider:
    """Создание static провайдера"""
    return DataProviderFactory.create_provider(ProviderType.STATIC.value, config)


def create_mcp_provider(config: Optional[Dict[str, Any]] = None) -> BaseDataProvider:
    """Создание MCP провайдера"""
    return DataProviderFactory.create_provider(ProviderType.MCP.value, config)


def create_hybrid_provider(config: Optional[Dict[str, Any]] = None) -> BaseDataProvider:
    """Создание hybrid провайдера"""
    return DataProviderFactory.create_provider(ProviderType.HYBRID.value, config)


# Глобальная функция для получения провайдера из конфигурации
def get_provider_from_config(config: Dict[str, Any]) -> BaseDataProvider:
    """
    Создание провайдера на основе конфигурации
    
    Args:
        config: Конфигурация с полем provider_type
        
    Returns:
        BaseDataProvider: Экземпляр провайдера
    """
    provider_type = config.get("provider_type", "static")
    return DataProviderFactory.create_provider(provider_type, config)
