"""
Model Context Protocol (MCP) Implementation for AI SEO Architects
Стандартизированный протокол для взаимодействия AI-агентов с внешними источниками данных
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
import asyncio
import json
import aiohttp
from abc import ABC, abstractmethod

class MCPResourceType(str, Enum):
    """Типы ресурсов в MCP протоколе"""
    SEO_DATA = "seo_data"
    CLIENT_DATA = "client_data" 
    COMPETITIVE_DATA = "competitive_data"
    KEYWORD_DATA = "keyword_data"
    BACKLINK_DATA = "backlink_data"
    CONTENT_DATA = "content_data"
    TECHNICAL_AUDIT = "technical_audit"
    ANALYTICS_DATA = "analytics_data"

class MCPMethod(str, Enum):
    """Методы MCP протокола"""
    GET_RESOURCE = "get_resource"
    LIST_RESOURCES = "list_resources"
    SEARCH_RESOURCES = "search_resources"
    CREATE_RESOURCE = "create_resource"
    UPDATE_RESOURCE = "update_resource"
    DELETE_RESOURCE = "delete_resource"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"

class MCPQuery(BaseModel):
    """Стандартизированный запрос MCP"""
    method: MCPMethod
    resource_type: MCPResourceType
    resource_id: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    filters: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: str = Field(default_factory=lambda: f"req_{datetime.now().timestamp()}")

class MCPResponse(BaseModel):
    """Стандартизированный ответ MCP"""
    request_id: str
    status: str  # "success", "error", "partial"
    data: Union[Dict[str, Any], List[Dict[str, Any]], None] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    processing_time_ms: Optional[float] = None
    data_source: Optional[str] = None
    cache_hit: bool = False

class MCPCapability(BaseModel):
    """Возможности MCP сервера"""
    name: str
    version: str
    supported_methods: List[MCPMethod]
    supported_resources: List[MCPResourceType]
    authentication_required: bool = False
    rate_limit: Optional[int] = None
    description: Optional[str] = None

class MCPServerInfo(BaseModel):
    """Информация о MCP сервере"""
    name: str
    version: str
    capabilities: List[MCPCapability]
    endpoints: Dict[str, str]
    authentication: Dict[str, Any] = Field(default_factory=dict)
    health_check_url: Optional[str] = None

class MCPContext(BaseModel):
    """Контекст для MCP запросов"""
    agent_id: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    workspace_id: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)
    capabilities: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)

class MCPClient(ABC):
    """Абстрактный базовый класс для MCP клиентов"""
    
    def __init__(self, server_info: MCPServerInfo, context: MCPContext):
        self.server_info = server_info
        self.context = context
        self.session = None
        self._connection_pool = None
        
    @abstractmethod
    async def connect(self) -> bool:
        """Установка соединения с MCP сервером"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Закрытие соединения с MCP сервером"""
        pass
    
    @abstractmethod
    async def execute_query(self, query: MCPQuery) -> MCPResponse:
        """Выполнение MCP запроса"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Проверка здоровья MCP сервера"""
        pass

