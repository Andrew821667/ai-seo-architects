#!/usr/bin/env python3
"""
Интеграционное тестирование агентов с русскоязычными базами знаний
Тестирует работу всех 14 агентов после обновления векторизации
"""

import os
import sys
import time
from datetime import datetime
from typing import Dict, Any, List

# Добавляем корневую директорию в path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mock_data_provider import MockDataProvider
from knowledge.knowledge_manager import knowledge_manager

# Импортируем всех агентов
from agents.executive.chief_seo_strategist import ChiefSEOStrategistAgent
from agents.executive.business_development_director import BusinessDevelopmentDirectorAgent
from agents.management.task_coordination import TaskCoordinationAgent
from agents.management.sales_operations_manager import SalesOperationsManagerAgent
from agents.management.technical_seo_operations_manager import TechnicalSEOOperationsManagerAgent
from agents.management.client_success_manager import ClientSuccessManagerAgent
from agents.operational.lead_qualification import LeadQualificationAgent
from agents.operational.sales_conversation import SalesConversationAgent
from agents.operational.proposal_generation import ProposalGenerationAgent
from agents.operational.technical_seo_auditor import TechnicalSEOAuditorAgent
from agents.operational.content_strategy import ContentStrategyAgent
from agents.operational.link_building import LinkBuildingAgent
from agents.operational.competitive_analysis import CompetitiveAnalysisAgent
from agents.operational.reporting import ReportingAgent


