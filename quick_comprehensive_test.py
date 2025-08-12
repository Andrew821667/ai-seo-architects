#!/usr/bin/env python3
"""
🚀 Быстрый комплексный тест всех функций системы AI SEO Architects
Оптимизированная версия для быстрой проверки критических компонентов
"""

import asyncio
import time
import json
from datetime import datetime
from typing import Dict, Any, List
import traceback

# Импорты для тестирования
from fastapi.testclient import TestClient

# Импорты компонентов системы
from api.main import app
from agents import AGENT_CLASSES
from core.orchestrator import AgentOrchestrator
from core.config import config
from core.data_providers.factory import DataProviderFactory
from core.mcp.agent_manager import MCPAgentManager

class QuickSystemTester:
    """Быстрый тестер системы AI SEO Architects"""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        
    def log(self, message: str, level: str = "INFO"):
        """Логирование с timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Запуск всех тестов системы"""
        self.log("🚀 Запуск быстрого комплексного тестирования AI SEO Architects")
        
        # 1. Базовые компоненты
        self.results['core'] = await self.test_core_components()
        
        # 2. Data Providers
        self.results['data_providers'] = await self.test_data_providers()
        
        # 3. Выборочное тестирование агентов (по одному с каждого уровня)
        self.results['agents'] = await self.test_sample_agents()
        
        # 4. MCP интеграция
        self.results['mcp'] = await self.test_mcp_basic()
        
        # 5. API endpoints
        self.results['api'] = await self.test_api_basic()
        
        # 6. Оркестратор
        self.results['orchestrator'] = await self.test_orchestrator_basic()
        
        return self.generate_report()
    
    async def test_core_components(self):
        """Тестирование базовых компонентов"""
        self.log("📦 Тестирование базовых компонентов...")
        results = {}
        
        try:
            # Тест конфигурации
            from core.config import load_config, get_config
            loaded_config = load_config()
            get_config_result = get_config()
            
            results['config'] = {
                'status': 'success',
                'provider_type': loaded_config.DATA_PROVIDER_TYPE,
                'models': f"{loaded_config.EXECUTIVE_MODEL}, {loaded_config.MANAGEMENT_MODEL}"
            }
            self.log("✅ Конфигурация загружена успешно")
            
        except Exception as e:
            results['config'] = {'status': 'failed', 'error': str(e)}
            self.log(f"❌ Ошибка конфигурации: {e}")
        
        try:
            # Тест импортов агентов
            assert len(AGENT_CLASSES) == 14, f"Ожидалось 14 агентов, найдено {len(AGENT_CLASSES)}"
            results['agent_imports'] = {
                'status': 'success',
                'total_agents': len(AGENT_CLASSES),
                'agents': list(AGENT_CLASSES.keys())[:5]  # Первые 5 для краткости
            }
            self.log(f"✅ Импорт агентов: {len(AGENT_CLASSES)} агентов")
            
        except Exception as e:
            results['agent_imports'] = {'status': 'failed', 'error': str(e)}
            self.log(f"❌ Ошибка импорта агентов: {e}")
        
        return results
    
    async def test_data_providers(self):
        """Тестирование провайдеров данных"""
        self.log("🗄️ Тестирование Data Providers...")
        results = {}
        
        try:
            # Тест Static Provider
            provider = DataProviderFactory.create_provider("static")
            assert provider is not None, "Static provider не создан"
            
            # Быстрый тест получения данных (без ожидания)
            seo_data = await provider.get_seo_data("example.com")
            assert seo_data is not None, "SEO данные не получены"
            
            results['static_provider'] = {
                'status': 'success',
                'provider_type': type(provider).__name__,
                'confidence_score': seo_data.confidence_score,
                'domain': seo_data.domain
            }
            self.log("✅ Static Provider работает")
            
        except Exception as e:
            results['static_provider'] = {'status': 'failed', 'error': str(e)}
            self.log(f"❌ Ошибка Static Provider: {e}")
        
        try:
            # Тест Factory
            available_providers = DataProviderFactory.get_available_providers()
            assert "static" in available_providers, "Static provider недоступен"
            
            results['factory'] = {
                'status': 'success',
                'available_providers': available_providers
            }
            self.log("✅ Provider Factory работает")
            
        except Exception as e:
            results['factory'] = {'status': 'failed', 'error': str(e)}
            self.log(f"❌ Ошибка Provider Factory: {e}")
        
        return results
    
    async def test_sample_agents(self):
        """Тестирование выборочных агентов (по одному с каждого уровня)"""
        self.log("🤖 Тестирование выборочных агентов...")
        results = {}
        
        # Тестируем по одному агенту с каждого уровня
        sample_agents = {
            'executive': 'chief_seo_strategist',
            'management': 'task_coordination', 
            'operational': 'lead_qualification'
        }
        
        for level, agent_id in sample_agents.items():
            try:
                from agents import get_agent_instance
                agent = get_agent_instance(agent_id)
                
                if agent is not None:
                    # Проверяем базовые атрибуты
                    has_process_task = hasattr(agent, 'process_task')
                    has_agent_id = hasattr(agent, 'agent_id')
                    
                    results[f'{level}_agent'] = {
                        'status': 'success',
                        'agent_id': agent_id,
                        'has_process_task': has_process_task,
                        'has_agent_id': has_agent_id,
                        'agent_class': type(agent).__name__
                    }
                    self.log(f"✅ {level.title()} агент ({agent_id}) создан")
                else:
                    results[f'{level}_agent'] = {
                        'status': 'failed',
                        'error': 'Агент не создан'
                    }
                    self.log(f"❌ {level.title()} агент ({agent_id}) не создан")
                    
            except Exception as e:
                results[f'{level}_agent'] = {
                    'status': 'failed',
                    'error': str(e)
                }
                self.log(f"❌ Ошибка {level} агента: {e}")
        
        return results
    
    async def test_mcp_basic(self):
        """Базовое тестирование MCP"""
        self.log("🔗 Тестирование MCP интеграции...")
        results = {}
        
        try:
            manager = MCPAgentManager()
            assert manager is not None, "MCP Manager не создан"
            
            # Получение доступных типов агентов
            agent_types = await manager.get_available_agent_types()
            
            results['mcp_manager'] = {
                'status': 'success',
                'available_types': len(agent_types),
                'sample_types': agent_types[:3] if agent_types else []
            }
            self.log(f"✅ MCP Manager: {len(agent_types)} типов агентов")
            
        except Exception as e:
            results['mcp_manager'] = {'status': 'failed', 'error': str(e)}
            self.log(f"❌ Ошибка MCP: {e}")
        
        return results
    
    async def test_api_basic(self):
        """Базовое тестирование API"""
        self.log("🌐 Тестирование FastAPI...")
        results = {}
        
        try:
            with TestClient(app) as client:
                # Health endpoint
                health_response = client.get("/health")
                health_success = health_response.status_code == 200
                
                results['health_endpoint'] = {
                    'status': 'success' if health_success else 'failed',
                    'status_code': health_response.status_code,
                    'response_data': health_response.json() if health_success else None
                }
                
                if health_success:
                    self.log("✅ API Health endpoint работает")
                else:
                    self.log(f"❌ API Health endpoint: {health_response.status_code}")
                
                # Auth endpoint
                try:
                    auth_response = client.post("/auth/login", json={
                        "username": "admin",
                        "password": "secret"
                    })
                    auth_success = auth_response.status_code == 200
                    
                    results['auth_endpoint'] = {
                        'status': 'success' if auth_success else 'failed',
                        'status_code': auth_response.status_code
                    }
                    
                    if auth_success:
                        self.log("✅ API Auth endpoint работает")
                    else:
                        self.log(f"❌ API Auth endpoint: {auth_response.status_code}")
                        
                except Exception as e:
                    results['auth_endpoint'] = {'status': 'failed', 'error': str(e)}
                    self.log(f"❌ Ошибка Auth endpoint: {e}")
                
        except Exception as e:
            results['api_basic'] = {'status': 'failed', 'error': str(e)}
            self.log(f"❌ Ошибка API: {e}")
        
        return results
    
    async def test_orchestrator_basic(self):
        """Базовое тестирование оркестратора"""
        self.log("🎯 Тестирование оркестратора...")
        results = {}
        
        try:
            orchestrator = AgentOrchestrator()
            assert orchestrator is not None, "Оркестратор не создан"
            
            # Создание workflow графа
            workflow = orchestrator.create_workflow_graph()
            assert workflow is not None, "Workflow граф не создан"
            
            # Компиляция workflow
            compiled = orchestrator.compile_workflow()
            assert compiled is not None, "Workflow не скомпилирован"
            
            results['orchestrator'] = {
                'status': 'success',
                'workflow_created': True,
                'workflow_compiled': True
            }
            self.log("✅ Оркестратор работает")
            
        except Exception as e:
            results['orchestrator'] = {'status': 'failed', 'error': str(e)}
            self.log(f"❌ Ошибка оркестратора: {e}")
        
        return results
    
    def generate_report(self) -> Dict[str, Any]:
        """Генерация финального отчета"""
        total_duration = time.time() - self.start_time
        
        # Подсчет успешных и проваленных тестов
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for category, tests in self.results.items():
            for test_name, test_result in tests.items():
                total_tests += 1
                if isinstance(test_result, dict) and test_result.get('status') == 'success':
                    passed_tests += 1
                else:
                    failed_tests += 1
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": round(success_rate, 2),
                "total_duration": round(total_duration, 2),
                "timestamp": datetime.now().isoformat()
            },
            "detailed_results": self.results,
            "system_status": "healthy" if success_rate >= 80 else "degraded" if success_rate >= 60 else "critical"
        }
        
        return report

