"""
API роуты для управления SEO кампаниями с PostgreSQL интеграцией
Реальная база данных вместо in-memory storage
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update
from sqlalchemy.orm import selectinload
from typing import List, Any, Optional, Dict
from datetime import datetime, timedelta
import uuid

from api.database.connection import get_db_session
from api.database.models import (
    Campaign as CampaignModel,
    CampaignCreate,
    CampaignResponse,
    CampaignMetrics as CampaignMetricsModel,
    Client as ClientModel
)
from api.models.responses import APIResponse, CampaignStatus
from api.monitoring.logger import get_logger
from core.mcp.agent_manager import get_mcp_agent_manager

logger = get_logger(__name__)
router = APIRouter()


async def get_agent_manager():
    """Dependency для получения MCP Agent Manager"""
    return await get_mcp_agent_manager()


@router.get("/", response_model=List[CampaignResponse])
async def list_campaigns(
    status: Optional[str] = Query(None, description="Фильтр по статусу кампании"),
    client_id: Optional[uuid.UUID] = Query(None, description="Фильтр по клиенту"),
    domain: Optional[str] = Query(None, description="Фильтр по домену"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Получить список SEO кампаний с фильтрацией и пагинацией
    Использует реальную PostgreSQL базу данных
    """
    try:
        logger.info(f"Запрос списка кампаний: status={status}, client_id={client_id}")
        
        # Строим базовый запрос с включением клиента
        query = select(CampaignModel).options(
            selectinload(CampaignModel.client)
        ).order_by(CampaignModel.created_at.desc())
        
        # Применяем фильтры
        if status:
            query = query.where(CampaignModel.status == status)
        
        if client_id:
            query = query.where(CampaignModel.client_id == client_id)
            
        if domain:
            query = query.where(CampaignModel.domain.ilike(f"%{domain}%"))
        
        # Применяем пагинацию
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        
        # Выполняем запрос
        result = await db.execute(query)
        campaigns = result.scalars().all()
        
        logger.info(f"Найдено кампаний: {len(campaigns)}")
        return campaigns
        
    except Exception as e:
        logger.error(f"Ошибка получения списка кампаний: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения кампаний: {str(e)}")


