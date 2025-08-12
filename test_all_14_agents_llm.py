#!/usr/bin/env python3
"""
🤖 Comprehensive тест всех 14 агентов AI SEO Architects с LLM интеграцией
Проверяем реальные вызовы OpenAI API с специализированными промптами
"""

import asyncio
import os
import json
from datetime import datetime
from typing import Dict, Any

# Executive Level (2 агента)
from agents.executive.chief_seo_strategist import ChiefSEOStrategistAgent
from agents.executive.business_development_director import BusinessDevelopmentDirectorAgent

# Management Level (4 агента)
from agents.management.task_coordination import TaskCoordinationAgent
from agents.management.sales_operations_manager import SalesOperationsManagerAgent
from agents.management.technical_seo_operations_manager import TechnicalSEOOperationsManagerAgent
from agents.management.client_success_manager import ClientSuccessManagerAgent

# Operational Level (8 агентов)
from agents.operational.lead_qualification import LeadQualificationAgent
from agents.operational.proposal_generation import ProposalGenerationAgent
from agents.operational.sales_conversation import SalesConversationAgent
from agents.operational.technical_seo_auditor import TechnicalSEOAuditorAgent
from agents.operational.content_strategy import ContentStrategyAgent
from agents.operational.link_building import LinkBuildingAgent
from agents.operational.competitive_analysis import CompetitiveAnalysisAgent
from agents.operational.reporting import ReportingAgent

