"""
Отладка Lead Qualification Agent
"""

import asyncio
import json
from datetime import datetime
from core.config import AIAgentsConfig
from agents.operational.lead_qualification import LeadQualificationAgent

async def debug_lead_qualification():
    """Детальная отладка работы Lead Qualification Agent"""
    
    print("🔍 ОТЛАДКА LEAD QUALIFICATION AGENT")
    print("=" * 50)
    
    # Инициализация
    config = AIAgentsConfig()
    data_provider = config.get_data_provider()
    lead_agent = LeadQualificationAgent(data_provider=data_provider)
    
    # Простые тестовые данные
    test_data = {
        "input_data": {
            "company_name": "TechCorp Solutions",
            "contact_name": "Анна Петрова",
            "email": "anna@techcorp.ru",
            "phone": "+7-495-123-4567",
            "website": "https://techcorp.ru",
            "company_size": "150 employees",
            "industry": "SaaS",
            "lead_source": "website_form",
            "current_seo_budget": "45000",
            "goals": ["Увеличить трафик"],
            "pain_points": ["Низкие позиции"],
            "timeline": "2-3 месяца",
            "budget_range": "50000-100000",
            "decision_making_authority": "yes"
        }
    }
    
    print("📋 Входные данные:")
    for key, value in test_data["input_data"].items():
        print(f"   {key}: {value}")
    
    print("\n🏃 Запуск обработки...")
    
    try:
        result = await lead_agent.process_task(test_data)
        
        print("\n📊 ПОЛНЫЙ РЕЗУЛЬТАТ:")
        print("=" * 30)
        
        # Выводим ВСЕ ключи результата
        for key, value in result.items():
            if key == "detailed_scoring":
                print(f"📈 {key}:")
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        print(f"     {sub_key}: {sub_value}")
                else:
                    print(f"     {value}")
            else:
                print(f"📌 {key}: {value}")
        
        print("\n🎯 КЛЮЧЕВЫЕ ПРОБЛЕМЫ:")
        issues = []
        
        if result.get("final_score") is None:
            issues.append("❌ final_score is None - должен быть числом")
        
        if result.get("classification") is None:
            issues.append("❌ classification is None - должен быть строкой")
        
        if result.get("estimated_deal_value", 0) == 0:
            issues.append("⚠️ estimated_deal_value is 0 - должен быть > 0")
        
        if not issues:
            print("✅ Все ключевые поля заполнены корректно!")
        else:
            for issue in issues:
                print(f"   {issue}")
                
        return result
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        print("📜 ПОЛНАЯ TRACEBACK:")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(debug_lead_qualification())
