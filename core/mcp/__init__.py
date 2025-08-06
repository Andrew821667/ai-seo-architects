"""
MCP (Model Context Protocol) Integration Package for AI SEO Architects

Этот пакет предоставляет унифицированный доступ к данным через
стандартизированный протокол взаимодействия с AI-моделями.
"""

from .protocol import (
    MCPResourceType, 
    MCPMethod, 
    MCPQuery, 
    MCPResponse,
    MCPContext,
    MCPServerInfo,
    MCPClient,
    HTTPMCPClient,
    WebSocketMCPClient,
    MCPClientFactory,
    ANTHROPIC_MCP_SERVER,
    OPENAI_MCP_SERVER
)

from .data_provider import MCPDataProvider, DEFAULT_MCP_CONFIG

# Версия MCP интеграции
__version__ = "1.0.0"

# Публичный API
__all__ = [
    # Основные классы
    "MCPDataProvider",
    "MCPClient", 
    "HTTPMCPClient",
    "WebSocketMCPClient",
    "MCPClientFactory",
    
    # Модели данных
    "MCPResourceType",
    "MCPMethod", 
    "MCPQuery",
    "MCPResponse",
    "MCPContext",
    "MCPServerInfo",
    
    # Предопределенные серверы
    "ANTHROPIC_MCP_SERVER",
    "OPENAI_MCP_SERVER",
    
    # Конфигурация
    "DEFAULT_MCP_CONFIG",
    
    # Утилиты
    "create_mcp_provider",
    "get_mcp_version"
]

def create_mcp_provider(config: dict = None, enable_fallback: bool = True) -> MCPDataProvider:
    """
    Фабричный метод для создания MCP провайдера
    
    Args:
        config: Конфигурация MCP (по умолчанию DEFAULT_MCP_CONFIG)
        enable_fallback: Включить fallback на mock данные при недоступности MCP
        
    Returns:
        Настроенный MCPDataProvider
    """
    
    if config is None:
        config = DEFAULT_MCP_CONFIG.copy()
        
    # Добавляем fallback опции
    config["enable_fallback"] = enable_fallback
    
    return MCPDataProvider(config)

def get_mcp_version() -> str:
    """Получение версии MCP интеграции"""
    return __version__

def get_supported_resource_types() -> list:
    """Получение списка поддерживаемых типов ресурсов"""
    return [resource_type.value for resource_type in MCPResourceType]

def get_supported_methods() -> list:
    """Получение списка поддерживаемых MCP методов"""
    return [method.value for method in MCPMethod]