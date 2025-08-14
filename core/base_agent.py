"""
Базовый класс для всех AI-агентов с поддержкой MCP (Model Context Protocol) и RAG
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime
import asyncio
import time
import logging
from functools import wraps
import openai
import os

# Избегаем circular imports
if TYPE_CHECKING:
    from core.mcp.data_provider import MCPDataProvider

logger = logging.getLogger(__name__)


def with_retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0, timeout: float = 30.0):
    """
    Декоратор для retry логики с exponential backoff и timeout
    
    Args:
        max_attempts: Максимальное количество попыток
        delay: Начальная задержка между попытками (секунды)
        backoff: Множитель для exponential backoff
        timeout: Общий timeout для всех попыток (секунды)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            current_delay = delay
            
            for attempt in range(max_attempts):
                # Проверяем общий timeout
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"Operation timed out after {timeout}s")
                
                try:
                    # Выполняем функцию с индивидуальным timeout
                    remaining_timeout = timeout - (time.time() - start_time)
                    if remaining_timeout <= 0:
                        raise TimeoutError("No time remaining for operation")
                    
                    result = await asyncio.wait_for(func(*args, **kwargs), timeout=remaining_timeout)
                    return result
                    
                except (asyncio.TimeoutError, TimeoutError) as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"Final timeout in {func.__name__} after {attempt + 1} attempts: {str(e)}")
                        raise TimeoutError(f"Operation failed after {max_attempts} attempts: timeout")
                    
                    logger.warning(f"Timeout in {func.__name__} (attempt {attempt + 1}), retrying...")
                    
                except Exception as e:
                    if attempt == max_attempts - 1:
                        logger.error(f"Final error in {func.__name__} after {attempt + 1} attempts: {str(e)}")
                        raise
                    
                    # Логируем ошибку и продолжаем
                    logger.warning(f"Error in {func.__name__} (attempt {attempt + 1}): {str(e)}, retrying...")
                
                # Ждем перед следующей попыткой (если это не последняя попытка)
                if attempt < max_attempts - 1:
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            
            # Этот код не должен выполняться, но на всякий случай
            raise RuntimeError(f"Unexpected end of retry loop in {func.__name__}")
        
        return wrapper
    return decorator


class AgentMetrics:
    """Метрики производительности агента"""
    
    def __init__(self):
        self.tasks_processed = 0
        self.tasks_successful = 0
        self.tasks_failed = 0
        self.total_processing_time = 0.0
        self.last_activity = None
    
    def record_task(self, success: bool, processing_time: float):
        """Записываем метрики выполнения задачи"""
        self.tasks_processed += 1
        if success:
            self.tasks_successful += 1
        else:
            self.tasks_failed += 1
        self.total_processing_time += processing_time
        self.last_activity = datetime.now()
    
    def get_success_rate(self) -> float:
        """Процент успешных задач"""
        if self.tasks_processed == 0:
            return 0.0
        return self.tasks_successful / self.tasks_processed
    
    def get_avg_processing_time(self) -> float:
        """Среднее время обработки задачи"""
        if self.tasks_processed == 0:
            return 0.0
        return self.total_processing_time / self.tasks_processed
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "tasks_processed": self.tasks_processed,
            "tasks_successful": self.tasks_successful,
            "tasks_failed": self.tasks_failed,
            "success_rate": self.get_success_rate(),
            "avg_processing_time": self.get_avg_processing_time(),
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }


