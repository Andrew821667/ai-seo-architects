"""
📊 Reporting Agent

Operational-level агент для автоматической генерации отчетов, KPI tracking, 
client dashboards и аналитики результатов SEO кампаний.

Основные возможности:
- Automated reporting & scheduling
- KPI tracking & monitoring
- Client dashboard creation
- Performance analytics & insights
- ROI measurement & attribution
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random

from core.base_agent import BaseAgent
from core.interfaces.data_models import AgentMetrics

logger = logging.getLogger(__name__)


class ReportingAgent(BaseAgent):
    """
    📊 Reporting Agent
    
    Operational-level агент для автоматической генерации отчетов,
    аналитики производительности и отслеживания KPI.
    """
    
    def __init__(self, data_provider=None, agent_level=None, **kwargs):
        # Убираем agent_level из kwargs если он там есть
        if 'agent_level' in kwargs:
            del kwargs['agent_level']
            
        super().__init__(
            agent_id="reporting_agent",
            name="Reporting Agent",
            agent_level=agent_level or "operational",
            data_provider=data_provider,
            knowledge_base="knowledge/operational/reporting.md",
            **kwargs
        )
        
        # Конфигурация Reporting
        self.supported_report_types = [
            "executive_summary", "detailed_performance", "technical_audit", 
            "competitive_intelligence", "roi_analysis"
        ]
        self.kpi_categories = [
            "visibility_metrics", "traffic_metrics", "conversion_metrics", 
            "revenue_metrics", "technical_metrics"
        ]
        self.alert_severity_levels = ["low", "medium", "high", "critical"]
        
        # Report generation settings
        self.max_report_data_points = 1000  # Максимальное количество data points в отчете
        self.default_time_period = 30  # Дней по умолчанию
        self.confidence_threshold = 0.85  # Порог достоверности для прогнозов
        
        # Data source weights
        self.data_source_reliability = {
            "google_analytics": 0.95,
            "search_console": 0.90,
            "third_party_tools": 0.80,
            "estimated_data": 0.60
        }
        
        logger.info(f"✅ {self.name} инициализирован:")
        logger.info(f"   📊 Supported Report Types: {len(self.supported_report_types)}")
        logger.info(f"   📈 KPI Categories: {len(self.kpi_categories)}")
        logger.info(f"   🎯 Confidence Threshold: {self.confidence_threshold}")
        logger.info(f"   📅 Default Period: {self.default_time_period} days")
    
    def get_system_prompt(self) -> str:
        """Специализированный системный промпт для reporting"""
        return f"""Ты - экспертный Reporting Agent, специалист по созданию профессиональных SEO отчётов и аналитики производительности.

ТВОЯ ЭКСПЕРТИЗА:
• SEO Performance Reporting - 30%
• KPI Analysis & Tracking - 25%
• ROI & Attribution Modeling - 20%
• Dashboard Data Preparation - 15%
• Insights & Recommendations Generation - 10%

ЗАДАЧА: Создать детальный, инсайтный SEO отчёт с ключевыми метриками, трендами и рекомендациями.

МЕТОДОЛОГИЯ ОТЧЁТОВ:
1. Performance Analysis (30 баллов):
   - Органический трафик dynamics (0-10)
   - Позиции и visibility trends (0-8)
   - Click-through rates анализ (0-6)
   - Impressions и reach metrics (0-6)

2. KPI Tracking (25 баллов):
   - Conversion tracking и attribution (0-8)
   - Goal completions analysis (0-7)
   - Revenue и business impact (0-5)
   - User engagement metrics (0-5)

3. ROI & Attribution (20 баллов):
   - Cost per acquisition calculations (0-7)
   - Revenue attribution modeling (0-7)
   - ROI по каналам и кампаниям (0-6)

4. Technical Metrics (15 баллов):
   - Site speed и Core Web Vitals (0-5)
   - Crawling и indexing status (0-5)
   - Mobile и accessibility scores (0-5)

5. Insights & Forecasting (10 баллов):
   - Тренд identification и analysis (0-4)
   - Performance forecasting (0-3)
   - Рекомендации prioritization (0-3)

ОТЧЁТНЫЕ ПАРАМЕТРЫ:
- Поддерживаемые типы: {', '.join(self.supported_report_types)}
- KPI категории: {', '.join(self.kpi_categories)}
- Период по умолчанию: {self.default_time_period} дней
- Порог достоверности: {self.confidence_threshold}
- Макс data points: {self.max_report_data_points}

ОТРАСЛЕВЫЕ БОНУСЫ:
• E-commerce: +15 (conversion & revenue focus)
• B2B Services: +12 (lead quality & attribution)
• FinTech: +10 (compliance & security metrics)
• Healthcare: +8 (trust & authority metrics)
• Local Business: +6 (local visibility metrics)

