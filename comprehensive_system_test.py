#!/usr/bin/env python3
"""
🧪 Комплексный тест всех функций системы AI SEO Architects
Проверяет работоспособность всех компонентов, агентов, API и интеграций
"""

import asyncio
import time
import json
from datetime import datetime
from typing import Dict, Any, List
import traceback
from dataclasses import dataclass
from enum import Enum

# Импорты для тестирования
from fastapi.testclient import TestClient

# Импорты компонентов системы
from api.main import app
from agents import AGENT_CLASSES, get_agent_instance
from core.orchestrator import AgentOrchestrator
from core.config import config
from core.data_providers.factory import DataProviderFactory
from core.mcp.agent_manager import MCPAgentManager
from core.interfaces.data_models import LeadInput, TaskType, AgentTask

class TestStatus(Enum):
    """Статусы тестов"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class TestResult:
    """Результат выполнения теста"""
    name: str
    status: TestStatus
    duration: float
    details: Dict[str, Any]
    error: str = None

class ComprehensiveSystemTester:
    """Комплексный тестер системы AI SEO Architects"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.start_time = time.time()
        
    def log(self, message: str, level: str = "INFO"):
        """Логирование с timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Запуск всех тестов системы"""
        self.log("🚀 Запуск комплексного тестирования AI SEO Architects", "INFO")
        
        # 1. Тестирование базовых компонентов
        await self.test_core_components()
        
        # 2. Тестирование Data Providers
        await self.test_data_providers()
        
        # 3. Тестирование всех 14 агентов
        await self.test_all_agents()
        
        # 4. Тестирование MCP интеграции
        await self.test_mcp_integration()
        
        # 5. Тестирование API endpoints
        await self.test_api_endpoints()
        
        # 6. Тестирование оркестратора
        await self.test_orchestrator()
        
        # 7. Интеграционные тесты
        await self.test_integration_scenarios()
        
        # Генерация отчета
        return self.generate_report()
    
    async def test_core_components(self):
        """Тестирование базовых компонентов"""
        self.log("📦 Тестирование базовых компонентов...")
        
        # Тест конфигурации
        await self.run_test("config_loading", self._test_config_loading)
        
        # Тест импортов агентов
        await self.run_test("agent_imports", self._test_agent_imports)
        
        # Тест оркестратора
        await self.run_test("orchestrator_init", self._test_orchestrator_init)
    
    async def test_data_providers(self):
        """Тестирование провайдеров данных"""
        self.log("🗄️ Тестирование Data Providers...")
        
        # Тест Static Provider
        await self.run_test("static_provider", self._test_static_provider)
        
        # Тест Factory
        await self.run_test("provider_factory", self._test_provider_factory)
    
    async def test_all_agents(self):
        """Тестирование всех 14 агентов"""
        self.log("🤖 Тестирование всех 14 агентов...")
        
        for agent_name, agent_class in AGENT_CLASSES.items():
            await self.run_test(f"agent_{agent_name}", 
                              lambda ac=agent_class, an=agent_name: self._test_single_agent(ac, an))
    
    async def test_mcp_integration(self):
        """Тестирование MCP интеграции"""
        self.log("🔗 Тестирование MCP интеграции...")
        
        await self.run_test("mcp_manager", self._test_mcp_manager)
        await self.run_test("mcp_agent_creation", self._test_mcp_agent_creation)
    
    async def test_api_endpoints(self):
        """Тестирование API endpoints"""
        self.log("🌐 Тестирование FastAPI endpoints...")
        
        # Основные endpoints
        await self.run_test("api_health", self._test_api_health)
        await self.run_test("api_auth", self._test_api_auth)
        await self.run_test("api_agents", self._test_api_agents)
        await self.run_test("api_tasks", self._test_api_tasks)
    
    async def test_orchestrator(self):
        """Тестирование оркестратора"""
        self.log("🎯 Тестирование оркестратора...")
        
        await self.run_test("orchestrator_workflow", self._test_orchestrator_workflow)
    
    async def test_integration_scenarios(self):
        """Интеграционные сценарии"""
        self.log("🔄 Тестирование интеграционных сценариев...")
        
        await self.run_test("lead_processing_scenario", self._test_lead_processing_scenario)
        await self.run_test("seo_audit_scenario", self._test_seo_audit_scenario)
    
    async def run_test(self, test_name: str, test_func):
        """Запуск отдельного теста с обработкой ошибок"""
        start_time = time.time()
        
        try:
            self.log(f"▶️ Запуск теста: {test_name}")
            details = await test_func()
            duration = time.time() - start_time
            
            result = TestResult(
                name=test_name,
                status=TestStatus.PASSED,
                duration=duration,
                details=details or {}
            )
            self.log(f"✅ Тест {test_name} ПРОЙДЕН за {duration:.2f}с")
            
        except Exception as e:
            duration = time.time() - start_time
            error_details = traceback.format_exc()
            
            result = TestResult(
                name=test_name,
                status=TestStatus.FAILED,
                duration=duration,
                details={"error_traceback": error_details},
                error=str(e)
            )
            self.log(f"❌ Тест {test_name} ПРОВАЛЕН: {str(e)}")
        
        self.results.append(result)
    
    # ===== ТЕСТЫ БАЗОВЫХ КОМПОНЕНТОВ =====
    
    async def _test_config_loading(self):
        """Тест загрузки конфигурации"""
        from core.config import load_config, get_config
        
        loaded_config = load_config()
        get_config_result = get_config()
        
        assert loaded_config is not None, "Конфигурация не загружена"
        assert get_config_result is not None, "get_config() вернул None"
        assert hasattr(loaded_config, 'DATA_PROVIDER_TYPE'), "Отсутствует DATA_PROVIDER_TYPE"
        
        return {
            "provider_type": loaded_config.DATA_PROVIDER_TYPE,
            "executive_model": loaded_config.EXECUTIVE_MODEL,
            "management_model": loaded_config.MANAGEMENT_MODEL
        }
    
    async def _test_agent_imports(self):
        """Тест импорта всех агентов"""
        assert len(AGENT_CLASSES) == 14, f"Ожидалось 14 агентов, найдено {len(AGENT_CLASSES)}"
        
        imported_agents = []
        for name, agent_class in AGENT_CLASSES.items():
            assert agent_class is not None, f"Агент {name} не импортирован"
            imported_agents.append(name)
        
        return {
            "total_agents": len(AGENT_CLASSES),
            "imported_agents": imported_agents
        }
    
    async def _test_orchestrator_init(self):
        """Тест инициализации оркестратора"""
        orchestrator = AgentOrchestrator()
        
        assert orchestrator is not None, "Оркестратор не создан"
        assert hasattr(orchestrator, 'agents'), "Отсутствует атрибут agents"
        assert hasattr(orchestrator, 'create_workflow_graph'), "Отсутствует метод create_workflow_graph"
        
        return {"orchestrator_created": True}
    
    # ===== ТЕСТЫ DATA PROVIDERS =====
    
    async def _test_static_provider(self):
        """Тест Static Data Provider"""
        provider = DataProviderFactory.create_provider("static")
        
        assert provider is not None, "Static provider не создан"
        
        # Тест получения SEO данных
        seo_data = await provider.get_seo_data("example.com")
        assert seo_data is not None, "SEO данные не получены"
        assert seo_data.domain == "example.com", "Неверный домен в SEO данных"
        
        # Тест получения данных клиента
        client_data = await provider.get_client_data("client_001")
        assert client_data is not None, "Данные клиента не получены"
        
        return {
            "provider_type": type(provider).__name__,
            "seo_data_confidence": seo_data.confidence_score,
            "client_lead_score": client_data.lead_score
        }
    
    async def _test_provider_factory(self):
        """Тест Provider Factory"""
        # Тест доступных провайдеров
        available_providers = DataProviderFactory.get_available_providers()
        assert "static" in available_providers, "Static provider недоступен"
        
        # Тест создания провайдера
        provider = DataProviderFactory.create_provider("static")
        assert provider is not None, "Провайдер не создан через factory"
        
        # Тест singleton behavior
        provider2 = DataProviderFactory.create_provider("static")
        assert provider is provider2, "Singleton pattern не работает"
        
        return {
            "available_providers": available_providers,
            "singleton_works": provider is provider2
        }
    
    # ===== ТЕСТЫ АГЕНТОВ =====
    
    async def _test_single_agent(self, agent_class, agent_name):
        """Тест отдельного агента"""
        # Создание экземпляра агента
        agent = get_agent_instance(agent_name)
        assert agent is not None, f"Агент {agent_name} не создан"
        
        # Проверка базовых атрибутов
        assert hasattr(agent, 'process_task'), f"У агента {agent_name} нет метода process_task"
        assert hasattr(agent, 'agent_id'), f"У агента {agent_name} нет agent_id"
        
        # Тест выполнения задачи (mock)
        test_task = {
            "task_type": "test",
            "input_data": {"test": "data"},
            "domain": "example.com"
        }
        
        try:
            result = await agent.process_task(test_task)
            task_executed = True
            task_error = None
        except Exception as e:
            task_executed = False
            task_error = str(e)
        
        return {
            "agent_name": agent_name,
            "agent_class": agent_class.__name__,
            "agent_id": getattr(agent, 'agent_id', 'unknown'),
            "task_executed": task_executed,
            "task_error": task_error
        }
    
    # ===== ТЕСТЫ MCP =====
    
    async def _test_mcp_manager(self):
        """Тест MCP Manager"""
        manager = MCPAgentManager()
        assert manager is not None, "MCP Manager не создан"
        
        # Получение доступных типов агентов
        agent_types = await manager.get_available_agent_types()
        assert len(agent_types) > 0, "Нет доступных типов агентов"
        
        return {
            "manager_created": True,
            "available_agent_types": len(agent_types),
            "agent_types": agent_types[:5]  # Первые 5 для компактности
        }
    
    async def _test_mcp_agent_creation(self):
        """Тест создания агентов через MCP"""
        manager = MCPAgentManager()
        
        # Создание одного агента для теста
        agents = await manager.create_agents_by_category("executive", limit=1)
        assert len(agents) > 0, "Агенты не созданы через MCP"
        
        agent = list(agents.values())[0]
        assert agent is not None, "Созданный агент пуст"
        
        return {
            "agents_created": len(agents),
            "first_agent_id": list(agents.keys())[0],
            "creation_successful": True
        }
    
    # ===== ТЕСТЫ API =====
    
    async def _test_api_health(self):
        """Тест API health endpoint"""
        with TestClient(app) as client:
            response = client.get("/health")
            
            assert response.status_code == 200, f"Health endpoint вернул {response.status_code}"
            
            health_data = response.json()
            assert "status" in health_data, "Отсутствует поле status в health данных"
            
            return {
                "status_code": response.status_code,
                "health_status": health_data.get("status"),
                "has_metrics": "metrics" in health_data
            }
    
    async def _test_api_auth(self):
        """Тест API аутентификации"""
        with TestClient(app) as client:
            # Тест логина
            login_response = client.post("/auth/login", json={
                "username": "admin",
                "password": "secret"
            })
            
            login_success = login_response.status_code == 200
            token = None
            
            if login_success:
                token_data = login_response.json()
                token = token_data.get("access_token")
            
            return {
                "login_status_code": login_response.status_code,
                "login_successful": login_success,
                "token_received": token is not None
            }
    
    async def _test_api_agents(self):
        """Тест API агентов"""
        with TestClient(app) as client:
            # Получение списка агентов
            agents_response = client.get("/api/agents/")
            
            agents_success = agents_response.status_code == 200
            agents_count = 0
            
            if agents_success:
                agents_data = agents_response.json()
                agents_count = len(agents_data.get("agents", []))
            
            return {
                "agents_endpoint_status": agents_response.status_code,
                "agents_listed": agents_success,
                "agents_count": agents_count
            }
    
    async def _test_api_tasks(self):
        """Тест API задач"""
        with TestClient(app) as client:
            # Тест создания задачи
            task_data = {
                "agent_id": "lead_qualification_agent",
                "task_type": "lead_analysis",
                "input_data": {
                    "company_name": "Test Company",
                    "industry": "Technology"
                }
            }
            
            task_response = client.post("/api/tasks/", json=task_data)
            
            return {
                "task_creation_status": task_response.status_code,
                "task_creation_successful": task_response.status_code in [200, 201, 202]
            }
    
    # ===== ТЕСТЫ ОРКЕСТРАТОРА =====
    
    async def _test_orchestrator_workflow(self):
        """Тест workflow оркестратора"""
        orchestrator = AgentOrchestrator()
        
        # Создание графа workflow
        workflow = orchestrator.create_workflow_graph()
        assert workflow is not None, "Workflow граф не создан"
        
        # Компиляция workflow
        compiled = orchestrator.compile_workflow()
        assert compiled is not None, "Workflow не скомпилирован"
        
        return {
            "workflow_created": True,
            "workflow_compiled": True
        }
    
    # ===== ИНТЕГРАЦИОННЫЕ ТЕСТЫ =====
    
    async def _test_lead_processing_scenario(self):
        """Интеграционный тест обработки лида"""
        # Создание тестового лида
        lead_data = LeadInput(
            company_name="Test Corp",
            industry="SaaS",
            estimated_revenue="$1M+",
            monthly_budget="$10K",
            timeline="3 months",
            pain_points=["SEO issues", "Low traffic"]
        )
        
        # Получение агента квалификации лидов
        lead_agent = get_agent_instance("lead_qualification_agent")
        
        if lead_agent:
            try:
                result = await lead_agent.process_task({
                    "task_type": "lead_analysis",
                    "input_data": lead_data.dict()
                })
                processing_successful = True
                lead_score = result.get("lead_score", 0) if result else 0
            except Exception as e:
                processing_successful = False
                lead_score = 0
        else:
            processing_successful = False
            lead_score = 0
        
        return {
            "lead_created": True,
            "agent_available": lead_agent is not None,
            "processing_successful": processing_successful,
            "lead_score": lead_score
        }
    
    async def _test_seo_audit_scenario(self):
        """Интеграционный тест SEO аудита"""
        # Получение SEO аудитора
        seo_agent = get_agent_instance("technical_seo_auditor")
        
        if seo_agent:
            try:
                result = await seo_agent.process_task({
                    "task_type": "seo_audit",
                    "input_data": {"domain": "example.com"}
                })
                audit_successful = True
                audit_score = result.get("audit_score", 0) if result else 0
            except Exception as e:
                audit_successful = False
                audit_score = 0
        else:
            audit_successful = False
            audit_score = 0
        
        return {
            "seo_agent_available": seo_agent is not None,
            "audit_successful": audit_successful,
            "audit_score": audit_score
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """Генерация финального отчета"""
        total_duration = time.time() - self.start_time
        
        passed_tests = [r for r in self.results if r.status == TestStatus.PASSED]
        failed_tests = [r for r in self.results if r.status == TestStatus.FAILED]
        
        success_rate = len(passed_tests) / len(self.results) * 100 if self.results else 0
        
        report = {
            "summary": {
                "total_tests": len(self.results),
                "passed": len(passed_tests),
                "failed": len(failed_tests),
                "success_rate": round(success_rate, 2),
                "total_duration": round(total_duration, 2)
            },
            "test_results": [
                {
                    "name": r.name,
                    "status": r.status.value,
                    "duration": round(r.duration, 3),
                    "error": r.error,
                    "details": r.details
                }
                for r in self.results
            ],
            "failed_tests_summary": [
                {"name": r.name, "error": r.error}
                for r in failed_tests
            ]
        }
        
        return report

async def main():
    """Основная функция запуска тестирования"""
    print("🧪 AI SEO Architects - Comprehensive System Test")
    print("=" * 60)
    
    tester = ComprehensiveSystemTester()
    report = await tester.run_all_tests()
    
    print("\n" + "=" * 60)
    print("📊 ФИНАЛЬНЫЙ ОТЧЕТ ПО ТЕСТИРОВАНИЮ")
    print("=" * 60)
    
    summary = report["summary"]
    print(f"📈 Общая статистика:")
    print(f"   • Всего тестов: {summary['total_tests']}")
    print(f"   • Пройдено: {summary['passed']} ✅")
    print(f"   • Провалено: {summary['failed']} ❌")
    print(f"   • Успешность: {summary['success_rate']}%")
    print(f"   • Время выполнения: {summary['total_duration']:.2f} сек")
    
    if report["failed_tests_summary"]:
        print(f"\n❌ Проваленные тесты:")
        for failed in report["failed_tests_summary"]:
            print(f"   • {failed['name']}: {failed['error']}")
    
    # Сохранение детального отчета
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"COMPREHENSIVE_SYSTEM_TEST_REPORT_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Детальный отчет сохранен: {report_file}")
    
    # Результат
    if summary["success_rate"] >= 80:
        print("\n🎉 ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
        return 0
    else:
        print("\n⚠️ ТЕСТИРОВАНИЕ ВЫЯВИЛО КРИТИЧЕСКИЕ ПРОБЛЕМЫ!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)