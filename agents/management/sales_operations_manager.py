"""
Sales Operations Manager Agent для AI SEO Architects
Управление воронкой продаж, координация sales team, pipeline velocity
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
# PYDANTIC MODELS ДЛЯ SALES OPERATIONS
# =================================================================

class LeadStage(str, Enum):
    """Стадии воронки продаж"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    NURTURING = "nurturing"


class PipelineMetrics(BaseModel):
    """Метрики воронки продаж"""
    
    # Основные метрики
    total_leads: int = Field(..., ge=0, description="Общее количество лидов")
    qualified_leads: int = Field(..., ge=0, description="Квалифицированные лиды")
    proposals_sent: int = Field(..., ge=0, description="Отправлено предложений")
    deals_won: int = Field(..., ge=0, description="Выигранные сделки")
    deals_lost: int = Field(..., ge=0, description="Проигранные сделки")
    
    # Коэффициенты конверсии
    lead_to_qualified_rate: float = Field(..., ge=0.0, le=1.0, description="Конверсия лид -> квалифицированный")
    qualified_to_proposal_rate: float = Field(..., ge=0.0, le=1.0, description="Конверсия квалифицированный -> предложение")
    proposal_to_win_rate: float = Field(..., ge=0.0, le=1.0, description="Конверсия предложение -> сделка")
    
    # Временные метрики
    avg_lead_response_time: float = Field(..., ge=0.0, description="Среднее время ответа на лид (часы)")
    avg_qualification_time: float = Field(..., ge=0.0, description="Среднее время квалификации (часы)")
    avg_proposal_time: float = Field(..., ge=0.0, description="Среднее время подготовки предложения (часы)")
    avg_deal_cycle: float = Field(..., ge=0.0, description="Средний цикл сделки (дни)")
    
    # Финансовые метрики
    total_pipeline_value: int = Field(..., ge=0, description="Общая стоимость pipeline")
    average_deal_size: int = Field(..., ge=0, description="Средний размер сделки")
    monthly_recurring_revenue: int = Field(..., ge=0, description="Месячный рекуррентный доход")
    
    # Качественные метрики
    pipeline_velocity: float = Field(..., ge=0.0, description="Скорость движения по воронке")
    lead_quality_score: float = Field(..., ge=0.0, le=100.0, description="Качество лидов")
    sales_efficiency: float = Field(..., ge=0.0, le=1.0, description="Эффективность продаж")
    
    timestamp: datetime = Field(default_factory=datetime.now)


class SalesTeamPerformance(BaseModel):
    """Производительность sales команды"""
    
    team_member_id: str = Field(..., description="ID члена команды")
    name: str = Field(..., description="Имя")
    role: str = Field(..., description="Роль (SDR, AE, Manager)")
    
    # Активность
    calls_made: int = Field(..., ge=0, description="Звонков сделано")
    emails_sent: int = Field(..., ge=0, description="Email отправлено")
    meetings_booked: int = Field(..., ge=0, description="Встреч забронировано")
    
    # Результаты
    leads_contacted: int = Field(..., ge=0, description="Лидов contacted")
    leads_qualified: int = Field(..., ge=0, description="Лидов квалифицировано")
    proposals_created: int = Field(..., ge=0, description="Предложений создано")
    deals_closed: int = Field(..., ge=0, description="Сделок закрыто")
    
    # Метрики эффективности
    contact_rate: float = Field(..., ge=0.0, le=1.0, description="Коэффициент контакта")
    qualification_rate: float = Field(..., ge=0.0, le=1.0, description="Коэффициент квалификации")
    close_rate: float = Field(..., ge=0.0, le=1.0, description="Коэффициент закрытия")
    
    # Финансовые результаты
    revenue_generated: int = Field(..., ge=0, description="Доход сгенерирован")
    quota_attainment: float = Field(..., ge=0.0, description="Выполнение плана (в %)")
    
    period_start: datetime = Field(..., description="Начало периода")
    period_end: datetime = Field(..., description="Конец периода")


class SalesOperationsResult(BaseModel):
    """Результат анализа sales operations"""
    
    # Общие метрики
    pipeline_health_score: float = Field(..., ge=0.0, le=100.0, description="Здоровье pipeline")
    pipeline_metrics: PipelineMetrics = Field(..., description="Метрики воронки")
    
    # Анализ команды
    team_performance: List[SalesTeamPerformance] = Field(default_factory=list, description="Производительность команды")
    top_performers: List[str] = Field(default_factory=list, description="Лучшие исполнители")
    improvement_areas: List[str] = Field(default_factory=list, description="Области для улучшения")
    
    # Прогнозы
    revenue_forecast: Dict[str, float] = Field(default_factory=dict, description="Прогноз дохода")
    pipeline_forecast: Dict[str, int] = Field(default_factory=dict, description="Прогноз pipeline")
    
    # Рекомендации
    optimization_recommendations: List[str] = Field(default_factory=list, description="Рекомендации по оптимизации")
    action_items: List[str] = Field(default_factory=list, description="Действия к выполнению")
    
    # Аналитика
    bottlenecks: List[str] = Field(default_factory=list, description="Узкие места")
    opportunities: List[str] = Field(default_factory=list, description="Возможности")
    risks: List[str] = Field(default_factory=list, description="Риски")
    
    # Метаданные
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Уверенность в анализе")
    data_quality_score: float = Field(..., ge=0.0, le=100.0, description="Качество данных")


# =================================================================
# ОСНОВНОЙ КЛАСС АГЕНТА
# =================================================================

