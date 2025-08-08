"""
FastAPI Backend для AI SEO Architects
Основной API сервер с REST endpoints и WebSocket поддержкой
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import asyncio
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import logging
import os

from .monitoring.logger import setup_structured_logging, get_logger
from .monitoring.metrics import MetricsCollector, get_metrics
from .routes import agents, campaigns, clients, analytics, auth, tasks
from .websocket.manager import ConnectionManager
from .auth.security import get_current_user
from .models.responses import APIResponse, HealthResponse
from .database.connection import init_database, close_database, db_manager
from .database.redis_client import init_redis, close_redis, redis_manager
from core.mcp.agent_manager import get_mcp_agent_manager
from core.base_agent import BaseAgent

# Настройка логирования
setup_structured_logging()
logger = get_logger(__name__)

# Глобальные объекты
connection_manager = ConnectionManager()
metrics_collector = MetricsCollector()
agent_manager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    
    # Startup
    logger.info("🚀 Запуск AI SEO Architects API Server...")
    
    global agent_manager
    try:
        # Инициализация баз данных
        await init_database()
        logger.info("✅ PostgreSQL инициализирован")
        
        await init_redis()
        logger.info("✅ Redis инициализирован")
        
        # Инициализация MCP менеджера агентов
        agent_manager = await get_mcp_agent_manager()
        logger.info("✅ MCP Agent Manager инициализирован")
        
        # Создаем всех 14 агентов с MCP интеграцией
        agents = await agent_manager.create_all_agents(enable_mcp=True)
        
        # Проверяем health check всех агентов
        health_results = await agent_manager.health_check_all_agents()
        healthy_agents = health_results.get("summary", {}).get("healthy_agents", 0)
        
        logger.info(f"✅ Создано {len(agents)} агентов, здоровых: {healthy_agents}")
        
        # Устанавливаем глобальную ссылку для доступа из API роутов
        app.state.agent_manager = agent_manager
        
        # Запускаем сбор метрик
        asyncio.create_task(metrics_collector.start_collection())
        logger.info("✅ Система метрик запущена")
        
        logger.info("🎉 API Server готов к работе!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🔄 Завершение работы API Server...")
    
    if agent_manager:
        await agent_manager.shutdown()
        logger.info("✅ Agent Manager завершил работу")
    
    await close_redis()
    logger.info("✅ Redis отключен")
    
    await close_database()
    logger.info("✅ PostgreSQL отключен")
    
    await metrics_collector.stop_collection()
    logger.info("✅ Система метрик остановлена")
    
    logger.info("👋 API Server завершил работу")


# Создание FastAPI приложения
app = FastAPI(
    title="AI SEO Architects API",
    description="Enterprise-ready мультиагентная система для автоматизации SEO-агентства",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы для дашборда
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Health Check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка состояния API сервера и инфраструктуры"""
    
    try:
        # Проверяем состояние баз данных
        db_healthy = await db_manager.health_check() if db_manager else False
        redis_healthy = await redis_manager.health_check() if redis_manager else False
        
        # Проверяем состояние агент-менеджера и MCP интеграций
        manager_healthy = agent_manager is not None and len(agent_manager.agents) > 0
        
        # Проверяем состояние всех 14 агентов
        agents_status = {}
        if agent_manager:
            try:
                health_results = await agent_manager.health_check_all_agents()
                agents_status = health_results.get("summary", {})
                # Добавляем MCP статус
                if hasattr(agent_manager, 'mcp_provider') and agent_manager.mcp_provider:
                    mcp_health = await agent_manager.mcp_provider.health_check()
                    agents_status['mcp_provider'] = mcp_health.get('overall_health', 'unknown')
            except Exception as e:
                logger.error(f"Health check agents error: {e}")
                agents_status = {"error": str(e)}
        
        # Получаем метрики
        metrics = await metrics_collector.get_current_metrics()
        
        # Определяем общий статус системы
        overall_healthy = all([db_healthy, redis_healthy, manager_healthy])
        status = "healthy" if overall_healthy else "degraded"
        
        # Добавляем информацию об инфраструктуре
        infrastructure = {
            "database": "healthy" if db_healthy else "unhealthy",
            "redis": "healthy" if redis_healthy else "unhealthy",
            "agent_manager": "healthy" if manager_healthy else "unhealthy"
        }
        
        return HealthResponse(
            status=status,
            timestamp=datetime.now().isoformat(),
            version="1.0.0",
            agents_status=agents_status,
            metrics={**metrics, "infrastructure": infrastructure},
            uptime_seconds=metrics.get("uptime_seconds", 0)
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            version="1.0.0",
            error=str(e)
        )


