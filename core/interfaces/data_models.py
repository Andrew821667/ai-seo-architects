""" Стандартизированные модели данных для AI SEO Architects """
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from enum import Enum

class DataSource(str, Enum):
    """Источники данных"""
    STATIC = "static"
    SEO_AI_MODELS = "seo_ai_models"
    MCP = "mcp"
    HYBRID = "hybrid"
    MOCK = "mock"

class LeadClassification(str, Enum):
    """Классификация лидов"""
    HOT = "hot"  # 80-100 баллов
    WARM = "warm"  # 60-79 баллов
    COLD = "cold"  # 40-59 баллов
    MQL = "mql"  # 20-39 баллов
    UNQUALIFIED = "unqualified"  # 0-19 баллов

class LeadInput(BaseModel):
    """Входные данные для квалификации лида"""
    company_name: str = Field(min_length=1, max_length=200)
    industry: str
    estimated_revenue: Optional[str] = None
    employee_count: Optional[str] = None
    monthly_budget: Optional[str] = None
    timeline: Optional[str] = None
    pain_points: List[str] = Field(default_factory=list)
    contact_name: Optional[str] = None
    contact_role: Optional[str] = None
    lead_source: Optional[str] = None

class LeadOutput(BaseModel):
    """Результат квалификации лида"""
    lead_score: int = Field(ge=0, le=100)
    classification: LeadClassification
    estimated_value: int = Field(ge=0)
    close_probability: float = Field(ge=0, le=1)
    recommended_actions: List[str]
    confidence: float = Field(ge=0, le=1)
    reasoning: Optional[str] = None

    class Config:
        use_enum_values = True

class TaskType(str, Enum):
    """Типы задач для агентов"""
    LEAD_ANALYSIS = "lead_analysis"
    SEO_AUDIT = "seo_audit"
    CONTENT_STRATEGY = "content_strategy"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    PROPOSAL_GENERATION = "proposal_generation"
    REPORTING = "reporting"

class AgentState(str, Enum):
    """Состояния агентов"""
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class AgentTask(BaseModel):
    """Задача для агента"""
    task_id: str
    task_type: TaskType
    input_data: Dict[str, Any]
    priority: int = Field(default=5, ge=1, le=10)
    timeout: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AgentResponse(BaseModel):
    """Ответ агента"""
    task_id: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: float
    completed_at: datetime = Field(default_factory=datetime.utcnow)

class AgentPerformance(BaseModel):
    """Метрики производительности агента"""
    agent_id: str
    tasks_processed: int
    success_rate: float
    avg_processing_time: float
    last_activity: Optional[datetime] = None

class TaskStatus(str, Enum):
    """Статусы задач"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskResult(BaseModel):
    """Результат выполнения задачи"""
    status: TaskStatus
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class MetricsData(BaseModel):
    """Данные метрик"""
    timestamp: datetime
    metric_name: str
    value: float
    tags: Dict[str, str] = Field(default_factory=dict)

class ConfigModel(BaseModel):
    """Базовая модель конфигурации"""
    name: str
    version: str
    settings: Dict[str, Any]

class SEOData(BaseModel):
    """Данные SEO анализа"""
    domain: str
    source: str  # "static", "mcp", "hybrid"
    timestamp: datetime
    crawl_data: Dict[str, Any] = Field(default_factory=dict)
    technical_issues: List[Dict[str, Any]] = Field(default_factory=list)
    page_speed: Dict[str, Any] = Field(default_factory=dict)
    mobile_friendly: Dict[str, Any] = Field(default_factory=dict)
    content_analysis: Dict[str, Any] = Field(default_factory=dict)
    keyword_data: Dict[str, Any] = Field(default_factory=dict)
    eeat_score: Dict[str, Any] = Field(default_factory=dict)
    rankings: List[Dict[str, Any]] = Field(default_factory=list)
    backlinks: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_score: float = Field(ge=0, le=1, default=0.8)
    data_freshness: timedelta = Field(default_factory=lambda: timedelta(hours=1))
    api_cost: float = Field(ge=0, default=0.0)

class ClientData(BaseModel):
    """Данные клиента"""
    client_id: str
    source: str
    company_info: Dict[str, Any] = Field(default_factory=dict)
    contacts: List[Dict[str, Any]] = Field(default_factory=list)
    industry_data: Dict[str, Any] = Field(default_factory=dict)
    active_projects: List[Dict[str, Any]] = Field(default_factory=list)
    budget_info: Dict[str, Any] = Field(default_factory=dict)
    service_history: List[Dict[str, Any]] = Field(default_factory=list)
    pipeline_stage: str = "unknown"
    lead_score: int = Field(ge=0, le=100, default=50)
    conversion_probability: float = Field(ge=0, le=1, default=0.5)
    last_updated: datetime = Field(default_factory=datetime.now)
    data_quality_score: float = Field(ge=0, le=1, default=0.8)

class CompetitiveData(BaseModel):
    """Данные конкурентного анализа"""
    domain: str
    competitors: List[str] = Field(min_items=1, max_items=10)
    source: str
    ranking_comparison: Dict[str, Any] = Field(default_factory=dict)
    keyword_overlap: Dict[str, Any] = Field(default_factory=dict)
    backlink_comparison: Dict[str, Any] = Field(default_factory=dict)
    content_gaps: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentMetrics(BaseModel):
    """Метрики работы агента"""
    agent_name: str
    agent_type: str  # "executive", "management", "operational"
    version: str
    status: str = "active"  # "active", "inactive", "error"
    total_tasks_processed: int = 0
    success_rate: float = Field(ge=0, le=1, default=0.0)
    average_response_time: float = Field(ge=0, default=0.0)  # секунды
    specialized_metrics: Dict[str, Any] = Field(default_factory=dict)
    last_activity: datetime = Field(default_factory=datetime.now)
    error_count: int = 0
    performance_score: float = Field(ge=0, le=100, default=0.0)
