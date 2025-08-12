"""Interfaces - =B5@D59AK 8 <>45;8 40==KE

-B>B ?0:5B >?@545;O5B >1I85 AB@C:BC@K 40==KE 8 8=B5@D59AK:

- >45;8 7040G (AgentTask, AgentResponse)
- "8?K 7040G (TaskType)
- !>AB>O=8O 035=B>2 (AgentState)
- >45;8 :>=D83C@0F88
"""

from .data_models import (
    AgentTask,
    AgentResponse,
    TaskType,
    AgentState,
    AgentPerformance,
    TaskStatus,
    TaskResult,
    MetricsData,
    ConfigModel
)

__all__ = [
    'AgentTask',
    'AgentResponse',
    'TaskType',
    'AgentState',
    'AgentPerformance',
    'TaskStatus',
    'TaskResult',
    'MetricsData',
    'ConfigModel'
]