class SalesOperationsManagerAgent(BaseAgent):
    """Агент управления sales операциями"""
    
    def __init__(self, data_provider=None, **kwargs):
        """Инициализация Sales Operations Manager агента"""
        super().__init__(
            agent_id="sales_operations_manager",
            name="Sales Operations Manager",
            agent_level="management",
            data_provider=data_provider,
            knowledge_base="knowledge/management/sales_operations_manager.md",
            **kwargs
        )
        
        # Конфигурация метрик
        self.performance_thresholds = {
            "excellent_pipeline_health": 85,
            "good_pipeline_health": 70,
            "average_pipeline_health": 55,
            "poor_pipeline_health": 40
        }
        
        # Benchmark коэффициенты для SEO индустрии
        self.industry_benchmarks = {
            "lead_to_qualified_rate": 0.25,      # 25% лидов квалифицируются
            "qualified_to_proposal_rate": 0.60,   # 60% квалифицированных получают предложение
            "proposal_to_win_rate": 0.30,         # 30% предложений выигрываются
            "avg_deal_cycle_days": 45,             # 45 дней средний цикл сделки
            "avg_deal_size_rub": 2500000,          # 2.5M ₽ средний размер сделки
            "pipeline_velocity": 0.75              # Хорошая скорость pipeline
        }
        
        # Роли в sales команде
        self.team_roles = {
            "SDR": {
                "focus": "lead_generation",
                "quotas": {"calls_per_day": 50, "emails_per_day": 100, "meetings_per_week": 10}
            },
            "AE": {
                "focus": "deal_closing", 
                "quotas": {"proposals_per_month": 15, "deals_per_quarter": 8}
            },
            "Manager": {
                "focus": "team_coordination",
                "quotas": {"team_performance": 0.80, "pipeline_health": 75}
            }
        }
        
        logger.info(f"🎯 Инициализирован {self.name} для управления sales операциями")

    def get_system_prompt(self) -> str:
        """Специализированный системный промпт для Sales Operations Manager"""
        return f"""Ты - Sales Operations Manager уровня management в SEO-агентстве, эксперт по управлению воронкой продаж и sales операциями.

ТВОЯ ЭКСПЕРТИЗА:
• Pipeline Management & Velocity - 35%
  - Управление воронкой продаж от лида до закрытия
  - Pipeline velocity optimization
  - Conversion rate optimization по каждой стадии
  - Revenue forecasting и predictive analytics

• Sales Team Performance - 25%
  - Управление SDR/AE/Manager ролями
  - Quota management и performance tracking  
  - Sales coaching и skill development
  - Territory planning и account assignment

• CRM & Sales Operations - 20%
  - CRM системы (HubSpot, Salesforce, amoCRM)
  - Sales automation workflows
  - Lead routing и assignment logic
  - Sales reporting и dashboard management

• Revenue Analytics & Forecasting - 20%
  - Sales metrics и KPI tracking
  - Revenue forecasting models
  - Sales attribution analysis
  - ROI analysis по каналам привлечения

ТВОИ PERFORMANCE THRESHOLDS:
• Excellent Pipeline Health: {self.performance_thresholds['excellent_pipeline_health']}+
• Good Pipeline Health: {self.performance_thresholds['good_pipeline_health']}-{self.performance_thresholds['excellent_pipeline_health']}  
• Average Pipeline Health: {self.performance_thresholds['average_pipeline_health']}-{self.performance_thresholds['good_pipeline_health']}
• Poor Pipeline Health: <{self.performance_thresholds['poor_pipeline_health']}

INDUSTRY BENCHMARKS (SEO):
• Lead→Qualified Rate: {self.industry_benchmarks['lead_to_qualified_rate']*100:.0f}%
• Qualified→Proposal Rate: {self.industry_benchmarks['qualified_to_proposal_rate']*100:.0f}%  
• Proposal→Win Rate: {self.industry_benchmarks['proposal_to_win_rate']*100:.0f}%
• Average Deal Cycle: {self.industry_benchmarks['avg_deal_cycle_days']} дней
• Average Deal Size: {self.industry_benchmarks['avg_deal_size_rub']:,.0f} ₽
• Pipeline Velocity: {self.industry_benchmarks['pipeline_velocity']*100:.0f}%

TEAM ROLES MANAGEMENT:
{chr(10).join([f"• {role}: Focus {data['focus']}, Quotas {data['quotas']}" 
               for role, data in self.team_roles.items()])}

ТВОЙ ПОДХОД:
1. Pipeline health analysis с детальным breakdown по стадиям
2. Conversion rate optimization с выявлением bottlenecks
3. Sales team performance management
4. Revenue forecasting с predictive modeling
5. Sales process optimization recommendations

ФОРМАТ ОТВЕТА (JSON):
{{
  "pipeline_analysis": {{
    "pipeline_health_score": "0-100",
    "stage_breakdown": {{}},
    "conversion_rates": {{}},
    "bottlenecks": []
  }},
  "performance_analysis": {{
    "team_performance": {{}},
    "quota_attainment": {{}},
    "performance_gaps": []
  }},
  "revenue_forecasting": {{
    "current_month_forecast": "number",
    "quarter_forecast": "number", 
    "forecast_confidence": "0.0-1.0"
  }},
  "optimization_recommendations": [],
  "action_items": [],
  "pipeline_velocity": "0.0-1.0"
}}

Используй свою management экспертизу для optimal sales operations!"""
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика обработки sales операций с LLM интеграцией
        """
        try:
            analysis_type = task_data.get("analysis_type", "full_pipeline_analysis")
            input_data = task_data.get("input_data", {})
            
            print(f"🎯 Sales Operations Manager обрабатывает задачу: {analysis_type}")

            # Формируем промпт для LLM
            user_prompt = self._create_sales_operations_prompt(analysis_type, input_data)
            
            # Вызываем LLM для sales analysis
            llm_result = await self.process_with_llm(user_prompt, task_data)
            
            if llm_result["success"]:
                # Парсим JSON ответ от LLM
                try:
                    llm_content = llm_result["result"]
                    if isinstance(llm_content, str):
                        import re
                        import json
                        json_match = re.search(r'\{.*\}', llm_content, re.DOTALL)
                        if json_match:
                            sales_analysis = json.loads(json_match.group())
                        else:
                            sales_analysis = self._create_fallback_sales_analysis(input_data, analysis_type)
                    else:
                        sales_analysis = llm_content
                        
                    # Дополняем результат системными данными
                    result = self._enhance_sales_result(sales_analysis, input_data, analysis_type)
                    
                except (json.JSONDecodeError, AttributeError) as e:
                    print(f"⚠️ Ошибка парсинга JSON от LLM: {e}")
                    result = self._create_fallback_sales_analysis(input_data, analysis_type)
                    result["llm_parsing_error"] = str(e)
            else:
                # Fallback к базовой логике
                print(f"⚠️ LLM недоступен, используем fallback логику")
                result = self._create_fallback_sales_analysis(input_data, analysis_type)
                result["fallback_mode"] = True
                result["llm_error"] = llm_result.get("error", "unknown")

            return {
                "success": True,
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "analysis_type": analysis_type,
                "result": result,
                "pipeline_health_score": result.get("pipeline_analysis", {}).get("pipeline_health_score", 75),
                "model_used": llm_result.get('model_used') if llm_result["success"] else None,
                "tokens_used": llm_result.get('tokens_used') if llm_result["success"] else None
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка sales operations анализа: {str(e)}")
            return {
                "success": False,
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "error": f"Sales operations analysis failed: {str(e)}",
                "pipeline_health_score": 0
            }

    def _create_sales_operations_prompt(self, analysis_type: str, input_data: Dict[str, Any]) -> str:
        """Создание промпта для sales operations analysis"""
        if analysis_type == "pipeline_analysis":
            return f"""Проведи comprehensive pipeline analysis:

