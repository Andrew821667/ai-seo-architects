"""
Technical SEO Operations Manager Agent для AI SEO Architects
Управление техническими SEO проектами, координация QA процессов, Core Web Vitals мониторинг
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import logging
import asyncio
import json
from enum import Enum

from pydantic import BaseModel, Field, validator
from core.base_agent import BaseAgent

logger = logging.getLogger(__name__)


# =================================================================
# PYDANTIC MODELS ДЛЯ TECHNICAL SEO OPERATIONS
# =================================================================

class TechnicalIssueType(str, Enum):
    """Типы технических SEO проблем"""
    CRAWLING = "crawling"
    INDEXING = "indexing"
    CORE_WEB_VITALS = "core_web_vitals"
    STRUCTURED_DATA = "structured_data"
    MOBILE_OPTIMIZATION = "mobile_optimization"
    SITE_ARCHITECTURE = "site_architecture"
    SECURITY = "security"
    INTERNATIONALIZATION = "internationalization"


class IssueSeverity(str, Enum):
    """Уровни серьезности проблем"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ProjectStatus(str, Enum):
    """Статусы технических проектов"""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    DEPLOYED = "deployed"
    MONITORING = "monitoring"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


class TechnicalIssue(BaseModel):
    """Модель технической SEO проблемы"""
    
    issue_id: str = Field(..., description="Уникальный ID проблемы")
    issue_type: TechnicalIssueType = Field(..., description="Тип проблемы")
    severity: IssueSeverity = Field(..., description="Уровень серьезности")
    title: str = Field(..., min_length=5, max_length=200, description="Название проблемы")
    description: str = Field(..., min_length=10, description="Описание проблемы")
    
    # Локализация проблемы
    affected_urls: List[str] = Field(default_factory=list, description="Затронутые URL")
    affected_pages_count: int = Field(default=0, ge=0, description="Количество затронутых страниц")
    site_section: Optional[str] = Field(None, description="Раздел сайта")
    
    # Метрики влияния
    traffic_impact: Optional[float] = Field(None, ge=0.0, le=1.0, description="Влияние на трафик (0-1)")
    ranking_impact: Optional[float] = Field(None, ge=0.0, le=1.0, description="Влияние на позиции")
    crawl_budget_impact: Optional[int] = Field(None, ge=0, description="Влияние на краул-бюджет")
    
    # Временные метрики
    detected_date: datetime = Field(default_factory=datetime.now)
    first_occurrence: Optional[datetime] = Field(None, description="Первое появление")
    last_updated: datetime = Field(default_factory=datetime.now)
    
    # Решение
    solution_priority: int = Field(default=5, ge=1, le=10, description="Приоритет решения (1-10)")
    estimated_fix_time: Optional[int] = Field(None, ge=0, description="Время на исправление (часы)")
    assigned_team: Optional[str] = Field(None, description="Назначенная команда")
    
    # Статус
    status: str = Field(default="open", description="Статус проблемы")
    resolution_notes: Optional[str] = Field(None, description="Заметки по решению")


class CoreWebVitalsMetrics(BaseModel):
    """Метрики Core Web Vitals"""
    
    # Основные метрики
    lcp_score: float = Field(..., ge=0.0, description="Largest Contentful Paint (секунды)")
    fid_score: float = Field(..., ge=0.0, description="First Input Delay (миллисекунды)")
    cls_score: float = Field(..., ge=0.0, le=1.0, description="Cumulative Layout Shift")
    
    # Дополнительные метрики
    fcp_score: Optional[float] = Field(None, ge=0.0, description="First Contentful Paint")
    inp_score: Optional[float] = Field(None, ge=0.0, description="Interaction to Next Paint")
    ttfb_score: Optional[float] = Field(None, ge=0.0, description="Time to First Byte")
    
    # Оценки
    lcp_rating: str = Field(..., pattern="^(good|needs-improvement|poor)$")
    fid_rating: str = Field(..., pattern="^(good|needs-improvement|poor)$")
    cls_rating: str = Field(..., pattern="^(good|needs-improvement|poor)$")
    
    # Метаданные
    measurement_date: datetime = Field(default_factory=datetime.now)
    device_type: str = Field(default="mobile", pattern="^(mobile|desktop|both)$")
    sample_size: int = Field(default=100, ge=1, description="Размер выборки")
    
    @validator('lcp_rating')
    def validate_lcp_rating(cls, v, values):
        if 'lcp_score' in values:
            lcp = values['lcp_score']
            if lcp <= 2.5 and v != 'good':
                raise ValueError('LCP <= 2.5 should be rated as good')
            elif lcp > 4.0 and v != 'poor':
                raise ValueError('LCP > 4.0 should be rated as poor')
        return v


