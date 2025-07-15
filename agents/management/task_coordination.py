"""
Task Coordination Agent - Management уровень
Ответственный за координацию задач между всеми operational агентами
"""

import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import json
import random

from core.base_agent import BaseAgent
from core.interfaces.data_models import LeadInput, LeadOutput

class TaskCoordinationAgent(BaseAgent):
    """
    Task Coordination Agent - Management уровень

    Ответственность:
    - Маршрутизация задач между operational агентами
    - Мониторинг SLA и производительности
    - Балансировка нагрузки и ресурсов
    - Координация мультиагентных процессов
    - Управление приоритетами и дедлайнами
    """

    def __init__(self, data_provider=None, **kwargs):
        super().__init__(
            agent_id="task_coordination",
            name="Task Coordination Agent",
            data_provider=data_provider,
            knowledge_base="knowledge/management/task_coordination.md",
            model_name="gpt-4o",  # Management уровень использует лучшую модель
            **kwargs
        )

        # ✅ ИНИЦИАЛИЗИРУЕМ STATS
        self.stats = {
            'total_tasks': 0,
            'success_count': 0,
            'error_count': 0,
            'total_processing_time': 0.0,
            'routing_decisions': 0,
            'sla_violations': 0,
            'coordination_success_rate': 0.95
        }

        # Конфигурация агентов системы
        self.agent_registry = {
            'lead_qualification': {
                'agent_id': 'lead_qualification',
                'level': 'operational',
                'specialization': ['lead_analysis', 'bant_scoring', 'qualification'],
                'capacity': 10,  # максимум задач одновременно
                'current_load': 0,
                'avg_processing_time': 300,  # 5 минут
                'sla_hours': 2,
                'success_rate': 0.92
            },
            'proposal_generation': {
                'agent_id': 'proposal_generation',
                'level': 'operational', 
                'specialization': ['proposals', 'pricing', 'service_packages'],
                'capacity': 8,
                'current_load': 0,
                'avg_processing_time': 600,  # 10 минут
                'sla_hours': 4,
                'success_rate': 0.89
            },
            'business_development_director': {
                'agent_id': 'business_development_director',
                'level': 'executive',
                'specialization': ['enterprise_deals', 'strategic_partnerships', 'executive_decisions'],
                'capacity': 5,
                'current_load': 0,
                'avg_processing_time': 1800,  # 30 минут
                'sla_hours': 24,
                'success_rate': 0.96
            }
        }

        # Матрица маршрутизации задач
        self.routing_matrix = {
            'lead_qualification': 'lead_qualification',
            'lead_analysis': 'lead_qualification',
            'bant_scoring': 'lead_qualification',
            'prospect_evaluation': 'lead_qualification',
            
            'proposal_generation': 'proposal_generation',
            'pricing_analysis': 'proposal_generation',
            'service_packaging': 'proposal_generation',
            'quote_creation': 'proposal_generation',
            
            'enterprise_assessment': 'business_development_director',
            'strategic_partnership': 'business_development_director',
            'competitive_analysis': 'business_development_director',
            'market_expansion': 'business_development_director',
            'executive_strategy': 'business_development_director'
        }

        # Система приоритетов (1000-балльная шкала)
        self.priority_weights = {
            'business_criticality': 0.35,  # 35%
            'time_constraints': 0.25,      # 25%
            'client_value': 0.20,          # 20%
            'task_complexity': 0.10,       # 10%
            'dependencies': 0.10           # 10%
        }

        # SLA матрица по типам задач
        self.sla_matrix = {
            'critical': {'hours': 1, 'priority_boost': 300},
            'high': {'hours': 4, 'priority_boost': 200},
            'medium': {'hours': 24, 'priority_boost': 100},
            'low': {'hours': 72, 'priority_boost': 0}
        }

        print(f"🎯 {self.name} инициализирован:")
        print(f"  📊 Зарегистрировано агентов: {len(self.agent_registry)}")
        print(f"  🎯 Типов задач в матрице: {len(self.routing_matrix)}")
        print(f"  ⚖️ Весовые коэффициенты: {len(self.priority_weights)}")
        print(f"  📈 Целевой coordination rate: {self.stats['coordination_success_rate']*100}%")

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика координации и маршрутизации задач
        """
        start_time = datetime.now()

        try:
            # Извлекаем данные
            input_data = task_data.get('input_data', {})
            task_type = input_data.get('task_type', 'route_task')

            print(f"🎯 Координация задачи типа: {task_type}")

            # Роутинг по типам координационных задач
            if task_type == 'route_task':
                result = await self._route_task(input_data)
            elif task_type == 'monitor_sla':
                result = await self._monitor_sla(input_data)
            elif task_type == 'balance_load':
                result = await self._balance_load(input_data)
            elif task_type == 'system_status':
                result = await self._get_system_status(input_data)
            elif task_type == 'escalate_issue':
                result = await self._escalate_issue(input_data)
            else:
                # Default: роутинг задачи
                result = await self._route_task(input_data)

            # Метрики производительности
            processing_time = (datetime.now() - start_time).total_seconds()

            # Обновляем статистику
            self.stats['total_tasks'] += 1
            self.stats['total_processing_time'] += processing_time
            self.stats['success_count'] += 1
            self.stats['routing_decisions'] += 1

            # Формируем результат
            coordination_result = {
                'agent_id': self.agent_id,
                'agent_name': self.name,
                'task_type': task_type,
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': round(processing_time, 2),
                'result': result,
                'management_level': True,
                'coordination_quality': self._assess_coordination_quality(result),
                'system_impact': result.get('system_impact', 'medium'),
                'success': True
            }

            print(f"✅ Координация завершена за {processing_time:.2f}с")
            return coordination_result

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
                'management_level': True,
                'success': False
            }

            print(f"❌ Ошибка координации: {str(e)}")
            return error_result

    async def _route_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Интеллектуальная маршрутизация задачи к оптимальному агенту
        """
        # Анализ входящей задачи
        task_analysis = self._analyze_incoming_task(data)
        
        # Определение целевого агента
        target_agent = self._determine_target_agent(task_analysis)
        
        # Расчет приоритета
        priority_analysis = self._calculate_priority(data, task_analysis)
        
        # Анализ capacity и нагрузки
        capacity_analysis = self._analyze_agent_capacity(target_agent)
        
        # Временной анализ и SLA
        timing_analysis = self._analyze_timing_and_sla(task_analysis, target_agent, priority_analysis)
        
        # Финальное решение маршрутизации
        routing_decision = self._make_routing_decision(
            target_agent, priority_analysis, capacity_analysis, timing_analysis
        )

        return {
            'task_analysis': task_analysis,
            'target_agent': target_agent,
            'priority_analysis': priority_analysis,
            'capacity_analysis': capacity_analysis,
            'timing_analysis': timing_analysis,
            'routing_decision': routing_decision,
            'estimated_completion': self._estimate_completion_time(target_agent, priority_analysis),
            'coordination_confidence': self._calculate_coordination_confidence(routing_decision)
        }

    def _analyze_incoming_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ входящей задачи"""
        original_task_type = data.get('original_task_type', 'unknown')
        task_data = data.get('task_data', {})
        client_info = data.get('client_info', {})
        
        # Классификация задачи
        task_category = self._classify_task_category(original_task_type)
        complexity_score = self._assess_task_complexity(task_data)
        urgency_level = self._determine_urgency(data)
        
        return {
            'original_task_type': original_task_type,
            'task_category': task_category,
            'complexity_score': complexity_score,
            'urgency_level': urgency_level,
            'client_tier': self._determine_client_tier(client_info),
            'estimated_effort': self._estimate_effort(task_data, complexity_score),
            'dependencies': self._identify_dependencies(task_data)
        }

    def _determine_target_agent(self, task_analysis: Dict[str, Any]) -> str:
        """Определение целевого агента на основе анализа задачи"""
        task_type = task_analysis['original_task_type']
        
        # Прямое соответствие из матрицы маршрутизации
        if task_type in self.routing_matrix:
            return self.routing_matrix[task_type]
        
        # Анализ по категории задачи
        task_category = task_analysis['task_category']
        
        if task_category == 'sales':
            if task_analysis['complexity_score'] >= 80:
                return 'business_development_director'  # Сложные sales задачи
            elif 'proposal' in task_type or 'pricing' in task_type:
                return 'proposal_generation'
            else:
                return 'lead_qualification'
        
        elif task_category == 'strategic':
            return 'business_development_director'
        
        elif task_category == 'operational':
            # Распределяем между operational агентами
            if 'lead' in task_type or 'qualification' in task_type:
                return 'lead_qualification'
            else:
                return 'proposal_generation'
        
        # Default fallback
        return 'lead_qualification'

    def _calculate_priority(self, data: Dict[str, Any], task_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет приоритета задачи по 1000-балльной шкале"""
        score = 0
        
        # 1. Business Criticality (35% веса = 350 баллов макс)
        urgency_level = task_analysis['urgency_level']
        criticality_score = {
            'critical': 350,
            'high': 250,
            'medium': 150,
            'low': 50
        }.get(urgency_level, 100)
        score += criticality_score
        
        # 2. Time Constraints (25% веса = 250 баллов макс)
        deadline = data.get('deadline_hours', 24)
        if deadline <= 1:
            time_score = 250
        elif deadline <= 4:
            time_score = 200
        elif deadline <= 24:
            time_score = 150
        elif deadline <= 72:
            time_score = 100
        else:
            time_score = 50
        score += time_score
        
        # 3. Client Value (20% веса = 200 баллов макс)
        client_tier = task_analysis.get('client_tier', 'standard')
        client_score = {
            'enterprise': 200,
            'premium': 150,
            'standard': 100,
            'small': 50,
            'prospect': 30
        }.get(client_tier, 50)
        score += client_score
        
        # 4. Task Complexity (10% веса = 100 баллов макс)
        complexity = task_analysis['complexity_score']
        if complexity >= 80:
            complexity_bonus = 30  # Сложные задачи получают boost
        elif complexity >= 60:
            complexity_bonus = 50  # Средне-сложные оптимальны
        elif complexity >= 40:
            complexity_bonus = 70  # Простые задачи быстро выполняются
        else:
            complexity_bonus = 100  # Очень простые = максимальный приоритет
        score += complexity_bonus
        
        # 5. Dependencies (10% веса = 100 баллов макс)
        dependencies = task_analysis.get('dependencies', [])
        if len(dependencies) == 0:
            dep_score = 100  # Независимые задачи = высокий приоритет
        elif len(dependencies) <= 2:
            dep_score = 70
        else:
            dep_score = 40  # Много зависимостей = низкий приоритет
        score += dep_score
        
        # Финальная нормализация
        final_score = min(score, 1000)
        
        # Определение категории приоритета
        if final_score >= 800:
            priority_category = 'critical'
        elif final_score >= 600:
            priority_category = 'high'
        elif final_score >= 400:
            priority_category = 'medium'
        else:
            priority_category = 'low'
        
        return {
            'calculated_priority': final_score,
            'priority_category': priority_category,
            'criticality_score': criticality_score,
            'time_score': time_score,
            'client_score': client_score,
            'complexity_bonus': complexity_bonus,
            'dependency_score': dep_score,
            'priority_breakdown': {
                'business_criticality': criticality_score / 1000,
                'time_constraints': time_score / 1000,
                'client_value': client_score / 1000,
                'task_complexity': complexity_bonus / 1000,
                'dependencies': dep_score / 1000
            }
        }

    def _analyze_agent_capacity(self, target_agent: str) -> Dict[str, Any]:
        """Анализ capacity и загрузки целевого агента"""
        if target_agent not in self.agent_registry:
            return {'error': f'Agent {target_agent} not found'}
        
        agent_info = self.agent_registry[target_agent]
        
        # Симулируем текущую загрузку (в реальной системе это бы брались из метрик)
        current_load = random.randint(0, agent_info['capacity'])
        load_percentage = (current_load / agent_info['capacity']) * 100
        
        # Обновляем загрузку в registry
        self.agent_registry[target_agent]['current_load'] = current_load
        
        # Анализ доступности
        if load_percentage >= 90:
            availability_status = 'overloaded'
            recommendation = 'consider_alternative_or_queue'
        elif load_percentage >= 75:
            availability_status = 'high_load'
            recommendation = 'monitor_closely'
        elif load_percentage >= 50:
            availability_status = 'normal_load'
            recommendation = 'proceed_normally'
        else:
            availability_status = 'low_load'
            recommendation = 'optimal_assignment'
        
        return {
            'agent_id': target_agent,
            'current_load': current_load,
            'max_capacity': agent_info['capacity'],
            'load_percentage': round(load_percentage, 1),
            'availability_status': availability_status,
            'recommendation': recommendation,
            'avg_processing_time': agent_info['avg_processing_time'],
            'success_rate': agent_info['success_rate'],
            'queue_position': current_load + 1 if current_load >= agent_info['capacity'] else 0
        }

    def _analyze_timing_and_sla(self, task_analysis: Dict, target_agent: str, priority_analysis: Dict) -> Dict[str, Any]:
        """Анализ временных рамок и SLA"""
        agent_info = self.agent_registry.get(target_agent, {})
        avg_processing_time = agent_info.get('avg_processing_time', 600)  # default 10 мин
        
        # Оценка времени выполнения с учетом сложности
        complexity_multiplier = 1 + (task_analysis['complexity_score'] / 100)
        estimated_duration = avg_processing_time * complexity_multiplier
        
        # Учет загрузки агента
        load_percentage = self._get_agent_load_percentage(target_agent)
        if load_percentage >= 75:
            queue_delay = (load_percentage - 50) * 10  # дополнительная задержка
            estimated_duration += queue_delay
        
        # SLA анализ
        priority_category = priority_analysis['priority_category']
        sla_requirements = self.sla_matrix.get(priority_category, {'hours': 24})
        sla_seconds = sla_requirements['hours'] * 3600
        
        # Вероятность соблюдения SLA
        if estimated_duration <= sla_seconds * 0.5:
            sla_compliance_probability = 0.95
        elif estimated_duration <= sla_seconds * 0.75:
            sla_compliance_probability = 0.85
        elif estimated_duration <= sla_seconds:
            sla_compliance_probability = 0.70
        else:
            sla_compliance_probability = 0.40
        
        return {
            'estimated_duration_seconds': round(estimated_duration),
            'estimated_duration_hours': round(estimated_duration / 3600, 2),
            'sla_requirement_hours': sla_requirements['hours'],
            'sla_compliance_probability': sla_compliance_probability,
            'queue_delay_factor': queue_delay if load_percentage >= 75 else 0,
            'complexity_adjustment': complexity_multiplier,
            'estimated_completion_time': (datetime.now() + timedelta(seconds=estimated_duration)).isoformat()
        }

    def _make_routing_decision(self, target_agent: str, priority_analysis: Dict, 
                              capacity_analysis: Dict, timing_analysis: Dict) -> Dict[str, Any]:
        """Принятие финального решения о маршрутизации"""
        
        # Проверяем критические условия
        if capacity_analysis['load_percentage'] >= 95:
            # Агент перегружен - ищем альтернативы
            alternative_agent = self._find_alternative_agent(target_agent, priority_analysis)
            if alternative_agent:
                decision = 'route_to_alternative'
                final_agent = alternative_agent
                reason = f'Primary agent {target_agent} overloaded, routing to {alternative_agent}'
            else:
                decision = 'queue_for_primary'
                final_agent = target_agent
                reason = f'No alternatives available, queuing for {target_agent}'
        elif timing_analysis['sla_compliance_probability'] < 0.5:
            # Низкая вероятность соблюдения SLA
            if priority_analysis['priority_category'] in ['critical', 'high']:
                decision = 'escalate_priority'
                final_agent = target_agent
                reason = 'SLA risk detected, escalating priority'
            else:
                decision = 'accept_risk'
                final_agent = target_agent
                reason = 'SLA risk acceptable for priority level'
        else:
            # Нормальная маршрутизация
            decision = 'route_normally'
            final_agent = target_agent
            reason = 'Optimal routing conditions'
        
        return {
            'decision': decision,
            'final_agent': final_agent,
            'reason': reason,
            'confidence': self._calculate_routing_confidence(capacity_analysis, timing_analysis),
            'alternative_considered': target_agent != final_agent,
            'risk_factors': self._identify_risk_factors(capacity_analysis, timing_analysis),
            'success_probability': min(
                capacity_analysis.get('success_rate', 0.9),
                timing_analysis['sla_compliance_probability']
            )
        }

    # Вспомогательные методы
    def _classify_task_category(self, task_type: str) -> str:
        """Классификация категории задачи"""
        if any(word in task_type.lower() for word in ['lead', 'qualification', 'prospect']):
            return 'sales'
        elif any(word in task_type.lower() for word in ['proposal', 'pricing', 'quote']):
            return 'sales'
        elif any(word in task_type.lower() for word in ['enterprise', 'strategic', 'partnership']):
            return 'strategic'
        else:
            return 'operational'

    def _assess_task_complexity(self, task_data: Dict) -> int:
        """Оценка сложности задачи (0-100)"""
        base_complexity = 50
        
        # Увеличиваем сложность на основе данных
        if isinstance(task_data, dict):
            if len(task_data) > 10:
                base_complexity += 20
            if any(isinstance(v, dict) for v in task_data.values()):
                base_complexity += 15
            if any(isinstance(v, list) and len(v) > 5 for v in task_data.values()):
                base_complexity += 10
        
        return min(base_complexity, 100)

    def _determine_urgency(self, data: Dict) -> str:
        """Определение уровня срочности"""
        deadline_hours = data.get('deadline_hours', 24)
        is_critical = data.get('is_critical', False)
        
        if is_critical or deadline_hours <= 1:
            return 'critical'
        elif deadline_hours <= 4:
            return 'high'
        elif deadline_hours <= 24:
            return 'medium'
        else:
            return 'low'

    def _determine_client_tier(self, client_info: Dict) -> str:
        """Определение уровня клиента"""
        monthly_value = client_info.get('monthly_value', 0)
        
        if monthly_value >= 25000:
            return 'enterprise'
        elif monthly_value >= 10000:
            return 'premium'
        elif monthly_value >= 5000:
            return 'standard'
        elif monthly_value > 0:
            return 'small'
        else:
            return 'prospect'

    def _estimate_effort(self, task_data: Dict, complexity_score: int) -> str:
        """Оценка усилий для выполнения задачи"""
        if complexity_score >= 80:
            return 'high'
        elif complexity_score >= 60:
            return 'medium'
        else:
            return 'low'

    def _identify_dependencies(self, task_data: Dict) -> List[str]:
        """Идентификация зависимостей задачи"""
        dependencies = []
        
        if isinstance(task_data, dict):
            if 'requires_approval' in task_data:
                dependencies.append('approval_required')
            if 'external_data_needed' in task_data:
                dependencies.append('external_data')
            if 'client_input_required' in task_data:
                dependencies.append('client_input')
        
        return dependencies

    def _get_agent_load_percentage(self, agent_id: str) -> float:
        """Получение текущей загрузки агента"""
        agent_info = self.agent_registry.get(agent_id, {})
        current_load = agent_info.get('current_load', 0)
        capacity = agent_info.get('capacity', 10)
        return (current_load / capacity) * 100

    def _find_alternative_agent(self, primary_agent: str, priority_analysis: Dict) -> Optional[str]:
        """Поиск альтернативного агента"""
        primary_info = self.agent_registry.get(primary_agent, {})
        primary_specialization = primary_info.get('specialization', [])
        
        # Ищем агента с пересекающейся специализацией и низкой загрузкой
        for agent_id, agent_info in self.agent_registry.items():
            if agent_id == primary_agent:
                continue
                
            # Проверяем пересечение специализаций
            if any(spec in agent_info['specialization'] for spec in primary_specialization):
                load_percentage = self._get_agent_load_percentage(agent_id)
                if load_percentage < 80:  # Менее 80% загрузки
                    return agent_id
        
        return None

    def _calculate_routing_confidence(self, capacity_analysis: Dict, timing_analysis: Dict) -> float:
        """Расчет уверенности в решении маршрутизации"""
        base_confidence = 0.8
        
        # Корректировка на основе загрузки
        load_percentage = capacity_analysis.get('load_percentage', 50)
        if load_percentage < 50:
            confidence_boost = 0.15
        elif load_percentage < 75:
            confidence_boost = 0.05
        else:
            confidence_boost = -0.1
        
        # Корректировка на основе SLA
        sla_probability = timing_analysis.get('sla_compliance_probability', 0.8)
        sla_boost = (sla_probability - 0.8) * 0.5
        
        final_confidence = base_confidence + confidence_boost + sla_boost
        return min(max(final_confidence, 0.0), 1.0)

    def _identify_risk_factors(self, capacity_analysis: Dict, timing_analysis: Dict) -> List[str]:
        """Идентификация факторов риска"""
        risks = []
        
        if capacity_analysis.get('load_percentage', 0) > 85:
            risks.append('high_agent_load')
        
        if timing_analysis.get('sla_compliance_probability', 1.0) < 0.7:
            risks.append('sla_risk')
        
        if timing_analysis.get('queue_delay_factor', 0) > 100:
            risks.append('queue_delays')
        
        return risks

    def _estimate_completion_time(self, target_agent: str, priority_analysis: Dict) -> Dict[str, Any]:
        """Оценка времени завершения"""
        agent_info = self.agent_registry.get(target_agent, {})
        base_time = agent_info.get('avg_processing_time', 600)
        
        # Корректировка на приоритет
        priority_multiplier = {
            'critical': 0.8,  # Критические задачи выполняются быстрее
            'high': 0.9,
            'medium': 1.0,
            'low': 1.2
        }.get(priority_analysis['priority_category'], 1.0)
        
        adjusted_time = base_time * priority_multiplier
        completion_time = datetime.now() + timedelta(seconds=adjusted_time)
        
        return {
            'estimated_seconds': round(adjusted_time),
            'estimated_completion': completion_time.isoformat(),
            'priority_adjustment_factor': priority_multiplier
        }

    def _calculate_coordination_confidence(self, routing_decision: Dict) -> float:
        """Расчет общей уверенности в координации"""
        base_confidence = routing_decision.get('confidence', 0.8)
        success_probability = routing_decision.get('success_probability', 0.9)
        
        # Учитываем историческую производительность
        coordination_rate = self.stats.get('coordination_success_rate', 0.95)
        
        overall_confidence = (base_confidence * 0.4 + success_probability * 0.4 + coordination_rate * 0.2)
        return min(overall_confidence, 1.0)

    def _assess_coordination_quality(self, result: Dict) -> str:
        """Оценка качества координации"""
        confidence = result.get('coordination_confidence', 0.8)
        
        if confidence >= 0.9:
            return 'excellent'
        elif confidence >= 0.8:
            return 'good'
        elif confidence >= 0.7:
            return 'acceptable'
        else:
            return 'needs_improvement'

    # Дополнительные методы для других типов задач
    async def _monitor_sla(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Мониторинг SLA"""
        return {
            'sla_status': 'monitoring_active',
            'violations_detected': 0,
            'agents_at_risk': [],
            'system_health': 'good'
        }

    async def _balance_load(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Балансировка нагрузки"""
        return {
            'balancing_action': 'load_redistribution',
            'agents_rebalanced': 2,
            'efficiency_improvement': 0.15
        }

    async def _get_system_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Получение статуса системы"""
        total_agents = len(self.agent_registry)
        healthy_agents = sum(1 for agent in self.agent_registry.values() 
                           if self._get_agent_load_percentage(agent.get('agent_id', '')) < 90)
        
        avg_load = sum(self._get_agent_load_percentage(agent_id) 
                      for agent_id in self.agent_registry.keys()) / total_agents
        
        return {
            'overall_status': 'healthy' if healthy_agents / total_agents > 0.8 else 'degraded',
            'total_agents': total_agents,
            'healthy_agents': healthy_agents,
            'system_load_percentage': round(avg_load, 1),
            'coordination_stats': {
                'total_coordinated': self.stats['total_tasks'],
                'success_rate': self.stats['success_count'] / max(self.stats['total_tasks'], 1),
                'coordination_success_rate': self.stats['coordination_success_rate']
            },
            'performance_metrics': {
                'avg_routing_time': self.stats['total_processing_time'] / max(self.stats['total_tasks'], 1),
                'sla_violations': self.stats['sla_violations'],
                'routing_decisions': self.stats['routing_decisions']
            }
        }

    async def _escalate_issue(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Эскалация проблемы"""
        return {
            'escalation_initiated': True,
            'escalation_level': 'management',
            'estimated_resolution_time': '30_minutes',
            'stakeholders_notified': ['operations_manager', 'technical_lead']
        }
