#!/usr/bin/env python3
"""
🚀 Быстрая проверка статуса всех 14 агентов после LLM интеграции
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def quick_agent_test():
    """Быстрая проверка инициализации всех агентов"""
    print("🧪 БЫСТРАЯ ПРОВЕРКА СТАТУСА ВСЕХ 14 АГЕНТОВ")
    print("=" * 60)
    
    agents_to_test = [
        # Executive Level
        ("agents.executive.chief_seo_strategist", "ChiefSEOStrategistAgent"),
        ("agents.executive.business_development_director", "BusinessDevelopmentDirectorAgent"),
        
        # Management Level  
        ("agents.management.task_coordination", "TaskCoordinationAgent"),
        ("agents.management.sales_operations_manager", "SalesOperationsManagerAgent"),
        ("agents.management.technical_seo_operations_manager", "TechnicalSEOOperationsManagerAgent"),
        ("agents.management.client_success_manager", "ClientSuccessManagerAgent"),
        
        # Operational Level
        ("agents.operational.lead_qualification", "LeadQualificationAgent"),
        ("agents.operational.proposal_generation", "ProposalGenerationAgent"),
        ("agents.operational.sales_conversation", "SalesConversationAgent"),
        ("agents.operational.technical_seo_auditor", "TechnicalSEOAuditorAgent"),
        ("agents.operational.content_strategy", "ContentStrategyAgent"),
        ("agents.operational.link_building", "LinkBuildingAgent"),
        ("agents.operational.competitive_analysis", "CompetitiveAnalysisAgent"),
        ("agents.operational.reporting", "ReportingAgent")
    ]
    
    successful = 0
    failed = 0
    
    for module_path, class_name in agents_to_test:
        try:
            # Импортируем модуль
            module = __import__(module_path, fromlist=[class_name])
            agent_class = getattr(module, class_name)
            
            # Создаем экземпляр агента
            agent = agent_class()
            
            # Проверяем базовые атрибуты
            has_agent_id = hasattr(agent, 'agent_id') and agent.agent_id
            has_openai_client = hasattr(agent, 'openai_client')
            has_process_method = hasattr(agent, 'process_task')
            has_system_prompt = hasattr(agent, 'get_system_prompt')
            
            if has_agent_id and has_process_method:
                print(f"✅ {class_name} - OK (ID: {agent.agent_id})")
                if has_openai_client:
                    print(f"   🤖 OpenAI готов")
                if has_system_prompt:
                    print(f"   💬 System prompt готов")
                successful += 1
            else:
                print(f"⚠️ {class_name} - Частично работает")
                failed += 1
                
        except Exception as e:
            print(f"❌ {class_name} - Ошибка: {str(e)[:50]}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 ИТОГИ БЫСТРОЙ ПРОВЕРКИ:")
    print(f"   ✅ Успешно: {successful}/14 ({(successful/14)*100:.1f}%)")
    print(f"   ❌ Ошибки: {failed}/14")
    
    if successful == 14:
        print(f"🎉 ВСЕ 14 АГЕНТОВ ГОТОВЫ К РАБОТЕ!")
        return 0
    else:
        print(f"⚠️ Требуется дополнительная настройка")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(quick_agent_test())
    sys.exit(exit_code)