#!/usr/bin/env python3
"""
Тест интеграции всех 5 агентов AI SEO Architects
Проверяет совместную работу агентов в полном цикле
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Any

# Добавляем путь к проекту
sys.path.insert(0, '.')

# Импорт агентов
from agents.executive.business_development_director import BusinessDevelopmentDirectorAgent
from agents.executive.chief_seo_strategist import ChiefSEOStrategistAgent
from agents.management.task_coordination import TaskCoordinationAgent  
from agents.operational.lead_qualification import LeadQualificationAgent
from agents.operational.proposal_generation import ProposalGenerationAgent
from agents.operational.sales_conversation import SalesConversationAgent
from mock_data_provider import MockDataProvider

def print_section(title: str):
    """Печать заголовка секции"""
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print('='*60)

def print_success(message: str):
    """Печать успешного результата"""
    print(f"✅ {message}")

def print_error(message: str):
    """Печать ошибки"""
    print(f"❌ {message}")

def print_info(message: str):
    """Печать информации"""
    print(f"ℹ️  {message}")

async def test_agent_initialization():
    """Тест 1: Инициализация всех агентов"""
    print_section("ТЕСТ 1: Инициализация агентов")
    
    agents = {}
    
    try:
        # Создаем mock data provider
        mock_provider = MockDataProvider()
        print_info(f"Mock Data Provider создан: {mock_provider.name}")
        
        # Chief SEO Strategist
        agents['chief_seo_strategist'] = ChiefSEOStrategistAgent(data_provider=mock_provider)
        print_success(f"Chief SEO Strategist инициализирован: {agents['chief_seo_strategist'].name}")
        
        # Business Development Director
        agents['bd_director'] = BusinessDevelopmentDirectorAgent(data_provider=mock_provider)
        print_success(f"Business Development Director инициализирован: {agents['bd_director'].name}")
        
        # Task Coordination Agent
        agents['task_coordinator'] = TaskCoordinationAgent(data_provider=mock_provider)
        print_success(f"Task Coordination Agent инициализирован: {agents['task_coordinator'].name}")
        
        # Lead Qualification Agent
        agents['lead_qualification'] = LeadQualificationAgent(data_provider=mock_provider)
        print_success(f"Lead Qualification Agent инициализирован: {agents['lead_qualification'].name}")
        
        # Proposal Generation Agent
        agents['proposal_generation'] = ProposalGenerationAgent(data_provider=mock_provider)
        print_success(f"Proposal Generation Agent инициализирован: {agents['proposal_generation'].name}")
        
        # Sales Conversation Agent
        agents['sales_conversation'] = SalesConversationAgent(data_provider=mock_provider)
        print_success(f"Sales Conversation Agent инициализирован: {agents['sales_conversation'].name}")
        
        print_info(f"Всего агентов инициализировано: {len(agents)}")
        return agents
        
    except Exception as e:
        print_error(f"Ошибка инициализации агентов: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_lead_qualification_flow(agents: Dict[str, Any]):
    """Тест 2: Полный цикл квалификации лида"""
    print_section("ТЕСТ 2: Цикл квалификации лида")
    
    # Создаем тестовые данные лида
    lead_data = {
        "company_name": "TechCorp Solutions",
        "email": "ceo@techcorp.ru",
        "phone": "+7-495-123-4567",
        "website": "https://techcorp.ru",
        "contact_name": "Алексей Петров",
        "contact_role": "CEO",
        "industry": "fintech",
        "company_size": "1000", 
        "budget_range": "5000000-10000000",
        "timeline": "Q2 2025",
        "current_seo": "basic",
        "pain_points": ["Низкий органический трафик", "Высокий CAC", "Слабые позиции в поиске"],
        "goals": ["Увеличить трафик на 300%", "Снизить стоимость привлечения клиентов"],
        "source": "website_form",
        "utm_source": "google",
        "utm_campaign": "seo_services"
    }
    
    try:
        # Шаг 1: Квалификация лида
        print_info("Шаг 1: Квалификация лида...")
        
        qualification_task = {
            "input_data": lead_data,
            "task_type": "lead_qualification"
        }
        
        qualification_result = await agents['lead_qualification'].process_task(qualification_task)
        
        if qualification_result.get('success', False):
            lead_score = qualification_result.get('lead_score', 0)
            qualification = qualification_result.get('qualification', 'Unknown')
            print_success(f"Лид квалифицирован: {qualification} (Score: {lead_score}/100)")
        else:
            print_error(f"Ошибка квалификации: {qualification_result.get('error', 'Unknown error')}")
            return None
            
        return qualification_result
        
    except Exception as e:
        print_error(f"Ошибка в цикле квалификации: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_sales_conversation_flow(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 3: Sales conversation процесс"""
    print_section("ТЕСТ 3: Sales Conversation")
    
    try:
        print_info("Проведение sales conversation...")
        
        conversation_task = {
            "input_data": {
                "qualification_result": qualification_result,
                "lead_data": qualification_result.get('enriched_data', {}),
                "conversation_type": "full_sales_conversation"
            },
            "conversation_type": "full_sales_conversation"
        }
        
        conversation_result = await agents['sales_conversation'].process_task(conversation_task)
        
        if conversation_result.get('success', False):
            quality = conversation_result.get('conversation_quality', 'Unknown')
            probability = conversation_result.get('probability_to_close', 0)
            print_success(f"Sales conversation завершен: {quality} качество, {probability:.1%} вероятность закрытия")
        else:
            print_error(f"Ошибка sales conversation: {conversation_result.get('error', 'Unknown error')}")
            return None
            
        return conversation_result
        
    except Exception as e:
        print_error(f"Ошибка в sales conversation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_proposal_generation_flow(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 4: Генерация предложения"""
    print_section("ТЕСТ 4: Генерация предложения")
    
    try:
        print_info("Генерация коммерческого предложения...")
        
        proposal_task = {
            "input_data": {
                "lead_qualification_result": qualification_result,
                "client_requirements": {
                    "focus_areas": ["technical_seo", "content_marketing"],
                    "priority": "high"
                },
                "proposal_type": "standard",
                "urgency": "medium"
            }
        }
        
        proposal_result = await agents['proposal_generation'].process_task(proposal_task)
        
        if proposal_result.get('success', False):
            proposal_data = proposal_result.get('proposal_data', {})
            total_annual = proposal_data.get('pricing', {}).get('total_annual', 0)
            confidence = proposal_data.get('confidence_score', 0)
            print_success(f"Предложение сгенерировано: {total_annual:,} ₽/год, confidence: {confidence}")
        else:
            print_error(f"Ошибка генерации предложения: {proposal_result.get('error', 'Unknown error')}")
            return None
            
        return proposal_result
        
    except Exception as e:
        print_error(f"Ошибка в генерации предложения: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_business_development_assessment(agents: Dict[str, Any], qualification_result: Dict[str, Any], proposal_result: Dict[str, Any]):
    """Тест 5: BD Director assessment"""
    print_section("ТЕСТ 5: Business Development Assessment")
    
    try:
        print_info("BD Director анализирует возможность...")
        
        # Подготавливаем данные для BD Director
        bd_task = {
            "input_data": {
                "task_type": "enterprise_assessment",
                **qualification_result.get('enriched_data', {})
            },
            "lead_analysis": qualification_result,
            "proposal_data": proposal_result.get('proposal_data', {})
        }
        
        bd_result = await agents['bd_director'].process_task(bd_task)
        
        if bd_result.get('success', False):
            strategic_impact = bd_result.get('strategic_impact', 'Unknown')
            deal_size = bd_result.get('deal_size', 0) 
            confidence = bd_result.get('confidence_score', 0)
            print_success(f"BD Assessment: {strategic_impact} impact, {deal_size:,} ₽ deal size, {confidence:.2f} confidence")
        else:
            print_error(f"Ошибка BD assessment: {bd_result.get('error', 'Unknown error')}")
            return None
            
        return bd_result
        
    except Exception as e:
        print_error(f"Ошибка в BD assessment: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_seo_strategic_analysis(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 6: Chief SEO Strategist анализ"""
    print_section("ТЕСТ 6: SEO Strategic Analysis")
    
    try:
        print_info("Chief SEO Strategist проводит стратегический анализ...")
        
        seo_task = {
            "input_data": {
                "task_type": "seo_strategic_analysis",
                **qualification_result.get('enriched_data', {}),
                "monthly_organic_traffic": 150000,
                "ranking_keywords_count": 12500,
                "domain_authority": 45,
                "current_seo_spend": 180000
            }
        }
        
        seo_result = await agents['chief_seo_strategist'].process_task(seo_task)
        
        if seo_result.get('success', False):
            strategic_impact = seo_result.get('strategic_impact', 'Unknown')
            investment_req = seo_result.get('investment_requirement', 0)
            confidence = seo_result.get('confidence_score', 0)
            print_success(f"SEO Analysis: {strategic_impact} impact, {investment_req:,} ₽ investment, {confidence:.2f} confidence")
        else:
            print_error(f"Ошибка SEO analysis: {seo_result.get('error', 'Unknown error')}")
            return None
            
        return seo_result
        
    except Exception as e:
        print_error(f"Ошибка в SEO strategic analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_task_coordination(agents: Dict[str, Any]):
    """Тест 7: Task Coordination"""
    print_section("ТЕСТ 7: Task Coordination")
    
    try:
        print_info("Task Coordinator маршрутизует задачу...")
        
        coordination_task = {
            "task_type": "lead_processing",
            "priority": "high",
            "client_context": {
                "industry": "fintech",
                "size": "enterprise"
            }
        }
        
        coordination_result = await agents['task_coordinator'].process_task(coordination_task)
        
        if coordination_result.get('success', False):
            routed_to = coordination_result.get('routed_to', 'Unknown')
            priority_score = coordination_result.get('priority_score', 0)
            print_success(f"Задача маршрутизирована к {routed_to}, приоритет: {priority_score}")
        else:
            print_error(f"Ошибка координации: {coordination_result.get('error', 'Unknown error')}")
            return None
            
        return coordination_result
        
    except Exception as e:
        print_error(f"Ошибка в task coordination: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_full_integration():
    """Полный интеграционный тест"""
    print_section("ПОЛНЫЙ ИНТЕГРАЦИОННЫЙ ТЕСТ AI SEO ARCHITECTS")
    
    test_results = {
        'initialization': False,
        'lead_qualification': False,
        'sales_conversation': False,
        'proposal_generation': False,
        'bd_assessment': False,
        'seo_strategic_analysis': False,
        'task_coordination': False
    }
    
    # Тест 1: Инициализация
    agents = await test_agent_initialization()
    if agents:
        test_results['initialization'] = True
    else:
        print_error("Критическая ошибка: не удалось инициализировать агентов")
        return test_results
    
    # Тест 2: Квалификация лида
    qualification_result = await test_lead_qualification_flow(agents)
    if qualification_result:
        test_results['lead_qualification'] = True
    else:
        print_error("Ошибка квалификации лида")
        return test_results
    
    # Тест 3: Sales conversation (параллельно с proposal)
    sales_task = test_sales_conversation_flow(agents, qualification_result)
    proposal_task = test_proposal_generation_flow(agents, qualification_result)
    
    # Запускаем параллельно
    sales_result, proposal_result = await asyncio.gather(sales_task, proposal_task, return_exceptions=True)
    
    if not isinstance(sales_result, Exception) and sales_result:
        test_results['sales_conversation'] = True
    
    if not isinstance(proposal_result, Exception) and proposal_result:
        test_results['proposal_generation'] = True
    
    # Тест 5: BD Assessment
    if proposal_result and qualification_result:
        bd_result = await test_business_development_assessment(agents, qualification_result, proposal_result)
        if bd_result:
            test_results['bd_assessment'] = True
    
    # Тест 6: SEO Strategic Analysis
    if qualification_result:
        seo_result = await test_seo_strategic_analysis(agents, qualification_result)
        if seo_result:
            test_results['seo_strategic_analysis'] = True
    
    # Тест 7: Task Coordination
    coordination_result = await test_task_coordination(agents)
    if coordination_result:
        test_results['task_coordination'] = True
    
    return test_results

async def main():
    """Главная функция"""
    print("🚀 ЗАПУСК ИНТЕГРАЦИОННОГО ТЕСТИРОВАНИЯ AI SEO ARCHITECTS")
    print(f"📅 Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = datetime.now()
    
    # Запуск полного интеграционного теста
    results = await test_full_integration()
    
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    # Отчет о результатах
    print_section("ОТЧЕТ О РЕЗУЛЬТАТАХ ТЕСТИРОВАНИЯ")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = passed_tests / total_tests * 100
    
    print(f"📊 Общие результаты:")
    print(f"   Всего тестов: {total_tests}")
    print(f"   Успешно: {passed_tests}")
    print(f"   Провалено: {total_tests - passed_tests}")
    print(f"   Процент успеха: {success_rate:.1f}%")
    print(f"   Время выполнения: {execution_time:.2f} секунд")
    
    print(f"\n📋 Детальные результаты:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name.replace('_', ' ').title()}: {status}")
    
    if success_rate >= 80:
        print(f"\n🎉 ИНТЕГРАЦИОННОЕ ТЕСТИРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО!")
        print(f"   Система готова к продакшену")
    elif success_rate >= 60:
        print(f"\n⚠️  ЧАСТИЧНЫЙ УСПЕХ")
        print(f"   Система работает, но требует доработки")
    else:
        print(f"\n🔥 КРИТИЧЕСКИЕ ПРОБЛЕМЫ")
        print(f"   Система требует серьезной отладки")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())