class HTTPMCPClient(MCPClient):
    """HTTP/REST реализация MCP клиента"""
    
    def __init__(self, server_info: MCPServerInfo, context: MCPContext):
        super().__init__(server_info, context)
        self.base_url = server_info.endpoints.get("http", "")
        self.timeout = aiohttp.ClientTimeout(total=30)
        
    async def connect(self) -> bool:
        """Установка HTTP соединения"""
        try:
            self.session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers=self._get_auth_headers()
            )
            
            # Проверяем соединение
            health_ok = await self.health_check()
            return health_ok
            
        except Exception as e:
            print(f"❌ MCP HTTP connection failed: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Закрытие HTTP соединения"""
        if self.session:
            await self.session.close()
            self.session = None
        return True
    
    async def execute_query(self, query: MCPQuery) -> MCPResponse:
        """Выполнение HTTP MCP запроса"""
        if not self.session:
            raise Exception("MCP client not connected")
        
        start_time = datetime.now()
        
        try:
            # Формируем URL и payload
            url = f"{self.base_url}/mcp/v1/{query.method.value}"
            payload = {
                "resource_type": query.resource_type.value,
                "resource_id": query.resource_id,
                "parameters": query.parameters,
                "filters": query.filters,
                "context": query.context,
                "agent_context": {
                    "agent_id": self.context.agent_id,
                    "session_id": self.context.session_id,
                    "capabilities": self.context.capabilities
                }
            }
            
            # Выполняем запрос
            async with self.session.post(url, json=payload) as response:
                response_data = await response.json()
                
                processing_time = (datetime.now() - start_time).total_seconds() * 1000
                
                if response.status == 200:
                    return MCPResponse(
                        request_id=query.request_id,
                        status="success",
                        data=response_data.get("data"),
                        metadata=response_data.get("metadata", {}),
                        processing_time_ms=processing_time,
                        data_source=response_data.get("source", "unknown"),
                        cache_hit=response_data.get("cache_hit", False)
                    )
                else:
                    return MCPResponse(
                        request_id=query.request_id,
                        status="error",
                        error_message=response_data.get("error", "Unknown error"),
                        error_code=str(response.status),
                        processing_time_ms=processing_time
                    )
                    
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            return MCPResponse(
                request_id=query.request_id,
                status="error",
                error_message=str(e),
                error_code="client_error",
                processing_time_ms=processing_time
            )
    
    async def health_check(self) -> bool:
        """HTTP health check"""
        if not self.session:
            return False
            
        try:
            health_url = self.server_info.health_check_url or f"{self.base_url}/health"
            async with self.session.get(health_url) as response:
                return response.status == 200
        except:
            return False
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Получение заголовков аутентификации"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"AI-SEO-Architects-MCP-Client/1.0 (Agent: {self.context.agent_id})"
        }
        
        auth_config = self.server_info.authentication
        if auth_config.get("type") == "bearer_token":
            headers["Authorization"] = f"Bearer {auth_config.get('token')}"
        elif auth_config.get("type") == "api_key":
            headers["X-API-Key"] = auth_config.get("api_key")
            
        return headers

