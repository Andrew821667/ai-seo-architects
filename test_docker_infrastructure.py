#!/usr/bin/env python3
"""
Тестирование полной Docker инфраструктуры AI SEO Architects
Проверяет PostgreSQL, Redis, Nginx, FastAPI, Prometheus, Grafana
"""

import asyncio
import aiohttp
import asyncpg
import redis.asyncio as redis
import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, Any

# Добавляем корневую директорию в PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class InfrastructureTester:
    """Класс для тестирования Docker инфраструктуры"""
    
    def __init__(self):
        self.results = {}
        self.base_url = "http://localhost"
        self.api_url = f"{self.base_url}:8000"
        
        # Connection strings
        self.postgres_url = "postgresql://ai_seo_user:secure_password_change_me@localhost:5432/ai_seo_architects"
        self.redis_url = "redis://localhost:6379/0"
        
    async def test_postgresql(self) -> Dict[str, Any]:
        """Тестирование PostgreSQL подключения и схемы"""
        print("\n🗄️ Тестирование PostgreSQL...")
        
        result = {
            'service': 'postgresql',
            'status': 'unknown',
            'connection': False,
            'schema_exists': False,
            'tables_count': 0,
            'agents_count': 0,
            'error': None
        }
        
        try:
            # Подключение к PostgreSQL
            conn = await asyncpg.connect(self.postgres_url)
            result['connection'] = True
            
            # Проверяем существование схемы ai_seo
            schema_exists = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = 'ai_seo')"
            )
            result['schema_exists'] = schema_exists
            
            if schema_exists:
                # Считаем таблицы в схеме ai_seo
                tables_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'ai_seo'"
                )
                result['tables_count'] = tables_count
                
                # Считаем агентов
                try:
                    agents_count = await conn.fetchval("SELECT COUNT(*) FROM ai_seo.agents")
                    result['agents_count'] = agents_count
                except:
                    pass
            
            await conn.close()
            result['status'] = 'healthy'
            print(f"   ✅ PostgreSQL подключение: OK")
            print(f"   ✅ Схема ai_seo: {'Есть' if schema_exists else 'Отсутствует'}")
            print(f"   ✅ Таблиц: {result['tables_count']}")
            print(f"   ✅ Агентов: {result['agents_count']}")
            
        except Exception as e:
            result['error'] = str(e)
            result['status'] = 'unhealthy'
            print(f"   ❌ PostgreSQL ошибка: {e}")
        
        return result
    
    async def test_redis(self) -> Dict[str, Any]:
        """Тестирование Redis подключения и функциональности"""
        print("\n🔴 Тестирование Redis...")
        
        result = {
            'service': 'redis',
            'status': 'unknown',
            'connection': False,
            'set_get_test': False,
            'info': {},
            'error': None
        }
        
        try:
            # Подключение к Redis
            r = redis.from_url(self.redis_url)
            
            # Ping test
            ping_result = await r.ping()
            result['connection'] = ping_result
            
            # Set/Get test
            test_key = "infrastructure_test"
            test_value = {"timestamp": datetime.now().isoformat(), "test": True}
            
            await r.set(test_key, json.dumps(test_value), ex=60)  # TTL 60 секунд
            retrieved_value = await r.get(test_key)
            
            if retrieved_value:
                retrieved_data = json.loads(retrieved_value)
                result['set_get_test'] = retrieved_data.get('test', False)
            
            # Получаем информацию о Redis
            info = await r.info()
            result['info'] = {
                'redis_version': info.get('redis_version', 'unknown'),
                'used_memory_human': info.get('used_memory_human', 'unknown'),
                'connected_clients': info.get('connected_clients', 0)
            }
            
            # Cleanup
            await r.delete(test_key)
            await r.close()
            
            result['status'] = 'healthy'
            print(f"   ✅ Redis подключение: OK")
            print(f"   ✅ Set/Get тест: {'OK' if result['set_get_test'] else 'FAIL'}")
            print(f"   ✅ Версия: {result['info']['redis_version']}")
            
        except Exception as e:
            result['error'] = str(e)
            result['status'] = 'unhealthy'
            print(f"   ❌ Redis ошибка: {e}")
        
        return result
    
    async def test_api_server(self) -> Dict[str, Any]:
        """Тестирование FastAPI сервера"""
        print("\n🚀 Тестирование FastAPI сервера...")
        
        result = {
            'service': 'api_server',
            'status': 'unknown',
            'health_check': False,
            'docs_accessible': False,
            'dashboard_accessible': False,
            'response_times': {},
            'error': None
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                
                # Health check
                start_time = time.time()
                async with session.get(f"{self.api_url}/health") as resp:
                    if resp.status == 200:
                        result['health_check'] = True
                        health_data = await resp.json()
                        result['health_data'] = health_data
                    result['response_times']['health'] = time.time() - start_time
                
                # API Docs
                start_time = time.time()
                async with session.get(f"{self.api_url}/api/docs") as resp:
                    result['docs_accessible'] = resp.status == 200
                    result['response_times']['docs'] = time.time() - start_time
                
                # Dashboard
                start_time = time.time()
                async with session.get(f"{self.api_url}/dashboard") as resp:
                    result['dashboard_accessible'] = resp.status == 200
                    result['response_times']['dashboard'] = time.time() - start_time
            
            result['status'] = 'healthy' if result['health_check'] else 'unhealthy'
            print(f"   ✅ Health check: {'OK' if result['health_check'] else 'FAIL'}")
            print(f"   ✅ API Docs: {'OK' if result['docs_accessible'] else 'FAIL'}")
            print(f"   ✅ Dashboard: {'OK' if result['dashboard_accessible'] else 'FAIL'}")
            print(f"   ⏱️ Время ответа: {result['response_times']['health']:.3f}s")
            
        except Exception as e:
            result['error'] = str(e)
            result['status'] = 'unhealthy'
            print(f"   ❌ API сервер ошибка: {e}")
        
        return result
    
    async def test_nginx(self) -> Dict[str, Any]:
        """Тестирование Nginx reverse proxy"""
        print("\n🌐 Тестирование Nginx...")
        
        result = {
            'service': 'nginx',
            'status': 'unknown',
            'reverse_proxy': False,
            'health_forwarding': False,
            'static_serving': False,
            'error': None
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                
                # Тестируем обращение через порт 80 (Nginx)
                try:
                    async with session.get(f"{self.base_url}/health") as resp:
                        if resp.status == 200:
                            result['reverse_proxy'] = True
                            result['health_forwarding'] = True
                except:
                    pass
                
                # Тестируем статические файлы
                try:
                    async with session.get(f"{self.base_url}/dashboard") as resp:
                        result['static_serving'] = resp.status == 200
                except:
                    pass
            
            result['status'] = 'healthy' if result['reverse_proxy'] else 'unhealthy'
            print(f"   ✅ Reverse proxy: {'OK' if result['reverse_proxy'] else 'FAIL'}")
            print(f"   ✅ Health forwarding: {'OK' if result['health_forwarding'] else 'FAIL'}")
            print(f"   ✅ Static serving: {'OK' if result['static_serving'] else 'FAIL'}")
            
        except Exception as e:
            result['error'] = str(e)
            result['status'] = 'unhealthy'
            print(f"   ❌ Nginx ошибка: {e}")
        
        return result
    
    async def test_monitoring(self) -> Dict[str, Any]:
        """Тестирование Prometheus и Grafana"""
        print("\n📊 Тестирование мониторинга...")
        
        result = {
            'service': 'monitoring',
            'status': 'unknown',
            'prometheus': False,
            'grafana': False,
            'error': None
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                
                # Prometheus
                try:
                    async with session.get("http://localhost:9090/api/v1/query?query=up") as resp:
                        result['prometheus'] = resp.status == 200
                except:
                    pass
                
                # Grafana
                try:
                    async with session.get("http://localhost:3000/api/health") as resp:
                        result['grafana'] = resp.status == 200
                except:
                    pass
            
            result['status'] = 'healthy' if result['prometheus'] and result['grafana'] else 'partial'
            print(f"   ✅ Prometheus: {'OK' if result['prometheus'] else 'FAIL'}")
            print(f"   ✅ Grafana: {'OK' if result['grafana'] else 'FAIL'}")
            
        except Exception as e:
            result['error'] = str(e)
            result['status'] = 'unhealthy'
            print(f"   ❌ Мониторинг ошибка: {e}")
        
        return result
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Запуск всех тестов инфраструктуры"""
        print("🐳 КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ DOCKER ИНФРАСТРУКТУРЫ")
        print("=" * 70)
        print(f"🕒 Время запуска: {datetime.now().isoformat()}")
        
        # Запуск всех тестов
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {}
        }
        
        test_results['tests']['postgresql'] = await self.test_postgresql()
        test_results['tests']['redis'] = await self.test_redis()
        test_results['tests']['api_server'] = await self.test_api_server()
        test_results['tests']['nginx'] = await self.test_nginx()
        test_results['tests']['monitoring'] = await self.test_monitoring()
        
        # Подсчет результатов
        total_services = len(test_results['tests'])
        healthy_services = sum(1 for test in test_results['tests'].values() if test['status'] == 'healthy')
        partial_services = sum(1 for test in test_results['tests'].values() if test['status'] == 'partial')
        
        # Итоговый статус
        print("\n" + "=" * 70)
        print("📋 ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
        print("=" * 70)
        
        for service_name, test_result in test_results['tests'].items():
            status = test_result['status']
            if status == 'healthy':
                icon = "✅"
            elif status == 'partial':
                icon = "⚠️"
            else:
                icon = "❌"
            
            print(f"   {icon} {service_name.upper()}: {status}")
        
        success_rate = (healthy_services / total_services) * 100
        print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
        print(f"   🎯 Работающих сервисов: {healthy_services}/{total_services} ({success_rate:.1f}%)")
        print(f"   ⚠️ Частично работающих: {partial_services}")
        print(f"   ❌ Неработающих: {total_services - healthy_services - partial_services}")
        
        # Финальная оценка
        if success_rate >= 90:
            grade = "A+"
            status = "🎉 ОТЛИЧНО!"
            message = "Инфраструктура полностью готова к production"
        elif success_rate >= 80:
            grade = "A"
            status = "✅ ХОРОШО!"
            message = "Инфраструктура готова к использованию"
        elif success_rate >= 60:
            grade = "B"
            status = "⚠️ УДОВЛЕТВОРИТЕЛЬНО"
            message = "Есть проблемы для устранения"
        else:
            grade = "C"
            status = "❌ КРИТИЧНО"
            message = "Серьезные проблемы с инфраструктурой"
        
        print(f"\n🏆 ИТОГОВАЯ ОЦЕНКА:")
        print(f"   {status} Оценка: {grade} ({success_rate:.1f}%)")
        print(f"   💬 {message}")
        
        test_results['summary'] = {
            'total_services': total_services,
            'healthy_services': healthy_services,
            'partial_services': partial_services,
            'success_rate': success_rate,
            'grade': grade,
            'status': status,
            'message': message
        }
        
        print(f"\n🕒 Тестирование завершено: {datetime.now().isoformat()}")
        
        return test_results


async def main():
    """Основная функция"""
    try:
        tester = InfrastructureTester()
        results = await tester.run_comprehensive_test()
        
        # Возвращаем код выхода
        success_rate = results['summary']['success_rate']
        if success_rate >= 80:
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
    asyncio.run(main())