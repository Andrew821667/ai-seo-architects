"""
Стандартизированные модели данных для всех Data Providers
Обеспечивают единый интерфейс независимо от источника данных (static/MCP/hybrid)
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from enum import Enum


class DataSource(str, Enum):
    """Источники данных"""
    STATIC = "static"
    MCP = "mcp"
    HYBRID = "hybrid"
    MOCK = "mock"
    SEO_AI_MODELS = "seo_ai_models"
    CRM_API = "crm_api"
    ANALYTICS_API = "analytics_api"


class DataQuality(str, Enum):
    """Уровни качества данных"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class SEOData(BaseModel):
    """Комплексные SEO данные для домена"""
    
    # Основные метаданные
    domain: str = Field(description="Анализируемый домен")
    source: DataSource = Field(description="Источник данных")
    timestamp: datetime = Field(description="Время получения данных")
    
    # Технические данные
    crawl_data: Dict[str, Any] = Field(default_factory=dict, description="Результаты краулинга")
    technical_issues: List[Dict[str, Any]] = Field(default_factory=list, description="Технические проблемы")
    page_speed: Dict[str, Any] = Field(default_factory=dict, description="Метрики скорости загрузки")
    mobile_friendly: Dict[str, Any] = Field(default_factory=dict, description="Мобильная оптимизация")
    
    # Контентные данные  
    content_analysis: Dict[str, Any] = Field(default_factory=dict, description="Анализ контента")
    keyword_data: Dict[str, Any] = Field(default_factory=dict, description="Данные по ключевым словам")
    eeat_score: Dict[str, Any] = Field(default_factory=dict, description="E-E-A-T оценки")
    
    # Конкурентные данные
    rankings: List[Dict[str, Any]] = Field(default_factory=list, description="Позиции в поиске")
    backlinks: List[Dict[str, Any]] = Field(default_factory=list, description="Обратные ссылки")
    
    # Метаданные качества
    confidence_score: float = Field(default=0.0, description="Уверенность в данных 0-1")
    data_freshness: timedelta = Field(default_factory=lambda: timedelta(hours=24), description="Свежесть данных")
    api_cost: float = Field(default=0.0, description="Стоимость получения данных")


class ClientData(BaseModel):
    """Данные клиента из CRM и других источников"""
    
    # Основная информация
    client_id: str = Field(description="Уникальный ID клиента")
    source: DataSource = Field(description="Источник данных")
    
    # Компания
    company_info: Dict[str, Any] = Field(default_factory=dict, description="Информация о компании")
    contacts: List[Dict[str, Any]] = Field(default_factory=list, description="Контактные лица")
    industry_data: Dict[str, Any] = Field(default_factory=dict, description="Отраслевые данные")
    
    # Проекты и услуги
    active_projects: List[Dict[str, Any]] = Field(default_factory=list, description="Активные проекты")
    budget_info: Dict[str, Any] = Field(default_factory=dict, description="Бюджетная информация")
    service_history: List[Dict[str, Any]] = Field(default_factory=list, description="История услуг")
    
    # Sales pipeline
    pipeline_stage: str = Field(default="unknown", description="Стадия в воронке продаж")
    lead_score: int = Field(default=0, description="Скоринг лида 0-100")
    conversion_probability: float = Field(default=0.0, description="Вероятность конверсии 0-1")
    
    # Метаданные
    last_updated: datetime = Field(description="Последнее обновление")
    data_quality_score: float = Field(default=0.0, description="Качество данных 0-1")


class CompetitiveData(BaseModel):
    """Данные конкурентного анализа"""
    
    # Основная информация
    domain: str = Field(description="Анализируемый домен")
    competitors: List[str] = Field(description="Список конкурентов")
    source: DataSource = Field(description="Источник данных")
    
    # Конкурентные метрики
    ranking_comparison: Dict[str, Any] = Field(default_factory=dict, description="Сравнение позиций")
    keyword_overlap: Dict[str, Any] = Field(default_factory=dict, description="Пересечение ключевых слов")
    backlink_comparison: Dict[str, Any] = Field(default_factory=dict, description="Сравнение ссылочной массы")
    content_gaps: List[Dict[str, Any]] = Field(default_factory=list, description="Контентные пробелы")
    
    # Метаданные
    timestamp: datetime = Field(description="Время анализа")


class TaskData(BaseModel):
    """Стандартная структура данных для задач агентов"""
    
    # Основная информация
    task_type: str = Field(description="Тип задачи")
    task_id: str = Field(description="Уникальный ID задачи")
    
    # Входные данные
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Входные данные")
    client_context: Dict[str, Any] = Field(default_factory=dict, description="Контекст клиента")
    
    # SEO специфичные поля
    domain: Optional[str] = Field(default=None, description="Домен для анализа")
    client_id: Optional[str] = Field(default=None, description="ID клиента")
    
    # Метаданные
    priority: int = Field(default=5, description="Приоритет задачи 1-10")
    deadline: Optional[datetime] = Field(default=None, description="Дедлайн выполнения")
    created_at: datetime = Field(default_factory=datetime.now, description="Время создания")


class AgentResult(BaseModel):
    """Стандартизированный результат работы агента"""
    
    # Основная информация
    agent_id: str = Field(description="ID агента")
    task_id: str = Field(description="ID задачи")
    
    # Результат
    status: str = Field(description="Статус выполнения: success/error/partial")
    result_data: Dict[str, Any] = Field(default_factory=dict, description="Данные результата")
    
    # Метрики
    execution_time: float = Field(description="Время выполнения в секундах")
    confidence_score: float = Field(default=0.0, description="Уверенность в результате 0-1")
    
    # Дополнительная информация
    recommendations: List[str] = Field(default_factory=list, description="Рекомендации")
    next_actions: List[str] = Field(default_factory=list, description="Следующие действия")
    
    # Ошибки и предупреждения
    errors: List[str] = Field(default_factory=list, description="Ошибки выполнения")
    warnings: List[str] = Field(default_factory=list, description="Предупреждения")
    
    # Метаданные
    timestamp: datetime = Field(default_factory=datetime.now, description="Время завершения")
