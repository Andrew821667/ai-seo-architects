#!/usr/bin/env python3
"""
Тест интеграции FAISS с OpenAI Embeddings для AI SEO Architects
Проверяет корректность работы векторизации знаний агентов
"""

import os
import sys
from pathlib import Path

# Добавляем корневую директорию в path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from knowledge.knowledge_manager import knowledge_manager, FAISSVectorStore
from langchain.schema import Document
from core.config import config
from datetime import datetime


def test_openai_embeddings():
    """Тест инициализации OpenAI Embeddings"""
    print("🧪 Тестирование инициализации OpenAI Embeddings...")
    
    if knowledge_manager.embeddings is not None:
        print("✅ OpenAI Embeddings успешно инициализированы")
        print(f"   Модель: text-embedding-ada-002")
        print(f"   API Key: {'sk-proj-' + '***' + config.OPENAI_API_KEY[-10:] if config.OPENAI_API_KEY else 'Не найден'}")
        return True
    else:
        print("❌ OpenAI Embeddings не инициализированы")
        return False


def test_faiss_vector_store():
    """Тест создания и работы FAISSVectorStore"""
    print("\n🧪 Тестирование FAISSVectorStore...")
    
    # Создаем тестовые документы
    test_documents = [
        Document(
            page_content="SEO оптимизация включает техническое SEO, контентную стратегию и линкбилдинг",
            metadata={"source": "test1.md", "agent": "test", "chunk_id": 0}
        ),
        Document(
            page_content="Lead qualification использует BANT и MEDDIC методологии для оценки клиентов",
            metadata={"source": "test2.md", "agent": "test", "chunk_id": 1}
        ),
        Document(
            page_content="Technical SEO аудит проверяет Core Web Vitals, crawling и индексацию страниц",
            metadata={"source": "test3.md", "agent": "test", "chunk_id": 2}
        )
    ]
    
    try:
        # Создаем FAISSVectorStore с embeddings
        if knowledge_manager.embeddings:
            vector_store = FAISSVectorStore(test_documents, knowledge_manager.embeddings)
        else:
            vector_store = FAISSVectorStore(test_documents, None)
        
        print("✅ FAISSVectorStore создан успешно")
        print(f"   Документов: {len(vector_store.documents)}")
        print(f"   FAISS индекс: {'Создан' if vector_store.index is not None else 'Fallback'}")
        
        # Тестируем поиск
        search_results = vector_store.similarity_search("SEO аудит", k=2)
        print(f"   Поиск 'SEO аудит': найдено {len(search_results)} документов")
        
        if search_results:
            print(f"   Первый результат: {search_results[0].page_content[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания FAISSVectorStore: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_knowledge_loading():
    """Тест загрузки знаний агентов с FAISS"""
    print("\n🧪 Тестирование загрузки знаний агентов...")
    
    test_agents = [
        ("lead_qualification", "operational"),
        ("technical_seo_auditor", "operational"), 
        ("chief_seo_strategist", "executive")
    ]
    
    results = {}
    
    for agent_name, agent_level in test_agents:
        try:
            print(f"\n🤖 Загрузка знаний для {agent_name}...")
            
            vector_store = knowledge_manager.load_agent_knowledge(agent_name, agent_level)
            
            if vector_store:
                results[agent_name] = {
                    'status': 'success',
                    'documents_count': len(vector_store.documents),
                    'faiss_index': vector_store.index is not None,
                    'embeddings_available': knowledge_manager.embeddings is not None
                }
                
                # Тестируем поиск по знаниям
                if vector_store.documents:
                    search_results = vector_store.similarity_search(f"{agent_name} tasks", k=1)
                    results[agent_name]['search_works'] = len(search_results) > 0
                    
                    if search_results:
                        print(f"   📄 Пример знаний: {search_results[0].page_content[:100]}...")
                
                print(f"   ✅ Успешно загружено: {len(vector_store.documents)} документов")
                print(f"   🔍 FAISS индекс: {'Активен' if vector_store.index else 'Fallback'}")
                
            else:
                results[agent_name] = {'status': 'failed', 'reason': 'No knowledge found'}
                print(f"   ❌ Знания не найдены")
                
        except Exception as e:
            results[agent_name] = {'status': 'error', 'error': str(e)}
            print(f"   ❌ Ошибка загрузки: {e}")
    
    return results


def test_vector_search_quality():
    """Тест качества векторного поиска"""
    print("\n🧪 Тестирование качества векторного поиска...")
    
    if not knowledge_manager.embeddings:
        print("⚠️ OpenAI Embeddings недоступны, пропускаем тест качества")
        return False
    
    # Загружаем знания для technical_seo_auditor
    vector_store = knowledge_manager.load_agent_knowledge("technical_seo_auditor", "operational")
    
    if not vector_store or not vector_store.documents:
        print("❌ Не удалось загрузить знания для тестирования")
        return False
    
    test_queries = [
        "Core Web Vitals",
        "crawling problems",
        "technical SEO audit",
        "page speed optimization",
        "structured data"
    ]
    
    print("🔍 Тестирование поисковых запросов:")
    
    for query in test_queries:
        try:
            # FAISS поиск
            faiss_results = vector_store._faiss_search(query, k=3)
            
            # Простой поиск для сравнения
            simple_results = vector_store._simple_search(query, k=3)
            
            print(f"\n   Query: '{query}'")
            print(f"   FAISS результатов: {len(faiss_results)}")
            print(f"   Simple результатов: {len(simple_results)}")
            
            if faiss_results:
                print(f"   FAISS топ-результат: {faiss_results[0].page_content[:80]}...")
                
        except Exception as e:
            print(f"   ❌ Ошибка поиска для '{query}': {e}")
    
    return True


def test_index_persistence():
    """Тест сохранения и загрузки FAISS индексов"""
    print("\n🧪 Тестирование персистентности индексов...")
    
    if not knowledge_manager.embeddings:
        print("⚠️ OpenAI Embeddings недоступны, пропускаем тест персистентности")
        return False
    
    try:
        # Загружаем знания агента
        agent_name = "lead_qualification"
        vector_store = knowledge_manager.load_agent_knowledge(agent_name, "operational")
        
        if not vector_store:
            print("❌ Не удалось загрузить знания агента")
            return False
        
        # Проверяем существование сохраненного индекса
        index_path = f"{config.VECTOR_STORE_PATH}/{agent_name}"
        faiss_index_file = f"{index_path}/faiss.index"
        metadata_file = f"{index_path}/metadata.pkl"
        
        index_exists = os.path.exists(faiss_index_file)
        metadata_exists = os.path.exists(metadata_file)
        
        print(f"   📦 Индекс файл существует: {index_exists}")
        print(f"   📋 Метаданные существуют: {metadata_exists}")
        
        if index_exists and metadata_exists:
            print("   ✅ Индекс успешно сохранен на диск")
            
            # Тестируем загрузку
            new_vector_store = FAISSVectorStore([], knowledge_manager.embeddings)
            load_success = new_vector_store.load_index(index_path)
            
            if load_success:
                print("   ✅ Индекс успешно загружен с диска")
                print(f"   📄 Загружено документов: {len(new_vector_store.documents)}")
                return True
            else:
                print("   ❌ Ошибка загрузки индекса")
                return False
        else:
            print("   ⚠️ Индекс не сохранен (возможно, используется fallback)")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка тестирования персистентности: {e}")
        return False


def main():
    """Основная функция тестирования FAISS интеграции"""
    print("🚀 ТЕСТИРОВАНИЕ FAISS + OPENAI EMBEDDINGS ИНТЕГРАЦИИ")
    print("=" * 70)
    print(f"🕒 Время запуска: {datetime.now().isoformat()}")
    print(f"🔧 OPENAI_API_KEY: {'Установлен' if config.OPENAI_API_KEY else 'Не найден'}")
    print(f"📁 Путь к знаниям: {config.KNOWLEDGE_BASE_PATH}")
    print(f"💾 Путь к векторам: {config.VECTOR_STORE_PATH}")
    
    test_results = {}
    
    # Тест 1: OpenAI Embeddings
    test_results['embeddings'] = test_openai_embeddings()
    
    # Тест 2: FAISS Vector Store
    test_results['faiss_store'] = test_faiss_vector_store()
    
    # Тест 3: Загрузка знаний агентов
    test_results['agent_loading'] = test_agent_knowledge_loading()
    
    # Тест 4: Качество поиска
    test_results['search_quality'] = test_vector_search_quality()
    
    # Тест 5: Персистентность индексов
    test_results['persistence'] = test_index_persistence()
    
    # Итоговый отчет
    print("\n" + "=" * 70)
    print("📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        if isinstance(result, bool):
            status = "✅ PASSED" if result else "❌ FAILED"
            if result:
                passed_tests += 1
        elif isinstance(result, dict):
            # Для теста agent_loading
            successful_agents = sum(1 for r in result.values() if r.get('status') == 'success')
            total_agents = len(result)
            status = f"✅ PASSED ({successful_agents}/{total_agents} агентов)"
            if successful_agents > 0:
                passed_tests += 1
        else:
            status = "❓ UNKNOWN"
        
        print(f"   {test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\n🏆 ОБЩИЙ РЕЗУЛЬТАТ: {passed_tests}/{total_tests} тестов пройдено")
    
    if passed_tests == total_tests:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! FAISS интеграция работает корректно")
    elif passed_tests > 0:
        print("⚠️  Частичная готовность. Некоторые функции могут работать в fallback режиме")
    else:
        print("❌ КРИТИЧЕСКИЕ ПРОБЛЕМЫ. Требуется диагностика")
    
    # Рекомендации
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    if not test_results.get('embeddings'):
        print("   • Проверьте корректность OPENAI_API_KEY")
        print("   • Убедитесь в наличии интернет соединения")
    
    if not test_results.get('persistence'):
        print("   • Проверьте права доступа к директории vector stores")
    
    print(f"\n🕒 Тестирование завершено: {datetime.now().isoformat()}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка тестирования: {e}")
        import traceback
        traceback.print_exc()