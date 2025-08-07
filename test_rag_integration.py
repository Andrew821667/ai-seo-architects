#!/usr/bin/env python3
"""
Тестирование RAG интеграции для AI SEO Architects
"""

import asyncio
import sys
import os
from datetime import datetime

# Добавляем корневую директорию в path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from knowledge.knowledge_manager import knowledge_manager
from agents.operational.lead_qualification import LeadQualificationAgent
from core.config import config


async def test_knowledge_manager():
    """Тест менеджера знаний"""
    print("🧪 Тестирование KnowledgeManager...")
    
    # Инициализация всех баз знаний
    results = knowledge_manager.initialize_all_agents_knowledge()
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"📊 Результаты инициализации:")
    print(f"   ✅ Успешно: {success_count}/{total_count}")
    print(f"   ❌ Неудачно: {total_count - success_count}/{total_count}")
    
    if success_count == 0:
        print("❌ Не удалось инициализировать ни одну базу знаний!")
        return False
    
    # Тест поиска знаний
    print("\n🔍 Тестирование поиска знаний...")
    
    test_queries = [
        ("lead_qualification", "lead scoring BANT methodology"),
        ("technical_seo_auditor", "Core Web Vitals optimization"),
        ("content_strategy", "keyword research E-E-A-T"),
        ("sales_conversation", "objection handling SPIN selling")
    ]
    
    for agent_name, query in test_queries:
        if results.get(agent_name):
            context = knowledge_manager.get_knowledge_context(agent_name, query, k=2)
            if context:
                print(f"   ✅ {agent_name}: найден контекст ({len(context)} символов)")
                print(f"      Фрагмент: {context[:100]}...")
            else:
                print(f"   ⚠️ {agent_name}: контекст не найден")
        else:
            print(f"   ❌ {agent_name}: база знаний не инициализирована")
    
    return success_count > 0


async def test_agent_rag_integration():
    """Тест интеграции RAG с агентом"""
    print("\n🤖 Тестирование RAG интеграции с агентами...")
    
    # Создание агента с RAG
    agent = LeadQualificationAgent()
    
    print(f"📋 Агент создан:")
    print(f"   ID: {agent.agent_id}")
    print(f"   Уровень: {agent.agent_level}")  
    print(f"   RAG включен: {agent.rag_enabled}")
    
    if not agent.rag_enabled:
        print("❌ RAG не включен для агента!")
        return False
    
    # Тест получения контекста знаний
    test_query = "lead qualification BANT scoring methodology enterprise clients"
    context = await agent.get_knowledge_context(test_query)
    
    if context:
        print(f"✅ Получен контекст знаний ({len(context)} символов)")
        print(f"   Фрагмент: {context[:200]}...")
        
        # Тест форматирования промпта с RAG
        test_prompt = "Квалифицируй этого лида"
        test_data = {"company": "TechCorp", "industry": "fintech"}
        
        enhanced_prompt = agent.format_prompt_with_rag(test_prompt, test_data)
        
        print(f"\n📝 Промпт обогащен контекстом знаний:")
        print(f"   Длина промпта: {len(enhanced_prompt)} символов")
        print(f"   Содержит контекст: {'КОНТЕКСТ ЗНАНИЙ' in enhanced_prompt}")
        
        return True
    else:
        print("❌ Контекст знаний не получен!")
        return False


async def test_full_agent_task_with_rag():
    """Тест полной задачи агента с RAG"""
    print("\n⚡ Тестирование выполнения задачи с RAG...")
    
    agent = LeadQualificationAgent()
    
    # Тестовые данные лида
    task_data = {
        "input_data": {
            "company_name": "TechCorp Solutions",
            "industry": "fintech", 
            "company_size": "mid-market",
            "budget_range": "500000-1000000",
            "timeline": "Q1 2025",
            "email": "contact@techcorp.com",
            "contact_role": "CTO"
        },
        "task_type": "lead_analysis",
        "priority": "high"
    }
    
    try:
        start_time = datetime.now()
        result = await agent.process_task(task_data)
        end_time = datetime.now()
        
        processing_time = (end_time - start_time).total_seconds()
        
        print(f"✅ Задача выполнена успешно:")
        print(f"   Время выполнения: {processing_time:.2f}s")
        print(f"   Статус: {result.get('success', False)}")
        
        if 'lead_score' in result:
            print(f"   Lead Score: {result['lead_score']}/100")
        
        if 'qualification_level' in result:
            print(f"   Квалификация: {result['qualification_level']}")
        
        # Проверяем статистику RAG
        rag_stats = agent.get_rag_stats()
        print(f"📊 RAG статистика:")
        print(f"   RAG включен: {rag_stats['rag_enabled']}")
        print(f"   Контекст длина: {rag_stats['knowledge_context_length']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка выполнения задачи: {e}")
        return False


async def main():
    """Основная функция тестирования"""
    print("🧪 AI SEO Architects - RAG Integration Testing")
    print("=" * 60)
    print(f"🕒 Время запуска: {datetime.now().isoformat()}")
    print(f"📁 RAG включен в конфигурации: {config.ENABLE_RAG}")
    print(f"📊 RAG настройки:")
    print(f"   Chunk size: {config.RAG_CHUNK_SIZE}")
    print(f"   Chunk overlap: {config.RAG_CHUNK_OVERLAP}")
    print(f"   Top K: {config.RAG_TOP_K}")
    print(f"   Similarity threshold: {config.RAG_SIMILARITY_THRESHOLD}")
    print("=" * 60)
    
    # Проверяем переменные окружения
    if not config.OPENAI_API_KEY:
        print("⚠️ OPENAI_API_KEY не установлен, некоторые функции могут не работать")
    
    test_results = []
    
    # Тест 1: Менеджер знаний
    result1 = await test_knowledge_manager()
    test_results.append(("KnowledgeManager", result1))
    
    if not result1:
        print("\n❌ Базовые тесты не пройдены, останавливаем тестирование")
        return
    
    # Тест 2: Интеграция RAG с агентом
    result2 = await test_agent_rag_integration()
    test_results.append(("Agent RAG Integration", result2))
    
    # Тест 3: Полная задача с RAG
    result3 = await test_full_agent_task_with_rag()
    test_results.append(("Full Task with RAG", result3))
    
    # Итоговые результаты
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 60)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:<25} {status}")
    
    success_count = sum(1 for _, result in test_results if result)
    total_count = len(test_results)
    
    print(f"\n🎯 Общий результат: {success_count}/{total_count} тестов пройдено")
    
    if success_count == total_count:
        print("🎉 Все тесты RAG интеграции прошли успешно!")
        print("🚀 RAG система готова к использованию!")
    else:
        print("⚠️ Некоторые тесты не пройдены, требуется доработка")
    
    print(f"🕒 Время завершения: {datetime.now().isoformat()}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()