"""
Task Coordination Agent для управления и маршрутизации задач между агентами
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random
from core.base_agent import BaseAgent

class TaskCoordinationAgent(BaseAgent):
    """Агент координации задач - управляет маршрутизацией и приоритизацией задач между агентами"""
    
    def __init__(self, data_provider=None, **kwargs):
        super().__init__(
            agent_id="task_coordination",
            name="Task Coordination Agent",
            description="Координация и маршрутизация задач между агентами системы",
            data_provider=data_provider,
            **kwargs
        )
        
        self.agent_registry = {
            'lead_qualification': {
                'agent_id': 'lead_qualification',
                'level': 'operational',
                'specialization': ['lead_analysis', 'bant_scoring', 'qualification'],
                'capacity': 10,
                'current_load': 0,
                'avg_processing_time': 300,
                'sla_hours': 2,
                'success_rate': 0.92
            },
            'proposal_generation': {
                'agent_id': 'proposal_generation',
                'level': 'operational',
                'specialization': ['proposals', 'pricing', 'service_packages'],
                'capacity': 8,
                'current_load': 0,
                'avg_processing_time': 600,
                'sla_hours': 4,
                'success_rate': 0.89
            },
            'business_development_director': {
                'agent_id': 'business_development_director',
                'level': 'executive',
                'specialization': ['enterprise_deals', 'strategic_partnerships'],
                'capacity': 5,
                'current_load': 0,
                'avg_processing_time': 1800,
                'sla_hours': 24,
                'success_rate': 0.96
            }
        }
        
        self.routing_matrix = {
            'lead_qualification': 'lead_qualification',
            'enterprise_assessment': 'business_development_director',
            'proposal_generation': 'proposal_generation',
            'strategic_partnership': 'business_development_director'
        }
        
        self.priority_weights = {
            'business_criticality': 0.35,
            'time_constraints': 0.25,
            'client_value': 0.20,
            'russian_market_priority': 0.15,
            'task_complexity': 0.10
        }
        
        self.stats = {
            'total_tasks_processed': 0,
            'successful_coordinations': 0,
            'coordination_success_rate': 0.95
        }
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Основной метод обработки координационных задач"""
        try:
            task_type = task_data.get('task_type', 'unknown')
            
            # Определяем целевого агента
            target_agent = self._route_task(task_data)
            
            # Рассчитываем приоритет
            priority_score = self._calculate_priority(task_data)
            
            # Анализируем загрузку агентов
            capacity_analysis = self._analyze_agent_capacity()
            
            result = {
                'success': True,
                'agent': self.agent_id,
                'task_type': task_type,
                'routed_to': target_agent,
                'priority_score': priority_score,
                'estimated_completion': self._estimate_completion_time(target_agent),
                'capacity_status': capacity_analysis,
                'coordination_quality': 'good',
                'confidence': 0.946
            }
            
            self.stats['total_tasks_processed'] += 1
            self.stats['successful_coordinations'] += 1
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Ошибка координации: {str(e)}',
                'agent': self.agent_id
            }
    
    def _route_task(self, task_data: Dict[str, Any]) -> str:
        """Определяет целевого агента для задачи"""
        task_type = task_data.get('task_type', 'lead_qualification')
        return self.routing_matrix.get(task_type, 'lead_qualification')
    
    def _calculate_priority(self, task_data: Dict[str, Any]) -> int:
        """Рассчитывает приоритет задачи (0-1000)"""
        base_score = 500
        
        # Российские клиенты получают приоритет
        if 'russian' in str(task_data).lower() or 'ru' in str(task_data).lower():
            base_score += 100
            
        # Enterprise клиенты получают приоритет
        if 'enterprise' in str(task_data).lower():
            base_score += 200
            
        return min(base_score, 1000)
    
    def _analyze_agent_capacity(self) -> Dict[str, Any]:
        """Анализирует текущую загрузку агентов"""
        total_capacity = sum(agent['capacity'] for agent in self.agent_registry.values())
        total_load = sum(agent['current_load'] for agent in self.agent_registry.values())
        
        return {
            'system_utilization': total_load / total_capacity if total_capacity > 0 else 0,
            'available_agents': len([a for a in self.agent_registry.values() if a['current_load'] < a['capacity']]),
            'overloaded_agents': len([a for a in self.agent_registry.values() if a['current_load'] >= a['capacity']])
        }
    
    def _estimate_completion_time(self, agent_id: str) -> str:
        """Оценивает время завершения задачи"""
        if agent_id in self.agent_registry:
            avg_time = self.agent_registry[agent_id]['avg_processing_time']
            completion_time = datetime.now() + timedelta(seconds=avg_time)
            return completion_time.isoformat()
        return datetime.now().isoformat()
