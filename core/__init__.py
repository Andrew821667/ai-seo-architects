"""Core AI SEO Architects - A=>2=K5 :><?>=5=BK A8AB5<K

-B>B ?0:5B A>45@68B 107>2CN 0@E8B5:BC@C 4;O:
- 07>2K5 :;0AAK 035=B>2
- @>20945@K 40==KE
- MCP (Model Context Protocol) 8=B53@0F8N
- @:5AB@0F8N @01>BK 035=B>2
- >45;8 40==KE 8 8=B5@D59AK
"""

from .base_agent import BaseAgent
from .orchestrator import AgentOrchestrator
from .config import load_config, get_config
from .data_providers.static_provider import StaticDataProvider
from .data_providers.factory import DataProviderFactory
from .mcp.agent_manager import MCPAgentManager, get_mcp_agent_manager
from .mcp.data_provider import MCPDataProvider
from .interfaces.data_models import AgentTask, AgentResponse, TaskType, AgentState

__version__ = "1.0.0"
__author__ = "Andrew Popov"
__email__ = "a.popov.gv@gmail.com"

__all__ = [
    # A=>2=K5 :;0AAK
    'BaseAgent',
    'AgentOrchestrator',
    'MCPAgentManager',
    
    # @>20945@K 40==KE
    'StaticDataProvider',
    'MCPDataProvider',
    'DataProviderFactory',
    
    # >45;8 40==KE
    'AgentTask',
    'AgentResponse',
    'TaskType',
    'AgentState',
    
    # >=D83C@0F8O
    'load_config',
    'get_config',
    
    # $01@8G=K5 <5B>4K
    'get_mcp_agent_manager'
]