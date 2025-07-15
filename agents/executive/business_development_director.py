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
    - Управление Enterprise сделками ($25K+ MRR)
    - Стратегические партнерства и альянсы
    - Конкурентное позиционирование
    - Стратегическое планирование роста
    - Executive-level коммуникация
    """

    def __init__(self, data_provider=None, **kwargs):
        super().__init__(
            agent_id="business_development_director",
            name="Business Development Director Agent",
            data_provider=data_provider,
            knowledge_base="knowledge/executive/business_development_director.md",
            model_name="gpt-4o",  # Executive уровень использует лучшую модель
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
        self.min_enterprise_deal_size = 25000  # $25K+ MRR minimum
        self.strategic_partnership_threshold = 100000  # $100K+ for strategic partnerships
        self.executive_approval_threshold = 50000  # $50K+ requires executive approval

        # Industry expertise mapping
        self.industry_expertise = {
            'technology': {
                'weight': 0.9,
                'specialization': ['saas', 'fintech', 'healthtech', 'edtech'],
                'average_deal_size': 75000,
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
            'average_deal_size': 75000,  # $75K+ target
            'enterprise_win_rate': 0.35,  # 35% win rate for enterprise
            'partnership_revenue_mix': 0.20,  # 20% from partnerships
            'customer_ltv': 500000,  # $500K+ LTV target
            'sales_cycle_months': 8  # 8 month average cycle
        }

        print(f"🎯 {self.name} инициализирован:")
        print(f"  💰 Min Enterprise Deal: ${self.min_enterprise_deal_size:,}/month")
        print(f"  🤝 Strategic Partnership Threshold: ${self.strategic_partnership_threshold:,}")
        print(f"  🏢 Industry Expertise: {len(self.industry_expertise)} verticals")
        print(f"  📊 Target ARR Growth: {self.kpi_targets['arr_growth']*100}%")

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика обработки задач Executive уровня
        """
        start_time = datetime.now()

        try:
            # Извлекаем данные
            input_data = task_data.get('input_data', {})
            task_type = input_data.get('task_type', 'enterprise_assessment')

            print(f"🎯 Обработка задачи Executive уровня: {task_type}")

            # Роутинг по типам задач
            if task_type == 'enterprise_assessment':
                result = await self._assess_enterprise_opportunity(input_data)
            elif task_type == 'strategic_partnership':
                result = await self._evaluate_partnership_opportunity(input_data)
            elif task_type == 'competitive_analysis':
                result = await self._conduct_competitive_analysis(input_data)
            elif task_type == 'market_expansion':
                result = await self._analyze_market_expansion(input_data)
            elif task_type == 'executive_strategy':
                result = await self._develop_executive_strategy(input_data)
            else:
                # Default: Enterprise opportunity assessment
                result = await self._assess_enterprise_opportunity(input_data)

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
                'requires_ceo_approval': result.get('deal_size', 0) > self.executive_approval_threshold,
                'success': True
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

    async def _assess_enterprise_opportunity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Оценка Enterprise возможности с использованием executive expertise
        """
        # Извлекаем данные о компании
        company_data = data.get('company_data', {})
        lead_analysis = data.get('lead_analysis', {})
        proposal_data = data.get('proposal_data', {})

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
            'executive_approval_required': revenue_analysis.get('projected_annual_value', 0) > self.executive_approval_threshold,
            'confidence_score': self._calculate_confidence_score(enterprise_score, strategic_value)
        }

    # ✅ ДОБАВЛЯЕМ НЕДОСТАЮЩИЙ МЕТОД
    def _evaluate_partnership_potential(self, company_data: Dict) -> Dict[str, Any]:
        """
        Оценка потенциала партнерства
        """
        tech_stack = company_data.get('tech_stack', [])
        existing_partnerships = company_data.get('existing_partnerships', [])
        annual_revenue = company_data.get('annual_revenue', 0)
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
        if annual_revenue >= 100000000:  # $100M+
            base_score += 25
        elif annual_revenue >= 50000000:   # $50M+
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
            'referral_potential': len(existing_partnerships) * 5000,  # $5K per partner
            'integration_opportunities': len(tech_stack),
            'strategic_fit': 'high' if final_score >= 70 else 'medium' if final_score >= 40 else 'low',
            'estimated_revenue_potential': final_score * 1000  # $1K per score point
        }

    def _calculate_enterprise_score(self, company_data: Dict, lead_analysis: Dict) -> int:
        """
        Расчет Enterprise score с executive-level критериями  
        """
        score = 0

        # 1. Deal Size Assessment (30% веса)
        annual_revenue = company_data.get('annual_revenue', 0)
        if annual_revenue >= 1000000000:  # $1B+ revenue
            score += 30
        elif annual_revenue >= 500000000:  # $500M+ revenue
            score += 25
        elif annual_revenue >= 100000000:  # $100M+ revenue
            score += 20
        elif annual_revenue >= 50000000:   # $50M+ revenue
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
        growth_rate = company_data.get('revenue_growth_rate', 0)
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
        market_share = company_data.get('market_share_percent', 0)
        score += min(market_share, 15)

        return min(int(score), 100)

    def _classify_deal_tier(self, enterprise_score: int, company_data: Dict) -> str:
        """Классификация уровня сделки"""
        annual_revenue = company_data.get('annual_revenue', 0)

        if enterprise_score >= 90 and annual_revenue >= 1000000000:
            return 'tier_1_enterprise'  # $100K+ MRR potential
        elif enterprise_score >= 70 and annual_revenue >= 100000000:
            return 'tier_2_enterprise'  # $50-100K MRR
        elif enterprise_score >= 50 and annual_revenue >= 50000000:
            return 'tier_3_enterprise'  # $25-50K MRR
        elif enterprise_score >= 30:
            return 'future_potential'   # $10-25K MRR
        else:
            return 'not_qualified'

    def _assess_strategic_value(self, company_data: Dict) -> Dict[str, Any]:
        """Оценка стратегической ценности"""
        brand_score = self._calculate_brand_value(company_data)
        market_influence = company_data.get('market_share_percent', 0) * 2
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
        media_mentions = company_data.get('annual_media_mentions', 0)
        score += min(media_mentions / 100 * 20, 20)

        # Social influence  
        social_followers = company_data.get('social_media_followers', 0)
        score += min(social_followers / 100000 * 15, 15)

        # Awards
        awards = len(company_data.get('industry_awards', []))
        score += min(awards * 5, 25)

        return min(score, 100)

    def _analyze_competitive_position(self, company_data: Dict) -> Dict[str, Any]:
        """Анализ конкурентной позиции"""
        market_share = company_data.get('market_share_percent', 0)
        
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
            'patent_portfolio': company_data.get('patent_count', 0)
        }

    def _analyze_revenue_potential(self, company_data: Dict, proposal_data: Dict) -> Dict[str, Any]:
        """Анализ потенциала дохода"""
        base_annual_value = proposal_data.get('total_annual_investment', 0)
        
        # Enterprise multipliers
        employee_count = company_data.get('employee_count', 0)
        if employee_count >= 10000:
            multiplier = 2.5
        elif employee_count >= 1000:
            multiplier = 2.0
        elif employee_count >= 500:
            multiplier = 1.5
        else:
            multiplier = 1.2

        projected_year_1 = base_annual_value * multiplier
        growth_rate = company_data.get('revenue_growth_rate', 0.2)
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
        """Анализ расширения рынка"""
        return {
            'target_markets': ['healthcare', 'financial_services'],
            'market_size_estimate': 2500000000,
            'roi_projection': 3.5
        }

    async def _develop_executive_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Разработка исполнительной стратегии"""
        return {
            'strategic_priorities': ['market_leadership', 'technology_innovation'],
            'timeline': '24_months',
            'success_metrics': ['market_share_growth', 'revenue_per_employee']
        }
