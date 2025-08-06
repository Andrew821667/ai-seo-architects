"""
Система структурированного логирования для AI SEO Architects API
Поддержка correlation ID, structured logging, и интеграция с monitoring системами
"""

import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from contextvars import ContextVar
from pythonjsonlogger import jsonlogger
import uuid
import os
from pathlib import Path

# Context variables for correlation tracking
correlation_id_var: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)


class CorrelationFilter(logging.Filter):
    """Фильтр для добавления correlation ID в лог записи"""
    
    def filter(self, record):
        # Добавляем correlation ID из context
        record.correlation_id = correlation_id_var.get()
        record.user_id = user_id_var.get()
        
        # Генерируем новый correlation ID если его нет
        if not record.correlation_id:
            record.correlation_id = str(uuid.uuid4())[:8]
            correlation_id_var.set(record.correlation_id)
        
        return True


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Кастомный JSON форматтер для структурированных логов"""
    
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        # Добавляем стандартные поля
        log_record['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['service'] = 'ai-seo-architects-api'
        
        # Добавляем информацию о процессе
        log_record['pid'] = os.getpid()
        
        # Добавляем дополнительные поля из record
        if hasattr(record, 'correlation_id'):
            log_record['correlation_id'] = record.correlation_id
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id
        if hasattr(record, 'endpoint'):
            log_record['endpoint'] = record.endpoint
        if hasattr(record, 'method'):
            log_record['method'] = record.method
        if hasattr(record, 'status_code'):
            log_record['status_code'] = record.status_code
        if hasattr(record, 'processing_time_seconds'):
            log_record['processing_time_seconds'] = record.processing_time_seconds
        if hasattr(record, 'agent_id'):
            log_record['agent_id'] = record.agent_id
        if hasattr(record, 'task_id'):
            log_record['task_id'] = record.task_id
        if hasattr(record, 'client_ip'):
            log_record['client_ip'] = record.client_ip


def setup_structured_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    Настройка структурированного логирования
    
    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Путь к файлу логов (опционально)
    """
    
    # Создаем директорию для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Основной логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Очищаем существующие handlers
    root_logger.handlers.clear()
    
    # JSON форматтер
    json_formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(logger)s %(message)s'
    )
    
    # Console handler для разработки
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    console_handler.addFilter(CorrelationFilter())
    root_logger.addHandler(console_handler)
    
    # File handler для production логов
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(json_formatter)
        file_handler.addFilter(CorrelationFilter())
        root_logger.addHandler(file_handler)
    
    # Дополнительный file handler для всех логов
    all_logs_handler = logging.FileHandler(log_dir / "api.log")
    all_logs_handler.setFormatter(json_formatter)
    all_logs_handler.addFilter(CorrelationFilter())
    root_logger.addHandler(all_logs_handler)
    
    # Отдельный handler для ошибок
    error_handler = logging.FileHandler(log_dir / "errors.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(json_formatter)
    error_handler.addFilter(CorrelationFilter())
    root_logger.addHandler(error_handler)
    
    # Настройка логгеров сторонних библиотек
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = True
    
    # Отключаем избыточные логи от библиотек
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    

class StructuredLogger:
    """Wrapper для структурированного логирования с контекстом"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def _log(self, level: int, message: str, **kwargs):
        """Внутренний метод логирования с дополнительными полями"""
        extra = {k: v for k, v in kwargs.items() if v is not None}
        self.logger.log(level, message, extra=extra)
    
    def debug(self, message: str, **kwargs):
        """Debug лог с дополнительными полями"""
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Info лог с дополнительными полями"""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Warning лог с дополнительными полями"""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Error лог с дополнительными полями"""
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Critical лог с дополнительными полями"""
        self._log(logging.CRITICAL, message, **kwargs)
    
    def log_request(self, method: str, endpoint: str, status_code: int, 
                   processing_time: float, client_ip: str, **kwargs):
        """Специальный метод для логирования HTTP запросов"""
        self.info(
            f"{method} {endpoint} - {status_code}",
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            processing_time_seconds=processing_time,
            client_ip=client_ip,
            **kwargs
        )
    
    def log_agent_task(self, agent_id: str, task_id: str, task_type: str, 
                      status: str, processing_time: float = None, **kwargs):
        """Специальный метод для логирования задач агентов"""
        message = f"Agent {agent_id} - Task {task_type} - {status}"
        
        log_kwargs = {
            'agent_id': agent_id,
            'task_id': task_id,
            'task_type': task_type,
            'task_status': status,
            **kwargs
        }
        
        if processing_time:
            log_kwargs['processing_time_seconds'] = processing_time
        
        if status == 'completed':
            self.info(message, **log_kwargs)
        elif status == 'failed':
            self.error(message, **log_kwargs)
        else:
            self.debug(message, **log_kwargs)
    
    def log_business_event(self, event_type: str, details: Dict[str, Any], **kwargs):
        """Специальный метод для логирования бизнес событий"""
        self.info(
            f"Business Event: {event_type}",
            event_type=event_type,
            event_details=details,
            **kwargs
        )


def get_logger(name: str) -> StructuredLogger:
    """
    Получение structured логгера
    
    Args:
        name: Название логгера (обычно __name__)
    
    Returns:
        StructuredLogger instance
    """
    return StructuredLogger(logging.getLogger(name))


def set_correlation_id(correlation_id: str):
    """Установка correlation ID в контекст"""
    correlation_id_var.set(correlation_id)


def get_correlation_id() -> Optional[str]:
    """Получение текущего correlation ID"""
    return correlation_id_var.get()


def set_user_id(user_id: str):
    """Установка user ID в контекст"""
    user_id_var.set(user_id)


def get_user_id() -> Optional[str]:
    """Получение текущего user ID"""
    return user_id_var.get()


class LoggingMiddleware:
    """Middleware для автоматической установки correlation ID"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Генерируем новый correlation ID для каждого запроса
            correlation_id = str(uuid.uuid4())[:8]
            set_correlation_id(correlation_id)
            
            # Добавляем correlation ID в headers ответа
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = list(message.get("headers", []))
                    headers.append((b"x-correlation-id", correlation_id.encode()))
                    message["headers"] = headers
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)


# Конфигурация для различных окружений
LOGGING_CONFIG = {
    "development": {
        "log_level": "DEBUG",
        "log_file": None
    },
    "testing": {
        "log_level": "WARNING",
        "log_file": "logs/test.log"
    },
    "production": {
        "log_level": "INFO",
        "log_file": "logs/production.log"
    }
}


def setup_environment_logging(environment: str = "development"):
    """Настройка логирования для конкретного окружения"""
    config = LOGGING_CONFIG.get(environment, LOGGING_CONFIG["development"])
    setup_structured_logging(**config)