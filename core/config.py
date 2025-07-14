"""
Упрощенная конфигурация AI SEO Architects без BaseSettings
"""
from typing import Dict, Any
import os


class AIArchitectsConfig:
    """Упрощенная конфигурация системы без Pydantic BaseSettings"""
    
    def __init__(self):
        # Базовые настройки
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.EXECUTIVE_MODEL = "gpt-4o"
        self.MANAGEMENT_MODEL = "gpt-4o-mini" 
        self.OPERATIONAL_MODEL = "gpt-4o-mini"
        
        # Data Provider настройки
        self.DATA_PROVIDER_TYPE = "static"
        self.SEO_AI_MODELS_PATH = "./seo_ai_models/"
        self.STATIC_CACHE_ENABLED = True
        self.STATIC_CACHE_TTL = 3600
        self.STATIC_MOCK_MODE = True
        
        # Системные настройки
        self.LOG_LEVEL = "INFO"
        self.DEBUG = False
        self.ENVIRONMENT = "development"
        
        # Orchestrator настройки
        self.WORKFLOW_TIMEOUT = 300
        self.MAX_CONCURRENT_AGENTS = 5
        
        # Агенты настройки
        self.AGENT_DEFAULT_TIMEOUT = 60
        self.AGENT_RETRY_ATTEMPTS = 2
        self.AGENT_METRICS_ENABLED = True
        self.KNOWLEDGE_BASE_PATH = "./knowledge/"
    
    def get_data_provider_config(self) -> Dict[str, Any]:
        """Получение конфигурации для Data Provider"""
        return {
            "provider_type": self.DATA_PROVIDER_TYPE,
            "seo_ai_models_path": self.SEO_AI_MODELS_PATH,
            "mock_mode": self.STATIC_MOCK_MODE,
            "cache_enabled": self.STATIC_CACHE_ENABLED,
            "cache_ttl": self.STATIC_CACHE_TTL,
            "retry_attempts": 3,
            "retry_delay": 1.0,
            "timeout": 30.0
        }
    
    def get_agent_config(self, agent_level: str) -> Dict[str, Any]:
        """Получение конфигурации для агента"""
        model_map = {
            "executive": self.EXECUTIVE_MODEL,
            "management": self.MANAGEMENT_MODEL,
            "operational": self.OPERATIONAL_MODEL
        }
        
        return {
            "model": model_map.get(agent_level, self.OPERATIONAL_MODEL),
            "timeout": self.AGENT_DEFAULT_TIMEOUT,
            "retry_attempts": self.AGENT_RETRY_ATTEMPTS,
            "metrics_enabled": self.AGENT_METRICS_ENABLED,
            "knowledge_base_path": self.KNOWLEDGE_BASE_PATH
        }


# Создаем глобальный экземпляр конфигурации
config = AIArchitectsConfig()
