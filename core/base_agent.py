"""
Базовый класс для всех AI-агентов
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class AgentMetrics:
    """Метрики производительности агента"""
    
    def __init__(self):
        self.tasks_processed = 0
        self.tasks_successful = 0
        self.tasks_failed = 0
        self.total_processing_time = 0.0
        self.last_activity = None
    
    def record_task(self, success: bool, processing_time: float):
        """Записываем метрики выполнения задачи"""
        self.tasks_processed += 1
        if success:
            self.tasks_successful += 1
        else:
            self.tasks_failed += 1
        self.total_processing_time += processing_time
        self.last_activity = datetime.now()
    
    def get_success_rate(self) -> float:
        """Процент успешных задач"""
        if self.tasks_processed == 0:
            return 0.0
        return self.tasks_successful / self.tasks_processed
    
    def get_avg_processing_time(self) -> float:
        """Среднее время обработки задачи"""
        if self.tasks_processed == 0:
            return 0.0
        return self.total_processing_time / self.tasks_processed
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "tasks_processed": self.tasks_processed,
            "tasks_successful": self.tasks_successful,
            "tasks_failed": self.tasks_failed,
            "success_rate": self.get_success_rate(),
            "avg_processing_time": self.get_avg_processing_time(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }


class BaseAgent(ABC):
    """Базовый класс для всех AI-агентов"""
    
    def __init__(self, 
                 agent_id: str,
                 name: str,
                 data_provider,  # BaseDataProvider - избегаем circular import
                 knowledge_base: Optional[str] = None,
                 model_name: Optional[str] = None,
                 **kwargs):  # Принимаем дополнительные параметры
        self.agent_id = agent_id
        self.name = name
        self.data_provider = data_provider
        self.model_name = model_name or "gpt-4o-mini"
        self.knowledge_base = knowledge_base
        self.context = {}
        self.metrics = AgentMetrics()
        
        # Дополнительные параметры сохраняем в context
        self.context.update(kwargs)
    
    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика обработки задачи агентом
        
        Args:
            task_data: Данные задачи для обработки
            
        Returns:
            Dict с результатами обработки, должен содержать:
            - success: bool - статус выполнения
            - agent: str - ID агента
            - timestamp: str - время выполнения
            - другие поля специфичные для агента
        """
        pass
    
    async def get_seo_data(self, domain: str):
        """Получение SEO данных через провайдер"""
        return await self.data_provider.get_seo_data(domain)
    
    async def get_client_data(self, client_id: str):
        """Получение данных клиента через провайдер"""
        return await self.data_provider.get_client_data(client_id)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Информация о здоровье агента"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "healthy",
            "model": self.model_name,
            "metrics": self.metrics.to_dict()
        }
    
    async def _execute_with_metrics(self, task_func, *args, **kwargs):
        """Выполнение задачи с записью метрик"""
        start_time = datetime.now()
        success = False
        
        try:
            result = await task_func(*args, **kwargs)
            success = result.get('success', True)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat()
            }
        finally:
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            self.metrics.record_task(success, processing_time)
