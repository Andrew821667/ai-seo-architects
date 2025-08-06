"""
API роуты для управления SEO кампаниями
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid

from api.models.responses import (
    APIResponse, Campaign, CampaignMetrics, CampaignStatus,
    PaginationParams, CampaignFilters
)
from api.monitoring.logger import get_logger
from core.mcp.agent_manager import get_mcp_agent_manager

logger = get_logger(__name__)
router = APIRouter()

# Временное хранилище кампаний (в production будет база данных)
campaigns_storage: Dict[str, Campaign] = {}
campaign_metrics_storage: Dict[str, CampaignMetrics] = {}


async def get_agent_manager():
    """Dependency для получения MCP Agent Manager"""
    return await get_mcp_agent_manager()


@router.get("/", response_model=List[Campaign])
async def list_campaigns(
    status: Optional[List[CampaignStatus]] = Query(None),
    client_id: Optional[str] = Query(None),
    domain: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100)
):
    """
    Получить список SEO кампаний с фильтрацией и пагинацией
    """
    try:
        # Фильтруем кампании
        filtered_campaigns = []
        
        for campaign in campaigns_storage.values():
            # Применяем фильтры
            if status and campaign.status not in status:
                continue
            if client_id and campaign.client_id != client_id:
                continue
            if domain and campaign.domain != domain:
                continue
            
            filtered_campaigns.append(campaign)
        
        # Сортируем по дате создания
        filtered_campaigns.sort(key=lambda x: x.created_at, reverse=True)
        
        # Пагинация
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_campaigns = filtered_campaigns[start_idx:end_idx]
        
        logger.info(f"Retrieved {len(paginated_campaigns)} campaigns", 
                   total_campaigns=len(filtered_campaigns))
        
        return paginated_campaigns
        
    except Exception as e:
        logger.error(f"Ошибка получения списка кампаний: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения кампаний: {str(e)}")


@router.post("/", response_model=Campaign)
async def create_campaign(
    campaign_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    manager = Depends(get_agent_manager)
):
    """
    Создать новую SEO кампанию
    """
    try:
        # Генерируем ID кампании
        campaign_id = f"camp_{uuid.uuid4().hex[:8]}"
        
        # Создаем кампанию
        campaign = Campaign(
            campaign_id=campaign_id,
            client_id=campaign_data["client_id"],
            name=campaign_data["name"],
            description=campaign_data.get("description"),
            status=CampaignStatus.DRAFT,
            domain=campaign_data["domain"],
            keywords=campaign_data.get("keywords", []),
            budget=campaign_data.get("budget"),
            start_date=campaign_data.get("start_date", datetime.now().isoformat()),
            end_date=campaign_data.get("end_date"),
            assigned_agents=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Сохраняем кампанию
        campaigns_storage[campaign_id] = campaign
        
        # Инициализируем метрики кампании
        metrics = CampaignMetrics(
            campaign_id=campaign_id,
            organic_traffic=0,
            keyword_rankings={},
            conversion_rate=0.0,
            roi_percentage=0.0,
            total_leads=0,
            qualified_leads=0,
            revenue_attributed=0.0,
            last_updated=datetime.now().isoformat()
        )
        campaign_metrics_storage[campaign_id] = metrics
        
        # Автоматически назначаем агентов в фоновом режиме
        background_tasks.add_task(auto_assign_agents, campaign_id, manager)
        
        logger.info(f"Создана новая кампания: {campaign_id}", 
                   client_id=campaign_data["client_id"],
                   domain=campaign_data["domain"])
        
        return campaign
        
    except Exception as e:
        logger.error(f"Ошибка создания кампании: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка создания кампании: {str(e)}")


@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: str):
    """
    Получить информацию о конкретной кампании
    """
    try:
        if campaign_id not in campaigns_storage:
            raise HTTPException(status_code=404, detail=f"Кампания {campaign_id} не найдена")
        
        return campaigns_storage[campaign_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения кампании {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения кампании: {str(e)}")


@router.put("/{campaign_id}", response_model=Campaign)
async def update_campaign(
    campaign_id: str,
    update_data: Dict[str, Any]
):
    """
    Обновить данные кампании
    """
    try:
        if campaign_id not in campaigns_storage:
            raise HTTPException(status_code=404, detail=f"Кампания {campaign_id} не найдена")
        
        campaign = campaigns_storage[campaign_id]
        
        # Обновляем разрешенные поля
        allowed_fields = ["name", "description", "status", "keywords", "budget", "end_date"]
        
        for field, value in update_data.items():
            if field in allowed_fields:
                setattr(campaign, field, value)
        
        # Обновляем timestamp
        campaign.updated_at = datetime.now().isoformat()
        
        logger.info(f"Обновлена кампания: {campaign_id}")
        
        return campaign
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления кампании {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка обновления кампании: {str(e)}")


@router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: str):
    """
    Удалить кампанию
    """
    try:
        if campaign_id not in campaigns_storage:
            raise HTTPException(status_code=404, detail=f"Кампания {campaign_id} не найдена")
        
        # Удаляем кампанию и её метрики
        del campaigns_storage[campaign_id]
        if campaign_id in campaign_metrics_storage:
            del campaign_metrics_storage[campaign_id]
        
        logger.info(f"Удалена кампания: {campaign_id}")
        
        return APIResponse(
            status="success",
            message=f"Campaign {campaign_id} deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления кампании {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка удаления кампании: {str(e)}")


@router.get("/{campaign_id}/metrics", response_model=CampaignMetrics)
async def get_campaign_metrics(campaign_id: str):
    """
    Получить метрики кампании
    """
    try:
        if campaign_id not in campaigns_storage:
            raise HTTPException(status_code=404, detail=f"Кампания {campaign_id} не найдена")
        
        if campaign_id not in campaign_metrics_storage:
            # Создаем пустые метрики если их нет
            metrics = CampaignMetrics(
                campaign_id=campaign_id,
                organic_traffic=0,
                keyword_rankings={},
                conversion_rate=0.0,
                roi_percentage=0.0,
                total_leads=0,
                qualified_leads=0,
                revenue_attributed=0.0,
                last_updated=datetime.now().isoformat()
            )
            campaign_metrics_storage[campaign_id] = metrics
        
        return campaign_metrics_storage[campaign_id]
        
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