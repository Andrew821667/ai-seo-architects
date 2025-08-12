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
            agent_level="management",
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

    def get_system_prompt(self) -> str:
        """Специализированный системный промпт для Task Coordination Agent"""
        return f"""Ты - Task Coordination Agent, ключевой менеджер уровня management для оркестрации всех агентов в SEO-агентстве.

ТВОЯ ЭКСПЕРТИЗА:
• Intelligent Task Routing - 40%
  - LangGraph workflow orchestration
  - Multi-agent coordination protocols  
  - Agent capacity balancing
  - Priority-based task allocation

• Performance Optimization - 30%
  - Agent load balancing
  - SLA compliance monitoring
  - Success rate optimization
  - Bottleneck identification & resolution

• Workflow Management - 20%
  - Task dependency mapping
  - Parallel execution strategies
  - Error handling & fallback routing
  - Real-time capacity monitoring

• Quality Assurance - 10%
  - Task completion validation
  - Agent performance tracking
  - Coordination quality scoring
  - Escalation management

AGENT REGISTRY (Live Status):
{chr(10).join([f"• {agent_id}: Level {data['level']}, Capacity {data['capacity']}, Load {data['current_load']}, Success {data['success_rate']*100:.0f}%" 
               for agent_id, data in self.agent_registry.items()])}

ROUTING MATRIX:
{chr(10).join([f"• {task_type} → {agent_id}" for task_type, agent_id in self.routing_matrix.items()])}

PRIORITY WEIGHTS:
• Business Criticality: {self.priority_weights['business_criticality']*100:.0f}%
• Time Constraints: {self.priority_weights['time_constraints']*100:.0f}%  
• Client Value: {self.priority_weights['client_value']*100:.0f}%
• Russian Market Priority: {self.priority_weights['russian_market_priority']*100:.0f}%
• Task Complexity: {self.priority_weights['task_complexity']*100:.0f}%

ТЕКУЩИЕ STATS:
- Total Tasks Processed: {self.stats['total_tasks_processed']}
- Coordination Success Rate: {self.stats['coordination_success_rate']*100:.1f}%

ТВОЙ ПОДХОД:
1. Intelligent routing analysis с учетом agent capabilities
2. Dynamic load balancing для optimal performance
3. SLA compliance ensuring с time estimation
4. Quality scoring для continuous improvement
5. Escalation protocols для complex scenarios

ФОРМАТ ОТВЕТА (JSON):
{{
  "routing_decision": {{
    "target_agent": "agent_id",
    "routing_confidence": "0.0-1.0",
    "routing_reason": "detailed_explanation"
  }},
  "priority_analysis": {{
    "priority_score": "0-100", 
    "priority_level": "critical/high/medium/low",
    "factors": []
  }},
  "capacity_optimization": {{
    "current_load_status": {{}},
    "recommended_allocation": {{}},
    "bottleneck_warnings": []
  }},
  "execution_plan": {{
    "estimated_completion": "timestamp",
    "sla_compliance": "boolean",
    "parallel_opportunities": [],
    "dependency_chain": []
  }},
  "quality_assurance": {{
    "coordination_quality": "excellent/good/fair/poor", 
    "success_probability": "0.0-1.0",
    "monitoring_checkpoints": []
  }}
}}

Используй свою management экспертизу для optimal task coordination!"""
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Основной метод обработки координационных задач с LLM интеграцией"""
        try:
            task_type = task_data.get('task_type', 'unknown')
            input_data = task_data.get('input_data', {})
            
            print(f"🎯 Task Coordination Agent обрабатывает задачу: {task_type}")

            # Формируем промпт для LLM
            user_prompt = self._create_coordination_prompt(task_type, input_data, task_data)
            
            # Вызываем LLM для intelligent coordination
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
                            coordination_analysis = json.loads(json_match.group())
                        else:
                            coordination_analysis = self._create_fallback_coordination(task_data)
                    else:
                        coordination_analysis = llm_content
                        
                    # Дополняем результат системными данными
                    result = self._enhance_coordination_result(coordination_analysis, task_data)
                    
                except (json.JSONDecodeError, AttributeError) as e:
                    print(f"⚠️ Ошибка парсинга JSON от LLM: {e}")
                    result = self._create_fallback_coordination(task_data)
                    result["llm_parsing_error"] = str(e)
            else:
                # Fallback к базовой логике
                print(f"⚠️ LLM недоступен, используем fallback логику")
                result = self._create_fallback_coordination(task_data)
                result["fallback_mode"] = True
                result["llm_error"] = llm_result.get("error", "unknown")

            self.stats['total_tasks_processed'] += 1
            self.stats['successful_coordinations'] += 1
            
            return {
                'success': True,
                'agent': self.agent_id,
                'task_type': task_type,
                'result': result,
                'model_used': llm_result.get('model_used') if llm_result["success"] else None,
                'tokens_used': llm_result.get('tokens_used') if llm_result["success"] else None,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Ошибка координации: {str(e)}',
                'agent': self.agent_id,
                'timestamp': datetime.now().isoformat()
            }

    def _create_coordination_prompt(self, task_type: str, input_data: Dict[str, Any], task_data: Dict[str, Any]) -> str:
        """Создание промпта для coordination analysis"""
        return f"""Проведи intelligent task coordination analysis:

