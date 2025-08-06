"""
WebSocket Connection Manager для real-time обновлений дашборда
Поддержка множественных подключений, broadcast сообщений, автоматические heartbeat
"""

import json
import asyncio
from typing import Dict, List, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import weakref
import uuid

from api.monitoring.logger import get_logger
from api.models.responses import WebSocketMessage, DashboardUpdate

logger = get_logger(__name__)


class WebSocketConnection:
    """Класс для управления одним WebSocket подключением"""
    
    def __init__(self, websocket: WebSocket, client_id: str):
        self.websocket = websocket
        self.client_id = client_id
        self.connected_at = datetime.now()
        self.last_heartbeat = datetime.now()
        self.subscriptions: Set[str] = set()  # Типы сообщений на которые подписан клиент
        self.metadata: Dict[str, Any] = {}
    
    async def send_message(self, message: Dict[str, Any]):
        """Отправить сообщение клиенту"""
        try:
            message_json = json.dumps(message, default=str)
            await self.websocket.send_text(message_json)
            logger.debug(f"Sent WebSocket message to {self.client_id}", 
                        message_type=message.get('type'))
        except Exception as e:
            logger.error(f"Failed to send WebSocket message to {self.client_id}: {e}")
            raise
    
    def update_heartbeat(self):
        """Обновить время последнего heartbeat"""
        self.last_heartbeat = datetime.now()
    
    def add_subscription(self, message_type: str):
        """Подписаться на тип сообщений"""
        self.subscriptions.add(message_type)
        logger.debug(f"Client {self.client_id} subscribed to {message_type}")
    
    def remove_subscription(self, message_type: str):
        """Отписаться от типа сообщений"""
        self.subscriptions.discard(message_type)
        logger.debug(f"Client {self.client_id} unsubscribed from {message_type}")
    
    def is_subscribed(self, message_type: str) -> bool:
        """Проверить подписан ли клиент на тип сообщений"""
        return message_type in self.subscriptions
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Получить информацию о подключении"""
        return {
            "client_id": self.client_id,
            "connected_at": self.connected_at.isoformat(),
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "subscriptions": list(self.subscriptions),
            "metadata": self.metadata
        }


class ConnectionManager:
    """Менеджер WebSocket подключений с поддержкой групп и broadcast"""
    
    def __init__(self):
        # Активные подключения
        self.connections: Dict[str, WebSocketConnection] = {}
        
        # Группы подключений для targeted broadcast
        self.groups: Dict[str, Set[str]] = {
            "dashboard": set(),      # Дашборд клиенты
            "monitoring": set(),     # Мониторинг клиенты
            "agents": set(),         # Клиенты агентов
            "campaigns": set()       # Клиенты кампаний
        }
        
        # Статистика
        self.total_connections = 0
        self.total_messages_sent = 0
        self.connection_errors = 0
        
        # Задача для heartbeat проверки
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._heartbeat_interval = 30  # секунд
        self._heartbeat_timeout = 60   # секунд
    
    async def connect(self, websocket: WebSocket, client_id: str = None, 
                     group: str = "dashboard", metadata: Dict[str, Any] = None):
        """
        Подключить WebSocket клиента
        
        Args:
            websocket: WebSocket instance
            client_id: ID клиента (генерируется автоматически если не указан)
            group: Группа для broadcast сообщений
            metadata: Дополнительные данные о клиенте
        """
        # Генерируем ID если не указан
        if not client_id:
            client_id = f"client_{uuid.uuid4().hex[:8]}"
        
        # Принимаем подключение
        await websocket.accept()
        
        # Создаем объект подключения
        connection = WebSocketConnection(websocket, client_id)
        if metadata:
            connection.metadata.update(metadata)
        
        # Регистрируем подключение
        self.connections[client_id] = connection
        self.groups[group].add(client_id)
        
        # Обновляем статистику
        self.total_connections += 1
        
        # Запускаем heartbeat если это первое подключение
        if len(self.connections) == 1 and not self._heartbeat_task:
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        logger.info(f"WebSocket client connected: {client_id} (group: {group})")
        
        # Отправляем приветственное сообщение
        welcome_message = {
            "type": "connection_established",
            "client_id": client_id,
            "server_time": datetime.now().isoformat(),
            "groups": [group]
        }
        await connection.send_message(welcome_message)
        
        return client_id
    
    def disconnect(self, websocket: WebSocket):
        """Отключить WebSocket клиента"""
        # Находим клиента по websocket
        client_id = None
        for cid, conn in self.connections.items():
            if conn.websocket == websocket:
                client_id = cid
                break
        
        if client_id:
            # Удаляем из всех групп
            for group_clients in self.groups.values():
                group_clients.discard(client_id)
            
            # Удаляем подключение
            del self.connections[client_id]
            
            # Останавливаем heartbeat если нет подключений
            if len(self.connections) == 0 and self._heartbeat_task:
                self._heartbeat_task.cancel()
                self._heartbeat_task = None
            
            logger.info(f"WebSocket client disconnected: {client_id}")
        else:
            logger.warning("Attempted to disconnect unknown WebSocket")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Отправить персональное сообщение конкретному клиенту"""
        try:
            await websocket.send_text(message)
            self.total_messages_sent += 1
        except Exception as e:
            self.connection_errors += 1
            logger.error(f"Failed to send personal message: {e}")
            raise
    
    async def send_to_client(self, client_id: str, message: Dict[str, Any]):
        """Отправить сообщение конкретному клиенту по ID"""
        if client_id not in self.connections:
            logger.warning(f"Attempted to send message to unknown client: {client_id}")
            return False
        
        try:
            connection = self.connections[client_id]
            await connection.send_message(message)
            self.total_messages_sent += 1
            return True
        except Exception as e:
            self.connection_errors += 1
            logger.error(f"Failed to send message to client {client_id}: {e}")
            # Удаляем проблемное подключение
            await self._cleanup_connection(client_id)
            return False
    
    async def broadcast_to_group(self, group: str, message: Dict[str, Any], 
                               message_type: str = None):
        """
        Broadcast сообщение группе клиентов
        
        Args:
            group: Название группы
            message: Сообщение для отправки
            message_type: Тип сообщения для фильтрации по подпискам
        """
        if group not in self.groups:
            logger.warning(f"Unknown group: {group}")
            return
        
        client_ids = self.groups[group].copy()  # Копируем для безопасности
        successful_sends = 0
        failed_sends = 0
        
        for client_id in client_ids:
            if client_id not in self.connections:
                continue
            
            connection = self.connections[client_id]
            
            # Проверяем подписку на тип сообщения
            if message_type and not connection.is_subscribed(message_type):
                continue
            
            try:
                await connection.send_message(message)
                successful_sends += 1
                self.total_messages_sent += 1
            except Exception as e:
                failed_sends += 1
                self.connection_errors += 1
                logger.error(f"Failed to broadcast to client {client_id}: {e}")
                # Планируем очистку проблемного подключения
                asyncio.create_task(self._cleanup_connection(client_id))
        
        logger.debug(f"Broadcast to group '{group}': {successful_sends} successful, {failed_sends} failed")
    
    async def broadcast_to_all(self, message: Dict[str, Any], message_type: str = None):
        """Broadcast сообщение всем подключенным клиентам"""
        client_ids = list(self.connections.keys())
        successful_sends = 0
        failed_sends = 0
        
        for client_id in client_ids:
            if client_id not in self.connections:
                continue
            
            connection = self.connections[client_id]
            
            # Проверяем подписку на тип сообщения
            if message_type and not connection.is_subscribed(message_type):
                continue
            
            try:
                await connection.send_message(message)
                successful_sends += 1
                self.total_messages_sent += 1
            except Exception as e:
                failed_sends += 1
                self.connection_errors += 1
                logger.error(f"Failed to broadcast to client {client_id}: {e}")
                asyncio.create_task(self._cleanup_connection(client_id))
        
        logger.debug(f"Broadcast to all: {successful_sends} successful, {failed_sends} failed")
    
    async def handle_client_message(self, client_id: str, message: Dict[str, Any]):
        """Обработать сообщение от клиента"""
        if client_id not in self.connections:
            logger.warning(f"Message from unknown client: {client_id}")
            return
        
        connection = self.connections[client_id]
        message_type = message.get("type")
        
        logger.debug(f"Received message from {client_id}: {message_type}")
        
        # Обрабатываем специальные типы сообщений
        if message_type == "heartbeat":
            connection.update_heartbeat()
            await connection.send_message({
                "type": "heartbeat_ack",
                "timestamp": datetime.now().isoformat()
            })
        
        elif message_type == "subscribe":
            subscription_type = message.get("subscription_type")
            if subscription_type:
                connection.add_subscription(subscription_type)
                await connection.send_message({
                    "type": "subscription_confirmed",
                    "subscription_type": subscription_type
                })
        
        elif message_type == "unsubscribe":
            subscription_type = message.get("subscription_type")
            if subscription_type:
                connection.remove_subscription(subscription_type)
                await connection.send_message({
                    "type": "unsubscription_confirmed",
                    "subscription_type": subscription_type
                })
        
        elif message_type == "join_group":
            group = message.get("group")
            if group and group in self.groups:
                self.groups[group].add(client_id)
                await connection.send_message({
                    "type": "group_joined",
                    "group": group
                })
        
        elif message_type == "leave_group":
            group = message.get("group")
            if group and group in self.groups:
                self.groups[group].discard(client_id)
                await connection.send_message({
                    "type": "group_left",
                    "group": group
                })
        
        else:
            logger.debug(f"Unhandled message type from {client_id}: {message_type}")
    
    async def _cleanup_connection(self, client_id: str):
        """Очистить проблемное подключение"""
        if client_id in self.connections:
            connection = self.connections[client_id]
            
            # Удаляем из всех групп
            for group_clients in self.groups.values():
                group_clients.discard(client_id)
            
            # Удаляем подключение
            del self.connections[client_id]
            
            logger.info(f"Cleaned up connection: {client_id}")
    
    async def _heartbeat_loop(self):
        """Цикл проверки heartbeat и очистки мертвых подключений"""
        try:
            while True:
                await asyncio.sleep(self._heartbeat_interval)
                
                current_time = datetime.now()
                dead_connections = []
                
                # Находим мертвые подключения
                for client_id, connection in self.connections.items():
                    time_since_heartbeat = (current_time - connection.last_heartbeat).total_seconds()
                    
                    if time_since_heartbeat > self._heartbeat_timeout:
                        dead_connections.append(client_id)
                
                # Очищаем мертвые подключения
                for client_id in dead_connections:
                    logger.info(f"Removing dead connection: {client_id}")
                    await self._cleanup_connection(client_id)
                
                # Отправляем heartbeat живым подключениям
                for client_id, connection in self.connections.items():
                    try:
                        await connection.send_message({
                            "type": "server_heartbeat",
                            "timestamp": current_time.isoformat()
                        })
                    except:
                        # Помечаем для удаления на следующей итерации
                        pass
                        
        except asyncio.CancelledError:
            logger.info("Heartbeat loop cancelled")
        except Exception as e:
            logger.error(f"Error in heartbeat loop: {e}")
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Получить статистику подключений"""
        return {
            "active_connections": len(self.connections),
            "total_connections_lifetime": self.total_connections,
            "total_messages_sent": self.total_messages_sent,
            "connection_errors": self.connection_errors,
            "groups": {
                group: len(clients) 
                for group, clients in self.groups.items()
            },
            "connections": [
                conn.get_connection_info() 
                for conn in self.connections.values()
            ]
        }
    
    async def shutdown(self):
        """Graceful shutdown менеджера"""
        logger.info("Shutting down WebSocket manager...")
        
        # Останавливаем heartbeat
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
        
        # Уведомляем всех клиентов о shutdown
        shutdown_message = {
            "type": "server_shutdown",
            "message": "Server is shutting down",
            "timestamp": datetime.now().isoformat()
        }
        
        await self.broadcast_to_all(shutdown_message)
        
        # Закрываем все подключения
        for client_id, connection in list(self.connections.items()):
            try:
                await connection.websocket.close()
            except:
                pass
        
        # Очищаем все данные
        self.connections.clear()
        for group in self.groups.values():
            group.clear()
        
        logger.info("WebSocket manager shutdown complete")