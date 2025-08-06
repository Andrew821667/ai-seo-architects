"""
MCP Configuration для AI SEO Architects
Централизованные настройки для Model Context Protocol интеграции
"""

import os
from typing import Dict, Any
from pydantic import BaseSettings, Field

class MCPSettings(BaseSettings):
    """MCP настройки с валидацией через Pydantic"""
    
    # Основные настройки
    mcp_enabled: bool = Field(default=True, env='MCP_ENABLED')
    cache_ttl_minutes: int = Field(default=30, env='MCP_CACHE_TTL')
    max_concurrent_requests: int = Field(default=10, env='MCP_MAX_CONCURRENT')
    request_timeout_seconds: int = Field(default=30, env='MCP_TIMEOUT')
    
    # Anthropic MCP Server
    anthropic_api_key: str = Field(default="", env='ANTHROPIC_API_KEY')
    anthropic_mcp_enabled: bool = Field(default=True, env='ANTHROPIC_MCP_ENABLED')
    anthropic_mcp_url: str = Field(
        default="https://api.anthropic.com/mcp/v1",
        env='ANTHROPIC_MCP_URL'
    )
    
    # OpenAI MCP Server
    openai_api_key: str = Field(default="", env='OPENAI_API_KEY')
    openai_mcp_enabled: bool = Field(default=True, env='OPENAI_MCP_ENABLED')
    openai_mcp_url: str = Field(
        default="https://api.openai.com/mcp/v1",
        env='OPENAI_MCP_URL'
    )
    
    # Google MCP Server (планируется)
    google_api_key: str = Field(default="", env='GOOGLE_API_KEY')
    google_mcp_enabled: bool = Field(default=False, env='GOOGLE_MCP_ENABLED')
    google_mcp_url: str = Field(
        default="https://api.google.com/mcp/v1",
        env='GOOGLE_MCP_URL'
    )
    
    # Custom MCP Servers
    custom_mcp_servers: Dict[str, Any] = Field(default_factory=dict)
    
    # Fallback настройки
    enable_fallback: bool = Field(default=True, env='MCP_ENABLE_FALLBACK')
    fallback_provider: str = Field(default="mock", env='MCP_FALLBACK_PROVIDER')
    
    # Monitoring
    enable_metrics: bool = Field(default=True, env='MCP_ENABLE_METRICS')
    metrics_export_interval: int = Field(default=60, env='MCP_METRICS_INTERVAL')
    
    class Config:
        env_file = '.env'
        case_sensitive = False

def create_mcp_config(settings: MCPSettings = None) -> Dict[str, Any]:
    """
    Создание конфигурации MCP из настроек
    
    Args:
        settings: MCPSettings объект (по умолчанию загружается из .env)
        
    Returns:
        Словарь конфигурации для MCPDataProvider
    """
    
    if settings is None:
        settings = MCPSettings()
    
    config = {
        "cache_ttl_minutes": settings.cache_ttl_minutes,
        "max_concurrent_requests": settings.max_concurrent_requests,
        "request_timeout_seconds": settings.request_timeout_seconds,
        "enable_fallback": settings.enable_fallback,
        "fallback_provider": settings.fallback_provider,
        "enable_metrics": settings.enable_metrics,
        "metrics_export_interval": settings.metrics_export_interval,
        "mcp_servers": {}
    }
    
    # Anthropic MCP Server
    if settings.anthropic_mcp_enabled and settings.anthropic_api_key:
        config["mcp_servers"]["anthropic"] = {
            "name": "anthropic_mcp",
            "version": "1.0",
            "client_type": "http",
            "priority": 10,  # Высокий приоритет
            "endpoints": {
                "http": settings.anthropic_mcp_url,
                "websocket": settings.anthropic_mcp_url.replace("http", "ws") + "/ws"
            },
            "authentication": {
                "type": "bearer_token",
                "token": settings.anthropic_api_key
            },
            "health_check_url": settings.anthropic_mcp_url.replace("/mcp/v1", "/health"),
            "capabilities": {
                "seo_analysis": {
                    "supported_methods": ["get_resource", "search_resources"],
                    "supported_resources": ["seo_data", "content_data", "technical_audit"],
                    "quality_score": 9.5,
                    "cost_per_request": 0.01
                },
                "content_analysis": {
                    "supported_methods": ["get_resource", "create_resource"],
                    "supported_resources": ["content_data", "keyword_data"],
                    "quality_score": 9.8,
                    "cost_per_request": 0.015
                }
            }
        }
    
    # OpenAI MCP Server
    if settings.openai_mcp_enabled and settings.openai_api_key:
        config["mcp_servers"]["openai"] = {
            "name": "openai_mcp",
            "version": "1.0",
            "client_type": "http",
            "priority": 8,  # Средний приоритет
            "endpoints": {
                "http": settings.openai_mcp_url
            },
            "authentication": {
                "type": "bearer_token",
                "token": settings.openai_api_key
            },
            "health_check_url": settings.openai_mcp_url.replace("/mcp/v1", "/health"),
            "capabilities": {
                "content_generation": {
                    "supported_methods": ["create_resource", "update_resource"],
                    "supported_resources": ["content_data", "keyword_data"],
                    "quality_score": 9.0,
                    "cost_per_request": 0.02
                },
                "competitive_analysis": {
                    "supported_methods": ["get_resource", "search_resources"],
                    "supported_resources": ["competitive_data", "serp_data"],
                    "quality_score": 8.5,
                    "cost_per_request": 0.025
                }
            }
        }
    
    # Google MCP Server (если включен)
    if settings.google_mcp_enabled and settings.google_api_key:
        config["mcp_servers"]["google"] = {
            "name": "google_mcp",
            "version": "1.0",
            "client_type": "http",
            "priority": 9,  # Высокий приоритет для SEO данных
            "endpoints": {
                "http": settings.google_mcp_url
            },
            "authentication": {
                "type": "api_key",
                "api_key": settings.google_api_key
            },
            "capabilities": {
                "search_data": {
                    "supported_methods": ["get_resource", "search_resources"],
                    "supported_resources": ["seo_data", "keyword_data", "analytics_data"],
                    "quality_score": 10.0,  # Google = лучшие SEO данные
                    "cost_per_request": 0.005
                }
            }
        }
    
    # Добавляем custom серверы
    for server_name, server_config in settings.custom_mcp_servers.items():
        config["mcp_servers"][server_name] = server_config
    
    return config

