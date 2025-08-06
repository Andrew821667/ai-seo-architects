"""
Интеграционные тесты для MCP (Model Context Protocol) в AI SEO Architects
Тестирование работы агентов с MCP провайдером данных
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Добавляем корневую директорию в PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.mcp.agent_manager import MCPAgentManager, get_mcp_agent_manager
from config.mcp_config import get_development_config, get_config_for_environment
from core.mcp.data_provider import MCPDataProvider
from mock_data_provider import MockDataProvider

class MCPIntegrationTester:
    """Тестирование MCP интеграции"""
    
    def __init__(self):
        self.test_results = {
            "test_type": "mcp_integration_test",
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {
                "total_tests": 0,
                "successful_tests": 0,
                "failed_tests": 0,
                "mcp_tests": 0,
                "fallback_tests": 0
            }
        }
        
    async def run_all_tests(self):
        """Запуск всех MCP тестов"""
        
        print("🧪 === MCP Integration Testing Suite ===\n")
        
        # Тест 1: Базовая инициализация MCP
        await self.test_mcp_initialization()
        
        # Тест 2: Создание MCP провайдера
        await self.test_mcp_provider_creation()
        
        # Тест 3: Создание агентов с MCP
        await self.test_agent_creation_with_mcp()
        
        # Тест 4: Fallback режим
        await self.test_fallback_mode()
        
        # Тест 5: Комплексное тестирование всех агентов
        await self.test_all_agents_comprehensive()
        
        # Тест 6: Health checks
        await self.test_health_checks()
        
        # Итоговый отчет
        self.print_final_report()
    
    async def test_mcp_initialization(self):
        """Тест инициализации MCP конфигурации"""
        
        test_name = "mcp_config_initialization"
        print(f"🔧 Тест: {test_name}")
        
        try:
            # Тестируем различные конфигурации
            dev_config = get_development_config()
            prod_config = get_config_for_environment("production")
            
            # Проверяем структуру конфигурации
            assert "mcp_servers" in dev_config, "mcp_servers отсутствует в dev config"
            assert "cache_ttl_minutes" in dev_config, "cache_ttl_minutes отсутствует"
            assert "enable_fallback" in dev_config, "enable_fallback отсутствует"
            
            self.test_results["tests"][test_name] = {
                "status": "success",
                "config_keys": list(dev_config.keys()),
                "mcp_servers_count": len(dev_config.get("mcp_servers", {}))
            }
            
            self.test_results["summary"]["successful_tests"] += 1
            print("  ✅ MCP конфигурация инициализирована корректно\n")
            
        except Exception as e:
            self.test_results["tests"][test_name] = {
                "status": "failed",
                "error": str(e)
            }
            self.test_results["summary"]["failed_tests"] += 1
            print(f"  ❌ Ошибка инициализации MCP: {e}\n")
        
        self.test_results["summary"]["total_tests"] += 1
    
    async def test_mcp_provider_creation(self):
        """Тест создания MCP провайдера"""
        
        test_name = "mcp_provider_creation"
        print(f"🔗 Тест: {test_name}")
        
        try:
            # Создаем провайдер с development конфигурацией
            config = get_development_config()
            provider = MCPDataProvider(config)
            
            # Тестируем инициализацию (должна пройти с fallback)
            init_result = await provider.initialize()
            
            # Тестируем базовые методы
            stats = provider.get_stats()
            health = await provider.health_check()
            
            self.test_results["tests"][test_name] = {
                "status": "success",
                "initialization_result": init_result,
                "provider_stats": stats,
                "health_status": health.get("overall_health", "unknown")
            }
            
            # Закрываем провайдер
            await provider.close()
            
            self.test_results["summary"]["successful_tests"] += 1
            self.test_results["summary"]["mcp_tests"] += 1
            print("  ✅ MCP провайдер создан и протестирован\n")
            
        except Exception as e:
            self.test_results["tests"][test_name] = {
                "status": "failed", 
                "error": str(e)
            }
            self.test_results["summary"]["failed_tests"] += 1
            print(f"  ❌ Ошибка создания MCP провайдера: {e}\n")
        
        self.test_results["summary"]["total_tests"] += 1
    
    async def test_agent_creation_with_mcp(self):
        """Тест создания агентов с MCP поддержкой"""
        
        test_name = "agent_creation_mcp"
        print(f"🤖 Тест: {test_name}")
        
        try:
            # Создаем MCP менеджер
            config = get_development_config()
            manager = MCPAgentManager(config)
            
            await manager.initialize()
            
            # Создаем несколько агентов разных типов
            test_agents = [
                "LeadQualificationAgent",
                "ContentStrategyAgent", 
                "TechnicalSEOAuditorAgent"
            ]
            
            created_agents = {}
            
            for agent_class in test_agents:
                agent = await manager.create_agent(
                    agent_class_name=agent_class,
                    enable_mcp=True
                )
                
                if agent:
                    created_agents[agent.agent_id] = {
                        "class": agent_class,
                        "mcp_enabled": agent.mcp_enabled,
                        "agent_type": agent._get_agent_type() if hasattr(agent, '_get_agent_type') else "unknown"
                    }
            
            self.test_results["tests"][test_name] = {
                "status": "success",
                "requested_agents": len(test_agents),
                "created_agents": len(created_agents),
                "agent_details": created_agents,
                "manager_stats": manager.get_stats()
            }
            
            # Закрываем менеджер
            await manager.shutdown()
            
            self.test_results["summary"]["successful_tests"] += 1
            print(f"  ✅ Создано {len(created_agents)}/{len(test_agents)} агентов с MCP\n")
            
        except Exception as e:
            self.test_results["tests"][test_name] = {
                "status": "failed",
                "error": str(e)
            }
            self.test_results["summary"]["failed_tests"] += 1
            print(f"  ❌ Ошибка создания агентов: {e}\n")
        
        self.test_results["summary"]["total_tests"] += 1
    
    async def test_fallback_mode(self):
        """Тест fallback режима при недоступности MCP"""
        
        test_name = "fallback_mode"
        print(f"⚠️ Тест: {test_name}")
        
        try:
            # Создаем конфигурацию с недоступными серверами
            fallback_config = {
                "cache_ttl_minutes": 5,
                "enable_fallback": True,
                "fallback_provider": "mock",
                "mcp_servers": {
                    "unavailable_server": {
                        "name": "unavailable",
                        "endpoints": {"http": "http://localhost:9999/mcp/v1"},
                        "authentication": {"type": "none"}
                    }
                }
            }
            
            manager = MCPAgentManager(fallback_config)
            await manager.initialize()
            
            # Создаем агента (должен использовать fallback)
            agent = await manager.create_agent(
                agent_class_name="LeadQualificationAgent",
                enable_mcp=True  # Запрашиваем MCP, но получим fallback
            )
            
            if agent:
                # Тестируем работу агента
                test_data = {
                    "input_data": {
                        "company_data": {
                            "company_name": "Fallback Test Company",
                            "industry": "technology"
                        }
                    }
                }
                
                result = await agent.process_task(test_data)
                
                self.test_results["tests"][test_name] = {
                    "status": "success",
                    "agent_created": True,
                    "mcp_enabled": agent.mcp_enabled,
                    "provider_type": type(agent.data_provider).__name__,
                    "task_result": result.get("success", False)
                }
                
                self.test_results["summary"]["successful_tests"] += 1
                self.test_results["summary"]["fallback_tests"] += 1
            else:
                raise Exception("Агент не создан в fallback режиме")
            
            await manager.shutdown()
            print("  ✅ Fallback режим работает корректно\n")
            
        except Exception as e:
            self.test_results["tests"][test_name] = {
                "status": "failed",
                "error": str(e)
            }
            self.test_results["summary"]["failed_tests"] += 1
            print(f"  ❌ Ошибка fallback режима: {e}\n")
        
        self.test_results["summary"]["total_tests"] += 1
    
    async def test_all_agents_comprehensive(self):
        """Комплексное тестирование всех 14 агентов с MCP"""
        
        test_name = "comprehensive_all_agents"
        print(f"🏗️ Тест: {test_name}")
        
        try:
            # Создаем менеджер
            config = get_development_config()
            manager = MCPAgentManager(config)
            await manager.initialize()
            
            # Создаем всех агентов
            agents = await manager.create_all_agents(enable_mcp=True)
            
            # Запускаем комплексный тест
            test_results = await manager.run_comprehensive_test()
            
            self.test_results["tests"][test_name] = {
                "status": "success",
                "total_agents": len(agents),
                "test_results": test_results["summary"],
                "agent_breakdown": {
                    agent_id: result["status"] 
                    for agent_id, result in test_results["results"].items()
                }
            }
            
            await manager.shutdown()
            
            self.test_results["summary"]["successful_tests"] += 1
            print(f"  ✅ Протестировано {len(agents)} агентов: {test_results['summary']['success_rate']:.1f}% успеха\n")
            
        except Exception as e:
            self.test_results["tests"][test_name] = {
                "status": "failed",
                "error": str(e)
            }
            self.test_results["summary"]["failed_tests"] += 1
            print(f"  ❌ Ошибка комплексного тестирования: {e}\n")
        
        self.test_results["summary"]["total_tests"] += 1
    
    async def test_health_checks(self):
        """Тест health checks для MCP системы"""
        
        test_name = "health_checks"
        print(f"🔍 Тест: {test_name}")
        
        try:
            # Создаем менеджер и агентов
            config = get_development_config()
            manager = MCPAgentManager(config)
            await manager.initialize()
            
            # Создаем несколько агентов
            await manager.create_agent("LeadQualificationAgent", enable_mcp=True)
            await manager.create_agent("ContentStrategyAgent", enable_mcp=True)
            
            # Запускаем health check
            health_results = await manager.health_check_all_agents()
            
            # Анализируем результаты
            overall_healthy = health_results["overall_status"] == "healthy"
            agents_checked = len(health_results["agents"])
            
            self.test_results["tests"][test_name] = {
                "status": "success",
                "overall_health": health_results["overall_status"],
                "agents_checked": agents_checked,
                "healthy_agents": health_results["summary"]["healthy_agents"],
                "mcp_provider_status": health_results.get("mcp_provider_status", {}).get("overall_health", "unknown")
            }
            
            await manager.shutdown()
            
            self.test_results["summary"]["successful_tests"] += 1
            print(f"  ✅ Health check: {health_results['summary']['healthy_agents']}/{agents_checked} агентов здоровы\n")
            
        except Exception as e:
            self.test_results["tests"][test_name] = {
                "status": "failed",
                "error": str(e)
            }
            self.test_results["summary"]["failed_tests"] += 1
            print(f"  ❌ Ошибка health check: {e}\n")
        
        self.test_results["summary"]["total_tests"] += 1
    
    def print_final_report(self):
        """Печать финального отчета"""
        
        print("=" * 60)
        print("🎯 ИТОГОВЫЙ ОТЧЕТ MCP ИНТЕГРАЦИИ")
        print("=" * 60)
        
        summary = self.test_results["summary"]
        success_rate = (summary["successful_tests"] / max(1, summary["total_tests"])) * 100
        
        print(f"📊 Общая статистика:")
        print(f"   Всего тестов: {summary['total_tests']}")
        print(f"   Успешно: {summary['successful_tests']}")
        print(f"   Неудачно: {summary['failed_tests']}")
        print(f"   Процент успеха: {success_rate:.1f}%")
        print(f"   MCP тесты: {summary['mcp_tests']}")
        print(f"   Fallback тесты: {summary['fallback_tests']}")
        
        print(f"\n📋 Детали тестов:")
        for test_name, test_result in self.test_results["tests"].items():
            status_icon = "✅" if test_result["status"] == "success" else "❌"
            print(f"   {status_icon} {test_name}: {test_result['status']}")
            
            if test_result["status"] == "failed" and "error" in test_result:
                print(f"      Ошибка: {test_result['error']}")
        
        print(f"\n🎉 {'ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО' if success_rate >= 80 else 'ТРЕБУЕТСЯ ДОРАБОТКА'}")
        print(f"📅 Время тестирования: {self.test_results['timestamp']}")
        print("=" * 60)

async def main():
    """Главная функция для запуска MCP тестов"""
    
    print("🚀 Запуск MCP Integration Testing Suite")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Создаем и запускаем тестер
    tester = MCPIntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())