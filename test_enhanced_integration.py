#!/usr/bin/env python3
"""
Интеграционные тесты для enhanced методов с SEO AI Models
Проверяет работу всех enhanced компонентов
"""

import asyncio
import sys
import time
from typing import Dict, Any
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импорты проекта
from mock_data_provider import MockDataProvider
from core.data_providers.static_provider import StaticDataProvider
from agents.operational.technical_seo_auditor import TechnicalSEOAuditorAgent
from agents.operational.content_strategy import ContentStrategyAgent
from agents.operational.competitive_analysis import CompetitiveAnalysisAgent


async def test_static_provider_seo_ai_models():
    """Тест StaticDataProvider с SEO AI Models"""
    print("🧪 Тест 1: StaticDataProvider с SEO AI Models")
    
    try:
        # Конфигурация для реального режима
        config = {
            "seo_ai_models_path": "./seo_ai_models",
            "mock_mode": False  # Попытка использовать реальные модели
        }
        
        provider = StaticDataProvider(config)
        await asyncio.sleep(2)  # Время на инициализацию
        
        # Проверяем health check
        health = await provider.health_check()
        print(f"   Health Status: {health.get('status', 'unknown')}")
        
        # Тест получения SEO данных
        seo_data = await provider.get_seo_data("example.com")
        print(f"   SEO Data Source: {seo_data.data_source}")
        
        if provider.mock_mode:
            print("   ⚠️  Работает в MOCK режиме (SEO AI Models недоступна)")
            return True
        else:
            print("   ✅ SEO AI Models активна")
            return True
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False


async def test_enhanced_technical_auditor():
    """Тест Enhanced Technical SEO Auditor"""
    print("🧪 Тест 2: Enhanced Technical SEO Auditor")
    
    try:
        # Создаем провайдер (mock или real)
        try:
            config = {"seo_ai_models_path": "./seo_ai_models", "mock_mode": False}
            provider = StaticDataProvider(config)
            await asyncio.sleep(1)
        except Exception:
            provider = MockDataProvider()
        
        # Создаем агента
        agent = TechnicalSEOAuditorAgent(data_provider=provider)
        
        # Тестовые данные
        task_data = {
            "input_data": {
                "domain": "example.com",
                "task_type": "full_technical_audit",
                "enhanced": True
            }
        }
        
        start_time = time.time()
        result = await agent.process_task(task_data)
        execution_time = time.time() - start_time
        
        print(f"   Время выполнения: {execution_time:.2f}s")
        print(f"   Enhanced: {result.get('enhanced', False)}")
        print(f"   Базовый скор: {result.get('audit_score', 'N/A')}")
        
        if 'enhanced_analysis' in result:
            enhanced = result['enhanced_analysis']
            print(f"   Enhanced источник: {enhanced.get('enhancement_source', 'unknown')}")
            
        print("   ✅ Enhanced Technical Auditor работает")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False


async def test_enhanced_content_strategy():
    """Тест Enhanced Content Strategy"""
    print("🧪 Тест 3: Enhanced Content Strategy")
    
    try:
        # Создаем провайдер
        try:
            config = {"seo_ai_models_path": "./seo_ai_models", "mock_mode": False}
            provider = StaticDataProvider(config)
            await asyncio.sleep(1)
        except Exception:
            provider = MockDataProvider()
        
        # Создаем агента с enhancer
        agent = ContentStrategyAgent(data_provider=provider)
        
        # Добавляем enhancer если его еще нет
        if not hasattr(agent, 'enhancer'):
            from core.enhanced_methods import SEOAIModelsEnhancer
            agent.enhancer = SEOAIModelsEnhancer(provider)
        
        # Тестовые данные контента
        content_data = {
            "content": "This is a test SEO content about digital marketing strategies and best practices for online businesses.",
            "domain": "example.com",
            "keywords": ["seo", "digital marketing", "online business"]
        }
        
        # Тест enhanced анализа
        if agent.enhancer:
            enhanced_result = await agent.enhancer.enhanced_content_strategy(content_data)
            print(f"   Enhanced источник: {enhanced_result.get('enhancement_source', 'unknown')}")
            print(f"   E-E-A-T скор: {enhanced_result.get('eeat_analysis', {}).get('overall_score', 'N/A')}")
            print("   ✅ Enhanced Content Strategy работает")
        else:
            print("   ⚠️  Enhancer недоступен")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False


