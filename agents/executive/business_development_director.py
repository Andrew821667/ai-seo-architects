"""
Business Development Director Agent - Executive уровень
Ответственный за развитие бизнеса, крупные сделки и стратегические партнерства
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import math

from core.base_agent import BaseAgent
from core.interfaces.data_models import LeadInput, LeadOutput

class BusinessDevelopmentDirectorAgent(BaseAgent):
    """
    Business Development Director Agent - Executive уровень

    Ответственность:
    - Управление Enterprise сделками (2.5M ₽+ MRR)
    - Стратегические партнерства и альянсы
    - Конкурентное позиционирование
    - Стратегическое планирование роста
    - Executive-level коммуникация
    """

    def __init__(self, data_provider=None, **kwargs):
        # Устанавливаем модель по умолчанию для Executive уровня, если не передана
        if 'model_name' not in kwargs:
            kwargs['model_name'] = "gpt-4o"
            
        super().__init__(
            agent_id="business_development_director",
            name="Business Development Director Agent",
            agent_level="executive",
            data_provider=data_provider,
            knowledge_base="knowledge/executive/business_development_director.md",
            **kwargs
        )

        # ✅ ДОБАВЛЯЕМ ИНИЦИАЛИЗАЦИЮ STATS
        self.stats = {
            'total_tasks': 0,
            'success_count': 0,
            'error_count': 0,
            'total_processing_time': 0.0
        }

        # Executive-specific конфигурация
        self.min_enterprise_deal_size = 2500000  # 2.5M ₽/месяц (Enterprise)  # 2.5M ₽+ MRR minimum
        self.strategic_partnership_threshold = 10000000  # 10M ₽ (Стратегическое партнерство)  # 10M ₽+ for strategic partnerships
        self.executive_approval_threshold = 5000000  # 5M ₽ (Требует одобрения руководства)  # 5M ₽+ requires executive approval

        # Industry expertise mapping
        self.industry_expertise = {
            'technology': {
                'weight': 0.9,
                'specialization': ['saas', 'fintech', 'healthtech', 'edtech'],
                'average_deal_size': 7500000,  # 7.5M ₽ средняя сделка
                'sales_cycle_months': 8
            },
            'ecommerce': {
                'weight': 0.85,
                'specialization': ['retail', 'marketplace', 'b2b_ecommerce'],
                'average_deal_size': 60000,
                'sales_cycle_months': 6
            },
            'professional_services': {
                'weight': 0.8,
                'specialization': ['consulting', 'legal', 'accounting', 'real_estate'],
                'average_deal_size': 45000,
                'sales_cycle_months': 9
            },
            'healthcare': {
                'weight': 0.75,
                'specialization': ['hospitals', 'pharma', 'medical_devices'],
                'average_deal_size': 85000,
                'sales_cycle_months': 12
            },
            'financial_services': {
                'weight': 0.8,
                'specialization': ['banking', 'insurance', 'investment'],
                'average_deal_size': 95000,
                'sales_cycle_months': 10
            }
        }

        # Success metrics tracking
        self.kpi_targets = {
            'arr_growth': 0.40,  # 40% annual growth target
            'average_deal_size': 7500000,  # 7.5M ₽ средняя сделка  # 7.5M ₽+ target
            'enterprise_win_rate': 0.35,  # 35% win rate for enterprise
            'partnership_revenue_mix': 0.20,  # 20% from partnerships
            'customer_ltv': 500000,  # ₽500K+ LTV target
            'sales_cycle_months': 8  # 8 month average cycle
        }

        print(f"🎯 {self.name} инициализирован:")
        print(f"💰 Мин Enterprise сделка: {self.min_enterprise_deal_size:,.0f} ₽/месяц")
        print(f"  🤝 Порог партнерства: {self.strategic_partnership_threshold:,.0f} ₽")
        print(f"  🏢 Industry Expertise: {len(self.industry_expertise)} verticals")
        print(f"  📊 Target ARR Growth: {self.kpi_targets['arr_growth']*100}%")

    def get_system_prompt(self) -> str:
        """Специализированный системный промпт для Business Development Director"""
        return f"""Ты - Executive Business Development Director в SEO-агентстве высшего уровня, специалист по enterprise-сделкам 2.5M+ ₽ MRR.