class BaseAgent(ABC):
    """Базовый класс для всех AI-агентов с поддержкой MCP, retries и timeouts"""
    
    def __init__(self, 
                 agent_id: str,
                 name: str,
                 agent_level: str,  # executive, management, operational
                 data_provider=None,  # Может быть MockDataProvider или MCPDataProvider
                 knowledge_base: Optional[str] = None,
                 model_name: Optional[str] = None,
                 mcp_enabled: bool = False,
                 rag_enabled: bool = True,
                 # Retry и timeout настройки
                 retry_attempts: int = 3,
                 retry_delay: float = 1.0,
                 retry_backoff: float = 2.0,
                 task_timeout: float = 30.0,
                 data_timeout: float = 15.0,
                 **kwargs):  # Принимаем дополнительные параметры
        self.agent_id = agent_id
        self.name = name
        self.agent_level = agent_level
        self.data_provider = data_provider
        self.model_name = model_name or "gpt-4o-mini"
        self.knowledge_base = knowledge_base
        self.context = {}
        self.metrics = AgentMetrics()
        self.mcp_enabled = mcp_enabled
        self.mcp_context = {}
        self.rag_enabled = rag_enabled
        self.knowledge_context = ""  # Контекст знаний для текущей задачи
        
        # Retry и timeout конфигурация
        self.retry_config = {
            "max_attempts": retry_attempts,
            "delay": retry_delay,
            "backoff": retry_backoff,
            "task_timeout": task_timeout,
            "data_timeout": data_timeout
        }
        
        # Дополнительные параметры сохраняем в context
        self.context.update(kwargs)
        
        # Инициализация MCP контекста если включен
        if self.mcp_enabled:
            self._initialize_mcp_context()
            
        # Инициализация RAG если включен
        if self.rag_enabled:
            self._initialize_rag_knowledge()
            
        # Инициализация OpenAI клиента
        self._initialize_openai_client()
    
    async def process_task_with_retry(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обертка для выполнения задач с retry логикой и метриками
        
        Args:
            task_data: Данные задачи для обработки
            
        Returns:
            Dict с результатами обработки
        """
        start_time = time.time()
        
        # Применяем retry с конфигурацией агента
        retry_decorator = with_retry(
            max_attempts=self.retry_config["max_attempts"],
            delay=self.retry_config["delay"],
            backoff=self.retry_config["backoff"],
            timeout=self.retry_config["task_timeout"]
        )
        
        try:
            # Выполняем задачу с retry логикой
            result = await retry_decorator(self.process_task)(task_data)
            
            # Записываем успешные метрики
            processing_time = time.time() - start_time
            self.metrics.record_task(True, processing_time)
            
            # Добавляем метаданные в результат
            if isinstance(result, dict):
                result.update({
                    "processing_time": processing_time,
                    "retry_attempts_used": 1,  # Минимум 1 попытка
                    "success": True
                })
            
            return result
            
        except Exception as e:
            # Записываем метрики ошибки
            processing_time = time.time() - start_time
            self.metrics.record_task(False, processing_time)
            
            logger.error(f"Task failed in agent {self.agent_id} after retries: {str(e)}")
            
            # Возвращаем структурированный ответ об ошибке
            return {
                "success": False,
                "agent": self.agent_id,
                "error": str(e),
                "error_type": type(e).__name__,
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat()
            }
    
    def _initialize_openai_client(self):
        """Инициализация OpenAI клиента"""
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if not openai.api_key:
                logger.warning(f"⚠️ OPENAI_API_KEY не установлен для агента {self.agent_id}")
                self.openai_client = None
            else:
                self.openai_client = openai.AsyncOpenAI(api_key=openai.api_key)
                logger.info(f"✅ OpenAI клиент инициализирован для {self.agent_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации OpenAI для {self.agent_id}: {e}")
            self.openai_client = None
    
    def get_system_prompt(self) -> str:
        """
        Базовый системный промпт (должен быть переопределен в наследниках)
        
        Returns:
            str: Системный промпт для агента
        """
        return f"""Ты - {self.name}, специализированный AI-агент уровня {self.agent_level}.
Твоя задача - выполнять задачи в рамках своей экспертизы с высоким качеством и профессионализмом.

ТВОИ ХАРАКТЕРИСТИКИ:
- Уровень: {self.agent_level}
- Специализация: {self.name}
- ID: {self.agent_id}

ИНСТРУКЦИИ:
1. Всегда отвечай профессионально и по существу
2. Используй свою экспертизу для качественного анализа
3. Форматируй ответ в JSON структуре
4. Будь конкретен и предоставляй actionable insights"""

    async def call_openai(self, messages: list, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Вызов OpenAI API с retry логикой
        
        Args:
            messages: Список сообщений для ChatGPT
            temperature: Параметр креативности (0.0-1.0)
            
        Returns:
            Dict с ответом от OpenAI
        """
        if not self.openai_client:
            return {
                "success": False,
                "error": "OpenAI client not initialized",
                "content": "Mock response - OpenAI не доступен"
            }
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            
            return {
                "success": True,
                "content": content,
                "model": self.model_name,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI API ошибка для {self.agent_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": f"Ошибка вызова OpenAI: {str(e)}"
            }

    async def process_with_llm(self, user_prompt: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка задачи с помощью LLM
        
        Args:
            user_prompt: Промпт пользователя
            task_data: Данные задачи
            
        Returns:
            Dict с результатом обработки
        """
        # Получаем контекст знаний если RAG включен
        knowledge_context = ""
        if self.rag_enabled:
            query = f"{user_prompt} {str(task_data)}"
            knowledge_context = await self.get_knowledge_context(query, k=3)
        
        # Формируем сообщения для ChatGPT
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": self.format_prompt_with_rag(user_prompt, task_data)}
        ]
        
        # Вызываем OpenAI API
        llm_response = await self.call_openai(messages)
        
        if llm_response["success"]:
            return {
                "success": True,
                "agent": self.agent_id,
                "result": llm_response["content"],
                "model_used": llm_response.get("model"),
                "tokens_used": llm_response.get("usage", {}),
                "knowledge_context_length": len(knowledge_context),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "agent": self.agent_id,
                "error": llm_response["error"],
                "fallback_result": f"Fallback ответ для {self.name}: задача требует ручной обработки",
                "timestamp": datetime.now().isoformat()
            }

    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика обработки задачи агентом (должна быть переопределена в наследниках)
        
        Args:
            task_data: Данные задачи для обработки
            
        Returns:
            Dict с результатами обработки, должен содержать:
            - success: bool - статус выполнения
            - agent: str - ID агента
            - timestamp: str - время выполнения
            - другие поля специфичные для агента
        """
        pass
    
    @with_retry()
    async def get_seo_data(self, domain: str, parameters: Dict[str, Any] = None):
        """Получение SEO данных через провайдер с retry логикой (MCP-compatible)"""
        return await self._get_seo_data_internal(domain, parameters)
    
    async def _get_seo_data_internal(self, domain: str, parameters: Dict[str, Any] = None):
        """Внутренний метод получения SEO данных"""
        if self.mcp_enabled and hasattr(self.data_provider, 'get_seo_data'):
            return await self.data_provider.get_seo_data(domain, parameters or {})
        elif hasattr(self.data_provider, 'get_seo_data'):
            return await self.data_provider.get_seo_data(domain)
        else:
            # Fallback для совместимости
            return {"domain": domain, "source": "fallback", "status": "no_provider"}
    
    @with_retry()
    async def get_client_data(self, client_id: str, parameters: Dict[str, Any] = None):
        """Получение данных клиента через провайдер с retry логикой (MCP-compatible)"""
        return await self._get_client_data_internal(client_id, parameters)
    
    async def _get_client_data_internal(self, client_id: str, parameters: Dict[str, Any] = None):
        """Внутренний метод получения данных клиента"""
        if self.mcp_enabled and hasattr(self.data_provider, 'get_client_data'):
            return await self.data_provider.get_client_data(client_id, parameters or {})
        elif hasattr(self.data_provider, 'get_client_data'):
            return await self.data_provider.get_client_data(client_id)
        else:
            # Fallback для совместимости
            return {"client_id": client_id, "source": "fallback", "status": "no_provider"}
    
    @with_retry()
    async def get_competitive_data(self, domain: str, competitors: list, parameters: Dict[str, Any] = None):
        """Получение конкурентных данных с retry логикой через MCP провайдер"""
        return await self._get_competitive_data_internal(domain, competitors, parameters)
    
    async def _get_competitive_data_internal(self, domain: str, competitors: list, parameters: Dict[str, Any] = None):
        """Внутренний метод получения конкурентных данных"""
        if self.mcp_enabled and hasattr(self.data_provider, 'get_competitive_data'):
            return await self.data_provider.get_competitive_data(domain, competitors, parameters or {})
        else:
            # Fallback данные для совместимости
            return {
                "domain": domain,
                "competitors": competitors,
                "source": "fallback",
                "status": "mcp_not_available"
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Информация о здоровье агента с retry конфигурацией"""
        health_status = {
            "agent_id": self.agent_id,
            "name": self.name,
            "agent_level": self.agent_level,
            "status": "healthy",
            "model": self.model_name,
            "metrics": self.metrics.to_dict(),
            "mcp_enabled": self.mcp_enabled,
            "rag_enabled": self.rag_enabled,
            "retry_config": self.retry_config
        }
        
        # Добавляем MCP статус если включен
        if self.mcp_enabled:
            health_status["mcp_context"] = self.mcp_context
            health_status["data_provider_type"] = type(self.data_provider).__name__
        
        # Добавляем RAG статус если включен
        if self.rag_enabled:
            health_status["rag_stats"] = self.get_rag_stats()
        
        return health_status
    
    async def _execute_with_metrics(self, task_func, *args, **kwargs):
        """Выполнение задачи с записью метрик"""
        start_time = datetime.now()
        success = False
        
        try:
            result = await task_func(*args, **kwargs)
            success = result.get('success', True)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat()
            }
        finally:
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            self.metrics.record_task(success, processing_time)
    
    def _initialize_mcp_context(self):
        """Инициализация MCP контекста для агента"""
        self.mcp_context = {
            "agent_id": self.agent_id,
            "agent_type": self._get_agent_type(),
            "capabilities": self._get_agent_capabilities(),
            "preferences": {
                "cache_enabled": True,
                "real_time_updates": False,
                "data_freshness_threshold": "1h"
            },
            "session_id": f"session_{self.agent_id}_{datetime.now().timestamp()}",
            "initialized_at": datetime.now().isoformat()
        }
    
    def _get_agent_type(self) -> str:
        """Определение типа агента по имени класса"""
        class_name = self.__class__.__name__.lower()
        
        if "executive" in self.name.lower() or any(word in class_name for word in ["chief", "director", "executive"]):
            return "executive"
        elif "manager" in class_name or "coordination" in class_name:
            return "management"  
        else:
            return "operational"
    
    def _get_agent_capabilities(self) -> list:
        """Получение списка возможностей агента"""
        capabilities = ["basic_analysis"]
        
        # Определяем возможности на основе типа агента
        agent_type = self._get_agent_type()
        class_name = self.__class__.__name__.lower()
        
        if agent_type == "executive":
            capabilities.extend(["strategic_planning", "enterprise_analysis", "roi_optimization"])
        elif agent_type == "management":
            capabilities.extend(["task_coordination", "performance_monitoring", "team_management"])
        else:  # operational
            capabilities.extend(["data_processing", "automated_analysis", "report_generation"])
        
        # Специфические возможности по названию агента
        if "seo" in class_name:
            capabilities.extend(["seo_analysis", "technical_audit", "keyword_research"])
        if "content" in class_name:
            capabilities.extend(["content_analysis", "content_strategy", "eeat_optimization"])
        if "competitive" in class_name:
            capabilities.extend(["competitive_analysis", "serp_analysis", "market_intelligence"])
        if "sales" in class_name:
            capabilities.extend(["lead_qualification", "sales_analysis", "proposal_generation"])
        if "link" in class_name:
            capabilities.extend(["link_analysis", "backlink_research", "outreach_automation"])
        if "reporting" in class_name:
            capabilities.extend(["business_intelligence", "data_visualization", "anomaly_detection"])
        
        return list(set(capabilities))  # Убираем дубликаты
    
    async def get_mcp_health_status(self) -> Dict[str, Any]:
        """Получение статуса здоровья MCP провайдера"""
        if not self.mcp_enabled or not hasattr(self.data_provider, 'health_check'):
            return {"status": "mcp_disabled"}
        
        try:
            health_data = await self.data_provider.health_check()
            return {
                "status": "healthy",
                "mcp_health": health_data,
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
    
    def enable_mcp(self, data_provider: "MCPDataProvider"):
        """Включение MCP для агента"""
        self.mcp_enabled = True
        self.data_provider = data_provider
        self._initialize_mcp_context()
        print(f"✅ MCP включен для агента {self.agent_id}")
    
    def disable_mcp(self):
        """Отключение MCP для агента"""
        self.mcp_enabled = False
        self.mcp_context = {}
        print(f"⚠️ MCP отключен для агента {self.agent_id}")
    
    def get_mcp_stats(self) -> Dict[str, Any]:
        """Получение статистики MCP провайдера"""
        if not self.mcp_enabled or not hasattr(self.data_provider, 'get_stats'):
            return {"status": "mcp_disabled"}
        
        try:
            return {
                "status": "enabled",
                "provider_stats": self.data_provider.get_stats(),
                "agent_mcp_context": self.mcp_context
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _initialize_rag_knowledge(self):
        """Инициализация RAG базы знаний с ChromaDB (исправленная версия)"""
        try:
            # ИСПРАВЛЕНО: Прямой импорт ChromaDB модуля (избегаем FAISS legacy код)
            import importlib.util
            import os
            
            # Проверяем что ChromaDB Knowledge Manager существует
            chroma_km_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'chroma_knowledge_manager.py')
            chroma_km_path = os.path.abspath(chroma_km_path)
            
            if not os.path.exists(chroma_km_path):
                print(f"⚠️ ChromaDB Knowledge Manager не найден по пути {chroma_km_path}")
                self.rag_enabled = False
                return
            
            # Прямой импорт ChromaDB модуля без legacy FAISS зависимостей
            spec = importlib.util.spec_from_file_location("chroma_knowledge_manager", chroma_km_path)
            chroma_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(chroma_module)
            
            # Получаем knowledge_manager из ChromaDB модуля
            knowledge_manager = chroma_module.knowledge_manager
            
            # Проверяем конфигурацию RAG
            from core.config import AIAgentsConfig
            config = AIAgentsConfig()
            
            if not config.ENABLE_RAG:
                print(f"⚠️ RAG отключен в конфигурации для {self.agent_id}")
                self.rag_enabled = False
                return
                
            # Загружаем базу знаний для данного агента через ChromaDB
            vector_store = knowledge_manager.load_agent_knowledge(
                self.agent_id, 
                self.agent_level
            )
            
            if vector_store:
                print(f"✅ ChromaDB RAG база знаний загружена для {self.agent_id}")
                # Сохраняем ссылку на knowledge_manager для дальнейшего использования
                self._knowledge_manager = knowledge_manager
            else:
                print(f"⚠️ ChromaDB RAG база знаний не найдена для {self.agent_id}")
                self.rag_enabled = False
                
        except Exception as e:
            print(f"❌ Ошибка инициализации ChromaDB RAG для {self.agent_id}: {str(e)[:60]}...")
            # НЕ показываем полный traceback чтобы избежать путаницы с FAISS ошибками
            self.rag_enabled = False
    
    async def get_knowledge_context(self, query: str, k: int = None) -> str:
        """
        Получает релевантный контекст знаний для запроса через ChromaDB (исправленная версия)
        
        Args:
            query: Поисковый запрос
            k: Количество результатов
            
        Returns:
            str: Форматированный контекст знаний
        """
        if not self.rag_enabled:
            return ""
            
        try:
            # Используем сохраненную ссылку на knowledge_manager или создаем новую
            if hasattr(self, '_knowledge_manager'):
                knowledge_manager = self._knowledge_manager
            else:
                # Fallback к прямому импорту ChromaDB модуля
                import importlib.util
                import os
                
                chroma_km_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'chroma_knowledge_manager.py')
                chroma_km_path = os.path.abspath(chroma_km_path)
                
                spec = importlib.util.spec_from_file_location("chroma_knowledge_manager", chroma_km_path)
                chroma_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(chroma_module)
                
                knowledge_manager = chroma_module.knowledge_manager
                self._knowledge_manager = knowledge_manager
            
            context = knowledge_manager.get_knowledge_context(
                self.agent_id, 
                query, 
                k
            )
            
            self.knowledge_context = context
            return context
            
        except Exception as e:
            print(f"⚠️ Ошибка получения контекста знаний через ChromaDB для {self.agent_id}: {e}")
            return ""
    
    def format_prompt_with_rag(self, user_prompt: str, task_data: Dict[str, Any]) -> str:
        """
        Форматирует промпт с учетом RAG контекста
        
        Args:
            user_prompt: Основной промпт пользователя
            task_data: Данные задачи
            
        Returns:
            str: Обогащенный промпт с контекстом знаний
        """
        # Базовый промпт
        enhanced_prompt = f"""
Ты - {self.name}, специализированный AI-агент уровня {self.agent_level}.

ЗАДАЧА:
{user_prompt}

ВХОДНЫЕ ДАННЫЕ:
{task_data}
"""

        # Добавляем контекст знаний если есть
        if self.knowledge_context:
            enhanced_prompt += f"""

КОНТЕКСТ ЗНАНИЙ (используй эту информацию для более точного ответа):
{self.knowledge_context}
"""

        enhanced_prompt += """

ИНСТРУКЦИИ:
1. Используй контекст знаний для формирования экспертного ответа
2. Если контекст знаний релевантен - ссылайся на него
3. Предоставь детальный и профессиональный ответ
4. Форматируй ответ в JSON структуре как ожидается

ОТВЕТ:"""

        return enhanced_prompt
    
    def enable_rag(self):
        """Включение RAG для агента"""
        self.rag_enabled = True
        self._initialize_rag_knowledge()
        print(f"✅ RAG включен для агента {self.agent_id}")
    
    def disable_rag(self):
        """Отключение RAG для агента"""
        self.rag_enabled = False
        self.knowledge_context = ""
        print(f"⚠️ RAG отключен для агента {self.agent_id}")
    
    def get_rag_stats(self) -> Dict[str, Any]:
        """Получение статистики RAG"""
        return {
            "rag_enabled": self.rag_enabled,
            "knowledge_context_length": len(self.knowledge_context) if self.knowledge_context else 0,
            "agent_level": self.agent_level,
            "knowledge_base": self.knowledge_base
        }
