"""
API роуты для аналитики и метрик
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from api.models.responses import (
    APIResponse, SystemMetrics, AgentPerformanceMetrics, 
    BusinessMetrics, MetricsTimeframe
)
from api.monitoring.logger import get_logger
from api.monitoring.metrics import get_metrics
from core.mcp.agent_manager import get_mcp_agent_manager

logger = get_logger(__name__)
router = APIRouter()


async def get_agent_manager():
    """Dependency для получения MCP Agent Manager"""
    return await get_mcp_agent_manager()


@router.get("/system", response_model=APIResponse)
async def get_system_metrics(
    timeframe: MetricsTimeframe = Query(MetricsTimeframe.HOUR)
):
    """
    Получить системные метрики за период
    """
    try:
        metrics_collector = get_metrics()
        
        # Конвертируем timeframe в часы
        timeframe_hours = {
            MetricsTimeframe.HOUR: 1,
            MetricsTimeframe.DAY: 24,
            MetricsTimeframe.WEEK: 168,
            MetricsTimeframe.MONTH: 720,
            MetricsTimeframe.QUARTER: 2160,
            MetricsTimeframe.YEAR: 8760
        }.get(timeframe, 1)
        
        # Получаем текущие метрики
        current_metrics = await metrics_collector.get_current_metrics()
        
        # Получаем детальные метрики за период
        detailed_metrics = await metrics_collector.get_detailed_metrics(timeframe_hours)
        
        # Формируем системные метрики
        system_metrics = SystemMetrics(
            timestamp=datetime.now().isoformat(),
            timeframe=timeframe,
            total_requests=detailed_metrics["summary"]["total_requests"],
            successful_requests=detailed_metrics["summary"]["total_requests"] - detailed_metrics["summary"]["total_errors"],
            error_rate=detailed_metrics["summary"]["total_errors"] / max(1, detailed_metrics["summary"]["total_requests"]),
            avg_response_time=current_metrics["http"]["avg_response_time_1h"],
            active_agents=len([a for a in current_metrics["agents"].keys()]),
            active_campaigns=0,  # Будет получено из campaigns storage
            active_clients=0,   # Будет получено из clients storage
            system_load=current_metrics["system"]["cpu_percent"],
            memory_usage_percent=current_metrics["system"]["memory_percent"],
            cpu_usage_percent=current_metrics["system"]["cpu_percent"]
        )
        
        return APIResponse(
            status="success",
            message=f"System metrics for {timeframe.value}",
            data={
                "metrics": system_metrics.dict(),
                "raw_metrics": current_metrics,
                "detailed_metrics": detailed_metrics
            }
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения системных метрик: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения метрик: {str(e)}")


@router.get("/agents", response_model=APIResponse)
async def get_agents_metrics(
    timeframe: MetricsTimeframe = Query(MetricsTimeframe.HOUR),
    agent_id: Optional[str] = Query(None),
    manager = Depends(get_agent_manager)
):
    """
    Получить метрики производительности агентов
    """
    try:
        metrics_collector = get_metrics()
        current_metrics = await metrics_collector.get_current_metrics()
        
        agent_metrics_data = []
        
        # Получаем метрики для всех агентов или конкретного
        agents_to_process = [agent_id] if agent_id else current_metrics["agents"].keys()
        
        for aid in agents_to_process:
            if aid not in current_metrics["agents"]:
                continue
                
            agent_data = current_metrics["agents"][aid]
            
            agent_metrics = AgentPerformanceMetrics(
                agent_id=aid,
                timeframe=timeframe,
                total_tasks=agent_data["total_tasks_1h"],
                successful_tasks=agent_data["successful_tasks_1h"],
                failed_tasks=agent_data["failed_tasks_1h"],
                success_rate=agent_data["success_rate_1h"],
                avg_processing_time=agent_data["avg_duration_1h"],
                throughput_per_hour=agent_data["tasks_per_minute"] * 60,
                error_types={},  # Будет расширено в будущем
                resource_usage={}  # Будет расширено в будущем
            )
            
            agent_metrics_data.append(agent_metrics)
        
        return APIResponse(
            status="success",
            message=f"Agent metrics for {timeframe.value}",
            data={
                "metrics": [metric.dict() for metric in agent_metrics_data],
                "total_agents": len(agent_metrics_data)
            }
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения метрик агентов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения метрик агентов: {str(e)}")


@router.get("/business", response_model=APIResponse)
async def get_business_metrics(
    timeframe: MetricsTimeframe = Query(MetricsTimeframe.DAY)
):
    """
    Получить бизнес-метрики
    """
    try:
        # Импортируем хранилища для подсчета бизнес метрик
        from api.routes.clients import clients_storage
        from api.routes.campaigns import campaigns_storage, campaign_metrics_storage
        
        # Подсчитываем бизнес метрики
        total_revenue = 0.0
        new_clients = 0
        churned_clients = 0
        total_clients = len(clients_storage)
        pipeline_value = 0.0
        total_leads = 0
        qualified_leads = 0
        
        # Временные рамки для анализа
        now = datetime.now()
        timeframe_deltas = {
            MetricsTimeframe.HOUR: timedelta(hours=1),
            MetricsTimeframe.DAY: timedelta(days=1),
            MetricsTimeframe.WEEK: timedelta(weeks=1),
            MetricsTimeframe.MONTH: timedelta(days=30),
            MetricsTimeframe.QUARTER: timedelta(days=90),
            MetricsTimeframe.YEAR: timedelta(days=365)
        }
        
        start_date = now - timeframe_deltas.get(timeframe, timedelta(days=1))
        
        # Анализ клиентов
        for client in clients_storage.values():
            created_at = datetime.fromisoformat(client.created_at.replace('Z', '+00:00'))
            
            # Новые клиенты
            if created_at >= start_date:
                new_clients += 1
            
            # Pipeline value
            if client.monthly_budget:
                pipeline_value += client.monthly_budget * 12
        
        # Анализ кампаний и revenue
        for campaign_id, metrics in campaign_metrics_storage.items():
            total_revenue += metrics.revenue_attributed
            total_leads += metrics.total_leads
            qualified_leads += metrics.qualified_leads
        
        # Средний размер сделки
        average_deal_size = total_revenue / max(1, total_clients)
        
        # Конверсия лидов
        lead_conversion_rate = qualified_leads / max(1, total_leads) if total_leads > 0 else 0
        
        # Retention rate (упрощенная версия)
        client_retention_rate = max(0, (total_clients - churned_clients) / max(1, total_clients))
        
        # Customer satisfaction (заглушка - в реальности из опросов)
        customer_satisfaction = 4.2  # Из 5
        
        business_metrics = BusinessMetrics(
            timestamp=now.isoformat(),
            timeframe=timeframe,
            total_revenue=total_revenue,
            new_clients=new_clients,
            churned_clients=churned_clients,
            client_retention_rate=client_retention_rate,
            average_deal_size=average_deal_size,
            pipeline_value=pipeline_value,
            lead_conversion_rate=lead_conversion_rate,
            customer_satisfaction=customer_satisfaction
        )
        
        return APIResponse(
            status="success",
            message=f"Business metrics for {timeframe.value}",
            data={
                "metrics": business_metrics.dict(),
                "additional_stats": {
                    "total_clients": total_clients,
                    "total_campaigns": len(campaigns_storage),
                    "active_campaigns": len([c for c in campaigns_storage.values() if c.status.value == "active"]),
                    "total_leads": total_leads,
                    "qualified_leads": qualified_leads
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения бизнес метрик: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения бизнес метрик: {str(e)}")


@router.get("/dashboard", response_model=APIResponse)
async def get_dashboard_data():
    """
    Получить агрегированные данные для дашборда
    """
    try:
        metrics_collector = get_metrics()
        current_metrics = await metrics_collector.get_current_metrics()
        
        # Импортируем хранилища
        from api.routes.clients import clients_storage
        from api.routes.campaigns import campaigns_storage, campaign_metrics_storage
        
        # Основная статистика
        dashboard_data = {
            "system_health": {
                "uptime_seconds": current_metrics["uptime_seconds"],
                "cpu_percent": current_metrics["system"]["cpu_percent"],
                "memory_percent": current_metrics["system"]["memory_percent"],
                "active_connections": current_metrics["system"]["active_connections"],
                "status": "healthy" if current_metrics["system"]["cpu_percent"] < 80 else "warning"
            },
            "agents_summary": {
                "total_agents": len(current_metrics["agents"]),
                "active_agents": len([a for a, data in current_metrics["agents"].items() 
                                    if data["total_tasks_1h"] > 0]),
                "avg_success_rate": sum(data["success_rate_1h"] for data in current_metrics["agents"].values()) / 
                                  max(1, len(current_metrics["agents"])),
                "total_tasks_1h": sum(data["total_tasks_1h"] for data in current_metrics["agents"].values())
            },
            "business_summary": {
                "total_clients": len(clients_storage),
                "total_campaigns": len(campaigns_storage),
                "active_campaigns": len([c for c in campaigns_storage.values() if c.status.value == "active"]),
                "total_revenue": sum(metrics.revenue_attributed for metrics in campaign_metrics_storage.values()),
                "total_leads": sum(metrics.total_leads for metrics in campaign_metrics_storage.values())
            },
            "http_summary": {
                "requests_1h": current_metrics["http"]["requests_1h"],
                "error_rate_1h": current_metrics["http"]["error_rate_1h"],
                "avg_response_time_1h": current_metrics["http"]["avg_response_time_1h"],
                "requests_per_minute": current_metrics["http"]["requests_per_minute"]
            },
            "recent_activity": await _get_recent_activity(),
            "top_performing_agents": _get_top_agents(current_metrics["agents"]),
            "alerts": await _get_system_alerts(current_metrics)
        }
        
        return APIResponse(
            status="success",
            message="Dashboard data retrieved",
            data=dashboard_data
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения данных дашборда: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных дашборда: {str(e)}")


@router.get("/export")
async def export_metrics(
    timeframe: MetricsTimeframe = Query(MetricsTimeframe.DAY),
    format: str = Query("json", regex="^(json|csv)$")
):
    """
    Экспорт метрик в файл
    """
    try:
        metrics_collector = get_metrics()
        
        # Генерируем имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"metrics_export_{timeframe.value}_{timestamp}.{format}"
        filepath = f"exports/{filename}"
        
        # Экспортируем метрики
        await metrics_collector.export_metrics(filepath)
        
        logger.info(f"Метрики экспортированы в файл: {filepath}")
        
        return APIResponse(
            status="success",
            message=f"Metrics exported successfully",
            data={
                "filename": filename,
                "filepath": filepath,
                "format": format,
                "timeframe": timeframe.value,
                "exported_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Ошибка экспорта метрик: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка экспорта метрик: {str(e)}")


async def _get_recent_activity() -> List[Dict[str, Any]]:
    """Получить недавнюю активность системы"""
    try:
        # Заглушка для недавней активности
        # В реальном проекте здесь будет запрос к базе данных или лог-файлам
        recent_activity = [
            {
                "timestamp": datetime.now().isoformat(),
                "type": "agent_task_completed",
                "message": "Technical SEO Audit completed for client XYZ",
                "agent_id": "technical_seo_auditor"
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "type": "new_client_created",
                "message": "New client registered: TechCorp Inc",
                "client_id": "client_12345"
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(),
                "type": "campaign_started",
                "message": "SEO Campaign started for example.com",
                "campaign_id": "camp_67890"
            }
        ]
        
        return recent_activity
        
    except Exception as e:
        logger.error(f"Ошибка получения недавней активности: {e}")
        return []


def _get_top_agents(agents_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Получить топ-агентов по производительности"""
    try:
        # Сортируем агентов по success rate и количеству задач
        agent_performance = []
        
        for agent_id, data in agents_data.items():
            score = data["success_rate_1h"] * data["total_tasks_1h"]  # Комбинированный показатель
            
            agent_performance.append({
                "agent_id": agent_id,
                "success_rate": data["success_rate_1h"],
                "total_tasks": data["total_tasks_1h"],
                "avg_duration": data["avg_duration_1h"],
                "performance_score": score
            })
        
        # Топ-5 агентов
        top_agents = sorted(agent_performance, key=lambda x: x["performance_score"], reverse=True)[:5]
        
        return top_agents
        
    except Exception as e:
        logger.error(f"Ошибка получения топ-агентов: {e}")
        return []


