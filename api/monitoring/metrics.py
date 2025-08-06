"""
Система сбора и мониторинга метрик для AI SEO Architects API
Включает системные метрики, метрики агентов, бизнес-метрики
"""

import asyncio
import time
import psutil
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict, deque
import json
from pathlib import Path
import threading
import weakref

from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class RequestMetrics:
    """Метрики HTTP запросов"""
    timestamp: float
    method: str
    endpoint: str
    status_code: int
    duration: float
    client_ip: str = ""


@dataclass
class AgentTaskMetrics:
    """Метрики выполнения задач агентов"""
    timestamp: float
    agent_id: str
    task_type: str
    status: str  # completed, failed, timeout
    duration: float
    error_type: Optional[str] = None


@dataclass
class SystemSnapshot:
    """Снимок системных метрик"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float
    disk_usage_percent: float
    network_bytes_sent: int
    network_bytes_recv: int
    active_connections: int = 0
    

class MetricsCollector:
    """Коллектор метрик с периодическим сбором и хранением"""
    
    def __init__(self, retention_hours: int = 24, collection_interval: int = 30):
        self.retention_hours = retention_hours
        self.collection_interval = collection_interval
        
        # Хранилища метрик (в памяти с ограничением времени)
        self.request_metrics: deque = deque()
        self.agent_metrics: deque = deque()
        self.system_metrics: deque = deque()
        
        # Агрегированные счетчики
        self.total_requests = 0
        self.total_errors = 0
        self.agent_task_counts = defaultdict(int)
        self.agent_error_counts = defaultdict(int)
        
        # Реальные метрики в реальном времени
        self.current_active_connections = 0
        self.start_time = time.time()
        
        # Флаг для остановки сбора
        self._collecting = False
        self._collection_task = None
        
        # Система подписчиков на события метрик
        self._subscribers: List[weakref.WeakMethod] = []
    
    async def start_collection(self):
        """Запуск периодического сбора метрик"""
        if self._collecting:
            logger.warning("Metrics collection уже запущен")
            return
        
        self._collecting = True
        self._collection_task = asyncio.create_task(self._collection_loop())
        logger.info(f"📊 Metrics collection запущен (интервал: {self.collection_interval}s)")
    
    async def stop_collection(self):
        """Остановка сбора метрик"""
        self._collecting = False
        
        if self._collection_task:
            self._collection_task.cancel()
            try:
                await self._collection_task
            except asyncio.CancelledError:
                pass
        
        logger.info("📊 Metrics collection остановлен")
    
    async def _collection_loop(self):
        """Основной цикл сбора метрик"""
        try:
            while self._collecting:
                await self._collect_system_metrics()
                await self._cleanup_old_metrics()
                await self._notify_subscribers()
                await asyncio.sleep(self.collection_interval)
        except asyncio.CancelledError:
            logger.info("Metrics collection cancelled")
        except Exception as e:
            logger.error(f"Ошибка в metrics collection: {e}")
    
    async def _collect_system_metrics(self):
        """Сбор системных метрик"""
        try:
            # CPU и память
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Сетевые метрики
            network = psutil.net_io_counters()
            
            # Создаем снимок
            snapshot = SystemSnapshot(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / (1024 * 1024),
                memory_total_mb=memory.total / (1024 * 1024),
                disk_usage_percent=disk.percent,
                network_bytes_sent=network.bytes_sent,
                network_bytes_recv=network.bytes_recv,
                active_connections=self.current_active_connections
            )
            
            self.system_metrics.append(snapshot)
            
        except Exception as e:
            logger.error(f"Ошибка сбора системных метрик: {e}")
    
    async def _cleanup_old_metrics(self):
        """Очистка старых метрик"""
        cutoff_time = time.time() - (self.retention_hours * 3600)
        
        # Очищаем старые запросы
        while self.request_metrics and self.request_metrics[0].timestamp < cutoff_time:
            self.request_metrics.popleft()
        
        # Очищаем старые метрики агентов
        while self.agent_metrics and self.agent_metrics[0].timestamp < cutoff_time:
            self.agent_metrics.popleft()
        
        # Очищаем старые системные метрики
        while self.system_metrics and self.system_metrics[0].timestamp < cutoff_time:
            self.system_metrics.popleft()
    
    def subscribe_to_updates(self, callback):
        """Подписка на обновления метрик"""
        self._subscribers.append(weakref.WeakMethod(callback))
    
    async def _notify_subscribers(self):
        """Уведомление подписчиков об обновлении метрик"""
        # Очищаем мертвые weak references
        self._subscribers = [ref for ref in self._subscribers if ref() is not None]
        
        # Получаем текущие метрики
        current_metrics = await self.get_current_metrics()
        
        # Уведомляем подписчиков
        for weak_method in self._subscribers:
            method = weak_method()
            if method:
                try:
                    await method(current_metrics)
                except Exception as e:
                    logger.error(f"Ошибка уведомления подписчика: {e}")
    
    async def record_request(self, method: str, endpoint: str, status_code: int, 
                           duration: float, client_ip: str = ""):
        """Записать метрику HTTP запроса"""
        metric = RequestMetrics(
            timestamp=time.time(),
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            duration=duration,
            client_ip=client_ip
        )
        
        self.request_metrics.append(metric)
        self.total_requests += 1
        
        if status_code >= 400:
            self.total_errors += 1
        
        # Логируем медленные запросы
        if duration > 5.0:  # > 5 секунд
            logger.warning(
                f"Медленный запрос: {method} {endpoint}",
                duration=duration,
                status_code=status_code
            )
    
    async def record_agent_task(self, agent_id: str, task_type: str, 
                              status: str, duration: float, error_type: str = None):
        """Записать метрику выполнения задачи агента"""
        metric = AgentTaskMetrics(
            timestamp=time.time(),
            agent_id=agent_id,
            task_type=task_type,
            status=status,
            duration=duration,
            error_type=error_type
        )
        
        self.agent_metrics.append(metric)
        self.agent_task_counts[agent_id] += 1
        
        if status == "failed":
            self.agent_error_counts[agent_id] += 1
    
    def update_active_connections(self, count: int):
        """Обновить счетчик активных соединений"""
        self.current_active_connections = count
    
    async def get_current_metrics(self) -> Dict[str, Any]:
        """Получить текущие агрегированные метрики"""
        now = time.time()
        uptime = now - self.start_time
        
        # Системные метрики (последний снимок)
        latest_system = self.system_metrics[-1] if self.system_metrics else None
        
        # HTTP метрики за последний час
        hour_ago = now - 3600
        recent_requests = [r for r in self.request_metrics if r.timestamp > hour_ago]
        
        # Метрики агентов за последний час
        recent_agent_tasks = [a for a in self.agent_metrics if a.timestamp > hour_ago]
        
        # Вычисляем агрегированные значения
        request_count_1h = len(recent_requests)
        error_count_1h = sum(1 for r in recent_requests if r.status_code >= 400)
        avg_response_time = (
            sum(r.duration for r in recent_requests) / len(recent_requests)
            if recent_requests else 0
        )
        
        # Статистика агентов
        agent_stats = defaultdict(lambda: {"total": 0, "successful": 0, "failed": 0, "avg_duration": 0})
        
        for task in recent_agent_tasks:
            stats = agent_stats[task.agent_id]
            stats["total"] += 1
            
            if task.status == "completed":
                stats["successful"] += 1
            elif task.status == "failed":
                stats["failed"] += 1
        
        # Средняя длительность задач по агентам
        for agent_id, stats in agent_stats.items():
            agent_tasks = [t for t in recent_agent_tasks if t.agent_id == agent_id]
            if agent_tasks:
                stats["avg_duration"] = sum(t.duration for t in agent_tasks) / len(agent_tasks)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": uptime,
            "system": {
                "cpu_percent": latest_system.cpu_percent if latest_system else 0,
                "memory_percent": latest_system.memory_percent if latest_system else 0,
                "memory_used_mb": latest_system.memory_used_mb if latest_system else 0,
                "memory_total_mb": latest_system.memory_total_mb if latest_system else 0,
                "disk_usage_percent": latest_system.disk_usage_percent if latest_system else 0,
                "active_connections": self.current_active_connections
            },
            "http": {
                "total_requests_lifetime": self.total_requests,
                "total_errors_lifetime": self.total_errors,
                "requests_1h": request_count_1h,
                "errors_1h": error_count_1h,
                "error_rate_1h": error_count_1h / max(1, request_count_1h),
                "avg_response_time_1h": avg_response_time,
                "requests_per_minute": request_count_1h / 60 if request_count_1h > 0 else 0
            },
            "agents": {
                agent_id: {
                    "total_tasks_1h": stats["total"],
                    "successful_tasks_1h": stats["successful"],
                    "failed_tasks_1h": stats["failed"],
                    "success_rate_1h": stats["successful"] / max(1, stats["total"]),
                    "avg_duration_1h": stats["avg_duration"],
                    "tasks_per_minute": stats["total"] / 60 if stats["total"] > 0 else 0
                }
                for agent_id, stats in agent_stats.items()
            }
        }
    
    async def get_detailed_metrics(self, timeframe_hours: int = 1) -> Dict[str, Any]:
        """Получить детальные метрики за период"""
        cutoff_time = time.time() - (timeframe_hours * 3600)
        
        # Фильтруем метрики по времени
        filtered_requests = [r for r in self.request_metrics if r.timestamp > cutoff_time]
        filtered_agent_tasks = [a for a in self.agent_metrics if a.timestamp > cutoff_time]
        filtered_system = [s for s in self.system_metrics if s.timestamp > cutoff_time]
        
        # Группируем по временным интервалам (по 5 минут)
        interval_seconds = 300  # 5 минут
        intervals = {}
        
        start_time = cutoff_time
        while start_time < time.time():
            interval_key = int(start_time / interval_seconds)
            intervals[interval_key] = {
                "timestamp": start_time,
                "requests": 0,
                "errors": 0,
                "avg_response_time": 0,
                "agent_tasks": 0,
                "agent_errors": 0,
                "cpu_percent": 0,
                "memory_percent": 0
            }
            start_time += interval_seconds
        
        # Заполняем интервалы данными
        for request in filtered_requests:
            interval_key = int(request.timestamp / interval_seconds)
            if interval_key in intervals:
                intervals[interval_key]["requests"] += 1
                if request.status_code >= 400:
                    intervals[interval_key]["errors"] += 1
        
        for task in filtered_agent_tasks:
            interval_key = int(task.timestamp / interval_seconds)
            if interval_key in intervals:
                intervals[interval_key]["agent_tasks"] += 1
                if task.status == "failed":
                    intervals[interval_key]["agent_errors"] += 1
        
        for snapshot in filtered_system:
            interval_key = int(snapshot.timestamp / interval_seconds)
            if interval_key in intervals:
                intervals[interval_key]["cpu_percent"] = snapshot.cpu_percent
                intervals[interval_key]["memory_percent"] = snapshot.memory_percent
        
        return {
            "timeframe_hours": timeframe_hours,
            "intervals": list(intervals.values()),
            "summary": {
                "total_requests": len(filtered_requests),
                "total_errors": sum(1 for r in filtered_requests if r.status_code >= 400),
                "total_agent_tasks": len(filtered_agent_tasks),
                "total_agent_errors": sum(1 for t in filtered_agent_tasks if t.status == "failed"),
                "avg_cpu": sum(s.cpu_percent for s in filtered_system) / max(1, len(filtered_system)),
                "avg_memory": sum(s.memory_percent for s in filtered_system) / max(1, len(filtered_system))
            }
        }
    
    async def export_metrics(self, filepath: str):
        """Экспорт метрик в файл"""
        try:
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "metrics": await self.get_current_metrics(),
                "detailed_metrics_1h": await self.get_detailed_metrics(1),
                "detailed_metrics_24h": await self.get_detailed_metrics(24),
                "retention_hours": self.retention_hours,
                "collection_interval": self.collection_interval
            }
            
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📊 Метрики экспортированы в {filepath}")
            
        except Exception as e:
            logger.error(f"Ошибка экспорта метрик: {e}")


# Глобальный экземпляр коллектора
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics() -> MetricsCollector:
    """Получить глобальный экземпляр коллектора метрик"""
    global _metrics_collector
    
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    
    return _metrics_collector


class MetricsMiddleware:
    """Middleware для автоматического сбора метрик HTTP запросов"""
    
    def __init__(self, app):
        self.app = app
        self.metrics = get_metrics()
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            # Обновляем счетчик активных соединений
            self.metrics.current_active_connections += 1
            
            try:
                # Обрабатываем запрос
                await self.app(scope, receive, send)
            finally:
                # Записываем метрику
                duration = time.time() - start_time
                
                await self.metrics.record_request(
                    method=scope.get("method", ""),
                    endpoint=scope.get("path", ""),
                    status_code=200,  # Будет перезаписан в middleware
                    duration=duration,
                    client_ip=scope.get("client", [""])[0] if scope.get("client") else ""
                )
                
                # Уменьшаем счетчик активных соединений
                self.metrics.current_active_connections -= 1
        else:
            await self.app(scope, receive, send)