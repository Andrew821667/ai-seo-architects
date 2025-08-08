"""
API роуты для управления клиентами с PostgreSQL интеграцией
Реальная база данных вместо in-memory storage
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from api.database.connection import get_db_session
from api.database.models import (
    Client as ClientModel, 
    ClientCreate, 
    ClientResponse,
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


@router.get("/", response_model=List[ClientResponse])
async def list_clients(
    industry: Optional[str] = Query(None, description="Фильтр по отрасли"),
    country: Optional[str] = Query(None, description="Фильтр по стране"),
    min_revenue: Optional[int] = Query(None, description="Минимальная выручка"),
    max_revenue: Optional[int] = Query(None, description="Максимальная выручка"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Получить список клиентов с фильтрацией и пагинацией
    Использует реальную PostgreSQL базу данных
    """
    try:
        logger.info(f"Запрос списка клиентов: industry={industry}, page={page}, size={size}")
        
        # Строим базовый запрос
        query = select(ClientModel).order_by(ClientModel.created_at.desc())
        
        # Применяем фильтры
        if industry:
            query = query.where(ClientModel.industry.ilike(f"%{industry}%"))
        
        if country:
            query = query.where(ClientModel.country == country)
            
        if min_revenue:
            query = query.where(ClientModel.annual_revenue >= min_revenue)
            
        if max_revenue:
            query = query.where(ClientModel.annual_revenue <= max_revenue)
        
        # Применяем пагинацию
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        
        # Выполняем запрос
        result = await db.execute(query)
        clients = result.scalars().all()
        
        logger.info(f"Найдено клиентов: {len(clients)}")
        return clients
        
    except Exception as e:
        logger.error(f"Ошибка получения списка клиентов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения клиентов: {str(e)}")


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: uuid.UUID,
    include_campaigns: bool = Query(False, description="Включить кампании клиента"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Получить клиента по ID
    """
    try:
        logger.info(f"Запрос клиента: {client_id}")
        
        # Строим запрос с возможным включением кампаний
        query = select(ClientModel).where(ClientModel.id == client_id)
        
        if include_campaigns:
            query = query.options(selectinload(ClientModel.campaigns))
        
        result = await db.execute(query)
        client = result.scalar_one_or_none()
        
        if not client:
            raise HTTPException(status_code=404, detail="Клиент не найден")
        
        logger.info(f"Клиент найден: {client.company_name}")
        return client
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения клиента: {str(e)}")


@router.post("/", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session),
    agent_manager = Depends(get_agent_manager)
):
    """
    Создать нового клиента
    Запускает фоновую задачу анализа клиента
    """
    try:
        logger.info(f"Создание клиента: {client_data.company_name}")
        
        # Проверяем дубликаты
        existing_client = await db.execute(
            select(ClientModel).where(ClientModel.company_name == client_data.company_name)
        )
        if existing_client.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Клиент с таким названием уже существует")
        
        # Создаем клиента
        new_client = ClientModel(
            **client_data.model_dump(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(new_client)
        await db.commit()
        await db.refresh(new_client)
        
        # Запускаем фоновый анализ клиента
        background_tasks.add_task(
            analyze_new_client,
            new_client.id,
            agent_manager
        )
        
        logger.info(f"Клиент создан: {new_client.id}")
        return new_client
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка создания клиента: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка создания клиента: {str(e)}")


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: uuid.UUID,
    client_data: ClientCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Обновить данные клиента
    """
    try:
        logger.info(f"Обновление клиента: {client_id}")
        
        # Находим клиента
        result = await db.execute(select(ClientModel).where(ClientModel.id == client_id))
        client = result.scalar_one_or_none()
        
        if not client:
            raise HTTPException(status_code=404, detail="Клиент не найден")
        
        # Обновляем данные
        update_data = client_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now()
        
        await db.execute(
            update(ClientModel)
            .where(ClientModel.id == client_id)
            .values(**update_data)
        )
        await db.commit()
        
        # Возвращаем обновленного клиента
        result = await db.execute(select(ClientModel).where(ClientModel.id == client_id))
        updated_client = result.scalar_one()
        
        logger.info(f"Клиент обновлен: {client_id}")
        return updated_client
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления клиента {client_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления клиента: {str(e)}")


@router.delete("/{client_id}")
async def delete_client(
    client_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Удалить клиента
    """
    try:
        logger.info(f"Удаление клиента: {client_id}")
        
        # Проверяем существование
        result = await db.execute(select(ClientModel).where(ClientModel.id == client_id))
        client = result.scalar_one_or_none()
        
        if not client:
            raise HTTPException(status_code=404, detail="Клиент не найден")
        
        # Проверяем активные кампании
        campaigns_count = await db.execute(
            select(func.count(CampaignModel.id))
            .where(CampaignModel.client_id == client_id)
            .where(CampaignModel.status.in_(["active", "draft"]))
        )
        
        if campaigns_count.scalar() > 0:
            raise HTTPException(
                status_code=400, 
                detail="Нельзя удалить клиента с активными кампаниями"
            )
        
        # Удаляем клиента
        await db.execute(delete(ClientModel).where(ClientModel.id == client_id))
        await db.commit()
        
        logger.info(f"Клиент удален: {client_id}")
        return {"message": f"Клиент {client_id} успешно удален"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления клиента {client_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка удаления клиента: {str(e)}")


@router.get("/{client_id}/campaigns")
async def get_client_campaigns(
    client_id: uuid.UUID,
    status: Optional[str] = Query(None, description="Фильтр по статусу кампании"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Получить кампании клиента
    """
    try:
        logger.info(f"Запрос кампаний клиента: {client_id}")
        
        # Проверяем существование клиента
        client_result = await db.execute(select(ClientModel).where(ClientModel.id == client_id))
        if not client_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Клиент не найден")
        
        # Получаем кампании
        query = select(CampaignModel).where(CampaignModel.client_id == client_id)
        
        if status:
            query = query.where(CampaignModel.status == status)
        
        result = await db.execute(query)
        campaigns = result.scalars().all()
        
        logger.info(f"Найдено кампаний: {len(campaigns)}")
        return campaigns
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения кампаний клиента {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения кампаний: {str(e)}")


@router.get("/stats/overview")
async def get_clients_stats(
    db: AsyncSession = Depends(get_db_session)
):
    """
    Получить общую статистику по клиентам
    """
    try:
        logger.info("Запрос статистики клиентов")
        
        # Общее количество клиентов
        total_clients = await db.execute(select(func.count(ClientModel.id)))
        total_count = total_clients.scalar()
        
        # Статистика по отраслям
        industry_stats = await db.execute(
            select(ClientModel.industry, func.count(ClientModel.id))
            .group_by(ClientModel.industry)
            .order_by(func.count(ClientModel.id).desc())
        )
        
        # Статистика по странам
        country_stats = await db.execute(
            select(ClientModel.country, func.count(ClientModel.id))
            .group_by(ClientModel.country)
            .order_by(func.count(ClientModel.id).desc())
        )
        
        # Средняя выручка
        avg_revenue = await db.execute(
            select(func.avg(ClientModel.annual_revenue))
            .where(ClientModel.annual_revenue.is_not(None))
        )
        
        stats = {
            "total_clients": total_count,
            "by_industry": [
                {"industry": row[0] or "Не указано", "count": row[1]}
                for row in industry_stats.all()
            ],
            "by_country": [
                {"country": row[0], "count": row[1]}
                for row in country_stats.all()
            ],
            "average_revenue": avg_revenue.scalar() or 0
        }
        
        logger.info(f"Статистика получена: {total_count} клиентов")
        return stats
        
    except Exception as e:
        logger.error(f"Ошибка получения статистики клиентов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")


async def analyze_new_client(client_id: uuid.UUID, agent_manager):
    """
    Фоновая задача анализа нового клиента
    """
    try:
        logger.info(f"Запуск анализа клиента: {client_id}")
        
        # Получаем business development директора
        bd_agent = await agent_manager.get_agent("business_development_director")
        
        if bd_agent:
            # Анализируем клиента
            analysis_result = await bd_agent.process_task({
                "task": "analyze_new_client",
                "client_id": str(client_id),
                "analysis_type": "comprehensive"
            })
            
            logger.info(f"Анализ клиента {client_id} завершен: {analysis_result.get('success', False)}")
        else:
            logger.warning(f"Business Development Director недоступен для анализа {client_id}")
            
    except Exception as e:
        logger.error(f"Ошибка анализа клиента {client_id}: {e}")


# Health check для клиентов
@router.get("/health/clients")
async def clients_health_check(db: AsyncSession = Depends(get_db_session)):
    """Проверка состояния системы клиентов"""
    try:
        # Проверяем подключение к базе данных
        result = await db.execute(select(func.count(ClientModel.id)))
        clients_count = result.scalar()
        
        return {
            "status": "healthy",
            "total_clients": clients_count,
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