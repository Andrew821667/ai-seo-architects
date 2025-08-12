#!/usr/bin/env python3
"""
🤖 Тест LLM интеграции в агентах AI SEO Architects
Проверяем реальные вызовы OpenAI API с промптами
"""

import asyncio
import os
from datetime import datetime

# Тестируемые агенты
from agents.operational.lead_qualification import LeadQualificationAgent
from agents.operational.technical_seo_auditor import TechnicalSEOAuditorAgent

async def test_lead_qualification_llm():
    """Тест Lead Qualification Agent с реальным OpenAI API"""
    print("🔍 Тестирование Lead Qualification Agent с LLM...")
    
    # Создаем агента
    agent = LeadQualificationAgent()
    
    # Тестовые данные лида
    test_data = {
        "input_data": {
            "company_name": "TechCorp Solutions",
            "industry": "fintech",
            "company_size": "500",
            "budget_range": "500000",
            "timeline": "3 months",
            "contact_role": "CMO",
            "email": "cmo@techcorp.com",
            "pain_points": "Low search visibility, poor lead generation",
            "goals": "Increase organic traffic by 300%",
            "current_seo": "Basic on-page optimization only"
        }
    }
    
    print(f"📤 Отправляем задачу агенту: {test_data['input_data']['company_name']}")
    
    # Выполняем задачу
    result = await agent.process_task_with_retry(test_data)
    
    print(f"📥 Результат: {result['success']}")
    if result["success"]:
        print(f"🤖 Модель: {result.get('model_used', 'unknown')}")
        print(f"🔢 Токены: {result.get('tokens_used', {})}")
        print(f"📄 Ответ (первые 200 символов): {str(result.get('result', ''))[:200]}...")
    else:
        print(f"❌ Ошибка: {result.get('error', 'unknown')}")
        if result.get('fallback_mode'):
            print("✅ Fallback режим работает корректно")
    
    return result

async def test_technical_seo_llm():
    """Тест Technical SEO Auditor Agent с реальным OpenAI API"""
    print("\n🔧 Тестирование Technical SEO Auditor Agent с LLM...")
    
    # Создаем агента
    agent = TechnicalSEOAuditorAgent()
    
    # Тестовые данные сайта
    test_data = {
        "input_data": {
            "domain": "example-ecommerce.com",
            "task_type": "full_technical_audit",
            "site_type": "e-commerce",
            "technology": "WordPress + WooCommerce",
            "current_issues": "Slow loading, poor mobile experience",
            "business_goals": "Improve search rankings and user experience",
            "target_audience": "Online shoppers"
        }
    }
    
    print(f"🌐 Отправляем аудит для домена: {test_data['input_data']['domain']}")
    
    # Выполняем задачу
    result = await agent.process_task_with_retry(test_data)
    
    print(f"📥 Результат: {result['success']}")
    if result["success"]:
        print(f"🤖 Модель: {result.get('model_used', 'unknown')}")
        print(f"🔢 Токены: {result.get('tokens_used', {})}")
        print(f"📄 Ответ (первые 300 символов): {str(result.get('result', ''))[:300]}...")
    else:
        print(f"❌ Ошибка: {result.get('error', 'unknown')}")
        if result.get('fallback_mode'):
            print("✅ Fallback режим работает корректно")
    
    return result

async def test_openai_api_key():
    """Проверяем наличие OpenAI API ключа"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY найден: {api_key[:10]}...{api_key[-4:]}")
        return True
    else:
        print("⚠️ OPENAI_API_KEY не установлен - будет использоваться fallback режим")
        return False

async def main():
    """Основная функция тестирования LLM интеграции"""
    print("🚀 AI SEO Architects - LLM Integration Test")
    print("=" * 60)
    print(f"Время начала: {datetime.now()}")
    
    # Проверяем API ключ
    has_api_key = await test_openai_api_key()
    
    results = {
        "lead_qualification": None,
        "technical_seo": None,
        "api_key_present": has_api_key
    }
    
    try:
        # Тест Lead Qualification
        results["lead_qualification"] = await test_lead_qualification_llm()
        
        # Тест Technical SEO Auditor  
        results["technical_seo"] = await test_technical_seo_llm()
        
    except Exception as e:
        print(f"❌ Критическая ошибка тестирования: {str(e)}")
        return 1
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ LLM ИНТЕГРАЦИИ")
    print("=" * 60)
    
    successful_tests = 0
    total_tests = 2
    
    if results["lead_qualification"] and results["lead_qualification"]["success"]:
        print("✅ Lead Qualification Agent: LLM интеграция работает")
        successful_tests += 1
    else:
        print("❌ Lead Qualification Agent: Проблемы с LLM")
    
    if results["technical_seo"] and results["technical_seo"]["success"]:
        print("✅ Technical SEO Auditor: LLM интеграция работает")  
        successful_tests += 1
    else:
        print("❌ Technical SEO Auditor: Проблемы с LLM")
    
    success_rate = (successful_tests / total_tests) * 100
    print(f"\n🎯 Успешность LLM интеграции: {success_rate:.1f}% ({successful_tests}/{total_tests})")
    
    if has_api_key and success_rate >= 100:
        print("🎉 ОТЛИЧНО! Все агенты успешно используют OpenAI API с промптами")
        return 0
    elif not has_api_key and success_rate >= 100:
        print("✅ ХОРОШО! Fallback режимы работают корректно (нужен OPENAI_API_KEY для полного тестирования)")
        return 0
    else:
        print("⚠️ ВНИМАНИЕ! Есть проблемы с LLM интеграцией")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)