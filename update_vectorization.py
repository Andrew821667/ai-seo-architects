#!/usr/bin/env python3
"""
Скрипт для обновления векторизации всех агентов с русскоязычными базами знаний
Принудительно пересоздает FAISS индексы для всех 14 агентов
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Добавляем корневую директорию в path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from knowledge.knowledge_manager import knowledge_manager
from core.config import config

def clear_old_vectors():
    """Очистка старых векторных индексов"""
    print("🗑️ Очистка старых векторных индексов...")
    
    vector_store_path = Path(config.VECTOR_STORE_PATH)
    
    if vector_store_path.exists():
        try:
            # Создаем бэкап
            backup_path = f"{vector_store_path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copytree(vector_store_path, backup_path)
            print(f"📦 Создан бэкап в {backup_path}")
            
            # Удаляем старые индексы
            shutil.rmtree(vector_store_path)
            os.makedirs(vector_store_path, exist_ok=True)
            print("✅ Старые индексы удалены")
            
        except Exception as e:
            print(f"⚠️ Ошибка очистки индексов: {e}")
    else:
        os.makedirs(vector_store_path, exist_ok=True)
        print("📁 Создана директория для векторов")

def force_reload_agent_knowledge(agent_name: str, agent_level: str):
    """Принудительная перезагрузка знаний агента"""
    print(f"\n🤖 Обновление векторизации для {agent_name} ({agent_level})...")
    
    try:
        # Удаляем из кэша если есть
        if agent_name in knowledge_manager.vector_stores:
            del knowledge_manager.vector_stores[agent_name]
        
        # Принудительно загружаем заново
        vector_store = knowledge_manager.load_agent_knowledge(agent_name, agent_level)
        
        if vector_store:
            print(f"   ✅ Успешно обновлено: {len(vector_store.documents)} документов")
            
            # Тестируем поиск
            test_results = vector_store.similarity_search(f"{agent_name} роль", k=1)
            if test_results:
                content_preview = test_results[0].page_content[:100]
                is_russian = any(ord(char) > 127 for char in content_preview)
                language_status = "🇷🇺 Русский" if is_russian else "🇺🇸 Английский"
                print(f"   🔍 Тест поиска: {language_status}")
                print(f"   📄 Превью: {content_preview}...")
            else:
                print(f"   ⚠️ Поиск не вернул результатов")
                
            return True
        else:
            print(f"   ❌ Не удалось загрузить знания")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка обновления {agent_name}: {e}")
        return False

def update_all_agents():
    """Обновление векторизации всех агентов"""
    print("🔄 Принудительное обновление векторизации всех агентов...")
    
    # Словарь соответствия агентов и их уровней
    agent_mappings = {
        # Executive level
        'chief_seo_strategist': 'executive',
        'business_development_director': 'executive',
        
        # Management level  
        'task_coordination': 'management',
        'sales_operations_manager': 'management',
        'technical_seo_operations_manager': 'management', 
        'client_success_manager': 'management',
        
        # Operational level - приоритет обновленным русскоязычным базам
        'lead_qualification': 'operational',
        'sales_conversation': 'operational',
        'proposal_generation': 'operational',
        'technical_seo_auditor': 'operational',
        'content_strategy': 'operational',
        'link_building': 'operational',
        'competitive_analysis': 'operational',
        'reporting': 'operational'
    }
    
    results = {}
    successful_count = 0
    
    for agent_name, agent_level in agent_mappings.items():
        result = force_reload_agent_knowledge(agent_name, agent_level)
        results[agent_name] = result
        if result:
            successful_count += 1
    
    return results, successful_count

def verify_vectorization():
    """Проверка корректности векторизации"""
    print("\n🔍 Верификация обновленной векторизации...")
    
    # Критически важные агенты с обновленными русскоязычными базами
    critical_agents = [
        ('lead_qualification', 'operational'),
        ('sales_conversation', 'operational'),  
        ('proposal_generation', 'operational'),
        ('technical_seo_auditor', 'operational'),
        ('technical_seo_operations_manager', 'management')
    ]
    
    verification_results = {}
    
    for agent_name, agent_level in critical_agents:
        print(f"\n🧪 Проверка {agent_name}...")
        
        try:
            # Загружаем знания
            vector_store = knowledge_manager.load_agent_knowledge(agent_name, agent_level)
            
            if vector_store and vector_store.documents:
                # Тестируем русскоязычный поиск
                russian_queries = [
                    "роль и ответственности",
                    "экспертные знания",
                    "российский рынок",
                    "SEO оптимизация"
                ]
                
                russian_results = 0
                total_tests = len(russian_queries)
                
                for query in russian_queries:
                    results = vector_store.similarity_search(query, k=1)
                    if results:
                        content = results[0].page_content
                        # Проверяем наличие русских символов
                        if any(ord(char) > 127 for char in content):
                            russian_results += 1
                
                russian_percentage = (russian_results / total_tests) * 100
                verification_results[agent_name] = {
                    'status': 'success',
                    'documents_count': len(vector_store.documents),
                    'russian_content_percentage': russian_percentage,
                    'faiss_active': vector_store.index is not None
                }
                
                status = "✅" if russian_percentage >= 75 else "⚠️" if russian_percentage >= 50 else "❌"
                print(f"   {status} Русский контент: {russian_percentage:.1f}%")
                print(f"   📄 Документов: {len(vector_store.documents)}")
                print(f"   🔍 FAISS: {'Активен' if vector_store.index else 'Fallback'}")
                
            else:
                verification_results[agent_name] = {
                    'status': 'failed',
                    'reason': 'No documents loaded'
                }
                print(f"   ❌ Документы не загружены")
                
        except Exception as e:
            verification_results[agent_name] = {
                'status': 'error', 
                'error': str(e)
            }
            print(f"   ❌ Ошибка: {e}")
    
    return verification_results

def main():
    """Основная функция обновления векторизации"""
    print("🚀 ОБНОВЛЕНИЕ ВЕКТОРИЗАЦИИ AI SEO ARCHITECTS")
    print("=" * 70)
    print(f"🕒 Время запуска: {datetime.now().isoformat()}")
    print(f"🔧 OpenAI Embeddings: {'✅ Готов' if knowledge_manager.embeddings else '❌ Недоступен'}")
    print(f"📁 Путь к знаниям: {config.KNOWLEDGE_BASE_PATH}")
    print(f"💾 Путь к векторам: {config.VECTOR_STORE_PATH}")
    
    if not knowledge_manager.embeddings:
        print("❌ OpenAI Embeddings не инициализированы. Проверьте OPENAI_API_KEY")
        return
    
    try:
        # Этап 1: Очистка старых индексов
        clear_old_vectors()
        
        # Этап 2: Обновление векторизации всех агентов
        results, successful_count = update_all_agents()
        
        # Этап 3: Верификация критически важных агентов
        verification_results = verify_vectorization()
        
        # Этап 4: Финальный отчет
        print("\n" + "=" * 70)
        print("📊 ИТОГОВЫЙ ОТЧЕТ ОБНОВЛЕНИЯ ВЕКТОРИЗАЦИИ")
        print("=" * 70)
        
        print(f"\n🔄 ОБНОВЛЕНИЕ АГЕНТОВ:")
        for agent_name, success in results.items():
            status = "✅" if success else "❌"
            print(f"   {status} {agent_name}")
        
        print(f"\n🧪 ВЕРИФИКАЦИЯ КРИТИЧЕСКИХ АГЕНТОВ:")
        for agent_name, result in verification_results.items():
            if result['status'] == 'success':
                percentage = result['russian_content_percentage']
                status = "✅" if percentage >= 75 else "⚠️" if percentage >= 50 else "❌"
                print(f"   {status} {agent_name}: {percentage:.1f}% русский контент")
            else:
                print(f"   ❌ {agent_name}: {result.get('reason', result.get('error', 'Неизвестная ошибка'))}")
        
        print(f"\n🏆 ОБЩИЙ РЕЗУЛЬТАТ:")
        print(f"   📊 Агентов обновлено: {successful_count}/{len(results)}")
        
        verified_count = sum(1 for r in verification_results.values() 
                           if r.get('status') == 'success' and r.get('russian_content_percentage', 0) >= 75)
        print(f"   ✅ Верифицировано (>75% RU): {verified_count}/{len(verification_results)}")
        
        if successful_count == len(results) and verified_count >= len(verification_results) * 0.8:
            print("\n🎉 ВЕКТОРИЗАЦИЯ УСПЕШНО ОБНОВЛЕНА!")
            print("   Все агенты готовы к работе с русскоязычными базами знаний")
        elif successful_count >= len(results) * 0.8:
            print("\n⚠️ ЧАСТИЧНО ГОТОВО")
            print("   Большинство агентов обновлено, но есть проблемы с некоторыми")
        else:
            print("\n❌ КРИТИЧЕСКИЕ ПРОБЛЕМЫ")
            print("   Требуется дополнительная диагностика")
        
        print(f"\n💡 РЕКОМЕНДАЦИИ:")
        if verified_count < len(verification_results):
            print("   • Проверьте корректность русскоязычных баз знаний")
            print("   • Убедитесь что файлы содержат русский текст")
        
        print(f"\n🕒 Обновление завершено: {datetime.now().isoformat()}")
        
    except KeyboardInterrupt:
        print("\n👋 Обновление прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()