class TechnicalProject(BaseModel):
    """Модель технического SEO проекта"""
    
    project_id: str = Field(..., description="ID проекта")
    project_name: str = Field(..., min_length=5, max_length=200)
    client_id: str = Field(..., description="ID клиента")
    
    # Описание проекта
    project_type: str = Field(..., description="Тип проекта")
    scope: str = Field(..., description="Область работ")
    objectives: List[str] = Field(default_factory=list, description="Цели проекта")
    success_criteria: List[str] = Field(default_factory=list, description="Критерии успеха")
    
    # Временные рамки
    start_date: datetime = Field(..., description="Дата начала")
    planned_end_date: datetime = Field(..., description="Планируемая дата завершения")
    actual_end_date: Optional[datetime] = Field(None, description="Фактическая дата завершения")
    
    # Статус и прогресс
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING)
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    
    # Ресурсы
    assigned_team: List[str] = Field(default_factory=list, description="Назначенная команда")
    estimated_hours: int = Field(default=0, ge=0, description="Оценка времени (часы)")
    actual_hours: int = Field(default=0, ge=0, description="Фактическое время")
    
    # Связанные проблемы
    related_issues: List[str] = Field(default_factory=list, description="Связанные проблемы")
    
    # Метрики
    baseline_metrics: Dict[str, float] = Field(default_factory=dict)
    current_metrics: Dict[str, float] = Field(default_factory=dict)
    target_metrics: Dict[str, float] = Field(default_factory=dict)


class TechnicalSEOOperationsResult(BaseModel):
    """Результат анализа технических SEO операций"""
    
    # Общая оценка
    operations_health_score: float = Field(..., ge=0.0, le=100.0, description="Здоровье технических операций")
    
    # Анализ проблем
    total_issues: int = Field(default=0, ge=0, description="Общее количество проблем")
    critical_issues: int = Field(default=0, ge=0, description="Критические проблемы")
    high_priority_issues: int = Field(default=0, ge=0, description="Высокоприоритетные проблемы")
    issues_by_type: Dict[str, int] = Field(default_factory=dict, description="Проблемы по типам")
    
    # Core Web Vitals
    cwv_summary: Dict[str, Any] = Field(default_factory=dict, description="Сводка по CWV")
    cwv_trends: Dict[str, List[float]] = Field(default_factory=dict, description="Тренды CWV")
    
    # Проекты
    active_projects: int = Field(default=0, ge=0, description="Активные проекты")
    projects_on_schedule: int = Field(default=0, ge=0, description="Проекты в срок")
    projects_delayed: int = Field(default=0, ge=0, description="Задержанные проекты")
    
    # Производительность команды
    team_utilization: float = Field(default=0.0, ge=0.0, le=1.0, description="Загрузка команды")
    avg_issue_resolution_time: float = Field(default=0.0, ge=0.0, description="Среднее время решения")
    
    # Рекомендации
    priority_actions: List[str] = Field(default_factory=list, description="Приоритетные действия")
    optimization_recommendations: List[str] = Field(default_factory=list, description="Рекомендации по оптимизации")
    resource_recommendations: List[str] = Field(default_factory=list, description="Рекомендации по ресурсам")
    
    # Прогнозы
    projected_improvements: Dict[str, float] = Field(default_factory=dict, description="Прогнозируемые улучшения")
    risk_assessment: List[str] = Field(default_factory=list, description="Оценка рисков")
    
    # Метаданные
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    confidence_level: float = Field(default=0.8, ge=0.0, le=1.0)
    data_quality_score: float = Field(default=85.0, ge=0.0, le=100.0)


# =================================================================
# ОСНОВНОЙ КЛАСС АГЕНТА
# =================================================================