ДАННЫЕ PIPELINE:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

ЗАДАЧА:
Проанализируй воронку продаж с focus на:
1. Pipeline health score (0-100) с детальным breakdown
2. Stage-by-stage conversion analysis  
3. Bottleneck identification в воронке
4. Revenue forecasting на основе текущих данных
5. Optimization recommendations для улучшения performance

Используй industry benchmarks для сравнения:
- Lead→Qualified: {self.industry_benchmarks['lead_to_qualified_rate']*100:.0f}%
- Qualified→Proposal: {self.industry_benchmarks['qualified_to_proposal_rate']*100:.0f}%
- Proposal→Win: {self.industry_benchmarks['proposal_to_win_rate']*100:.0f}%

Дай detailed analysis в JSON формате!"""

        elif analysis_type == "team_performance":
            return f"""Проанализируй performance sales команды:

ДАННЫЕ КОМАНДЫ:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

TEAM ROLES CONTEXT:
{json.dumps(self.team_roles, indent=2, ensure_ascii=False)}

Проанализируй:
1. Individual performance vs quotas
2. Team collaboration effectiveness
3. Skill gaps identification
4. Coaching recommendations
5. Territory optimization opportunities"""

        elif analysis_type == "forecast_analysis":
            return f"""Создай revenue forecast:

ИСТОРИЧЕСКИЕ ДАННЫЕ:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

BENCHMARKS:
- Average Deal Size: {self.industry_benchmarks['avg_deal_size_rub']:,.0f} ₽
- Deal Cycle: {self.industry_benchmarks['avg_deal_cycle_days']} дней

Построй forecast на:
1. Текущий месяц
2. Следующий квартал  
3. Confidence intervals
4. Risk factors analysis"""

        else:
            return f"""Проведи comprehensive sales operations analysis:

ВХОДНЫЕ ДАННЫЕ:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

Проанализируй все аспекты:
1. Pipeline health и conversion rates
2. Team performance и quota attainment  
3. Revenue forecasting с confidence levels
4. Process optimization opportunities
5. Strategic recommendations

