"""
Модели состояния для координации агентов в LangGraph
Определяют структуру данных передаваемых между AI-архитекторами
"""
from typing import TypedDict, List, Dict, Any, Optional

class SEOArchitectsState(TypedDict):
    """Состояние системы AI SEO Architects для координации между агентами"""
    
    # Данные клиента
    client_id: str                    # Идентификатор клиента
    client_data: Dict[str, Any]       # Полная информация о клиенте
    client_industry: str              # Отрасль клиента для персонализации
    
    # Текущая задача  
    task_id: str                      # Уникальный ID задачи
    task_type: str                    # Тип задачи (аудит, стратегия, продажи)
    task_description: str             # Описание задачи
    task_priority: int                # Приоритет от 1 (высокий) до 5 (низкий)
    
    # Состояние выполнения
    current_agent: str                # Текущий активный агент
    previous_agents: List[str]        # История выполнения агентами
    next_agents: List[str]            # Планируемые агенты
    
    # Обрабатываемые данные
    input_data: Dict[str, Any]        # Входящие данные для обработки
    processing_results: List[Dict]    # Результаты от агентов
    final_output: Optional[Dict]      # Финальный результат
    
    # Контекст и память
    conversation_history: List[Dict]  # История диалогов с клиентом
    client_context: Dict[str, Any]    # Контекст клиента для персонализации
    
    # Статус и обработка ошибок
    status: str                       # "ожидание", "обработка", "завершено", "ошибка"
    errors: List[str]                 # Список ошибок
    warnings: List[str]               # Предупреждения
    
    # Метаданные выполнения
    created_at: str                   # Время создания задачи
    updated_at: str                   # Последнее обновление
    deadline: Optional[str]           # Крайний срок выполнения
