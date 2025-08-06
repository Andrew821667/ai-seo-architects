"""
Базовый класс для всех AI-агентов с поддержкой MCP (Model Context Protocol)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime

# Избегаем circular imports
if TYPE_CHECKING:
    from core.mcp.data_provider import MCPDataProvider


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
    """Базовый класс для всех AI-агентов с поддержкой MCP"""
    
    def __init__(self, 
                 agent_id: str,
                 name: str,
                 data_provider=None,  # Может быть MockDataProvider или MCPDataProvider
                 knowledge_base: Optional[str] = None,
                 model_name: Optional[str] = None,
                 mcp_enabled: bool = False,
                 **kwargs):  # Принимаем дополнительные параметры
        self.agent_id = agent_id
        self.name = name
        self.data_provider = data_provider
        self.model_name = model_name or "gpt-4o-mini"
        self.knowledge_base = knowledge_base
        self.context = {}
        self.metrics = AgentMetrics()
        self.mcp_enabled = mcp_enabled
        self.mcp_context = {}
        
        # Дополнительные параметры сохраняем в context
        self.context.update(kwargs)
        
        # Инициализация MCP контекста если включен
        if self.mcp_enabled:
            self._initialize_mcp_context()
    
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
    
    async def get_seo_data(self, domain: str, parameters: Dict[str, Any] = None):
        """Получение SEO данных через провайдер (MCP-compatible)"""
        if self.mcp_enabled and hasattr(self.data_provider, 'get_seo_data'):
            return await self.data_provider.get_seo_data(domain, parameters or {})
        elif hasattr(self.data_provider, 'get_seo_data'):
            return await self.data_provider.get_seo_data(domain)
        else:
            # Fallback для совместимости
            return {"domain": domain, "source": "fallback", "status": "no_provider"}
    
    async def get_client_data(self, client_id: str, parameters: Dict[str, Any] = None):
        """Получение данных клиента через провайдер (MCP-compatible)"""
        if self.mcp_enabled and hasattr(self.data_provider, 'get_client_data'):
            return await self.data_provider.get_client_data(client_id, parameters or {})
        elif hasattr(self.data_provider, 'get_client_data'):
            return await self.data_provider.get_client_data(client_id)
        else:
            # Fallback для совместимости
            return {"client_id": client_id, "source": "fallback", "status": "no_provider"}
    
    async def get_competitive_data(self, domain: str, competitors: list, parameters: Dict[str, Any] = None):
        """Получение конкурентных данных через MCP провайдер"""
        if self.mcp_enabled and hasattr(self.data_provider, 'get_competitive_data'):
            return await self.data_provider.get_competitive_data(domain, competitors, parameters or {})
        else:
            # Fallback данные для совместимости
            return {
                "domain": domain,
                "competitors": competitors,
                "source": "fallback",
                "status": "mcp_not_available"
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Информация о здоровье агента"""
        health_status = {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "healthy",
            "model": self.model_name,
            "metrics": self.metrics.to_dict(),
            "mcp_enabled": self.mcp_enabled
        }
        
        # Добавляем MCP статус если включен
        if self.mcp_enabled:
            health_status["mcp_context"] = self.mcp_context
            health_status["data_provider_type"] = type(self.data_provider).__name__
        
        return health_status
    
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
    
    def _initialize_mcp_context(self):
        """Инициализация MCP контекста для агента"""
        self.mcp_context = {
            "agent_id": self.agent_id,
            "agent_type": self._get_agent_type(),
            "capabilities": self._get_agent_capabilities(),
            "preferences": {
                "cache_enabled": True,
                "real_time_updates": False,
                "data_freshness_threshold": "1h"
            },
            "session_id": f"session_{self.agent_id}_{datetime.now().timestamp()}",
            "initialized_at": datetime.now().isoformat()
        }
    
    def _get_agent_type(self) -> str:
        """Определение типа агента по имени класса"""
        class_name = self.__class__.__name__.lower()
        
        if "executive" in self.name.lower() or any(word in class_name for word in ["chief", "director", "executive"]):
            return "executive"
        elif "manager" in class_name or "coordination" in class_name:
            return "management"  
        else:
            return "operational"
    
    def _get_agent_capabilities(self) -> list:
        """Получение списка возможностей агента"""
        capabilities = ["basic_analysis"]
        
        # Определяем возможности на основе типа агента
        agent_type = self._get_agent_type()
        class_name = self.__class__.__name__.lower()
        
        if agent_type == "executive":
            capabilities.extend(["strategic_planning", "enterprise_analysis", "roi_optimization"])
        elif agent_type == "management":
            capabilities.extend(["task_coordination", "performance_monitoring", "team_management"])
        else:  # operational
            capabilities.extend(["data_processing", "automated_analysis", "report_generation"])
        
        # Специфические возможности по названию агента
        if "seo" in class_name:
            capabilities.extend(["seo_analysis", "technical_audit", "keyword_research"])
        if "content" in class_name:
            capabilities.extend(["content_analysis", "content_strategy", "eeat_optimization"])
        if "competitive" in class_name:
            capabilities.extend(["competitive_analysis", "serp_analysis", "market_intelligence"])
        if "sales" in class_name:
            capabilities.extend(["lead_qualification", "sales_analysis", "proposal_generation"])
        if "link" in class_name:
            capabilities.extend(["link_analysis", "backlink_research", "outreach_automation"])
        if "reporting" in class_name:
            capabilities.extend(["business_intelligence", "data_visualization", "anomaly_detection"])
        
        return list(set(capabilities))  # Убираем дубликаты
    
    async def get_mcp_health_status(self) -> Dict[str, Any]:
        """Получение статуса здоровья MCP провайдера"""
        if not self.mcp_enabled or not hasattr(self.data_provider, 'health_check'):
            return {"status": "mcp_disabled"}
        
        try:
            health_data = await self.data_provider.health_check()
            return {
                "status": "healthy",
                "mcp_health": health_data,
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
    
    def enable_mcp(self, data_provider: "MCPDataProvider"):
        """Включение MCP для агента"""
        self.mcp_enabled = True
        self.data_provider = data_provider
        self._initialize_mcp_context()
        print(f"✅ MCP включен для агента {self.agent_id}")
    
    def disable_mcp(self):
        """Отключение MCP для агента"""
        self.mcp_enabled = False
        self.mcp_context = {}
        print(f"⚠️ MCP отключен для агента {self.agent_id}")
    
    def get_mcp_stats(self) -> Dict[str, Any]:
        """Получение статистики MCP провайдера"""
        if not self.mcp_enabled or not hasattr(self.data_provider, 'get_stats'):
            return {"status": "mcp_disabled"}
        
        try:
            return {
                "status": "enabled",
                "provider_stats": self.data_provider.get_stats(),
                "agent_mcp_context": self.mcp_context
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
