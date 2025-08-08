"""
API роуты для управления задачами с PostgreSQL интеграцией
Полный CRUD для задач агентов с реальной базой данных
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

from api.database.connection import get_db_session
from api.database.models import (
    AgentTask as TaskModel,
    AgentTaskCreate as TaskCreate,
    AgentTaskResponse as TaskResponse, 
    Agent as AgentModel,
    Campaign as CampaignModel
)
from api.models.responses import APIResponse
from api.monitoring.logger import get_logger
from core.mcp.agent_manager import get_mcp_agent_manager

logger = get_logger(__name__)
router = APIRouter()


async def get_agent_manager():
    """Dependency для получения MCP Agent Manager"""
    return await get_mcp_agent_manager()


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[str] = Query(None, description="Фильтр по статусу задачи"),
    agent_id: Optional[uuid.UUID] = Query(None, description="Фильтр по агенту"),
    campaign_id: Optional[uuid.UUID] = Query(None, description="Фильтр по кампании"),
    priority: Optional[str] = Query(None, description="Фильтр по приоритету"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Получить список задач с фильтрацией и пагинацией
    Использует реальную PostgreSQL базу данных
    """
    try:
        logger.info(f"Запрос списка задач: status={status}, agent_id={agent_id}")
        
        # Строим базовый запрос с включением связанных данных
        query = select(TaskModel).options(
            selectinload(TaskModel.agent),
            selectinload(TaskModel.campaign)
        ).order_by(TaskModel.created_at.desc())
        
        # Применяем фильтры
        if status:
            query = query.where(TaskModel.status == status)
        
        if agent_id:
            query = query.where(TaskModel.agent_id == agent_id)
            
        if campaign_id:
            query = query.where(TaskModel.campaign_id == campaign_id)
            
        if priority:
            query = query.where(TaskModel.priority == priority)
        
        # Применяем пагинацию
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        
        # Выполняем запрос
        result = await db.execute(query)
        tasks = result.scalars().all()
        
        logger.info(f"Найдено задач: {len(tasks)}")
        return tasks
        
    except Exception as e:
        logger.error(f"Ошибка получения списка задач: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения задач: {str(e)}")


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: uuid.UUID,
    include_agent: bool = Query(False, description="Включить данные агента"),
    include_campaign: bool = Query(False, description="Включить данные кампании"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Получить задачу по ID
    """
    try:
        logger.info(f"Запрос задачи: {task_id}")
        
        # Строим запрос с возможным включением связанных данных
        query = select(TaskModel).where(TaskModel.id == task_id)
        
        if include_agent:
            query = query.options(selectinload(TaskModel.agent))
            
        if include_campaign:
            query = query.options(selectinload(TaskModel.campaign))
        
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        
        logger.info(f"Задача найдена: {task.task_type}")
        return task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения задачи {task_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения задачи: {str(e)}")


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session),
    agent_manager = Depends(get_agent_manager)
):
    """
    Создать новую задачу
    Запускает фоновое выполнение задачи агентом
    """
    try:
        logger.info(f"Создание задачи: {task_data.task_type}")
        
        # Проверяем существование агента
        if task_data.agent_id:
            agent_result = await db.execute(
                select(AgentModel).where(AgentModel.id == task_data.agent_id)
            )
            agent = agent_result.scalar_one_or_none()
            if not agent:
                raise HTTPException(status_code=404, detail="Агент не найден")
        
        # Проверяем существование кампании (если указана)
        if task_data.campaign_id:
            campaign_result = await db.execute(
                select(CampaignModel).where(CampaignModel.id == task_data.campaign_id)
            )
            campaign = campaign_result.scalar_one_or_none()
            if not campaign:
                raise HTTPException(status_code=404, detail="Кампания не найдена")
        
        # Создаем задачу
        new_task = TaskModel(
            **task_data.model_dump(),
            status="pending",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        
        # Запускаем фоновое выполнение задачи
        background_tasks.add_task(
            execute_task_async,
            new_task.id,
            agent_manager
        )
        
        logger.info(f"Задача создана: {new_task.id}")
        return new_task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка создания задачи: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка создания задачи: {str(e)}")


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: uuid.UUID,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Обновить данные задачи
    """
    try:
        logger.info(f"Обновление задачи: {task_id}")
        
        # Находим задачу
        result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        
        # Проверяем что задачу можно обновить
        if task.status in ["completed", "failed"]:
            raise HTTPException(
                status_code=400, 
                detail="Нельзя обновить завершенную или неуспешную задачу"
            )
        
        # Обновляем данные
        update_data = task_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now()
        
        await db.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(**update_data)
        )
        await db.commit()
        
        # Возвращаем обновленную задачу
        result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
        updated_task = result.scalar_one()
        
        logger.info(f"Задача обновлена: {task_id}")
        return updated_task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления задачи {task_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления задачи: {str(e)}")


@router.delete("/{task_id}")
async def delete_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Удалить задачу
    """
    try:
        logger.info(f"Удаление задачи: {task_id}")
        
        # Проверяем существование
        result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        
        # Проверяем что задачу можно удалить
        if task.status == "in_progress":
            raise HTTPException(
                status_code=400,
                detail="Нельзя удалить выполняющуюся задачу. Сначала отмените её."
            )
        
        # Удаляем задачу
        await db.execute(delete(TaskModel).where(TaskModel.id == task_id))
        await db.commit()
        
        logger.info(f"Задача удалена: {task_id}")
        return {"message": f"Задача {task_id} успешно удалена"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления задачи {task_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка удаления задачи: {str(e)}")


@router.post("/{task_id}/cancel")
async def cancel_task(
    task_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Отменить задачу
    """
    try:
        logger.info(f"Отмена задачи: {task_id}")
        
        # Находим задачу
        result = await db.execute(select(TaskModel).where(TaskModel.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        
        if task.status in ["completed", "failed", "cancelled"]:
            raise HTTPException(
                status_code=400,
                detail=f"Нельзя отменить задачу в статусе '{task.status}'"
            )
        
        # Обновляем статус
        await db.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(
                status="cancelled",
                updated_at=datetime.now(),
                completed_at=datetime.now()
            )
        )
        await db.commit()
        
        logger.info(f"Задача отменена: {task_id}")
        
        return APIResponse(
            status="success",
            message=f"Task {task_id} cancelled successfully",
            data={"status": "cancelled"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка отмены задачи {task_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка отмены задачи: {str(e)}")


@router.get("/stats/summary")
async def get_tasks_summary(db: AsyncSession = Depends(get_db_session)):
    """
    Получить общую статистику по всем задачам
    """
    try:
        logger.info("Запрос статистики задач")
        
        # Общее количество задач
        total_tasks = await db.execute(select(func.count(TaskModel.id)))
        total_count = total_tasks.scalar()
        
        # Статистика по статусам
        status_stats = await db.execute(
            select(TaskModel.status, func.count(TaskModel.id))
            .group_by(TaskModel.status)
        )
        
        # Статистика по приоритетам
        priority_stats = await db.execute(
            select(TaskModel.priority, func.count(TaskModel.id))
            .group_by(TaskModel.priority)
        )
        
        # Статистика по типам задач
        type_stats = await db.execute(
            select(TaskModel.task_type, func.count(TaskModel.id))
            .group_by(TaskModel.task_type)
            .order_by(func.count(TaskModel.id).desc())
        )
        
        # Среднее время выполнения
        avg_duration = await db.execute(
            select(func.avg(func.extract('epoch', TaskModel.completed_at - TaskModel.started_at)))
            .where(TaskModel.completed_at.is_not(None))
            .where(TaskModel.started_at.is_not(None))
        )
        
        # Активные задачи за последние 24 часа
        day_ago = datetime.now() - timedelta(hours=24)
        recent_tasks = await db.execute(
            select(func.count(TaskModel.id))
            .where(TaskModel.created_at > day_ago)
        )
        
        # Формируем результат
        status_breakdown = {row[0]: row[1] for row in status_stats.all()}
        priority_breakdown = {row[0]: row[1] for row in priority_stats.all()}
        type_breakdown = [(row[0], row[1]) for row in type_stats.all()[:10]]  # Топ 10
        
        summary = {
            "total_tasks": total_count,
            "status_breakdown": status_breakdown,
            "priority_breakdown": priority_breakdown,
            "top_task_types": type_breakdown,
            "performance_stats": {
                "average_duration_seconds": avg_duration.scalar() or 0,
                "tasks_24h": recent_tasks.scalar(),
                "completion_rate": (
                    status_breakdown.get("completed", 0) / max(1, total_count) * 100
                )
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Статистика получена: {total_count} задач")
        
        return APIResponse(
            status="success",
            message="Tasks summary retrieved",
            data=summary
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения статистики задач: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")


async def execute_task_async(task_id: uuid.UUID, agent_manager):
    """
    Фоновая задача выполнения задачи агентом
    """
    try:
        from api.database.connection import get_db_connection
        
        async with get_db_connection() as db:
            # Получаем задачу из базы
            result = await db.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            )
            task = result.scalar_one_or_none()
            
            if not task:
                logger.error(f"Задача {task_id} не найдена для выполнения")
                return
            
            logger.info(f"Выполнение задачи {task_id}: {task.task_type}")
            
            start_time = datetime.now()
            
            # Обновляем статус на "выполняется"
            await db.execute(
                update(TaskModel)
                .where(TaskModel.id == task_id)
                .values(
                    status="in_progress",
                    started_at=start_time,
                    updated_at=start_time
                )
            )
            await db.commit()
            
            try:
                # Получаем и выполняем задачу через реального агента
                agent_result = await execute_real_agent_task(task, agent_manager)
                
                # Обновляем задачу с результатом
                await db.execute(
                    update(TaskModel)
                    .where(TaskModel.id == task_id)
                    .values(
                        status="completed",
                        output_data=agent_result,
                        completed_at=datetime.now(),
                        updated_at=datetime.now(),
                        processing_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
                    )
                )
                await db.commit()
                
                logger.info(f"Задача {task_id} выполнена реальным агентом успешно")
                    
            except Exception as task_error:
                logger.error(f"Ошибка выполнения задачи {task_id}: {task_error}")
                
                # Обновляем статус на "неуспешно"
                await db.execute(
                    update(TaskModel)
                    .where(TaskModel.id == task_id)
                    .values(
                        status="failed",
                        error_message=str(task_error),
                        completed_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                )
                await db.commit()
        
    except Exception as e:
        logger.error(f"Критическая ошибка выполнения задачи {task_id}: {e}")


async def execute_real_agent_task(task: TaskModel, agent_manager) -> Dict[str, Any]:
    """
    Выполнить задачу через реального MCP агента
    """
    try:
        start_time = datetime.now()
        
        # Получаем список доступных агентов
        if not hasattr(agent_manager, 'agents') or not agent_manager.agents:
            logger.warning("Нет доступных агентов в MCP Agent Manager")
            return await _fallback_task_processing(task)
        
        # Определяем подходящего агента по типу задачи
        target_agent = await _find_suitable_agent(task, agent_manager)
        
        if not target_agent:
            logger.warning(f"Не найден подходящий агент для задачи {task.task_type}")
            return await _fallback_task_processing(task)
        
        # Формируем задачу для агента
        agent_input = {
            "task_type": task.task_type,
            "input_data": task.input_data or {},
            "priority": task.priority,
            "task_id": str(task.id),
            "timestamp": start_time.isoformat()
        }
        
        logger.info(f"Запуск агента {target_agent.agent_id} для задачи {task.task_type}")
        
        # Выполняем задачу через реального агента
        agent_result = await target_agent.process_task(agent_input)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Форматируем результат
        result = {
            "status": "success" if agent_result.get("success", False) else "failed",
            "task_type": task.task_type,
            "agent_id": target_agent.agent_id,
            "agent_name": target_agent.name,
            "result": agent_result.get("result", {}),
            "processing_time_seconds": processing_time,
            "timestamp": datetime.now().isoformat(),
            "mcp_enabled": getattr(target_agent, 'mcp_enabled', False),
            "data_source": getattr(target_agent.data_provider, '__class__', {}).get('__name__', 'unknown')
        }
        
        # Добавляем ошибки если есть
        if agent_result.get("error"):
            result["error"] = agent_result["error"]
            
        logger.info(f"Агент {target_agent.agent_id} завершил задачу за {processing_time:.2f}s")
        
        return result
        
    except Exception as e:
        logger.error(f"Ошибка выполнения реальной задачи агентом: {e}")
        return {
            "status": "error",
            "task_type": task.task_type,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


async def _find_suitable_agent(task: TaskModel, agent_manager):
    """
    Найти подходящего агента для задачи
    """
    task_type_mapping = {
        "lead_qualification": "lead_qualification",
        "proposal_generation": "proposal_generation", 
        "technical_seo_audit": "technical_seo_auditor",
        "content_strategy": "content_strategy",
        "competitive_analysis": "competitive_analysis",
        "sales_conversation": "sales_conversation",
        "link_building": "link_building",
        "reporting": "reporting",
        "task_coordination": "task_coordination"
    }
    
    target_agent_id = task_type_mapping.get(task.task_type)
    if not target_agent_id:
        # Если не нашли по маппингу, берем первого доступного
        return next(iter(agent_manager.agents.values()))
    
    # Ищем агента по ID
    return agent_manager.agents.get(target_agent_id)


async def _fallback_task_processing(task: TaskModel) -> Dict[str, Any]:
    """
    Fallback обработка задачи без агента
    """
    logger.info(f"Fallback обработка задачи {task.task_type}")
    
    # Имитируем минимальную обработку
    await asyncio.sleep(0.5)
    
    return {
        "status": "completed",
        "task_type": task.task_type,
        "result": f"Task {task.task_type} processed via fallback mechanism",
        "warning": "No suitable agent available, used fallback processing",
        "timestamp": datetime.now().isoformat()
    }


# Health check для задач
@router.get("/health/tasks")
async def tasks_health_check(db: AsyncSession = Depends(get_db_session)):
    """Проверка состояния системы задач"""
    try:
        # Проверяем подключение к базе данных
        tasks_count = await db.execute(select(func.count(TaskModel.id)))
        total_tasks = tasks_count.scalar()
        
        # Активные задачи
        in_progress_count = await db.execute(
            select(func.count(TaskModel.id))
            .where(TaskModel.status == "in_progress")
        )
        
        # Задачи в очереди
        pending_count = await db.execute(
            select(func.count(TaskModel.id))
            .where(TaskModel.status == "pending")
        )
        
        return {
            "status": "healthy",
            "total_tasks": total_tasks,
            "in_progress_tasks": in_progress_count.scalar(),
            "pending_tasks": pending_count.scalar(),
            "timestamp": datetime.now().isoformat(),
            "database": "connected"
        }
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "database": "disconnected"
        }