async def main():
    """Основная функция запуска тестирования"""
    print("🧪 AI SEO Architects - Quick Comprehensive Test")
    print("=" * 60)
    
    tester = QuickSystemTester()
    report = await tester.run_all_tests()
    
    print("\n" + "=" * 60)
    print("📊 ОТЧЕТ ПО БЫСТРОМУ ТЕСТИРОВАНИЮ")
    print("=" * 60)
    
    summary = report["summary"]
    print(f"📈 Статистика:")
    print(f"   • Всего тестов: {summary['total_tests']}")
    print(f"   • Пройдено: {summary['passed']} ✅")
    print(f"   • Провалено: {summary['failed']} ❌")
    print(f"   • Успешность: {summary['success_rate']}%")
    print(f"   • Время выполнения: {summary['total_duration']:.2f} сек")
    print(f"   • Статус системы: {report['system_status']}")
    
    # Детальные результаты
    print(f"\n📋 Детальные результаты:")
    for category, tests in report["detailed_results"].items():
        print(f"\n🔹 {category.upper()}:")
        for test_name, result in tests.items():
            if isinstance(result, dict):
                status = result.get('status', 'unknown')
                icon = "✅" if status == 'success' else "❌"
                print(f"   {icon} {test_name}: {status}")
                if status == 'failed' and 'error' in result:
                    print(f"      Error: {result['error']}")
    
    # Сохранение отчета
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"QUICK_SYSTEM_TEST_REPORT_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Отчет сохранен: {report_file}")
    
    # Результат
    if summary["success_rate"] >= 80:
        print("\n🎉 СИСТЕМА РАБОТАЕТ КОРРЕКТНО!")
        return 0
    elif summary["success_rate"] >= 60:
        print("\n⚠️ СИСТЕМА РАБОТАЕТ С НЕКОТОРЫМИ ПРОБЛЕМАМИ")
        return 0
    else:
        print("\n🚨 СИСТЕМА ИМЕЕТ КРИТИЧЕСКИЕ ПРОБЛЕМЫ!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)