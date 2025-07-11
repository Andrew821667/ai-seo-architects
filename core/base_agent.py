"""
Базовый класс для всех AI-архитекторов
Определяет общий интерфейс и функциональность агентов
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from core.state_models import SEOArchitectsState
from core.config import config
from knowledge.knowledge_manager import knowledge_manager

class BaseAgent(ABC):
    """Базовый класс для всех AI SEO Architects"""
    
    def __init__(
        self,
        name: str,
        level: str,
        specialization: str,
        model: Optional[str] = None
    ):
        """
        Инициализация базового агента
        
        Args:
            name: Имя агента
            level: Уровень агента (executive/management/operational)
            specialization: Специализация агента
            model: Модель LLM для агента
        """
        self.name = name
        self.level = level  
        self.specialization = specialization
        self.model = model or config.AGENT_CONFIGS[level]["model"]
        self.temperature = config.AGENT_CONFIGS[level]["temperature"]
        self.max_tokens = config.AGENT_CONFIGS[level]["max_tokens"]
        
        # Загружаем базу знаний агента
        self.knowledge_store = knowledge_manager.load_agent_knowledge(
            agent_name=name.lower().replace(" ", "_"),
            agent_level=level
        )
        
        print(f"🤖 Инициализирован агент: {name} ({level} уровень)")
    
    @abstractmethod
    async def process_task(self, state: SEOArchitectsState) -> SEOArchitectsState:
        """
        Абстрактный метод обработки задачи агентом
        
        Args:
            state: Текущее состояние системы
            
        Returns:
            SEOArchitectsState: Обновленное состояние
        """
        pass
    
    def search_knowledge(self, query: str, k: int = 3) -> List[str]:
        """
        Поиск релевантных знаний для задачи
        
        Args:
            query: Поисковый запрос
            k: Количество результатов
            
        Returns:
            List[str]: Список релевантных знаний
        """
        if not self.knowledge_store:
            return []
            
        documents = knowledge_manager.search_knowledge(
            agent_name=self.name.lower().replace(" ", "_"),
            query=query,
            k=k
        )
        
        return [doc.page_content for doc in documents]
    
    def log_action(self, action: str, details: Dict[str, Any]) -> None:
        """
        Логирование действий агента
        
        Args:
            action: Описание действия
            details: Детали действия
        """
        timestamp = datetime.now().isoformat()
        print(f"📋 [{timestamp}] {self.name}: {action}")
        if details:
            for key, value in details.items():
                print(f"   {key}: {value}")
    
    def update_state(
        self, 
        state: SEOArchitectsState, 
        result: Dict[str, Any],
        next_agent: Optional[str] = None
    ) -> SEOArchitectsState:
        """
        Обновляет состояние системы после обработки
        
        Args:
            state: Текущее состояние
            result: Результат обработки агентом
            next_agent: Следующий агент для обработки
            
        Returns:
            SEOArchitectsState: Обновленное состояние
        """
        # Добавляем результат
        state["processing_results"].append({
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        
        # Обновляем историю агентов
        state["previous_agents"].append(state["current_agent"])
        
        if next_agent:
            state["current_agent"] = next_agent
            state["next_agents"] = [next_agent] if next_agent != "END" else []
        
        # Обновляем время
        state["updated_at"] = datetime.now().isoformat()
        
        return state
