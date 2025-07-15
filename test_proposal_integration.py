"""
Тестирование интеграции Lead Qualification → Proposal Generation
AI SEO Architects - Milestone 3 - ИСПРАВЛЕННАЯ ВЕРСИЯ
"""

import asyncio
import json
from datetime import datetime
from core.config import AIAgentsConfig
from agents.operational.lead_qualification import LeadQualificationAgent
from agents.operational.proposal_generation import ProposalGenerationAgent

async def test_proposal_integration():
    """Полный тест интеграции: Lead Qualification → Proposal Generation"""
    
    print("🚀 Тестирование интеграции Lead Qualification → Proposal Generation")
    print("=" * 70)
    
    # Инициализация конфигурации
    config = AIAgentsConfig()
    data_provider = config.get_data_provider()
    
    # Создание агентов
    lead_agent = LeadQualificationAgent(data_provider=data_provider)
    proposal_agent = ProposalGenerationAgent(data_provider=data_provider)
    
    # ИСПРАВЛЕННЫЕ тестовые данные лида (соответствуют LeadData модели)
    test_lead_data = {
        "input_data": {
            "company_name": "TechCorp Solutions",  # Было: company
            "contact_name": "Анна Петрова",
            "email": "anna@techcorp.ru", 
            "phone": "+7-495-123-4567",
            "website": "https://techcorp.ru",
            "company_size": "150 employees",        # Было: employees (число)
            "industry": "SaaS",
            "lead_source": "website_form",          # Было: source
            "current_seo_budget": "45000",          # Строка вместо числа
            "goals": [
                "Увеличить органический трафик",
                "Улучшить конверсию с сайта", 
                "Повысить видимость в поиске"
            ],
            "pain_points": [
                "Низкие позиции в поиске",
                "Маленький поток заявок с сайта",
                "Высокая стоимость контекстной рекламы"
            ],
            "timeline": "2-3 месяца",
            "budget_range": "50000-100000",
            "decision_making_authority": "yes"       # Было: decision_maker
        }
    }
    
    print("📋 Тестовые данные лида (исправленные):")
    print(f"   Компания: {test_lead_data['input_data']['company_name']}")
    print(f"   Отрасль: {test_lead_data['input_data']['industry']}")
    print(f"   Размер: {test_lead_data['input_data']['company_size']}")
    print(f"   Текущий SEO бюджет: {test_lead_data['input_data']['current_seo_budget']} руб.")
    print(f"   Источник: {test_lead_data['input_data']['lead_source']}")
    print()
    
    # Этап 1: Lead Qualification
    print("📊 ЭТАП 1: Квалификация лида")
    print("-" * 30)
    
    start_time = datetime.now()
    
    try:
        lead_result = await lead_agent.process_task(test_lead_data)
        lead_time = (datetime.now() - start_time).total_seconds()
        
        print(f"⏱️  Время выполнения: {lead_time:.2f}с")
        print(f"📊 Lead Score: {lead_result.get('final_score')}/100")
        print(f"📋 Квалификация: {lead_result.get('classification')}")
        print(f"🎯 Тип лида: {lead_result.get('lead_type')}")
        print(f"💰 Оценочная стоимость: ${lead_result.get('estimated_deal_value', 0):,}")
        print(f"🔍 Уверенность: {lead_result.get('confidence_score', 0):.1%}")
        print()
        
        # Этап 2: Proposal Generation только если квалификация прошла успешно
        if lead_result.get("final_score", 0) > 0:
            print("📄 ЭТАП 2: Генерация предложения")
            print("-" * 30)
            
            # Подготавливаем данные для proposal agent
            proposal_input = {
                "input_data": {
                    "lead_qualification_result": lead_result,
                    "client_requirements": {
                        "services_interest": ["seo_audit", "monthly_seo", "content_strategy"],
                        "budget_confirmed": True,
                        "timeline_flexibility": "medium"
                    },
                    "proposal_type": "standard",
                    "urgency": "medium"
                }
            }
            
            start_time = datetime.now()
            proposal_result = await proposal_agent.process_task(proposal_input)
            proposal_time = (datetime.now() - start_time).total_seconds()
            
            print(f"⏱️  Время выполнения: {proposal_time:.2f}с")
            
            if proposal_result.get("proposal_data"):
                proposal_data = proposal_result["proposal_data"]
                pricing = proposal_data.get("pricing", {})
                
                print(f"📄 Proposal ID: {proposal_data.get('proposal_id')}")
                print(f"💰 Общая стоимость первого года: ${pricing.get('total_annual', 0):,}")
                print(f"💰 Единоразовые расходы: ${pricing.get('total_one_time', 0):,}")
                print(f"💰 Ежемесячные расходы: ${pricing.get('total_monthly', 0):,}")
                print(f"🎯 Уверенность: {proposal_data.get('confidence_score', 0):.1%}")
                
                # ROI проекции
                roi_data = proposal_data.get("roi_projections", {})
                if roi_data and "projections" in roi_data:
                    roi_12m = roi_data["projections"].get("12_months", {})
                    print(f"📈 Прогноз ROI (12 мес): {roi_12m.get('roi_percentage', 'N/A')}")
                    print(f"💵 Прогноз выручки: ${roi_12m.get('annual_revenue', 0):,}/год")
                
                # Пакетные предложения
                packages = pricing.get("packages", {})
                if packages:
                    print(f"\n📦 Доступные пакеты: {len(packages)}")
                    for package_name, package_data in packages.items():
                        one_time = package_data.get('one_time_price', 0)
                        monthly = package_data.get('monthly_price', 0)
                        print(f"   - {package_data['name']}: ${one_time:,} + ${monthly:,}/мес")
                
                print()
                
                # Суммарная статистика
                print("📊 ИТОГОВАЯ СТАТИСТИКА")
                print("=" * 30)
                print(f"⏱️  Общее время выполнения: {lead_time + proposal_time:.2f}с")
                print(f"🔄 Интеграция агентов: ✅ Успешно")
                print(f"📈 Производительность: {1/(lead_time + proposal_time):.1f} предложений/сек")
                
                # Детальный анализ качества
                print(f"\n🎯 АНАЛИЗ КАЧЕСТВА")
                print("=" * 20)
                
                lead_score = lead_result.get("final_score", 0)
                confidence = proposal_data.get("confidence_score", 0)
                
                print(f"📊 Качество квалификации: {'Высокое' if lead_score >= 70 else 'Среднее' if lead_score >= 50 else 'Низкое'}")
                print(f"🎯 Качество предложения: {'Высокое' if confidence >= 0.8 else 'Среднее' if confidence >= 0.6 else 'Низкое'}")
                print(f"💼 Готовность к отправке: {'✅ Да' if confidence >= 0.7 and lead_score >= 40 else '⚠️ Требует проверки'}")
                
                # Рекомендации
                next_steps = proposal_data.get("next_steps", [])
                if next_steps:
                    print(f"\n📋 СЛЕДУЮЩИЕ ШАГИ:")
                    for i, step in enumerate(next_steps[:3], 1):
                        print(f"   {i}. {step}")
                
                return {
                    "lead_result": lead_result,
                    "proposal_result": proposal_result,
                    "total_time": lead_time + proposal_time,
                    "success": True
                }
            else:
                print("❌ Ошибка генерации предложения:")
                print(f"   {proposal_result.get('error', 'Неизвестная ошибка')}")
                return {
                    "lead_result": lead_result,
                    "proposal_result": proposal_result,
                    "total_time": lead_time,
                    "success": False
                }
        else:
            print("⚠️ Лид не прошел квалификацию - пропускаем генерацию предложения")
            return {
                "lead_result": lead_result,
                "proposal_result": None,
                "total_time": lead_time,
                "success": False
            }
            
    except Exception as e:
        lead_time = (datetime.now() - start_time).total_seconds()
        print(f"❌ Ошибка квалификации лида: {str(e)}")
        print(f"⏱️  Время до ошибки: {lead_time:.2f}с")
        
        return {
            "lead_result": None,
            "proposal_result": None,
            "total_time": lead_time,
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Запуск теста
    print("🔧 Запуск исправленного теста интеграции...")
    result = asyncio.run(test_proposal_integration())
    
    if result["success"]:
        print(f"\n🏆 ТЕСТ ЗАВЕРШЕН УСПЕШНО!")
        print(f"💾 Интеграция работает корректно за {result['total_time']:.2f}с")
    else:
        print(f"\n⚠️ ТЕСТ ЗАВЕРШЕН С ПРОБЛЕМАМИ")
        if "error" in result:
            print(f"❌ Ошибка: {result['error']}")
        print("🔧 Требуется дополнительная отладка")
