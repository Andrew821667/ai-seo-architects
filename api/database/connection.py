"""
Database connection management для AI SEO Architects
Поддержка асинхронного PostgreSQL через SQLAlchemy 2.0
"""

import os
from typing import AsyncGenerator, Optional, Dict, Any
import logging

# Проверяем доступность SQLAlchemy и asyncpg
try:
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
    from sqlalchemy.ext.asyncio import async_sessionmaker
    from sqlalchemy.orm import DeclarativeBase
    from sqlalchemy import text
    import asyncpg
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    
    # Mock базы данных для случаев когда PostgreSQL/asyncpg недоступны
    class MockAsyncSession:
        """Mock AsyncSession для fallback режима"""
        def __init__(self):
            self._data = {}
        
        async def execute(self, query, params=None):
            # Mock результат
            class MockResult:
                def scalar_one_or_none(self):
                    return None
                def scalars(self):
                    return MockScalars()
                def fetchall(self):
                    return []
            return MockResult()
        
        def add(self, obj):
            pass
        
        async def commit(self):
            pass
        
        async def rollback(self):
            pass
        
        async def close(self):
            pass
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, *args):
            pass
    
    class MockScalars:
        def all(self):
            return []
        
        def first(self):
            return None
    
    class MockEngine:
        async def dispose(self):
            pass
    
    # Создаем заглушки
    AsyncSession = MockAsyncSession
    AsyncEngine = MockEngine
    create_async_engine = lambda *args, **kwargs: MockEngine()
    async_sessionmaker = lambda *args, **kwargs: lambda: MockAsyncSession()
    
    class DeclarativeBase:
        pass
    
    def text(query: str):
        return query

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    pass


class DatabaseManager:
    """Менеджер базы данных с connection pooling"""
    
    def __init__(self):
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker] = None
        self._initialized = False
    
    async def initialize(self, database_url: str = None):
        """Инициализация подключения к базе данных"""
        if self._initialized:
            return
            
        if not DATABASE_AVAILABLE:
            logger.warning("PostgreSQL/asyncpg недоступен, используем mock базу данных")
            # Инициализируем mock версию
            self.engine = create_async_engine()  # Возвращает MockEngine
            self.session_factory = async_sessionmaker()  # Возвращает mock фабрику
            self._initialized = True
            return
            
        # Получение URL базы данных
        if not database_url:
            database_url = self._get_database_url()
        
        # Создание асинхронного engine
        self.engine = create_async_engine(
            database_url,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true",
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,  # 1 час
            connect_args={
                "server_settings": {
                    "application_name": "ai_seo_architects",
                }
            }
        )
        
        # Создание фабрики сессий
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        self._initialized = True
        logger.info("✅ База данных инициализирована")
    
    def _get_database_url(self) -> str:
        """Получение URL базы данных из переменных окружения"""
        # Production режим (Docker)
        if os.getenv("ENVIRONMENT") == "production":
            return (
                f"postgresql+asyncpg://"
                f"{os.getenv('POSTGRES_USER', 'ai_seo_user')}:"
                f"{os.getenv('POSTGRES_PASSWORD', 'secure_password_change_me')}@"
                f"{os.getenv('POSTGRES_HOST', 'postgres')}:"
                f"{os.getenv('POSTGRES_PORT', '5432')}/"
                f"{os.getenv('POSTGRES_DB', 'ai_seo_architects')}"
            )
        
        # Development режим
        return (
            f"postgresql+asyncpg://"
            f"{os.getenv('DEV_POSTGRES_USER', 'postgres')}:"
            f"{os.getenv('DEV_POSTGRES_PASSWORD', 'postgres')}@"
            f"{os.getenv('DEV_POSTGRES_HOST', 'localhost')}:"
            f"{os.getenv('DEV_POSTGRES_PORT', '5432')}/"
            f"{os.getenv('DEV_POSTGRES_DB', 'ai_seo_architects_dev')}"
        )
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получение сессии базы данных"""
        if not self._initialized:
            await self.initialize()
            
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def health_check(self) -> bool:
        """Проверка состояния базы данных"""
        try:
            if not self._initialized:
                return False
            
            if not DATABASE_AVAILABLE:
                # Mock база всегда "здорова"
                return True
                
            async with self.session_factory() as session:
                result = await session.execute(text("SELECT 1"))
                return result.scalar() == 1
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def close(self):
        """Закрытие всех подключений"""
        if self.engine:
            await self.engine.dispose()
            self._initialized = False
            logger.info("🔒 База данных отключена")


# Глобальный экземпляр менеджера базы данных
db_manager = DatabaseManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для получения сессии базы данных в FastAPI"""
    async for session in db_manager.get_session():
        yield session


async def init_database():
    """Инициализация базы данных при запуске приложения"""
    await db_manager.initialize()


async def close_database():
    """Закрытие базы данных при остановке приложения"""
    await db_manager.close()