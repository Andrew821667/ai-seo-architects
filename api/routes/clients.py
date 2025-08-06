"""
API роуты для управления клиентами
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from api.models.responses import (
    APIResponse, Client, ClientTier, PaginationParams
)
from api.monitoring.logger import get_logger
from core.mcp.agent_manager import get_mcp_agent_manager

logger = get_logger(__name__)
router = APIRouter()

# Временное хранилище клиентов (в production будет база данных)
clients_storage: Dict[str, Client] = {}


async def get_agent_manager():
    """Dependency для получения MCP Agent Manager"""
    return await get_mcp_agent_manager()


@router.get("/", response_model=List[Client])
async def list_clients(
    tier: Optional[ClientTier] = Query(None),
    industry: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100)
):
    """
    Получить список клиентов с фильтрацией и пагинацией
    """
    try:
        # Фильтруем клиентов
        filtered_clients = []
        
        for client in clients_storage.values():
            # Применяем фильтры
            if tier and client.tier != tier:
                continue
            if industry and client.industry.lower() != industry.lower():
                continue
            
            filtered_clients.append(client)
        
        # Сортируем по дате создания
        filtered_clients.sort(key=lambda x: x.created_at, reverse=True)
        
        # Пагинация
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_clients = filtered_clients[start_idx:end_idx]
        
        logger.info(f"Retrieved {len(paginated_clients)} clients", 
                   total_clients=len(filtered_clients))
        
        return paginated_clients
        
    except Exception as e:
        logger.error(f"Ошибка получения списка клиентов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения клиентов: {str(e)}")


@router.post("/", response_model=Client)
async def create_client(
    client_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    manager = Depends(get_agent_manager)
):
    """
    Создать нового клиента
    """
    try:
        # Генерируем ID клиента
        client_id = f"client_{uuid.uuid4().hex[:8]}"
        
        # Определяем tier на основе данных
        annual_revenue = client_data.get("annual_revenue", 0)
        employee_count = client_data.get("employee_count", 0)
        
        if annual_revenue >= 100000000 or employee_count >= 500:  # 100M+ revenue or 500+ employees
            tier = ClientTier.ENTERPRISE
        elif annual_revenue >= 10000000 or employee_count >= 50:  # 10M+ revenue or 50+ employees
            tier = ClientTier.SMB
        else:
            tier = ClientTier.STARTUP
        
        # Создаем клиента
        client = Client(
            client_id=client_id,
            company_name=client_data["company_name"],
            industry=client_data["industry"],
            tier=tier,
            contact_email=client_data["contact_email"],
            contact_name=client_data.get("contact_name"),
            phone=client_data.get("phone"),
            website=client_data.get("website"),
            monthly_budget=client_data.get("monthly_budget"),
            annual_revenue=annual_revenue,
            employee_count=employee_count,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Сохраняем клиента
        clients_storage[client_id] = client
        
        # Запускаем квалификацию лида в фоновом режиме
        background_tasks.add_task(qualify_new_client, client_id, client_data, manager)
        
        logger.info(f"Создан новый клиент: {client_id}", 
                   company_name=client_data["company_name"],
                   tier=tier.value)
        
        return client
        
    except Exception as e:
        logger.error(f"Ошибка создания клиента: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка создания клиента: {str(e)}")


@router.get("/{client_id}", response_model=Client)
async def get_client(client_id: str):
    """
    Получить информацию о конкретном клиенте
    """
    try:
        if client_id not in clients_storage:
            raise HTTPException(status_code=404, detail=f"Клиент {client_id} не найден")
        
        return clients_storage[client_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения клиента: {str(e)}")


@router.put("/{client_id}", response_model=Client)
async def update_client(
    client_id: str,
    update_data: Dict[str, Any]
):
    """
    Обновить данные клиента
    """
    try:
        if client_id not in clients_storage:
            raise HTTPException(status_code=404, detail=f"Клиент {client_id} не найден")
        
        client = clients_storage[client_id]
        
        # Обновляем разрешенные поля
        allowed_fields = [
            "contact_name", "contact_email", "phone", "website", 
            "monthly_budget", "annual_revenue", "employee_count"
        ]
        
        for field, value in update_data.items():
            if field in allowed_fields:
                setattr(client, field, value)
        
        # Пересчитываем tier если изменились финансовые данные
        if "annual_revenue" in update_data or "employee_count" in update_data:
            annual_revenue = client.annual_revenue or 0
            employee_count = client.employee_count or 0
            
            if annual_revenue >= 100000000 or employee_count >= 500:
                client.tier = ClientTier.ENTERPRISE
            elif annual_revenue >= 10000000 or employee_count >= 50:
                client.tier = ClientTier.SMB
            else:
                client.tier = ClientTier.STARTUP
        
        # Обновляем timestamp
        client.updated_at = datetime.now().isoformat()
        
        logger.info(f"Обновлен клиент: {client_id}")
        
        return client
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка обновления клиента: {str(e)}")


@router.delete("/{client_id}")
async def delete_client(client_id: str):
    """
    Удалить клиента
    """
    try:
        if client_id not in clients_storage:
            raise HTTPException(status_code=404, detail=f"Клиент {client_id} не найден")
        
        # Удаляем клиента
        del clients_storage[client_id]
        
        logger.info(f"Удален клиент: {client_id}")
        
        return APIResponse(
            status="success",
            message=f"Client {client_id} deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка удаления клиента: {str(e)}")


@router.post("/{client_id}/qualify")
async def qualify_client_lead(
    client_id: str,
    manager = Depends(get_agent_manager)
):
    """
    Квалифицировать лид клиента
    """
    try:
        if client_id not in clients_storage:
            raise HTTPException(status_code=404, detail=f"Клиент {client_id} не найден")
        
        client = clients_storage[client_id]
        
        # Проверяем наличие агента квалификации лидов
        if "lead_qualification" not in manager.agents:
            raise HTTPException(status_code=503, detail="Lead Qualification Agent недоступен")
        
        lead_agent = manager.agents["lead_qualification"]
        
        # Подготавливаем данные для квалификации
        lead_data = {
            "company_data": {
                "company_name": client.company_name,
                "industry": client.industry,
                "annual_revenue": str(client.annual_revenue) if client.annual_revenue else "unknown",
                "employee_count": str(client.employee_count) if client.employee_count else "unknown",
                "website_domain": client.website if client.website else "unknown",
                "current_seo_spend": str(client.monthly_budget * 12) if client.monthly_budget else "unknown"
            }
        }
        
        # Запускаем квалификацию
        result = await lead_agent.process_task({
            "input_data": lead_data
        })
        
        # Обновляем данные клиента на основе результатов квалификации
        if result.get("success") and result.get("result"):
            qualification_result = result["result"]
            
            # Сохраняем score и другие метрики
            # (В реальном проекте это будет отдельная таблица lead_qualifications)
            
            logger.info(f"Квалификация лида завершена для клиента {client_id}",
                       lead_score=qualification_result.get("lead_score"))
        
        return APIResponse(
            status="success",
            message=f"Lead qualification completed for client {client_id}",
            data=result.get("result", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка квалификации лида для клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка квалификации лида: {str(e)}")


@router.post("/{client_id}/proposal")
async def generate_client_proposal(
    client_id: str,
    manager = Depends(get_agent_manager)
):
    """
    Сгенерировать коммерческое предложение для клиента
    """
    try:
        if client_id not in clients_storage:
            raise HTTPException(status_code=404, detail=f"Клиент {client_id} не найден")
        
        client = clients_storage[client_id]
        
        # Проверяем наличие агента генерации предложений
        if "proposal_generation" not in manager.agents:
            raise HTTPException(status_code=503, detail="Proposal Generation Agent недоступен")
        
        proposal_agent = manager.agents["proposal_generation"]
        
        # Подготавливаем данные для генерации предложения
        proposal_data = {
            "company_data": {
                "company_name": client.company_name,
                "industry": client.industry,
                "annual_revenue": str(client.annual_revenue) if client.annual_revenue else "unknown",
                "employee_count": str(client.employee_count) if client.employee_count else "unknown",
                "website_domain": client.website if client.website else "unknown",
                "monthly_budget": str(client.monthly_budget) if client.monthly_budget else "unknown"
            }
        }
        
        # Генерируем предложение
        result = await proposal_agent.process_task({
            "input_data": proposal_data
        })
        
        logger.info(f"Сгенерировано предложение для клиента {client_id}")
        
        return APIResponse(
            status="success",
            message=f"Proposal generated for client {client_id}",
            data=result.get("result", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка генерации предложения для клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка генерации предложения: {str(e)}")


@router.get("/{client_id}/campaigns")
async def get_client_campaigns(client_id: str):
    """
    Получить кампании клиента
    """
    try:
        if client_id not in clients_storage:
            raise HTTPException(status_code=404, detail=f"Клиент {client_id} не найден")
        
        # Импортируем хранилище кампаний
        from api.routes.campaigns import campaigns_storage
        
        # Находим кампании клиента
        client_campaigns = [
            campaign for campaign in campaigns_storage.values()
            if campaign.client_id == client_id
        ]
        
        # Сортируем по дате создания
        client_campaigns.sort(key=lambda x: x.created_at, reverse=True)
        
        return APIResponse(
            status="success",
            message=f"Campaigns for client {client_id}",
            data={
                "campaigns": [campaign.dict() for campaign in client_campaigns],
                "total_campaigns": len(client_campaigns)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения кампаний клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения кампаний: {str(e)}")


async def qualify_new_client(client_id: str, client_data: Dict[str, Any], manager):
    """
    Автоматическая квалификация нового клиента в фоновом режиме
    """
    try:
        # Проверяем наличие агента квалификации
        if "lead_qualification" not in manager.agents:
            logger.warning(f"Lead Qualification Agent недоступен для клиента {client_id}")
            return
        
        lead_agent = manager.agents["lead_qualification"]
        
        # Подготавливаем данные
        lead_data = {
            "company_data": {
                "company_name": client_data["company_name"],
                "industry": client_data["industry"],
                "annual_revenue": str(client_data.get("annual_revenue", "unknown")),
                "employee_count": str(client_data.get("employee_count", "unknown")),
                "website_domain": client_data.get("website", "unknown"),
                "current_seo_spend": str(client_data.get("monthly_budget", 0) * 12) if client_data.get("monthly_budget") else "unknown"
            }
        }
        
        # Запускаем квалификацию
        result = await lead_agent.process_task({
            "input_data": lead_data
        })
        
        if result.get("success") and result.get("result"):
            qualification_result = result["result"]
            lead_score = qualification_result.get("lead_score", 0)
            
            logger.info(f"Автоквалификация завершена для клиента {client_id}",
                       lead_score=lead_score,
                       quality=qualification_result.get("lead_quality"))
        
    except Exception as e:
        logger.error(f"Ошибка автоквалификации клиента {client_id}: {e}")


@router.get("/stats/summary")
async def get_clients_summary():
    """
    Получить общую статистику по всем клиентам
    """
    try:
        total_clients = len(clients_storage)
        
        # Подсчитываем по tier
        tier_counts = {}
        for tier in ClientTier:
            tier_counts[tier.value] = 0
        
        # Подсчитываем по индустриям
        industry_counts = {}
        total_budget = 0.0
        total_revenue = 0.0
        
        for client in clients_storage.values():
            tier_counts[client.tier.value] += 1
            
            # Индустрии
            industry = client.industry.lower()
            industry_counts[industry] = industry_counts.get(industry, 0) + 1
            
            # Бюджеты
            if client.monthly_budget:
                total_budget += client.monthly_budget * 12  # Годовой бюджет
            
            if client.annual_revenue:
                total_revenue += client.annual_revenue
        
        # Топ-5 индустрий
        top_industries = sorted(industry_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary = {
            "total_clients": total_clients,
            "tier_breakdown": tier_counts,
            "top_industries": dict(top_industries),
            "total_annual_budget": total_budget,
            "total_client_revenue": total_revenue,
            "average_client_value": total_budget / total_clients if total_clients > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }
        
        return APIResponse(
            status="success",
            message="Clients summary retrieved",
            data=summary
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения статистики клиентов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")