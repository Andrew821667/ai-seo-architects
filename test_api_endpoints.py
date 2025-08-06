#!/usr/bin/env python3
"""
Быстрое тестирование API endpoints AI SEO Architects
"""

import asyncio
import httpx
import json
from datetime import datetime


class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    async def test_health(self):
        """Тест health endpoint"""
        print("🔍 Тестирование health endpoint...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/health")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Health check: {data.get('status', 'unknown')}")
                    print(f"   Версия: {data.get('version', 'N/A')}")
                    print(f"   Uptime: {data.get('uptime_seconds', 0):.0f}s")
                else:
                    print(f"❌ Health check failed: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Health check error: {e}")
    
    async def test_authentication(self):
        """Тест аутентификации"""
        print("\n🔐 Тестирование аутентификации...")
        
        try:
            async with httpx.AsyncClient() as client:
                # Попытка авторизации
                response = await client.post(
                    f"{self.base_url}/auth/login",
                    json={"username": "admin", "password": "secret"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get("access_token")
                    self.headers["Authorization"] = f"Bearer {self.token}"
                    print("✅ Авторизация успешна")
                    print(f"   Token type: {data.get('token_type')}")
                    print(f"   Expires in: {data.get('expires_in')}s")
                else:
                    print(f"❌ Авторизация failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
        except Exception as e:
            print(f"❌ Authentication error: {e}")
    
    async def test_agents_list(self):
        """Тест получения списка агентов"""
        print("\n🤖 Тестирование списка агентов...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/agents/",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Получено агентов: {data.get('total_count', 0)}")
                    print(f"   Активные: {data.get('active_count', 0)}")
                    print(f"   MCP включен: {data.get('mcp_enabled_count', 0)}")
                    
                    # Показываем первые 3 агента
                    agents = data.get('agents', [])[:3]
                    for agent in agents:
                        print(f"   - {agent.get('name', 'Unknown')}: {agent.get('status', 'unknown')}")
                else:
                    print(f"❌ Agents list failed: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Agents list error: {e}")
    
    async def test_agent_creation(self):
        """Тест создания агентов"""
        print("\n🏗️ Тестирование создания агентов...")
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/agents/create-all",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = data.get('data', {})
                    print(f"✅ Создано агентов: {result.get('created_count', 0)}")
                    print(f"   MCP enabled: {result.get('mcp_enabled', False)}")
                else:
                    print(f"❌ Agent creation failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
        except Exception as e:
            print(f"❌ Agent creation error: {e}")
    
    async def test_agent_task(self):
        """Тест выполнения задачи агентом"""
        print("\n⚡ Тестирование выполнения задачи агентом...")
        
        task_data = {
            "task_type": "lead_analysis",
            "input_data": {
                "company_data": {
                    "company_name": "Test Company API",
                    "industry": "technology",
                    "annual_revenue": "5000000",
                    "employee_count": "50"
                }
            },
            "priority": "normal"
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/agents/lead_qualification/tasks",
                    json=task_data,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Задача выполнена: {data.get('status', 'unknown')}")
                    print(f"   Processing time: {data.get('processing_time', 0):.2f}s")
                    print(f"   Task ID: {data.get('task_id', 'N/A')}")
                    
                    # Показываем результат если есть
                    result = data.get('result')
                    if result and isinstance(result, dict):
                        lead_score = result.get('lead_score')
                        if lead_score:
                            print(f"   Lead Score: {lead_score}/100")
                else:
                    print(f"❌ Agent task failed: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
        except Exception as e:
            print(f"❌ Agent task error: {e}")
    
    async def test_dashboard_data(self):
        """Тест получения данных дашборда"""
        print("\n📊 Тестирование данных дашборда...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/analytics/dashboard",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    dashboard_data = data.get('data', {})
                    
                    print("✅ Dashboard data получены:")
                    
                    # System health
                    system = dashboard_data.get('system_health', {})
                    print(f"   System: {system.get('status', 'unknown')}")
                    print(f"   CPU: {system.get('cpu_percent', 0):.1f}%")
                    print(f"   Memory: {system.get('memory_percent', 0):.1f}%")
                    
                    # Agents summary
                    agents = dashboard_data.get('agents_summary', {})
                    print(f"   Agents: {agents.get('active_agents', 0)}/{agents.get('total_agents', 0)}")
                    print(f"   Success rate: {agents.get('avg_success_rate', 0):.1%}")
                    
                else:
                    print(f"❌ Dashboard data failed: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Dashboard data error: {e}")
    
    async def test_websocket_connection(self):
        """Тест WebSocket подключения"""
        print("\n🔗 Тестирование WebSocket подключения...")
        
        try:
            import websockets
            
            uri = f"ws://localhost:8000/ws/dashboard"
            
            async with websockets.connect(uri) as websocket:
                print("✅ WebSocket подключение установлено")
                
                # Отправляем heartbeat
                await websocket.send(json.dumps({
                    "type": "heartbeat"
                }))
                
                # Ждем ответ
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                
                print(f"   Received: {data.get('type', 'unknown')}")
                print("✅ WebSocket работает корректно")
                
        except ImportError:
            print("⚠️ WebSocket test skipped (websockets package not installed)")
        except asyncio.TimeoutError:
            print("❌ WebSocket timeout")
        except Exception as e:
            print(f"❌ WebSocket error: {e}")
    
    async def run_all_tests(self):
        """Запуск всех тестов"""
        print("🧪 AI SEO Architects API Testing Suite")
        print("=" * 50)
        print(f"Base URL: {self.base_url}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 50)
        
        # Последовательность тестов
        await self.test_health()
        await self.test_authentication()
        
        if self.token:  # Только если авторизация прошла успешно
            await self.test_agent_creation()
            await self.test_agents_list()
            await self.test_agent_task()
            await self.test_dashboard_data()
        
        await self.test_websocket_connection()
        
        print("\n" + "=" * 50)
        print("🎉 Тестирование завершено!")
        print("💡 Откройте http://localhost:8000/dashboard для просмотра UI")
        print("📚 API Docs: http://localhost:8000/api/docs")


async def main():
    """Главная функция"""
    tester = APITester()
    await tester.run_all_tests()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка тестирования: {e}")