"""
Mock Data Provider для тестирования агентов
Предоставляет фиктивные данные для SEO и клиентской информации
"""

from typing import Dict, Any, Optional
from datetime import datetime
import random

class MockSEOData:
    """Mock класс для SEO данных"""
    
    def __init__(self, domain: str):
        self.domain = domain
        self.content_analysis = {
            "title_tags": 25,
            "meta_descriptions": 20,
            "h1_tags": 30,
            "content_quality": "medium",
            "keyword_density": 0.02
        }
        self.crawl_data = {
            "pages_crawled": random.randint(10, 500),
            "errors_found": random.randint(0, 20),
            "load_time": random.uniform(1.0, 5.0)
        }

class MockClientData:
    """Mock класс для клиентских данных"""
    
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.source = "mock_provider"
        self.company_info = {
            "name": f"Test Company {client_id}",
            "industry": random.choice(["fintech", "ecommerce", "b2b_services"]),
            "size": random.choice(["small", "medium", "large"])
        }
        self.lead_score = random.randint(50, 95)

class MockDataProvider:
    """Mock Data Provider для тестирования"""
    
    def __init__(self):
        self.name = "MockDataProvider"
        self.calls_count = 0
        self.success_count = 0
    
    async def get_seo_data(self, domain: str) -> MockSEOData:
        """Получение mock SEO данных"""
        self.calls_count += 1
        self.success_count += 1
        return MockSEOData(domain)
    
    async def get_client_data(self, client_id: str) -> MockClientData:
        """Получение mock клиентских данных"""
        self.calls_count += 1
        self.success_count += 1
        return MockClientData(client_id)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Метрики провайдера"""
        return {
            "calls_total": self.calls_count,
            "success_rate": self.success_count / max(1, self.calls_count),
            "cache_hit_rate": 0.8  # Mock значение
        }