class ComprehensiveLLMTester:
    """Comprehensive тестер для всех 14 агентов"""
    
    def __init__(self):
        self.results = {}
        self.test_data_sets = self._prepare_test_data()
        
    def _prepare_test_data(self) -> Dict[str, Dict[str, Any]]:
        """Подготавливаем тестовые данные для каждого типа агентов"""
        return {
            # Executive Level Test Data
            "executive": {
                "input_data": {
                    "company_name": "MegaCorp Industries",
                    "industry": "manufacturing", 
                    "annual_revenue": 5000000000,
                    "employee_count": 15000,
                    "market_share_percent": 12,
                    "business_goals": "Expand digital presence, increase B2B lead generation",
                    "current_challenges": "Poor online visibility, outdated digital infrastructure",
                    "strategic_timeline": "18 months",
                    "budget_range": "50000000"
                }
            },
            
            # Management Level Test Data
            "management": {
                "input_data": {
                    "current_leads": 150,
                    "qualified_leads": 45,
                    "proposals_sent": 25,
                    "deals_won": 8,
                    "team_size": 12,
                    "monthly_revenue": 2500000,
                    "target_metrics": {
                        "conversion_rate": 0.35,
                        "pipeline_velocity": 0.80,
                        "team_performance": 85
                    }
                }
            },
            
            # Operational Level Test Data  
            "operational": {
                "input_data": {
                    "company_name": "TechStart Solutions",
                    "industry": "fintech",
                    "domain": "techstart-solutions.ru",
                    "company_size": "250",
                    "budget_range": "300000",
                    "timeline": "6 months",
                    "contact_role": "Marketing Director",
                    "pain_points": "Low organic traffic, poor conversion rates",
                    "goals": "Increase organic traffic by 200%, improve lead quality",
                    "current_seo": "Basic optimization, no content strategy",
                    "competitors": ["competitor1.com", "competitor2.com"],
                    "target_keywords": ["fintech solutions", "digital banking", "payment processing"]
                }
            }
        }

    async def test_agent(self, agent_class, agent_name: str, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Тестирует конкретного агента"""
        print(f"\n🧪 Тестируем {agent_name}...")
        
        try:
            # Создаем агента
            agent = agent_class()
            
            # Выполняем задачу
            if hasattr(agent, 'process_task_with_retry'):
                result = await agent.process_task_with_retry(test_data)
            else:
                result = await agent.process_task(test_data)
            
            print(f"  📊 Успех: {result.get('success', False)}")
            if result.get('model_used'):
                print(f"  🤖 Модель: {result.get('model_used')}")
            if result.get('tokens_used'):
                tokens = result.get('tokens_used', {})
                print(f"  🔢 Токены: {tokens.get('total_tokens', 'N/A')}")
            
            # Проверяем наличие fallback режима
            result_data = result.get('result', {})
            fallback_used = False
            if isinstance(result_data, dict):
                fallback_used = result_data.get('fallback_used') or result_data.get('fallback_mode')
            elif result.get('fallback_mode'):
                fallback_used = True
            
            if fallback_used:
                print(f"  ⚠️ Используется fallback режим")
            
            return {
                "agent": agent_name,
                "success": result.get('success', False),
                "model_used": result.get('model_used'),
                "tokens_used": result.get('tokens_used', {}),
                "fallback_mode": fallback_used,
                "response_size": len(str(result.get('result', ''))),
                "error": result.get('error')
            }
            
        except Exception as e:
            print(f"  ❌ Ошибка: {str(e)}")
            return {
                "agent": agent_name,
                "success": False,
                "error": str(e),
                "fallback_mode": False
            }

    async def test_executive_agents(self):
        """Тестируем Executive агентов"""
        print("\n" + "="*60)
        print("🏢 ТЕСТИРОВАНИЕ EXECUTIVE УРОВНЯ (2/14)")
        print("="*60)
        
        executive_agents = [
            (ChiefSEOStrategistAgent, "Chief SEO Strategist"),
            (BusinessDevelopmentDirectorAgent, "Business Development Director")
        ]
        
        for agent_class, agent_name in executive_agents:
            result = await self.test_agent(agent_class, agent_name, self.test_data_sets["executive"])
            self.results[agent_name] = result

    async def test_management_agents(self):
        """Тестируем Management агентов"""
        print("\n" + "="*60)
        print("📋 ТЕСТИРОВАНИЕ MANAGEMENT УРОВНЯ (4/14)")
        print("="*60)
        
        management_agents = [
            (TaskCoordinationAgent, "Task Coordination Agent"),
            (SalesOperationsManagerAgent, "Sales Operations Manager"),
            (TechnicalSEOOperationsManagerAgent, "Technical SEO Operations Manager"),
            (ClientSuccessManagerAgent, "Client Success Manager")
        ]
        
        for agent_class, agent_name in management_agents:
            result = await self.test_agent(agent_class, agent_name, self.test_data_sets["management"])
            self.results[agent_name] = result

    async def test_operational_agents(self):
        """Тестируем Operational агентов"""
        print("\n" + "="*60)
        print("⚙️ ТЕСТИРОВАНИЕ OPERATIONAL УРОВНЯ (8/14)")
        print("="*60)
        
        operational_agents = [
            (LeadQualificationAgent, "Lead Qualification Agent"),
            (ProposalGenerationAgent, "Proposal Generation Agent"),
            (SalesConversationAgent, "Sales Conversation Agent"),
            (TechnicalSEOAuditorAgent, "Technical SEO Auditor Agent"),
            (ContentStrategyAgent, "Content Strategy Agent"),
            (LinkBuildingAgent, "Link Building Agent"),
            (CompetitiveAnalysisAgent, "Competitive Analysis Agent"),
            (ReportingAgent, "Reporting Agent")
        ]
        
        for agent_class, agent_name in operational_agents:
            result = await self.test_agent(agent_class, agent_name, self.test_data_sets["operational"])
            self.results[agent_name] = result

    async def check_openai_api_key(self):
        """Проверяем наличие OpenAI API ключа"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print(f"✅ OPENAI_API_KEY найден: {api_key[:10]}...{api_key[-4:]}")
            return True
        else:
            print("⚠️ OPENAI_API_KEY не установлен - будет использоваться fallback режим")
            return False

    def generate_final_report(self, has_api_key: bool):
        """Генерируем финальный отчет"""
        print("\n" + "="*80)
        print("📊 ФИНАЛЬНЫЙ ОТЧЕТ: LLM ИНТЕГРАЦИЯ ВСЕХ 14 АГЕНТОВ")
        print("="*80)
        
        # Статистика по уровням
        executive_results = [r for name, r in self.results.items() if "Chief" in name or "Director" in name]
        management_results = [r for name, r in self.results.items() if any(x in name for x in ["Task", "Sales Operations", "Technical SEO Operations", "Client Success"])]
        operational_results = [r for name, r in self.results.items() if name not in [r["agent"] for r in executive_results + management_results]]
        
        print(f"\n🏢 EXECUTIVE УРОВЕНЬ (2 агента):")
        self._print_level_stats(executive_results)
        
        print(f"\n📋 MANAGEMENT УРОВЕНЬ (4 агента):")
        self._print_level_stats(management_results)
        
        print(f"\n⚙️ OPERATIONAL УРОВЕНЬ (8 агентов):")
        self._print_level_stats(operational_results)
        
        # Общая статистика
        total_agents = len(self.results)
        successful_agents = sum(1 for r in self.results.values() if r["success"])
        llm_agents = sum(1 for r in self.results.values() if r.get("model_used") and not r.get("fallback_mode"))
        fallback_agents = sum(1 for r in self.results.values() if r.get("fallback_mode"))
        
        success_rate = (successful_agents / total_agents) * 100 if total_agents > 0 else 0
        llm_usage_rate = (llm_agents / total_agents) * 100 if total_agents > 0 else 0
        
        print(f"\n🎯 ОБЩАЯ СТАТИСТИКА:")
        print(f"   Всего агентов: {total_agents}/14")
        print(f"   Успешных тестов: {successful_agents}/{total_agents} ({success_rate:.1f}%)")
        print(f"   Использование LLM: {llm_agents}/{total_agents} ({llm_usage_rate:.1f}%)")
        print(f"   Fallback режим: {fallback_agents}/{total_agents}")
        
        # Токены и модели
        total_tokens = sum(r.get("tokens_used", {}).get("total_tokens", 0) for r in self.results.values())
        models_used = set(r.get("model_used") for r in self.results.values() if r.get("model_used"))
        
        if total_tokens > 0:
            print(f"\n💰 ИСПОЛЬЗОВАНИЕ РЕСУРСОВ:")
            print(f"   Общее количество токенов: {total_tokens:,}")
            print(f"   Использованные модели: {', '.join(models_used)}")
        
        # Финальная оценка
        if has_api_key and success_rate >= 95 and llm_usage_rate >= 80:
            print(f"\n🎉 ОТЛИЧНО! Все агенты успешно интегрированы с LLM")
            return 0
        elif success_rate >= 95:
            print(f"\n✅ ХОРОШО! Fallback системы работают корректно")
            return 0
        else:
            print(f"\n⚠️ ВНИМАНИЕ! Обнаружены проблемы в LLM интеграции")
            return 1

    def _print_level_stats(self, results):
        """Печатает статистику для уровня агентов"""
        successful = sum(1 for r in results if r["success"])
        total = len(results)
        llm_usage = sum(1 for r in results if r.get("model_used") and not r.get("fallback_mode"))
        
        for result in results:
            status = "✅" if result["success"] else "❌"
            llm_status = "🤖" if result.get("model_used") and not result.get("fallback_mode") else "⚠️"
            print(f"   {status} {llm_status} {result['agent']}")
            
        print(f"   📊 Успешность: {successful}/{total} ({(successful/total)*100:.1f}%)")
        print(f"   🤖 LLM использование: {llm_usage}/{total} ({(llm_usage/total)*100:.1f}%)")

async def main():
    """Главная функция тестирования"""
    print("🚀 AI SEO ARCHITECTS - COMPREHENSIVE LLM INTEGRATION TEST")
    print("Тестируем все 14 агентов с реальными OpenAI API вызовами")
    print(f"Время начала: {datetime.now()}")
    
    tester = ComprehensiveLLMTester()
    
    # Проверяем API ключ
    has_api_key = await tester.check_openai_api_key()
    
    try:
        # Тестируем все уровни
        await tester.test_executive_agents()
        await tester.test_management_agents() 
        await tester.test_operational_agents()
        
        # Генерируем отчет
        exit_code = tester.generate_final_report(has_api_key)
        
        print(f"\n⏱️ Время завершения: {datetime.now()}")
        return exit_code
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка тестирования: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)