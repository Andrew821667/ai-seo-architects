"""
API роуты для управления агентами
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio

from api.models.responses import (
    APIResponse, AgentInfo, AgentTask, AgentTaskResult, 
    AgentsListResponse, AgentStatus, PaginationParams,
    AgentFilters
)
from api.monitoring.logger import get_logger
from api.monitoring.metrics import get_metrics
from core.mcp.agent_manager import get_mcp_agent_manager

logger = get_logger(__name__)
router = APIRouter()


async def get_agent_manager():
    """Dependency для получения MCP Agent Manager"""
    return await get_mcp_agent_manager()


@router.get("/", response_model=AgentsListResponse)
async def list_agents(
    status: Optional[List[AgentStatus]] = Query(None),
    agent_type: Optional[str] = Query(None),
    mcp_enabled: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    manager = Depends(get_agent_manager)
):
    """
    Получить список всех агентов с фильтрацией и пагинацией
    """
    try:
        logger.info("Запрос списка агентов", 
                   filters={"status": status, "agent_type": agent_type, "mcp_enabled": mcp_enabled})
        
        # Получаем всех агентов
        all_agents = []
        categories = {"executive": 0, "management": 0, "operational": 0}
        
        for agent_id, agent in manager.agents.items():
            # Определяем тип агента
            agent_class_name = agent.__class__.__name__
            if "Executive" in agent_class_name or "Chief" in agent_class_name or "Business" in agent_class_name:
                category = "executive"
            elif "Manager" in agent_class_name or "Coordination" in agent_class_name:
                category = "management"
            else:
                category = "operational"
            
            categories[category] += 1
            
            # Получаем статус агента
            health = agent.get_health_status()
            agent_status = AgentStatus.ACTIVE if health.get("status") == "healthy" else AgentStatus.ERROR
            
            # Применяем фильтры
            if status and agent_status not in status:
                continue
            if agent_type and category != agent_type:
                continue
            if mcp_enabled is not None and agent.mcp_enabled != mcp_enabled:
                continue
            
            # Создаем объект AgentInfo
            agent_info = AgentInfo(
                agent_id=agent.agent_id,
                name=agent.name,
                agent_type=category,
                status=agent_status,
                mcp_enabled=agent.mcp_enabled,
                created_at=datetime.now().isoformat(),
                success_rate=health.get("success_rate", 0.0),
                processing_time_avg=health.get("avg_processing_time", 0.0)
            )
            
            all_agents.append(agent_info)
        
        # Применяем пагинацию
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_agents = all_agents[start_idx:end_idx]
        
        # Подсчитываем активных агентов
        active_count = sum(1 for agent in all_agents if agent.status == AgentStatus.ACTIVE)
        mcp_count = sum(1 for agent in all_agents if agent.mcp_enabled)
        
        return AgentsListResponse(
            agents=paginated_agents,
            total_count=len(all_agents),
            active_count=active_count,
            mcp_enabled_count=mcp_count,
            categories=categories
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения списка агентов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения списка агентов: {str(e)}")


@router.get("/{agent_id}", response_model=AgentInfo)
async def get_agent(
    agent_id: str,
    manager = Depends(get_agent_manager)
):
    """
    Получить информацию о конкретном агенте
    """
    try:
        if agent_id not in manager.agents:
            raise HTTPException(status_code=404, detail=f"Агент {agent_id} не найден")
        
        agent = manager.agents[agent_id]
        health = agent.get_health_status()
        
        # Определяем категорию агента
        agent_class_name = agent.__class__.__name__
        if "Executive" in agent_class_name or "Chief" in agent_class_name or "Business" in agent_class_name:
            category = "executive"
        elif "Manager" in agent_class_name or "Coordination" in agent_class_name:
            category = "management"
        else:
            category = "operational"
        
        agent_status = AgentStatus.ACTIVE if health.get("status") == "healthy" else AgentStatus.ERROR
        
        return AgentInfo(
            agent_id=agent.agent_id,
            name=agent.name,
            agent_type=category,
            status=agent_status,
            mcp_enabled=agent.mcp_enabled,
            created_at=datetime.now().isoformat(),
            success_rate=health.get("success_rate", 0.0),
            processing_time_avg=health.get("avg_processing_time", 0.0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения агента {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения агента: {str(e)}")


@router.post("/{agent_id}/tasks", response_model=AgentTaskResult)
async def execute_agent_task(
    agent_id: str,
    task: AgentTask,
    background_tasks: BackgroundTasks,
    manager = Depends(get_agent_manager)
):
    """
    Выполнить задачу для конкретного агента
    """
    try:
        if agent_id not in manager.agents:
            raise HTTPException(status_code=404, detail=f"Агент {agent_id} не найден")
        
        agent = manager.agents[agent_id]
        metrics = get_metrics()
        
        logger.info(f"Выполнение задачи для агента {agent_id}",
                   task_id=task.task_id,
                   task_type=task.task_type)
        
        # Записываем время начала
        start_time = datetime.now()
        
        try:
            # Выполняем задачу
            result = await agent.process_task({
                "input_data": task.input_data,
                "task_type": task.task_type,
                "task_id": task.task_id,
                "metadata": task.metadata
            })
            
            # Вычисляем время выполнения
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            # Определяем статус
            success = result.get("success", False)
            status = "completed" if success else "failed"
            error = result.get("error") if not success else None
            
            # Записываем метрики
            background_tasks.add_task(
                metrics.record_agent_task,
                agent_id=agent_id,
                task_type=task.task_type,
                status=status,
                duration=processing_time,
                error_type=error
            )
            
            logger.log_agent_task(
                agent_id=agent_id,
                task_id=task.task_id,
                task_type=task.task_type,
                status=status,
                processing_time=processing_time
            )
            
            return AgentTaskResult(
                task_id=task.task_id,
                agent_id=agent_id,
                status=status,
                result=result.get("result"),
                error=error,
                processing_time=processing_time,
                started_at=start_time.isoformat(),
                completed_at=end_time.isoformat(),
                metadata=task.metadata
            )
            
        except asyncio.TimeoutError:
            processing_time = task.timeout or 300
            
            background_tasks.add_task(
                metrics.record_agent_task,
                agent_id=agent_id,
                task_type=task.task_type,
                status="timeout",
                duration=processing_time
            )
            
            logger.error(f"Задача {task.task_id} превысила timeout",
                        agent_id=agent_id,
                        timeout=task.timeout)
            
            return AgentTaskResult(
                task_id=task.task_id,
                agent_id=agent_id,
                status="timeout",
                error=f"Task exceeded timeout of {task.timeout} seconds",
                processing_time=processing_time,
                started_at=start_time.isoformat(),
                completed_at=datetime.now().isoformat(),
                metadata=task.metadata
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка выполнения задачи для агента {agent_id}: {e}",
                    task_id=task.task_id)
        raise HTTPException(status_code=500, detail=f"Ошибка выполнения задачи: {str(e)}")


@router.get("/{agent_id}/health")
async def get_agent_health(
    agent_id: str,
    manager = Depends(get_agent_manager)
):
    """
    Получить статус здоровья конкретного агента
    """
    try:
        if agent_id not in manager.agents:
            raise HTTPException(status_code=404, detail=f"Агент {agent_id} не найден")
        
        agent = manager.agents[agent_id]
        health = agent.get_health_status()
        
        # Дополнительная MCP проверка если доступна
        if hasattr(agent, 'get_mcp_health_status'):
            mcp_health = await agent.get_mcp_health_status()
            health["mcp_status"] = mcp_health
        
        return APIResponse(
            status="success",
            message=f"Health check for agent {agent_id}",
            data=health
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка health check агента {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка health check: {str(e)}")


@router.post("/{agent_id}/enable-mcp")
async def enable_agent_mcp(
    agent_id: str,
    manager = Depends(get_agent_manager)
):
    """
    Включить MCP для конкретного агента
    """
    try:
        if agent_id not in manager.agents:
            raise HTTPException(status_code=404, detail=f"Агент {agent_id} не найден")
        
        agent = manager.agents[agent_id]
        
        if not agent.mcp_enabled and manager.mcp_provider:
            agent.enable_mcp(manager.mcp_provider)
            
            logger.info(f"MCP включен для агента {agent_id}")
            
            return APIResponse(
                status="success",
                message=f"MCP enabled for agent {agent_id}",
                data={"mcp_enabled": True}
            )
        elif agent.mcp_enabled:
            return APIResponse(
                status="warning",
                message=f"MCP already enabled for agent {agent_id}",
                data={"mcp_enabled": True}
            )
        else:
            raise HTTPException(status_code=503, detail="MCP provider недоступен")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка включения MCP для агента {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка включения MCP: {str(e)}")


@router.post("/{agent_id}/disable-mcp")
async def disable_agent_mcp(
    agent_id: str,
    manager = Depends(get_agent_manager)
):
    """
    Отключить MCP для конкретного агента
    """
    try:
        if agent_id not in manager.agents:
            raise HTTPException(status_code=404, detail=f"Агент {agent_id} не найден")
        
        agent = manager.agents[agent_id]
        
        if agent.mcp_enabled:
            agent.disable_mcp()
            
            logger.info(f"MCP отключен для агента {agent_id}")
            
            return APIResponse(
                status="success",
                message=f"MCP disabled for agent {agent_id}",
                data={"mcp_enabled": False}
            )
        else:
            return APIResponse(
                status="warning",
                message=f"MCP already disabled for agent {agent_id}",
                data={"mcp_enabled": False}
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка отключения MCP для агента {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка отключения MCP: {str(e)}")


@router.get("/{agent_id}/stats")
async def get_agent_stats(
    agent_id: str,
    timeframe_hours: int = Query(1, ge=1, le=168),  # 1 час - 1 неделя
    manager = Depends(get_agent_manager)
):
    """
    Получить статистику работы агента за период
    """
    try:
        if agent_id not in manager.agents:
            raise HTTPException(status_code=404, detail=f"Агент {agent_id} не найден")
        
        metrics = get_metrics()
        current_metrics = await metrics.get_current_metrics()
        agent_metrics = current_metrics.get("agents", {}).get(agent_id, {})
        
        # Дополнительные статистики можно добавить позже
        stats = {
            "agent_id": agent_id,
            "timeframe_hours": timeframe_hours,
            "current_metrics": agent_metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        return APIResponse(
            status="success",
            message=f"Statistics for agent {agent_id}",
            data=stats
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения статистики агента {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")


@router.post("/create-all")
async def create_all_agents(
    enable_mcp: bool = Query(True),
    manager = Depends(get_agent_manager)
):
    """
    Создать всех агентов (14 агентов)
    """
    try:
        logger.info(f"Создание всех агентов (MCP: {enable_mcp})")
        
        agents = await manager.create_all_agents(enable_mcp=enable_mcp)
        
        return APIResponse(
            status="success",
            message=f"Created {len(agents)} agents",
            data={
                "created_count": len(agents),
                "mcp_enabled": enable_mcp,
                "agent_ids": list(agents.keys())
            }
        )
        
    except Exception as e:
        logger.error(f"Ошибка создания всех агентов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка создания агентов: {str(e)}")


@router.get("/health/all")
async def health_check_all_agents(
    manager = Depends(get_agent_manager)
):
    """
    Проверка здоровья всех агентов
    """
    try:
        health_results = await manager.health_check_all_agents()
        
        return APIResponse(
            status="success",
            message="Health check completed for all agents",
            data=health_results
        )
        
    except Exception as e:
        logger.error(f"Ошибка health check всех агентов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка health check: {str(e)}")


@router.post("/test/comprehensive")
async def run_comprehensive_test(
    manager = Depends(get_agent_manager)
):
    """
    Запустить комплексное тестирование всех агентов
    """
    try:
        logger.info("Запуск комплексного тестирования всех агентов")
        
        test_results = await manager.run_comprehensive_test()
        
        return APIResponse(
            status="success",
            message="Comprehensive test completed",
            data=test_results
        )
        
    except Exception as e:
        logger.error(f"Ошибка комплексного тестирования: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка тестирования: {str(e)}")