РЕЗУЛЬТАТ: Верни ТОЛЬКО JSON с полным SEO performance отчётом, ключевыми метриками, трендами и actionable рекомендациями."""

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика создания SEO отчётов с реальными LLM вызовами
        
        Args:
            task_data: Данные задачи с метриками и конфигурацией отчёта
            
        Returns:
            Dict с полным SEO performance отчётом от OpenAI
        """
        try:
            # Извлекаем входные данные
            input_data = task_data.get("input_data", {})
            task_type = task_data.get('task_type', 'comprehensive_performance_report')
            
            logger.info(f"📊 Начинаем генерацию отчёта: {input_data.get('domain', 'Unknown')}, тип: {task_type}")
            
            # Формируем специализированный промпт для reporting
            user_prompt = f"""Создай профессиональный SEO performance отчёт с глубокой аналитикой:

ДАННЫЕ ПРОЕКТА:
Domain: {input_data.get('domain', 'Unknown')}
Industry: {input_data.get('industry', 'Unknown')}
Report Type: {task_type}
Period: {input_data.get('period_days', self.default_time_period)} дней
Client Type: {input_data.get('client_type', 'General')}

ТЕКУЩИЕ МЕТРИКИ:
Organic Traffic: {input_data.get('organic_traffic', 'N/A')}
Organic Keywords: {input_data.get('organic_keywords', 'N/A')}
Average Position: {input_data.get('avg_position', 'N/A')}
Click-Through Rate: {input_data.get('ctr', 'N/A')}%
Conversions: {input_data.get('conversions', 'N/A')}
Revenue Attribution: {input_data.get('revenue', 'N/A')} ₽
Site Speed (CWV): {input_data.get('site_speed', 'N/A')}
Mobile Score: {input_data.get('mobile_score', 'N/A')}
Backlinks: {input_data.get('backlinks', 'N/A')}
Referring Domains: {input_data.get('referring_domains', 'N/A')}

ПРЕДЫДУЩИЕ ПОКАЗАТЕЛИ (для сравнения):
Previous Traffic: {input_data.get('previous_traffic', 'N/A')}
Previous Keywords: {input_data.get('previous_keywords', 'N/A')}
Previous Conversions: {input_data.get('previous_conversions', 'N/A')}
Previous Revenue: {input_data.get('previous_revenue', 'N/A')} ₽

ЦЕЛИ И KPI:
Target Goals: {input_data.get('target_goals', 'Unknown')}
KPI Focus: {input_data.get('kpi_focus', 'Traffic & Conversions')}
Budget/Investment: {input_data.get('budget', 'N/A')} ₽

Создай полный профессиональный SEO отчёт с детальной аналитикой. Верни результат строго в JSON формате:
{{
    "report_performance_score": <number 0-100>,
    "report_summary": "<executive summary отчёта>",
    "performance_analysis": {{
        "organic_traffic": {{
            "current_value": <number>,
            "previous_value": <number>,
            "change_percentage": <number>,
            "trend": "<рост/спад/стабильность>",
            "trend_analysis": "<анализ тренда>"
        }},
        "keyword_performance": {{
            "total_keywords": <number>,
            "top_10_keywords": <number>,
            "avg_position_change": <number>,
            "visibility_score": <number>,
            "keyword_trends": "<оценка трендов>"
        }},
        "user_engagement": {{
            "ctr_performance": <percentage>,
            "bounce_rate_estimate": <percentage>,
            "avg_session_duration": "<estimate>",
            "engagement_quality": "<high/medium/low>"
        }}
    }},
    "conversion_analysis": {{
        "conversion_rate": <percentage>,
        "conversion_change": <percentage>,
        "goal_completions": <number>,
        "revenue_attribution": <number>,
        "cost_per_conversion": <number>,
        "conversion_trends": "<анализ>"
    }},
    "roi_analysis": {{
        "seo_roi_percentage": <number>,
        "revenue_generated": <number>,
        "investment_vs_return": "<соотношение>",
        "payback_period": "<оценка>",
        "ltv_impact": "<влияние на LTV>"
    }},
    "technical_performance": {{
        "site_speed_score": <0-100>,
        "mobile_optimization": <0-100>,
        "core_web_vitals": "<pass/fail>",
        "indexing_health": "<оценка>",
        "technical_issues": ["<список проблем>"]
    }},
    "competitive_position": {{
        "market_share_estimate": <percentage>,
        "visibility_vs_competitors": "<сравнение>",
        "competitive_advantages": ["<преимущества>"],
        "competitive_threats": ["<угрозы>"]
    }},
    "key_insights": ["<топ-5 ключевых инсайтов>"],
    "strategic_recommendations": {{
        "high_priority": ["<высокоприоритетные действия>"],
        "medium_priority": ["<среднеприоритетные действия>"],
        "long_term_strategy": ["<долгосрочная стратегия>"]
    }},
    "forecasting": {{
        "30_day_projection": "<прогноз на 30 дней>",
        "90_day_projection": "<прогноз на 90 дней>",
        "growth_trajectory": "<траектория роста>",
        "confidence_level": <0.0-1.0>
    }},
    "next_actions": ["<конкретные следующие шаги>"]
}}"""

            # Используем базовый метод с LLM интеграцией
            result = await self.process_with_llm(user_prompt, input_data)
            
            if result["success"]:
                logger.info(f"✅ SEO отчёт создан через OpenAI: {result.get('model_used', 'unknown')}")
                # Добавляем метаданные агента
                if isinstance(result.get("result"), str):
                    # Если результат строка, оборачиваем в структуру
                    result["reporting_response"] = result["result"]
                    result["agent_type"] = "reporting"
                    result["report_type"] = task_type
                    result["methodology"] = ["Performance Analysis", "KPI Tracking", "ROI Calculation"]
                
                return result
            else:
                # Fallback к базовой логике если OpenAI недоступен
                logger.warning("⚠️ OpenAI недоступен, используем fallback reporting")
                return await self._fallback_reporting(input_data, task_type)
                
        except Exception as e:
            logger.error(f"❌ Ошибка в reporting: {str(e)}")
            return {
                "success": False,
                "agent": self.agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _fallback_reporting(self, input_data: Dict[str, Any], task_type: str) -> Dict[str, Any]:
        """Fallback логика reporting без LLM"""
        try:
            domain = input_data.get('domain', 'unknown-domain.com')
            period_days = input_data.get('period_days', self.default_time_period)
            
            # Базовый performance скор
            base_score = 65  # Средний скор
            
            # Простые корректировки на основе данных
            current_traffic = input_data.get('organic_traffic', 0)
            previous_traffic = input_data.get('previous_traffic', 0)
            
            if current_traffic > previous_traffic and previous_traffic > 0:
                traffic_growth = ((current_traffic - previous_traffic) / previous_traffic) * 100
                base_score += min(15, traffic_growth * 0.3)
            
            conversions = input_data.get('conversions', 0)
            if conversions > 0:
                base_score += 10
                
            # Определяем общую производительность
            if base_score >= 80:
                performance = "Excellent"
                trend = "сильный рост"
            elif base_score >= 65:
                performance = "Good"
                trend = "умеренный рост"
            elif base_score >= 50:
                performance = "Average"
                trend = "стабильность"
            else:
                performance = "Needs Improvement"
                trend = "снижение"
            
            # Базовые рекомендации
            recommendations = [
                "Провести детальный анализ ключевых слов",
                "Оптимизировать контент для повышения CTR",
                "Улучшить технические показатели сайта"
            ]
            
            if base_score < 60:
                recommendations.insert(0, "Критическое улучшение SEO стратегии (приоритет)")
            
            return {
                "success": True,
                "agent": self.agent_id,
                "result": {
                    "report_performance_score": base_score,
                    "performance_summary": performance,
                    "domain": domain,
                    "reporting_period": f"{period_days} дней",
                    "traffic_trend": trend,
                    "current_metrics": {
                        "organic_traffic": current_traffic,
                        "conversions": conversions,
                        "avg_position": input_data.get('avg_position', 'N/A')
                    },
                    "key_recommendations": recommendations,
                    "note": "Отчёт создан без OpenAI (fallback режим)",
                    "report_config": {
                        "supported_types": self.supported_report_types,
                        "kpi_categories": self.kpi_categories,
                        "confidence_threshold": self.confidence_threshold
                    }
                },
                "fallback_mode": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "agent": self.agent_id,
                "error": f"Fallback reporting failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    async def _generate_report(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация отчета определенного типа"""
        report_config = task_data.get('report_config', {})
        report_type = report_config.get('type', 'detailed_performance')
        domain = report_config.get('domain', 'example.com')
        period_days = report_config.get('period_days', self.default_time_period)
        client_type = report_config.get('client_type', 'general')
        
        # Генерация данных отчета
        report_data = await self._collect_report_data(domain, period_days, report_type)
        
        # Создание отчета на основе типа
        if report_type == 'executive_summary':
            report_content = await self._create_executive_summary(report_data, client_type)
        elif report_type == 'detailed_performance':
            report_content = await self._create_detailed_performance_report(report_data)
        elif report_type == 'technical_audit':
            report_content = await self._create_technical_audit_report(report_data)
        elif report_type == 'competitive_intelligence':
            report_content = await self._create_competitive_report(report_data)
        elif report_type == 'roi_analysis':
            report_content = await self._create_roi_analysis_report(report_data)
        else:
            report_content = await self._create_detailed_performance_report(report_data)
        
        # Метаданные отчета
        report_metadata = {
            "report_id": f"rpt_{int(datetime.now().timestamp())}",
            "generated_at": datetime.now().isoformat(),
            "domain": domain,
            "report_type": report_type,
            "period_days": period_days,
            "client_type": client_type,
            "data_sources": list(report_data.keys()),
            "confidence_score": self._calculate_report_confidence(report_data)
        }
        
        # Рекомендации на основе отчета
        recommendations = self._generate_report_recommendations(report_content, report_type)
        
        logger.info(f"📊 Report Generated:")
        logger.info(f"   📈 Type: {report_type}")
        logger.info(f"   🌐 Domain: {domain}")
        logger.info(f"   📅 Period: {period_days} days")
        logger.info(f"   🎯 Confidence: {report_metadata['confidence_score']:.1%}")
        
        return {
            "success": True,
            "report_metadata": report_metadata,
            "report_content": report_content,
            "recommendations": recommendations,
            "export_formats": ["pdf", "excel", "powerpoint", "json"],
            "sharing_options": ["email", "dashboard", "api", "download"],
            "agent": self.name,
            "confidence": report_metadata['confidence_score']
        }

    async def _analyze_kpis(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ KPI и трендов"""
        kpi_config = task_data.get('kpi_config', {})
        domain = kpi_config.get('domain', 'example.com')
        kpi_categories = kpi_config.get('categories', self.kpi_categories)
        period_days = kpi_config.get('period_days', 30)
        comparison_period = kpi_config.get('comparison', 'previous_period')
        
        # Сбор KPI данных
        current_kpis = self._collect_kpi_data(domain, period_days)
        comparison_kpis = self._collect_comparison_kpi_data(domain, period_days, comparison_period)
        
        # Анализ трендов
        kpi_analysis = {}
        
        for category in kpi_categories:
            if category in current_kpis:
                category_analysis = self._analyze_kpi_category(
                    current_kpis[category], 
                    comparison_kpis.get(category, {}),
                    category
                )
                kpi_analysis[category] = category_analysis
        
        # Общая оценка производительности
        overall_performance = self._calculate_overall_performance(kpi_analysis)
        
        # Выявление аномалий
        anomalies = self._detect_kpi_anomalies(current_kpis, comparison_kpis)
        
        # Прогнозирование трендов
        trend_forecasts = self._forecast_kpi_trends(current_kpis, period_days)
        
        # Алерты на основе пороговых значений
        alerts = self._generate_kpi_alerts(current_kpis, comparison_kpis)
        
        logger.info(f"📈 KPI Analysis:")
        logger.info(f"   📊 Categories Analyzed: {len(kpi_categories)}")
        logger.info(f"   🎯 Overall Performance: {overall_performance['score']}/100")
        logger.info(f"   🚨 Alerts Generated: {len(alerts)}")
        logger.info(f"   ⚠️ Anomalies Detected: {len(anomalies)}")
        
        return {
            "success": True,
            "domain": domain,
            "analysis_period": period_days,
            "comparison_period": comparison_period,
            "kpi_analysis": kpi_analysis,
            "overall_performance": overall_performance,
            "anomalies": anomalies,
            "trend_forecasts": trend_forecasts,
            "alerts": alerts,
            "data_quality_score": self._assess_data_quality(current_kpis),
            "agent": self.name,
            "confidence": round(random.uniform(0.82, 0.95), 2)
        }

    async def _prepare_dashboard_data(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Подготовка данных для dashboard"""
        dashboard_config = task_data.get('dashboard_config', {})
        domain = dashboard_config.get('domain', 'example.com')
        dashboard_type = dashboard_config.get('type', 'performance_overview')
        refresh_interval = dashboard_config.get('refresh_minutes', 60)
        user_role = dashboard_config.get('user_role', 'marketing_manager')
        
        # Определение виджетов для dashboard
        dashboard_widgets = self._get_dashboard_widgets(dashboard_type, user_role)
        
        # Сбор данных для каждого виджета
        widget_data = {}
        for widget_id, widget_config in dashboard_widgets.items():
            widget_data[widget_id] = await self._collect_widget_data(
                domain, widget_config, dashboard_type
            )
        
        # Настройка фильтров и интерактивности
        dashboard_filters = self._configure_dashboard_filters(dashboard_type, user_role)
        
        # Настройка алертов реального времени
        real_time_alerts = self._setup_realtime_alerts(domain, dashboard_type)
        
        # Персонализация для пользователя
        personalization = self._apply_dashboard_personalization(user_role, dashboard_type)
        
        # Метрики производительности dashboard
        performance_metrics = {
            "data_freshness": self._calculate_data_freshness(widget_data),
            "load_time_estimate": f"{random.randint(800, 2000)}ms",
            "data_points_count": sum(len(str(data)) for data in widget_data.values()),
            "update_frequency": f"Every {refresh_interval} minutes"
        }
        
        logger.info(f"📊 Dashboard Data Prepared:")
        logger.info(f"   🎛️ Type: {dashboard_type}")
        logger.info(f"   👤 User Role: {user_role}")
        logger.info(f"   📈 Widgets: {len(dashboard_widgets)}")
        logger.info(f"   🔄 Refresh: {refresh_interval} min")
        
        return {
            "success": True,
            "dashboard_config": {
                "domain": domain,
                "type": dashboard_type,
                "user_role": user_role,
                "refresh_interval": refresh_interval
            },
            "widgets": dashboard_widgets,
            "widget_data": widget_data,
            "filters": dashboard_filters,
            "real_time_alerts": real_time_alerts,
            "personalization": personalization,
            "performance_metrics": performance_metrics,
            "export_options": ["pdf_snapshot", "excel_data", "scheduled_email"],
            "agent": self.name,
            "confidence": round(random.uniform(0.88, 0.96), 2)
        }

    async def _generate_performance_insights(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация инсайтов производительности"""
        insight_config = task_data.get('insight_config', {})
        domain = insight_config.get('domain', 'example.com')
        analysis_depth = insight_config.get('depth', 'comprehensive')
        focus_areas = insight_config.get('focus_areas', ['traffic', 'conversions', 'technical'])
        business_context = insight_config.get('business_context', {})
        
        # Сбор данных для анализа
        performance_data = await self._collect_performance_data(domain, analysis_depth)
        
        # Генерация различных типов инсайтов
        insights = {}
        
        # Trend insights
        if 'trends' in focus_areas or analysis_depth == 'comprehensive':
            insights['trend_insights'] = self._generate_trend_insights(performance_data)
        
        # Anomaly insights  
        if 'anomalies' in focus_areas or analysis_depth == 'comprehensive':
            insights['anomaly_insights'] = self._generate_anomaly_insights(performance_data)
        
        # Opportunity insights
        if 'opportunities' in focus_areas or analysis_depth == 'comprehensive':
            insights['opportunity_insights'] = self._generate_opportunity_insights(performance_data)
        
        # Performance attribution
        if 'attribution' in focus_areas or analysis_depth == 'comprehensive':
            insights['attribution_insights'] = self._generate_attribution_insights(performance_data)
        
        # Competitive insights
        if 'competitive' in focus_areas or analysis_depth == 'comprehensive':
            insights['competitive_insights'] = self._generate_competitive_insights(performance_data)
        
        # Predictive insights
        if 'forecasting' in focus_areas or analysis_depth == 'comprehensive':
            insights['predictive_insights'] = self._generate_predictive_insights(performance_data)
        
        # Приоритизация инсайтов
        prioritized_insights = self._prioritize_insights(insights, business_context)
        
        # Actionable recommendations
        actionable_recommendations = self._create_actionable_recommendations(
            prioritized_insights, business_context
        )
        
        # Confidence scoring
        insight_confidence = self._calculate_insight_confidence(insights, performance_data)
        
        logger.info(f"🔍 Performance Insights Generated:")
        logger.info(f"   📊 Analysis Depth: {analysis_depth}")
        logger.info(f"   🎯 Focus Areas: {len(focus_areas)}")
        logger.info(f"   💡 Total Insights: {sum(len(category) for category in insights.values())}")
        logger.info(f"   🚀 High Priority: {len([i for i in prioritized_insights if i['priority'] == 'high'])}")
        
        return {
            "success": True,
            "domain": domain,
            "analysis_depth": analysis_depth,
            "focus_areas": focus_areas,
            "insights": insights,
            "prioritized_insights": prioritized_insights,
            "actionable_recommendations": actionable_recommendations,
            "insight_confidence": insight_confidence,
            "business_impact_estimate": self._estimate_business_impact(prioritized_insights),
            "implementation_timeline": self._create_implementation_timeline(actionable_recommendations),
            "agent": self.name,
            "confidence": insight_confidence['overall_confidence']
        }

    async def _calculate_roi_attribution(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет ROI и атрибуции"""
        roi_config = task_data.get('roi_config', {})
        domain = roi_config.get('domain', 'example.com')
        attribution_model = roi_config.get('attribution_model', 'data_driven')
        time_period = roi_config.get('period_days', 90)
        investment_data = roi_config.get('investment_data', {})
        
        # Сбор данных о доходах и конверсиях
        revenue_data = self._collect_revenue_data(domain, time_period)
        conversion_data = self._collect_conversion_data(domain, time_period)
        
        # Применение модели атрибуции
        attributed_results = self._apply_attribution_model(
            revenue_data, conversion_data, attribution_model
        )
        
        # Расчет ROI по различным метрикам
        roi_calculations = {
            "direct_roi": self._calculate_direct_roi(attributed_results, investment_data),
            "assisted_roi": self._calculate_assisted_roi(attributed_results, investment_data),
            "lifetime_value_roi": self._calculate_ltv_roi(attributed_results, investment_data),
            "blended_roi": self._calculate_blended_roi(attributed_results, investment_data)
        }
        
        # Анализ по каналам
        channel_attribution = self._analyze_channel_attribution(attributed_results)
        
        # Временной анализ ROI
        roi_trends = self._analyze_roi_trends(revenue_data, investment_data, time_period)
        
        # Прогноз ROI
        roi_forecast = self._forecast_roi_performance(roi_trends, investment_data)
        
        # Бенчмаркинг
        industry_benchmarks = self._get_industry_roi_benchmarks(domain)
        benchmark_comparison = self._compare_to_benchmarks(roi_calculations, industry_benchmarks)
        
        # Рекомендации по оптимизации ROI
        optimization_recommendations = self._generate_roi_optimization_recommendations(
            roi_calculations, channel_attribution, benchmark_comparison
        )
        
        logger.info(f"💰 ROI Attribution Analysis:")
        logger.info(f"   📊 Attribution Model: {attribution_model}")
        logger.info(f"   📅 Time Period: {time_period} days")
        logger.info(f"   💎 Direct ROI: {roi_calculations['direct_roi']['roi_percentage']:.1%}")
        logger.info(f"   🔄 Blended ROI: {roi_calculations['blended_roi']['roi_percentage']:.1%}")
        
        return {
            "success": True,
            "domain": domain,
            "attribution_model": attribution_model,
            "analysis_period": time_period,
            "roi_calculations": roi_calculations,
            "attributed_results": attributed_results,
            "channel_attribution": channel_attribution,
            "roi_trends": roi_trends,
            "roi_forecast": roi_forecast,
            "benchmark_comparison": benchmark_comparison,
            "optimization_recommendations": optimization_recommendations,
            "data_reliability": self._assess_attribution_reliability(attributed_results),
            "agent": self.name,
            "confidence": round(random.uniform(0.75, 0.88), 2)
        }

    async def _comprehensive_performance_report(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Комплексный отчет производительности (по умолчанию)"""
        report_data = task_data.get('input_data', task_data.get('report_data', {}))
        domain = report_data.get('domain', 'example.com')
        client_type = report_data.get('client_type', 'general')
        
        # Запуск ключевых анализов
        kpi_analysis = await self._analyze_kpis({
            'kpi_config': {'domain': domain, 'period_days': 30}
        })
        
        performance_insights = await self._generate_performance_insights({
            'insight_config': {'domain': domain, 'depth': 'comprehensive'}
        })
        
        roi_analysis = await self._calculate_roi_attribution({
            'roi_config': {'domain': domain, 'period_days': 90}
        })
        
        # Создание комплексного отчета
        comprehensive_report = {
            "executive_summary": {
                "overall_performance_score": kpi_analysis["overall_performance"]["score"],
                "key_achievements": self._extract_key_achievements(kpi_analysis, performance_insights),
                "primary_challenges": self._extract_primary_challenges(kpi_analysis, performance_insights),
                "roi_summary": {
                    "direct_roi": roi_analysis["roi_calculations"]["direct_roi"]["roi_percentage"],
                    "total_attributed_revenue": roi_analysis["attributed_results"]["total_revenue"],
                    "investment_efficiency": roi_analysis["benchmark_comparison"]["performance_vs_benchmark"]
                }
            },
            "detailed_performance": {
                "kpi_analysis": kpi_analysis["kpi_analysis"],
                "trend_analysis": performance_insights["insights"].get("trend_insights", []),
                "anomaly_detection": performance_insights["insights"].get("anomaly_insights", [])
            },
            "strategic_insights": {
                "high_priority_opportunities": performance_insights["prioritized_insights"][:5],
                "actionable_recommendations": performance_insights["actionable_recommendations"],
                "competitive_position": performance_insights["insights"].get("competitive_insights", {})
            },
            "financial_analysis": {
                "roi_breakdown": roi_analysis["roi_calculations"],
                "channel_performance": roi_analysis["channel_attribution"],
                "forecast": roi_analysis["roi_forecast"]
            }
        }
        
        # Метаданные отчета
        report_metadata = {
            "report_type": "comprehensive_performance",
            "generated_at": datetime.now().isoformat(),
            "domain": domain,
            "client_type": client_type,
            "data_period": "Last 30-90 days",
            "confidence_score": (
                kpi_analysis["confidence"] + 
                performance_insights["confidence"] + 
                roi_analysis["confidence"]
            ) / 3
        }
        
        logger.info(f"📊 Comprehensive Performance Report:")
        logger.info(f"   🎯 Overall Score: {comprehensive_report['executive_summary']['overall_performance_score']}/100")
        logger.info(f"   💰 Direct ROI: {comprehensive_report['executive_summary']['roi_summary']['direct_roi']:.1%}")
        logger.info(f"   🚀 High Priority Opportunities: {len(comprehensive_report['strategic_insights']['high_priority_opportunities'])}")
        
        return {
            "success": True,
            "report_metadata": report_metadata,
            "comprehensive_report": comprehensive_report,
            "component_analyses": {
                "kpi_analysis": kpi_analysis,
                "performance_insights": performance_insights,
                "roi_analysis": roi_analysis
            },
            "next_steps": self._create_next_steps_plan(comprehensive_report),
            "agent": self.name,
            "confidence": report_metadata["confidence_score"]
        }

    # Helper methods

    async def _collect_report_data(self, domain: str, period_days: int, report_type: str) -> Dict[str, Any]:
        """Сбор данных для отчета"""
        # Симуляция сбора данных из различных источников
        return {
            "google_analytics": {
                "sessions": random.randint(10000, 100000),
                "users": random.randint(8000, 80000),
                "pageviews": random.randint(25000, 250000),
                "bounce_rate": random.uniform(0.35, 0.65),
                "avg_session_duration": random.uniform(120, 300),
                "conversion_rate": random.uniform(0.02, 0.08)
            },
            "search_console": {
                "total_clicks": random.randint(5000, 50000),
                "total_impressions": random.randint(100000, 1000000),
                "avg_ctr": random.uniform(0.03, 0.12),
                "avg_position": random.uniform(8.5, 25.0),
                "indexed_pages": random.randint(500, 5000)
            },
            "third_party_tools": {
                "domain_authority": random.randint(35, 75),
                "backlinks": random.randint(1000, 25000),
                "referring_domains": random.randint(100, 2000),
                "organic_keywords": random.randint(2000, 20000)
            }
        }

    async def _create_executive_summary(self, report_data: Dict, client_type: str) -> Dict[str, Any]:
        """Создание executive summary"""
        return {
            "period_overview": f"Performance summary for last {self.default_time_period} days",
            "key_metrics": {
                "traffic_growth": f"+{random.randint(5, 25)}%",
                "conversion_improvement": f"+{random.randint(8, 35)}%",
                "roi_achievement": f"{random.randint(150, 400)}%",
                "market_share_gain": f"+{random.uniform(0.5, 3.2):.1f}%"
            },
            "strategic_highlights": [
                "Organic traffic grew significantly in target segments",
                "Conversion rate optimization yielded strong results",  
                "Technical SEO improvements boosted site performance",
                "Competitive positioning strengthened in key markets"
            ],
            "priority_actions": [
                "Scale successful content marketing initiatives",
                "Expand technical optimization to remaining pages",
                "Increase investment in high-performing channels"
            ]
        }

    async def _create_detailed_performance_report(self, report_data: Dict) -> Dict[str, Any]:
        """Создание детального отчета производительности"""
        return {
            "traffic_analysis": {
                "organic_sessions": report_data["google_analytics"]["sessions"],
                "session_growth": f"+{random.randint(10, 30)}%",
                "user_behavior": {
                    "bounce_rate": report_data["google_analytics"]["bounce_rate"],
                    "pages_per_session": random.uniform(2.1, 4.5),
                    "avg_session_duration": report_data["google_analytics"]["avg_session_duration"]
                }
            },
            "search_performance": {
                "keyword_rankings": {
                    "total_keywords": report_data["third_party_tools"]["organic_keywords"],
                    "top_10_keywords": random.randint(150, 800),
                    "featured_snippets": random.randint(5, 25),
                    "avg_position_change": random.uniform(-1.5, 2.2)
                },
                "serp_visibility": {
                    "total_impressions": report_data["search_console"]["total_impressions"],
                    "click_through_rate": report_data["search_console"]["avg_ctr"],
                    "impression_share": random.uniform(0.15, 0.45)
                }
            },
            "conversion_analysis": {
                "conversion_rate": report_data["google_analytics"]["conversion_rate"],
                "goal_completions": random.randint(500, 5000),
                "revenue_attribution": random.randint(500000, 5000000),
                "cost_per_acquisition": random.randint(500, 2500)
            }
        }

    def _collect_kpi_data(self, domain: str, period_days: int) -> Dict[str, Any]:
        """Сбор KPI данных"""
        return {
            "visibility_metrics": {
                "organic_impressions": random.randint(100000, 1000000),
                "average_position": random.uniform(8.0, 20.0),
                "serp_features": random.randint(10, 50),
                "voice_share": random.uniform(0.05, 0.25)
            },
            "traffic_metrics": {
                "organic_sessions": random.randint(20000, 200000),
                "organic_users": random.randint(15000, 150000),
                "pages_per_session": random.uniform(2.0, 5.0),
                "session_duration": random.uniform(120, 400)
            },
            "conversion_metrics": {
                "goal_completions": random.randint(500, 8000),
                "micro_conversions": random.randint(2000, 20000),
                "conversion_rate": random.uniform(0.02, 0.12),
                "assisted_conversions": random.randint(200, 3000)
            },
            "revenue_metrics": {
                "revenue_attributed": random.randint(1000000, 10000000),
                "revenue_assisted": random.randint(500000, 5000000),
                "cost_per_acquisition": random.randint(500, 3000),
                "lifetime_value": random.randint(5000, 25000)
            },
            "technical_metrics": {
                "core_web_vitals": random.uniform(0.6, 0.95),
                "crawl_efficiency": random.uniform(0.8, 0.98),
                "site_errors": random.randint(0, 50),
                "security_score": random.uniform(0.85, 1.0)
            }
        }

    def _collect_comparison_kpi_data(self, domain: str, period_days: int, comparison: str) -> Dict[str, Any]:
        """Сбор данных для сравнения KPI"""
        # Симуляция данных предыдущего периода (обычно немного ниже)
        base_data = self._collect_kpi_data(domain, period_days)
        
        # Применение изменений для сравнительного периода
        comparison_data = {}
        for category, metrics in base_data.items():
            comparison_data[category] = {}
            for metric, value in metrics.items():
                if isinstance(value, (int, float)):
                    # Случайное изменение от -20% до +10% для предыдущего периода
                    change_factor = random.uniform(0.8, 1.1)
                    comparison_data[category][metric] = value * change_factor
                else:
                    comparison_data[category][metric] = value
        
        return comparison_data

    def _analyze_kpi_category(self, current_data: Dict, comparison_data: Dict, category: str) -> Dict[str, Any]:
        """Анализ категории KPI"""
        analysis = {
            "category": category,
            "metrics": {},
            "overall_trend": "stable",
            "significant_changes": []
        }
        
        total_improvement = 0
        metric_count = 0
        
        for metric, current_value in current_data.items():
            if isinstance(current_value, (int, float)) and metric in comparison_data:
                previous_value = comparison_data[metric]
                change_percent = ((current_value - previous_value) / previous_value) * 100
                
                analysis["metrics"][metric] = {
                    "current_value": current_value,
                    "previous_value": previous_value,
                    "change_percent": round(change_percent, 1),
                    "trend": "up" if change_percent > 5 else "down" if change_percent < -5 else "stable"
                }
                
                if abs(change_percent) > 15:
                    analysis["significant_changes"].append({
                        "metric": metric,
                        "change": change_percent,
                        "significance": "high" if abs(change_percent) > 25 else "medium"
                    })
                
                total_improvement += change_percent
                metric_count += 1
        
        if metric_count > 0:
            avg_improvement = total_improvement / metric_count
            if avg_improvement > 5:
                analysis["overall_trend"] = "improving"
            elif avg_improvement < -5:
                analysis["overall_trend"] = "declining"
        
        return analysis

    def _calculate_overall_performance(self, kpi_analysis: Dict) -> Dict[str, Any]:
        """Расчет общей производительности"""
        category_scores = []
        
        for category, analysis in kpi_analysis.items():
            improving_metrics = sum(1 for m in analysis["metrics"].values() if m["trend"] == "up")
            stable_metrics = sum(1 for m in analysis["metrics"].values() if m["trend"] == "stable")
            declining_metrics = sum(1 for m in analysis["metrics"].values() if m["trend"] == "down")
            total_metrics = len(analysis["metrics"])
            
            if total_metrics > 0:
                category_score = ((improving_metrics * 2 + stable_metrics) / (total_metrics * 2)) * 100
                category_scores.append(category_score)
        
        overall_score = sum(category_scores) / len(category_scores) if category_scores else 50
        
        return {
            "score": round(overall_score, 1),
            "grade": "excellent" if overall_score >= 80 else "good" if overall_score >= 60 else "needs_improvement" if overall_score >= 40 else "critical",
            "category_scores": dict(zip(kpi_analysis.keys(), category_scores))
        }

    def _detect_kpi_anomalies(self, current_kpis: Dict, comparison_kpis: Dict) -> List[Dict]:
        """Выявление аномалий в KPI"""
        anomalies = []
        
        for category, metrics in current_kpis.items():
            if category in comparison_kpis:
                for metric, current_value in metrics.items():
                    if isinstance(current_value, (int, float)) and metric in comparison_kpis[category]:
                        previous_value = comparison_kpis[category][metric]
                        change_percent = abs(((current_value - previous_value) / previous_value) * 100)
                        
                        if change_percent > 50:  # Более 50% изменения считается аномалией
                            anomalies.append({
                                "category": category,
                                "metric": metric,
                                "current_value": current_value,
                                "previous_value": previous_value,
                                "change_percent": round(change_percent, 1),
                                "severity": "critical" if change_percent > 75 else "high",
                                "direction": "spike" if current_value > previous_value else "drop"
                            })
        
        return sorted(anomalies, key=lambda x: x["change_percent"], reverse=True)

    def _forecast_kpi_trends(self, current_kpis: Dict, period_days: int) -> Dict[str, Any]:
        """Прогнозирование трендов KPI"""
        forecasts = {}
        
        for category, metrics in current_kpis.items():
            forecasts[category] = {}
            for metric, current_value in metrics.items():
                if isinstance(current_value, (int, float)):
                    # Простое прогнозирование на основе случайного тренда
                    trend_factor = random.uniform(0.95, 1.15)  # -5% до +15% роста
                    forecast_30d = current_value * trend_factor
                    forecast_90d = current_value * (trend_factor ** 3)
                    
                    forecasts[category][metric] = {
                        "current_value": current_value,
                        "forecast_30d": round(forecast_30d, 2),
                        "forecast_90d": round(forecast_90d, 2),
                        "confidence": random.uniform(0.7, 0.9),
                        "trend_direction": "up" if trend_factor > 1.05 else "down" if trend_factor < 0.95 else "stable"
                    }
        
        return forecasts

    def _generate_kpi_alerts(self, current_kpis: Dict, comparison_kpis: Dict) -> List[Dict]:
        """Генерация алертов на основе KPI"""
        alerts = []
        
        # Алерты для критических изменений
        for category, metrics in current_kpis.items():
            if category in comparison_kpis:
                for metric, current_value in metrics.items():
                    if isinstance(current_value, (int, float)) and metric in comparison_kpis[category]:
                        previous_value = comparison_kpis[category][metric]
                        change_percent = ((current_value - previous_value) / previous_value) * 100
                        
                        # Алерт для снижения трафика
                        if metric in ["organic_sessions", "organic_users"] and change_percent < -20:
                            alerts.append({
                                "type": "traffic_drop",
                                "severity": "high",
                                "metric": metric,
                                "change_percent": round(change_percent, 1),
                                "message": f"{metric} decreased by {abs(change_percent):.1f}%",
                                "action_required": True
                            })
                        
                        # Алерт для падения конверсий
                        elif metric == "conversion_rate" and change_percent < -15:
                            alerts.append({
                                "type": "conversion_drop",
                                "severity": "critical",
                                "metric": metric,
                                "change_percent": round(change_percent, 1),
                                "message": f"Conversion rate dropped by {abs(change_percent):.1f}%",
                                "action_required": True
                            })
        
        return sorted(alerts, key=lambda x: {"critical": 3, "high": 2, "medium": 1, "low": 0}[x["severity"]], reverse=True)

    def _assess_data_quality(self, kpis: Dict) -> float:
        """Оценка качества данных"""
        quality_factors = []
        
        # Проверка полноты данных
        total_expected_metrics = sum(len(category) for category in kpis.values())
        actual_metrics = sum(sum(1 for v in category.values() if v is not None) for category in kpis.values())
        completeness = actual_metrics / total_expected_metrics if total_expected_metrics > 0 else 0
        quality_factors.append(completeness)
        
        # Проверка разумности значений
        reasonable_values = 0
        total_numeric_values = 0
        for category in kpis.values():
            for metric, value in category.items():
                if isinstance(value, (int, float)):
                    total_numeric_values += 1
                    if value >= 0 and not (value == 0 and metric not in ["site_errors"]):  # Основные метрики не должны быть 0
                        reasonable_values += 1
        
        reasonableness = reasonable_values / total_numeric_values if total_numeric_values > 0 else 0
        quality_factors.append(reasonableness)
        
        return sum(quality_factors) / len(quality_factors)

    def _get_dashboard_widgets(self, dashboard_type: str, user_role: str) -> Dict[str, Dict]:
        """Получение виджетов для dashboard"""
        base_widgets = {
            "performance_scorecard": {
                "type": "scorecard",
                "metrics": ["traffic", "conversions", "rankings", "roi"],
                "size": "large"
            },
            "traffic_chart": {
                "type": "time_series",
                "metrics": ["organic_sessions", "organic_users"],
                "size": "medium"
            },
            "keyword_table": {
                "type": "data_table",
                "metrics": ["keyword", "position", "volume", "clicks"],
                "size": "medium"
            }
        }
        
        if user_role == "executive":
            base_widgets["roi_summary"] = {
                "type": "financial_summary",
                "metrics": ["roi", "revenue", "cost"],
                "size": "large"
            }
        elif user_role == "technical":
            base_widgets["technical_health"] = {
                "type": "health_monitor",
                "metrics": ["core_web_vitals", "errors", "crawl_rate"],
                "size": "medium"
            }
        
        return base_widgets

    async def _collect_widget_data(self, domain: str, widget_config: Dict, dashboard_type: str) -> Dict[str, Any]:
        """Сбор данных для виджета"""
        widget_data = {}
        
        for metric in widget_config["metrics"]:
            if metric == "traffic":
                widget_data[metric] = random.randint(10000, 100000)
            elif metric == "conversions":
                widget_data[metric] = random.randint(500, 5000)
            elif metric == "rankings":
                widget_data[metric] = random.uniform(8.0, 15.0)
            elif metric == "roi":
                widget_data[metric] = random.uniform(1.5, 4.5)
            else:
                widget_data[metric] = random.randint(100, 10000)
        
        return widget_data

    def _configure_dashboard_filters(self, dashboard_type: str, user_role: str) -> Dict[str, Any]:
        """Настройка фильтров dashboard"""
        return {
            "time_range": ["last_7_days", "last_30_days", "last_90_days", "custom"],
            "device": ["desktop", "mobile", "tablet"],
            "geography": ["all", "russia", "moscow", "spb"],
            "traffic_source": ["organic", "direct", "referral", "social", "paid"]
        }

    def _setup_realtime_alerts(self, domain: str, dashboard_type: str) -> List[Dict]:
        """Настройка алертов реального времени"""
        return [
            {
                "alert_type": "traffic_anomaly",
                "threshold": "20% deviation from normal",
                "enabled": True
            },
            {
                "alert_type": "conversion_drop",
                "threshold": "15% decrease",
                "enabled": True
            },
            {
                "alert_type": "ranking_loss",
                "threshold": "5+ position drop for target keywords",
                "enabled": True
            }
        ]

    def _apply_dashboard_personalization(self, user_role: str, dashboard_type: str) -> Dict[str, Any]:
        """Применение персонализации dashboard"""
        return {
            "preferred_metrics": {
                "executive": ["roi", "revenue", "market_share"],
                "marketing_manager": ["traffic", "conversions", "cost_per_acquisition"],
                "technical": ["site_speed", "crawl_errors", "security_score"]
            }.get(user_role, ["traffic", "conversions"]),
            "default_time_range": "last_30_days",
            "notification_preferences": {
                "email": True,
                "slack": False,
                "dashboard": True
            }
        }

    def _calculate_data_freshness(self, widget_data: Dict) -> str:
        """Расчет свежести данных"""
        # Симуляция проверки свежести данных
        freshness_minutes = random.randint(5, 60)
        if freshness_minutes <= 15:
            return "very_fresh"
        elif freshness_minutes <= 30:
            return "fresh"
        elif freshness_minutes <= 60:
            return "moderate"
        else:
            return "stale"

    def _calculate_report_confidence(self, report_data: Dict) -> float:
        """Расчет достоверности отчета"""
        source_weights = []
        
        for source, data in report_data.items():
            reliability = self.data_source_reliability.get(source, 0.5)
            data_completeness = len([v for v in data.values() if v is not None]) / len(data)
            source_confidence = reliability * data_completeness
            source_weights.append(source_confidence)
        
        return sum(source_weights) / len(source_weights) if source_weights else 0.5

    def _generate_report_recommendations(self, report_content: Dict, report_type: str) -> List[str]:
        """Генерация рекомендаций на основе отчета"""
        recommendations = []
        
        if report_type == "executive_summary":
            recommendations.extend([
                "Увеличить инвестиции в высокоэффективные каналы",
                "Оптимизировать конверсионную воронку",
                "Расширить успешные контентные стратегии"
            ])
        elif report_type == "technical_audit":
            recommendations.extend([
                "Исправить критические технические ошибки",
                "Улучшить Core Web Vitals показатели",
                "Оптимизировать мобильную версию сайта"
            ])
        else:
            recommendations.extend([
                "Сосредоточиться на высокоприоритетных возможностях",
                "Улучшить производительность недоэффективных страниц",
                "Развивать успешные направления деятельности"
            ])
        
        return recommendations

    def get_agent_metrics(self) -> AgentMetrics:
        """Получение метрик работы агента"""
        return AgentMetrics(
            agent_name=self.name,
            agent_type="operational",
            version="1.0.0",
            status="active",
            total_tasks_processed=getattr(self, '_tasks_processed', 0),
            success_rate=getattr(self, '_success_rate', 0.0),
            average_response_time=getattr(self, '_avg_response_time', 0.0),
            specialized_metrics={
                "supported_report_types": len(self.supported_report_types),
                "kpi_categories": len(self.kpi_categories),
                "max_data_points": self.max_report_data_points,
                "confidence_threshold": self.confidence_threshold
            }
        )