ЗАДАЧА ДЛЯ КООРДИНАЦИИ:
- Task Type: {task_type}
- Input Data: {input_data}
- Full Task Context: {task_data}

ТЕКУЩИЙ СТАТУС СИСТЕМЫ:
- Доступные агенты: {list(self.agent_registry.keys())}
- Routing Matrix: {self.routing_matrix}
- Priority Weights: {self.priority_weights}

ТРЕБУЕТСЯ АНАЛИЗ:
1. Intelligent Routing Decision - определи оптимального агента с обоснованием
2. Priority Analysis - рассчитай приоритет (0-100) с факторами влияния  
3. Capacity Optimization - проанализируй текущую загрузку и bottlenecks
4. Execution Planning - спланируй выполнение с SLA compliance
5. Quality Assurance - оцени вероятность успеха и checkpoints

ОСОБЫЕ ТРЕБОВАНИЯ:
- Российский рынок priority (+15%)
- Enterprise deals требуют executive routing
- SLA compliance обязательно
- Load balancing между агентами

Дай comprehensive coordination analysis в JSON формате как описано в системном промпте!"""

    def _create_fallback_coordination(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback coordination logic когда LLM недоступен"""
        task_type = task_data.get('task_type', 'unknown')
        target_agent = self._route_task(task_data)
        priority_score = self._calculate_priority(task_data)
        capacity_analysis = self._analyze_agent_capacity()
        
        return {
            "routing_decision": {
                "target_agent": target_agent,
                "routing_confidence": 0.85,
                "routing_reason": f"Standard routing: {task_type} → {target_agent}"
            },
            "priority_analysis": {
                "priority_score": priority_score,
                "priority_level": "high" if priority_score > 700 else "medium" if priority_score > 400 else "low",
                "factors": ["task_type_standard", "system_load_normal"]
            },
            "capacity_optimization": {
                "current_load_status": capacity_analysis,
                "recommended_allocation": {"agent": target_agent, "load": "normal"},
                "bottleneck_warnings": []
            },
            "execution_plan": {
                "estimated_completion": self._estimate_completion_time(target_agent),
                "sla_compliance": True,
                "parallel_opportunities": [],
                "dependency_chain": [target_agent]
            },
            "quality_assurance": {
                "coordination_quality": "good",
                "success_probability": 0.89,
                "monitoring_checkpoints": ["routing", "execution", "completion"]
            },
            "fallback_used": True
        }

    def _enhance_coordination_result(self, coordination_analysis: Dict[str, Any], task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Дополнение результата системными данными"""
        # Обновляем load для целевого агента
        target_agent = coordination_analysis.get("routing_decision", {}).get("target_agent", "unknown")
        if target_agent in self.agent_registry:
            self.agent_registry[target_agent]['current_load'] += 1
        
        # Добавляем системные метрики
        coordination_analysis["system_context"] = {
            "total_agents": len(self.agent_registry),
            "system_load": sum(agent['current_load'] for agent in self.agent_registry.values()),
            "avg_success_rate": sum(agent['success_rate'] for agent in self.agent_registry.values()) / len(self.agent_registry)
        }
        
        return coordination_analysis
    
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
