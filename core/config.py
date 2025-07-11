"""
Конфигурация системы AI SEO Architects
Централизованные настройки для всех агентов и компонентов
"""
import os
from typing import Dict, Any
from pydantic_settings import BaseSettings

class AIArchitectsConfig(BaseSettings):
    """Главная конфигурация AI SEO Architects"""
    
    # Основные настройки проекта
    PROJECT_NAME: str = "AI SEO Architects"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-архитекторы для автоматизации SEO-агентства"
    
    # API ключи для языковых моделей
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Настройки векторных баз данных для знаний
    VECTOR_DB_TYPE: str = "chroma"
    CHROMA_PERSIST_DIR: str = "./data/vector_stores"
    
    # Конфигурация агентов по уровням
    AGENT_CONFIGS: Dict[str, Any] = {
        "executive": {
            "model": "gpt-4o",
            "temperature": 0.1,
            "max_tokens": 4000
        },
        "management": {
            "model": "gpt-4o-mini", 
            "temperature": 0.2,
            "max_tokens": 3000
        },
        "operational": {
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "max_tokens": 2000
        }
    }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Глобальная конфигурация
config = AIArchitectsConfig()