class WebSocketMCPClient(MCPClient):
    """WebSocket реализация MCP клиента для real-time данных"""
    
    def __init__(self, server_info: MCPServerInfo, context: MCPContext):
        super().__init__(server_info, context)
        self.ws_url = server_info.endpoints.get("websocket", "")
        self.websocket = None
        self.subscriptions = set()
        
    async def connect(self) -> bool:
        """Установка WebSocket соединения"""
        try:
            import websockets
            
            headers = self._get_auth_headers()
            self.websocket = await websockets.connect(
                self.ws_url, 
                extra_headers=headers,
                ping_interval=20,
                ping_timeout=10
            )
            
            # Отправляем handshake
            handshake = {
                "type": "handshake",
                "agent_id": self.context.agent_id,
                "capabilities": self.context.capabilities,
                "version": "1.0"
            }
            
            await self.websocket.send(json.dumps(handshake))
            response = await self.websocket.recv()
            response_data = json.loads(response)
            
            return response_data.get("status") == "connected"
            
        except Exception as e:
            print(f"❌ MCP WebSocket connection failed: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Закрытие WebSocket соединения"""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        return True
    
    async def execute_query(self, query: MCPQuery) -> MCPResponse:
        """Выполнение WebSocket MCP запроса"""
        if not self.websocket:
            raise Exception("MCP WebSocket client not connected")
        
        start_time = datetime.now()
        
        try:
            # Отправляем запрос
            message = {
                "type": "query",
                "request_id": query.request_id,
                "method": query.method.value,
                "resource_type": query.resource_type.value,
                "resource_id": query.resource_id,
                "parameters": query.parameters,
                "filters": query.filters,
                "context": query.context
            }
            
            await self.websocket.send(json.dumps(message))
            
            # Ждем ответ
            response_raw = await self.websocket.recv()
            response_data = json.loads(response_raw)
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            if response_data.get("status") == "success":
                return MCPResponse(
                    request_id=query.request_id,
                    status="success",
                    data=response_data.get("data"),
                    metadata=response_data.get("metadata", {}),
                    processing_time_ms=processing_time,
                    data_source=response_data.get("source", "websocket"),
                    cache_hit=response_data.get("cache_hit", False)
                )
            else:
                return MCPResponse(
                    request_id=query.request_id,
                    status="error",
                    error_message=response_data.get("error", "Unknown error"),
                    error_code=response_data.get("error_code", "ws_error"),
                    processing_time_ms=processing_time
                )
                
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            return MCPResponse(
                request_id=query.request_id,
                status="error",
                error_message=str(e),
                error_code="websocket_error",
                processing_time_ms=processing_time
            )
    
    async def health_check(self) -> bool:
        """WebSocket health check"""
        if not self.websocket:
            return False
            
        try:
            ping_message = {"type": "ping", "timestamp": datetime.now().isoformat()}
            await self.websocket.send(json.dumps(ping_message))
            
            # Ждем pong в течение 5 секунд
            response = await asyncio.wait_for(self.websocket.recv(), timeout=5.0)
            response_data = json.loads(response)
            
            return response_data.get("type") == "pong"
            
        except:
            return False
    
    async def subscribe(self, resource_type: MCPResourceType, filters: Dict[str, Any] = None) -> bool:
        """Подписка на real-time обновления"""
        if not self.websocket:
            return False
        
        try:
            subscribe_message = {
                "type": "subscribe",
                "resource_type": resource_type.value,
                "filters": filters or {},
                "agent_id": self.context.agent_id
            }
            
            await self.websocket.send(json.dumps(subscribe_message))
            self.subscriptions.add(resource_type)
            return True
            
        except Exception as e:
            print(f"❌ MCP subscription failed: {e}")
            return False
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Получение заголовков для WebSocket аутентификации"""
        headers = {}
        
        auth_config = self.server_info.authentication
        if auth_config.get("type") == "bearer_token":
            headers["Authorization"] = f"Bearer {auth_config.get('token')}"
        elif auth_config.get("type") == "api_key":
            headers["X-API-Key"] = auth_config.get("api_key")
            
        return headers

class MCPClientFactory:
    """Factory для создания MCP клиентов"""
    
    @staticmethod
    def create_client(server_info: MCPServerInfo, context: MCPContext, 
                     client_type: str = "http") -> MCPClient:
        """Создание MCP клиента"""
        
        if client_type == "http":
            return HTTPMCPClient(server_info, context)
        elif client_type == "websocket":
            return WebSocketMCPClient(server_info, context)
        else:
            raise ValueError(f"Unsupported MCP client type: {client_type}")

# Удобные константы для популярных MCP серверов
ANTHROPIC_MCP_SERVER = MCPServerInfo(
    name="anthropic_mcp",
    version="1.0",
    endpoints={
        "http": "https://api.anthropic.com/mcp/v1",
        "websocket": "wss://api.anthropic.com/mcp/v1/ws"
    },
    capabilities=[
        MCPCapability(
            name="seo_analysis",
            version="1.0",
            supported_methods=[MCPMethod.GET_RESOURCE, MCPMethod.SEARCH_RESOURCES],
            supported_resources=[MCPResourceType.SEO_DATA, MCPResourceType.CONTENT_DATA],
            authentication_required=True
        )
    ],
    authentication={"type": "bearer_token", "token": "${ANTHROPIC_API_KEY}"},
    health_check_url="https://api.anthropic.com/health"
)

OPENAI_MCP_SERVER = MCPServerInfo(
    name="openai_mcp", 
    version="1.0",
    endpoints={
        "http": "https://api.openai.com/mcp/v1"
    },
    capabilities=[
        MCPCapability(
            name="content_analysis",
            version="1.0", 
            supported_methods=[MCPMethod.GET_RESOURCE, MCPMethod.CREATE_RESOURCE],
            supported_resources=[MCPResourceType.CONTENT_DATA, MCPResourceType.KEYWORD_DATA],
            authentication_required=True
        )
    ],
    authentication={"type": "bearer_token", "token": "${OPENAI_API_KEY}"}
)