# Root endpoint
@app.get("/")
async def root():
    """Корневая страница API"""
    
    return {
        "message": "AI SEO Architects API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs",
        "health": "/health",
        "websocket": "/ws/dashboard",
        "dashboard": "/static/dashboard.html"
    }


# Dashboard endpoint
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Дашборд интерфейс"""
    try:
        dashboard_path = os.path.join(static_dir, "dashboard.html")
        if os.path.exists(dashboard_path):
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                return HTMLResponse(content=f.read())
        else:
            return HTMLResponse(
                content="""
                <html>
                    <body>
                        <h1>Dashboard не найден</h1>
                        <p>Файл dashboard.html не найден в директории static</p>
                        <a href="/api/docs">API Documentation</a>
                    </body>
                </html>
                """,
                status_code=404
            )
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        return HTMLResponse(
            content=f"<html><body><h1>Ошибка загрузки дашборда</h1><p>{str(e)}</p></body></html>",
            status_code=500
        )


# WebSocket endpoint для real-time дашборда
@app.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket, token: str = None):
    """WebSocket для real-time обновлений дашборда"""
    
    try:
        # TODO: Добавить аутентификацию через token
        await connection_manager.connect(websocket, client_id=f"dashboard_{datetime.now().timestamp()}")
        logger.info("📡 WebSocket подключение установлено для дашборда")
        
        # Отправляем начальные данные
        initial_data = {
            "type": "initial",
            "data": {
                "timestamp": datetime.now().isoformat(),
                "agents_count": len(agent_manager.agents) if agent_manager else 0,
                "status": "connected"
            }
        }
        
        await connection_manager.send_personal_message(json.dumps(initial_data), websocket)
        
        # Слушаем сообщения от клиента
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            
            # Обрабатываем команды от дашборда
            if data.get("type") == "request_metrics":
                metrics = await metrics_collector.get_current_metrics()
                response = {
                    "type": "metrics_update",
                    "data": metrics,
                    "timestamp": datetime.now().isoformat()
                }
                await connection_manager.send_personal_message(json.dumps(response), websocket)
            
            elif data.get("type") == "request_agents_status":
                if agent_manager:
                    health_results = await agent_manager.health_check_all_agents()
                    response = {
                        "type": "agents_status",
                        "data": health_results,
                        "timestamp": datetime.now().isoformat()
                    }
                    await connection_manager.send_personal_message(json.dumps(response), websocket)
                    
    except WebSocketDisconnect:
        logger.info("📡 WebSocket подключение закрыто")
        connection_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket ошибка: {e}")
        await connection_manager.disconnect(websocket)


# Metrics endpoint для Prometheus
@app.get("/metrics")
async def prometheus_metrics():
    \"\"\"Prometheus metrics endpoint\"\"\"
    try:
        # Получаем текущие метрики
        current_metrics = await metrics_collector.get_current_metrics()
        
        # Конвертируем в Prometheus формат
        metrics_lines = []
        
        # Системные метрики
        system = current_metrics.get("system", {})
        metrics_lines.extend([
            f'# HELP system_cpu_percent Current CPU usage percentage',
            f'# TYPE system_cpu_percent gauge',
            f'system_cpu_percent {system.get("cpu_percent", 0)}',
            f'',
            f'# HELP system_memory_percent Current memory usage percentage', 
            f'# TYPE system_memory_percent gauge',
            f'system_memory_percent {system.get("memory_percent", 0)}',
            f'',
            f'# HELP system_active_connections Current active connections',
            f'# TYPE system_active_connections gauge', 
            f'system_active_connections {system.get("active_connections", 0)}',
            f''
        ])
        
        # HTTP метрики
        http = current_metrics.get("http", {})
        metrics_lines.extend([
            f'# HELP http_requests_total Total HTTP requests',
            f'# TYPE http_requests_total counter',
            f'http_requests_total {http.get("total_requests_lifetime", 0)}',
            f'',
            f'# HELP http_errors_total Total HTTP errors',
            f'# TYPE http_errors_total counter', 
            f'http_errors_total {http.get("total_errors_lifetime", 0)}',
            f'',
            f'# HELP http_request_duration_seconds Average HTTP request duration',
            f'# TYPE http_request_duration_seconds gauge',
            f'http_request_duration_seconds {http.get("avg_response_time_1h", 0)}',
            f''
        ])
        
        # Метрики агентов
        agents = current_metrics.get("agents", {})
        for agent_id, agent_stats in agents.items():
            metrics_lines.extend([
                f'# HELP agent_tasks_total Total tasks processed by agent',
                f'# TYPE agent_tasks_total counter',
                f'agent_tasks_total{{agent_id=\"{agent_id}\"}} {agent_stats.get("total_tasks_1h", 0)}',
                f'',
                f'# HELP agent_success_rate Success rate of agent tasks',
                f'# TYPE agent_success_rate gauge',
                f'agent_success_rate{{agent_id=\"{agent_id}\"}} {agent_stats.get("success_rate_1h", 0)}',
                f'',
                f'# HELP agent_task_duration_seconds Average task duration',
                f'# TYPE agent_task_duration_seconds gauge', 
                f'agent_task_duration_seconds{{agent_id=\"{agent_id}\"}} {agent_stats.get("avg_duration_1h", 0)}',
                f''
            ])
        
        return \"\\n\".join(metrics_lines)
        
    except Exception as e:
        logger.error(f\"Metrics endpoint error: {e}\")
        return \"# Error generating metrics\"

# API метрики endpoints
@app.get(\"/api/metrics/system\")
async def get_system_metrics():
    \"\"\"Получить системные метрики\"\"\"
    try:
        metrics = await metrics_collector.get_current_metrics()
        return {
            \"status\": \"success\",
            \"data\": metrics.get(\"system\", {}),
            \"timestamp\": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f\"System metrics error: {e}\")
        raise HTTPException(status_code=500, detail=str(e))

@app.get(\"/api/metrics/agents\")
async def get_agents_metrics():
    \"\"\"Получить метрики агентов\"\"\"
    try:
        metrics = await metrics_collector.get_current_metrics()
        return {
            \"status\": \"success\",
            \"data\": metrics.get(\"agents\", {}),
            \"timestamp\": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f\"Agents metrics error: {e}\")
        raise HTTPException(status_code=500, detail=str(e))

@app.get(\"/api/metrics/detailed\")
async def get_detailed_metrics(hours: int = 1):
    \"\"\"Получить детальные метрики за период\"\"\"
    try:
        if hours > 24:
            hours = 24  # Максимум 24 часа
        
        detailed_metrics = await metrics_collector.get_detailed_metrics(hours)
        return {
            \"status\": \"success\",
            \"data\": detailed_metrics,
            \"timestamp\": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f\"Detailed metrics error: {e}\")
        raise HTTPException(status_code=500, detail=str(e))

# Подключение роутеров
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])


# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request, call_next):
    """Middleware для логирования HTTP запросов"""
    
    start_time = datetime.now()
    correlation_id = f"req_{start_time.timestamp()}"
    
    # Логируем начало запроса
    logger.info(
        "HTTP Request",
        extra={
            "correlation_id": correlation_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host
        }
    )
    
    # Обрабатываем запрос
    response = await call_next(request)
    
    # Считаем время выполнения
    processing_time = (datetime.now() - start_time).total_seconds()
    
    # Логируем завершение запроса
    logger.info(
        "HTTP Response",
        extra={
            "correlation_id": correlation_id,
            "status_code": response.status_code,
            "processing_time_seconds": processing_time
        }
    )
    
    # Обновляем метрики
    await metrics_collector.record_request(
        method=request.method,
        endpoint=str(request.url.path),
        status_code=response.status_code,
        duration=processing_time
    )
    
    return response


if __name__ == "__main__":
    # Запуск сервера для разработки
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )