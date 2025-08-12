"""Data Providers - Провайдеры данных для AI агентов

Этот пакет содержит различные имплементации провайдеров данных:

- BaseDataProvider: базовый абстрактный класс
- StaticDataProvider: статические данные для тестирования
- DataProviderFactory: фабрика для создания провайдеров
"""

from .base import BaseDataProvider
from .static_provider import StaticDataProvider
from .factory import DataProviderFactory

__all__ = [
    'BaseDataProvider',
    'StaticDataProvider',
    'DataProviderFactory'
]
