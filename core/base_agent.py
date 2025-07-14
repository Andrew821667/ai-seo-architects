"""
Базовый класс для всех AI-агентов с Data Provider поддержкой
Обеспечивает единый интерфейс для работы с данными
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
import time
from datetime import datetime

from core.data_providers.base import BaseDataProvider
from core.data_providers.factory import ProviderFactory
from core.interfaces.data_models import SEOData, ClientData, CompetitiveData, TaskData, AgentResult

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Базовый класс для всех AI-агентов с Data Provider поддержкой"""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        data_provider: Optional[BaseDataProvider] = None,
        knowledge_base: Optional[str] = None,
        model_config: Optional[Dict[str, Any]] = None
    ):
        """
        Инициализация агента
        
        Args:
            agent_id: Уникальный идентификатор агента
            name: Имя агента
            data_provider: Провайдер данных (если None, создается static по умолчанию)
            knowledge_base: Путь к базе знаний агента
            model_config: Конфигурация LLM модели
        """
        self.agent_id = agent_id
        self.name = name
        self.knowledge_base = knowledge_base
        self.model_config = model_config or {}
        self.context = {}
        self.execution_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_execution_time": 0.0,
            "avg_execution_time": 0.0
        }
        
        # Инициализация data provider
        if data_provider is None:
            logger.info(f"🔧 Создаем default static provider для {self.agent_id}")
            self.data_provider = ProviderFactory.create_provider("static")
        else:
            self.data_provider = data_provider
        
        logger.info(f"🤖 Инициализирован агент {self.name} ({self.agent_id})")
        logger.info(f"📊 Использует {type(self.data_provider).__name__}")
    
    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика обработки задачи агентом
        
        Args:
            task_data: Данные задачи
            
        Returns:
            Dict с результатами выполнения
        """
        pass
    
    # =================================================================
    # DATA PROVIDER INTEGRATION METHODS
    # =================================================================
    
    async def get_seo_data(self, domain: str, **kwargs) -> SEOData:
        """
        Получение SEO данных через провайдер
        
        Args:
            domain: Анализируемый домен
            **kwargs: Дополнительные параметры
            
        Returns:
            SEOData: Структурированные SEO данные
        """
        try:
            logger.debug(f"📊 {self.agent_id} запрашивает SEO данные для {domain}")
            seo_data = await self.data_provider.get_seo_data(domain, **kwargs)
            logger.debug(f"✅ SEO данные получены из {seo_data.source}")
            return seo_data
        except Exception as e:
            logger.error(f"❌ Ошибка получения SEO данных для {domain}: {str(e)}")
            raise
    
    async def get_client_data(self, client_id: str, **kwargs) -> ClientData:
        """
        Получение данных клиента через провайдер
        
        Args:
            client_id: ID клиента
            **kwargs: Дополнительные параметры
            
        Returns:
            ClientData: Данные клиента
        """
        try:
            logger.debug(f"👤 {self.agent_id} запрашивает данные клиента {client_id}")
            client_data = await self.data_provider.get_client_data(client_id, **kwargs)
            logger.debug(f"✅ Данные клиента получены из {client_data.source}")
            return client_data
        except Exception as e:
            logger.error(f"❌ Ошибка получения данных клиента {client_id}: {str(e)}")
            raise
    
    async def get_competitive_data(
        self, 
        domain: str, 
        competitors: List[str], 
        **kwargs
    ) -> CompetitiveData:
        """
        Получение конкурентных данных через провайдер
        
        Args:
            domain: Основной домен
            competitors: Список конкурентов
            **kwargs: Дополнительные параметры
            
        Returns:
            CompetitiveData: Данные конкурентного анализа
        """
        try:
            logger.debug(f"🎯 {self.agent_id} запрашивает конкурентный анализ для {domain}")
            competitive_data = await self.data_provider.get_competitive_data(
                domain, competitors, **kwargs
            )
            logger.debug(f"✅ Конкурентные данные получены из {competitive_data.source}")
            return competitive_data
        except Exception as e:
            logger.error(f"❌ Ошибка получения конкурентных данных: {str(e)}")
            raise
    
    # =================================================================
    # EXECUTION METHODS WITH METRICS
    # =================================================================
    
    async def execute_task(self, task_data: Dict[str, Any]) -> AgentResult:
        """
        Выполнение задачи с метриками и error handling
        
        Args:
            task_data: Данные задачи
            
        Returns:
            AgentResult: Стандартизированный результат
        """
        start_time = time.time()
        task_id = task_data.get("task_id", f"task_{int(time.time())}")
        
        try:
            logger.info(f"🚀 {self.agent_id} начинает выполнение задачи {task_id}")
            
            # Вызываем основную логику агента
            result_data = await self.process_task(task_data)
            
            # Вычисляем время выполнения
            execution_time = time.time() - start_time
            
            # Обновляем метрики
            self._update_execution_metrics(True, execution_time)
            
            # Создаем стандартизированный результат
            agent_result = AgentResult(
                agent_id=self.agent_id,
                task_id=task_id,
                status="success",
                result_data=result_data,
                execution_time=execution_time,
                confidence_score=result_data.get("confidence_score", 0.8),
                recommendations=result_data.get("recommendations", []),
                next_actions=result_data.get("next_actions", []),
                errors=[],
                warnings=result_data.get("warnings", []),
                timestamp=datetime.now()
            )
            
            logger.info(f"✅ {self.agent_id} завершил задачу {task_id} за {execution_time:.2f}s")
            return agent_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._update_execution_metrics(False, execution_time)
            
            error_msg = str(e)
            logger.error(f"❌ {self.agent_id} ошибка в задаче {task_id}: {error_msg}")
            
            # Возвращаем результат с ошибкой
            agent_result = AgentResult(
                agent_id=self.agent_id,
                task_id=task_id,
                status="error",
                result_data={},
                execution_time=execution_time,
                confidence_score=0.0,
                recommendations=[],
                next_actions=["Проверить входные данные", "Повторить задачу"],
                errors=[error_msg],
                warnings=[],
                timestamp=datetime.now()
            )
            
            return agent_result
    
    def _update_execution_metrics(self, success: bool, execution_time: float) -> None:
        """Обновление метрик выполнения агента"""
        if success:
            self.execution_metrics["tasks_completed"] += 1
        else:
            self.execution_metrics["tasks_failed"] += 1
        
        self.execution_metrics["total_execution_time"] += execution_time
        
        total_tasks = (
            self.execution_metrics["tasks_completed"] + 
            self.execution_metrics["tasks_failed"]
        )
        
        if total_tasks > 0:
            self.execution_metrics["avg_execution_time"] = (
                self.execution_metrics["total_execution_time"] / total_tasks
            )
    
    # =================================================================
    # UTILITY METHODS
    # =================================================================
    
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Информация об используемом провайдере данных
        
        Returns:
            Dict с информацией о провайдере
        """
        try:
            return {
                "provider_type": type(self.data_provider).__name__,
                "provider_metrics": self.data_provider.get_metrics(),
                "cache_size": len(getattr(self.data_provider, 'cache', {})),
                "health_status": "unknown"  # Можно добавить async health check
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_agent_metrics(self) -> Dict[str, Any]:
        """
        Получение метрик агента
        
        Returns:
            Dict с метриками агента
        """
        return {
            "agent_id": self.agent_id,
            "agent_name": self.name,
            "execution_metrics": self.execution_metrics.copy(),
            "provider_info": self.get_provider_info(),
            "model_config": self.model_config,
            "knowledge_base": self.knowledge_base,
            "context_size": len(self.context)
        }
    
    def reset_metrics(self) -> None:
        """Сброс метрик агента"""
        self.execution_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_execution_time": 0.0,
            "avg_execution_time": 0.0
        }
        logger.info(f"📊 Метрики агента {self.agent_id} сброшены")
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        """
        Обновление контекста агента
        
        Args:
            new_context: Новые данные контекста
        """
        self.context.update(new_context)
        logger.debug(f"📝 Контекст агента {self.agent_id} обновлен")
    
    def clear_context(self) -> None:
        """Очистка контекста агента"""
        self.context.clear()
        logger.debug(f"🗑️ Контекст агента {self.agent_id} очищен")
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Проверка здоровья агента
        
        Returns:
            Dict со статусом агента
        """
        try:
            # Проверяем data provider
            provider_health = await self.data_provider.health_check()
            
            # Базовые проверки агента
            agent_status = {
                "agent_id": self.agent_id,
                "status": "healthy",
                "provider_status": provider_health.get("status", "unknown"),
                "metrics": self.get_agent_metrics(),
                "last_check": datetime.now().isoformat()
            }
            
            # Проверяем критические показатели
            success_rate = 0
            if self.execution_metrics["tasks_completed"] + self.execution_metrics["tasks_failed"] > 0:
                success_rate = (
                    self.execution_metrics["tasks_completed"] / 
                    (self.execution_metrics["tasks_completed"] + self.execution_metrics["tasks_failed"])
                )
            
            if success_rate < 0.5 and self.execution_metrics["tasks_completed"] > 5:
                agent_status["status"] = "degraded"
                agent_status["warning"] = "Низкий процент успешных задач"
            
            return agent_status
            
        except Exception as e:
            return {
                "agent_id": self.agent_id,
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
    
    def __str__(self) -> str:
        """Строковое представление агента"""
        return f"{self.name} ({self.agent_id})"
    
    def __repr__(self) -> str:
        """Детальное представление агента"""
        return (
            f"BaseAgent(agent_id='{self.agent_id}', name='{self.name}', "
            f"provider={type(self.data_provider).__name__})"
        )


# =================================================================
# CONVENIENCE FUNCTIONS
# =================================================================

def create_agent_with_static_provider(
    agent_class,
    agent_id: str,
    name: str,
    **kwargs
) -> BaseAgent:
    """
    Создание агента со static data provider
    
    Args:
        agent_class: Класс агента
        agent_id: ID агента
        name: Имя агента
        **kwargs: Дополнительные параметры
        
    Returns:
        Экземпляр агента
    """
    static_provider = ProviderFactory.create_provider("static")
    return agent_class(
        agent_id=agent_id,
        name=name,
        data_provider=static_provider,
        **kwargs
    )


def create_agent_with_provider(
    agent_class,
    agent_id: str,
    name: str,
    provider_type: str,
    provider_config: Optional[Dict[str, Any]] = None,
    **kwargs
) -> BaseAgent:
    """
    Создание агента с указанным провайдером
    
    Args:
        agent_class: Класс агента
        agent_id: ID агента
        name: Имя агента
        provider_type: Тип провайдера
        provider_config: Конфигурация провайдера
        **kwargs: Дополнительные параметры
        
    Returns:
        Экземпляр агента
    """
    provider = ProviderFactory.create_provider(provider_type, provider_config)
    return agent_class(
        agent_id=agent_id,
        name=name,
        data_provider=provider,
        **kwargs
    )
