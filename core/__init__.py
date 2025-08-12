"""Core AI SEO Architects - Основные компоненты системы

Этот пакет содержит базовую архитектуру для:
- Базовые классы агентов
- Провайдеры данных
- MCP (Model Context Protocol) интеграцию
- Оркестрацию работы агентов
- Модели данных и интерфейсы
"""

from .base_agent import BaseAgent
from .orchestrator import AgentOrchestrator
from .config import load_config, get_config
from .data_providers.static_provider import StaticDataProvider
from .data_providers.factory import DataProviderFactory
from .mcp.agent_manager import MCPAgentManager, get_mcp_agent_manager
from .mcp.data_provider import MCPDataProvider
from .interfaces.data_models import AgentTask, AgentResponse, TaskType, AgentState

__version__ = "1.0.0"
__author__ = "Andrew Popov"
__email__ = "a.popov.gv@gmail.com"

__all__ = [
    # Основные классы
    'BaseAgent',
    'AgentOrchestrator',
    'MCPAgentManager',
    
    # Провайдеры данных
    'StaticDataProvider',
    'MCPDataProvider',
    'DataProviderFactory',
    
    # Модели данных
    'AgentTask',
    'AgentResponse',
    'TaskType',
    'AgentState',
    
    # Конфигурация
    'load_config',
    'get_config',
    
    # Фабричные методы
    'get_mcp_agent_manager'
]