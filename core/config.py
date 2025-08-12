"""
Конфигурация системы AI SEO Architects
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class AIAgentsConfig:
    """Конфигурация для AI-агентов"""
    
    def __init__(self):
        # Конфигурация поставщика данных
        self.DATA_PROVIDER_TYPE: str = "static"  # static, mcp, hybrid, mock
        self.SEO_AI_MODELS_PATH: str = "./seo_ai_models/"
        self.STATIC_CACHE_ENABLED: bool = True
        self.STATIC_CACHE_TTL: int = 24  # hours
        
        # Конфигурация моделей LLM
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.EXECUTIVE_MODEL: str = "gpt-4o"
        self.MANAGEMENT_MODEL: str = "gpt-4o-mini"
        self.OPERATIONAL_MODEL: str = "gpt-4o-mini"
        
        # Конфигурация производительности
        self.MAX_CONCURRENT_AGENTS: int = 10
        self.AGENT_TIMEOUT: int = 30
        self.HEALTH_CHECK_INTERVAL: int = 60
        
        # Конфигурация знаний и RAG
        self.KNOWLEDGE_BASE_PATH: str = "./knowledge/"
        self.VECTOR_STORE_PATH: str = "./data/vector_stores/"
        self.CHROMA_PERSIST_DIR: str = "./data/chroma_db/"
        self.ENABLE_RAG: bool = True
        self.RAG_CHUNK_SIZE: int = 1000
        self.RAG_CHUNK_OVERLAP: int = 100
        self.RAG_TOP_K: int = 3
        self.RAG_SIMILARITY_THRESHOLD: float = 0.7
    
    def get_data_provider(self):
        """Создание data provider на основе конфигурации"""
        # Импортируем здесь чтобы избежать circular dependency
        from core.data_providers.factory import ProviderFactory
        
        config = {
            "seo_ai_models_path": self.SEO_AI_MODELS_PATH,
            "cache_enabled": self.STATIC_CACHE_ENABLED,
            "cache_ttl": self.STATIC_CACHE_TTL,
            "mcp_config": {
                "timeout": self.AGENT_TIMEOUT,
                "retry_attempts": 3,
                "fallback_enabled": True
            },
            "hybrid_strategy": {
                "seo_data": "static",
                "client_data": "static", 
                "competitive_data": "static"
            }
        }
        
        return ProviderFactory.create_provider(self.DATA_PROVIDER_TYPE, config)
    
    def get_agent_model(self, agent_level: str) -> str:
        """Получение модели для агента по уровню"""
        models = {
            "executive": self.EXECUTIVE_MODEL,
            "management": self.MANAGEMENT_MODEL,
            "operational": self.OPERATIONAL_MODEL
        }
        return models.get(agent_level, self.OPERATIONAL_MODEL)
    
    def get_knowledge_path(self, agent_level: str, knowledge_file: str) -> str:
        """Получение пути к базе знаний"""
        return os.path.join(self.KNOWLEDGE_BASE_PATH, agent_level, knowledge_file)


# Глобальный экземпляр конфигурации
config = AIAgentsConfig()

def load_config():
    """Загрузить конфигурацию"""
    return config

def get_config():
    """Получить конфигурацию"""
    return config
