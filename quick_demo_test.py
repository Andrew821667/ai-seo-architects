#!/usr/bin/env python3
"""
Быстрый демо-тест всех 14 агентов AI SEO Architects
Использует стандартные тестовые данные для стабильной работы
"""

import asyncio
import time
from datetime import datetime
from mock_data_provider import MockDataProvider

# Импорты всех агентов
from agents.executive.chief_seo_strategist import ChiefSEOStrategistAgent
from agents.executive.business_development_director import BusinessDevelopmentDirectorAgent
from agents.management.task_coordination import TaskCoordinationAgent
from agents.management.sales_operations_manager import SalesOperationsManagerAgent
from agents.management.technical_seo_operations_manager import TechnicalSEOOperationsManagerAgent
from agents.management.client_success_manager import ClientSuccessManagerAgent
from agents.operational.lead_qualification import LeadQualificationAgent
from agents.operational.proposal_generation import ProposalGenerationAgent
from agents.operational.sales_conversation import SalesConversationAgent
from agents.operational.technical_seo_auditor import TechnicalSEOAuditorAgent
from agents.operational.content_strategy import ContentStrategyAgent
from agents.operational.link_building import LinkBuildingAgent
from agents.operational.competitive_analysis import CompetitiveAnalysisAgent
from agents.operational.reporting import ReportingAgent