async def _get_system_alerts(current_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Получить системные алерты"""
    try:
        alerts = []
        
        # Проверяем CPU
        cpu_percent = current_metrics["system"]["cpu_percent"]
        if cpu_percent > 80:
            alerts.append({
                "type": "warning",
                "message": f"High CPU usage: {cpu_percent:.1f}%",
                "timestamp": datetime.now().isoformat()
            })
        
        # Проверяем память
        memory_percent = current_metrics["system"]["memory_percent"]
        if memory_percent > 85:
            alerts.append({
                "type": "warning",
                "message": f"High memory usage: {memory_percent:.1f}%",
                "timestamp": datetime.now().isoformat()
            })
        
        # Проверяем error rate
        error_rate = current_metrics["http"]["error_rate_1h"]
        if error_rate > 0.05:  # > 5%
            alerts.append({
                "type": "error",
                "message": f"High error rate: {error_rate:.1%}",
                "timestamp": datetime.now().isoformat()
            })
        
        # Проверяем агентов с низким success rate
        for agent_id, data in current_metrics["agents"].items():
            if data["success_rate_1h"] < 0.8 and data["total_tasks_1h"] > 0:  # < 80%
                alerts.append({
                    "type": "warning",
                    "message": f"Low success rate for agent {agent_id}: {data['success_rate_1h']:.1%}",
                    "timestamp": datetime.now().isoformat()
                })
        
        return alerts
        
    except Exception as e:
        logger.error(f"Ошибка получения алертов: {e}")
        return []


@router.get("/health")
async def analytics_health_check():
    """
    Health check для аналитического модуля
    """
    try:
        metrics_collector = get_metrics()
        stats = metrics_collector.get_stats()
        
        health_status = {
            "status": "healthy",
            "metrics_collector": {
                "active_connections": stats.get("active_connections", 0),
                "total_requests_lifetime": stats.get("total_requests_lifetime", 0),
                "uptime_seconds": stats.get("uptime_seconds", 0)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return APIResponse(
            status="success",
            message="Analytics module is healthy",
            data=health_status
        )
        
    except Exception as e:
        logger.error(f"Ошибка health check аналитики: {e}")
        raise HTTPException(status_code=500, detail=f"Analytics health check failed: {str(e)}")