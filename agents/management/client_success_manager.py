"""
🤝 Client Success Manager Agent

Management-level агент для максимизации клиентского успеха, предотвращения оттока 
и развития долгосрочных отношений с клиентами SEO-агентства.

Основные возможности:
- Churn prediction & prevention
- Onboarding automation  
- Upsell/cross-sell identification
- QBR generation
- Success metrics tracking
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random

from core.base_agent import BaseAgent
from core.interfaces.data_models import AgentMetrics

logger = logging.getLogger(__name__)


class ClientSuccessManagerAgent(BaseAgent):
    """
    🤝 Client Success Manager Agent
    
    Management-level агент для управления клиентским успехом и предотвращения оттока.
    Обеспечивает максимальную лояльность клиентов и расширение сотрудничества.
    """
    
    def __init__(self, data_provider=None, **kwargs):
        super().__init__(
            agent_id="client_success_manager",
            name="Client Success Manager",
            agent_level="management",
            data_provider=data_provider,
            **kwargs
        )
        
        # Конфигурация Client Success
        self.churn_risk_threshold = 60  # Порог риска оттока
        self.upsell_probability_min = 0.40  # Минимальная вероятность для предложений
        self.health_score_critical = 30  # Критический уровень здоровья клиента
        self.nps_target = 8.0  # Целевой NPS
        
        # Churn prediction factors
        self.churn_factors = {
            "contract_value": {"weight": 0.25, "threshold_low": 500000},
            "engagement_score": {"weight": 0.20, "threshold_low": 60},
            "payment_delays": {"weight": 0.15, "threshold_high": 2},
            "support_tickets": {"weight": 0.15, "threshold_high": 5},
            "feature_adoption": {"weight": 0.10, "threshold_low": 40},
            "nps_score": {"weight": 0.10, "threshold_low": 7},
            "last_login": {"weight": 0.05, "threshold_high": 14}
        }
        
        # Upsell opportunities matrix
        self.upsell_opportunities = {
            "technical_seo": {
                "package": "Advanced Technical SEO",
                "value": 500000,
                "probability": 0.65
            },
            "content_marketing": {
                "package": "Content Strategy Premium", 
                "value": 300000,
                "probability": 0.55
            },
            "link_building": {
                "package": "Enterprise Link Building",
                "value": 800000,
                "probability": 0.45
            },
            "local_seo": {  
                "package": "Multi-Location SEO",
                "value": 200000,
                "probability": 0.70
            }
        }
        
        logger.info(f"✅ {self.name} инициализирован:")
        logger.info(f"   🎯 Churn Risk Threshold: {self.churn_risk_threshold}%")
        logger.info(f"   💰 Min Upsell Probability: {self.upsell_probability_min:.0%}")
        logger.info(f"   🚨 Critical Health Score: {self.health_score_critical}")
        logger.info(f"   📊 Target NPS: {self.nps_target}")

    def get_system_prompt(self) -> str:
        """Системный промпт для Client Success Manager"""
        return f"""Ты - Client Success Manager уровня management, эксперт по клиентскому успеху и retention.

ТВОЯ ЭКСПЕРТИЗА:
• Churn Prediction & Prevention - 35%
• Customer Success Strategy - 25% 
• Upsell/Cross-sell Optimization - 20%
• QBR & Reporting - 20%

ПОРОГОВЫЕ ЗНАЧЕНИЯ:
• Churn Risk Threshold: {self.churn_risk_threshold}%
• Min Upsell Probability: {self.upsell_probability_min:.0%}
• Critical Health Score: {self.health_score_critical}
• Target NPS: {self.nps_target}

ЗАДАЧА: Проведи comprehensive client success analysis.

