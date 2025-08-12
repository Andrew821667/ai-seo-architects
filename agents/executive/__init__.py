"""Executive level agents for strategic decision making.

Этот пакет содержит агентов высшего уровня для стратегического
планирования и принятия ключевых бизнес-решений.

Агенты:
- ChiefSEOStrategistAgent: Главный SEO стратег
- BusinessDevelopmentDirectorAgent: Директор по развитию бизнеса
"""

from .chief_seo_strategist import ChiefSEOStrategistAgent
from .business_development_director import BusinessDevelopmentDirectorAgent

__all__ = [
    'ChiefSEOStrategistAgent',
    'BusinessDevelopmentDirectorAgent'
]
