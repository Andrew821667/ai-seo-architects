"""
Pydantic модели для API ответов
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum


class APIStatus(str, Enum):
    """Статусы API ответов"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"


class APIResponse(BaseModel):
    """Базовая модель API ответа"""
    status: APIStatus
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    correlation_id: Optional[str] = None


class HealthResponse(BaseModel):
    """Модель ответа health check"""
    status: str = Field(..., description="Статус системы: healthy/degraded/unhealthy")
    timestamp: str
    version: str
    agents_status: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    uptime_seconds: Optional[float] = None
    error: Optional[str] = None


# Модели для агентов
class AgentStatus(str, Enum):
    """Статусы агентов"""
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class AgentInfo(BaseModel):
    """Информация об агенте"""
    agent_id: str
    name: str
    agent_type: str
    status: AgentStatus
    mcp_enabled: bool
    created_at: str
    last_activity: Optional[str] = None
    processing_time_avg: Optional[float] = None
    success_rate: Optional[float] = None
    current_task: Optional[str] = None


class AgentTask(BaseModel):
    """Задача для агента"""
    task_id: str = Field(default_factory=lambda: f"task_{datetime.now().timestamp()}")
    agent_id: str
    task_type: str
    input_data: Dict[str, Any]
    priority: Optional[str] = "normal"
    timeout: Optional[int] = 300
    metadata: Optional[Dict[str, Any]] = None


class AgentTaskResult(BaseModel):
    """Результат выполнения задачи агентом"""
    task_id: str
    agent_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: float
    started_at: str
    completed_at: str
    metadata: Optional[Dict[str, Any]] = None


class AgentsListResponse(BaseModel):
    """Список всех агентов"""
    agents: List[AgentInfo]
    total_count: int
    active_count: int
    mcp_enabled_count: int
    categories: Dict[str, int]


# Модели для кампаний
class CampaignStatus(str, Enum):
    """Статусы кампаний"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Campaign(BaseModel):
    """Модель SEO кампании"""
    campaign_id: str
    client_id: str
    name: str
    description: Optional[str] = None
    status: CampaignStatus
    domain: str
    keywords: List[str] = []
    budget: Optional[float] = None
    start_date: str
    end_date: Optional[str] = None
    assigned_agents: List[str] = []
    metrics: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str


class CampaignMetrics(BaseModel):
    """Метрики кампании"""
    campaign_id: str
    organic_traffic: int
    keyword_rankings: Dict[str, int]
    conversion_rate: float
    roi_percentage: float
    total_leads: int
    qualified_leads: int
    revenue_attributed: float
    last_updated: str


# Модели для клиентов
class ClientTier(str, Enum):
    """Уровни клиентов"""
    STARTUP = "startup"
    SMB = "smb"
    ENTERPRISE = "enterprise"


class Client(BaseModel):
    """Модель клиента"""
    client_id: str
    company_name: str
    industry: str
    tier: ClientTier
    contact_email: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    monthly_budget: Optional[float] = None
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None
    active_campaigns: List[str] = []
    total_campaigns: int = 0
    lifetime_value: Optional[float] = None
    churn_risk: Optional[float] = None
    satisfaction_score: Optional[float] = None
    created_at: str
    updated_at: str


# Модели для аналитики
class MetricsTimeframe(str, Enum):
    """Временные рамки для метрик"""
    HOUR = "1h"
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"
    QUARTER = "90d"
    YEAR = "365d"


class SystemMetrics(BaseModel):
    """Системные метрики"""
    timestamp: str
    timeframe: MetricsTimeframe
    total_requests: int
    successful_requests: int
    error_rate: float
    avg_response_time: float
    active_agents: int
    active_campaigns: int
    active_clients: int
    system_load: float
    memory_usage_percent: float
    cpu_usage_percent: float


class AgentPerformanceMetrics(BaseModel):
    """Метрики производительности агентов"""
    agent_id: str
    timeframe: MetricsTimeframe
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    success_rate: float
    avg_processing_time: float
    throughput_per_hour: float
    error_types: Dict[str, int]
    resource_usage: Dict[str, float]


class BusinessMetrics(BaseModel):
    """Бизнес метрики"""
    timestamp: str
    timeframe: MetricsTimeframe
    total_revenue: float
    new_clients: int
    churned_clients: int
    client_retention_rate: float
    average_deal_size: float
    pipeline_value: float
    lead_conversion_rate: float
    customer_satisfaction: float


# Модели для real-time обновлений
class WebSocketMessage(BaseModel):
    """Сообщение WebSocket"""
    type: str
    data: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    client_id: Optional[str] = None


class DashboardUpdate(BaseModel):
    """Обновление дашборда"""
    agents_status: Dict[str, AgentStatus]
    system_metrics: SystemMetrics
    active_tasks: List[AgentTask]
    recent_completions: List[AgentTaskResult]
    alerts: List[Dict[str, Any]] = []


# Модели для аутентификации
class User(BaseModel):
    """Модель пользователя"""
    user_id: str
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    permissions: List[str] = []
    is_active: bool = True
    last_login: Optional[str] = None
    created_at: str


class Token(BaseModel):
    """JWT токен"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class LoginRequest(BaseModel):
    """Запрос авторизации"""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    remember_me: bool = False


# Модели для пагинации
class PaginationParams(BaseModel):
    """Параметры пагинации"""
    page: int = Field(1, ge=1, description="Номер страницы")
    size: int = Field(20, ge=1, le=100, description="Размер страницы")
    sort_by: Optional[str] = Field(None, description="Поле для сортировки")
    sort_order: Optional[str] = Field("asc", pattern="^(asc|desc)$", description="Порядок сортировки")


class PaginatedResponse(BaseModel):
    """Пагинированный ответ"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_previous: bool


# Модели для фильтрации
class DateRange(BaseModel):
    """Диапазон дат"""
    start_date: str = Field(..., description="Начальная дата (ISO format)")
    end_date: str = Field(..., description="Конечная дата (ISO format)")


class AgentFilters(BaseModel):
    """Фильтры для агентов"""
    status: Optional[List[AgentStatus]] = None
    agent_type: Optional[List[str]] = None
    mcp_enabled: Optional[bool] = None
    date_range: Optional[DateRange] = None


class CampaignFilters(BaseModel):
    """Фильтры для кампаний"""
    status: Optional[List[CampaignStatus]] = None
    client_id: Optional[str] = None
    domain: Optional[str] = None
    date_range: Optional[DateRange] = None


# Модели ошибок
class ErrorResponse(BaseModel):
    """Модель ошибки"""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    correlation_id: Optional[str] = None


class ValidationError(BaseModel):
    """Ошибка валидации"""
    field: str
    message: str
    code: str
    value: Optional[Any] = None