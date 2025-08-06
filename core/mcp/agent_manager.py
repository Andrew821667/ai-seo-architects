"""
MCP Agent Manager для AI SEO Architects
Управление агентами с MCP интеграцией
"""

import asyncio
from typing import Dict, Any, List, Optional, Type
from datetime import datetime
import importlib
import os

from core.base_agent import BaseAgent
from core.mcp.data_provider import MCPDataProvider
from config.mcp_config import get_config_for_environment

class MCPAgentManager:
    """
    Менеджер для управления агентами с MCP поддержкой
    Обеспечивает инициализацию, мониторинг и управление жизненным циклом агентов
    """
    
    def __init__(self, mcp_config: Dict[str, Any] = None):
        self.mcp_config = mcp_config or get_config_for_environment()
        self.mcp_provider: Optional[MCPDataProvider] = None
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_types: Dict[str, Type[BaseAgent]] = {}
        self.stats = {
            "total_agents": 0,
            "mcp_enabled_agents": 0,
            "fallback_agents": 0,
            "last_health_check": None
        }
        
    async def initialize(self) -> bool:
        """Инициализация MCP менеджера и провайдера данных"""
        
        try:
            print("🔧 Инициализация MCP Agent Manager...")
            
            # Инициализируем MCP провайдер
            if self.mcp_config.get("mcp_servers"):
                self.mcp_provider = MCPDataProvider(self.mcp_config)
                
                if await self.mcp_provider.initialize():
                    print("✅ MCP провайдер инициализирован успешно")
                else:
                    print("⚠️ MCP провайдер не удалось инициализировать, используем fallback")
                    self.mcp_provider = None
            else:
                print("⚠️ MCP серверы не настроены, используем fallback режим")
                
            # Загружаем типы агентов
            await self._discover_agent_types()
            
            print(f"✅ MCP Agent Manager инициализирован. Найдено {len(self.agent_types)} типов агентов")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка инициализации MCP Agent Manager: {e}")
            return False
    
    async def create_agent(self, agent_class_name: str, agent_id: str = None, 
                          enable_mcp: bool = True, **kwargs) -> Optional[BaseAgent]:
        """
        Создание агента с MCP поддержкой
        
        Args:
            agent_class_name: Название класса агента (например, "LeadQualificationAgent")
            agent_id: ID агента (по умолчанию генерируется из класса)
            enable_mcp: Включить MCP для агента
            **kwargs: Дополнительные параметры для агента
            
        Returns:
            Созданный агент или None при ошибке
        """
        
        try:
            # Получаем класс агента
            agent_class = self.agent_types.get(agent_class_name)
            if not agent_class:
                print(f"❌ Неизвестный тип агента: {agent_class_name}")
                return None
            
            # Генерируем ID если не задан
            if not agent_id:
                agent_id = self._generate_agent_id(agent_class_name)
                
            # Определяем провайдер данных
            data_provider = None
            mcp_enabled = False
            
            if enable_mcp and self.mcp_provider:
                data_provider = self.mcp_provider
                mcp_enabled = True
                self.stats["mcp_enabled_agents"] += 1
                print(f"🔗 Агент {agent_id} будет использовать MCP провайдер")
            else:
                # Fallback на MockDataProvider
                from mock_data_provider import MockDataProvider
                data_provider = MockDataProvider()
                self.stats["fallback_agents"] += 1
                print(f"⚠️ Агент {agent_id} будет использовать fallback провайдер")
            
            # Создаем агента
            agent = agent_class(
                agent_id=agent_id,
                name=self._generate_agent_name(agent_class_name),
                data_provider=data_provider,
                mcp_enabled=mcp_enabled,
                **kwargs
            )
            
            # Регистрируем агента
            self.agents[agent_id] = agent
            self.stats["total_agents"] += 1
            
            print(f"✅ Агент {agent_id} ({agent_class_name}) создан успешно")
            return agent
            
        except Exception as e:
            print(f"❌ Ошибка создания агента {agent_class_name}: {e}")
            return None
    
    async def create_all_agents(self, enable_mcp: bool = True) -> Dict[str, BaseAgent]:
        """
        Создание всех доступных агентов
        
        Args:
            enable_mcp: Включить MCP для всех агентов
            
        Returns:
            Словарь созданных агентов {agent_id: agent_instance}
        """
        
        created_agents = {}
        
        print(f"🏗️ Создание всех агентов (MCP: {'включен' if enable_mcp else 'отключен'})...")
        
        # Создаем агентов по категориям
        agent_categories = {
            "executive": [
                "ChiefSEOStrategistAgent",
                "BusinessDevelopmentDirectorAgent"
            ],
            "management": [
                "TaskCoordinationAgent",
                "SalesOperationsManagerAgent", 
                "TechnicalSEOOperationsManagerAgent",
                "ClientSuccessManagerAgent"
            ],
            "operational": [
                "LeadQualificationAgent",
                "ProposalGenerationAgent",
                "SalesConversationAgent",
                "TechnicalSEOAuditorAgent",
                "ContentStrategyAgent",
                "LinkBuildingAgent",
                "CompetitiveAnalysisAgent",
                "ReportingAgent"
            ]
        }
        
        for category, agent_classes in agent_categories.items():
            print(f"\n📂 Создание агентов категории '{category}':")
            
            for agent_class_name in agent_classes:
                agent = await self.create_agent(
                    agent_class_name=agent_class_name,
                    enable_mcp=enable_mcp
                )
                
                if agent:
                    created_agents[agent.agent_id] = agent
                    print(f"  ✅ {agent.agent_id}")
                else:
                    print(f"  ❌ Не удалось создать {agent_class_name}")
        
        print(f"\n🎉 Создано {len(created_agents)} из {sum(len(agents) for agents in agent_categories.values())} агентов")
        return created_agents
    
    async def health_check_all_agents(self) -> Dict[str, Any]:
        """Проверка здоровья всех агентов"""
        
        health_results = {
            "overall_status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "mcp_provider_status": None,
            "summary": {
                "total_agents": len(self.agents),
                "healthy_agents": 0,
                "unhealthy_agents": 0,
                "mcp_enabled": 0,
                "fallback_mode": 0
            }
        }
        
        print("🔍 Проверка здоровья всех агентов...")
        
        # Проверяем MCP провайдер
        if self.mcp_provider:
            try:
                mcp_health = await self.mcp_provider.health_check()
                health_results["mcp_provider_status"] = mcp_health
            except Exception as e:
                health_results["mcp_provider_status"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        # Проверяем каждого агента
        for agent_id, agent in self.agents.items():
            try:
                agent_health = agent.get_health_status()
                
                # Дополнительная MCP проверка
                if hasattr(agent, 'get_mcp_health_status'):
                    mcp_health = await agent.get_mcp_health_status()
                    agent_health["mcp_status"] = mcp_health
                
                health_results["agents"][agent_id] = agent_health
                
                # Обновляем статистику
                if agent_health.get("status") == "healthy":
                    health_results["summary"]["healthy_agents"] += 1
                else:
                    health_results["summary"]["unhealthy_agents"] += 1
                    health_results["overall_status"] = "degraded"
                
                if agent_health.get("mcp_enabled", False):
                    health_results["summary"]["mcp_enabled"] += 1
                else:
                    health_results["summary"]["fallback_mode"] += 1
                    
            except Exception as e:
                health_results["agents"][agent_id] = {
                    "status": "error",
                    "error": str(e)
                }
                health_results["summary"]["unhealthy_agents"] += 1
                health_results["overall_status"] = "degraded"
        
        self.stats["last_health_check"] = datetime.now()
        
        print(f"📊 Health check завершен: {health_results['summary']['healthy_agents']}/{len(self.agents)} агентов здоровы")
        return health_results
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Запуск комплексного теста всех агентов с MCP"""
        
        print("🧪 Запуск комплексного теста агентов с MCP...")
        
        test_results = {
            "test_type": "comprehensive_mcp_test",
            "timestamp": datetime.now().isoformat(),
            "results": {},
            "summary": {
                "total_tests": 0,
                "successful_tests": 0,
                "failed_tests": 0,
                "mcp_tests": 0,
                "fallback_tests": 0
            }
        }
        
        # Тестовые данные
        test_data = {
            "company_data": {
                "company_name": "Test Company MCP",
                "annual_revenue": "50000000",
                "employee_count": "250",
                "industry": "technology",
                "current_seo_spend": "500000",
                "website_domain": "test-company-mcp.com"
            },
            "task_type": "comprehensive_analysis"
        }
        
        # Тестируем каждого агента
        for agent_id, agent in self.agents.items():
            try:
                print(f"🔄 Тестирование агента {agent_id}...")
                
                start_time = datetime.now()
                
                # Запускаем задачу
                result = await agent.process_task({"input_data": test_data})
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Анализируем результат
                test_success = result.get("success", False)
                mcp_used = agent.mcp_enabled and hasattr(agent.data_provider, 'get_stats')
                
                test_results["results"][agent_id] = {
                    "status": "success" if test_success else "failed",
                    "processing_time": processing_time,
                    "mcp_enabled": agent.mcp_enabled,
                    "mcp_used": mcp_used,
                    "result_summary": {
                        "has_data": bool(result.get("result")),
                        "error": result.get("error"),
                        "agent_type": agent._get_agent_type() if hasattr(agent, '_get_agent_type') else "unknown"
                    }
                }
                
                # Обновляем статистику
                test_results["summary"]["total_tests"] += 1
                if test_success:
                    test_results["summary"]["successful_tests"] += 1
                else:
                    test_results["summary"]["failed_tests"] += 1
                
                if mcp_used:
                    test_results["summary"]["mcp_tests"] += 1
                else:
                    test_results["summary"]["fallback_tests"] += 1
                    
                print(f"  {'✅' if test_success else '❌'} {agent_id} - {processing_time:.3f}s")
                
            except Exception as e:
                test_results["results"][agent_id] = {
                    "status": "error",
                    "error": str(e),
                    "mcp_enabled": agent.mcp_enabled
                }
                test_results["summary"]["total_tests"] += 1
                test_results["summary"]["failed_tests"] += 1
                print(f"  ❌ {agent_id} - ошибка: {e}")
        
        # Финальная статистика
        success_rate = (
            test_results["summary"]["successful_tests"] / 
            max(1, test_results["summary"]["total_tests"]) * 100
        )
        
        print(f"\n📈 Результаты тестирования:")
        print(f"   Всего тестов: {test_results['summary']['total_tests']}")
        print(f"   Успешно: {test_results['summary']['successful_tests']}")
        print(f"   Неудачно: {test_results['summary']['failed_tests']}")
        print(f"   Процент успеха: {success_rate:.1f}%")
        print(f"   MCP тесты: {test_results['summary']['mcp_tests']}")
        print(f"   Fallback тесты: {test_results['summary']['fallback_tests']}")
        
        test_results["summary"]["success_rate"] = success_rate
        
        return test_results
    
    async def shutdown(self):
        """Завершение работы менеджера и освобождение ресурсов"""
        
        print("🔄 Завершение работы MCP Agent Manager...")
        
        # Закрываем MCP провайдер
        if self.mcp_provider:
            try:
                await self.mcp_provider.close()
                print("✅ MCP провайдер закрыт")
            except Exception as e:
                print(f"❌ Ошибка закрытия MCP провайдера: {e}")
        
        # Очищаем агенты
        self.agents.clear()
        self.stats = {
            "total_agents": 0,
            "mcp_enabled_agents": 0,
            "fallback_agents": 0,
            "last_health_check": None
        }
        
        print("✅ MCP Agent Manager завершил работу")
    
    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики менеджера"""
        
        stats = self.stats.copy()
        stats["mcp_provider_available"] = self.mcp_provider is not None
        stats["registered_agent_types"] = len(self.agent_types)
        stats["active_agents"] = len(self.agents)
        
        if self.mcp_provider:
            try:
                stats["mcp_provider_stats"] = self.mcp_provider.get_stats()
            except:
                stats["mcp_provider_stats"] = "unavailable"
        
        return stats
    
    async def _discover_agent_types(self):
        """Автоматическое обнаружение типов агентов"""
        
        print("🔍 Поиск доступных типов агентов...")
        
        # Пути к агентам
        agent_paths = [
            "agents.executive",
            "agents.management", 
            "agents.operational"
        ]
        
        for path in agent_paths:
            try:
                # Получаем список файлов в директории
                module_dir = path.replace(".", "/")
                if os.path.exists(module_dir):
                    for filename in os.listdir(module_dir):
                        if filename.endswith(".py") and filename != "__init__.py":
                            module_name = filename[:-3]  # убираем .py
                            full_module_path = f"{path}.{module_name}"
                            
                            try:
                                module = importlib.import_module(full_module_path)
                                
                                # Ищем классы агентов
                                for attr_name in dir(module):
                                    attr = getattr(module, attr_name)
                                    
                                    if (isinstance(attr, type) and 
                                        issubclass(attr, BaseAgent) and 
                                        attr != BaseAgent and
                                        attr_name.endswith("Agent")):
                                        
                                        self.agent_types[attr_name] = attr
                                        print(f"  ✅ Найден агент: {attr_name}")
                                        
                            except Exception as e:
                                print(f"  ⚠️ Ошибка загрузки модуля {full_module_path}: {e}")
                                
            except Exception as e:
                print(f"  ⚠️ Ошибка обработки пути {path}: {e}")
        
        print(f"📦 Найдено {len(self.agent_types)} типов агентов")
    
    def _generate_agent_id(self, class_name: str) -> str:
        """Генерация ID агента из названия класса"""
        
        # Преобразуем CamelCase в snake_case
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
        snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        
        # Убираем суффикс _agent
        if snake_case.endswith("_agent"):
            snake_case = snake_case[:-6]
            
        return snake_case
    
    def _generate_agent_name(self, class_name: str) -> str:
        """Генерация понятного имени агента"""
        
        # Убираем суффикс Agent
        if class_name.endswith("Agent"):
            name = class_name[:-5]
        else:
            name = class_name
        
        # Разбиваем CamelCase на слова
        import re
        words = re.findall(r'[A-Z][a-z]+', name)
        
        return " ".join(words) + " Agent"

# Глобальный экземпляр менеджера
_global_manager: Optional[MCPAgentManager] = None

async def get_mcp_agent_manager(config: Dict[str, Any] = None) -> MCPAgentManager:
    """Получение глобального экземпляра MCP менеджера"""
    
    global _global_manager
    
    if _global_manager is None:
        _global_manager = MCPAgentManager(config)
        await _global_manager.initialize()
    
    return _global_manager

async def shutdown_global_manager():
    """Завершение работы глобального менеджера"""
    
    global _global_manager
    
    if _global_manager:
        await _global_manager.shutdown()
        _global_manager = None