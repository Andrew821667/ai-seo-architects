"""
MCP Data Provider для AI SEO Architects
Унифицированный доступ к данным через Model Context Protocol
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import asyncio
import json
from core.mcp.protocol import (
    MCPClient, MCPQuery, MCPResponse, MCPContext, MCPServerInfo,
    MCPResourceType, MCPMethod, MCPClientFactory
)
from core.interfaces.data_models import SEOData, ClientData, CompetitiveData

class MCPDataProvider:
    """
    Основной провайдер данных через MCP протокол
    Обеспечивает унифицированный доступ к различным источникам данных
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.clients: Dict[str, MCPClient] = {}
        self.cache: Dict[str, Any] = {}
        self.cache_ttl = timedelta(minutes=config.get("cache_ttl_minutes", 30))
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "errors": 0,
            "response_times": []
        }
        
    async def initialize(self) -> bool:
        """Инициализация всех MCP клиентов"""
        try:
            servers = self.config.get("mcp_servers", {})
            
            for server_name, server_config in servers.items():
                # Создаем server info
                server_info = MCPServerInfo(
                    name=server_config["name"],
                    version=server_config.get("version", "1.0"),
                    endpoints=server_config["endpoints"],
                    authentication=server_config.get("authentication", {}),
                    health_check_url=server_config.get("health_check_url"),
                    capabilities=[]  # Будем получать динамически
                )
                
                # Создаем контекст
                context = MCPContext(
                    agent_id=f"ai_seo_architects_{server_name}",
                    capabilities=["seo_analysis", "content_analysis", "competitive_analysis"]
                )
                
                # Создаем и подключаем клиент
                client_type = server_config.get("client_type", "http")
                client = MCPClientFactory.create_client(server_info, context, client_type)
                
                if await client.connect():
                    self.clients[server_name] = client
                    print(f"✅ MCP client '{server_name}' подключен")
                else:
                    print(f"❌ Не удалось подключить MCP client '{server_name}'")
                    
            return len(self.clients) > 0
            
        except Exception as e:
            print(f"❌ Ошибка инициализации MCP: {e}")
            return False
    
    async def get_seo_data(self, domain: str, parameters: Dict[str, Any] = None) -> SEOData:
        """Получение SEO данных через MCP"""
        
        cache_key = f"seo_data:{domain}:{hash(str(parameters))}"
        
        # Проверяем кэш
        if self._check_cache(cache_key):
            self.stats["cache_hits"] += 1
            cached_data = self.cache[cache_key]["data"]
            return self._convert_to_seo_data(cached_data, domain)
        
        start_time = datetime.now()
        self.stats["total_requests"] += 1
        
        try:
            # Определяем лучший MCP сервер для SEO данных
            best_client = self._select_best_client_for_resource(MCPResourceType.SEO_DATA)
            
            if not best_client:
                raise Exception("Нет доступных MCP серверов для SEO данных")
            
            # Формируем MCP запрос
            query = MCPQuery(
                method=MCPMethod.GET_RESOURCE,
                resource_type=MCPResourceType.SEO_DATA,
                resource_id=domain,
                parameters=parameters or {},
                context={
                    "analysis_type": "comprehensive",
                    "include_technical": True,
                    "include_content": True,
                    "include_performance": True
                }
            )
            
            # Выполняем запрос
            response = await best_client.execute_query(query)
            
            # Обрабатываем ответ
            if response.status == "success":
                # Кэшируем результат
                self._cache_result(cache_key, response.data)
                
                # Конвертируем в наш формат
                seo_data = self._convert_to_seo_data(response.data, domain)
                seo_data.source = f"mcp:{best_client.server_info.name}"
                seo_data.api_cost = self._calculate_api_cost(response)
                
                # Обновляем статистику
                processing_time = (datetime.now() - start_time).total_seconds()
                self.stats["response_times"].append(processing_time)
                
                return seo_data
            else:
                raise Exception(f"MCP error: {response.error_message}")
                
        except Exception as e:
            self.stats["errors"] += 1
            print(f"❌ Ошибка получения SEO данных через MCP: {e}")
            
            # Fallback на mock данные
            return self._create_fallback_seo_data(domain)
    
    async def get_client_data(self, client_id: str, parameters: Dict[str, Any] = None) -> ClientData:
        """Получение клиентских данных через MCP"""
        
        cache_key = f"client_data:{client_id}:{hash(str(parameters))}"
        
        if self._check_cache(cache_key):
            self.stats["cache_hits"] += 1
            cached_data = self.cache[cache_key]["data"]
            return self._convert_to_client_data(cached_data, client_id)
        
        start_time = datetime.now()
        self.stats["total_requests"] += 1
        
        try:
            best_client = self._select_best_client_for_resource(MCPResourceType.CLIENT_DATA)
            
            if not best_client:
                raise Exception("Нет доступных MCP серверов для клиентских данных")
            
            query = MCPQuery(
                method=MCPMethod.GET_RESOURCE,
                resource_type=MCPResourceType.CLIENT_DATA,
                resource_id=client_id,
                parameters=parameters or {},
                context={
                    "include_history": True,
                    "include_analytics": True,
                    "include_contacts": True
                }
            )
            
            response = await best_client.execute_query(query)
            
            if response.status == "success":
                self._cache_result(cache_key, response.data)
                
                client_data = self._convert_to_client_data(response.data, client_id)
                client_data.source = f"mcp:{best_client.server_info.name}"
                
                processing_time = (datetime.now() - start_time).total_seconds()
                self.stats["response_times"].append(processing_time)
                
                return client_data
            else:
                raise Exception(f"MCP error: {response.error_message}")
                
        except Exception as e:
            self.stats["errors"] += 1
            print(f"❌ Ошибка получения клиентских данных через MCP: {e}")
            
            return self._create_fallback_client_data(client_id)
    
    async def get_competitive_data(self, domain: str, competitors: List[str], 
                                 parameters: Dict[str, Any] = None) -> CompetitiveData:
        """Получение конкурентных данных через MCP"""
        
        cache_key = f"competitive_data:{domain}:{hash(str(competitors))}:{hash(str(parameters))}"
        
        if self._check_cache(cache_key):
            self.stats["cache_hits"] += 1
            cached_data = self.cache[cache_key]["data"]
            return self._convert_to_competitive_data(cached_data, domain, competitors)
        
        start_time = datetime.now()
        self.stats["total_requests"] += 1
        
        try:
            best_client = self._select_best_client_for_resource(MCPResourceType.COMPETITIVE_DATA)
            
            if not best_client:
                raise Exception("Нет доступных MCP серверов для конкурентных данных")
            
            query = MCPQuery(
                method=MCPMethod.GET_RESOURCE,
                resource_type=MCPResourceType.COMPETITIVE_DATA,
                resource_id=domain,
                parameters={
                    "competitors": competitors,
                    **(parameters or {})
                },
                context={
                    "analysis_depth": "comprehensive",
                    "include_keywords": True,
                    "include_backlinks": True,
                    "include_content_gaps": True
                }
            )
            
            response = await best_client.execute_query(query)
            
            if response.status == "success":
                self._cache_result(cache_key, response.data)
                
                competitive_data = self._convert_to_competitive_data(
                    response.data, domain, competitors
                )
                competitive_data.source = f"mcp:{best_client.server_info.name}"
                
                processing_time = (datetime.now() - start_time).total_seconds()
                self.stats["response_times"].append(processing_time)
                
                return competitive_data
            else:
                raise Exception(f"MCP error: {response.error_message}")
                
        except Exception as e:
            self.stats["errors"] += 1
            print(f"❌ Ошибка получения конкурентных данных через MCP: {e}")
            
            return self._create_fallback_competitive_data(domain, competitors)
    
    async def search_resources(self, resource_type: MCPResourceType, 
                             search_query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Поиск ресурсов через MCP"""
        
        try:
            best_client = self._select_best_client_for_resource(resource_type)
            
            if not best_client:
                return []
            
            query = MCPQuery(
                method=MCPMethod.SEARCH_RESOURCES,
                resource_type=resource_type,
                parameters={"query": search_query},
                filters=filters or {},
                context={"max_results": 50}
            )
            
            response = await best_client.execute_query(query)
            
            if response.status == "success" and isinstance(response.data, list):
                return response.data
            else:
                return []
                
        except Exception as e:
            print(f"❌ Ошибка поиска ресурсов через MCP: {e}")
            return []
    
    async def health_check(self) -> Dict[str, Any]:
        """Проверка здоровья всех MCP клиентов"""
        
        health_status = {}
        
        for client_name, client in self.clients.items():
            try:
                is_healthy = await client.health_check()
                health_status[client_name] = {
                    "status": "healthy" if is_healthy else "unhealthy",
                    "server": client.server_info.name,
                    "version": client.server_info.version,
                    "last_check": datetime.now().isoformat()
                }
            except Exception as e:
                health_status[client_name] = {
                    "status": "error",
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
        
        return {
            "overall_health": "healthy" if all(
                status["status"] == "healthy" for status in health_status.values()
            ) else "degraded",
            "clients": health_status,
            "stats": self.get_stats()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики провайдера"""
        
        avg_response_time = (
            sum(self.stats["response_times"]) / len(self.stats["response_times"])
            if self.stats["response_times"] else 0
        )
        
        cache_hit_rate = (
            self.stats["cache_hits"] / max(1, self.stats["total_requests"])
        )
        
        error_rate = (
            self.stats["errors"] / max(1, self.stats["total_requests"])
        )
        
        return {
            "total_requests": self.stats["total_requests"],
            "cache_hit_rate": cache_hit_rate,
            "error_rate": error_rate,
            "average_response_time_seconds": avg_response_time,
            "active_clients": len(self.clients),
            "cache_size": len(self.cache)
        }
    
    def _select_best_client_for_resource(self, resource_type: MCPResourceType) -> Optional[MCPClient]:
        """Выбор лучшего MCP клиента для типа ресурса"""
        
        # Простая логика выбора - можно усложнить
        for client_name, client in self.clients.items():
            for capability in client.server_info.capabilities:
                if resource_type in capability.supported_resources:
                    return client
        
        # Если специализированного клиента нет, возвращаем первый доступный
        return next(iter(self.clients.values())) if self.clients else None
    
    def _check_cache(self, cache_key: str) -> bool:
        """Проверка кэша"""
        
        if cache_key not in self.cache:
            return False
        
        cached_item = self.cache[cache_key]
        cache_age = datetime.now() - cached_item["timestamp"]
        
        if cache_age > self.cache_ttl:
            del self.cache[cache_key]
            return False
        
        return True
    
    def _cache_result(self, cache_key: str, data: Any):
        """Кэширование результата"""
        
        self.cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now()
        }
        
        # Простая очистка кэша по размеру
        if len(self.cache) > 1000:
            # Удаляем 20% самых старых записей
            sorted_items = sorted(
                self.cache.items(), 
                key=lambda x: x[1]["timestamp"]
            )
            
            items_to_remove = int(len(sorted_items) * 0.2)
            for i in range(items_to_remove):
                del self.cache[sorted_items[i][0]]
    
    def _calculate_api_cost(self, response: MCPResponse) -> float:
        """Расчет стоимости API запроса"""
        
        # Базовая стоимость на основе времени обработки
        base_cost = (response.processing_time_ms or 0) / 1000 * 0.001  # $0.001 за секунду
        
        # Дополнительная стоимость в зависимости от источника данных
        if response.data_source and "premium" in response.data_source:
            base_cost *= 3
            
        return round(base_cost, 6)
    
    def _convert_to_seo_data(self, mcp_data: Dict[str, Any], domain: str) -> SEOData:
        """Конвертация MCP данных в SEOData"""
        
        return SEOData(
            domain=domain,
            source="mcp",
            timestamp=datetime.now(),
            crawl_data=mcp_data.get("crawl_data", {}),
            technical_issues=mcp_data.get("technical_issues", []),
            page_speed=mcp_data.get("page_speed", {}),
            mobile_friendly=mcp_data.get("mobile_friendly", {}),
            content_analysis=mcp_data.get("content_analysis", {}),
            keyword_data=mcp_data.get("keyword_data", {}),
            eeat_score=mcp_data.get("eeat_score", {}),
            rankings=mcp_data.get("rankings", []),
            backlinks=mcp_data.get("backlinks", []),
            confidence_score=mcp_data.get("confidence_score", 0.8)
        )
    
    def _convert_to_client_data(self, mcp_data: Dict[str, Any], client_id: str) -> ClientData:
        """Конвертация MCP данных в ClientData"""
        
        return ClientData(
            client_id=client_id,
            source="mcp",
            company_info=mcp_data.get("company_info", {}),
            contacts=mcp_data.get("contacts", []),
            industry_data=mcp_data.get("industry_data", {}),
            active_projects=mcp_data.get("active_projects", []),
            budget_info=mcp_data.get("budget_info", {}),
            service_history=mcp_data.get("service_history", []),
            pipeline_stage=mcp_data.get("pipeline_stage", "unknown"),
            lead_score=mcp_data.get("lead_score", 50),
            conversion_probability=mcp_data.get("conversion_probability", 0.5)
        )
    
    def _convert_to_competitive_data(self, mcp_data: Dict[str, Any], 
                                   domain: str, competitors: List[str]) -> CompetitiveData:
        """Конвертация MCP данных в CompetitiveData"""
        
        return CompetitiveData(
            domain=domain,
            competitors=competitors,
            source="mcp",
            ranking_comparison=mcp_data.get("ranking_comparison", {}),
            keyword_overlap=mcp_data.get("keyword_overlap", {}),
            backlink_comparison=mcp_data.get("backlink_comparison", {}),
            content_gaps=mcp_data.get("content_gaps", [])
        )
    
    # Fallback методы для создания базовых данных при недоступности MCP
    def _create_fallback_seo_data(self, domain: str) -> SEOData:
        """Создание fallback SEO данных"""
        
        return SEOData(
            domain=domain,
            source="fallback",
            timestamp=datetime.now(),
            crawl_data={"status": "fallback_mode", "pages_crawled": 0},
            confidence_score=0.3
        )
    
    def _create_fallback_client_data(self, client_id: str) -> ClientData:
        """Создание fallback клиентских данных"""
        
        return ClientData(
            client_id=client_id,
            source="fallback",
            company_info={"name": f"Client {client_id}", "status": "fallback_mode"},
            data_quality_score=0.3
        )
    
    def _create_fallback_competitive_data(self, domain: str, competitors: List[str]) -> CompetitiveData:
        """Создание fallback конкурентных данных"""
        
        return CompetitiveData(
            domain=domain,
            competitors=competitors,
            source="fallback",
            ranking_comparison={"status": "fallback_mode"}
        )
    
    async def close(self):
        """Закрытие всех MCP соединений"""
        
        for client_name, client in self.clients.items():
            try:
                await client.disconnect()
                print(f"✅ MCP client '{client_name}' отключен")
            except Exception as e:
                print(f"❌ Ошибка отключения MCP client '{client_name}': {e}")
        
        self.clients.clear()
        self.cache.clear()

# Конфигурация по умолчанию для MCP провайдера
DEFAULT_MCP_CONFIG = {
    "cache_ttl_minutes": 30,
    "mcp_servers": {
        "anthropic": {
            "name": "anthropic_mcp",
            "version": "1.0",
            "client_type": "http",
            "endpoints": {
                "http": "https://api.anthropic.com/mcp/v1"
            },
            "authentication": {
                "type": "bearer_token",
                "token": "${ANTHROPIC_API_KEY}"
            },
            "health_check_url": "https://api.anthropic.com/health"
        },
        "openai": {
            "name": "openai_mcp",
            "version": "1.0", 
            "client_type": "http",
            "endpoints": {
                "http": "https://api.openai.com/mcp/v1"
            },
            "authentication": {
                "type": "bearer_token",
                "token": "${OPENAI_API_KEY}"
            }
        }
    }
}