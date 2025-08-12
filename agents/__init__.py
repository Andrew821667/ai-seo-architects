"""AI SEO Architects - 35=BK 4;O 02B><0B870F88 SEO-035=BAB20

-B>B ?0:5B A>45@68B ?>;=CN :><0=4C 87 14 AI-035=B>2, >@30=87>20==KE ?> C@>2=O<:
- Executive Level (2 035=B0): AB@0B538G5A:>5 ?;0=8@>20=85 8 @0728B85 187=5A0
- Management Level (4 035=B0): :>>@48=0F8O ?@>F5AA>2 8 >?5@0F89
- Operational Level (8 035=B>2): 2K?>;=5=85 A?5F80;878@>20==KE 7040G
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

# @C??8@>2:0 ?> C@>2=O<
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

# A5 035=BK
ALL_AGENTS = EXECUTIVE_AGENTS + MANAGEMENT_AGENTS + OPERATIONAL_AGENTS

# Mapping ?> ID 035=B>2
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
    'AGENT_CLASSES'
]

def get_agent_class(agent_id: str):
    """>;CG8BL :;0AA 035=B0 ?> 53> ID"""
    return AGENT_CLASSES.get(agent_id)

def get_agents_by_level(level: str):
    """>;CG8BL 035=B>2 ?> C@>2=N (executive/management/operational)"""
    level_map = {
        'executive': EXECUTIVE_AGENTS,
        'management': MANAGEMENT_AGENTS,
        'operational': OPERATIONAL_AGENTS
    }
    return level_map.get(level.lower(), [])

def get_agent_count():
    """>;CG8BL >1I55 :>;8G5AB2> 035=B>2"""
    return len(ALL_AGENTS)