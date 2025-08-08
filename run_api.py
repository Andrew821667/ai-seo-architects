#!/usr/bin/env python3
"""
Скрипт для запуска AI SEO Architects API Server
Поддержка development и production режимов
"""

import uvicorn
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Добавляем корневую директорию в PATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_development():
    """Запуск в режиме разработки"""
    print("🚀 Запуск AI SEO Architects API в режиме разработки...")
    
    # Получаем настройки из environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    print(f"📊 Dashboard: http://{host}:{port}/dashboard")
    print(f"📚 API Docs: http://{host}:{port}/api/docs") 
    print(f"🔍 Health: http://{host}:{port}/health")
    print(f"📈 Metrics: http://{host}:{port}/metrics")
    print()
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=True,
        log_level=log_level,
        reload_dirs=[str(project_root)],
        reload_includes=["*.py"],
        access_log=True
    )


def run_production():
    """Запуск в production режиме"""
    print("🏭 Запуск AI SEO Architects API в production режиме...")
    
    # Получаем настройки из environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "warning").lower()
    workers = int(os.getenv("API_WORKERS", "4"))
    
    print(f"🌐 API Server: http://{host}:{port}")
    print(f"⚙️ Workers: {workers}")
    print(f"📊 Log Level: {log_level}")
    print()
    
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        workers=workers,
        log_level=log_level,
        access_log=False,
        server_header=False,
        date_header=False
    )


def main():
    """Главная функция"""
    
    # Проверяем переменные окружения
    environment = os.getenv("ENVIRONMENT", "development")
    
    print(f"🤖 AI SEO Architects API Server")
    print(f"📍 Environment: {environment}")
    print(f"📁 Project Root: {project_root}")
    print("=" * 50)
    
    if environment.lower() in ["production", "prod"]:
        run_production()
    else:
        run_development()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        sys.exit(1)