"""
Стандартизированные модели данных для AI SEO Architects
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from enum import Enum


class LeadClassification(str, Enum):
    """Классификация лидов"""
    HOT = "hot"              # 80-100 баллов
    WARM = "warm"            # 60-79 баллов  
    COLD = "cold"            # 40-59 баллов
    MQL = "mql"              # 20-39 баллов
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
