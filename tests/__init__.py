"""Tests - "5AB>20O A8AB5<0 4;O AI SEO Architects

-B>B ?0:5B A>45@68B ?>;=CN B5AB>2CN A8AB5<C:

!B@C:BC@0:
- unit/: .=8B-B5ABK 4;O >B45;L=KE :><?>=5=B>2
- integration/: =B53@0F8>==K5 B5ABK
- fixtures/: "5AB>2K5 40==K5 8 <>:8
- conftest.py: >=D83C@0F8O pytest

"5AB>2>5 ?>:@KB85:
- 14/14 035=B>2 ?>:@KB> B5AB0<8
- API endpoints B5AB8@>20=85
- MCP 8=B53@0F8>==>5 B5AB8@>20=85
- Docker 8=D@0AB@C:BC@0 B5ABK
"""

import os
import sys

# >102;O5< :>@=52CN 48@5:B>@8N 2 PYTHONPATH
test_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(test_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 1I85 B5AB>2K5 :>=D83C@0F88
TEST_CONFIG = {
    'environment': 'test',
    'debug': True,
    'log_level': 'DEBUG',
    'database_url': 'sqlite:///:memory:',
    'redis_url': 'redis://localhost:6379/15',  # test database
    'enable_mock_data': True,
    'test_timeout': 30,
    'agent_test_timeout': 10
}

# >:8 4;O 2=5H=8E A5@28A>2
MOCK_SERVICES = {
    'openai_api': True,
    'anthropic_api': True,
    'external_apis': True,
    'file_system': False,  # A?>;L7C5< @50;L=CN D09;>2CN A8AB5<C
    'database': False      # A?>;L7C5< in-memory SQLite
}

__version__ = "1.0.0"
__test_coverage__ = "85%+"  # &5;52>5 ?>:@KB85

__all__ = [
    'TEST_CONFIG',
    'MOCK_SERVICES',
    'setup_test_environment',
    'cleanup_test_environment',
    'get_test_config'
]

def setup_test_environment():
    """0AB@>9:0 B5AB>2>9 A@54K"""
    # #AB0=02;8205< ?5@5<5==K5 >:@C65=8O 4;O B5AB>2
    for key, value in TEST_CONFIG.items():
        os.environ[key.upper()] = str(value)
    
    # B:;NG05< ;>38@>20=85 2 B5AB0E
    import logging
    logging.getLogger().setLevel(logging.CRITICAL)
    
    print(" "5AB>20O A@540 =0AB@>5=0")

def cleanup_test_environment():
    """G8AB:0 ?>A;5 B5AB>2"""
    # G8I05< 2@5<5==K5 D09;K
    import tempfile
    import shutil
    
    temp_dir = tempfile.gettempdir()
    for item in os.listdir(temp_dir):
        if item.startswith('ai_seo_test_'):
            item_path = os.path.join(temp_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    
    print(" "5AB>20O A@540 >G8I5=0")

def get_test_config(key: str = None):
    """>;CG8BL B5AB>2CN :>=D83C@0F8N"""
    if key:
        return TEST_CONFIG.get(key)
    return TEST_CONFIG.copy()