ТВОЯ ЭКСПЕРТИЗА:
• Enterprise Sales Excellence - 35%
  - Fortune 500/крупные корпорации России
  - Сделки 2.5M-15M ₽ MRR
  - Многоуровневая enterprise квалификация
  - Executive-level презентации и переговоры

• Strategic Partnerships & Alliances - 30%  
  - Стратегические альянсы 10M+ ₽
  - Technology partnerships
  - Referral programs
  - Channel partner development

• Competitive Intelligence & Positioning - 20%
  - Market leadership analysis
  - Competitive differentiation
  - Strategic positioning
  - Industry expertise mapping

• Revenue Strategy & Growth - 15%
  - ARR optimization strategies
  - LTV/CAC optimization  
  - Revenue forecasting
  - Market expansion planning

ТВОИ KPI TARGETS:
- ARR Growth: {self.kpi_targets['arr_growth']*100}% annually
- Average Deal Size: {self.kpi_targets['average_deal_size']:,.0f} ₽
- Enterprise Win Rate: {self.kpi_targets['enterprise_win_rate']*100}%
- Customer LTV: {self.kpi_targets['customer_ltv']:,.0f}+ ₽

ОТРАСЛЕВАЯ ЭКСПЕРТИЗА:
{chr(10).join([f"• {industry.title()}: {data['weight']*100:.0f}% expertise, {data['sales_cycle_months']}м cycle" 
               for industry, data in self.industry_expertise.items()])}

EXECUTIVE DECISION CRITERIA:
- Minimum Enterprise Deal: {self.min_enterprise_deal_size:,.0f} ₽/месяц
- Strategic Partnership Threshold: {self.strategic_partnership_threshold:,.0f} ₽
- Executive Approval Required: {self.executive_approval_threshold:,.0f}+ ₽

ТВОЙ ПОДХОД:
1. Стратегический анализ enterprise возможностей
2. Competitive intelligence и positioning
3. Partnership evaluation и revenue modeling
4. Executive action plans с clear ROI
5. Long-term relationship building

ФОРМАТ ОТВЕТА (JSON):
{{
  "enterprise_assessment": {{
    "enterprise_score": "0-100",
    "deal_tier": "tier_1_enterprise/tier_2_enterprise/tier_3_enterprise",
    "strategic_value": {{}},
    "competitive_position": {{}},
    "revenue_analysis": {{}},
    "partnership_potential": {{}}
  }},
  "strategic_recommendations": [],
  "executive_action_plan": {{}},
  "deal_size": "number",
  "strategic_impact": "transformational/high/medium/low",
  "confidence_score": "0.0-1.0"
}}

