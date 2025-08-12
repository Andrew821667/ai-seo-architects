"""AI SEO Architects - Агенты для автоматизации SEO-агентства

Этот пакет содержит полную команду из 14 AI-агентов, организованных по уровням:
- Executive Level (2 агента): стратегическое планирование и развитие бизнеса
- Management Level (4 агента): координация процессов и операций
- Operational Level (8 агентов): выполнение специализированных задач
"""

from .executive.chief_seo_strategist import ChiefSEOStrategistAgent
from .executive.business_development_director import BusinessDevelopmentDirectorAgent

from .management.task_coordination import TaskCoordinationAgent
from .management.sales_operations_manager import SalesOperationsManagerAgent
from .management.technical_seo_operations_manager import TechnicalSEOOperationsManagerAgent
from .management.client_success_manager import ClientSuccessManagerAgent

from .operational.lead_qualification import LeadQualificationAgent
from .operational.proposal_generation import ProposalGenerationAgent
from .operational.sales_conversation import SalesConversationAgent
from .operational.technical_seo_auditor import TechnicalSEOAuditorAgent
from .operational.content_strategy import ContentStrategyAgent
from .operational.link_building import LinkBuildingAgent
from .operational.competitive_analysis import CompetitiveAnalysisAgent
from .operational.reporting import ReportingAgent

# Группировка по уровням
EXECUTIVE_AGENTS = [
    ChiefSEOStrategistAgent,
    BusinessDevelopmentDirectorAgent
]

MANAGEMENT_AGENTS = [
    TaskCoordinationAgent,
    SalesOperationsManagerAgent,
    TechnicalSEOOperationsManagerAgent,
    ClientSuccessManagerAgent
]

OPERATIONAL_AGENTS = [
    LeadQualificationAgent,
    ProposalGenerationAgent,
    SalesConversationAgent,
    TechnicalSEOAuditorAgent,
    ContentStrategyAgent,
    LinkBuildingAgent,
    CompetitiveAnalysisAgent,
    ReportingAgent
]

# Все агенты
ALL_AGENTS = EXECUTIVE_AGENTS + MANAGEMENT_AGENTS + OPERATIONAL_AGENTS

# Mapping по ID агентов
AGENT_CLASSES = {
    'chief_seo_strategist': ChiefSEOStrategistAgent,
    'business_development_director': BusinessDevelopmentDirectorAgent,
    'task_coordination': TaskCoordinationAgent,
    'sales_operations_manager': SalesOperationsManagerAgent,
    'technical_seo_operations_manager': TechnicalSEOOperationsManagerAgent,
    'client_success_manager': ClientSuccessManagerAgent,
    'lead_qualification': LeadQualificationAgent,
    'proposal_generation': ProposalGenerationAgent,
    'sales_conversation': SalesConversationAgent,
    'technical_seo_auditor': TechnicalSEOAuditorAgent,
    'content_strategy': ContentStrategyAgent,
    'link_building': LinkBuildingAgent,
    'competitive_analysis': CompetitiveAnalysisAgent,
    'reporting': ReportingAgent
}

__version__ = "1.0.0"
__author__ = "Andrew Popov"
__email__ = "a.popov.gv@gmail.com"

__all__ = [
    # Agent classes
    'ChiefSEOStrategistAgent',
    'BusinessDevelopmentDirectorAgent',
    'TaskCoordinationAgent',
    'SalesOperationsManagerAgent',
    'TechnicalSEOOperationsManagerAgent',
    'ClientSuccessManagerAgent',
    'LeadQualificationAgent',
    'ProposalGenerationAgent',
    'SalesConversationAgent',
    'TechnicalSEOAuditorAgent',
    'ContentStrategyAgent',
    'LinkBuildingAgent',
    'CompetitiveAnalysisAgent',
    'ReportingAgent',
    
    # Agent groups
    'EXECUTIVE_AGENTS',
    'MANAGEMENT_AGENTS',
    'OPERATIONAL_AGENTS',
    'ALL_AGENTS',
    'AGENT_CLASSES',
    
    # Utility functions
    'get_agent_class',
    'get_agents_by_level',
    'get_agent_count',
    'get_agent_instance'
]

def get_agent_class(agent_id: str):
    """Получить класс агента по его ID"""
    return AGENT_CLASSES.get(agent_id)

def get_agents_by_level(level: str):
    """Получить агентов по уровню (executive/management/operational)"""
    level_map = {
        'executive': EXECUTIVE_AGENTS,
        'management': MANAGEMENT_AGENTS,
        'operational': OPERATIONAL_AGENTS
    }
    return level_map.get(level.lower(), [])

def get_agent_count():
    """Получить общее количество агентов"""
    return len(ALL_AGENTS)

def get_agent_instance(agent_id: str):
    """Создать экземпляр агента по его ID"""
    agent_class = AGENT_CLASSES.get(agent_id)
    if agent_class:
        try:
            # Создаем экземпляр агента с минимальной конфигурацией
            return agent_class()
        except Exception as e:
            print(f"Ошибка создания агента {agent_id}: {e}")
            return None
    return None