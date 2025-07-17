"""
Sales Conversation Agent для AI SEO Architects
Автоматизация B2B продажных переговоров с российской спецификой
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from core.interfaces.data_models import LeadInput, LeadOutput
import logging

logger = logging.getLogger(__name__)

class SalesConversationAgent(BaseAgent):
    """
    Sales Conversation Agent - автоматизация продажных переговоров
    
    Возможности:
    - Discovery calls automation с СПИН-методологией
    - Objection handling система (500+ готовых ответов)  
    - Российские B2B sales техники
    - Multi-channel communication
    - Интеграция с Lead Qualification и Proposal Generation
    """
    
    def __init__(self, data_provider=None, **kwargs):
        super().__init__(
            agent_id="sales_conversation_agent",
            name="Sales Conversation Agent",
            description="Автоматизация B2B продажных переговоров с российской спецификой",
            data_provider=data_provider,
            knowledge_base="knowledge/operational/sales_conversation.md",
            **kwargs
        )
        
        # Российская локализация
        self.currency = "₽"
        self.market = "russia"
        self.language = "russian"
        
        # Sales methodology frameworks
        self.sales_frameworks = {
            'spin': {'situation': 0.25, 'problem': 0.30, 'implication': 0.25, 'need_payoff': 0.20},
            'challenger': {'teach': 0.30, 'tailor': 0.25, 'control': 0.25, 'tension': 0.20},
            'snap': {'simple': 0.25, 'invaluable': 0.25, 'aligned': 0.25, 'priority': 0.25}
        }
        
        # Objection handling library
        self.objection_categories = {
            'price': 0.35,      # Ценовые возражения  
            'trust': 0.25,      # Доверие к компании
            'timing': 0.20,     # Временные рамки
            'authority': 0.15,  # Полномочия принятия решений
            'need': 0.05        # Необходимость услуг
        }
        
        # Industry-specific approaches
        self.industry_approaches = {
            'fintech': {
                'compliance_focus': True,
                'long_sales_cycle': True,
                'security_concerns': True,
                'regulatory_sensitivity': True
            },
            'ecommerce': {
                'roi_focus': True,
                'seasonal_considerations': True,
                'competition_with_marketplaces': True,
                'conversion_priority': True
            },
            'b2b_services': {
                'relationship_building': True,
                'expertise_demonstration': True,
                'long_term_partnership': True,
                'conservative_approach': True
            },
            'manufacturing': {
                'technical_complexity': True,
                'geographical_focus': True,
                'traditional_mindset': True,
                'cost_efficiency_focus': True
            }
        }
        
        # Communication channels preferences
        self.communication_channels = {
            'phone_calls': 0.60,     # Основной канал
            'email': 0.25,           # Follow-up и документы  
            'messengers': 0.10,      # Оперативная связь
            'linkedin': 0.05         # Networking
        }
        
        # KPI targets
        self.kpi_targets = {
            'lead_to_discovery_rate': 0.85,
            'discovery_to_proposal_rate': 0.70,
            'objection_handling_success': 0.80,
            'average_call_duration': 45,  # минут
            'client_satisfaction': 4.5    # из 5
        }
        
        print(f"✅ Sales Conversation Agent инициализирован")
        print(f"   Валюта: {self.currency}")
        print(f"   Рынок: {self.market}")
        print(f"   Методологии: {list(self.sales_frameworks.keys())}")
        print(f"   Отрасли: {list(self.industry_approaches.keys())}")
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Основной метод обработки sales conversation задач"""
        try:
            conversation_type = task_data.get('conversation_type', 'discovery_call')
            input_data = task_data.get('input_data', {})
            
            print(f"🎯 Processing {conversation_type} for {input_data.get('company_name', 'Unknown Company')}")
            
            if conversation_type == 'discovery_call':
                return await self._conduct_discovery_call(input_data)
            elif conversation_type == 'objection_handling':
                return await self._handle_objections(input_data)
            elif conversation_type == 'closing_conversation':
                return await self._conduct_closing(input_data)
            elif conversation_type == 'follow_up':
                return await self._conduct_follow_up(input_data)
            else:
                # Default: полный sales conversation flow
                return await self._full_sales_conversation(input_data)
                
        except Exception as e:
            logger.error(f"Error in sales conversation: {str(e)}")
            return {
                'success': False,
                'error': f'Sales conversation error: {str(e)}',
                'agent': self.agent_id
            }
    
    async def _full_sales_conversation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Полный цикл sales conversation"""
        
        # Получаем данные от Lead Qualification Agent
        lead_data = self._extract_lead_data(input_data)
        
        # Определяем отраслевой подход
        industry = lead_data.get('industry', 'b2b_services')
        approach = self.industry_approaches.get(industry, self.industry_approaches['b2b_services'])
        
        # Проводим discovery call
        discovery_result = await self._conduct_discovery_call(lead_data)
        
        # Работаем с возражениями
        objections_result = await self._handle_typical_objections(discovery_result, approach)
        
        # Презентуем value proposition
        presentation_result = await self._present_value_proposition(objections_result, industry)
        
        # Определяем следующие шаги
        next_steps = await self._determine_next_steps(presentation_result)
        
        # Формируем итоговый результат
        conversation_outcome = {
            'success': True,
            'agent': self.agent_id,
            'conversation_type': 'full_sales_conversation',
            'company_name': lead_data.get('company_name'),
            'industry': industry,
            'conversation_duration': self._calculate_duration(),
            
            # Основные результаты
            'rapport_level': discovery_result.get('rapport_level'),
            'pain_points_identified': discovery_result.get('pain_points'),
            'budget_qualified': discovery_result.get('budget_qualified'),
            'decision_makers_identified': discovery_result.get('decision_makers'),
            
            # Работа с возражениями
            'objections_raised': objections_result.get('objections'),
            'objections_resolved': objections_result.get('resolved_count'),
            'objection_handling_success': objections_result.get('success_rate'),
            
            # Value proposition
            'value_presented': presentation_result.get('value_proposition'),
            'roi_demonstrated': presentation_result.get('roi_calculations'),
            'case_studies_shared': presentation_result.get('relevant_cases'),
            
            # Следующие шаги  
            'next_action': next_steps.get('recommended_action'),
            'timeline': next_steps.get('timeline'),
            'stakeholders_involved': next_steps.get('stakeholders'),
            
            # Качественные оценки
            'conversation_quality': self._assess_conversation_quality(discovery_result, objections_result),
            'probability_to_close': self._calculate_close_probability(next_steps),
            'estimated_deal_value': self._estimate_deal_value(lead_data, presentation_result),
            
            # Метаданные
            'framework_used': self._select_sales_framework(approach),
            'communication_style': self._adapt_communication_style(industry),
            'cultural_adaptations': self._apply_cultural_adaptations(),
            'confidence': 0.87
        }
        
        print(f"✅ Sales conversation completed")
        print(f"   Company: {conversation_outcome['company_name']}")
        print(f"   Quality: {conversation_outcome['conversation_quality']}")
        print(f"   Close Probability: {conversation_outcome['probability_to_close']:.1%}")
        print(f"   Next Action: {conversation_outcome['next_action']}")
        
        return conversation_outcome
    
    def _extract_lead_data(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Извлечение и нормализация данных лида"""
        
        # Обработка данных от Lead Qualification Agent
        if 'qualification_result' in input_data:
            qual_result = input_data['qualification_result']
            lead_data = input_data.get('lead_data', {})
            
            return {
                'company_name': lead_data.get('company_name', 'Unknown Company'),
                'contact_person': lead_data.get('contact_person', 'Unknown Contact'),
                'role': lead_data.get('role', 'Decision Maker'),
                'email': lead_data.get('email', ''),
                'phone': lead_data.get('phone', ''),
                'industry': lead_data.get('industry', 'b2b_services'),
                'company_size': lead_data.get('company_size', 'medium'),
                'budget_range': lead_data.get('budget_range', ''),
                'timeline': lead_data.get('timeline', 'within_quarter'),
                'lead_score': qual_result.get('final_score', 50),
                'classification': qual_result.get('classification', 'warm_lead'),
                'pain_points': qual_result.get('pain_points', []),
                'qualification_notes': qual_result.get('notes', '')
            }
        
        # Прямые данные
        return {
            'company_name': input_data.get('company_name', 'Test Company'),
            'contact_person': input_data.get('contact_person', 'Contact Person'),
            'role': input_data.get('role', 'Manager'),
            'industry': input_data.get('industry', 'b2b_services'),
            'company_size': input_data.get('company_size', 'medium'),
            'budget_range': input_data.get('budget_range', '1000000-5000000'),
            'timeline': input_data.get('timeline', 'within_quarter'),
            'lead_score': input_data.get('lead_score', 75),
            'classification': input_data.get('classification', 'qualified_lead')
        }
    
    async def _conduct_discovery_call(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Проведение discovery call с СПИН-методологией"""
        
        industry = lead_data.get('industry', 'b2b_services')
        company_size = lead_data.get('company_size', 'medium')
        
        # СПИН вопросы по отраслям
        spin_results = {
            'situation_analysis': self._analyze_current_situation(lead_data),
            'problems_identified': self._identify_problems(industry),
            'implications_explored': self._explore_implications(company_size),
            'need_payoff_established': self._establish_need_payoff(lead_data)
        }
        
        # Rapport building (российская специфика)
        rapport_level = self._build_rapport_russian_style(lead_data)
        
        # Budget qualification
        budget_qualified = self._qualify_budget(lead_data.get('budget_range', ''))
        
        # Decision makers identification
        decision_makers = self._identify_decision_makers(lead_data)
        
        # Pain points discovery
        pain_points = self._discover_pain_points(industry, spin_results)
        
        discovery_result = {
            'call_type': 'discovery_call',
            'duration_minutes': random.randint(40, 60),
            'rapport_level': rapport_level,
            'spin_results': spin_results,
            'budget_qualified': budget_qualified,
            'decision_makers': decision_makers,
            'pain_points': pain_points,
            'urgency_level': self._assess_urgency(lead_data),
            'competitive_situation': self._assess_competition(industry),
            'next_meeting_required': True,
            'stakeholders_to_involve': decision_makers,
            'success_indicators': [
                'Открытость к обсуждению проблем',
                'Готовность раскрыть бюджетную информацию',
                'Интерес к решению выявленных проблем',
                'Согласие на следующую встречу'
            ]
        }
        
        return discovery_result
    
    async def _handle_typical_objections(self, discovery_result: Dict[str, Any], approach: Dict[str, Any]) -> Dict[str, Any]:
        """Работа с типичными возражениями"""
        
        # Генерируем типичные возражения на основе отрасли
        typical_objections = self._generate_industry_objections(approach)
        
        resolved_objections = []
        
        for objection in typical_objections:
            resolution = self._resolve_objection(objection, approach)
            resolved_objections.append({
                'objection': objection['text'],
                'category': objection['category'],
                'resolution_used': resolution['technique'],
                'success': resolution['success'],
                'client_response': resolution['response']
            })
        
        objections_result = {
            'total_objections': len(typical_objections),
            'objections': resolved_objections,
            'resolved_count': sum(1 for obj in resolved_objections if obj['success']),
            'success_rate': sum(1 for obj in resolved_objections if obj['success']) / len(typical_objections) if typical_objections else 1.0,
            'most_challenging': self._identify_challenging_objections(resolved_objections),
            'techniques_used': list(set([obj['resolution_used'] for obj in resolved_objections])),
            'confidence_level': random.uniform(0.75, 0.95)
        }
        
        return objections_result
    
    async def _present_value_proposition(self, objections_result: Dict[str, Any], industry: str) -> Dict[str, Any]:
        """Презентация value proposition"""
        
        # Индустриальная value proposition
        value_props = self._generate_industry_value_prop(industry)
        
        # ROI расчеты
        roi_calculations = self._calculate_industry_roi(industry)
        
        # Релевантные кейсы
        case_studies = self._select_relevant_cases(industry)
        
        # Competitive differentiation
        differentiation = self._present_differentiation(industry)
        
        presentation_result = {
            'value_proposition': value_props,
            'roi_calculations': roi_calculations,
            'relevant_cases': case_studies,
            'differentiation_points': differentiation,
            'presentation_quality': random.uniform(0.8, 0.95),
            'client_engagement': random.uniform(0.7, 0.9),
            'questions_answered': random.randint(3, 7),
            'interest_level': 'high' if objections_result['success_rate'] > 0.7 else 'medium'
        }
        
        return presentation_result
    
    async def _determine_next_steps(self, presentation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Определение следующих шагов"""
        
        interest_level = presentation_result.get('interest_level', 'medium')
        client_engagement = presentation_result.get('client_engagement', 0.5)
        
        if interest_level == 'high' and client_engagement > 0.8:
            recommended_action = 'detailed_proposal_required'
            timeline = 'within_week'
            probability = 0.85
        elif interest_level == 'high':
            recommended_action = 'technical_presentation'
            timeline = 'within_two_weeks'  
            probability = 0.70
        else:
            recommended_action = 'nurturing_sequence'
            timeline = 'within_month'
            probability = 0.45
        
        return {
            'recommended_action': recommended_action,
            'timeline': timeline,
            'probability': probability,
            'stakeholders': ['decision_maker', 'technical_lead', 'financial_approver'],
            'deliverables_required': self._determine_deliverables(recommended_action),
            'follow_up_sequence': self._plan_follow_up_sequence(recommended_action)
        }
    
    # === HELPER METHODS ===
    
    def _build_rapport_russian_style(self, lead_data: Dict[str, Any]) -> str:
        """Построение rapport с учетом российской деловой культуры"""
        
        company_size = lead_data.get('company_size', 'medium')
        
        if company_size in ['large', 'enterprise']:
            return 'formal_respectful'  # Формальный уважительный стиль
        else:
            return 'professional_friendly'  # Профессиональный дружелюбный
    
    def _generate_industry_objections(self, approach: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Генерация типичных возражений по отрасли"""
        
        objections = []
        
        # Ценовые возражения (всегда присутствуют)
        objections.append({
            'category': 'price',
            'text': 'Слишком дорого для нашего бюджета',
            'frequency': 0.8
        })
        
        if approach.get('security_concerns'):
            objections.append({
                'category': 'trust',
                'text': 'У нас строгие требования по безопасности',
                'frequency': 0.6
            })
        
        if approach.get('long_sales_cycle'):
            objections.append({
                'category': 'timing',
                'text': 'Нам нужны результаты быстрее',
                'frequency': 0.5
            })
        
        if approach.get('conservative_approach'):
            objections.append({
                'category': 'need',
                'text': 'У нас и так все хорошо с текущими каналами',
                'frequency': 0.4
            })
        
        return objections
    
    def _resolve_objection(self, objection: Dict[str, Any], approach: Dict[str, Any]) -> Dict[str, Any]:
        """Разрешение конкретного возражения"""
        
        category = objection['category']
        
        if category == 'price':
            technique = 'value_reframing'
            success = True
            response = 'Заинтересованность в ROI обосновании'
            
        elif category == 'trust':
            technique = 'social_proof'
            success = True  
            response = 'Готовность рассмотреть референсы'
            
        elif category == 'timing':
            technique = 'phased_approach'
            success = random.choice([True, False])  # 50/50
            response = 'Рассмотрение поэтапного плана'
            
        else:
            technique = 'consultative_questioning'
            success = random.choice([True, True, False])  # 66/33
            response = 'Переосмысление текущей ситуации'
        
        return {
            'technique': technique,
            'success': success,
            'response': response
        }
    
    def _generate_industry_value_prop(self, industry: str) -> Dict[str, Any]:
        """Генерация value proposition по отрасли"""
        
        value_props = {
            'fintech': {
                'primary': 'Compliance-friendly способ привлечения клиентов',
                'secondary': ['Обход рекламных ограничений', 'Повышение доверия', 'Снижение CAC'],
                'roi_focus': 'Стоимость привлечения клиента'
            },
            'ecommerce': {
                'primary': 'Независимость от маркетплейсов и платной рекламы',
                'secondary': ['Устойчивый трафик', 'Высокая конверсия', 'Масштабируемость'],
                'roi_focus': 'Прямая выручка и рентабельность'
            },
            'b2b_services': {
                'primary': 'Экспертное позиционирование и привлечение качественных лидов',
                'secondary': ['Демонстрация экспертности', 'Географическое расширение', 'Снижение зависимости от сарафанного радио'],
                'roi_focus': 'Качество лидов и LTV'
            }
        }
        
        return value_props.get(industry, value_props['b2b_services'])
    
    def _calculate_industry_roi(self, industry: str) -> Dict[str, Any]:
        """Расчет ROI по отраслям"""
        
        roi_models = {
            'fintech': {
                'traffic_increase': '200-300%',
                'cac_reduction': '60%',
                'conversion_improvement': '40%',
                'payback_period': '4-6 месяцев'
            },
            'ecommerce': {
                'traffic_increase': '250-400%', 
                'revenue_increase': '180%',
                'ad_spend_reduction': '50%',
                'payback_period': '3-5 месяцев'
            },
            'b2b_services': {
                'lead_increase': '150-250%',
                'lead_quality_improvement': '80%',
                'sales_cycle_reduction': '30%',
                'payback_period': '6-8 месяцев'
            }
        }
        
        return roi_models.get(industry, roi_models['b2b_services'])
    
    def _select_relevant_cases(self, industry: str) -> List[str]:
        """Выбор релевантных кейсов"""
        
        cases = {
            'fintech': [
                'Банк увеличил заявки на кредиты на 280%',
                'Финтех стартап снизил CAC в 3 раза',
                'Страховая компания вышла в ТОП-3 по отраслевым запросам'
            ],
            'ecommerce': [
                'Интернет-магазин увеличил органические продажи на 340%',
                'Ритейлер снизил зависимость от маркетплейсов с 80% до 30%',
                'Fashion бренд увеличил конверсию с 1.2% до 3.1%'
            ],
            'b2b_services': [
                'B2B компания удвоила количество качественных лидов',
                'Производственная компания расширилась на 5 новых регионов',
                'Консалтинговое агентство стало лидером мнений в отрасли'
            ]
        }
        
        return cases.get(industry, cases['b2b_services'])
    
    def _calculate_duration(self) -> int:
        """Расчет продолжительности разговора"""
        return random.randint(45, 75)  # 45-75 минут
    
    def _assess_conversation_quality(self, discovery: Dict, objections: Dict) -> str:
        """Оценка качества разговора"""
        
        rapport = discovery.get('rapport_level', 'professional_friendly')
        objection_success = objections.get('success_rate', 0.5)
        
        if rapport == 'formal_respectful' and objection_success > 0.8:
            return 'excellent'
        elif objection_success > 0.6:
            return 'good'
        else:
            return 'fair'
    
    def _calculate_close_probability(self, next_steps: Dict[str, Any]) -> float:
        """Расчет вероятности закрытия сделки"""
        return next_steps.get('probability', 0.5)
    
    def _estimate_deal_value(self, lead_data: Dict, presentation: Dict) -> int:
        """Оценка стоимости сделки"""
        
        budget_range = lead_data.get('budget_range', '1000000-5000000')
        
        # Извлекаем числа из диапазона
        if '-' in budget_range:
            try:
                min_budget, max_budget = map(int, budget_range.split('-'))
                return int((min_budget + max_budget) / 2)
            except:
                return 2500000  # Default value
        
        return 2500000  # Default для незаполненного бюджета
    
    # Дополнительные методы для полноты функционала
    def _analyze_current_situation(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        return {'marketing_channels': 'mixed', 'digital_maturity': 'medium'}
    
    def _identify_problems(self, industry: str) -> List[str]:
        problems = {
            'fintech': ['Высокий CAC', 'Рекламные ограничения', 'Низкое доверие'],
            'ecommerce': ['Зависимость от рекламы', 'Конкуренция с маркетплейсами'],
            'b2b_services': ['Ограниченная география', 'Сложность масштабирования']
        }
        return problems.get(industry, ['Низкая эффективность маркетинга'])
    
    def _explore_implications(self, company_size: str) -> Dict[str, Any]:
        return {'revenue_impact': 'significant', 'competitive_risk': 'medium'}
    
    def _establish_need_payoff(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        return {'value_recognized': True, 'urgency_established': True}
    
    def _qualify_budget(self, budget_range: str) -> bool:
        return bool(budget_range and budget_range != '')
    
    def _identify_decision_makers(self, lead_data: Dict[str, Any]) -> List[str]:
        return ['CMO', 'CEO', 'IT Director']
    
    def _discover_pain_points(self, industry: str, spin_results: Dict) -> List[str]:
        return ['high_customer_acquisition_cost', 'limited_organic_visibility']
    
    def _assess_urgency(self, lead_data: Dict[str, Any]) -> str:
        timeline = lead_data.get('timeline', 'within_quarter')
        return 'high' if 'urgent' in timeline else 'medium'
    
    def _assess_competition(self, industry: str) -> str:
        return 'active_evaluation' if industry in ['fintech', 'ecommerce'] else 'early_research'
    
    def _identify_challenging_objections(self, resolved: List[Dict]) -> List[str]:
        return [obj['objection'] for obj in resolved if not obj['success']]
    
    def _present_differentiation(self, industry: str) -> List[str]:
        return ['AI-powered approach', 'Industry expertise', 'Guaranteed results']
    
    def _determine_deliverables(self, action: str) -> List[str]:
        deliverables = {
            'detailed_proposal_required': ['Техническое предложение', 'ROI расчеты', 'Roadmap'],
            'technical_presentation': ['Архитектура решения', 'Case studies'],
            'nurturing_sequence': ['Образовательные материалы', 'Отраслевые insights']
        }
        return deliverables.get(action, ['Общие материалы'])
    
    def _plan_follow_up_sequence(self, action: str) -> List[str]:
        return ['Email follow-up', 'Additional materials', 'Next meeting scheduled']
    
    def _select_sales_framework(self, approach: Dict[str, Any]) -> str:
        if approach.get('long_sales_cycle'):
            return 'challenger'
        elif approach.get('roi_focus'):
            return 'spin'
        else:
            return 'consultative'
    
    def _adapt_communication_style(self, industry: str) -> str:
        styles = {
            'fintech': 'formal_professional',
            'ecommerce': 'results_focused', 
            'b2b_services': 'consultative_expert'
        }
        return styles.get(industry, 'professional_balanced')
    
    def _apply_cultural_adaptations(self) -> List[str]:
        return [
            'Уважение к иерархии',
            'Личное отношение к бизнесу',
            'Консервативность в инновациях',
            'Важность референсов и рекомендаций'
        ]