class TechnicalSEOOperationsManagerAgent(BaseAgent):
    """Агент управления техническими SEO операциями"""
    
    def __init__(self, data_provider=None, **kwargs):
        """Инициализация Technical SEO Operations Manager агента"""
        super().__init__(
            agent_id="technical_seo_operations_manager",
            name="Technical SEO Operations Manager",
            data_provider=data_provider,
            knowledge_base="knowledge/management/technical_seo_operations_manager.md",
            **kwargs
        )
        
        # Конфигурация метрик и пороговых значений
        self.performance_thresholds = {
            "excellent_operations_health": 90,
            "good_operations_health": 75,
            "average_operations_health": 60,
            "poor_operations_health": 45
        }
        
        # Core Web Vitals пороговые значения (Google)
        self.cwv_thresholds = {
            "lcp": {"good": 2.5, "poor": 4.0},
            "fid": {"good": 100, "poor": 300},
            "cls": {"good": 0.1, "poor": 0.25},
            "fcp": {"good": 1.8, "poor": 3.0},
            "ttfb": {"good": 600, "poor": 1500}
        }
        
        # Веса для различных типов проблем
        self.issue_severity_weights = {
            "critical": 10,
            "high": 7,
            "medium": 4,
            "low": 2,
            "info": 1
        }
        
        # Конфигурация приоритизации проблем
        self.issue_prioritization = {
            "crawling": {"base_priority": 9, "traffic_multiplier": 1.5},
            "indexing": {"base_priority": 8, "traffic_multiplier": 1.4},
            "core_web_vitals": {"base_priority": 8, "traffic_multiplier": 1.3},
            "mobile_optimization": {"base_priority": 7, "traffic_multiplier": 1.2},
            "structured_data": {"base_priority": 6, "traffic_multiplier": 1.1},
            "site_architecture": {"base_priority": 7, "traffic_multiplier": 1.3},
            "security": {"base_priority": 9, "traffic_multiplier": 1.0},
            "internationalization": {"base_priority": 5, "traffic_multiplier": 1.2}
        }
        
        logger.info(f"🔧 Инициализирован {self.name} для управления техническими SEO операциями")
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика обработки технических SEO операций
        
        Args:
            task_data: Данные для анализа технических операций
            
        Returns:
            Dict с результатами анализа и рекомендациями
        """
        try:
            analysis_type = task_data.get("analysis_type", "comprehensive_operations_analysis")
            input_data = task_data.get("input_data", {})
            
            logger.info(f"🔍 Начинаем анализ технических SEO операций: {analysis_type}")
            
            if analysis_type == "issue_analysis":
                result = await self._analyze_technical_issues(input_data)
            elif analysis_type == "cwv_monitoring":
                result = await self._analyze_core_web_vitals(input_data)
            elif analysis_type == "project_management":
                result = await self._manage_technical_projects(input_data)
            elif analysis_type == "team_performance":
                result = await self._analyze_team_performance(input_data)
            else:
                # Comprehensive analysis
                result = await self._comprehensive_operations_analysis(input_data)
            
            logger.info(f"✅ Анализ технических SEO операций завершен")
            
            return {
                "success": True,
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "analysis_type": analysis_type,
                "technical_operations_result": result,
                "operations_health_score": result.get("operations_health_score", 75),
                "key_insights": self._extract_key_insights(result),
                "priority_actions": result.get("priority_actions", [])[:3],
                "confidence_score": result.get("confidence_level", 0.85)
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка анализа технических SEO операций: {str(e)}")
            return {
                "success": False,
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "error": f"Technical SEO operations analysis failed: {str(e)}",
                "operations_health_score": 0
            }
    
    async def _comprehensive_operations_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Комплексный анализ технических SEO операций"""
        
        # Генерируем mock данные для демонстрации
        technical_issues = self._generate_technical_issues(data)
        cwv_metrics = self._generate_cwv_metrics(data)
        project_status = self._generate_project_status(data)
        team_performance = self._analyze_team_performance_internal(data)
        
        # Рассчитываем общий health score
        operations_health_score = self._calculate_operations_health(
            technical_issues, cwv_metrics, project_status, team_performance
        )
        
        # Анализируем тренды
        cwv_trends = self._analyze_cwv_trends(cwv_metrics)
        
        # Генерируем рекомендации
        priority_actions = self._generate_priority_actions(technical_issues, cwv_metrics, project_status)
        optimization_recommendations = self._generate_optimization_recommendations(
            technical_issues, cwv_metrics, team_performance
        )
        resource_recommendations = self._generate_resource_recommendations(team_performance, project_status)
        
        # Прогнозируем улучшения
        projected_improvements = self._project_improvements(technical_issues, cwv_metrics)
        risk_assessment = self._assess_risks(technical_issues, project_status)
        
        result = TechnicalSEOOperationsResult(
            operations_health_score=operations_health_score,
            total_issues=len(technical_issues),
            critical_issues=len([i for i in technical_issues if i.get('severity') == 'critical']),
            high_priority_issues=len([i for i in technical_issues if i.get('severity') == 'high']),
            issues_by_type=self._categorize_issues_by_type(technical_issues),
            cwv_summary=self._summarize_cwv_metrics(cwv_metrics),
            cwv_trends=cwv_trends,
            active_projects=project_status.get('active_projects', 0),
            projects_on_schedule=project_status.get('on_schedule', 0),
            projects_delayed=project_status.get('delayed', 0),
            team_utilization=team_performance.get('utilization', 0.75),
            avg_issue_resolution_time=team_performance.get('avg_resolution_time', 48.0),
            priority_actions=priority_actions,
            optimization_recommendations=optimization_recommendations,
            resource_recommendations=resource_recommendations,
            projected_improvements=projected_improvements,
            risk_assessment=risk_assessment,
            confidence_level=0.88,
            data_quality_score=82.5
        )
        
        return result.dict()
    
    async def _analyze_technical_issues(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ технических проблем"""
        technical_issues = self._generate_technical_issues(data)
        health_score = self._calculate_issues_health_score(technical_issues)
        
        return {
            "operations_health_score": health_score,
            "total_issues": len(technical_issues),
            "issues_analysis": technical_issues,
            "priority_issues": [i for i in technical_issues if i.get('severity') in ['critical', 'high']],
            "confidence_level": 0.90
        }
    
    async def _analyze_core_web_vitals(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ Core Web Vitals"""
        cwv_metrics = self._generate_cwv_metrics(data)
        cwv_health = self._calculate_cwv_health_score(cwv_metrics)
        
        return {
            "operations_health_score": cwv_health,
            "cwv_metrics": cwv_metrics,
            "cwv_recommendations": self._generate_cwv_recommendations(cwv_metrics),
            "confidence_level": 0.85
        }
    
    async def _manage_technical_projects(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Управление техническими проектами"""
        project_status = self._generate_project_status(data)
        project_health = self._calculate_project_health_score(project_status)
        
        return {
            "operations_health_score": project_health,
            "project_status": project_status,
            "project_recommendations": self._generate_project_recommendations(project_status),
            "confidence_level": 0.82
        }
    
    async def _analyze_team_performance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ производительности команды"""
        team_performance = self._analyze_team_performance_internal(data)
        team_health = self._calculate_team_health_score(team_performance)
        
        return {
            "operations_health_score": team_health,
            "team_performance": team_performance,
            "team_recommendations": self._generate_team_recommendations(team_performance),
            "confidence_level": 0.80
        }
    
    # =================================================================
    # MOCK DATA GENERATION METHODS
    # =================================================================
    
    def _generate_technical_issues(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерация технических проблем (mock данные)"""
        
        if "technical_issues" in data:
            return data["technical_issues"]
        
        # Mock технические проблемы
        mock_issues = [
            {
                "issue_id": "TECH-001",
                "issue_type": "core_web_vitals",
                "severity": "high",
                "title": "LCP превышает 4 секунды на мобильных устройствах",
                "description": "Медленная загрузка основного контента на мобильных устройствах",
                "affected_pages_count": 1250,
                "traffic_impact": 0.35,
                "ranking_impact": 0.25,
                "solution_priority": 9,
                "estimated_fix_time": 72
            },
            {
                "issue_id": "TECH-002", 
                "issue_type": "crawling",
                "severity": "critical",
                "title": "Robots.txt блокирует важные разделы сайта",
                "description": "Роботы поисковых систем не могут получить доступ к категорийным страницам",
                "affected_pages_count": 850,
                "traffic_impact": 0.60,
                "ranking_impact": 0.45,
                "solution_priority": 10,
                "estimated_fix_time": 24
            },
            {
                "issue_id": "TECH-003",
                "issue_type": "structured_data",
                "severity": "medium",
                "title": "Отсутствует Schema.org разметка для продуктов",
                "description": "Нет микроданных для товарных страниц, что снижает видимость в расширенных сниппетах",
                "affected_pages_count": 3200,
                "traffic_impact": 0.15,
                "ranking_impact": 0.10,
                "solution_priority": 6,
                "estimated_fix_time": 48
            },
            {
                "issue_id": "TECH-004",
                "issue_type": "mobile_optimization",
                "severity": "high",
                "title": "Проблемы с мобильной адаптивностью",
                "description": "Контент не помещается на экранах мобильных устройств",
                "affected_pages_count": 680,
                "traffic_impact": 0.40,
                "ranking_impact": 0.30,
                "solution_priority": 8,
                "estimated_fix_time": 96
            },
            {
                "issue_id": "TECH-005",
                "issue_type": "indexing",
                "severity": "medium",
                "title": "Дублированные страницы без canonical",
                "description": "Обнаружены дублированные страницы без правильной canonical разметки",
                "affected_pages_count": 420,
                "traffic_impact": 0.20,
                "ranking_impact": 0.15,
                "solution_priority": 7,
                "estimated_fix_time": 36
            }
        ]
        
        return mock_issues
    
    def _generate_cwv_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация метрик Core Web Vitals"""
        
        if "cwv_metrics" in data:
            return data["cwv_metrics"]
        
        # Mock CWV данные
        return {
            "mobile": {
                "lcp_score": 3.8,
                "fid_score": 145,
                "cls_score": 0.18,
                "fcp_score": 2.2,
                "ttfb_score": 720,
                "lcp_rating": "needs-improvement",
                "fid_rating": "needs-improvement", 
                "cls_rating": "needs-improvement",
                "sample_size": 5000,
                "measurement_date": datetime.now().isoformat()
            },
            "desktop": {
                "lcp_score": 2.1,
                "fid_score": 85,
                "cls_score": 0.08,
                "fcp_score": 1.4,
                "ttfb_score": 480,
                "lcp_rating": "good",
                "fid_rating": "good",
                "cls_rating": "good", 
                "sample_size": 2000,
                "measurement_date": datetime.now().isoformat()
            }
        }
    
    def _generate_project_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация статуса проектов"""
        
        if "project_status" in data:
            return data["project_status"]
        
        return {
            "active_projects": 8,
            "on_schedule": 5,
            "delayed": 2,
            "completed_this_month": 3,
            "projects_by_type": {
                "core_web_vitals_optimization": 3,
                "site_migration": 1,
                "mobile_optimization": 2,
                "structured_data_implementation": 2
            },
            "resource_utilization": {
                "frontend_developers": 0.85,
                "backend_developers": 0.75,
                "seo_specialists": 0.90
            }
        }
    
    def _analyze_team_performance_internal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ производительности команды"""
        
        if "team_performance" in data:
            return data["team_performance"]
        
        return {
            "utilization": 0.82,
            "avg_resolution_time": 54.5,  # hours
            "issues_resolved_this_month": 23,
            "projects_delivered_on_time": 0.75,
            "team_satisfaction": 8.2,  # out of 10
            "skill_gaps": ["JavaScript performance optimization", "Advanced Schema.org"],
            "productivity_trend": "improving",
            "top_performers": ["Анна Смирнова", "Дмитрий Козлов"],
            "areas_for_improvement": ["Automation skills", "Performance monitoring"]
        }
    
    # =================================================================
    # CALCULATION METHODS
    # =================================================================
    
    def _calculate_operations_health(self, issues, cwv_metrics, project_status, team_performance) -> float:
        """Расчет общего здоровья технических операций"""
        
        # Веса различных компонентов
        weights = {
            "issues": 0.35,
            "cwv": 0.25,
            "projects": 0.25,
            "team": 0.15
        }
        
        # Расчет скоров по компонентам
        issues_score = self._calculate_issues_health_score(issues)
        cwv_score = self._calculate_cwv_health_score(cwv_metrics)
        project_score = self._calculate_project_health_score(project_status)
        team_score = self._calculate_team_health_score(team_performance)
        
        # Взвешенный итоговый скор
        health_score = (
            issues_score * weights["issues"] +
            cwv_score * weights["cwv"] +
            project_score * weights["projects"] +
            team_score * weights["team"]
        )
        
        return round(min(health_score, 100), 1)
    
    def _calculate_issues_health_score(self, issues: List[Dict[str, Any]]) -> float:
        """Расчет скора здоровья на основе технических проблем"""
        
        if not issues:
            return 95.0  # Отлично, если нет проблем
        
        # Базовый скор
        base_score = 100.0
        
        # Штрафы за проблемы по серьезности
        for issue in issues:
            severity = issue.get('severity', 'medium')
            affected_pages = issue.get('affected_pages_count', 0)
            traffic_impact = issue.get('traffic_impact', 0.1)
            
            # Базовый штраф по серьезности
            severity_penalty = self.issue_severity_weights.get(severity, 2)
            
            # Дополнительный штраф за масштаб
            scale_multiplier = min(affected_pages / 1000, 2.0)  # Максимум x2
            impact_multiplier = 1 + traffic_impact
            
            total_penalty = severity_penalty * scale_multiplier * impact_multiplier
            base_score -= total_penalty
        
        return max(base_score, 20.0)  # Минимум 20
    
    def _calculate_cwv_health_score(self, cwv_metrics: Dict[str, Any]) -> float:
        """Расчет скора Core Web Vitals"""
        
        mobile_metrics = cwv_metrics.get('mobile', {})
        desktop_metrics = cwv_metrics.get('desktop', {})
        
        # Мобильные метрики важнее (70% веса)
        mobile_score = self._score_device_cwv(mobile_metrics) * 0.7
        desktop_score = self._score_device_cwv(desktop_metrics) * 0.3
        
        return round(mobile_score + desktop_score, 1)
    
    def _score_device_cwv(self, metrics: Dict[str, Any]) -> float:
        """Скоринг CWV для конкретного устройства"""
        
        if not metrics:
            return 50.0
        
        lcp_score = self._score_lcp(metrics.get('lcp_score', 5.0))
        fid_score = self._score_fid(metrics.get('fid_score', 300))
        cls_score = self._score_cls(metrics.get('cls_score', 0.3))
        
        # Равные веса для всех метрик
        return (lcp_score + fid_score + cls_score) / 3
    
    def _score_lcp(self, lcp_value: float) -> float:
        """Скоринг LCP"""
        if lcp_value <= 2.5:
            return 100.0
        elif lcp_value <= 4.0:
            return 100 - ((lcp_value - 2.5) / 1.5) * 40  # Линейное снижение до 60
        else:
            return max(20, 60 - ((lcp_value - 4.0) * 10))  # Быстрое снижение
    
    def _score_fid(self, fid_value: float) -> float:
        """Скоринг FID"""
        if fid_value <= 100:
            return 100.0
        elif fid_value <= 300:
            return 100 - ((fid_value - 100) / 200) * 40  # До 60
        else:
            return max(20, 60 - ((fid_value - 300) / 50))
    
    def _score_cls(self, cls_value: float) -> float:
        """Скоринг CLS"""
        if cls_value <= 0.1:
            return 100.0
        elif cls_value <= 0.25:
            return 100 - ((cls_value - 0.1) / 0.15) * 40  # До 60
        else:
            return max(20, 60 - (cls_value - 0.25) * 100)
    
    def _calculate_project_health_score(self, project_status: Dict[str, Any]) -> float:
        """Расчет скора проектов"""
        
        active = project_status.get('active_projects', 0)
        on_schedule = project_status.get('on_schedule', 0)
        delayed = project_status.get('delayed', 0)
        
        if active == 0:
            return 80.0  # Средний скор если нет активных проектов
        
        # Процент проектов в срок
        on_time_rate = on_schedule / active if active > 0 else 0
        delay_penalty = (delayed / active) * 30 if active > 0 else 0
        
        base_score = 100
        score = base_score * on_time_rate - delay_penalty
        
        return max(score, 30.0)
    
    def _calculate_team_health_score(self, team_performance: Dict[str, Any]) -> float:
        """Расчет скора команды"""
        
        utilization = team_performance.get('utilization', 0.5)
        resolution_time = team_performance.get('avg_resolution_time', 72)
        on_time_delivery = team_performance.get('projects_delivered_on_time', 0.5)
        satisfaction = team_performance.get('team_satisfaction', 5.0)
        
        # Нормализация метрик
        util_score = min(utilization * 100, 100)  # Идеальная утилизация = 100%
        time_score = max(100 - (resolution_time - 24) / 2, 20)  # Штраф за долгое решение
        delivery_score = on_time_delivery * 100
        satisfaction_score = (satisfaction / 10) * 100
        
        # Взвешенный скор
        team_score = (
            util_score * 0.3 +
            time_score * 0.3 +
            delivery_score * 0.25 +
            satisfaction_score * 0.15
        )
        
        return round(team_score, 1)
    
    # =================================================================
    # ANALYSIS METHODS
    # =================================================================
    
    def _categorize_issues_by_type(self, issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Категоризация проблем по типам"""
        
        categories = {}
        for issue in issues:
            issue_type = issue.get('issue_type', 'unknown')
            categories[issue_type] = categories.get(issue_type, 0) + 1
        
        return categories
    
    def _summarize_cwv_metrics(self, cwv_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Суммарный анализ CWV метрик"""
        
        mobile = cwv_metrics.get('mobile', {})
        desktop = cwv_metrics.get('desktop', {})
        
        return {
            "mobile_performance": {
                "lcp_rating": mobile.get('lcp_rating', 'unknown'),
                "fid_rating": mobile.get('fid_rating', 'unknown'),
                "cls_rating": mobile.get('cls_rating', 'unknown'),
                "overall_rating": self._determine_overall_cwv_rating(mobile)
            },
            "desktop_performance": {
                "lcp_rating": desktop.get('lcp_rating', 'unknown'),
                "fid_rating": desktop.get('fid_rating', 'unknown'),
                "cls_rating": desktop.get('cls_rating', 'unknown'),
                "overall_rating": self._determine_overall_cwv_rating(desktop)
            },
            "priority_improvements": self._identify_cwv_priorities(mobile, desktop)
        }
    
    def _determine_overall_cwv_rating(self, metrics: Dict[str, Any]) -> str:
        """Определение общего рейтинга CWV"""
        
        ratings = [
            metrics.get('lcp_rating', 'poor'),
            metrics.get('fid_rating', 'poor'),
            metrics.get('cls_rating', 'poor')
        ]
        
        if all(r == 'good' for r in ratings):
            return 'good'
        elif any(r == 'poor' for r in ratings):
            return 'poor'
        else:
            return 'needs-improvement'
    
    def _analyze_cwv_trends(self, cwv_metrics: Dict[str, Any]) -> Dict[str, List[float]]:
        """Анализ трендов CWV (mock данные)"""
        
        # Mock тренды за последние 30 дней
        return {
            "lcp_trend": [4.2, 4.0, 3.9, 3.8, 3.8, 3.7, 3.8],  # Улучшение
            "fid_trend": [180, 165, 155, 150, 145, 145, 145],   # Стабилизация
            "cls_trend": [0.22, 0.20, 0.19, 0.18, 0.18, 0.18, 0.18]  # Стабильно
        }
    
    # =================================================================
    # RECOMMENDATION ENGINES
    # =================================================================
    
    def _generate_priority_actions(self, issues, cwv_metrics, project_status) -> List[str]:
        """Генерация приоритетных действий"""
        
        actions = []
        
        # Действия на основе критических проблем
        critical_issues = [i for i in issues if i.get('severity') == 'critical']
        if critical_issues:
            actions.append(f"Немедленно исправить {len(critical_issues)} критических проблем")
        
        # Действия на основе CWV
        mobile_cwv = cwv_metrics.get('mobile', {})
        if mobile_cwv.get('lcp_rating') == 'poor':
            actions.append("Оптимизировать LCP на мобильных устройствах")
        
        # Действия на основе проектов
        delayed_projects = project_status.get('delayed', 0)
        if delayed_projects > 0:
            actions.append(f"Пересмотреть планы {delayed_projects} задержанных проектов")
        
        # Общие действия
        actions.extend([
            "Провести аудит производительности команды",
            "Обновить процессы мониторинга технических метрик",
            "Внедрить автоматизированные проверки качества"
        ])
        
        return actions[:5]  # Топ 5 действий
    
    def _generate_optimization_recommendations(self, issues, cwv_metrics, team_performance) -> List[str]:
        """Генерация рекомендаций по оптимизации"""
        
        recommendations = []
        
        # Рекомендации на основе типов проблем
        issue_types = self._categorize_issues_by_type(issues)
        
        if issue_types.get('core_web_vitals', 0) > 0:
            recommendations.append("Внедрить continuous monitoring Core Web Vitals")
            recommendations.append("Оптимизировать изображения и использовать современные форматы")
        
        if issue_types.get('crawling', 0) > 0:
            recommendations.append("Настроить автоматические проверки robots.txt и sitemap")
        
        # Рекомендации на основе CWV
        mobile_cwv = cwv_metrics.get('mobile', {})
        if mobile_cwv.get('cls_rating') in ['poor', 'needs-improvement']:
            recommendations.append("Зарезервировать пространство для динамического контента")
        
        # Рекомендации на основе команды
        if team_performance.get('avg_resolution_time', 0) > 60:
            recommendations.append("Автоматизировать routine технические проверки")
            recommendations.append("Создать knowledge base для частых проблем")
        
        # Общие рекомендации
        recommendations.extend([
            "Внедрить Real User Monitoring (RUM)",
            "Создать performance budget для новых функций",
            "Регулярно проводить technical debt review"
        ])
        
        return recommendations
    
    def _generate_resource_recommendations(self, team_performance, project_status) -> List[str]:
        """Генерация рекомендаций по ресурсам"""
        
        recommendations = []
        
        utilization = team_performance.get('utilization', 0.5)
        skill_gaps = team_performance.get('skill_gaps', [])
        
        if utilization > 0.9:
            recommendations.append("Рассмотреть найм дополнительных технических специалистов")
        elif utilization < 0.6:
            recommendations.append("Перераспределить ресурсы на другие проекты")
        
        if skill_gaps:
            recommendations.append(f"Организовать обучение по: {', '.join(skill_gaps[:2])}")
        
        delayed_projects = project_status.get('delayed', 0)
        if delayed_projects > 2:
            recommendations.append("Провести анализ capacity planning")
        
        recommendations.extend([
            "Внедрить cross-training между членами команды",
            "Создать emergency response team для критических проблем"
        ])
        
        return recommendations
    
    def _project_improvements(self, issues, cwv_metrics) -> Dict[str, float]:
        """Прогнозирование улучшений"""
        
        return {
            "expected_cwv_improvement": 15.0,  # % улучшение CWV
            "expected_issue_reduction": 40.0,  # % сокращение проблем
            "expected_performance_gain": 25.0,  # % улучшение производительности
            "timeline_weeks": 8.0  # Временные рамки
        }
    
    def _assess_risks(self, issues, project_status) -> List[str]:
        """Оценка рисков"""
        
        risks = []
        
        critical_count = len([i for i in issues if i.get('severity') == 'critical'])
        if critical_count > 2:
            risks.append("Высокий риск негативного влияния на SEO из-за критических проблем")
        
        delayed_projects = project_status.get('delayed', 0)
        if delayed_projects > 1:
            risks.append("Риск дальнейшего срыва дедлайнов по проектам")
        
        risks.extend([
            "Возможное снижение Core Web Vitals при росте трафика",
            "Риск потери квалифицированных специалистов"
        ])
        
        return risks
    
    def _generate_cwv_recommendations(self, cwv_metrics) -> List[str]:
        """Рекомендации по улучшению CWV"""
        
        recommendations = []
        mobile = cwv_metrics.get('mobile', {})
        
        if mobile.get('lcp_score', 0) > 2.5:
            recommendations.extend([
                "Оптимизировать server response time",
                "Внедрить preloading для критических ресурсов",
                "Оптимизировать изображения hero-секции"
            ])
        
        if mobile.get('fid_score', 0) > 100:
            recommendations.extend([
                "Уменьшить JavaScript execution time",
                "Внедрить code splitting",
                "Оптимизировать third-party scripts"
            ])
        
        if mobile.get('cls_score', 0) > 0.1:
            recommendations.extend([
                "Зарезервировать размеры для изображений",
                "Избегать динамической вставки контента",
                "Оптимизировать web fonts loading"
            ])
        
        return recommendations
    
    def _generate_project_recommendations(self, project_status) -> List[str]:
        """Рекомендации по управлению проектами"""
        
        recommendations = []
        
        if project_status.get('delayed', 0) > 0:
            recommendations.extend([
                "Пересмотреть scope задержанных проектов",
                "Провести retrospective анализ причин задержек",
                "Улучшить estimation процессы"
            ])
        
        utilization = project_status.get('resource_utilization', {})
        for role, util in utilization.items():
            if util > 0.9:
                recommendations.append(f"Снизить нагрузку на {role}")
        
        return recommendations
    
    def _generate_team_recommendations(self, team_performance) -> List[str]:
        """Рекомендации по команде"""
        
        recommendations = []
        
        if team_performance.get('team_satisfaction', 5) < 7:
            recommendations.append("Провести survey для выявления проблем в команде")
        
        if team_performance.get('productivity_trend') == 'declining':
            recommendations.append("Анализировать bottlenecks в процессах")
        
        skill_gaps = team_performance.get('skill_gaps', [])
        if skill_gaps:
            recommendations.append(f"Организовать тренинги по {skill_gaps[0]}")
        
        return recommendations
    
    def _identify_cwv_priorities(self, mobile, desktop) -> List[str]:
        """Определение приоритетов улучшения CWV"""
        
        priorities = []
        
        # Проверяем мобильные метрики (приоритет)
        if mobile.get('lcp_rating') == 'poor':
            priorities.append("LCP оптимизация (мобильные)")
        if mobile.get('fid_rating') == 'poor':
            priorities.append("FID оптимизация (мобильные)")
        if mobile.get('cls_rating') == 'poor':
            priorities.append("CLS оптимизация (мобильные)")
        
        # Десктоп метрики
        if desktop.get('lcp_rating') == 'poor':
            priorities.append("LCP оптимизация (десктоп)")
        
        return priorities[:3]  # Топ 3 приоритета
    
    def _extract_key_insights(self, result: Dict[str, Any]) -> List[str]:
        """Извлечение ключевых инсайтов"""
        
        insights = []
        
        health_score = result.get("operations_health_score", 0)
        if health_score >= 85:
            insights.append(f"Отличное состояние технических операций ({health_score}%)")
        elif health_score >= 70:
            insights.append(f"Хорошее состояние с возможностями для улучшения ({health_score}%)")
        else:
            insights.append(f"Требуется внимание к техническим операциям ({health_score}%)")
        
        # Инсайты по CWV
        cwv_summary = result.get("cwv_summary", {})
        mobile_rating = cwv_summary.get("mobile_performance", {}).get("overall_rating")
        if mobile_rating:
            insights.append(f"Мобильная производительность: {mobile_rating}")
        
        # Инсайты по проектам
        active_projects = result.get("active_projects", 0)
        delayed_projects = result.get("projects_delayed", 0)
        if delayed_projects > 0:
            insights.append(f"{delayed_projects} из {active_projects} проектов имеют задержки")
        
        return insights