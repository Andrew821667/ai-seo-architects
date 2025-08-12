"""Knowledge Base - 070 7=0=89 4;O AI SEO Architects

-B>B ?0:5B A>45@68B AB@C:BC@8@>20==CN 107C 7=0=89 4;O 2A5E 14 035=B>2:

!B@C:BC@0 ?> C@>2=O<:
- executive/: =0=8O 4;O AB@0B538G5A:>3> C@>2=O (2 035=B0)
- management/: =0=8O 4;O C?@02;5=G5A:>3> C@>2=O (4 035=B0)
- operational/: =0=8O 4;O >?5@0F8>==>3> C@>2=O (8 035=B>2)

064K9 D09; 7=0=89 A>45@68B:
- ?8A0=85 @>;8 8 >B25BAB25==>AB8 035=B0
- @>D5AA8>=0;L=K5 :><?5B5=F88
- ?B8<0;L=K5 ?@>F5AAK 8 <5B>4>;>388
- @0:B8G5A:85 A?@02>G=8:8 8 H01;>=K
-  >AA89A:CN A?5F8D8:C @K=:0
"""

from .knowledge_manager import KnowledgeManager

# 0??8=3 035=B>2 =0 D09;K 7=0=89
KNOWLEDGE_MAPPING = {
    # Executive Level
    'chief_seo_strategist': 'executive/chief_seo_strategist.md',
    'business_development_director': 'executive/business_development_director.md',
    
    # Management Level
    'task_coordination': 'management/task_coordination.md',
    'sales_operations_manager': 'management/sales_operations_manager.md',
    'technical_seo_operations_manager': 'management/technical_seo_operations_manager.md',
    'client_success_manager': 'management/client_success_manager.md',
    
    # Operational Level
    'lead_qualification': 'operational/lead_qualification.md',
    'proposal_generation': 'operational/proposal_generation.md',
    'sales_conversation': 'operational/sales_conversation.md',
    'technical_seo_auditor': 'operational/technical_seo_auditor.md',
    'content_strategy': 'operational/content_strategy.md',
    'link_building': 'operational/link_building.md',
    'competitive_analysis': 'operational/competitive_analysis.md',
    'reporting': 'operational/reporting.md'
}

# !B0B8AB8:0 107K 7=0=89
KNOWLEDGE_STATS = {
    'total_agents': 14,
    'executive_agents': 2,
    'management_agents': 4,
    'operational_agents': 8,
    'knowledge_files': len(KNOWLEDGE_MAPPING),
    'language': 'Russian',
    'format': 'Markdown',
    'encoding': 'UTF-8'
}

__version__ = "1.0.0"
__knowledge_version__ = "2024.08"  # 5@A8O 107K 7=0=89

__all__ = [
    'KnowledgeManager',
    'KNOWLEDGE_MAPPING',
    'KNOWLEDGE_STATS',
    'get_knowledge_path',
    'get_agent_knowledge',
    'validate_knowledge_base'
]

def get_knowledge_path(agent_id: str) -> str:
    """>;CG8BL ?CBL : D09;C 7=0=89 035=B0"""
    import os
    knowledge_dir = os.path.dirname(__file__)
    relative_path = KNOWLEDGE_MAPPING.get(agent_id)
    if relative_path:
        return os.path.join(knowledge_dir, relative_path)
    return None

def get_agent_knowledge(agent_id: str) -> str:
    """>;CG8BL A>45@68<>5 107K 7=0=89 035=B0"""
    knowledge_path = get_knowledge_path(agent_id)
    if knowledge_path and os.path.exists(knowledge_path):
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def validate_knowledge_base() -> dict:
    """@>25@8BL F5;>AB=>ABL 107K 7=0=89"""
    import os
    
    results = {
        'valid': True,
        'missing_files': [],
        'total_files': len(KNOWLEDGE_MAPPING),
        'existing_files': 0,
        'file_sizes': {}
    }
    
    for agent_id, relative_path in KNOWLEDGE_MAPPING.items():
        knowledge_path = get_knowledge_path(agent_id)
        if knowledge_path and os.path.exists(knowledge_path):
            results['existing_files'] += 1
            results['file_sizes'][agent_id] = os.path.getsize(knowledge_path)
        else:
            results['valid'] = False
            results['missing_files'].append(agent_id)
    
    return results