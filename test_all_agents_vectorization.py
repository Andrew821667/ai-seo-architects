#!/usr/bin/env python3
"""
Комплексная проверка векторизации всех 14 агентов AI SEO Architects
Тестирует корректность FAISS индексов, русскоязычность контента и качество поиска
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Добавляем корневую директорию в path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from knowledge.knowledge_manager import knowledge_manager
from core.config import config

def test_agent_vectorization(agent_name: str, agent_level: str):
    """Комплексное тестирование векторизации агента"""
    print(f"\n🤖 Тестирование {agent_name} ({agent_level})")
    print("-" * 60)
    
    result = {
        'agent_name': agent_name,
        'agent_level': agent_level,
        'status': 'unknown',
        'documents_count': 0,
        'faiss_active': False,
        'russian_percentage': 0.0,
        'search_quality_score': 0.0,
        'issues': []
    }
    
    try:
        # Загружаем знания агента
        vector_store = knowledge_manager.load_agent_knowledge(agent_name, agent_level)
        
        if not vector_store:
            result['status'] = 'failed'
            result['issues'].append('Knowledge base not loaded')
            print("   ❌ База знаний не загружена")
            return result
        
        result['documents_count'] = len(vector_store.documents)
        result['faiss_active'] = vector_store.index is not None
        
        print(f"   📄 Документов загружено: {result['documents_count']}")
        print(f"   🔍 FAISS индекс: {'✅ Активен' if result['faiss_active'] else '❌ Неактивен'}")
        
        # Тестируем русскоязычность контента
        russian_queries = [
            "роль и ответственности агента",
            "основные задачи и функции", 
            "экспертные знания и навыки",
            "российский рынок SEO",
            "стратегия оптимизации"
        ]
        
        russian_hits = 0
        total_searches = len(russian_queries)
        search_scores = []
        
        for query in russian_queries:
            try:
                search_results = vector_store.similarity_search(query, k=2)
                
                if search_results:
                    # Проверяем русскоязычность результатов
                    content = search_results[0].page_content
                    has_cyrillic = any(ord(char) > 127 for char in content[:200])
                    
                    if has_cyrillic:
                        russian_hits += 1
                    
                    # Оценка качества поиска (простая метрика)
                    relevance_keywords = ['агент', 'SEO', 'оптимизация', 'стратегия', 'роль']
                    relevance_score = sum(1 for kw in relevance_keywords if kw.lower() in content.lower())
                    search_scores.append(relevance_score / len(relevance_keywords))
                    
            except Exception as e:
                result['issues'].append(f"Search error for '{query}': {str(e)}")
        
        result['russian_percentage'] = (russian_hits / total_searches) * 100
        result['search_quality_score'] = sum(search_scores) / len(search_scores) if search_scores else 0.0
        
        print(f"   🇷🇺 Русский контент: {result['russian_percentage']:.1f}%")
        print(f"   📊 Качество поиска: {result['search_quality_score']:.2f}/1.0")
        
        # Определяем общий статус
        if result['documents_count'] == 0:
            result['status'] = 'no_documents'
        elif not result['faiss_active']:
            result['status'] = 'no_faiss'
            result['issues'].append('FAISS index not active')
        elif result['russian_percentage'] < 50:
            result['status'] = 'low_russian'
            result['issues'].append('Low Russian content percentage')
        elif result['russian_percentage'] >= 80 and result['search_quality_score'] >= 0.3:
            result['status'] = 'excellent'
        elif result['russian_percentage'] >= 60 and result['search_quality_score'] >= 0.2:
            result['status'] = 'good'
        else:
            result['status'] = 'needs_improvement'
        
        status_icons = {
            'excellent': '🏆',
            'good': '✅', 
            'needs_improvement': '⚠️',
            'low_russian': '❌',
            'no_faiss': '🔧',
            'no_documents': '📁'
        }
        
        print(f"   {status_icons.get(result['status'], '❓')} Статус: {result['status']}")
        
        if result['issues']:
            print(f"   ⚠️ Проблемы: {', '.join(result['issues'])}")
        
    except Exception as e:
        result['status'] = 'error'
        result['issues'].append(str(e))
        print(f"   ❌ Критическая ошибка: {e}")
    
    return result

def test_search_cross_agent():
    """Тестирование межагентного поиска знаний"""
    print("\n🔄 Тестирование межагентного поиска знаний...")
    print("-" * 60)
    
    # Тестовые запросы для разных областей
    test_scenarios = [
        {
            'query': 'BANT методология квалификации лидов',
            'expected_agent': 'lead_qualification',
            'description': 'Квалификация лидов'
        },
        {
            'query': 'Core Web Vitals оптимизация',
            'expected_agent': 'technical_seo_auditor',
            'description': 'Технический аудит'
        },
        {
            'query': 'стратегия ценообразования предложений',
            'expected_agent': 'proposal_generation', 
            'description': 'Генерация предложений'
        },
        {
            'query': 'SPIN selling техники продаж',
            'expected_agent': 'sales_conversation',
            'description': 'Продажные разговоры'
        }
    ]
    
    cross_search_results = []
    
    for scenario in test_scenarios:
        try:
            # Ищем знания в целевом агенте
            context = knowledge_manager.get_knowledge_context(
                scenario['expected_agent'], 
                scenario['query'], 
                k=2
            )
            
            found_relevant = len(context) > 100 and any(
                keyword in context.lower() 
                for keyword in scenario['query'].lower().split()[:2]
            )
            
            cross_search_results.append({
                'scenario': scenario['description'],
                'agent': scenario['expected_agent'],
                'query': scenario['query'],
                'found_relevant': found_relevant,
                'context_length': len(context)
            })
            
            status = "✅" if found_relevant else "❌"
            print(f"   {status} {scenario['description']}: {scenario['expected_agent']}")
            
        except Exception as e:
            cross_search_results.append({
                'scenario': scenario['description'],
                'agent': scenario['expected_agent'], 
                'query': scenario['query'],
                'found_relevant': False,
                'error': str(e)
            })
            print(f"   ❌ {scenario['description']}: Ошибка - {e}")
    
    return cross_search_results

def main():
    """Основная функция комплексного тестирования"""
    print("🚀 КОМПЛЕКСНАЯ ПРОВЕРКА ВЕКТОРИЗАЦИИ ВСЕХ АГЕНТОВ")
    print("=" * 70)
    print(f"🕒 Время запуска: {datetime.now().isoformat()}")
    print(f"🔧 OpenAI Embeddings: {'✅ Активен' if knowledge_manager.embeddings else '❌ Неактивен'}")
    print(f"📁 Путь к знаниям: {config.KNOWLEDGE_BASE_PATH}")
    print(f"💾 Путь к векторам: {config.VECTOR_STORE_PATH}")
    
    if not knowledge_manager.embeddings:
        print("❌ OpenAI Embeddings не активен. Тестирование ограничено.")
        return
    
    # Словарь всех агентов
    all_agents = {
        # Executive level
        'chief_seo_strategist': 'executive',
        'business_development_director': 'executive',
        
        # Management level  
        'task_coordination': 'management',
        'sales_operations_manager': 'management',
        'technical_seo_operations_manager': 'management', 
        'client_success_manager': 'management',
        
        # Operational level
        'lead_qualification': 'operational',
        'sales_conversation': 'operational',
        'proposal_generation': 'operational',
        'technical_seo_auditor': 'operational',
        'content_strategy': 'operational',
        'link_building': 'operational',
        'competitive_analysis': 'operational',
        'reporting': 'operational'
    }
    
    print(f"🎯 Тестирование {len(all_agents)} агентов:")
    
    # Тестируем каждого агента
    all_results = []
    
    for agent_name, agent_level in all_agents.items():
        result = test_agent_vectorization(agent_name, agent_level)
        all_results.append(result)
    
    # Тестируем межагентный поиск
    cross_search_results = test_search_cross_agent()
    
    # Итоговая статистика
    print("\n" + "=" * 70)
    print("📊 ИТОГОВАЯ СТАТИСТИКА ВЕКТОРИЗАЦИИ")
    print("=" * 70)
    
    # Группируем результаты по статусу
    status_groups = {}
    for result in all_results:
        status = result['status']
        if status not in status_groups:
            status_groups[status] = []
        status_groups[status].append(result['agent_name'])
    
    print("\n📋 РЕЗУЛЬТАТЫ ПО СТАТУСАМ:")
    status_descriptions = {
        'excellent': '🏆 Отлично (90%+ русский, высокое качество)',
        'good': '✅ Хорошо (60%+ русский, нормальное качество)',
        'needs_improvement': '⚠️ Требует улучшения',
        'low_russian': '❌ Мало русского контента',
        'no_faiss': '🔧 FAISS не активен',
        'no_documents': '📁 Нет документов',
        'error': '💥 Критические ошибки'
    }
    
    for status, agents in status_groups.items():
        description = status_descriptions.get(status, f'❓ {status}')
        print(f"   {description}: {len(agents)} агентов")
        if len(agents) <= 5:  # Показываем имена если агентов немного
            for agent in agents:
                print(f"     • {agent}")
    
    # Статистика по уровням
    print(f"\n🎯 СТАТИСТИКА ПО УРОВНЯМ:")
    level_stats = {}
    for result in all_results:
        level = result['agent_level']
        if level not in level_stats:
            level_stats[level] = {'total': 0, 'excellent': 0, 'good': 0}
        level_stats[level]['total'] += 1
        if result['status'] in ['excellent', 'good']:
            level_stats[level][result['status']] += 1
    
    for level, stats in level_stats.items():
        success_rate = ((stats['excellent'] + stats['good']) / stats['total']) * 100
        print(f"   {level.capitalize()}: {stats['excellent']}🏆 + {stats['good']}✅ / {stats['total']} ({success_rate:.1f}%)")
    
    # Общие метрики
    total_agents = len(all_results)
    excellent_count = len(status_groups.get('excellent', []))
    good_count = len(status_groups.get('good', []))
    successful_agents = excellent_count + good_count
    
    total_documents = sum(r['documents_count'] for r in all_results)
    avg_russian_percentage = sum(r['russian_percentage'] for r in all_results) / total_agents
    faiss_active_count = sum(1 for r in all_results if r['faiss_active'])
    
    print(f"\n📈 ОБЩИЕ МЕТРИКИ:")
    print(f"   🎯 Успешных агентов: {successful_agents}/{total_agents} ({(successful_agents/total_agents)*100:.1f}%)")
    print(f"   📄 Всего документов: {total_documents}")
    print(f"   🇷🇺 Средняя русскоязычность: {avg_russian_percentage:.1f}%")
    print(f"   🔍 FAISS активен: {faiss_active_count}/{total_agents} агентов")
    
    # Результаты межагентного поиска
    cross_successful = sum(1 for r in cross_search_results if r.get('found_relevant', False))
    print(f"   🔄 Межагентный поиск: {cross_successful}/{len(cross_search_results)} сценариев")
    
    # Финальная оценка
    print(f"\n🏆 ИТОГОВАЯ ОЦЕНКА:")
    if successful_agents >= total_agents * 0.9 and faiss_active_count >= total_agents * 0.9:
        print("   🎉 ПРЕВОСХОДНО! Все системы работают отлично")
        grade = "A+"
    elif successful_agents >= total_agents * 0.8 and faiss_active_count >= total_agents * 0.8:
        print("   ✅ ОТЛИЧНО! Система готова к использованию")
        grade = "A"
    elif successful_agents >= total_agents * 0.6 and faiss_active_count >= total_agents * 0.6:
        print("   ⚠️ ХОРОШО! Есть небольшие проблемы для устранения")
        grade = "B"
    else:
        print("   ❌ ТРЕБУЕТСЯ РАБОТА! Есть критические проблемы")
        grade = "C"
    
    print(f"   📊 Оценка системы: {grade}")
    
    # Рекомендации
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    if 'low_russian' in status_groups:
        print("   • Обновить базы знаний с низким процентом русского контента")
    if 'no_faiss' in status_groups:
        print("   • Исправить проблемы с FAISS индексацией")
    if cross_successful < len(cross_search_results):
        print("   • Проверить качество межагентного поиска")
    if grade in ['B', 'C']:
        print("   • Провести детальную диагностику проблемных агентов")
    else:
        print("   • Система готова к production использованию!")
    
    print(f"\n🕒 Тестирование завершено: {datetime.now().isoformat()}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()