Используй свою executive экспертизу для максимально точного анализа enterprise возможностей!"""

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика обработки задач Executive уровня с использованием LLM
        """
        start_time = datetime.now()

        try:
            # Извлекаем данные
            input_data = task_data.get('input_data', {})
            task_type = input_data.get('task_type', 'enterprise_assessment')

            print(f"🎯 Business Development Director обрабатывает задачу: {task_type}")

            # Формируем промпт для LLM
            user_prompt = self._create_user_prompt(task_type, input_data)
            
            # Вызываем LLM для анализа
            llm_result = await self.process_with_llm(user_prompt, task_data)
            
            if llm_result["success"]:
                # Парсим JSON ответ от LLM
                try:
                    llm_content = llm_result["result"]
                    if isinstance(llm_content, str):
                        # Пытаемся извлечь JSON из ответа
                        import re
                        json_match = re.search(r'\{.*\}', llm_content, re.DOTALL)
                        if json_match:
                            result = json.loads(json_match.group())
                        else:
                            # Если JSON не найден, создаем структурированный ответ
                            result = self._create_fallback_result(llm_content, task_type)
                    else:
                        result = llm_content
                        
                    # Дополняем результат метаданными executive уровня
                    result = self._enhance_executive_result(result, task_type, input_data)
                    
                except (json.JSONDecodeError, AttributeError) as e:
                    print(f"⚠️ Ошибка парсинга JSON от LLM: {e}")
                    # Fallback к базовой логике
                    result = await self._assess_enterprise_opportunity_fallback(task_data)
                    result["llm_parsing_error"] = str(e)
            else:
                # Fallback к базовой логике если LLM недоступен
                print(f"⚠️ LLM недоступен, используем fallback логику")
                result = await self._assess_enterprise_opportunity_fallback(task_data)
                result["fallback_mode"] = True
                result["llm_error"] = llm_result.get("error", "unknown")

            # Метрики производительности
            processing_time = (datetime.now() - start_time).total_seconds()

            # Обновляем статистику агента
            self.stats['total_tasks'] += 1
            self.stats['total_processing_time'] += processing_time
            self.stats['success_count'] += 1

            # Формируем финальный результат
            executive_result = {
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'task_type': task_type,
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': round(processing_time, 2),
                'result': result,
                'executive_level': True,
                'strategic_impact': result.get('strategic_impact', 'medium'),
                'requires_ceo_approval': safe_numeric(result.get('deal_size', 0)) > self.executive_approval_threshold,
                'success': True,
                'model_used': llm_result.get('model_used') if llm_result["success"] else None,
                'tokens_used': llm_result.get('tokens_used') if llm_result["success"] else None
            }

            print(f"✅ Executive задача завершена за {processing_time:.2f}с")
            return executive_result

        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.stats['total_tasks'] += 1
            self.stats['total_processing_time'] += processing_time
            self.stats['error_count'] += 1

            error_result = {
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'task_type': task_data.get('input_data', {}).get('task_type', 'unknown'),
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': round(processing_time, 2),
                'error': str(e),
                'executive_level': True,
                'success': False
            }

            print(f"❌ Ошибка в Executive задаче: {str(e)}")
            return error_result

    def _create_user_prompt(self, task_type: str, input_data: Dict[str, Any]) -> str:
        """Создание специализированного промпта для BD Director"""
        if task_type == 'enterprise_assessment':
            return f"""Проведи экспертную оценку Enterprise возможности:

ДАННЫЕ КОМПАНИИ:
- Название: {input_data.get('company_name', 'N/A')}
- Отрасль: {input_data.get('industry', 'N/A')}
- Годовой доход: {input_data.get('annual_revenue', 'N/A')} ₽
- Количество сотрудников: {input_data.get('employee_count', 'N/A')}
- Текущие SEO расходы: {input_data.get('current_seo_spend', 'N/A')} ₽
- Рост доходов: {input_data.get('revenue_growth_rate', 'N/A')}%
- Доля рынка: {input_data.get('market_share_percent', 'N/A')}%
- Технологический стек: {input_data.get('tech_stack', [])}
- Бренд: {input_data.get('brand_recognition', 'N/A')}
- Готовность к case study: {input_data.get('case_study_willingness', False)}

ЗАДАЧА: 
Проведи comprehensive enterprise assessment с focus на:
1. Enterprise score (0-100) с детальным обоснованием
2. Deal tier classification (tier_1/tier_2/tier_3_enterprise)
3. Strategic value analysis с учетом brand value и market influence
4. Revenue potential modeling на 3 года
5. Partnership opportunities assessment
6. Strategic recommendations для executive approach
7. Confidence score для принятия решений

Дай максимально детальный executive-level анализ в формате JSON!"""

        elif task_type == 'strategic_partnership':
            return f"""Оцени стратегическое партнерство:

ДАННЫЕ ПАРТНЕРСТВА:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

Проанализируй potential partnerships, revenue opportunities, strategic fit."""

        elif task_type == 'market_expansion':
            return f"""Проанализируй возможности расширения рынка:

ДАННЫЕ КОМПАНИИ:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

Определи best expansion opportunities в российском рынке."""

        else:
            return f"""Проведи executive analysis для задачи '{task_type}':

ВХОДНЫЕ ДАННЫЕ:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

Дай стратегический анализ с executive recommendations."""

    def _create_fallback_result(self, llm_content: str, task_type: str) -> Dict[str, Any]:
        """Создание структурированного результата из текстового ответа LLM"""
        return {
            "enterprise_assessment": {
                "enterprise_score": 75,
                "deal_tier": "tier_2_enterprise",
                "strategic_value": {"overall_strategic_value": 65},
                "competitive_position": {"competitive_strength": "strong_player"},
                "revenue_analysis": {"projected_annual_value": 5000000},
                "partnership_potential": {"partnership_score": 60}
            },
            "strategic_recommendations": [
                {"type": "executive_engagement", "priority": "high", "action": "Персональная работа BD Director"}
            ],
            "executive_action_plan": {
                "executive_involvement_level": "bd_director_oversight",
                "timeline": {"closing_timeline": "6-8 weeks"}
            },
            "deal_size": 5000000,
            "strategic_impact": "high",
            "confidence_score": 0.8,
            "llm_analysis": llm_content[:500] + "..." if len(llm_content) > 500 else llm_content,
            "analysis_method": "llm_with_fallback_parsing"
        }

    def _enhance_executive_result(self, result: Dict[str, Any], task_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Дополнение результата executive метаданными"""
        # Добавляем executive контекст
        if "enterprise_assessment" not in result:
            result["enterprise_assessment"] = {}
            
        # Определяем требуется ли одобрение CEO
        deal_size = result.get("deal_size", 0)
        result["requires_ceo_approval"] = deal_size > self.executive_approval_threshold
        
        # Добавляем industry expertise context
        industry = input_data.get("industry", "").lower()
        if industry in self.industry_expertise:
            result["industry_expertise"] = {
                "weight": self.industry_expertise[industry]["weight"],
                "sales_cycle_months": self.industry_expertise[industry]["sales_cycle_months"],
                "specialization": self.industry_expertise[industry]["specialization"]
            }
        
        # Executive decision context
        result["executive_decision_context"] = {
            "min_enterprise_deal": self.min_enterprise_deal_size,
            "strategic_partnership_threshold": self.strategic_partnership_threshold,
            "kpi_targets": self.kpi_targets
        }
        
        return result

    async def _assess_enterprise_opportunity_fallback(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback логика для оценки enterprise возможности (когда LLM недоступен)"""
        return await self._assess_enterprise_opportunity(task_data)

    async def _assess_enterprise_opportunity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Оценка Enterprise возможности с использованием executive expertise
        """
        # Умное извлечение данных (поддерживает input_data и company_data)
        if 'input_data' in data:
            # Данные пришли через process_task (input_data формат)
            company_data = data.get('input_data', {})
        else:
            # Данные пришли через прямой вызов (company_data формат)
            company_data = data.get('company_data', {})
            
        lead_analysis = data.get('lead_analysis', {})
        proposal_data = data.get('proposal_data', {})
        
        print(f"🔍 BD Director получил данные:")
        print(f"   Company: {company_data.get('company_name', 'N/A')}")
        # Безопасное форматирование revenue
        revenue_raw = company_data.get('annual_revenue', 0)
        try:
            revenue_num = float(revenue_raw) if revenue_raw else 0
        except (ValueError, TypeError):
            revenue_num = 0
        print(f"   Revenue: {revenue_num:,.0f} ₽")
        seo_spend = company_data.get('current_seo_spend', 0)
        seo_spend_num = int(seo_spend) if isinstance(seo_spend, (str, int, float)) and str(seo_spend).replace('.', '').isdigit() else 0
        print(f"   SEO Spend: {seo_spend_num:,.0f} ₽")
        print(f"   Source: {'input_data' if 'input_data' in data else 'company_data'}")

        # Enterprise квалификация
        enterprise_score = self._calculate_enterprise_score(company_data, lead_analysis)
        deal_tier = self._classify_deal_tier(enterprise_score, company_data)
        strategic_value = self._assess_strategic_value(company_data)

        # Competitive positioning analysis
        competitive_position = self._analyze_competitive_position(company_data)

        # Revenue и partnership potential
        revenue_analysis = self._analyze_revenue_potential(company_data, proposal_data)
        partnership_potential = self._evaluate_partnership_potential(company_data)

        # Strategic recommendations
        recommendations = self._generate_strategic_recommendations(
            enterprise_score, deal_tier, strategic_value, competitive_position
        )

        # Executive action plan
        action_plan = self._create_executive_action_plan(deal_tier, recommendations)

        return {
            'enterprise_assessment': {
                'enterprise_score': enterprise_score,
                'deal_tier': deal_tier,
                'strategic_value': strategic_value,
                'competitive_position': competitive_position,
                'revenue_analysis': revenue_analysis,
                'partnership_potential': partnership_potential
            },
            'strategic_recommendations': recommendations,
            'executive_action_plan': action_plan,
            'deal_size': revenue_analysis.get('projected_annual_value', 0),
            'strategic_impact': self._determine_strategic_impact(enterprise_score, strategic_value),
            'executive_approval_required': safe_numeric(revenue_analysis.get('projected_annual_value', 0)) > self.executive_approval_threshold,
            'confidence_score': self._calculate_confidence_score(enterprise_score, strategic_value)
        }

    # ✅ ДОБАВЛЯЕМ НЕДОСТАЮЩИЙ МЕТОД
    def _evaluate_partnership_potential(self, company_data: Dict) -> Dict[str, Any]:
        """
        Оценка потенциала партнерства
        """
        # Безопасная конвертация числовых значений
        def safe_numeric(value, default=0):
            try:
                return float(value) if value else default
            except (ValueError, TypeError):
                return default
        
        tech_stack = company_data.get('tech_stack', [])
        existing_partnerships = company_data.get('existing_partnerships', [])
        annual_revenue = safe_numeric(company_data.get('annual_revenue', 0))
        industry = company_data.get('industry', '').lower()

        # Базовая оценка потенциала
        base_score = 0

        # Технологический стек (влияет на интеграции)
        if len(tech_stack) >= 5:
            base_score += 30
        elif len(tech_stack) >= 3:
            base_score += 20
        else:
            base_score += 10

        # Существующие партнерства (показатель партнерской культуры)
        if len(existing_partnerships) >= 5:
            base_score += 25
        elif len(existing_partnerships) >= 2:
            base_score += 15
        else:
            base_score += 5

        # Размер компании (больше возможностей)
        if annual_revenue >= 100000000:  # ₽100M+
            base_score += 25
        elif annual_revenue >= 50000000:   # ₽50M+
            base_score += 15
        else:
            base_score += 5

        # Отраслевой множитель
        industry_multiplier = self.industry_expertise.get(industry, {}).get('weight', 1.0)
        final_score = int(base_score * industry_multiplier)

        # Определяем типы возможных партнерств
        partnership_types = []
        if len(tech_stack) >= 3:
            partnership_types.append('technology_integration')
        if len(existing_partnerships) >= 3:
            partnership_types.append('referral_program')
        if annual_revenue >= 100000000:
            partnership_types.append('strategic_alliance')

        return {
            'partnership_score': min(final_score, 100),
            'partnership_types': partnership_types,
            'referral_potential': len(existing_partnerships) * 5000,  # ₽5K per partner
            'integration_opportunities': len(tech_stack),
            'strategic_fit': 'high' if final_score >= 70 else 'medium' if final_score >= 40 else 'low',
            'estimated_revenue_potential': final_score * 1000  # ₽1K per score point
        }

    def _calculate_enterprise_score(self, company_data: Dict, lead_analysis: Dict) -> int:
        """
        Расчет Enterprise score с executive-level критериями  
        """
        # Безопасная конвертация числовых значений
        def safe_numeric(value, default=0):
            try:
                return float(value) if value else default
            except (ValueError, TypeError):
                return default
        
        score = 0

        # 1. Deal Size Assessment (30% веса)
        annual_revenue = safe_numeric(company_data.get('annual_revenue', 0))
        if annual_revenue >= 1000000000:  # ₽1B+ revenue
            score += 30
        elif annual_revenue >= 500000000:  # ₽500M+ revenue
            score += 25
        elif annual_revenue >= 100000000:  # ₽100M+ revenue
            score += 20
        elif annual_revenue >= 50000000:   # ₽50M+ revenue
            score += 15
        else:
            score += min(annual_revenue / 50000000 * 15, 15)

        # 2. Strategic Value (25% веса)
        industry = company_data.get('industry', '').lower()
        brand_recognition = company_data.get('brand_recognition', 'unknown')

        if industry in self.industry_expertise:
            industry_weight = self.industry_expertise[industry]['weight']
            score += 10 * industry_weight

        brand_score = {
            'fortune_500': 10, 'industry_leader': 8, 'well_known': 6,
            'regional_leader': 4, 'emerging': 2, 'unknown': 0
        }.get(brand_recognition, 0)
        score += brand_score

        # 3. Growth Potential (15% веса)
        growth_rate = safe_numeric(company_data.get('revenue_growth_rate', 0))
        if growth_rate >= 0.5:
            score += 15
        elif growth_rate >= 0.3:
            score += 12
        elif growth_rate >= 0.15:
            score += 8
        else:
            score += max(growth_rate * 15, 0)

        # 4. Partnership & Tech (15% веса)
        tech_stack = len(company_data.get('tech_stack', []))
        partnerships = len(company_data.get('existing_partnerships', []))
        score += min(tech_stack * 2 + partnerships * 1.5, 15)

        # 5. Market Position (15% веса)
        market_share = safe_numeric(company_data.get('market_share_percent', 0))
        score += min(market_share, 15)

        return min(int(score), 100)

    def _classify_deal_tier(self, enterprise_score: int, company_data: Dict) -> str:
        """Классификация уровня сделки"""
        # Безопасная конвертация числовых значений
        def safe_numeric(value, default=0):
            try:
                return float(value) if value else default
            except (ValueError, TypeError):
                return default
        
        annual_revenue = safe_numeric(company_data.get('annual_revenue', 0))

        if enterprise_score >= 90 and annual_revenue >= 1000000000:
            return 'tier_1_enterprise'  # 10M ₽+ MRR potential
        elif enterprise_score >= 70 and annual_revenue >= 100000000:
            return 'tier_2_enterprise'  # ₽50-100K MRR
        elif enterprise_score >= 50 and annual_revenue >= 50000000:
            return 'tier_3_enterprise'  # ₽25-50K MRR
        elif enterprise_score >= 30:
            return 'future_potential'   # ₽10-25K MRR
        else:
            return 'not_qualified'

    def _assess_strategic_value(self, company_data: Dict) -> Dict[str, Any]:
        """Оценка стратегической ценности"""
        brand_score = self._calculate_brand_value(company_data)
        market_influence = safe_numeric(company_data.get('market_share_percent', 0)) * 2
        reference_potential = 50 if company_data.get('case_study_willingness', False) else 20

        return {
            'brand_value_score': brand_score,
            'market_influence_score': min(market_influence, 100),
            'reference_potential_score': reference_potential,
            'overall_strategic_value': (brand_score + market_influence + reference_potential) / 3
        }

    def _calculate_brand_value(self, company_data: Dict) -> int:
        """Расчет ценности бренда"""
        score = 0
        brand_recognition = company_data.get('brand_recognition', 'unknown')
        
        score += {
            'fortune_500': 40, 'industry_leader': 30, 'well_known': 20,
            'regional_leader': 10, 'emerging': 5, 'unknown': 0
        }.get(brand_recognition, 0)

        # Media presence
        media_mentions = safe_numeric(company_data.get('annual_media_mentions', 0))
        score += min(media_mentions / 100 * 20, 20)

        # Social influence  
        social_followers = safe_numeric(company_data.get('social_media_followers', 0))
        score += min(social_followers / 100000 * 15, 15)

        # Awards
        awards = len(company_data.get('industry_awards', []))
        score += min(awards * 5, 25)

        return min(score, 100)

    def _analyze_competitive_position(self, company_data: Dict) -> Dict[str, Any]:
        """Анализ конкурентной позиции"""
        market_share = safe_numeric(company_data.get('market_share_percent', 0))
        
        if market_share >= 25:
            competitive_strength = 'market_leader'
        elif market_share >= 10:
            competitive_strength = 'strong_player'
        elif market_share >= 5:
            competitive_strength = 'established_player'
        else:
            competitive_strength = 'niche_player'

        return {
            'competitive_strength': competitive_strength,
            'market_share_percent': market_share,
            'competitor_count': len(company_data.get('main_competitors', [])),
            'technology_advantages': company_data.get('technology_advantages', []),
            'patent_portfolio': safe_numeric(company_data.get('patent_count', 0))
        }

    def _analyze_revenue_potential(self, company_data: Dict, proposal_data: Dict) -> Dict[str, Any]:
        """Анализ потенциала дохода"""
        base_annual_value = proposal_data.get('total_annual_investment', 0)
        
        # Enterprise multipliers
        employee_count = safe_numeric(company_data.get('employee_count', 0))
        if employee_count >= 10000:
            multiplier = 2.5
        elif employee_count >= 1000:
            multiplier = 2.0
        elif employee_count >= 500:
            multiplier = 1.5
        else:
            multiplier = 1.2

        projected_year_1 = base_annual_value * multiplier
        growth_rate = safe_numeric(company_data.get('revenue_growth_rate', 0.2))
        projected_year_2 = projected_year_1 * (1 + growth_rate)
        projected_year_3 = projected_year_2 * (1 + growth_rate * 0.8)

        return {
            'base_annual_value': base_annual_value,
            'projected_year_1': projected_year_1,
            'projected_year_2': projected_year_2, 
            'projected_year_3': projected_year_3,
            'three_year_total': projected_year_1 + projected_year_2 + projected_year_3,
            'projected_annual_value': projected_year_1,
            'lifetime_value_estimate': (projected_year_1 + projected_year_2 + projected_year_3) * 1.5
        }

    def _generate_strategic_recommendations(self, enterprise_score: int, deal_tier: str,
                                          strategic_value: Dict, competitive_position: Dict) -> List[Dict[str, Any]]:
        """Генерация стратегических рекомендаций"""
        recommendations = []

        if deal_tier == 'tier_1_enterprise':
            recommendations.append({
                'type': 'executive_engagement',
                'priority': 'critical',
                'action': 'Немедленная персональная работа Business Development Director',
                'timeline': '24 hours'
            })

        if strategic_value.get('overall_strategic_value', 0) >= 70:
            recommendations.append({
                'type': 'strategic_partnership',
                'priority': 'high', 
                'action': 'Исследовать возможности стратегического партнерства',
                'timeline': '1 month'
            })

        if enterprise_score >= 70:
            recommendations.append({
                'type': 'competitive_differentiation',
                'priority': 'medium',
                'action': 'Подчеркнуть competitive advantages в presentation', 
                'timeline': '1 week'
            })

        return recommendations

    def _create_executive_action_plan(self, deal_tier: str, recommendations: List[Dict]) -> Dict[str, Any]:
        """Создание executive action plan"""
        involvement_levels = {
            'tier_1_enterprise': 'direct_bd_director',
            'tier_2_enterprise': 'bd_director_oversight', 
            'tier_3_enterprise': 'bd_director_consultation',
            'future_potential': 'sales_ops_with_bd_input',
            'not_qualified': 'standard_sales_process'
        }

        timeline_maps = {
            'tier_1_enterprise': '6-8 weeks total',
            'tier_2_enterprise': '5-7 weeks total',
            'tier_3_enterprise': '4-5 weeks total'
        }

        return {
            'executive_involvement_level': involvement_levels.get(deal_tier, 'standard_sales_process'),
            'timeline': {'closing_timeline': timeline_maps.get(deal_tier, '4-5 weeks total')},
            'success_criteria': {'minimum_deal_size': self.min_enterprise_deal_size}
        }

    def _determine_strategic_impact(self, enterprise_score: int, strategic_value: Dict) -> str:
        """Определение уровня стратегического воздействия"""
        overall_strategic_value = strategic_value.get('overall_strategic_value', 0)

        if enterprise_score >= 90 and overall_strategic_value >= 80:
            return 'transformational'
        elif enterprise_score >= 70 and overall_strategic_value >= 60:
            return 'high'
        elif enterprise_score >= 50 and overall_strategic_value >= 40:
            return 'medium'
        else:
            return 'low'

    def _calculate_confidence_score(self, enterprise_score: int, strategic_value: Dict) -> float:
        """Расчет уверенности в executive assessment"""
        base_confidence = min(enterprise_score / 100, 1.0)
        strategic_confidence = min(strategic_value.get('overall_strategic_value', 0) / 100, 1.0)
        experience_bonus = 0.1  # Executive опыт
        
        confidence = (base_confidence * 0.6 + strategic_confidence * 0.4) + experience_bonus
        return min(confidence, 1.0)

    # Partnership evaluation methods (заглушки для других типов задач)
    async def _evaluate_partnership_opportunity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Оценка возможности партнерства"""
        return {
            'partnership_type': 'strategic_alliance',
            'opportunity_score': 75,
            'revenue_potential': 150000,
            'recommendation': 'proceed_with_pilot'
        }

    async def _conduct_competitive_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Проведение конкурентного анализа"""
        return {
            'competitive_landscape': 'highly_competitive',
            'our_position': 'strong_challenger',
            'key_differentiators': ['ai_technology', 'enterprise_focus']
        }

    async def _analyze_market_expansion(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """ИСПРАВЛЕННАЯ ФУНКЦИЯ: Анализ возможностей расширения рынка"""
        
        # Правильное извлечение данных
        if "company_data" in data:
            company_data = data["company_data"]
        elif "input_data" in data and "company_data" in data["input_data"]:
            company_data = data["input_data"]["company_data"]
        elif "input_data" in data:
            company_data = data["input_data"]
        else:
            company_data = data
        current_industry = company_data.get("industry", "unknown")
        annual_revenue = safe_numeric(company_data.get("annual_revenue", 0))
        
        # Российские рынки для экспансии
        russian_markets = {
            "fintech": {
                "size_rub": 2500000000000,  # 2.5 трлн рублей
                "growth_rate": 25,
                "competition": "высокая",
                "entry_timeline": "18-24 месяца"
            },
            "ecommerce": {
                "size_rub": 4000000000000,  # 4 трлн рублей
                "growth_rate": 20,
                "competition": "очень высокая",
                "entry_timeline": "12-18 месяцев"
            },
            "manufacturing": {
                "size_rub": 15000000000000,  # 15 трлн рублей
                "growth_rate": 8,
                "competition": "средняя",
                "entry_timeline": "24-36 месяцев"
            },
            "retail": {
                "size_rub": 6000000000000,  # 6 трлн рублей
                "growth_rate": 12,
                "competition": "высокая",
                "entry_timeline": "12-24 месяца"
            },
            "government": {
                "size_rub": 8000000000000,  # 8 трлн рублей
                "growth_rate": 5,
                "competition": "низкая",
                "entry_timeline": "36-48 месяцев"
            }
        }
        
        # Определяем наиболее привлекательные рынки
        expansion_opportunities = []
        for market, market_data in russian_markets.items():
            if market != current_industry:  # Исключаем текущую отрасль
                # Потенциальная доля рынка (консервативная оценка)
                potential_share = min(0.001, annual_revenue / market_data["size_rub"])
                potential_revenue = market_data["size_rub"] * potential_share
                
                opportunity_score = (
                    market_data["growth_rate"] * 0.4 +  # Рост важнее всего
                    (100 if market_data["competition"] == "низкая" else
                     60 if market_data["competition"] == "средняя" else 30) * 0.3 +  # Конкуренция
                    (potential_revenue / 1000000000) * 0.3  # Размер возможности
                )
                
                expansion_opportunities.append({
                    "market": market,
                    "market_size_rub": market_data["size_rub"],
                    "growth_rate_percent": market_data["growth_rate"],
                    "competition_level": market_data["competition"],
                    "entry_timeline": market_data["entry_timeline"],
                    "potential_revenue_3yr": potential_revenue * 3,
                    "opportunity_score": round(opportunity_score, 1),
                    "recommended": opportunity_score > 50
                })
        
        # Сортируем по привлекательности
        expansion_opportunities.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return {
            "analysis_type": "market_expansion",
            "current_industry": current_industry,
            "total_addressable_market_rub": sum(m["size_rub"] for m in russian_markets.values()),
            "expansion_opportunities": expansion_opportunities,
            "top_recommendation": expansion_opportunities[0] if expansion_opportunities else None,
            "investment_estimate_rub": max(50000000, annual_revenue * 0.1),  # Мин 50М или 10% дохода
            "expected_roi_3yr": 2.8,
            "success_probability": 0.72,
            "key_risks": [
                "Регулятивные изменения",
                "Конкурентная борьба",
                "Экономическая нестабильность"
            ],
            "next_steps": [
                "Детальное исследование рынка",
                "Поиск стратегических партнеров",
                "Пилотный проект в выбранной отрасли"
            ]
        }

    async def _develop_executive_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Разработка исполнительной стратегии"""
        return {
            'strategic_priorities': ['market_leadership', 'technology_innovation'],
            'timeline': '24_months',
            'success_metrics': ['market_share_growth', 'revenue_per_employee']
        }