async def demo_all_agents():
    """Демонстрация работы всех агентов"""
    
    print("🚀 ДЕМОНСТРАЦИЯ AI SEO ARCHITECTS - ВСЕ 14 АГЕНТОВ")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🏢 Тестовая компания: TechCorp Solutions (FinTech)")
    print("=" * 80)
    
    provider = MockDataProvider()
    results = []
    
    # Стандартные тестовые данные
    test_data = {
        "input_data": {
            "company_name": "TechCorp Solutions",
            "industry": "fintech",
            "email": "ceo@techcorp.ru",
            "budget_range": "5000000-10000000",
            "domain": "https://techcorp.ru"
        }
    }
    
    # Список агентов для тестирования
    agents_config = [
        ("👑 Chief SEO Strategist", ChiefSEOStrategistAgent, "seo_strategic_analysis"),
        ("👑 Business Development Director", BusinessDevelopmentDirectorAgent, "enterprise_assessment"),
        ("🎛️ Task Coordination Agent", TaskCoordinationAgent, "task_routing"),
        ("🎛️ Sales Operations Manager", SalesOperationsManagerAgent, "sales_operations_analysis"),
        ("🎛️ Technical SEO Operations Manager", TechnicalSEOOperationsManagerAgent, "comprehensive_operations_analysis"),
        ("🎛️ Client Success Manager", ClientSuccessManagerAgent, "comprehensive_client_analysis"),
        ("⚙️ Lead Qualification Agent", LeadQualificationAgent, "lead_qualification"),
        ("⚙️ Proposal Generation Agent", ProposalGenerationAgent, "proposal_generation"),
        ("⚙️ Sales Conversation Agent", SalesConversationAgent, "full_sales_conversation"),
        ("⚙️ Technical SEO Auditor", TechnicalSEOAuditorAgent, "full_technical_audit"),
        ("⚙️ Content Strategy Agent", ContentStrategyAgent, "comprehensive_content_strategy"),
        ("⚙️ Link Building Agent", LinkBuildingAgent, "comprehensive_analysis"),
        ("⚙️ Competitive Analysis Agent", CompetitiveAnalysisAgent, "comprehensive_analysis"),
        ("⚙️ Reporting Agent", ReportingAgent, "comprehensive_analysis"),
    ]
    
    total_agents = len(agents_config)
    successful = 0
    total_time = 0
    
    for i, (name, agent_class, task_type) in enumerate(agents_config, 1):
        try:
            print(f"\n[{i:2d}/{total_agents}] {name}")
            print("-" * 60)
            
            # Создание агента
            agent = agent_class(data_provider=provider)
            
            # Подготовка задачи
            task = test_data.copy()
            task["input_data"]["task_type"] = task_type
            
            # Выполнение
            start_time = time.time()
            result = await agent.process_task(task)
            duration = time.time() - start_time
            total_time += duration
            
            # Анализ результата
            success = result.get('success', True)
            if success:
                successful += 1
                status = "✅ SUCCESS"
                color = "\033[92m"  # Green
            else:
                status = "❌ ERROR"
                color = "\033[91m"  # Red
            
            reset_color = "\033[0m"
            
            print(f"   Статус: {color}{status}{reset_color}")
            print(f"   Время: {duration:.3f}s")
            
            # Ключевые метрики
            metrics = extract_key_metrics(name, result)
            if metrics:
                print(f"   Результат: {metrics}")
            
            results.append({
                "agent": name,
                "success": success,
                "duration": duration,
                "metrics": metrics
            })
            
        except Exception as e:
            print(f"   Статус: \033[91m❌ ERROR\033[0m")
            print(f"   Ошибка: {str(e)[:80]}...")
            results.append({
                "agent": name,
                "success": False,
                "duration": 0,
                "error": str(e)
            })
    
    # Итоговый отчет
    print("\n" + "=" * 80)
    print("📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print("=" * 80)
    
    success_rate = (successful / total_agents) * 100
    avg_time = total_time / total_agents if total_agents > 0 else 0
    
    print(f"✅ Успешно выполнено: {successful}/{total_agents} ({success_rate:.1f}%)")
    print(f"⏱️  Общее время: {total_time:.2f}s (среднее: {avg_time:.3f}s)")
    
    if success_rate == 100:
        print("🎉 ВСЕ АГЕНТЫ РАБОТАЮТ ОТЛИЧНО!")
    elif success_rate >= 80:
        print("👍 БОЛЬШИНСТВО АГЕНТОВ ФУНКЦИОНАЛЬНЫ")
    else:
        print("⚠️  ТРЕБУЕТСЯ ДОРАБОТКА НЕКОТОРЫХ АГЕНТОВ")
    
    # Группировка по уровням
    executive_agents = [r for r in results if "👑" in r["agent"]]
    management_agents = [r for r in results if "🎛️" in r["agent"]]
    operational_agents = [r for r in results if "⚙️" in r["agent"]]
    
    print(f"\n📋 По уровням архитектуры:")
    print(f"   👑 Executive: {sum(1 for a in executive_agents if a['success'])}/{len(executive_agents)}")
    print(f"   🎛️ Management: {sum(1 for a in management_agents if a['success'])}/{len(management_agents)}")
    print(f"   ⚙️ Operational: {sum(1 for a in operational_agents if a['success'])}/{len(operational_agents)}")
    
    # Сохранение в файл
    save_results_to_markdown(results, successful, total_agents, total_time)
    
    return success_rate == 100

def extract_key_metrics(agent_name: str, result: dict) -> str:
    """Извлечение ключевых метрик для отображения"""
    
    if "Lead Qualification" in agent_name:
        score = result.get('lead_score', 0)
        qual = result.get('qualification', 'N/A')
        return f"Score {score}/100, {qual}"
    
    elif "Proposal Generation" in agent_name:
        value = result.get('total_annual_value', 0)
        return f"Proposal {value:,.0f} ₽/год"
    
    elif "Sales Conversation" in agent_name:
        quality = result.get('conversation_quality', 'N/A')
        prob = result.get('close_probability', 0)
        return f"{quality}, {prob*100:.0f}% close"
    
    elif "Technical SEO Auditor" in agent_name:
        score = result.get('audit_score', 0)
        issues = result.get('critical_issues_count', 0)
        return f"Audit {score}/100, {issues} issues"
    
    elif "Content Strategy" in agent_name:
        keywords = result.get('total_keywords', 0)
        budget = result.get('recommended_budget', 0)
        return f"{keywords} keywords, {budget:,.0f} ₽"
    
    elif "Business Development" in agent_name:
        score = result.get('enterprise_score', 0)
        impact = result.get('strategic_impact', 'N/A')
        return f"Enterprise {score}/100, {impact}"
    
    elif "Chief SEO Strategist" in agent_name:
        score = result.get('strategic_score', 0)
        impact = result.get('strategic_impact', 'N/A')
        return f"Strategic {score}/100, {impact}"
    
    elif "Sales Operations" in agent_name:
        health = result.get('pipeline_health_score', 0)
        insights = len(result.get('key_insights', []))
        return f"Pipeline {health:.0f}/100, {insights} insights"
    
    elif "Technical SEO Operations" in agent_name:
        health = result.get('operations_health_score', 0)
        issues = len(result.get('technical_issues', []))
        return f"Ops {health:.0f}/100, {issues} issues"
    
    elif "Client Success" in agent_name:
        health = result.get('overall_health_score', 0)
        status = result.get('health_status', 'N/A')
        return f"Health {health}/100, {status}"
    
    elif "Link Building" in agent_name:
        prospects = result.get('total_prospects', 0)
        quality = result.get('high_quality_count', 0)
        return f"{prospects} prospects, {quality} high quality"
    
    elif "Competitive Analysis" in agent_name:
        competitors = len(result.get('competitor_analysis', []))
        ownership = result.get('serp_ownership', 0)
        return f"{competitors} competitors, {ownership*100:.1f}% SERP"
    
    elif "Reporting" in agent_name:
        report_type = result.get('report_type', 'N/A')
        confidence = result.get('confidence', 0)
        return f"{report_type}, {confidence*100:.0f}% confidence"
    
    elif "Task Coordination" in agent_name:
        agent_assigned = result.get('assigned_agent', 'N/A')
        priority = result.get('priority', 0)
        return f"→ {agent_assigned}, priority {priority}"
    
    return "Completed successfully"

def save_results_to_markdown(results, successful, total, total_time):
    """Сохранение результатов в markdown"""
    
    filename = f"DEMO_RESULTS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    md_content = f"""# 🤖 AI SEO Architects - Demo Results

**Дата тестирования:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Тестовая компания:** TechCorp Solutions (FinTech)

## 📊 Общие результаты

- **Всего агентов:** {total}
- **Успешно выполнено:** {successful}
- **Процент успеха:** {(successful/total)*100:.1f}%
- **Общее время:** {total_time:.2f}s
- **Среднее время на агента:** {total_time/total:.3f}s

## 📋 Результаты по агентам

"""
    
    for result in results:
        status_emoji = "✅" if result['success'] else "❌"
        agent_name = result['agent'].replace('👑 ', '').replace('🎛️ ', '').replace('⚙️ ', '')
        
        md_content += f"### {status_emoji} {agent_name}\n\n"
        md_content += f"- **Время выполнения:** {result.get('duration', 0):.3f}s\n"
        
        if result['success']:
            metrics = result.get('metrics', 'Completed successfully')
            md_content += f"- **Результат:** {metrics}\n"
        else:
            error = result.get('error', 'Unknown error')
            md_content += f"- **Ошибка:** {error}\n"
        
        md_content += "\n"
    
    md_content += f"""## 🎯 Заключение

{"🎉 Все агенты работают отлично!" if successful == total else 
 "👍 Большинство агентов функциональны" if successful/total >= 0.8 else 
 "⚠️ Требуется доработка некоторых агентов"}

**Система готова к {"production" if successful == total else "дальнейшей разработке"}**

---

*Сгенерировано AI SEO Architects Demo Suite*
"""
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"\n💾 Результаты сохранены: {filename}")
    except Exception as e:
        print(f"⚠️  Ошибка сохранения: {e}")

if __name__ == "__main__":
    success = asyncio.run(demo_all_agents())
    exit(0 if success else 1)