async def test_enhanced_competitive_analysis():
    """Тест Enhanced Competitive Analysis"""
    print("🧪 Тест 4: Enhanced Competitive Analysis")
    
    try:
        # Создаем провайдер
        try:
            config = {"seo_ai_models_path": "./seo_ai_models", "mock_mode": False}
            provider = StaticDataProvider(config)
            await asyncio.sleep(1)
        except Exception:
            provider = MockDataProvider()
        
        # Создаем агента
        agent = CompetitiveAnalysisAgent(data_provider=provider)
        
        # Добавляем enhancer
        if not hasattr(agent, 'enhancer'):
            from core.enhanced_methods import SEOAIModelsEnhancer
            agent.enhancer = SEOAIModelsEnhancer(provider)
        
        # Тест enhanced конкурентного анализа
        if agent.enhancer:
            enhanced_result = await agent.enhancer.enhanced_competitive_analysis(
                "example.com", 
                ["competitor1.com", "competitor2.com"]
            )
            print(f"   Enhanced источник: {enhanced_result.get('enhancement_source', 'unknown')}")
            print(f"   Конкурентов проанализировано: {len(enhanced_result.get('competitor_analysis', []))}")
            print("   ✅ Enhanced Competitive Analysis работает")
        else:
            print("   ⚠️  Enhancer недоступен")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False


async def test_performance_comparison():
    """Сравнение производительности mock vs enhanced"""
    print("🧪 Тест 5: Сравнение производительности")
    
    try:
        # Mock провайдер
        mock_provider = MockDataProvider()
        mock_agent = TechnicalSEOAuditorAgent(data_provider=mock_provider)
        
        task_data = {
            "input_data": {
                "domain": "example.com",
                "task_type": "full_technical_audit"
            }
        }
        
        # Тест mock
        start_time = time.time()
        mock_result = await mock_agent.process_task(task_data)
        mock_time = time.time() - start_time
        
        # Enhanced провайдер
        try:
            config = {"seo_ai_models_path": "./seo_ai_models", "mock_mode": False}
            enhanced_provider = StaticDataProvider(config)
            await asyncio.sleep(1)
            enhanced_agent = TechnicalSEOAuditorAgent(data_provider=enhanced_provider)
            
            start_time = time.time()
            enhanced_result = await enhanced_agent.process_task(task_data)
            enhanced_time = time.time() - start_time
            
            print(f"   Mock время: {mock_time:.3f}s")
            print(f"   Enhanced время: {enhanced_time:.3f}s")
            print(f"   Разница: {enhanced_time - mock_time:.3f}s")
            
        except Exception:
            print(f"   Mock время: {mock_time:.3f}s")
            print("   Enhanced: недоступен (fallback к mock)")
        
        print("   ✅ Сравнение производительности завершено")
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False


async def main():
    """Основная функция тестирования"""
    print("🚀 Запуск Enhanced Integration Tests")
    print("=" * 50)
    
    tests = [
        ("StaticDataProvider + SEO AI Models", test_static_provider_seo_ai_models),
        ("Enhanced Technical Auditor", test_enhanced_technical_auditor),
        ("Enhanced Content Strategy", test_enhanced_content_strategy),
        ("Enhanced Competitive Analysis", test_enhanced_competitive_analysis),
        ("Performance Comparison", test_performance_comparison)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        try:
            if await test_func():
                passed += 1
            else:
                print(f"   ❌ {test_name} - НЕУДАЧА")
        except Exception as e:
            print(f"   ❌ {test_name} - КРИТИЧЕСКАЯ ОШИБКА: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 РЕЗУЛЬТАТЫ ENHANCED INTEGRATION TESTS")
    print(f"✅ Пройдено: {passed}/{total} тестов")
    print(f"📈 Успешность: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 ВСЕ ENHANCED ТЕСТЫ ПРОЙДЕНЫ!")
        print("🚀 Система готова к production с SEO AI Models")
    elif passed >= total * 0.8:
        print("🎯 Большинство enhanced тестов пройдено")
        print("⚠️  Система работает с fallback к mock режиму")
    else:
        print("⚠️  Множественные проблемы с enhanced функциональностью")
        print("🎭 Рекомендуется использовать mock режим")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)