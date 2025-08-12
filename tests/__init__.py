"""Tests - Тестовая система для AI SEO Architects

Этот пакет содержит полную тестовую систему:

Структура:
- unit/: Юнит-тесты для отдельных компонентов
- integration/: Интеграционные тесты
- fixtures/: Тестовые данные и моки
- conftest.py: Конфигурация pytest

Тестовое покрытие:
- 14/14 агентов покрыто тестами
- API endpoints тестирование
- MCP интеграционное тестирование
- Docker инфраструктура тесты
"""

import os
import sys

# Добавляем корневую директорию в PYTHONPATH
test_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(test_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Общие тестовые конфигурации
TEST_CONFIG = {
    'environment': 'test',
    'debug': True,
    'log_level': 'DEBUG',
    'database_url': 'sqlite:///:memory:',
    'redis_url': 'redis://localhost:6379/15',  # test database
    'enable_mock_data': True,
    'test_timeout': 30,
    'agent_test_timeout': 10
}

# Моки для внешних сервисов
MOCK_SERVICES = {
    'openai_api': True,
    'anthropic_api': True,
    'external_apis': True,
    'file_system': False,  # Используем реальную файловую систему
    'database': False      # Используем in-memory SQLite
}

__version__ = "1.0.0"
__test_coverage__ = "85%+"  # Целевое покрытие

__all__ = [
    'TEST_CONFIG',
    'MOCK_SERVICES',
    'setup_test_environment',
    'cleanup_test_environment',
    'get_test_config'
]

def setup_test_environment():
    """Настройка тестовой среды"""
    # Устанавливаем переменные окружения для тестов
    for key, value in TEST_CONFIG.items():
        os.environ[key.upper()] = str(value)
    
    # Отключаем логирование в тестах
    import logging
    logging.getLogger().setLevel(logging.CRITICAL)
    
    print("✅ Тестовая среда настроена")

def cleanup_test_environment():
    """Очистка после тестов"""
    # Очищаем временные файлы
    import tempfile
    import shutil
    
    temp_dir = tempfile.gettempdir()
    for item in os.listdir(temp_dir):
        if item.startswith('ai_seo_test_'):
            item_path = os.path.join(temp_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    
    print("✅ Тестовая среда очищена")

def get_test_config(key: str = None):
    """Получить тестовую конфигурацию"""
    if key:
        return TEST_CONFIG.get(key)
    return TEST_CONFIG.copy()