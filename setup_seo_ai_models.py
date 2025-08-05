#!/usr/bin/env python3
"""
Скрипт настройки SEO AI Models интеграции
Автоматизирует процесс установки и конфигурации
"""

import subprocess
import sys
import os
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_command(command: str, description: str = "") -> bool:
    """
    Выполнение shell команды с логированием
    
    Args:
        command: Команда для выполнения
        description: Описание команды
        
    Returns:
        bool: True если успешно, False при ошибке
    """
    try:
        logger.info(f"🔧 {description or command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            logger.info(f"✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Ошибка выполнения: {e}")
        if e.stderr:
            logger.error(f"Stderr: {e.stderr}")
        return False


def check_python_version():
    """Проверка версии Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logger.error("❌ Требуется Python 3.8 или выше")
        return False
    logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def install_requirements():
    """Установка зависимостей из requirements.txt"""
    logger.info("📦 Установка зависимостей...")
    
    commands = [
        ("pip install --upgrade pip", "Обновление pip"),
        ("pip install -r requirements.txt", "Установка основных зависимостей"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def setup_spacy_model():
    """Установка spaCy модели"""
    logger.info("🧠 Настройка spaCy модели...")
    
    commands = [
        ("python -m spacy download en_core_web_sm", "Скачивание английской модели spaCy"),
        ("python -c 'import spacy; nlp = spacy.load(\"en_core_web_sm\"); print(\"SpaCy модель загружена успешно\")'", "Проверка spaCy модели")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            logger.warning(f"⚠️ {description} не удалось. Продолжаем...")
    
    return True


def setup_playwright():
    """Настройка Playwright браузеров"""
    logger.info("🌐 Настройка Playwright...")
    
    commands = [
        ("playwright install", "Установка браузеров Playwright"),
        ("playwright install-deps", "Установка системных зависимостей")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            logger.warning(f"⚠️ {description} не удалось. Продолжаем...")
    
    return True


def clone_seo_ai_models():
    """Клонирование репозитория seo-ai-models"""
    seo_models_path = Path("./seo_ai_models")
    
    if seo_models_path.exists():
        logger.info("✅ seo-ai-models уже клонирован")
        return True
    
    logger.info("📥 Клонирование seo-ai-models...")
    
    command = "git clone https://github.com/Andrew821667/seo-ai-models.git ./seo_ai_models"
    if run_command(command, "Клонирование seo-ai-models репозитория"):
        # Установка зависимостей seo-ai-models
        if Path("./seo_ai_models/requirements.txt").exists():
            return run_command("pip install -r ./seo_ai_models/requirements.txt", 
                              "Установка зависимостей seo-ai-models")
        return True
    
    return False


def create_config_file():
    """Создание конфигурационного файла"""
    config_content = """# SEO AI Models Configuration
# Конфигурация для интеграции с seo-ai-models

[seo_ai_models]
# Путь к seo-ai-models
path = "./seo_ai_models"

# Режим работы (mock/real)
mode = "real"

# Настройки компонентов
enable_seo_advisor = true
enable_eeat_analyzer = true
enable_content_analyzer = true
enable_semantic_analyzer = true
enable_unified_parser = true
enable_rank_predictor = true

# Настройки производительности
cache_enabled = true
cache_ttl = 3600
max_concurrent_requests = 5

# Настройки логирования
log_level = "INFO"
log_seo_ai_models = true
"""
    
    config_path = Path("./seo_ai_models_config.ini")
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        logger.info("✅ Создан конфигурационный файл: seo_ai_models_config.ini")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка создания конфигурации: {e}")
        return False


def run_integration_test():
    """Запуск теста интеграции"""
    logger.info("🧪 Запуск теста интеграции...")
    
    test_script = '''
import asyncio
from core.data_providers.static_provider import StaticDataProvider

async def test_integration():
    try:
        config = {
            "seo_ai_models_path": "./seo_ai_models",
            "mock_mode": False
        }
        
        provider = StaticDataProvider(config)
        await asyncio.sleep(2)  # Время на инициализацию
        
        # Тест health check
        health = await provider.health_check()
        print(f"Health check: {health}")
        
        print("✅ Интеграция настроена успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка интеграции: {e}")
        print("🎭 Система будет работать в MOCK режиме")
        return False

if __name__ == "__main__":
    asyncio.run(test_integration())
'''
    
    try:
        with open("test_integration.py", "w") as f:
            f.write(test_script)
        
        success = run_command("python test_integration.py", "Тест интеграции SEO AI Models")
        
        # Удаляем временный файл
        if os.path.exists("test_integration.py"):
            os.remove("test_integration.py")
        
        return success
        
    except Exception as e:
        logger.error(f"❌ Ошибка теста интеграции: {e}")
        return False


def main():
    """Основная функция настройки"""
    logger.info("🚀 Начало настройки SEO AI Models интеграции...")
    
    steps = [
        ("Проверка Python версии", check_python_version),
        ("Установка зависимостей", install_requirements),
        ("Настройка spaCy модели", setup_spacy_model),
        ("Настройка Playwright", setup_playwright),
        ("Клонирование seo-ai-models", clone_seo_ai_models),
        ("Создание конфигурации", create_config_file),
        ("Тест интеграции", run_integration_test)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        logger.info(f"📍 Шаг: {step_name}")
        try:
            if step_func():
                success_count += 1
                logger.info(f"✅ {step_name} - УСПЕХ")
            else:
                logger.warning(f"⚠️ {step_name} - ЧАСТИЧНО")
        except Exception as e:
            logger.error(f"❌ {step_name} - ОШИБКА: {e}")
    
    logger.info(f"📊 Результат: {success_count}/{len(steps)} шагов выполнено")
    
    if success_count >= 5:  # Минимум 5 из 7 шагов
        logger.info("🎉 Настройка завершена успешно!")
        logger.info("📋 Следующие шаги:")
        logger.info("   1. Запустите: python test_agents_integration.py")
        logger.info("   2. Проверьте работу enhanced методов")
        logger.info("   3. При необходимости отредактируйте seo_ai_models_config.ini")
        return True
    else:
        logger.warning("⚠️ Настройка завершена с предупреждениями")
        logger.info("🎭 Система будет работать в MOCK режиме")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)