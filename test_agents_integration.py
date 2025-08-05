#!/usr/bin/env python3
"""
Тест интеграции всех 14 агентов AI SEO Architects
Проверяет совместную работу агентов в полном цикле
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Any

# Добавляем путь к проекту
sys.path.insert(0, '.')

# Импорт агентов
from agents.executive.business_development_director import BusinessDevelopmentDirectorAgent
from agents.executive.chief_seo_strategist import ChiefSEOStrategistAgent
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
from mock_data_provider import MockDataProvider

def print_section(title: str):
    """Печать заголовка секции"""
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print('='*60)

def print_success(message: str):
    """Печать успешного результата"""
    print(f"✅ {message}")

def print_error(message: str):
    """Печать ошибки"""
    print(f"❌ {message}")

def print_info(message: str):
    """Печать информации"""
    print(f"ℹ️  {message}")

async def test_agent_initialization():
    """Тест 1: Инициализация всех агентов"""
    print_section("ТЕСТ 1: Инициализация агентов")
    
    agents = {}
    
    try:
        # Создаем mock data provider
        mock_provider = MockDataProvider()
        print_info(f"Mock Data Provider создан: {mock_provider.name}")
        
        # Chief SEO Strategist
        agents['chief_seo_strategist'] = ChiefSEOStrategistAgent(data_provider=mock_provider)
        print_success(f"Chief SEO Strategist инициализирован: {agents['chief_seo_strategist'].name}")
        
        # Business Development Director
        agents['bd_director'] = BusinessDevelopmentDirectorAgent(data_provider=mock_provider)
        print_success(f"Business Development Director инициализирован: {agents['bd_director'].name}")
        
        # Task Coordination Agent
        agents['task_coordinator'] = TaskCoordinationAgent(data_provider=mock_provider)
        print_success(f"Task Coordination Agent инициализирован: {agents['task_coordinator'].name}")
        
        # Lead Qualification Agent
        agents['lead_qualification'] = LeadQualificationAgent(data_provider=mock_provider)
        print_success(f"Lead Qualification Agent инициализирован: {agents['lead_qualification'].name}")
        
        # Proposal Generation Agent
        agents['proposal_generation'] = ProposalGenerationAgent(data_provider=mock_provider)
        print_success(f"Proposal Generation Agent инициализирован: {agents['proposal_generation'].name}")
        
        # Sales Conversation Agent
        agents['sales_conversation'] = SalesConversationAgent(data_provider=mock_provider)
        print_success(f"Sales Conversation Agent инициализирован: {agents['sales_conversation'].name}")
        
        # Technical SEO Auditor Agent
        agents['technical_seo_auditor'] = TechnicalSEOAuditorAgent(data_provider=mock_provider)
        print_success(f"Technical SEO Auditor инициализирован: {agents['technical_seo_auditor'].name}")
        
        # Content Strategy Agent
        agents['content_strategy'] = ContentStrategyAgent(data_provider=mock_provider)
        print_success(f"Content Strategy Agent инициализирован: {agents['content_strategy'].name}")
        
        # Sales Operations Manager Agent
        agents['sales_operations_manager'] = SalesOperationsManagerAgent(data_provider=mock_provider)
        print_success(f"Sales Operations Manager инициализирован: {agents['sales_operations_manager'].name}")
        
        # Technical SEO Operations Manager Agent
        agents['technical_seo_operations_manager'] = TechnicalSEOOperationsManagerAgent(data_provider=mock_provider)
        print_success(f"Technical SEO Operations Manager инициализирован: {agents['technical_seo_operations_manager'].name}")
        
        # Client Success Manager Agent
        agents['client_success_manager'] = ClientSuccessManagerAgent(data_provider=mock_provider)
        print_success(f"Client Success Manager инициализирован: {agents['client_success_manager'].name}")
        
        # Link Building Agent
        agents['link_building'] = LinkBuildingAgent(data_provider=mock_provider)
        print_success(f"Link Building Agent инициализирован: {agents['link_building'].name}")
        
        # Competitive Analysis Agent
        agents['competitive_analysis'] = CompetitiveAnalysisAgent(data_provider=mock_provider)
        print_success(f"Competitive Analysis Agent инициализирован: {agents['competitive_analysis'].name}")
        
        # Reporting Agent
        agents['reporting'] = ReportingAgent(data_provider=mock_provider)
        print_success(f"Reporting Agent инициализирован: {agents['reporting'].name}")
        
        print_info(f"Всего агентов инициализировано: {len(agents)}")
        return agents
        
    except Exception as e:
        print_error(f"Ошибка инициализации агентов: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_lead_qualification_flow(agents: Dict[str, Any]):
    """Тест 2: Полный цикл квалификации лида"""
    print_section("ТЕСТ 2: Цикл квалификации лида")
    
    # Создаем тестовые данные лида
    lead_data = {
        "company_name": "TechCorp Solutions",
        "email": "ceo@techcorp.ru",
        "phone": "+7-495-123-4567",
        "website": "https://techcorp.ru",
        "contact_name": "Алексей Петров",
        "contact_role": "CEO",
        "industry": "fintech",
        "company_size": "1000", 
        "budget_range": "5000000-10000000",
        "timeline": "Q2 2025",
        "current_seo": "basic",
        "pain_points": ["Низкий органический трафик", "Высокий CAC", "Слабые позиции в поиске"],
        "goals": ["Увеличить трафик на 300%", "Снизить стоимость привлечения клиентов"],
        "source": "website_form",
        "utm_source": "google",
        "utm_campaign": "seo_services"
    }
    
    try:
        # Шаг 1: Квалификация лида
        print_info("Шаг 1: Квалификация лида...")
        
        qualification_task = {
            "input_data": lead_data,
            "task_type": "lead_qualification"
        }
        
        qualification_result = await agents['lead_qualification'].process_task(qualification_task)
        
        if qualification_result.get('success', False):
            lead_score = qualification_result.get('lead_score', 0)
            qualification = qualification_result.get('qualification', 'Unknown')
            print_success(f"Лид квалифицирован: {qualification} (Score: {lead_score}/100)")
        else:
            print_error(f"Ошибка квалификации: {qualification_result.get('error', 'Unknown error')}")
            return None
            
        return qualification_result
        
    except Exception as e:
        print_error(f"Ошибка в цикле квалификации: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_sales_conversation_flow(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 3: Sales conversation процесс"""
    print_section("ТЕСТ 3: Sales Conversation")
    
    try:
        print_info("Проведение sales conversation...")
        
        conversation_task = {
            "input_data": {
                "qualification_result": qualification_result,
                "lead_data": qualification_result.get('enriched_data', {}),
                "conversation_type": "full_sales_conversation"
            },
            "conversation_type": "full_sales_conversation"
        }
        
        conversation_result = await agents['sales_conversation'].process_task(conversation_task)
        
        if conversation_result.get('success', False):
            quality = conversation_result.get('conversation_quality', 'Unknown')
            probability = conversation_result.get('probability_to_close', 0)
            print_success(f"Sales conversation завершен: {quality} качество, {probability:.1%} вероятность закрытия")
        else:
            print_error(f"Ошибка sales conversation: {conversation_result.get('error', 'Unknown error')}")
            return None
            
        return conversation_result
        
    except Exception as e:
        print_error(f"Ошибка в sales conversation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_proposal_generation_flow(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 4: Генерация предложения"""
    print_section("ТЕСТ 4: Генерация предложения")
    
    try:
        print_info("Генерация коммерческого предложения...")
        
        proposal_task = {
            "input_data": {
                "lead_qualification_result": qualification_result,
                "client_requirements": {
                    "focus_areas": ["technical_seo", "content_marketing"],
                    "priority": "high"
                },
                "proposal_type": "standard",
                "urgency": "medium"
            }
        }
        
        proposal_result = await agents['proposal_generation'].process_task(proposal_task)
        
        if proposal_result.get('success', False):
            proposal_data = proposal_result.get('proposal_data', {})
            total_annual = proposal_data.get('pricing', {}).get('total_annual', 0)
            confidence = proposal_data.get('confidence_score', 0)
            print_success(f"Предложение сгенерировано: {total_annual:,} ₽/год, confidence: {confidence}")
        else:
            print_error(f"Ошибка генерации предложения: {proposal_result.get('error', 'Unknown error')}")
            return None
            
        return proposal_result
        
    except Exception as e:
        print_error(f"Ошибка в генерации предложения: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_business_development_assessment(agents: Dict[str, Any], qualification_result: Dict[str, Any], proposal_result: Dict[str, Any]):
    """Тест 5: BD Director assessment"""
    print_section("ТЕСТ 5: Business Development Assessment")
    
    try:
        print_info("BD Director анализирует возможность...")
        
        # Подготавливаем данные для BD Director
        bd_task = {
            "input_data": {
                "task_type": "enterprise_assessment",
                **qualification_result.get('enriched_data', {})
            },
            "lead_analysis": qualification_result,
            "proposal_data": proposal_result.get('proposal_data', {})
        }
        
        bd_result = await agents['bd_director'].process_task(bd_task)
        
        if bd_result.get('success', False):
            strategic_impact = bd_result.get('strategic_impact', 'Unknown')
            deal_size = bd_result.get('deal_size', 0) 
            confidence = bd_result.get('confidence_score', 0)
            print_success(f"BD Assessment: {strategic_impact} impact, {deal_size:,} ₽ deal size, {confidence:.2f} confidence")
        else:
            print_error(f"Ошибка BD assessment: {bd_result.get('error', 'Unknown error')}")
            return None
            
        return bd_result
        
    except Exception as e:
        print_error(f"Ошибка в BD assessment: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_seo_strategic_analysis(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 6: Chief SEO Strategist анализ"""
    print_section("ТЕСТ 6: SEO Strategic Analysis")
    
    try:
        print_info("Chief SEO Strategist проводит стратегический анализ...")
        
        seo_task = {
            "input_data": {
                "task_type": "seo_strategic_analysis",
                **qualification_result.get('enriched_data', {}),
                "monthly_organic_traffic": 150000,
                "ranking_keywords_count": 12500,
                "domain_authority": 45,
                "current_seo_spend": 180000
            }
        }
        
        seo_result = await agents['chief_seo_strategist'].process_task(seo_task)
        
        if seo_result.get('success', False):
            strategic_impact = seo_result.get('strategic_impact', 'Unknown')
            investment_req = seo_result.get('investment_requirement', 0)
            confidence = seo_result.get('confidence_score', 0)
            print_success(f"SEO Analysis: {strategic_impact} impact, {investment_req:,} ₽ investment, {confidence:.2f} confidence")
        else:
            print_error(f"Ошибка SEO analysis: {seo_result.get('error', 'Unknown error')}")
            return None
            
        return seo_result
        
    except Exception as e:
        print_error(f"Ошибка в SEO strategic analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_technical_seo_audit(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 7: Technical SEO Auditor анализ"""
    print_section("ТЕСТ 7: Technical SEO Audit")
    
    try:
        print_info("Technical SEO Auditor проводит технический аудит...")
        
        audit_task = {
            "input_data": {
                "task_type": "full_technical_audit",
                "domain": qualification_result.get('enriched_data', {}).get('website', 'techcorp.ru'),
                "industry": qualification_result.get('enriched_data', {}).get('industry', 'fintech'),
                # Симуляция технических данных
                "lcp": 3.2,  # seconds
                "fid": 150,  # ms
                "cls": 0.15,
                "mobile_friendly": True,
                "https_implemented": True,
                "schema_markup_present": False,
                "crawling_errors": 8
            }
        }
        
        audit_result = await agents['technical_seo_auditor'].process_task(audit_task)
        
        if audit_result.get('success', False):
            audit_quality = audit_result.get('audit_quality', 'Unknown')
            technical_score = audit_result.get('result', {}).get('technical_audit_results', {}).get('overall_technical_score', 0)
            critical_issues = audit_result.get('result', {}).get('audit_summary', {}).get('critical_issues_count', 0)
            print_success(f"Technical Audit: {technical_score}/100 score, {critical_issues} critical issues, {audit_quality} quality")
        else:
            print_error(f"Ошибка Technical SEO audit: {audit_result.get('error', 'Unknown error')}")
            return None
            
        return audit_result
        
    except Exception as e:
        print_error(f"Ошибка в Technical SEO audit: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_content_strategy_analysis(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 8: Content Strategy Analysis"""
    print_section("ТЕСТ 8: Content Strategy Analysis")
    
    try:
        print_info("Content Strategy Agent проводит контентную стратегию...")
        
        content_task = {
            "input_data": {
                "task_type": "content_strategy",
                "domain": qualification_result.get('enriched_data', {}).get('website', 'techcorp.ru'),
                "industry": qualification_result.get('enriched_data', {}).get('industry', 'fintech'),
                "business_goals": ["traffic_growth", "lead_generation"],
                "monthly_budget": 150000,
                "target_audience": {"segment": "B2B", "size": "enterprise"}
            }
        }
        
        content_result = await agents['content_strategy'].process_task(content_task)
        
        if content_result.get('success', False):
            content_quality = content_result.get('content_quality', 'Unknown')
            strategy_confidence = content_result.get('strategy_confidence', 0)
            keyword_count = content_result.get('result', {}).get('keyword_research', {}).get('keyword_research_results', {}).get('total_keywords', 0)
            monthly_budget = content_result.get('result', {}).get('content_strategy', {}).get('content_strategy', {}).get('monthly_budget', 0)
            print_success(f"Content Strategy: {keyword_count} keywords, {monthly_budget:,}₽ budget, {content_quality} quality, {strategy_confidence:.2f} confidence")
        else:
            print_error(f"Ошибка Content Strategy analysis: {content_result.get('error', 'Unknown error')}")
            return None
            
        return content_result
        
    except Exception as e:
        print_error(f"Ошибка в Content Strategy analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_task_coordination(agents: Dict[str, Any]):
    """Тест 9: Task Coordination"""
    print_section("ТЕСТ 9: Task Coordination")
    
    try:
        print_info("Task Coordinator маршрутизует задачу...")
        
        coordination_task = {
            "task_type": "lead_processing",
            "priority": "high",
            "client_context": {
                "industry": "fintech",
                "size": "enterprise"
            }
        }
        
        coordination_result = await agents['task_coordinator'].process_task(coordination_task)
        
        if coordination_result.get('success', False):
            routed_to = coordination_result.get('routed_to', 'Unknown')
            priority_score = coordination_result.get('priority_score', 0)
            print_success(f"Задача маршрутизирована к {routed_to}, приоритет: {priority_score}")
        else:
            print_error(f"Ошибка координации: {coordination_result.get('error', 'Unknown error')}")
            return None
            
        return coordination_result
        
    except Exception as e:
        print_error(f"Ошибка в task coordination: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_sales_operations_analysis(agents: Dict[str, Any], qualification_result: Dict[str, Any], proposal_result: Dict[str, Any]):
    """Тест 10: Sales Operations Manager Analysis"""
    print_section("ТЕСТ 10: Sales Operations Analysis")
    
    try:
        print_info("Sales Operations Manager проводит анализ sales операций...")
        
        # Подготавливаем mock данные pipeline
        sales_ops_task = {
            "analysis_type": "full_pipeline_analysis",
            "input_data": {
                "pipeline_data": {
                    "total_leads": 180,
                    "qualified_leads": 45,
                    "proposals_sent": 28,
                    "deals_won": 8,
                    "deals_lost": 5,
                    "lead_to_qualified_rate": 0.25,
                    "qualified_to_proposal_rate": 0.62,
                    "proposal_to_win_rate": 0.29,
                    "avg_lead_response_time": 2.1,
                    "avg_qualification_time": 16.0,
                    "avg_proposal_time": 68.0,
                    "avg_deal_cycle": 38.0,
                    "total_pipeline_value": 52000000,
                    "average_deal_size": 3200000,
                    "monthly_recurring_revenue": 9200000,
                    "pipeline_velocity": 0.82,
                    "lead_quality_score": 76.5,
                    "sales_efficiency": 0.73
                },
                "team_data": {
                    "sdr_performance": [
                        {"name": "Анна Петрова", "quota_attainment": 1.15, "lead_quality": 8.2},
                        {"name": "Дмитрий Смирнов", "quota_attainment": 0.95, "lead_quality": 7.8}
                    ],
                    "ae_performance": [
                        {"name": "Елена Кузнецова", "quota_attainment": 1.08, "close_rate": 0.32},
                        {"name": "Михаил Волков", "quota_attainment": 0.87, "close_rate": 0.28}
                    ]
                }
            }
        }
        
        sales_ops_result = await agents['sales_operations_manager'].process_task(sales_ops_task)
        
        if sales_ops_result.get('success', False):
            pipeline_health = sales_ops_result.get('pipeline_health_score', 0)
            key_insights_count = len(sales_ops_result.get('key_insights', []))
            priority_actions_count = len(sales_ops_result.get('priority_actions', []))
            confidence = sales_ops_result.get('confidence_score', 0)
            print_success(f"Sales Ops Analysis: {pipeline_health:.1f}/100 pipeline health, {key_insights_count} insights, {priority_actions_count} priority actions, {confidence:.2f} confidence")
        else:
            print_error(f"Ошибка Sales Operations analysis: {sales_ops_result.get('error', 'Unknown error')}")
            return None
            
        return sales_ops_result
        
    except Exception as e:
        print_error(f"Ошибка в Sales Operations analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_technical_seo_operations_analysis(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 11: Technical SEO Operations Manager Analysis"""
    print_section("ТЕСТ 11: Technical SEO Operations Analysis")
    
    try:
        print_info("Technical SEO Operations Manager проводит анализ технических операций...")
        
        # Подготавливаем mock данные для технического анализа
        tech_ops_task = {
            "analysis_type": "comprehensive_operations_analysis",
            "input_data": {
                "technical_issues": [
                    {
                        "issue_id": "TECH-001",
                        "issue_type": "core_web_vitals",
                        "severity": "high",
                        "title": "LCP превышает 4 секунды на мобильных устройствах",
                        "affected_pages_count": 1250,
                        "traffic_impact": 0.35,
                        "ranking_impact": 0.25,
                        "solution_priority": 9,
                        "estimated_fix_time": 72
                    },
                    {
                        "issue_id": "TECH-002",
                        "issue_type": "crawling", 
                        "severity": "critical",
                        "title": "Robots.txt блокирует важные разделы сайта",
                        "affected_pages_count": 850,
                        "traffic_impact": 0.60,
                        "ranking_impact": 0.45,
                        "solution_priority": 10,
                        "estimated_fix_time": 24
                    }
                ],
                "cwv_metrics": {
                    "mobile": {
                        "lcp_score": 3.8,
                        "fid_score": 145,
                        "cls_score": 0.18,
                        "lcp_rating": "needs-improvement",
                        "fid_rating": "needs-improvement",
                        "cls_rating": "needs-improvement"
                    },
                    "desktop": {
                        "lcp_score": 2.1,
                        "fid_score": 85,
                        "cls_score": 0.08,
                        "lcp_rating": "good",
                        "fid_rating": "good", 
                        "cls_rating": "good"
                    }
                },
                "project_status": {
                    "active_projects": 8,
                    "on_schedule": 5,
                    "delayed": 2,
                    "completed_this_month": 3
                },
                "team_performance": {
                    "utilization": 0.82,
                    "avg_resolution_time": 54.5,
                    "issues_resolved_this_month": 23,
                    "projects_delivered_on_time": 0.75
                }
            }
        }
        
        tech_ops_result = await agents['technical_seo_operations_manager'].process_task(tech_ops_task)
        
        if tech_ops_result.get('success', False):
            operations_health = tech_ops_result.get('operations_health_score', 0)
            key_insights_count = len(tech_ops_result.get('key_insights', []))
            priority_actions_count = len(tech_ops_result.get('priority_actions', []))
            confidence = tech_ops_result.get('confidence_score', 0)
            print_success(f"Technical SEO Ops Analysis: {operations_health:.1f}/100 operations health, {key_insights_count} insights, {priority_actions_count} priority actions, {confidence:.2f} confidence")
        else:
            print_error(f"Ошибка Technical SEO Operations analysis: {tech_ops_result.get('error', 'Unknown error')}")
            return None
            
        return tech_ops_result
        
    except Exception as e:
        print_error(f"Ошибка в Technical SEO Operations analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_client_success_management(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 12: Client Success Manager Analysis"""
    print_section("ТЕСТ 12: Client Success Management")
    
    try:
        print_info("Client Success Manager проводит анализ здоровья клиента...")
        
        client_success_task = {
            "task_type": "client_health_assessment",
            "client_data": {
                "company_name": qualification_result.get('enriched_data', {}).get('company_name', 'TechCorp Solutions'),
                "monthly_value": 850000,
                "engagement_score": 78,
                "payment_delays": 1,
                "support_tickets": 3,
                "feature_adoption": 85,
                "nps_score": 8,
                "last_login_days": 2
            }
        }
        
        client_success_result = await agents['client_success_manager'].process_task(client_success_task)
        
        if client_success_result.get('success', False):
            health_score = client_success_result.get('health_score', 0)
            health_status = client_success_result.get('health_status', 'unknown')
            nps_score = client_success_result.get('metrics', {}).get('nps_score', 0)
            recommendations_count = len(client_success_result.get('recommendations', []))
            print_success(f"Client Success Analysis: {health_score}/100 health score, {health_status} status, NPS {nps_score}/10, {recommendations_count} recommendations")
        else:
            print_error(f"Ошибка Client Success analysis: {client_success_result.get('error', 'Unknown error')}")
            return None
            
        return client_success_result
        
    except Exception as e:
        print_error(f"Ошибка в Client Success analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_link_building_analysis(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 13: Link Building Agent Analysis"""
    print_section("ТЕСТ 13: Link Building Analysis")
    
    try:
        print_info("Link Building Agent проводит анализ ссылочного профиля...")
        
        link_building_task = {
            "task_type": "link_prospect_analysis",
            "domain_data": {
                "domain": qualification_result.get('enriched_data', {}).get('website', 'techcorp.ru').replace('https://', ''),
                "industry": qualification_result.get('enriched_data', {}).get('industry', 'fintech')
            }
        }
        
        link_building_result = await agents['link_building'].process_task(link_building_task)
        
        if link_building_result.get('success', False):
            total_prospects = link_building_result.get('total_prospects_found', 0)
            premium_prospects = link_building_result.get('quality_distribution', {}).get('premium', 0)
            high_prospects = link_building_result.get('quality_distribution', {}).get('high', 0)
            monthly_capacity = link_building_result.get('estimated_monthly_capacity', {}).get('total_realistic_capacity', 0)
            print_success(f"Link Building Analysis: {total_prospects} prospects found, {premium_prospects} premium + {high_prospects} high quality, {monthly_capacity} monthly capacity")
        else:
            print_error(f"Ошибка Link Building analysis: {link_building_result.get('error', 'Unknown error')}")
            return None
            
        return link_building_result
        
    except Exception as e:
        print_error(f"Ошибка в Link Building analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_competitive_analysis(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 14: Competitive Analysis Agent"""
    print_section("ТЕСТ 14: Competitive Analysis")
    
    try:
        print_info("Competitive Analysis Agent проводит конкурентный анализ...")
        
        competitive_task = {
            "task_type": "serp_analysis",
            "query_data": {
                "keywords": ["финтех услуги", "цифровые банковские решения", "SEO для финтеха"],
                "our_domain": qualification_result.get('enriched_data', {}).get('website', 'techcorp.ru').replace('https://', '')
            }
        }
        
        competitive_result = await agents['competitive_analysis'].process_task(competitive_task)
        
        if competitive_result.get('success', False):
            keywords_analyzed = competitive_result.get('keywords_analyzed', 0)
            serp_ownership = competitive_result.get('serp_feature_ownership', 0)
            high_priority_opps = len(competitive_result.get('high_priority_opportunities', []))
            medium_priority_opps = len(competitive_result.get('medium_priority_opportunities', []))
            print_success(f"Competitive Analysis: {keywords_analyzed} keywords analyzed, {serp_ownership:.1f}% SERP ownership, {high_priority_opps} high + {medium_priority_opps} medium priority opportunities")
        else:
            print_error(f"Ошибка Competitive analysis: {competitive_result.get('error', 'Unknown error')}")
            return None
            
        return competitive_result
        
    except Exception as e:
        print_error(f"Ошибка в Competitive analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_reporting_analysis(agents: Dict[str, Any], qualification_result: Dict[str, Any]):
    """Тест 15: Reporting Agent Analysis"""
    print_section("ТЕСТ 15: Reporting Analysis")
    
    try:
        print_info("Reporting Agent генерирует комплексный отчет...")
        
        reporting_task = {
            "task_type": "generate_report", 
            "report_config": {
                "type": "comprehensive_performance",
                "domain": qualification_result.get('enriched_data', {}).get('website', 'techcorp.ru').replace('https://', ''),
                "period_days": 30,
                "client_type": "enterprise"
            }
        }
        
        reporting_result = await agents['reporting'].process_task(reporting_task)
        
        if reporting_result.get('success', False):
            report_type = reporting_result.get('report_metadata', {}).get('report_type', 'unknown')
            confidence_score = reporting_result.get('report_metadata', {}).get('confidence_score', 0)
            recommendations_count = len(reporting_result.get('recommendations', []))
            export_formats = len(reporting_result.get('export_formats', []))
            print_success(f"Reporting Analysis: {report_type} report generated, {confidence_score:.1%} confidence, {recommendations_count} recommendations, {export_formats} export formats")
        else:
            print_error(f"Ошибка Reporting analysis: {reporting_result.get('error', 'Unknown error')}")
            return None
            
        return reporting_result
        
    except Exception as e:
        print_error(f"Ошибка в Reporting analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

async def test_full_integration():
    """Полный интеграционный тест"""
    print_section("ПОЛНЫЙ ИНТЕГРАЦИОННЫЙ ТЕСТ AI SEO ARCHITECTS")
    
    test_results = {
        'initialization': False,
        'lead_qualification': False,
        'sales_conversation': False,
        'proposal_generation': False,
        'bd_assessment': False,
        'seo_strategic_analysis': False,
        'technical_seo_audit': False,
        'content_strategy_analysis': False,
        'task_coordination': False,
        'sales_operations_analysis': False,
        'technical_seo_operations_analysis': False,
        'client_success_management': False,
        'link_building_analysis': False,
        'competitive_analysis': False,
        'reporting_analysis': False
    }
    
    # Тест 1: Инициализация
    agents = await test_agent_initialization()
    if agents:
        test_results['initialization'] = True
    else:
        print_error("Критическая ошибка: не удалось инициализировать агентов")
        return test_results
    
    # Тест 2: Квалификация лида
    qualification_result = await test_lead_qualification_flow(agents)
    if qualification_result:
        test_results['lead_qualification'] = True
    else:
        print_error("Ошибка квалификации лида")
        return test_results
    
    # Тест 3: Sales conversation (параллельно с proposal)
    sales_task = test_sales_conversation_flow(agents, qualification_result)
    proposal_task = test_proposal_generation_flow(agents, qualification_result)
    
    # Запускаем параллельно
    sales_result, proposal_result = await asyncio.gather(sales_task, proposal_task, return_exceptions=True)
    
    if not isinstance(sales_result, Exception) and sales_result:
        test_results['sales_conversation'] = True
    
    if not isinstance(proposal_result, Exception) and proposal_result:
        test_results['proposal_generation'] = True
    
    # Тест 5: BD Assessment
    if proposal_result and qualification_result:
        bd_result = await test_business_development_assessment(agents, qualification_result, proposal_result)
        if bd_result:
            test_results['bd_assessment'] = True
    
    # Тест 6: SEO Strategic Analysis
    if qualification_result:
        seo_result = await test_seo_strategic_analysis(agents, qualification_result)
        if seo_result:
            test_results['seo_strategic_analysis'] = True
    
    # Тест 7: Technical SEO Audit
    if qualification_result:
        technical_audit_result = await test_technical_seo_audit(agents, qualification_result)
        if technical_audit_result:
            test_results['technical_seo_audit'] = True
    
    # Тест 8: Content Strategy Analysis
    if qualification_result:
        content_strategy_result = await test_content_strategy_analysis(agents, qualification_result)
        if content_strategy_result:
            test_results['content_strategy_analysis'] = True
    
    # Тест 9: Task Coordination
    coordination_result = await test_task_coordination(agents)
    if coordination_result:
        test_results['task_coordination'] = True
    
    # Тест 10: Sales Operations Analysis
    if qualification_result and proposal_result:
        sales_ops_result = await test_sales_operations_analysis(agents, qualification_result, proposal_result)
        if sales_ops_result:
            test_results['sales_operations_analysis'] = True
    
    # Тест 11: Technical SEO Operations Analysis
    if qualification_result:
        tech_seo_ops_result = await test_technical_seo_operations_analysis(agents, qualification_result)
        if tech_seo_ops_result:
            test_results['technical_seo_operations_analysis'] = True
    
    # Тест 12: Client Success Management
    if qualification_result:
        client_success_result = await test_client_success_management(agents, qualification_result)
        if client_success_result:
            test_results['client_success_management'] = True
    
    # Тест 13: Link Building Analysis
    if qualification_result:
        link_building_result = await test_link_building_analysis(agents, qualification_result)
        if link_building_result:
            test_results['link_building_analysis'] = True
    
    # Тест 14: Competitive Analysis
    if qualification_result:
        competitive_result = await test_competitive_analysis(agents, qualification_result)
        if competitive_result:
            test_results['competitive_analysis'] = True
    
    # Тест 15: Reporting Analysis
    if qualification_result:
        reporting_result = await test_reporting_analysis(agents, qualification_result)
        if reporting_result:
            test_results['reporting_analysis'] = True
    
    return test_results

async def main():
    """Главная функция"""
    print("🚀 ЗАПУСК ИНТЕГРАЦИОННОГО ТЕСТИРОВАНИЯ AI SEO ARCHITECTS")
    print(f"📅 Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = datetime.now()
    
    # Запуск полного интеграционного теста
    results = await test_full_integration()
    
    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    
    # Отчет о результатах
    print_section("ОТЧЕТ О РЕЗУЛЬТАТАХ ТЕСТИРОВАНИЯ")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = passed_tests / total_tests * 100
    
    print(f"📊 Общие результаты:")
    print(f"   Всего тестов: {total_tests}")
    print(f"   Успешно: {passed_tests}")
    print(f"   Провалено: {total_tests - passed_tests}")
    print(f"   Процент успеха: {success_rate:.1f}%")
    print(f"   Время выполнения: {execution_time:.2f} секунд")
    
    print(f"\n📋 Детальные результаты:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name.replace('_', ' ').title()}: {status}")
    
    if success_rate >= 80:
        print(f"\n🎉 ИНТЕГРАЦИОННОЕ ТЕСТИРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО!")
        print(f"   Система готова к продакшену")
    elif success_rate >= 60:
        print(f"\n⚠️  ЧАСТИЧНЫЙ УСПЕХ")
        print(f"   Система работает, но требует доработки")
    else:
        print(f"\n🔥 КРИТИЧЕСКИЕ ПРОБЛЕМЫ")
        print(f"   Система требует серьезной отладки")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())