ФОРМАТ ОТВЕТА (JSON):
{{
  "client_analysis": {{
    "health_score": "0-100",
    "churn_risk": "0-100",
    "satisfaction_metrics": {{}},
    "engagement_level": "high/medium/low"
  }},
  "retention_strategy": [],
  "upsell_opportunities": [],
  "action_items": [],
  "confidence_score": "0.0-1.0"
}}"""

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка задач Client Success Manager с LLM интеграцией
        """
        task_type = task_data.get('task_type', 'client_health_assessment')
        input_data = task_data.get('input_data', {})
        
        print(f"🎯 Client Success Manager обрабатывает задачу: {task_type}")

        try:
            # Формируем промпт для LLM
            user_prompt = f"""Проведи client success analysis:
            
ЗАДАЧА: {task_type}
ДАННЫЕ КЛИЕНТА: 
{input_data}

Проанализируй клиентский успех и дай рекомендации по retention и upsell."""
            
            # Вызываем LLM
            llm_result = await self.process_with_llm(user_prompt, task_data)
            
            if llm_result["success"]:
                try:
                    import re
                    import json
                    llm_content = llm_result["result"]
                    if isinstance(llm_content, str):
                        json_match = re.search(r'\{.*\}', llm_content, re.DOTALL)
                        if json_match:
                            result = json.loads(json_match.group())
                        else:
                            result = self._create_fallback_client_analysis(input_data, task_type)
                    else:
                        result = llm_content
                except (json.JSONDecodeError, AttributeError):
                    result = self._create_fallback_client_analysis(input_data, task_type)
            else:
                result = self._create_fallback_client_analysis(input_data, task_type)
                result["fallback_mode"] = True

            return {
                "success": True,
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "task_type": task_type,
                "result": result,
                "model_used": llm_result.get('model_used') if llm_result["success"] else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "agent": self.agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _create_fallback_client_analysis(self, input_data: Dict[str, Any], task_type: str) -> Dict[str, Any]:
        """Fallback client success analysis"""
        return {
            "client_analysis": {
                "health_score": 78,
                "churn_risk": 25,
                "satisfaction_metrics": {"nps": 8.2, "csat": 4.1},
                "engagement_level": "high"
            },
            "retention_strategy": [
                "Усилить коммуникации с клиентом",
                "Провести дополнительный QBR"
            ],
            "upsell_opportunities": [
                "Дополнительные SEO услуги",
                "Расширение geografic coverage"
            ],
            "action_items": [
                "Назначить звонок с клиентом",
                "Подготовить proposal для upsell"
            ],
            "confidence_score": 0.85,
            "fallback_used": True
        }

    async def _assess_client_health(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Оценка общего здоровья клиента"""
        client_data = task_data.get('client_data', {})
        client_name = client_data.get('company_name', 'Unknown Client')
        
        # Симуляция данных клиента
        monthly_value = client_data.get('monthly_value', random.randint(200000, 2000000))
        engagement_score = random.randint(45, 95)
        payment_delays = random.randint(0, 3)
        support_tickets = random.randint(1, 8)
        feature_adoption = random.randint(30, 85)
        nps_score = random.randint(6, 10)
        last_login_days = random.randint(1, 21)
        
        # Расчет health score
        health_score = self._calculate_health_score({
            'monthly_value': monthly_value,
            'engagement_score': engagement_score,
            'payment_delays': payment_delays,
            'support_tickets': support_tickets,
            'feature_adoption': feature_adoption,
            'nps_score': nps_score,
            'last_login_days': last_login_days
        })
        
        # Определение статуса здоровья
        if health_score >= 80:
            health_status = "excellent"
            health_description = "Клиент-чемпион"
        elif health_score >= 60:
            health_status = "good"
            health_description = "Стабильный клиент"
        elif health_score >= 40:
            health_status = "at_risk"
            health_description = "Требует внимания"
        else:
            health_status = "critical"
            health_description = "Критический риск"
        
        # Рекомендации по действиям
        action_recommendations = self._get_health_recommendations(health_score, {
            'engagement_score': engagement_score,
            'payment_delays': payment_delays,
            'support_tickets': support_tickets,
            'nps_score': nps_score
        })
        
        logger.info(f"🤝 Client Health Assessment для {client_name}:")
        logger.info(f"   📊 Health Score: {health_score}/100")
        logger.info(f"   💚 Status: {health_status}")
        logger.info(f"   🎯 NPS: {nps_score}/10")
        
        return {
            "success": True,
            "client_name": client_name,
            "health_score": health_score,
            "health_status": health_status,
            "health_description": health_description,
            "metrics": {
                "monthly_value": monthly_value,
                "engagement_score": engagement_score,
                "payment_delays": payment_delays,
                "support_tickets": support_tickets,
                "feature_adoption": feature_adoption,
                "nps_score": nps_score,
                "last_login_days": last_login_days
            },
            "recommendations": action_recommendations,
            "agent": self.name,
            "confidence": round(random.uniform(0.75, 0.95), 2)
        }

    async def _analyze_churn_risk(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ риска оттока клиента"""
        client_data = task_data.get('client_data', {})
        client_name = client_data.get('company_name', 'Unknown Client')
        
        # Получение метрик для анализа риска
        monthly_value = client_data.get('monthly_value', random.randint(200000, 2000000))
        engagement_score = random.randint(35, 85)  # Более низкий для анализа риска
        payment_delays = random.randint(0, 4)
        support_tickets = random.randint(2, 12)
        feature_adoption = random.randint(20, 70)
        nps_score = random.randint(4, 9)
        last_login_days = random.randint(1, 30)
        
        # Расчет churn risk score
        churn_score = self._calculate_churn_risk({
            'monthly_value': monthly_value,
            'engagement_score': engagement_score,
            'payment_delays': payment_delays,
            'support_tickets': support_tickets,
            'feature_adoption': feature_adoption,
            'nps_score': nps_score,
            'last_login_days': last_login_days
        })
        
        # Определение уровня риска
        if churn_score <= 30:
            risk_level = "low"
            risk_description = "Низкий риск оттока"
            action_priority = "maintain"
        elif churn_score <= 60:
            risk_level = "medium"
            risk_description = "Средний риск оттока"
            action_priority = "engage"
        elif churn_score <= 80:
            risk_level = "high"
            risk_description = "Высокий риск оттока"
            action_priority = "intervene"
        else:
            risk_level = "critical"
            risk_description = "Критический риск оттока"
            action_priority = "emergency_save"
        
        # Специфические предупреждающие сигналы
        warning_signals = self._identify_warning_signals({
            'engagement_score': engagement_score,
            'payment_delays': payment_delays,
            'support_tickets': support_tickets,
            'last_login_days': last_login_days,
            'nps_score': nps_score
        })
        
        # План предотвращения оттока
        retention_plan = self._create_retention_plan(risk_level, warning_signals)
        
        logger.info(f"🚨 Churn Risk Analysis для {client_name}:")
        logger.info(f"   📊 Churn Score: {churn_score}/100")
        logger.info(f"   ⚠️ Risk Level: {risk_level}")
        logger.info(f"   🎯 Action Priority: {action_priority}")
        
        return {
            "success": True,
            "client_name": client_name,
            "churn_score": churn_score,
            "risk_level": risk_level,
            "risk_description": risk_description,
            "action_priority": action_priority,
            "warning_signals": warning_signals,
            "retention_plan": retention_plan,
            "metrics": {
                "monthly_value": monthly_value,
                "engagement_score": engagement_score,
                "payment_delays": payment_delays,
                "support_tickets": support_tickets,
                "feature_adoption": feature_adoption,
                "nps_score": nps_score,
                "last_login_days": last_login_days
            },
            "agent": self.name,
            "confidence": round(random.uniform(0.70, 0.90), 2)
        }

    async def _analyze_upsell_opportunities(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ возможностей для upsell/cross-sell"""
        client_data = task_data.get('client_data', {})
        client_name = client_data.get('company_name', 'Unknown Client')
        
        current_spend = client_data.get('monthly_value', random.randint(500000, 2000000))
        industry = client_data.get('industry', 'general')
        business_type = client_data.get('business_type', 'enterprise')
        
        # Симуляция текущих метрик клиента
        technical_score = random.randint(45, 85)
        content_score = random.randint(40, 80)
        domain_authority = random.randint(35, 70)
        organic_traffic = random.randint(50000, 500000)
        locations = random.randint(1, 15)
        
        # Анализ возможностей upsell
        opportunities = []
        total_potential_value = 0
        
        # Technical SEO upsell
        if current_spend < 1000000 and technical_score < 70:
            opp = self.upsell_opportunities['technical_seo'].copy()
            opp['current_gap'] = 70 - technical_score
            opp['fit_score'] = round(random.uniform(0.60, 0.80), 2)
            opportunities.append(opp)
            total_potential_value += opp['value']
        
        # Content Marketing upsell
        if content_score < 60 and organic_traffic > 100000:
            opp = self.upsell_opportunities['content_marketing'].copy()
            opp['current_gap'] = 60 - content_score  
            opp['fit_score'] = round(random.uniform(0.50, 0.70), 2)
            opportunities.append(opp)
            total_potential_value += opp['value']
        
        # Link Building upsell
        if domain_authority < 50 and current_spend > 2000000:
            opp = self.upsell_opportunities['link_building'].copy()
            opp['current_gap'] = 50 - domain_authority
            opp['fit_score'] = round(random.uniform(0.40, 0.60), 2)
            opportunities.append(opp)
            total_potential_value += opp['value']
        
        # Local SEO upsell
        if business_type == 'local' and locations > 5:
            opp = self.upsell_opportunities['local_seo'].copy()
            opp['locations_potential'] = locations
            opp['fit_score'] = round(random.uniform(0.65, 0.85), 2)
            opportunities.append(opp)
            total_potential_value += opp['value']
        
        # Приоритизация возможностей
        opportunities = sorted(opportunities, key=lambda x: x['fit_score'] * x['value'], reverse=True)
        
        # Расчет общего expansion potential
        expansion_percentage = round((total_potential_value / current_spend) * 100, 1)
        
        logger.info(f"💰 Upsell Analysis для {client_name}:")
        logger.info(f"   📊 Current Spend: {current_spend:,} ₽/мес")
        logger.info(f"   🚀 Opportunities Found: {len(opportunities)}")
        logger.info(f"   💎 Total Potential: {total_potential_value:,} ₽/мес")
        logger.info(f"   📈 Expansion Potential: +{expansion_percentage}%")
        
        return {
            "success": True,
            "client_name": client_name,
            "current_monthly_spend": current_spend,
            "opportunities_count": len(opportunities),
            "total_potential_value": total_potential_value,
            "expansion_percentage": expansion_percentage,
            "opportunities": opportunities,
            "client_metrics": {
                "technical_score": technical_score,
                "content_score": content_score,
                "domain_authority": domain_authority,
                "organic_traffic": organic_traffic,
                "locations": locations
            },
            "recommendations": self._create_upsell_recommendations(opportunities),
            "agent": self.name,
            "confidence": round(random.uniform(0.65, 0.85), 2)
        }

    async def _track_onboarding_progress(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Отслеживание прогресса онбординга клиента"""
        client_data = task_data.get('client_data', {})
        client_name = client_data.get('company_name', 'Unknown Client')
        onboarding_day = task_data.get('onboarding_day', random.randint(1, 90))
        
        # Определение фазы онбординга
        if onboarding_day <= 30:
            phase = "foundation"
            phase_name = "Foundation (Days 0-30)"
        elif onboarding_day <= 60:
            phase = "implementation"
            phase_name = "Implementation (Days 31-60)"  
        else:
            phase = "optimization"
            phase_name = "Optimization (Days 61-90)"
        
        # Симуляция прогресса по ключевым метрикам
        progress_metrics = {
            "initial_audit_completion": min(100, max(0, onboarding_day * 3.33)),
            "stakeholder_alignment": min(100, max(0, (onboarding_day - 5) * 4.76)),
            "baseline_metrics": min(100, max(0, (onboarding_day - 10) * 5.56)),
            "team_introductions": min(100, max(0, (onboarding_day - 3) * 3.70)),
            "first_report_delivered": 100 if onboarding_day >= 14 else 0,
            "strategy_approval": 100 if onboarding_day >= 21 else 0,
            "implementation_start": 100 if onboarding_day >= 30 else 0
        }
        
        # Расчет общего прогресса
        overall_progress = round(sum(progress_metrics.values()) / len(progress_metrics), 1)
        
        # Определение статуса онбординга
        if overall_progress >= 90:
            status = "excellent"
            status_description = "Опережает план"
        elif overall_progress >= 70:
            status = "on_track"
            status_description = "В соответствии с планом"
        elif overall_progress >= 50:
            status = "delayed"
            status_description = "Небольшая задержка"
        else:
            status = "at_risk"
            status_description = "Риск провала онбординга"
        
        # Next steps recommendations  
        next_steps = self._get_onboarding_next_steps(phase, overall_progress)
        
        # Ожидаемая дата завершения
        if overall_progress > 0:
            estimated_completion_days = round(90 * (100 / overall_progress))
            days_remaining = max(0, estimated_completion_days - onboarding_day)
        else:
            days_remaining = 90 - onboarding_day
        
        logger.info(f"🚀 Onboarding Progress для {client_name}:")
        logger.info(f"   📅 Day: {onboarding_day}/90")
        logger.info(f"   📊 Overall Progress: {overall_progress}%")
        logger.info(f"   🎯 Phase: {phase_name}")
        logger.info(f"   ✅ Status: {status}")
        
        return {
            "success": True,
            "client_name": client_name,
            "onboarding_day": onboarding_day,
            "phase": phase,
            "phase_name": phase_name,
            "overall_progress": overall_progress,
            "status": status,
            "status_description": status_description,
            "progress_metrics": progress_metrics,
            "days_remaining": days_remaining,
            "next_steps": next_steps,
            "agent": self.name,
            "confidence": round(random.uniform(0.80, 0.95), 2)
        }

    async def _prepare_qbr(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Подготовка квартального бизнес-обзора (QBR)"""
        client_data = task_data.get('client_data', {})
        client_name = client_data.get('company_name', 'Unknown Client')
        quarter = task_data.get('quarter', 'Q1 2025')
        
        # Симуляция квартальных метрик
        quarterly_metrics = {
            "organic_traffic_growth": round(random.uniform(15, 45), 1),
            "keyword_rankings_improved": random.randint(25, 80),
            "technical_score_improvement": random.randint(10, 35),
            "content_pieces_published": random.randint(12, 36),
            "conversion_rate_lift": round(random.uniform(8, 25), 1),
            "revenue_attributed": random.randint(2500000, 15000000)
        }
        
        # Highlights и achievements
        quarterly_highlights = [
            f"Organic traffic рост на {quarterly_metrics['organic_traffic_growth']}%",
            f"{quarterly_metrics['keyword_rankings_improved']} keywords в топ-10",
            f"Technical SEO score улучшен на {quarterly_metrics['technical_score_improvement']} пунктов"
        ]
        
        # Стратегические приоритеты на следующий квартал
        next_quarter_priorities = [
            "Масштабирование контентной стратегии",
            "Оптимизация Core Web Vitals",
            "Расширение семантического ядра"
        ]
        
        # Investment recommendations
        investment_recommendations = {
            "technical_optimization": {
                "budget": random.randint(300000, 800000),
                "focus": "Core Web Vitals, mobile optimization"
            },
            "content_expansion": {
                "budget": random.randint(400000, 1000000),
                "focus": "Premium content, expert articles"
            },
            "link_building": {
                "budget": random.randint(500000, 1200000),
                "focus": "High-authority partnerships"
            }
        }
        
        # Risk assessment
        risk_factors = [
            "Competitive pressure в ключевых segments",
            "Google algorithm updates impact",
            "Seasonal traffic fluctuations"
        ]
        
        # Success probability для следующего квартала  
        success_probability = round(random.uniform(0.75, 0.92), 2)
        
        logger.info(f"📊 QBR Preparation для {client_name} ({quarter}):")
        logger.info(f"   📈 Traffic Growth: {quarterly_metrics['organic_traffic_growth']}%")
        logger.info(f"   🎯 Keywords Improved: {quarterly_metrics['keyword_rankings_improved']}")
        logger.info(f"   💰 Revenue Attributed: {quarterly_metrics['revenue_attributed']:,} ₽")
        logger.info(f"   🚀 Success Probability: {success_probability:.0%}")
        
        return {
            "success": True,
            "client_name": client_name,
            "quarter": quarter,
            "quarterly_metrics": quarterly_metrics,
            "quarterly_highlights": quarterly_highlights,
            "next_quarter_priorities": next_quarter_priorities,
            "investment_recommendations": investment_recommendations,
            "risk_factors": risk_factors,
            "success_probability": success_probability,
            "qbr_agenda": {
                "executive_summary": "10 мин - ключевые достижения",
                "performance_deep_dive": "20 мин - детальная аналитика", 
                "strategic_roadmap": "15 мин - планы на следующий квартал",
                "open_discussion": "15 мин - обратная связь и предложения"
            },
            "agent": self.name,
            "confidence": round(random.uniform(0.85, 0.95), 2)
        }

    async def _comprehensive_client_analysis(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Комплексный анализ клиента (по умолчанию)"""
        client_data = task_data.get('input_data', task_data.get('client_data', {}))
        client_name = client_data.get('company_name', 'Unknown Client')
        
        # Запуск всех ключевых анализов
        health_analysis = await self._assess_client_health({'client_data': client_data})
        churn_analysis = await self._analyze_churn_risk({'client_data': client_data})
        upsell_analysis = await self._analyze_upsell_opportunities({'client_data': client_data})
        
        # Общая оценка и рекомендации
        overall_score = round((
            health_analysis['health_score'] * 0.4 +
            (100 - churn_analysis['churn_score']) * 0.4 +
            min(100, upsell_analysis['expansion_percentage'] * 2) * 0.2
        ), 1)
        
        # Определение общего статуса клиента
        if overall_score >= 80:
            client_status = "champion"
            status_description = "Клиент-чемпион, максимальная лояльность"
        elif overall_score >= 60:
            client_status = "stable"
            status_description = "Стабильный клиент, хорошие перспективы"
        elif overall_score >= 40:
            client_status = "at_risk"
            status_description = "Требует повышенного внимания"
        else:
            client_status = "critical"
            status_description = "Критическое состояние, экстренные меры"
        
        # Стратегические рекомендации
        strategic_actions = self._get_strategic_recommendations(
            health_analysis, churn_analysis, upsell_analysis
        )
        
        logger.info(f"🎯 Comprehensive Client Analysis для {client_name}:")
        logger.info(f"   📊 Overall Score: {overall_score}/100")
        logger.info(f"   🏆 Client Status: {client_status}")
        logger.info(f"   💰 Upsell Potential: {upsell_analysis['total_potential_value']:,} ₽/мес")
        
        return {
            "success": True,
            "client_name": client_name,
            "overall_score": overall_score,
            "client_status": client_status,
            "status_description": status_description,
            "health_analysis": {
                "health_score": health_analysis['health_score'],
                "health_status": health_analysis['health_status']
            },
            "churn_analysis": {
                "churn_score": churn_analysis['churn_score'],
                "risk_level": churn_analysis['risk_level']
            },
            "upsell_analysis": {
                "opportunities_count": upsell_analysis['opportunities_count'],
                "total_potential_value": upsell_analysis['total_potential_value'],
                "expansion_percentage": upsell_analysis['expansion_percentage']
            },
            "strategic_actions": strategic_actions,
            "priority_level": self._determine_priority_level(overall_score),
            "agent": self.name,
            "confidence": round(random.uniform(0.75, 0.90), 2)
        }

    def _calculate_health_score(self, metrics: Dict[str, Any]) -> int:
        """Расчет health score клиента"""
        score = 0
        
        # Financial health (25%)
        if metrics['monthly_value'] >= 1000000:
            score += 25
        elif metrics['monthly_value'] >= 500000:
            score += 20
        else:
            score += 15
        
        # Engagement (20%)
        if metrics['engagement_score'] >= 80:
            score += 20
        elif metrics['engagement_score'] >= 60:
            score += 15
        else:
            score += 10
        
        # Payment behavior (15%)
        if metrics['payment_delays'] == 0:
            score += 15
        elif metrics['payment_delays'] <= 1:
            score += 10
        else:
            score += 5
        
        # Support load (15%)
        if metrics['support_tickets'] <= 2:
            score += 15
        elif metrics['support_tickets'] <= 5:
            score += 10
        else:
            score += 5
        
        # Feature adoption (10%)
        if metrics['feature_adoption'] >= 70:
            score += 10
        elif metrics['feature_adoption'] >= 50:
            score += 8
        else:
            score += 5
        
        # NPS satisfaction (10%)
        if metrics['nps_score'] >= 9:
            score += 10
        elif metrics['nps_score'] >= 7:
            score += 8
        else:
            score += 5
        
        # Activity recency (5%)
        if metrics['last_login_days'] <= 3:
            score += 5
        elif metrics['last_login_days'] <= 7:
            score += 3
        else:
            score += 1
        
        return min(100, score)

    def _calculate_churn_risk(self, metrics: Dict[str, Any]) -> int:
        """Расчет churn risk score"""
        risk_score = 0
        
        # Низкая стоимость контракта = higher risk
        if metrics['monthly_value'] < 500000:
            risk_score += 25
        elif metrics['monthly_value'] < 1000000:
            risk_score += 15
        
        # Низкий engagement = higher risk
        if metrics['engagement_score'] < 40:
            risk_score += 30
        elif metrics['engagement_score'] < 60:
            risk_score += 20
        elif metrics['engagement_score'] < 80:
            risk_score += 10
        
        # Payment delays = higher risk
        risk_score += min(20, metrics['payment_delays'] * 7)
        
        # High support load = higher risk
        if metrics['support_tickets'] > 8:
            risk_score += 20
        elif metrics['support_tickets'] > 5:
            risk_score += 15
        elif metrics['support_tickets'] > 3:
            risk_score += 10
        
        # Low feature adoption = higher risk
        if metrics['feature_adoption'] < 30:
            risk_score += 15
        elif metrics['feature_adoption'] < 50:
            risk_score += 10
        
        # Low NPS = higher risk
        if metrics['nps_score'] <= 6:
            risk_score += 15
        elif metrics['nps_score'] <= 7:
            risk_score += 10
        
        # Inactivity = higher risk
        if metrics['last_login_days'] > 14:
            risk_score += 10
        elif metrics['last_login_days'] > 7:
            risk_score += 5
        
        return min(100, risk_score)

    def _get_health_recommendations(self, health_score: int, metrics: Dict[str, Any]) -> List[str]:
        """Получение рекомендаций на основе health score"""
        recommendations = []
        
        if health_score >= 80:
            recommendations.extend([
                "Maintain excellent relationship",
                "Identify upsell opportunities", 
                "Request case study/testimonial",
                "Explore referral potential"
            ])
        elif health_score >= 60:
            recommendations.extend([
                "Regular check-ins to maintain satisfaction",
                "Monitor engagement trends",
                "Proactive feature education"
            ])
        elif health_score >= 40:  
            recommendations.extend([
                "Schedule urgent stakeholder meeting",
                "Review and optimize current strategy",
                "Address immediate pain points"
            ])
        else:
            recommendations.extend([
                "Emergency client save protocol",
                "C-level escalation required", 
                "Comprehensive account review",
                "Consider retention offers"
            ])
        
        # Specific recommendations based on weak areas
        if metrics['engagement_score'] < 60:
            recommendations.append("Improve dashboard engagement through training")
        if metrics['payment_delays'] > 1:
            recommendations.append("Address payment process concerns")
        if metrics['support_tickets'] > 5:
            recommendations.append("Investigate recurring support issues")
        if metrics['nps_score'] < 7:
            recommendations.append("Conduct satisfaction survey and feedback session")
        
        return recommendations

    def _identify_warning_signals(self, metrics: Dict[str, Any]) -> List[str]:
        """Идентификация предупреждающих сигналов"""
        warnings = []
        
        if metrics['engagement_score'] < 50:
            warnings.append("Low dashboard engagement")
        if metrics['payment_delays'] > 2:
            warnings.append("Recurring payment delays")
        if metrics['support_tickets'] > 7:
            warnings.append("High support ticket volume")
        if metrics['last_login_days'] > 14:
            warnings.append("Extended period of inactivity")
        if metrics['nps_score'] <= 6:
            warnings.append("Low satisfaction score")
        
        return warnings

    def _create_retention_plan(self, risk_level: str, warnings: List[str]) -> Dict[str, Any]:
        """Создание плана удержания клиента"""
        if risk_level == "low":
            return {
                "timeline": "30 days",
                "actions": ["Monthly check-in", "Success story sharing", "Feature education"],
                "owner": "CSM",
                "budget": 0
            }
        elif risk_level == "medium":
            return {
                "timeline": "14 days", 
                "actions": ["Executive meeting", "Strategy review", "Quick wins identification"],
                "owner": "CSM + Account Director",
                "budget": 50000
            }
        elif risk_level == "high":
            return {
                "timeline": "7 days",
                "actions": ["Emergency audit", "Senior escalation", "Custom solutions"],
                "owner": "Account Director + VP",
                "budget": 150000
            }
        else:  # critical
            return {
                "timeline": "3 days",
                "actions": ["C-suite escalation", "Complete strategy overhaul", "Win-back campaign"],
                "owner": "VP + CEO",
                "budget": 300000
            }

    def _create_upsell_recommendations(self, opportunities: List[Dict]) -> List[str]:
        """Создание рекомендаций по upsell"""
        if not opportunities:
            return ["No immediate upsell opportunities identified"]
        
        recommendations = []
        
        # Топ-1 opportunity
        top_opp = opportunities[0]
        recommendations.append(f"Priority: {top_opp['package']} (+{top_opp['value']:,} ₽/мес)")
        
        # Если есть высокие fit scores
        high_fit_opps = [o for o in opportunities if o['fit_score'] > 0.65]
        if len(high_fit_opps) > 1:
            recommendations.append(f"Bundle opportunity: {len(high_fit_opps)} services with high fit")
        
        # Timing recommendations
        if any(o['fit_score'] > 0.75 for o in opportunities):
            recommendations.append("Timing: Ready for immediate upsell presentation")
        else:
            recommendations.append("Timing: Nurture relationship before upsell approach")
        
        return recommendations

    def _get_onboarding_next_steps(self, phase: str, progress: float) -> List[str]:
        """Получение следующих шагов для онбординга"""
        if phase == "foundation":
            if progress < 50:
                return [
                    "Accelerate initial audit completion",
                    "Schedule stakeholder alignment meeting",
                    "Establish baseline metrics tracking"
                ]
            else:
                return [
                    "Finalize strategy approval",
                    "Prepare implementation roadmap",
                    "Set up communication cadence"
                ]
        elif phase == "implementation":
            if progress < 70:
                return [
                    "Focus on critical technical fixes",
                    "Accelerate content production",
                    "Enhance client team training"
                ]
            else:
                return [
                    "Monitor early performance indicators",
                    "Prepare optimization recommendations", 
                    "Plan success celebration activities"
                ]
        else:  # optimization
            return [
                "Conduct comprehensive performance review",
                "Identify strategy refinement opportunities",
                "Prepare for transition to regular operations",
                "Document lessons learned and best practices"
            ]

    def _get_strategic_recommendations(self, health_analysis: Dict, churn_analysis: Dict, upsell_analysis: Dict) -> List[str]:
        """Получение стратегических рекомендаций"""
        recommendations = []
        
        # Health-based recommendations
        if health_analysis['health_score'] >= 80:
            recommendations.append("Champion client: Focus on case studies and referrals")
        elif health_analysis['health_score'] < 40:
            recommendations.append("Critical attention required: Immediate intervention plan")
        
        # Churn-based recommendations  
        if churn_analysis['churn_score'] > 60:
            recommendations.append("High churn risk: Execute retention protocol immediately")
        
        # Upsell-based recommendations
        if upsell_analysis['expansion_percentage'] > 30:
            recommendations.append("Significant upsell potential: Prepare expansion proposal")
        elif upsell_analysis['opportunities_count'] == 0:
            recommendations.append("Limited expansion: Focus on retention and satisfaction")
        
        return recommendations

    def _determine_priority_level(self, overall_score: float) -> str:
        """Определение уровня приоритета клиента"""
        if overall_score >= 80:
            return "champion"
        elif overall_score >= 60:
            return "standard"
        elif overall_score >= 40:
            return "attention_required"
        else:
            return "critical"

    def get_agent_metrics(self) -> AgentMetrics:
        """Получение метрик работы агента"""
        return AgentMetrics(
            agent_name=self.name,
            agent_type="management",
            version="1.0.0",
            status="active",
            total_tasks_processed=getattr(self, '_tasks_processed', 0),
            success_rate=getattr(self, '_success_rate', 0.0),
            average_response_time=getattr(self, '_avg_response_time', 0.0),
            specialized_metrics={
                "churn_risk_threshold": self.churn_risk_threshold,
                "upsell_probability_min": self.upsell_probability_min,
                "health_score_critical": self.health_score_critical,
                "nps_target": self.nps_target
            }
        )