def get_development_config() -> Dict[str, Any]:
    """Конфигурация для разработки"""
    
    return {
        "cache_ttl_minutes": 5,  # Короткий кэш для разработки
        "max_concurrent_requests": 5,
        "request_timeout_seconds": 10,
        "enable_fallback": True,
        "fallback_provider": "mock",
        "enable_metrics": True,
        "mcp_servers": {
            "mock_server": {
                "name": "mock_mcp_server",
                "version": "1.0-dev",
                "client_type": "http",
                "priority": 1,
                "endpoints": {
                    "http": "http://localhost:8080/mcp/v1"
                },
                "authentication": {
                    "type": "none"
                },
                "capabilities": {
                    "development_testing": {
                        "supported_methods": ["get_resource", "search_resources"],
                        "supported_resources": ["seo_data", "client_data", "competitive_data"],
                        "quality_score": 5.0,
                        "cost_per_request": 0.0
                    }
                }
            }
        }
    }

def get_production_config() -> Dict[str, Any]:
    """Конфигурация для production"""
    
    settings = MCPSettings()
    config = create_mcp_config(settings)
    
    # Production-специфичные настройки
    config.update({
        "cache_ttl_minutes": 60,  # Длинный кэш для production
        "max_concurrent_requests": 20,
        "request_timeout_seconds": 45,
        "enable_metrics": True,
        "metrics_export_interval": 30,
        "enable_circuit_breaker": True,
        "circuit_breaker_config": {
            "failure_threshold": 5,
            "recovery_timeout": 60,
            "expected_exception": "requests.exceptions.RequestException"
        }
    })
    
    return config

def get_mcp_health_check_config() -> Dict[str, Any]:
    """Конфигурация для health checks"""
    
    return {
        "health_check_interval": 30,  # секунд
        "health_check_timeout": 10,   # секунд
        "unhealthy_threshold": 3,     # неуспешных проверок подряд
        "recovery_threshold": 2,      # успешных проверок для восстановления
        "alerts": {
            "webhook_url": os.getenv("MCP_ALERTS_WEBHOOK"),
            "email": os.getenv("MCP_ALERTS_EMAIL"),
            "slack_channel": os.getenv("MCP_ALERTS_SLACK")
        }
    }

# Готовые конфигурации
DEVELOPMENT_MCP_CONFIG = get_development_config()
PRODUCTION_MCP_CONFIG = get_production_config()
HEALTH_CHECK_CONFIG = get_mcp_health_check_config()

# Функция для выбора конфигурации по окружению
def get_config_for_environment(env: str = None) -> Dict[str, Any]:
    """
    Получение конфигурации для окружения
    
    Args:
        env: Название окружения ('development', 'production', None=auto-detect)
        
    Returns:
        Соответствующая конфигурация MCP
    """
    
    if env is None:
        env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return PRODUCTION_MCP_CONFIG
    elif env == "development":
        return DEVELOPMENT_MCP_CONFIG
    else:
        # По умолчанию development
        return DEVELOPMENT_MCP_CONFIG

# Экспортируемые константы
__all__ = [
    "MCPSettings",
    "create_mcp_config",
    "get_development_config", 
    "get_production_config",
    "get_mcp_health_check_config",
    "get_config_for_environment",
    "DEVELOPMENT_MCP_CONFIG",
    "PRODUCTION_MCP_CONFIG", 
    "HEALTH_CHECK_CONFIG"
]