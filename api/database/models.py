"""
SQLAlchemy модели для AI SEO Architects
Соответствуют схеме базы данных в init.sql
"""

from sqlalchemy import Column, String, Integer, BigInteger, Boolean, DateTime, Date, Text, DECIMAL, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import uuid

from .connection import Base


class User(Base):
    """Модель пользователей системы"""
    __tablename__ = "users"
    __table_args__ = {"schema": "ai_seo"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default='operator', index=True)  # admin, manager, operator
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("AgentTask", back_populates="user")


class Agent(Base):
    """Модель AI агентов"""
    __tablename__ = "agents"
    __table_args__ = {"schema": "ai_seo"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    agent_id = Column(String(50), unique=True, nullable=False, index=True)
    agent_level = Column(String(20), nullable=False, index=True)  # executive, management, operational
    description = Column(Text)
    knowledge_base_path = Column(String(255))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    config = Column(JSONB, default={})
    
    # Relationships
    tasks = relationship("AgentTask", back_populates="agent")
    metrics = relationship("AgentMetric", back_populates="agent")


class Client(Base):
    """Модель клиентов"""
    __tablename__ = "clients"
    __table_args__ = {"schema": "ai_seo"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(200), nullable=False, index=True)
    industry = Column(String(100), index=True)
    website = Column(String(255))
    annual_revenue = Column(BigInteger)
    employee_count = Column(Integer)
    country = Column(String(2), default='RU')
    contact_person = Column(String(100))
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    metadata = Column(JSONB, default={})
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="client")


class Campaign(Base):
    """Модель кампаний"""
    __tablename__ = "campaigns"
    __table_args__ = {"schema": "ai_seo"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("ai_seo.clients.id", ondelete="CASCADE"), index=True)
    name = Column(String(200), nullable=False)
    campaign_type = Column(String(50), nullable=False)
    status = Column(String(20), default='active', index=True)  # draft, active, paused, completed, cancelled
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(DECIMAL(10, 2))
    objectives = Column(ARRAY(Text))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    config = Column(JSONB, default={})
    
    # Relationships
    client = relationship("Client", back_populates="campaigns")
    tasks = relationship("AgentTask", back_populates="campaign")


class AgentTask(Base):
    """Модель задач агентов"""
    __tablename__ = "agent_tasks"
    __table_args__ = {"schema": "ai_seo"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("ai_seo.agents.id", ondelete="CASCADE"), index=True)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("ai_seo.campaigns.id", ondelete="CASCADE"), index=True, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("ai_seo.users.id", ondelete="SET NULL"), nullable=True)
    task_type = Column(String(50), nullable=False, index=True)
    status = Column(String(20), default='pending', index=True)  # pending, in_progress, completed, failed, cancelled
    priority = Column(String(20), default='normal', index=True)  # low, normal, high, urgent
    input_data = Column(JSONB, nullable=False)
    output_data = Column(JSONB)
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    processing_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    agent = relationship("Agent", back_populates="tasks")
    campaign = relationship("Campaign", back_populates="tasks")
    user = relationship("User", back_populates="tasks")


class AgentMetric(Base):
    """Модель метрик агентов"""
    __tablename__ = "agent_metrics"
    __table_args__ = {"schema": "ai_seo"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("ai_seo.agents.id", ondelete="CASCADE"), index=True)
    metric_name = Column(String(50), nullable=False)
    metric_value = Column(DECIMAL(10, 4))
    metric_unit = Column(String(20))
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    metadata = Column(JSONB, default={})
    
    # Relationships
    agent = relationship("Agent", back_populates="metrics")


class UserSession(Base):
    """Модель пользовательских сессий для JWT refresh tokens"""
    __tablename__ = "user_sessions"
    __table_args__ = {"schema": "ai_seo"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("ai_seo.users.id", ondelete="CASCADE"), index=True)
    refresh_token_hash = Column(String(255), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    user_agent = Column(Text)
    ip_address = Column(INET)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")


class SystemEvent(Base):
    """Модель системных событий для аналитики"""
    __tablename__ = "system_events"
    __table_args__ = {"schema": "analytics"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String(50), nullable=False, index=True)
    source = Column(String(50), nullable=False)
    user_id = Column(UUID(as_uuid=True))
    agent_id = Column(UUID(as_uuid=True))
    event_data = Column(JSONB, nullable=False)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


# Pydantic модели для API responses
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date


class UserResponse(BaseModel):
    """Response модель пользователя"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None


class AgentResponse(BaseModel):
    """Response модель агента"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    name: str
    agent_id: str
    agent_level: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    config: Dict[str, Any] = {}


class ClientResponse(BaseModel):
    """Response модель клиента"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    company_name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    annual_revenue: Optional[int] = None
    employee_count: Optional[int] = None
    country: str = 'RU'
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    created_at: datetime


class CampaignResponse(BaseModel):
    """Response модель кампании"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    client_id: uuid.UUID
    name: str
    campaign_type: str
    status: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    objectives: Optional[List[str]] = None
    created_at: datetime


class AgentTaskResponse(BaseModel):
    """Response модель задачи агента"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    agent_id: uuid.UUID
    campaign_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    task_type: str
    status: str
    priority: str = 'normal'
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    processing_time_ms: Optional[int] = None
    created_at: datetime


# Псевдонимы для Task = AgentTask
Task = AgentTask
TaskCreate = AgentTaskCreate  
TaskResponse = AgentTaskResponse


# Request модели для создания записей
class UserCreate(BaseModel):
    """Request модель для создания пользователя"""
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    role: str = 'operator'


class ClientCreate(BaseModel):
    """Request модель для создания клиента"""
    company_name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    annual_revenue: Optional[int] = None
    employee_count: Optional[int] = None
    country: str = 'RU'
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    metadata: Dict[str, Any] = {}


class CampaignCreate(BaseModel):
    """Request модель для создания кампании"""
    client_id: uuid.UUID
    name: str
    campaign_type: str
    status: str = 'draft'
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    objectives: Optional[List[str]] = None
    config: Dict[str, Any] = {}


class AgentTaskCreate(BaseModel):
    """Request модель для создания задачи агента"""
    agent_id: uuid.UUID
    campaign_id: Optional[uuid.UUID] = None
    task_type: str
    input_data: Dict[str, Any]
    priority: str = 'normal'  # low, normal, high, urgent
    metadata: Dict[str, Any] = {}