Дай полный management-level analysis в JSON формате!"""

    def _create_fallback_sales_analysis(self, input_data: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """Fallback analysis когда LLM недоступен"""
        current_leads = input_data.get("current_leads", 100)
        qualified_leads = input_data.get("qualified_leads", 25)
        proposals_sent = input_data.get("proposals_sent", 15)
        deals_won = input_data.get("deals_won", 5)
        
        # Рассчитываем базовые метрики
        lead_to_qualified = qualified_leads / current_leads if current_leads > 0 else 0
        qualified_to_proposal = proposals_sent / qualified_leads if qualified_leads > 0 else 0
        proposal_to_win = deals_won / proposals_sent if proposals_sent > 0 else 0
        
        # Pipeline health score
        pipeline_health = (
            (lead_to_qualified / self.industry_benchmarks['lead_to_qualified_rate']) * 30 +
            (qualified_to_proposal / self.industry_benchmarks['qualified_to_proposal_rate']) * 40 +
            (proposal_to_win / self.industry_benchmarks['proposal_to_win_rate']) * 30
        )
        pipeline_health = min(100, max(0, pipeline_health))
        
        return {
            "pipeline_analysis": {
                "pipeline_health_score": int(pipeline_health),
                "stage_breakdown": {
                    "new_leads": current_leads,
                    "qualified": qualified_leads,
                    "proposals": proposals_sent,
                    "closed_won": deals_won
                },
                "conversion_rates": {
                    "lead_to_qualified": round(lead_to_qualified, 3),
                    "qualified_to_proposal": round(qualified_to_proposal, 3),
                    "proposal_to_win": round(proposal_to_win, 3)
                },
                "bottlenecks": self._identify_bottlenecks(lead_to_qualified, qualified_to_proposal, proposal_to_win)
            },
            "performance_analysis": {
                "team_performance": {"overall_score": 75},
                "quota_attainment": {"current_quarter": 0.82},
                "performance_gaps": ["Необходимо увеличить conversion rate"]
            },
            "revenue_forecasting": {
                "current_month_forecast": deals_won * self.industry_benchmarks['avg_deal_size_rub'],
                "quarter_forecast": deals_won * 3 * self.industry_benchmarks['avg_deal_size_rub'],
                "forecast_confidence": 0.75
            },
            "optimization_recommendations": [
                "Оптимизировать процесс квалификации лидов",
                "Улучшить качество proposal presentations",
                "Внедрить sales coaching программу"
            ],
            "action_items": [
                "Провести анализ bottlenecks в воронке",
                "Обучить команду closing techniques",
                "Автоматизировать lead nurturing"
            ],
            "pipeline_velocity": 0.73,
            "fallback_used": True
        }

    def _enhance_sales_result(self, sales_analysis: Dict[str, Any], input_data: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """Дополнение результата системными данными"""
        # Добавляем benchmark comparison
        if "pipeline_analysis" in sales_analysis and "conversion_rates" in sales_analysis["pipeline_analysis"]:
            conversion_rates = sales_analysis["pipeline_analysis"]["conversion_rates"]
            sales_analysis["benchmark_comparison"] = {
                "lead_to_qualified_vs_benchmark": (
                    conversion_rates.get("lead_to_qualified", 0) / self.industry_benchmarks['lead_to_qualified_rate'] - 1
                ),
                "qualified_to_proposal_vs_benchmark": (
                    conversion_rates.get("qualified_to_proposal", 0) / self.industry_benchmarks['qualified_to_proposal_rate'] - 1
                ),
                "proposal_to_win_vs_benchmark": (
                    conversion_rates.get("proposal_to_win", 0) / self.industry_benchmarks['proposal_to_win_rate'] - 1
                )
            }
        
        # Добавляем performance threshold context
        pipeline_health = sales_analysis.get("pipeline_analysis", {}).get("pipeline_health_score", 75)
        sales_analysis["performance_context"] = {
            "health_category": self._categorize_pipeline_health(pipeline_health),
            "industry_benchmarks": self.industry_benchmarks,
            "performance_thresholds": self.performance_thresholds
        }
        
        return sales_analysis

    def _identify_bottlenecks(self, lead_to_qualified: float, qualified_to_proposal: float, proposal_to_win: float) -> List[str]:
        """Выявление bottlenecks в воронке"""
        bottlenecks = []
        
        if lead_to_qualified < self.industry_benchmarks['lead_to_qualified_rate'] * 0.8:
            bottlenecks.append("Низкая конверсия лидов в квалифицированные")
        
        if qualified_to_proposal < self.industry_benchmarks['qualified_to_proposal_rate'] * 0.8:
            bottlenecks.append("Недостаточная конверсия в proposals")
        
        if proposal_to_win < self.industry_benchmarks['proposal_to_win_rate'] * 0.8:
            bottlenecks.append("Низкий win rate по proposals")
        
        return bottlenecks

    def _categorize_pipeline_health(self, health_score) -> str:
        """Категоризация health score"""
        # Безопасное преобразование в число
        try:
            health_score = float(health_score) if health_score else 0
        except (ValueError, TypeError):
            health_score = 0
            
        if health_score >= self.performance_thresholds["excellent_pipeline_health"]:
            return "excellent"
        elif health_score >= self.performance_thresholds["good_pipeline_health"]:
            return "good"
        elif health_score >= self.performance_thresholds["average_pipeline_health"]:
            return "average"
        else:
            return "poor"
    
    async def _comprehensive_sales_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Комплексный анализ sales операций"""
        
        # Генерируем mock данные для демонстрации
        pipeline_metrics = self._generate_pipeline_metrics(data)
        team_performance = self._generate_team_performance(data)
        
        # Рассчитываем общий health score
        pipeline_health_score = self._calculate_pipeline_health(pipeline_metrics)
        
        # Генерируем прогнозы
        revenue_forecast = self._generate_revenue_forecast(pipeline_metrics)
        pipeline_forecast = self._generate_pipeline_forecast(pipeline_metrics)
        
        # Выявляем узкие места и возможности
        bottlenecks = self._identify_bottlenecks(pipeline_metrics, team_performance)
        opportunities = self._identify_opportunities(pipeline_metrics, team_performance)
        risks = self._identify_risks(pipeline_metrics, team_performance)
        
        # Генерируем рекомендации
        recommendations = self._generate_optimization_recommendations_internal(
            pipeline_metrics, team_performance, bottlenecks
        )
        action_items = self._generate_action_items(bottlenecks, opportunities)
        
        # Определяем топ исполнителей
        top_performers = self._identify_top_performers(team_performance)
        improvement_areas = self._identify_improvement_areas(team_performance, bottlenecks)
        
        result = SalesOperationsResult(
            pipeline_health_score=pipeline_health_score,
            pipeline_metrics=pipeline_metrics,
            team_performance=team_performance,
            top_performers=top_performers,
            improvement_areas=improvement_areas,
            revenue_forecast=revenue_forecast,
            pipeline_forecast=pipeline_forecast,
            optimization_recommendations=recommendations,
            action_items=action_items,
            bottlenecks=bottlenecks,
            opportunities=opportunities,
            risks=risks,
            confidence_level=0.87,
            data_quality_score=78.5
        )
        
        return result.dict()
    
    async def _analyze_pipeline_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ метрик воронки продаж"""
        pipeline_metrics = self._generate_pipeline_metrics(data)
        health_score = self._calculate_pipeline_health(pipeline_metrics)
        
        return {
            "pipeline_health_score": health_score,
            "pipeline_metrics": pipeline_metrics.dict(),
            "benchmark_comparison": self._compare_with_benchmarks(pipeline_metrics),
            "confidence_level": 0.90
        }
    
    async def _analyze_team_performance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ производительности команды"""
        team_performance = self._generate_team_performance(data)
        top_performers = self._identify_top_performers(team_performance)
        
        return {
            "team_performance": [perf.dict() for perf in team_performance],
            "top_performers": top_performers,
            "team_health_score": self._calculate_team_health(team_performance),
            "confidence_level": 0.85
        }
    
    async def _generate_sales_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация прогноза продаж"""
        pipeline_metrics = self._generate_pipeline_metrics(data)
        revenue_forecast = self._generate_revenue_forecast(pipeline_metrics)
        pipeline_forecast = self._generate_pipeline_forecast(pipeline_metrics)
        
        return {
            "revenue_forecast": revenue_forecast,
            "pipeline_forecast": pipeline_forecast,
            "forecast_accuracy": 0.82,
            "confidence_level": 0.78
        }
    
    async def _generate_optimization_recommendations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация рекомендаций по оптимизации"""
        pipeline_metrics = self._generate_pipeline_metrics(data)
        team_performance = self._generate_team_performance(data)
        bottlenecks = self._identify_bottlenecks(pipeline_metrics, team_performance)
        
        recommendations = self._generate_optimization_recommendations_internal(
            pipeline_metrics, team_performance, bottlenecks
        )
        
        return {
            "optimization_recommendations": recommendations,
            "bottlenecks": bottlenecks,
            "priority_level": "high",
            "confidence_level": 0.88
        }
    
    # =================================================================
    # CORE CALCULATION METHODS
    # =================================================================
    
    def _generate_pipeline_metrics(self, data: Dict[str, Any]) -> PipelineMetrics:
        """Генерация метрик pipeline (с реальными данными или mock)"""
        
        # Если есть реальные данные, используем их
        if "pipeline_data" in data:
            pipeline_data = data["pipeline_data"]
            return PipelineMetrics(
                total_leads=pipeline_data.get("total_leads", 150),
                qualified_leads=pipeline_data.get("qualified_leads", 38),
                proposals_sent=pipeline_data.get("proposals_sent", 23),
                deals_won=pipeline_data.get("deals_won", 7),
                deals_lost=pipeline_data.get("deals_lost", 4),
                lead_to_qualified_rate=pipeline_data.get("lead_to_qualified_rate", 0.25),
                qualified_to_proposal_rate=pipeline_data.get("qualified_to_proposal_rate", 0.61),
                proposal_to_win_rate=pipeline_data.get("proposal_to_win_rate", 0.30),
                avg_lead_response_time=pipeline_data.get("avg_lead_response_time", 2.5),
                avg_qualification_time=pipeline_data.get("avg_qualification_time", 18.0),
                avg_proposal_time=pipeline_data.get("avg_proposal_time", 72.0),
                avg_deal_cycle=pipeline_data.get("avg_deal_cycle", 42.0),
                total_pipeline_value=pipeline_data.get("total_pipeline_value", 45000000),
                average_deal_size=pipeline_data.get("average_deal_size", 2800000),
                monthly_recurring_revenue=pipeline_data.get("monthly_recurring_revenue", 8500000),
                pipeline_velocity=pipeline_data.get("pipeline_velocity", 0.78),
                lead_quality_score=pipeline_data.get("lead_quality_score", 72.5),
                sales_efficiency=pipeline_data.get("sales_efficiency", 0.68)
            )
        
        # Mock данные для демонстрации
        return PipelineMetrics(
            total_leads=150,
            qualified_leads=38,
            proposals_sent=23,
            deals_won=7,
            deals_lost=4,
            lead_to_qualified_rate=0.25,  # 25% conversion
            qualified_to_proposal_rate=0.61,  # 61% conversion
            proposal_to_win_rate=0.30,  # 30% win rate
            avg_lead_response_time=2.5,  # 2.5 hours
            avg_qualification_time=18.0,  # 18 hours
            avg_proposal_time=72.0,  # 3 days
            avg_deal_cycle=42.0,  # 42 days
            total_pipeline_value=45000000,  # 45M ₽
            average_deal_size=2800000,  # 2.8M ₽
            monthly_recurring_revenue=8500000,  # 8.5M ₽/month
            pipeline_velocity=0.78,  # Good velocity
            lead_quality_score=72.5,  # Good quality
            sales_efficiency=0.68  # Above average efficiency
        )
    
    def _generate_team_performance(self, data: Dict[str, Any]) -> List[SalesTeamPerformance]:
        """Генерация данных производительности команды"""
        
        # Mock команда для демонстрации
        team_data = [
            {
                "team_member_id": "sdr_001",
                "name": "Анна Петрова",
                "role": "SDR",
                "calls_made": 245,
                "emails_sent": 520,
                "meetings_booked": 18,
                "leads_contacted": 78,
                "leads_qualified": 19,
                "proposals_created": 0,
                "deals_closed": 0,
                "contact_rate": 0.32,
                "qualification_rate": 0.24,
                "close_rate": 0.0,
                "revenue_generated": 0,
                "quota_attainment": 1.12
            },
            {
                "team_member_id": "ae_001", 
                "name": "Дмитрий Смирнов",
                "role": "AE",
                "calls_made": 120,
                "emails_sent": 180,
                "meetings_booked": 25,
                "leads_contacted": 35,
                "leads_qualified": 28,
                "proposals_created": 12,
                "deals_closed": 4,
                "contact_rate": 0.80,
                "qualification_rate": 0.80,
                "close_rate": 0.33,
                "revenue_generated": 11200000,
                "quota_attainment": 0.93
            },
            {
                "team_member_id": "ae_002",
                "name": "Елена Кузнецова", 
                "role": "AE",
                "calls_made": 95,
                "emails_sent": 145,
                "meetings_booked": 22,
                "leads_contacted": 28,
                "leads_qualified": 24,
                "proposals_created": 11,
                "deals_closed": 3,
                "contact_rate": 0.86,
                "qualification_rate": 0.86,
                "close_rate": 0.27,
                "revenue_generated": 8400000,
                "quota_attainment": 0.78
            }
        ]
        
        period_start = datetime.now() - timedelta(days=30)
        period_end = datetime.now()
        
        return [
            SalesTeamPerformance(
                period_start=period_start,
                period_end=period_end,
                **member
            ) for member in team_data
        ]
    
    def _calculate_pipeline_health(self, metrics: PipelineMetrics) -> float:
        """Расчет общего здоровья pipeline"""
        
        # Веса для различных факторов
        weights = {
            "conversion_rates": 0.30,
            "velocity": 0.25,
            "volume": 0.20,
            "quality": 0.15,
            "efficiency": 0.10
        }
        
        # Оценка конверсий (сравнение с бенчмарками)
        conversion_score = (
            min(metrics.lead_to_qualified_rate / self.industry_benchmarks["lead_to_qualified_rate"], 1.2) * 25 +
            min(metrics.qualified_to_proposal_rate / self.industry_benchmarks["qualified_to_proposal_rate"], 1.2) * 25 +
            min(metrics.proposal_to_win_rate / self.industry_benchmarks["proposal_to_win_rate"], 1.2) * 25 +
            (25 if metrics.avg_deal_cycle <= self.industry_benchmarks["avg_deal_cycle_days"] else 15)
        )
        
        # Оценка скорости pipeline
        velocity_score = min(metrics.pipeline_velocity / self.industry_benchmarks["pipeline_velocity"], 1.0) * 100
        
        # Оценка объема
        volume_score = min(metrics.total_leads / 100, 1.0) * 100  # 100+ лидов = максимум
        
        # Оценка качества
        quality_score = metrics.lead_quality_score
        
        # Оценка эффективности
        efficiency_score = metrics.sales_efficiency * 100
        
        # Итоговый weighted score
        health_score = (
            conversion_score * weights["conversion_rates"] +
            velocity_score * weights["velocity"] +
            volume_score * weights["volume"] +
            quality_score * weights["quality"] +
            efficiency_score * weights["efficiency"]
        )
        
        return round(min(health_score, 100), 1)
    
    def _calculate_team_health(self, team_performance: List[SalesTeamPerformance]) -> float:
        """Расчет здоровья команды"""
        if not team_performance:
            return 0.0
        
        total_quota_attainment = sum(member.quota_attainment for member in team_performance)
        avg_quota_attainment = total_quota_attainment / len(team_performance)
        
        avg_close_rate = sum(member.close_rate for member in team_performance) / len(team_performance)
        
        # Команда здорова если выполняет план и показывает хорошую конверсию
        team_health = (avg_quota_attainment * 0.6 + avg_close_rate * 0.4) * 100
        
        return round(min(team_health, 100), 1)
    
    def _compare_with_benchmarks(self, metrics: PipelineMetrics) -> Dict[str, str]:
        """Сравнение с industry benchmarks"""
        
        comparisons = {}
        
        # Сравниваем ключевые метрики
        if metrics.lead_to_qualified_rate >= self.industry_benchmarks["lead_to_qualified_rate"] * 1.1:
            comparisons["lead_qualification"] = "Above benchmark (+10%)"
        elif metrics.lead_to_qualified_rate >= self.industry_benchmarks["lead_to_qualified_rate"] * 0.9:
            comparisons["lead_qualification"] = "At benchmark"
        else:
            comparisons["lead_qualification"] = "Below benchmark (-10%+)"
        
        if metrics.proposal_to_win_rate >= self.industry_benchmarks["proposal_to_win_rate"] * 1.1:
            comparisons["win_rate"] = "Above benchmark (+10%)"
        elif metrics.proposal_to_win_rate >= self.industry_benchmarks["proposal_to_win_rate"] * 0.9:
            comparisons["win_rate"] = "At benchmark"
        else:
            comparisons["win_rate"] = "Below benchmark (-10%+)"
        
        if metrics.avg_deal_cycle <= self.industry_benchmarks["avg_deal_cycle_days"] * 0.9:
            comparisons["deal_cycle"] = "Faster than benchmark (+10%)"
        elif metrics.avg_deal_cycle <= self.industry_benchmarks["avg_deal_cycle_days"] * 1.1:
            comparisons["deal_cycle"] = "At benchmark"
        else:
            comparisons["deal_cycle"] = "Slower than benchmark (-10%+)"
        
        return comparisons
    
    # =================================================================
    # ANALYSIS METHODS
    # =================================================================
    
    def _identify_bottlenecks(self, metrics: PipelineMetrics, team: List[SalesTeamPerformance]) -> List[str]:
        """Выявление узких мест в процессе продаж"""
        
        bottlenecks = []
        
        # Анализ конверсий
        if metrics.lead_to_qualified_rate < self.industry_benchmarks["lead_to_qualified_rate"] * 0.8:
            bottlenecks.append("Низкая конверсия лидов в квалифицированные (< 20%)")
        
        if metrics.qualified_to_proposal_rate < self.industry_benchmarks["qualified_to_proposal_rate"] * 0.8:
            bottlenecks.append("Низкая конверсия квалифицированных лидов в предложения (< 48%)")
        
        if metrics.proposal_to_win_rate < self.industry_benchmarks["proposal_to_win_rate"] * 0.8:
            bottlenecks.append("Низкая конверсия предложений в сделки (< 24%)")
        
        # Анализ времени
        if metrics.avg_lead_response_time > 4.0:  # > 4 часов
            bottlenecks.append("Медленное время ответа на лиды (> 4 часов)")
        
        if metrics.avg_deal_cycle > self.industry_benchmarks["avg_deal_cycle_days"] * 1.2:
            bottlenecks.append("Длинный цикл сделки (> 54 дней)")
        
        # Анализ команды
        underperformers = [member for member in team if member.quota_attainment < 0.8]
        if len(underperformers) > len(team) * 0.3:  # > 30% команды
            bottlenecks.append("Высокий процент underperformers в команде (> 30%)")
        
        return bottlenecks
    
    def _identify_opportunities(self, metrics: PipelineMetrics, team: List[SalesTeamPerformance]) -> List[str]:
        """Выявление возможностей для улучшения"""
        
        opportunities = []
        
        # Возможности по метрикам
        if metrics.lead_quality_score < 80:
            opportunities.append("Улучшение качества лидов через лучшую квалификацию")
        
        if metrics.average_deal_size < self.industry_benchmarks["avg_deal_size_rub"] * 0.9:
            opportunities.append("Увеличение среднего размера сделки через upselling")
        
        if metrics.pipeline_velocity < 0.85:
            opportunities.append("Ускорение движения по pipeline через автоматизацию")
        
        # Возможности по команде
        top_performers = [member for member in team if member.quota_attainment > 1.1]
        if top_performers:
            opportunities.append("Масштабирование best practices от топ исполнителей")
        
        # Возможности по процессам
        if metrics.avg_proposal_time > 48:  # > 2 дней
            opportunities.append("Ускорение подготовки предложений через шаблоны")
        
        return opportunities
    
    def _identify_risks(self, metrics: PipelineMetrics, team: List[SalesTeamPerformance]) -> List[str]:
        """Выявление рисков"""
        
        risks = []
        
        # Риски по pipeline
        if metrics.total_pipeline_value < metrics.monthly_recurring_revenue * 3:
            risks.append("Недостаточный pipeline для поддержания роста (< 3x MRR)")
        
        if metrics.deals_lost > metrics.deals_won:
            risks.append("Негативный тренд выигранных vs проигранных сделок")
        
        # Риски по команде
        high_performers = [member for member in team if member.quota_attainment > 1.2]
        if len(high_performers) < 2:
            risks.append("Зависимость от малого количества high performers")
        
        # Риски по качеству
        if metrics.lead_quality_score < 60:
            risks.append("Низкое качество лидов может снизить эффективность команды")
        
        return risks
    
    def _identify_top_performers(self, team: List[SalesTeamPerformance]) -> List[str]:
        """Выявление лучших исполнителей"""
        
        # Сортируем по quota attainment и берем топ
        sorted_team = sorted(team, key=lambda x: x.quota_attainment, reverse=True)
        
        top_performers = []
        for member in sorted_team[:2]:  # Топ 2
            if member.quota_attainment > 1.0:
                top_performers.append(f"{member.name} ({member.role}) - {member.quota_attainment:.0%} quota")
        
        return top_performers
    
    def _identify_improvement_areas(self, team: List[SalesTeamPerformance], bottlenecks: List[str]) -> List[str]:
        """Определение областей для улучшения"""
        
        improvement_areas = []
        
        # На основе производительности команды
        avg_contact_rate = sum(member.contact_rate for member in team) / len(team)
        if avg_contact_rate < 0.7:
            improvement_areas.append("Улучшение навыков cold outreach")
        
        avg_close_rate = sum(member.close_rate for member in team) / len(team)  
        if avg_close_rate < 0.25:
            improvement_areas.append("Развитие навыков closing deals")
        
        # На основе узких мест
        if any("конверсия" in bottleneck.lower() for bottleneck in bottlenecks):
            improvement_areas.append("Оптимизация процесса квалификации")
        
        if any("время" in bottleneck.lower() for bottleneck in bottlenecks):
            improvement_areas.append("Автоматизация рутинных процессов")
        
        return improvement_areas
    
    # =================================================================
    # FORECASTING METHODS
    # =================================================================
    
    def _generate_revenue_forecast(self, metrics: PipelineMetrics) -> Dict[str, float]:
        """Генерация прогноза дохода"""
        
        # Базовые расчеты
        current_mrr = metrics.monthly_recurring_revenue
        pipeline_value = metrics.total_pipeline_value
        win_rate = metrics.proposal_to_win_rate
        avg_cycle = metrics.avg_deal_cycle / 30  # В месяцах
        
        # Прогноз на следующие месяцы
        forecast = {}
        
        # Текущий месяц (доходы от закрывающихся сделок)
        forecast["current_month"] = current_mrr + (pipeline_value * win_rate * 0.3)  # 30% закроется в этом месяце
        
        # Следующий месяц
        forecast["next_month"] = current_mrr * 1.05 + (pipeline_value * win_rate * 0.4)  # 40% закроется
        
        # 3 месяца
        forecast["3_months"] = current_mrr * 1.15 + (pipeline_value * win_rate * 0.7)  # 70% закроется
        
        # 6 месяцев  
        forecast["6_months"] = current_mrr * 1.35 + (pipeline_value * win_rate * 0.9)  # 90% закроется
        
        return forecast
    
    def _generate_pipeline_forecast(self, metrics: PipelineMetrics) -> Dict[str, int]:
        """Генерация прогноза pipeline"""
        
        monthly_lead_flow = metrics.total_leads  # Предполагаем месячный поток
        qualification_rate = metrics.lead_to_qualified_rate
        
        forecast = {}
        
        # Прогноз новых лидов
        forecast["leads_next_month"] = int(monthly_lead_flow * 1.1)  # 10% рост
        forecast["qualified_leads_next_month"] = int(forecast["leads_next_month"] * qualification_rate)
        
        # Прогноз на квартал
        forecast["leads_next_quarter"] = int(monthly_lead_flow * 3.3)  # 10% рост за квартал
        forecast["qualified_leads_next_quarter"] = int(forecast["leads_next_quarter"] * qualification_rate)
        
        return forecast
    
    # =================================================================
    # RECOMMENDATIONS ENGINE
    # =================================================================
    
    def _generate_optimization_recommendations_internal(
        self, 
        metrics: PipelineMetrics, 
        team: List[SalesTeamPerformance], 
        bottlenecks: List[str]
    ) -> List[str]:
        """Генерация рекомендаций по оптимизации"""
        
        recommendations = []
        
        # Рекомендации на основе метрик
        if metrics.lead_to_qualified_rate < 0.2:
            recommendations.append("Внедрить BANT-скоринг для улучшения квалификации лидов")
            recommendations.append("Провести тренинг команды по методологии MEDDIC")
        
        if metrics.proposal_to_win_rate < 0.25:
            recommendations.append("Улучшить качество предложений через персонализацию")
            recommendations.append("Внедрить конкурентный анализ в процесс подготовки предложений")
        
        if metrics.avg_deal_cycle > 50:
            recommendations.append("Автоматизировать follow-up процессы")
            recommendations.append("Внедрить CRM-воркфлоу для ускорения сделок")
        
        # Рекомендации на основе команды
        underperformers = [member for member in team if member.quota_attainment < 0.8]
        if underperformers:
            recommendations.append("Создать индивидуальные планы развития для underperformers")
            recommendations.append("Внедрить buddy system с топ исполнителями")
        
        # Рекомендации на основе узких мест
        if any("время ответа" in bottleneck.lower() for bottleneck in bottlenecks):
            recommendations.append("Внедрить lead routing automation")
            recommendations.append("Настроить real-time уведомления для новых лидов")
        
        # Технологические рекомендации
        if metrics.sales_efficiency < 0.7:
            recommendations.append("Внедрить sales intelligence платформу")
            recommendations.append("Автоматизировать reporting и analytics")
        
        return recommendations
    
    def _generate_action_items(self, bottlenecks: List[str], opportunities: List[str]) -> List[str]:
        """Генерация конкретных действий"""
        
        actions = []
        
        # Действия на основе узких мест
        if bottlenecks:
            actions.append("Провести root cause analysis для ключевых bottlenecks")
            actions.append("Создать action plan для устранения топ-3 узких мест")
        
        # Действия на основе возможностей
        if opportunities:
            actions.append("Приоритизировать возможности по ROI и сложности внедрения")
            actions.append("Запустить пилотный проект по топ возможности")
        
        # Общие действия
        actions.extend([
            "Настроить еженедельный sales performance review",
            "Внедрить real-time dashboard для отслеживания KPI",
            "Провести анализ win/loss для улучшения процессов",
            "Создать library лучших практик от топ исполнителей",
            "Запустить A/B тесты для оптимизации email templates"
        ])
        
        return actions
    
    def _extract_key_insights(self, result: Dict[str, Any]) -> List[str]:
        """Извлечение ключевых инсайтов"""
        
        insights = []
        
        health_score = result.get("pipeline_health_score", 0)
        if health_score >= 80:
            insights.append(f"Excellent pipeline health ({health_score}%) - система работает эффективно")
        elif health_score >= 65:
            insights.append(f"Good pipeline health ({health_score}%) - есть возможности для оптимизации")
        else:
            insights.append(f"Pipeline требует внимания ({health_score}%) - критические узкие места")
        
        # Инсайты по команде
        if "team_performance" in result:
            team_data = result["team_performance"]
            if isinstance(team_data, list) and team_data:
                avg_quota = sum(member.get("quota_attainment", 0) for member in team_data) / len(team_data)
                if avg_quota > 1.0:
                    insights.append(f"Команда перевыполняет план на {(avg_quota-1)*100:.0f}%")
                else:
                    insights.append(f"Команда недовыполняет план на {(1-avg_quota)*100:.0f}%")
        
        # Инсайты по возможностям
        opportunities = result.get("opportunities", [])
        if opportunities:
            insights.append(f"Выявлено {len(opportunities)} ключевых возможностей для роста")
        
        return insights