class RussianAgentsTester:
    """Класс для тестирования русскоязычных агентов"""
    
    def __init__(self):
        self.results = {}
        self.mock_provider = MockDataProvider()
        self.agents = {}
        self.test_queries = {
            'russian_general': [
                "Какие основные роли и ответственности у агента?",
                "Опишите экспертные компетенции в SEO",
                "Расскажите о стратегиях работы с российским рынком"
            ],
            'agent_specific': {}
        }
        
        # Специфичные запросы для каждого типа агента
        self.test_queries['agent_specific'] = {
            'lead_qualification': [
                "Как применять BANT методологию для квалификации лидов?",
                "Расскажите о machine learning в scoring лидов",
                "Какие техники conversation intelligence используются?"
            ],
            'sales_conversation': [
                "Опишите SPIN selling методологию",
                "Как работать с возражениями клиентов?", 
                "Какие техники эмоционального интеллекта применяются?"
            ],
            'proposal_generation': [
                "Как формировать value-based pricing стратегии?",
                "Расскажите о ROI моделировании в предложениях",
                "Какие persuasive writing техники эффективны?"
            ],
            'technical_seo_auditor': [
                "Опишите процесс аудита Core Web Vitals",
                "Как оптимизировать краулинг и индексацию?",
                "Какие современные веб-стандарты важны для SEO?"
            ],
            'technical_seo_operations_manager': [
                "Как управлять командой технических SEO специалистов?",
                "Опишите процессы мониторинга производительности",
                "Какие KPI важны для технического SEO?"
            ]
        }
    
    def initialize_agents(self) -> bool:
        """Инициализация всех агентов с правильными параметрами"""
        print("🤖 Инициализация агентов с русскоязычными базами знаний...")
        
        agent_configs = {
            # Executive level
            'chief_seo_strategist': {
                'class': ChiefSEOStrategistAgent,
                'level': 'executive'
            },
            'business_development_director': {
                'class': BusinessDevelopmentDirectorAgent,
                'level': 'executive'
            },
            
            # Management level
            'task_coordination': {
                'class': TaskCoordinationAgent,
                'level': 'management'
            },
            'sales_operations_manager': {
                'class': SalesOperationsManagerAgent,
                'level': 'management'
            },
            'technical_seo_operations_manager': {
                'class': TechnicalSEOOperationsManagerAgent,
                'level': 'management'
            },
            'client_success_manager': {
                'class': ClientSuccessManagerAgent,
                'level': 'management'
            },
            
            # Operational level
            'lead_qualification': {
                'class': LeadQualificationAgent,
                'level': 'operational'
            },
            'sales_conversation': {
                'class': SalesConversationAgent,
                'level': 'operational'
            },
            'proposal_generation': {
                'class': ProposalGenerationAgent,
                'level': 'operational'
            },
            'technical_seo_auditor': {
                'class': TechnicalSEOAuditorAgent,
                'level': 'operational'
            },
            'content_strategy': {
                'class': ContentStrategyAgent,
                'level': 'operational'
            },
            'link_building': {
                'class': LinkBuildingAgent,
                'level': 'operational'
            },
            'competitive_analysis': {
                'class': CompetitiveAnalysisAgent,
                'level': 'operational'
            },
            'reporting': {
                'class': ReportingAgent,
                'level': 'operational'
            }
        }
        
        successful_init = 0
        
        for agent_name, config in agent_configs.items():
            try:
                # Создаем агента с правильными параметрами
                agent = config['class'](
                    data_provider=self.mock_provider,
                    agent_level=config['level'],  # Добавляем обязательный параметр
                    rag_enabled=True
                )
                
                self.agents[agent_name] = agent
                print(f"   ✅ {agent_name} ({config['level']})")
                successful_init += 1
                
            except Exception as e:
                print(f"   ❌ {agent_name}: {e}")
                self.results[agent_name] = {
                    'status': 'initialization_failed',
                    'error': str(e)
                }
        
        print(f"\n📊 Инициализировано агентов: {successful_init}/{len(agent_configs)}")
        return successful_init > 0
    
    def test_agent_knowledge_access(self, agent_name: str) -> Dict[str, Any]:
        """Тестирование доступа к знаниям агента"""
        if agent_name not in self.agents:
            return {'status': 'not_initialized'}
        
        agent = self.agents[agent_name]
        result = {
            'agent_name': agent_name,
            'knowledge_loaded': False,
            'russian_content': False,
            'search_results': [],
            'response_quality': 0.0
        }
        
        try:
            # Проверяем доступ к знаниям через knowledge_manager
            if hasattr(agent, 'agent_level'):
                knowledge_context = knowledge_manager.get_knowledge_context(
                    agent_name, 
                    "роль и ответственности агента", 
                    k=2
                )
                
                if knowledge_context:
                    result['knowledge_loaded'] = True
                    result['russian_content'] = any(ord(char) > 127 for char in knowledge_context[:500])
                    result['context_length'] = len(knowledge_context)
                    
                    # Тестируем специфичные запросы если есть
                    if agent_name in self.test_queries['agent_specific']:
                        for query in self.test_queries['agent_specific'][agent_name][:2]:
                            context = knowledge_manager.get_knowledge_context(agent_name, query, k=1)
                            if context:
                                result['search_results'].append({
                                    'query': query,
                                    'found': True,
                                    'length': len(context),
                                    'has_russian': any(ord(char) > 127 for char in context[:200])
                                })
                
        except Exception as e:
            result['error'] = str(e)
        
        # Вычисляем общий рейтинг качества
        quality_score = 0.0
        if result['knowledge_loaded']:
            quality_score += 0.4
        if result['russian_content']:
            quality_score += 0.4
        if result['search_results']:
            search_success_rate = sum(1 for r in result['search_results'] if r['found']) / len(result['search_results'])
            quality_score += 0.2 * search_success_rate
        
        result['response_quality'] = quality_score
        
        return result
    
    def test_agent_task_processing(self, agent_name: str) -> Dict[str, Any]:
        """Тестирование обработки задач агентом"""
        if agent_name not in self.agents:
            return {'status': 'not_initialized'}
        
        agent = self.agents[agent_name]
        result = {
            'agent_name': agent_name,
            'task_processed': False,
            'response_length': 0,
            'russian_response': False,
            'processing_time': 0.0,
            'error': None
        }
        
        # Тестовые задачи для разных агентов
        test_tasks = {
            'lead_qualification': {
                'task': 'analyze_lead',
                'data': {
                    'company': 'ООО Российский Бизнес',
                    'industry': 'E-commerce',
                    'revenue': '50M RUB',
                    'employees': '50-100',
                    'contact': 'Директор по маркетингу',
                    'inquiry': 'Нужна помощь с SEO продвижением интернет-магазина'
                }
            },
            'technical_seo_auditor': {
                'task': 'technical_audit',
                'data': {
                    'domain': 'example-shop.ru',
                    'audit_scope': 'comprehensive',
                    'focus_areas': ['Core Web Vitals', 'crawling', 'indexing', 'mobile']
                }
            },
            'sales_conversation': {
                'task': 'conversation_analysis',
                'data': {
                    'client_type': 'enterprise',
                    'stage': 'needs_assessment',
                    'concerns': ['budget', 'timeline', 'ROI'],
                    'industry': 'финтех'
                }
            },
            'proposal_generation': {
                'task': 'generate_proposal',
                'data': {
                    'client': 'Банк России',
                    'services': ['Technical SEO', 'Content Strategy'],
                    'budget': '2M RUB',
                    'timeline': '6 months'
                }
            }
        }
        
        # Используем общую задачу если нет специфичной
        task_data = test_tasks.get(agent_name, {
            'task': 'analyze',
            'data': {'query': 'Проанализируйте текущую ситуацию с SEO'}
        })
        
        try:
            start_time = time.time()
            
            # Обрабатываем задачу
            if hasattr(agent, 'process_task'):
                response = agent.process_task(task_data)
                
                if response:
                    result['task_processed'] = True
                    response_text = str(response)
                    result['response_length'] = len(response_text)
                    result['russian_response'] = any(ord(char) > 127 for char in response_text[:500])
            
            result['processing_time'] = time.time() - start_time
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Запуск комплексного тестирования"""
        print("🚀 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ РУССКОЯЗЫЧНЫХ АГЕНТОВ")
        print("=" * 70)
        print(f"🕒 Время запуска: {datetime.now().isoformat()}")
        
        comprehensive_results = {
            'timestamp': datetime.now().isoformat(),
            'total_agents': 0,
            'initialized_agents': 0,
            'agents_with_knowledge': 0,
            'agents_with_russian': 0,
            'agents_processing_tasks': 0,
            'detailed_results': {},
            'summary': {}
        }
        
        # Этап 1: Инициализация агентов
        print("\n🔧 ЭТАП 1: Инициализация агентов")
        print("-" * 50)
        
        if not self.initialize_agents():
            print("❌ Критическая ошибка: агенты не инициализированы")
            return comprehensive_results
        
        comprehensive_results['total_agents'] = len(self.agents)
        comprehensive_results['initialized_agents'] = len(self.agents)
        
        # Этап 2: Тестирование доступа к знаниям
        print("\n📚 ЭТАП 2: Тестирование доступа к русскоязычным знаниям")
        print("-" * 50)
        
        knowledge_results = {}
        
        for agent_name in self.agents.keys():
            print(f"🧪 Тестирование знаний {agent_name}...")
            
            knowledge_result = self.test_agent_knowledge_access(agent_name)
            knowledge_results[agent_name] = knowledge_result
            
            # Обновляем статистику
            if knowledge_result.get('knowledge_loaded', False):
                comprehensive_results['agents_with_knowledge'] += 1
            
            if knowledge_result.get('russian_content', False):
                comprehensive_results['agents_with_russian'] += 1
            
            # Выводим результат
            quality = knowledge_result.get('response_quality', 0.0)
            if quality >= 0.8:
                status = "🏆 Отлично"
            elif quality >= 0.6:
                status = "✅ Хорошо"
            elif quality >= 0.4:
                status = "⚠️ Удовл."
            else:
                status = "❌ Плохо"
            
            print(f"   {status} Качество: {quality:.2f}")
        
        # Этап 3: Тестирование обработки задач
        print("\n⚙️ ЭТАП 3: Тестирование обработки задач")
        print("-" * 50)
        
        task_results = {}
        
        for agent_name in list(self.agents.keys())[:5]:  # Тестируем первые 5 агентов для демо
            print(f"🎯 Тестирование обработки задач {agent_name}...")
            
            task_result = self.test_agent_task_processing(agent_name)
            task_results[agent_name] = task_result
            
            if task_result.get('task_processed', False):
                comprehensive_results['agents_processing_tasks'] += 1
            
            # Выводим результат
            if task_result.get('task_processed'):
                processing_time = task_result.get('processing_time', 0)
                russian_resp = "🇷🇺" if task_result.get('russian_response') else "🇺🇸"
                print(f"   ✅ Обработано за {processing_time:.2f}с {russian_resp}")
            else:
                error = task_result.get('error', 'Неизвестная ошибка')
                print(f"   ❌ Ошибка: {error}")
        
        # Сохраняем детальные результаты
        comprehensive_results['detailed_results'] = {
            'knowledge_tests': knowledge_results,
            'task_tests': task_results
        }
        
        # Этап 4: Итоговый анализ
        print("\n📊 ЭТАП 4: Итоговый анализ")
        print("=" * 70)
        
        total = comprehensive_results['total_agents']
        init_success = (comprehensive_results['initialized_agents'] / total) * 100
        knowledge_success = (comprehensive_results['agents_with_knowledge'] / total) * 100
        russian_success = (comprehensive_results['agents_with_russian'] / total) * 100
        
        print(f"📈 СТАТИСТИКА ГОТОВНОСТИ:")
        print(f"   🤖 Инициализировано агентов: {comprehensive_results['initialized_agents']}/{total} ({init_success:.1f}%)")
        print(f"   📚 Агентов с знаниями: {comprehensive_results['agents_with_knowledge']}/{total} ({knowledge_success:.1f}%)")
        print(f"   🇷🇺 Русскоязычных агентов: {comprehensive_results['agents_with_russian']}/{total} ({russian_success:.1f}%)")
        print(f"   ⚙️ Обрабатывающих задачи: {comprehensive_results['agents_processing_tasks']}/{len(task_results)} (демо)")
        
        # Итоговая оценка
        overall_score = (init_success + knowledge_success + russian_success) / 3
        
        if overall_score >= 90:
            grade = "A+"
            status = "🎉 ПРЕВОСХОДНО!"
            message = "Система полностью готова к production"
        elif overall_score >= 80:
            grade = "A"
            status = "✅ ОТЛИЧНО!"
            message = "Система готова к использованию"
        elif overall_score >= 70:
            grade = "B"
            status = "⚠️ ХОРОШО"
            message = "Есть небольшие проблемы для устранения"
        else:
            grade = "C"
            status = "❌ ТРЕБУЕТСЯ РАБОТА"
            message = "Есть критические проблемы"
        
        print(f"\n🏆 ИТОГОВАЯ ОЦЕНКА:")
        print(f"   {status} Оценка: {grade} ({overall_score:.1f}%)")
        print(f"   💬 {message}")
        
        comprehensive_results['summary'] = {
            'overall_score': overall_score,
            'grade': grade,
            'status': status,
            'message': message
        }
        
        print(f"\n🕒 Тестирование завершено: {datetime.now().isoformat()}")
        
        return comprehensive_results

def main():
    """Основная функция тестирования"""
    try:
        tester = RussianAgentsTester()
        results = tester.run_comprehensive_test()
        
        # Возвращаем успешный код если всё хорошо
        if results['summary']['overall_score'] >= 80:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n👋 Тестирование прервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()