@router.post("/", response_model=CampaignResponse)
async def create_campaign(
    campaign_data: CampaignCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session),
    manager = Depends(get_agent_manager)
):
    """
    Создать новую SEO кампанию
    Запускает фоновую задачу назначения агентов
    """
    try:
        logger.info(f"Создание кампании: {campaign_data.name}")
        
        # Проверяем существование клиента
        client_result = await db.execute(
            select(ClientModel).where(ClientModel.id == campaign_data.client_id)
        )
        client = client_result.scalar_one_or_none()
        if not client:
            raise HTTPException(status_code=404, detail="Клиент не найден")
        
        # Проверяем дубликаты по имени и клиенту
        existing_campaign = await db.execute(
            select(CampaignModel).where(
                CampaignModel.name == campaign_data.name,
                CampaignModel.client_id == campaign_data.client_id
            )
        )
        if existing_campaign.scalar_one_or_none():
            raise HTTPException(
                status_code=400, 
                detail="Кампания с таким названием уже существует для данного клиента"
            )
        
        # Создаем кампанию
        new_campaign = CampaignModel(
            **campaign_data.model_dump(),
            status="draft",
            assigned_agents=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(new_campaign)
        await db.commit()
        await db.refresh(new_campaign)
        
        # Запускаем фоновые задачи
        background_tasks.add_task(
            auto_assign_agents,
            new_campaign.id,
            manager
        )
        
        logger.info(f"Кампания создана: {new_campaign.id}")
        return new_campaign
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка создания кампании: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка создания кампании: {str(e)}")


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: uuid.UUID,
    include_client: bool = Query(False, description="Включить данные клиента"),
    include_tasks: bool = Query(False, description="Включить задачи кампании"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Получить информацию о конкретной кампании
    """
    try:
        logger.info(f"Запрос кампании: {campaign_id}")
        
        # Строим запрос с опциональным включением связанных данных
        query = select(CampaignModel).where(CampaignModel.id == campaign_id)
        
        if include_client:
            query = query.options(selectinload(CampaignModel.client))
            
        if include_tasks:
            query = query.options(selectinload(CampaignModel.tasks))
        
        result = await db.execute(query)
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Кампания не найдена")
        
        logger.info(f"Кампания найдена: {campaign.name}")
        return campaign
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения кампании {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения кампании: {str(e)}")


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: uuid.UUID,
    campaign_data: CampaignCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Обновить данные кампании
    """
    try:
        logger.info(f"Обновление кампании: {campaign_id}")
        
        # Находим кампанию
        result = await db.execute(
            select(CampaignModel).where(CampaignModel.id == campaign_id)
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Кампания не найдена")
        
        # Проверяем, что новый клиент существует (если изменился)
        if campaign_data.client_id != campaign.client_id:
            client_result = await db.execute(
                select(ClientModel).where(ClientModel.id == campaign_data.client_id)
            )
            if not client_result.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Новый клиент не найден")
        
        # Обновляем данные
        update_data = campaign_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now()
        
        await db.execute(
            update(CampaignModel)
            .where(CampaignModel.id == campaign_id)
            .values(**update_data)
        )
        await db.commit()
        
        # Возвращаем обновленную кампанию
        result = await db.execute(
            select(CampaignModel).where(CampaignModel.id == campaign_id)
        )
        updated_campaign = result.scalar_one()
        
        logger.info(f"Кампания обновлена: {campaign_id}")
        return updated_campaign
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления кампании {campaign_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления кампании: {str(e)}")


@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Удалить кампанию
    """
    try:
        logger.info(f"Удаление кампании: {campaign_id}")
        
        # Проверяем существование
        result = await db.execute(
            select(CampaignModel).where(CampaignModel.id == campaign_id)
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Кампания не найдена")
        
        # Проверяем, можно ли удалить кампанию (например, если она не активна)
        if campaign.status == "active":
            raise HTTPException(
                status_code=400,
                detail="Нельзя удалить активную кампанию. Сначала приостановите её."
            )
        
        # Удаляем кампанию (каскадное удаление задач обрабатывается БД)
        await db.execute(
            delete(CampaignModel).where(CampaignModel.id == campaign_id)
        )
        await db.commit()
        
        logger.info(f"Кампания удалена: {campaign_id}")
        return {"message": f"Кампания {campaign_id} успешно удалена"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления кампании {campaign_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка удаления кампании: {str(e)}")


@router.get("/{campaign_id}/metrics")
async def get_campaign_metrics(
    campaign_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Получить метрики кампании
    """
    try:
        logger.info(f"Запрос метрик кампании: {campaign_id}")
        
        # Проверяем существование кампании
        campaign_result = await db.execute(
            select(CampaignModel).where(CampaignModel.id == campaign_id)
        )
        campaign = campaign_result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Кампания не найдена")
        
        # Ищем метрики в базе данных
        metrics_result = await db.execute(
            select(CampaignMetricsModel).where(CampaignMetricsModel.campaign_id == campaign_id)
        )
        metrics = metrics_result.scalar_one_or_none()
        
        if not metrics:
            # Создаем пустые метрики если их нет
            metrics = CampaignMetricsModel(
                campaign_id=campaign_id,
                organic_traffic=0,
                keyword_rankings={},
                conversion_rate=0.0,
                roi_percentage=0.0,
                total_leads=0,
                qualified_leads=0,
                revenue_attributed=0.0,
                last_updated=datetime.now()
            )
            db.add(metrics)
            await db.commit()
            await db.refresh(metrics)
            
            logger.info(f"Созданы пустые метрики для кампании: {campaign_id}")
        
        return metrics
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения метрик кампании {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения метрик: {str(e)}")


@router.post("/{campaign_id}/start")
async def start_campaign(
    campaign_id: str,
    background_tasks: BackgroundTasks,
    manager = Depends(get_agent_manager)
):
    """
    Запустить кампанию
    """
    try:
        if campaign_id not in campaigns_storage:
            raise HTTPException(status_code=404, detail=f"Кампания {campaign_id} не найдена")
        
        campaign = campaigns_storage[campaign_id]
        
        if campaign.status != CampaignStatus.DRAFT:
            raise HTTPException(status_code=400, detail="Можно запустить только кампании в статусе DRAFT")
        
        # Обновляем статус
        campaign.status = CampaignStatus.ACTIVE
        campaign.start_date = datetime.now().isoformat()
        campaign.updated_at = datetime.now().isoformat()
        
        # Запускаем начальный аудит в фоновом режиме
        background_tasks.add_task(run_initial_campaign_audit, campaign_id, manager)
        
        logger.info(f"Запущена кампания: {campaign_id}")
        
        return APIResponse(
            status="success",
            message=f"Campaign {campaign_id} started successfully",
            data={"status": "active", "start_date": campaign.start_date}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка запуска кампании {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка запуска кампании: {str(e)}")


@router.post("/{campaign_id}/pause")
async def pause_campaign(campaign_id: str):
    """
    Приостановить кампанию
    """
    try:
        if campaign_id not in campaigns_storage:
            raise HTTPException(status_code=404, detail=f"Кампания {campaign_id} не найдена")
        
        campaign = campaigns_storage[campaign_id]
        
        if campaign.status != CampaignStatus.ACTIVE:
            raise HTTPException(status_code=400, detail="Можно приостановить только активные кампании")
        
        campaign.status = CampaignStatus.PAUSED
        campaign.updated_at = datetime.now().isoformat()
        
        logger.info(f"Приостановлена кампания: {campaign_id}")
        
        return APIResponse(
            status="success",
            message=f"Campaign {campaign_id} paused successfully",
            data={"status": "paused"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка приостановки кампании {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка приостановки кампании: {str(e)}")


@router.post("/{campaign_id}/resume")
async def resume_campaign(campaign_id: str):
    """
    Возобновить приостановленную кампанию
    """
    try:
        if campaign_id not in campaigns_storage:
            raise HTTPException(status_code=404, detail=f"Кампания {campaign_id} не найдена")
        
        campaign = campaigns_storage[campaign_id]
        
        if campaign.status != CampaignStatus.PAUSED:
            raise HTTPException(status_code=400, detail="Можно возобновить только приостановленные кампании")
        
        campaign.status = CampaignStatus.ACTIVE
        campaign.updated_at = datetime.now().isoformat()
        
        logger.info(f"Возобновлена кампания: {campaign_id}")
        
        return APIResponse(
            status="success",
            message=f"Campaign {campaign_id} resumed successfully",
            data={"status": "active"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка возобновления кампании {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка возобновления кампании: {str(e)}")


async def auto_assign_agents(campaign_id: str, manager):
    """
    Автоматически назначить агентов для кампании
    """
    try:
        campaign = campaigns_storage[campaign_id]
        
        # Определяем необходимых агентов на основе типа кампании
        recommended_agents = [
            "technical_seo_auditor",    # Технический аудит
            "content_strategy",         # Контентная стратегия
            "competitive_analysis",     # Анализ конкурентов
            "link_building",           # Линкбилдинг
            "reporting"                # Отчетность
        ]
        
        # Проверяем доступность агентов
        available_agents = []
        for agent_id in recommended_agents:
            if agent_id in manager.agents:
                available_agents.append(agent_id)
        
        # Назначаем агентов
        campaign.assigned_agents = available_agents
        campaign.updated_at = datetime.now().isoformat()
        
        logger.info(f"Автоматически назначены агенты для кампании {campaign_id}: {available_agents}")
        
    except Exception as e:
        logger.error(f"Ошибка автоназначения агентов для кампании {campaign_id}: {e}")


async def run_initial_campaign_audit(campaign_id: str, manager):
    """
    Запустить начальный аудит для кампании
    """
    try:
        campaign = campaigns_storage[campaign_id]
        
        # Запускаем технический аудит
        if "technical_seo_auditor" in manager.agents:
            auditor = manager.agents["technical_seo_auditor"]
            
            audit_result = await auditor.process_task({
                "input_data": {
                    "domain": campaign.domain,
                    "task_type": "initial_audit"
                }
            })
            
            logger.info(f"Выполнен начальный аудит для кампании {campaign_id}")
        
        # Запускаем анализ конкурентов
        if "competitive_analysis" in manager.agents:
            competitor_agent = manager.agents["competitive_analysis"]
            
            competitor_result = await competitor_agent.process_task({
                "input_data": {
                    "domain": campaign.domain,
                    "task_type": "competitor_research"
                }
            })
            
            logger.info(f"Выполнен анализ конкурентов для кампании {campaign_id}")
        
    except Exception as e:
        logger.error(f"Ошибка выполнения начального аудита для кампании {campaign_id}: {e}")


@router.get("/stats/summary")
async def get_campaigns_summary():
    """
    Получить общую статистику по всем кампаниям
    """
    try:
        total_campaigns = len(campaigns_storage)
        
        # Подсчитываем по статусам
        status_counts = {}
        for status in CampaignStatus:
            status_counts[status.value] = 0
        
        total_budget = 0.0
        total_revenue = 0.0
        
        for campaign in campaigns_storage.values():
            status_counts[campaign.status.value] += 1
            
            if campaign.budget:
                total_budget += campaign.budget
            
            # Добавляем revenue из метрик
            if campaign.campaign_id in campaign_metrics_storage:
                metrics = campaign_metrics_storage[campaign.campaign_id]
                total_revenue += metrics.revenue_attributed
        
        summary = {
            "total_campaigns": total_campaigns,
            "status_breakdown": status_counts,
            "total_budget": total_budget,
            "total_revenue_attributed": total_revenue,
            "roi_percentage": (total_revenue / total_budget * 100) if total_budget > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }
        
        return APIResponse(
            status="success",
            message="Campaigns summary retrieved",
            data=summary
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения статистики кампаний: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")


# Health check для кампаний
@router.get("/health/campaigns")
async def campaigns_health_check(db: AsyncSession = Depends(get_db_session)):
    """Проверка состояния системы кампаний"""
    try:
        # Проверяем подключение к базе данных
        campaigns_count = await db.execute(select(func.count(CampaignModel.id)))
        total_campaigns = campaigns_count.scalar()
        
        # Активные кампании
        active_count = await db.execute(
            select(func.count(CampaignModel.id))
            .where(CampaignModel.status == "active")
        )
        
        return {
            "status": "healthy",
            "total_campaigns": total_campaigns,
            "active_campaigns": active_count.scalar(),
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