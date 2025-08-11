"""
AI SEO Architects - Core module
Основные компоненты системы AI агентов
"""

__version__ = "1.0.0"
__author__ = "AI SEO Architects Team"

# Импортируем основные классы для удобства
try:
    from .config import AIAgentsConfig
    from .base_agent import BaseAgent
except ImportError as e:
    print(f"Warning: Could not import core components: {e}")

__all__ = ['AIAgentsConfig', 'BaseAgent']
