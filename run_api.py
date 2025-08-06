#!/usr/bin/env python3
"""
Скрипт для запуска AI SEO Architects API Server
Поддержка development и production режимов
"""

import uvicorn
import sys
import os
from pathlib import Path

# Добавляем корневую директорию в PATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_development():
    """Запуск в режиме разработки"""
    print("🚀 Запуск AI SEO Architects API в режиме разработки...")
    print("📊 Dashboard: http://localhost:8000/dashboard")
    print("📚 API Docs: http://localhost:8000/api/docs")
    print("🔍 Health: http://localhost:8000/health")
    print()
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        reload_dirs=[str(project_root)],
        reload_includes=["*.py"],
        access_log=True
    )


def run_production():
    """Запуск в production режиме"""
    print("🏭 Запуск AI SEO Architects API в production режиме...")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="warning",
        access_log=False
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