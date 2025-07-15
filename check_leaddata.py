"""
Проверка полей LeadData модели
"""

from agents.operational.lead_qualification import LeadData
import inspect

def check_leaddata_fields():
    """Проверяет какие поля требует LeadData модель"""
    
    print("🔍 АНАЛИЗ LEADDATA МОДЕЛИ")
    print("=" * 40)
    
    # Получаем аннотации полей
    if hasattr(LeadData, '__annotations__'):
        annotations = LeadData.__annotations__
        print("📋 Обязательные поля:")
        for field_name, field_type in annotations.items():
            print(f"   - {field_name}: {field_type}")
    
    # Пробуем создать пустой объект чтобы увидеть какие поля требуются
    print("\n🧪 ТЕСТ СОЗДАНИЯ ОБЪЕКТА С МИНИМАЛЬНЫМИ ДАННЫМИ:")
    
    test_data = {
        "company_name": "Test Company",
        "contact_name": "Test Contact", 
        "email": "test@test.com",
        "phone": "+7-123-456-7890",
        "website": "https://test.com",
        "company_size": "50 employees",
        "industry": "Technology",
        "lead_source": "website",
        "current_seo_budget": "0",
        "timeline": "3 months",
        "budget_range": "10000-50000",
        "decision_making_authority": "yes"
    }
    
    try:
        lead_obj = LeadData(**test_data)
        print("✅ Базовые поля корректны!")
        print(f"   Создан объект: {lead_obj.company_name}")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    check_leaddata_fields()
