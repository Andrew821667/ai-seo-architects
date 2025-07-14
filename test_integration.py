"""
Тест интеграции Lead Qualification Agent с Data Provider архитектурой
"""

import asyncio
import sys
import os
from pathlib import Path

# Добавляем корневую папку в Python path
sys.path.insert(0, '/content/ai-seo-architects')

# Импорты
from core.data_providers.factory import ProviderFactory
from core.orchestrator import orchestrator
from core.state_models import SEOArchitectsState
from agents.operational.lead_qualification import LeadQualificationAgent
from datetime import datetime


async def test_lead_qualification_integration():
    """Тест интеграции Lead Qualification Agent с Data Providers"""
    
    print("🧪 ТЕСТ: Lead Qualification Agent + Data Providers")
    print("=" * 60)
    
    try:
        # 1. Создаем static data provider
        print("📊 Создаем Static Data Provider...")
        static_provider = ProviderFactory.create_provider("static", {
            "seo_ai_models_path": "./seo_ai_models/",
            "mock_mode": True,
            "cache_enabled": True
        })
        print(f"✅ Provider создан: {type(static_provider).__name__}")
        
        # 2. Создаем Lead Qualification Agent с provider
        print("\n🤖 Создаем Lead Qualification Agent...")
        agent = LeadQualificationAgent(data_provider=static_provider)
        print(f"✅ Агент создан: {agent.name}")
        
        # 3. Проверяем health check агента
        print("\n🩺 Health check агента...")
        health_result = await agent.health_check()
        print(f"Status: {health_result.get('status')}")
        print(f"Provider status: {health_result.get('provider_status')}")
        
        # 4. Тестируем получение данных через provider
        print("\n📊 Тестируем получение client data...")
        client_data = await agent.get_client_data("test_client_001")
        print(f"✅ Client data получена из {client_data.source}")
        print(f"Company: {client_data.company_info.get('name', 'Unknown')}")
        print(f"Lead score: {client_data.lead_score}")
        
        # 5. Тестируем выполнение задачи
        print("\n🎯 Тестируем выполнение задачи квалификации...")
        task_data = {
            "task_type": "lead_qualification",
            "task_id": "test_task_001",
            "input_data": {
                "company_name": "TechCorp Solutions",
                "email": "contact@techcorp.com",
                "phone": "+1-555-0123",
                "website": "techcorp.com",
                "source": "website_form",
                "budget_range": "10000-25000",
                "timeline": "Q2 2024",
                "industry": "SaaS",
                "company_size": "50-100",
                "current_seo": "basic",
                "pain_points": ["low organic traffic", "poor rankings"]
            },
            "client_context": {
                "utm_source": "google",
                "utm_campaign": "seo_services"
            }
        }
        
        result = await agent.execute_task(task_data)
        
        print(f"✅ Задача выполнена: {result.status}")
        print(f"Время выполнения: {result.execution_time:.2f}s")
        print(f"Confidence: {result.confidence_score}")
        
        if result.status == "success":
            lead_score = result.result_data.get("lead_score", 0)
            qualification = result.result_data.get("qualification", "unknown")
            print(f"Lead Score: {lead_score}/100")
            print(f"Qualification: {qualification}")
        
        # 6. Проверяем метрики агента
        print("\n📈 Метрики агента:")
        metrics = agent.get_agent_metrics()
        exec_metrics = metrics["execution_metrics"]
        print(f"Completed tasks: {exec_metrics['tasks_completed']}")
        print(f"Failed tasks: {exec_metrics['tasks_failed']}")
        print(f"Avg execution time: {exec_metrics['avg_execution_time']:.2f}s")
        
        # 7. Проверяем provider метрики
        print("\n📊 Метрики Data Provider:")
        provider_metrics = static_provider.get_metrics()
        print(f"Total calls: {provider_metrics['calls_total']}")
        print(f"Success rate: {provider_metrics['success_rate']:.2%}")
        print(f"Cache hit rate: {provider_metrics['cache_hit_rate']:.2%}")
        
        print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        return True
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ТЕСТА: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_orchestrator_integration():
    """Тест интеграции с Orchestrator"""
    
    print("\n🔄 ТЕСТ: Orchestrator Integration")
    print("=" * 60)
    
    try:
        # 1. Создаем и регистрируем агента в orchestrator
        print("🤖 Регистрируем Lead Qualification Agent в Orchestrator...")
        
        static_provider = ProviderFactory.create_provider("static")
        agent = LeadQualificationAgent(data_provider=static_provider)
        
        orchestrator.register_agent("lead_qualification_agent", agent)
        print("✅ Агент зарегистрирован в orchestrator")
        
        # 2. Создаем workflow
        print("\n🏗️ Создаем workflow...")
        workflow = orchestrator.create_workflow_graph()
        compiled_workflow = orchestrator.compile_workflow()
        print("✅ Workflow скомпилирован")
        
        # 3. Тестируем выполнение через orchestrator
        print("\n🚀 Тестируем выполнение через orchestrator...")
        
        initial_state = SEOArchitectsState(
            client_id="test_client_002",
            client_data={
                "company": "Example Corp",
                "email": "test@example.com"
            },
            task_id="orchestrator_test_001",
            task_type="lead_processing",
            task_description="Квалификация нового лида через orchestrator",
            current_agent="lead_qualification_agent",
            previous_agents=[],
            next_agents=[],
            input_data={
                "company_name": "Example Corp",
                "email": "test@example.com",
                "website": "example.com",
                "budget_range": "15000-30000"
            },
            processing_results=[],
            final_output=None,
            timestamp=datetime.now().isoformat(),
            priority=5,
            deadline=None,
            conversation_history=[],
            client_context={},
            status="pending",
            errors=[],
            warnings=[]
        )
        
        # Запускаем workflow
        final_state = await orchestrator.execute_workflow(initial_state)
        
        print(f"✅ Workflow выполнен: {final_state['status']}")
        print(f"Processing results: {len(final_state['processing_results'])}")
        
        if final_state['processing_results']:
            last_result = final_state['processing_results'][-1]
            print(f"Last agent: {last_result.get('agent')}")
            print(f"Status: {last_result.get('status')}")
        
        print("\n✅ ORCHESTRATOR ТЕСТ ПРОЙДЕН!")
        return True
        
    except Exception as e:
        print(f"\n❌ ОШИБКА ORCHESTRATOR ТЕСТА: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Главная функция тестирования"""
    print("🧪 ПОЛНОЕ ТЕСТИРОВАНИЕ AI SEO ARCHITECTS")
    print("🎯 Milestone 2: Data Provider Foundation")
    print("=" * 80)
    
    # Запускаем все тесты
    test1_result = await test_lead_qualification_integration()
    test2_result = await test_orchestrator_integration()
    
    print("\n" + "=" * 80)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ:")
    print(f"✅ Agent + Data Provider: {'PASS' if test1_result else 'FAIL'}")
    print(f"✅ Orchestrator Integration: {'PASS' if test2_result else 'FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 MILESTONE 2 УСПЕШНО ЗАВЕРШЕН!")
        print("🚀 Готовность к Milestone 3: Core Agents Creation")
    else:
        print("\n⚠️ Есть проблемы, требующие исправления")


# Запускаем тестирование
if __name__ == "__main__":
    asyncio.run(main())
