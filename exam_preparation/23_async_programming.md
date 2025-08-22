# Тема 23: Асинхронное программирование в Python и ИИ системах

## Основы асинхронности

### Концепции асинхронного программирования
- **Concurrency vs Parallelism**: Конкурентность и параллелизм
- **Event Loop**: Цикл событий как основа async/await
- **Coroutines**: Корутины и их жизненный цикл
- **Tasks**: Задачи и их планирование
- **Futures**: Объекты будущих результатов

### Базовый синтаксис async/await
```python
import asyncio
import aiohttp
import time
from typing import List, Dict, Optional, Coroutine, Any

# Простые примеры асинхронных функций
async def simple_async_function():
    """Базовая асинхронная функция"""
    print("Начало выполнения")
    await asyncio.sleep(1)  # Имитация асинхронной операции
    print("Конец выполнения")
    return "Результат"

async def fetch_data(url: str, delay: float = 1.0) -> str:
    """Имитация получения данных"""
    print(f"Начинаем загрузку {url}")
    await asyncio.sleep(delay)  # Имитация сетевого запроса
    print(f"Завершили загрузку {url}")
    return f"Данные с {url}"

# Запуск асинхронных функций
async def main_example():
    # Последовательное выполнение
    start_time = time.time()
    result1 = await fetch_data("site1.com")
    result2 = await fetch_data("site2.com")
    sequential_time = time.time() - start_time
    print(f"Последовательно: {sequential_time:.2f} сек")
    
    # Параллельное выполнение
    start_time = time.time()
    task1 = asyncio.create_task(fetch_data("site3.com"))
    task2 = asyncio.create_task(fetch_data("site4.com"))
    
    results = await asyncio.gather(task1, task2)
    parallel_time = time.time() - start_time
    print(f"Параллельно: {parallel_time:.2f} сек")
    print(f"Результаты: {results}")

# Запуск: asyncio.run(main_example())
```

### Управление задачами и исключениями
```python
import asyncio
from asyncio import Task
from typing import List, Tuple

class AsyncTaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.results: List[Tuple[str, Any, Optional[Exception]]] = []
    
    async def add_task(self, coro: Coroutine, name: str = None) -> Task:
        """Добавление задачи в менеджер"""
        task = asyncio.create_task(coro, name=name)
        self.tasks.append(task)
        return task
    
    async def wait_for_all(self, timeout: float = None) -> List[Tuple[str, Any, Optional[Exception]]]:
        """Ожидание завершения всех задач с обработкой ошибок"""
        if not self.tasks:
            return []
        
        try:
            # Ждем завершения всех задач
            done, pending = await asyncio.wait(
                self.tasks, 
                timeout=timeout,
                return_when=asyncio.ALL_COMPLETED
            )
            
            # Обрабатываем завершенные задачи
            for task in done:
                task_name = task.get_name()
                try:
                    result = await task
                    self.results.append((task_name, result, None))
                except Exception as e:
                    self.results.append((task_name, None, e))
            
            # Отменяем незавершенные задачи
            for task in pending:
                task.cancel()
                self.results.append((task.get_name(), None, asyncio.CancelledError("Timeout")))
        
        except Exception as e:
            print(f"Ошибка в wait_for_all: {e}")
        
        return self.results
    
    async def wait_for_first(self) -> Tuple[str, Any, Optional[Exception]]:
        """Ожидание первого завершенного результата"""
        if not self.tasks:
            return ("", None, Exception("No tasks"))
        
        done, pending = await asyncio.wait(
            self.tasks,
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Отменяем оставшиеся задачи
        for task in pending:
            task.cancel()
        
        # Получаем результат первой завершенной задачи
        completed_task = list(done)[0]
        try:
            result = await completed_task
            return (completed_task.get_name(), result, None)
        except Exception as e:
            return (completed_task.get_name(), None, e)

# Пример с обработкой ошибок
async def unreliable_task(task_id: int, fail_chance: float = 0.3) -> str:
    """Задача, которая может завершиться с ошибкой"""
    await asyncio.sleep(1)
    
    import random
    if random.random() < fail_chance:
        raise Exception(f"Задача {task_id} завершилась с ошибкой")
    
    return f"Результат задачи {task_id}"

async def error_handling_example():
    manager = AsyncTaskManager()
    
    # Добавляем несколько задач
    for i in range(5):
        await manager.add_task(
            unreliable_task(i, fail_chance=0.4), 
            name=f"task_{i}"
        )
    
    # Ждем завершения всех задач
    results = await manager.wait_for_all(timeout=5.0)
    
    # Анализируем результаты
    successful = [r for r in results if r[2] is None]
    failed = [r for r in results if r[2] is not None]
    
    print(f"Успешно выполнено: {len(successful)}")
    print(f"Завершилось с ошибкой: {len(failed)}")
    
    for name, result, error in failed:
        print(f"Ошибка в {name}: {error}")

# asyncio.run(error_handling_example())
```

## Асинхронные HTTP запросы

### Использование aiohttp для API запросов
```python
import aiohttp
import asyncio
from typing import List, Dict, Optional
import json

class AsyncAPIClient:
    def __init__(self, base_url: str = "", headers: Dict[str, str] = None):
        self.base_url = base_url.rstrip('/')
        self.default_headers = headers or {}
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers=self.default_headers,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get(self, endpoint: str, params: Dict = None) -> Dict:
        """Асинхронный GET запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def post(self, endpoint: str, data: Dict = None, json_data: Dict = None) -> Dict:
        """Асинхронный POST запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        kwargs = {}
        if data:
            kwargs['data'] = data
        if json_data:
            kwargs['json'] = json_data
        
        async with self.session.post(url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()
    
    async def batch_get(self, endpoints: List[str], max_concurrent: int = 10) -> List[Dict]:
        """Пакетные GET запросы с ограничением конкурентности"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def limited_get(endpoint: str) -> Dict:
            async with semaphore:
                try:
                    return await self.get(endpoint)
                except Exception as e:
                    return {"error": str(e), "endpoint": endpoint}
        
        tasks = [limited_get(endpoint) for endpoint in endpoints]
        return await asyncio.gather(*tasks)

# Пример использования с различными API
async def fetch_multiple_apis():
    """Получение данных из нескольких API одновременно"""
    
    # Пример работы с разными API
    async with AsyncAPIClient() as client:
        # Создаем задачи для разных источников данных
        tasks = [
            client.get("https://jsonplaceholder.typicode.com/posts/1"),
            client.get("https://jsonplaceholder.typicode.com/posts/2"),
            client.get("https://jsonplaceholder.typicode.com/posts/3"),
        ]
        
        # Выполняем запросы параллельно
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Обрабатываем результаты
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Ошибка в запросе {i+1}: {result}")
            else:
                print(f"Пост {i+1}: {result.get('title', 'N/A')}")

# asyncio.run(fetch_multiple_apis())

# Пример с rate limiting
class RateLimitedAPIClient(AsyncAPIClient):
    def __init__(self, base_url: str, requests_per_second: float = 10):
        super().__init__(base_url)
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
        self.lock = asyncio.Lock()
    
    async def _wait_for_rate_limit(self):
        """Ожидание согласно ограничению частоты запросов"""
        async with self.lock:
            current_time = asyncio.get_event_loop().time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.min_interval:
                await asyncio.sleep(self.min_interval - time_since_last)
            
            self.last_request_time = asyncio.get_event_loop().time()
    
    async def get(self, endpoint: str, params: Dict = None) -> Dict:
        """GET запрос с rate limiting"""
        await self._wait_for_rate_limit()
        return await super().get(endpoint, params)
```

### Асинхронная работа с базами данных
```python
import asyncpg
import aiosqlite
from typing import List, Dict, Any

class AsyncDatabaseManager:
    def __init__(self, db_type: str = "sqlite", connection_string: str = ""):
        self.db_type = db_type
        self.connection_string = connection_string
        self.connection_pool = None
    
    async def init_connection_pool(self):
        """Инициализация пула соединений"""
        if self.db_type == "postgresql":
            self.connection_pool = await asyncpg.create_pool(
                self.connection_string,
                min_size=1,
                max_size=10
            )
    
    async def close_pool(self):
        """Закрытие пула соединений"""
        if self.connection_pool:
            await self.connection_pool.close()
    
    async def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Выполнение запроса с возвратом результатов"""
        if self.db_type == "sqlite":
            return await self._execute_sqlite(query, params)
        elif self.db_type == "postgresql":
            return await self._execute_postgresql(query, params)
    
    async def _execute_sqlite(self, query: str, params: tuple = None) -> List[Dict]:
        """Выполнение запроса к SQLite"""
        async with aiosqlite.connect(self.connection_string) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(query, params or ()) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def _execute_postgresql(self, query: str, params: tuple = None) -> List[Dict]:
        """Выполнение запроса к PostgreSQL"""
        async with self.connection_pool.acquire() as connection:
            rows = await connection.fetch(query, *(params or ()))
            return [dict(row) for row in rows]
    
    async def batch_insert(self, table: str, records: List[Dict]) -> int:
        """Массовая вставка записей"""
        if not records:
            return 0
        
        # Формируем запрос на основе первой записи
        columns = list(records[0].keys())
        placeholders = ', '.join(['?' if self.db_type == "sqlite" else f'${i+1}' 
                                 for i in range(len(columns))])
        
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Подготавливаем данные для вставки
        insert_data = [tuple(record[col] for col in columns) for record in records]
        
        if self.db_type == "sqlite":
            async with aiosqlite.connect(self.connection_string) as db:
                await db.executemany(query, insert_data)
                await db.commit()
                return len(insert_data)
        
        elif self.db_type == "postgresql":
            async with self.connection_pool.acquire() as connection:
                await connection.executemany(query, insert_data)
                return len(insert_data)

# Пример асинхронной работы с данными
async def process_large_dataset():
    """Обработка большого набора данных асинхронно"""
    db_manager = AsyncDatabaseManager("sqlite", "example.db")
    
    # Создаем таблицу
    await db_manager.execute_query("""
        CREATE TABLE IF NOT EXISTS processed_data (
            id INTEGER PRIMARY KEY,
            content TEXT,
            processed_result TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Генерируем тестовые данные
    test_data = [
        {"content": f"Данные для обработки {i}"}
        for i in range(100)
    ]
    
    # Асинхронная обработка данных
    async def process_item(item: Dict) -> Dict:
        # Имитация обработки данных
        await asyncio.sleep(0.1)
        processed = f"Обработано: {item['content']}"
        
        return {
            "content": item['content'],
            "processed_result": processed
        }
    
    # Обрабатываем данные пакетами
    batch_size = 10
    processed_records = []
    
    for i in range(0, len(test_data), batch_size):
        batch = test_data[i:i + batch_size]
        
        # Обрабатываем пакет параллельно
        tasks = [process_item(item) for item in batch]
        batch_results = await asyncio.gather(*tasks)
        
        processed_records.extend(batch_results)
        print(f"Обработан пакет {i//batch_size + 1}, записей: {len(batch_results)}")
    
    # Сохраняем результаты в базу данных
    inserted_count = await db_manager.batch_insert("processed_data", processed_records)
    print(f"Вставлено записей: {inserted_count}")
    
    # Проверяем результат
    results = await db_manager.execute_query("SELECT COUNT(*) as count FROM processed_data")
    print(f"Всего записей в базе: {results[0]['count']}")

# asyncio.run(process_large_dataset())
```

## Асинхронная работа с файлами

### Асинхронное чтение и запись файлов
```python
import aiofiles
import asyncio
import os
from pathlib import Path
from typing import List, AsyncGenerator

class AsyncFileProcessor:
    @staticmethod
    async def read_file_async(file_path: str) -> str:
        """Асинхронное чтение файла"""
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
            content = await file.read()
            return content
    
    @staticmethod
    async def write_file_async(file_path: str, content: str) -> bool:
        """Асинхронная запись в файл"""
        try:
            async with aiofiles.open(file_path, mode='w', encoding='utf-8') as file:
                await file.write(content)
                return True
        except Exception as e:
            print(f"Ошибка записи файла {file_path}: {e}")
            return False
    
    @staticmethod
    async def process_files_batch(file_paths: List[str], 
                                 processor_func) -> List[tuple]:
        """Пакетная обработка файлов"""
        semaphore = asyncio.Semaphore(5)  # Ограничение до 5 одновременных файлов
        
        async def process_single_file(file_path: str):
            async with semaphore:
                try:
                    content = await AsyncFileProcessor.read_file_async(file_path)
                    result = await processor_func(content)
                    return (file_path, result, None)
                except Exception as e:
                    return (file_path, None, e)
        
        tasks = [process_single_file(path) for path in file_paths]
        return await asyncio.gather(*tasks)
    
    @staticmethod
    async def read_large_file_chunks(file_path: str, 
                                   chunk_size: int = 8192) -> AsyncGenerator[str, None]:
        """Асинхронное чтение файла по частям"""
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

# Пример обработки текстовых файлов
async def text_processing_example():
    """Пример асинхронной обработки текстовых файлов"""
    
    # Функция для обработки содержимого файла
    async def process_text_content(content: str) -> Dict[str, Any]:
        # Имитация времязатратной обработки
        await asyncio.sleep(0.5)
        
        word_count = len(content.split())
        char_count = len(content)
        line_count = len(content.splitlines())
        
        return {
            'word_count': word_count,
            'char_count': char_count,
            'line_count': line_count,
            'avg_word_length': char_count / max(word_count, 1)
        }
    
    # Получаем список файлов для обработки
    text_files = [str(p) for p in Path('.').glob('*.txt')][:10]  # Первые 10 файлов
    
    if not text_files:
        print("Текстовые файлы не найдены")
        return
    
    print(f"Обрабатываем {len(text_files)} файлов...")
    
    # Обрабатываем файлы асинхронно
    results = await AsyncFileProcessor.process_files_batch(
        text_files, 
        process_text_content
    )
    
    # Анализируем результаты
    successful_results = [r for r in results if r[2] is None]
    failed_results = [r for r in results if r[2] is not None]
    
    print(f"Успешно обработано: {len(successful_results)} файлов")
    print(f"Ошибок: {len(failed_results)}")
    
    if successful_results:
        # Сохраняем сводку результатов
        summary = {
            'total_files': len(successful_results),
            'total_words': sum(r[1]['word_count'] for r in successful_results),
            'total_chars': sum(r[1]['char_count'] for r in successful_results),
            'average_file_size': sum(r[1]['char_count'] for r in successful_results) / len(successful_results)
        }
        
        summary_json = json.dumps(summary, indent=2, ensure_ascii=False)
        await AsyncFileProcessor.write_file_async('processing_summary.json', summary_json)
        print("Сводка сохранена в processing_summary.json")

# asyncio.run(text_processing_example())
```

## Асинхронные очереди и паттерны

### Producer-Consumer паттерн
```python
import asyncio
from asyncio import Queue
from typing import Any, Callable, Optional
import random

class AsyncProducerConsumer:
    def __init__(self, queue_size: int = 10):
        self.queue: Queue = asyncio.Queue(maxsize=queue_size)
        self.producers_active = True
        self.consumers_active = True
    
    async def producer(self, producer_id: int, item_generator: Callable, 
                      production_rate: float = 1.0):
        """Производитель данных"""
        item_count = 0
        
        while self.producers_active:
            try:
                # Генерируем данные
                item = await item_generator(producer_id, item_count)
                
                # Добавляем в очередь
                await self.queue.put(item)
                print(f"Производитель {producer_id} создал: {item}")
                
                item_count += 1
                
                # Контролируем скорость производства
                await asyncio.sleep(1.0 / production_rate)
                
            except asyncio.CancelledError:
                print(f"Производитель {producer_id} остановлен")
                break
            except Exception as e:
                print(f"Ошибка в производителе {producer_id}: {e}")
    
    async def consumer(self, consumer_id: int, processor: Callable,
                      consumption_rate: float = 1.0):
        """Потребитель данных"""
        processed_count = 0
        
        while self.consumers_active:
            try:
                # Получаем данные из очереди с таймаутом
                item = await asyncio.wait_for(self.queue.get(), timeout=5.0)
                
                # Обрабатываем данные
                result = await processor(consumer_id, item)
                print(f"Потребитель {consumer_id} обработал: {item} -> {result}")
                
                # Отмечаем задачу как выполненную
                self.queue.task_done()
                processed_count += 1
                
                # Контролируем скорость потребления
                await asyncio.sleep(1.0 / consumption_rate)
                
            except asyncio.TimeoutError:
                print(f"Потребитель {consumer_id}: таймаут ожидания данных")
                break
            except asyncio.CancelledError:
                print(f"Потребитель {consumer_id} остановлен")
                break
            except Exception as e:
                print(f"Ошибка в потребителе {consumer_id}: {e}")
        
        print(f"Потребитель {consumer_id} обработал {processed_count} элементов")
    
    async def stop_producers(self):
        """Остановка производителей"""
        self.producers_active = False
    
    async def stop_consumers(self):
        """Остановка потребителей"""
        self.consumers_active = False
        
        # Ждем завершения обработки очереди
        await self.queue.join()
    
    def get_queue_size(self) -> int:
        """Текущий размер очереди"""
        return self.queue.qsize()

# Пример использования Producer-Consumer
async def producer_consumer_example():
    """Демонстрация паттерна Producer-Consumer"""
    
    # Функция генерации данных
    async def data_generator(producer_id: int, item_count: int) -> str:
        await asyncio.sleep(0.1)  # Имитация времени генерации
        return f"data_p{producer_id}_i{item_count}_{random.randint(1, 100)}"
    
    # Функция обработки данных
    async def data_processor(consumer_id: int, item: str) -> str:
        await asyncio.sleep(0.2)  # Имитация времени обработки
        return f"processed_{item}_by_c{consumer_id}"
    
    # Создаем систему
    system = AsyncProducerConsumer(queue_size=5)
    
    # Запускаем производителей и потребителей
    tasks = []
    
    # 2 производителя
    for i in range(2):
        task = asyncio.create_task(
            system.producer(i, data_generator, production_rate=2.0),
            name=f"producer_{i}"
        )
        tasks.append(task)
    
    # 3 потребителя
    for i in range(3):
        task = asyncio.create_task(
            system.consumer(i, data_processor, consumption_rate=1.5),
            name=f"consumer_{i}"
        )
        tasks.append(task)
    
    # Мониторинг системы
    async def monitor_system():
        for _ in range(10):  # Мониторим 10 секунд
            await asyncio.sleep(1)
            queue_size = system.get_queue_size()
            print(f"Размер очереди: {queue_size}")
    
    monitor_task = asyncio.create_task(monitor_system())
    
    # Работаем 10 секунд, затем останавливаем
    await asyncio.sleep(10)
    
    # Останавливаем производителей
    await system.stop_producers()
    
    # Даем время обработать оставшиеся данные
    await asyncio.sleep(2)
    
    # Останавливаем потребителей
    await system.stop_consumers()
    
    # Отменяем все задачи
    for task in tasks:
        task.cancel()
    
    await monitor_task

# asyncio.run(producer_consumer_example())
```

## Ключевые моменты для экзамена

### Основы асинхронности
1. **Event Loop**: Цикл событий как основа асинхронного выполнения
2. **Coroutines**: Функции, которые могут быть приостановлены и возобновлены
3. **Tasks**: Планирование и параллельное выполнение корутин
4. **async/await**: Синтаксис для создания и ожидания асинхронных операций

### Практические паттерны
- **Concurrent execution**: Параллельное выполнение независимых задач
- **Producer-Consumer**: Асинхронная обработка данных через очереди
- **Rate limiting**: Контроль частоты запросов к внешним сервисам
- **Error handling**: Обработка исключений в асинхронном коде

### Применение в ИИ системах
- **Batch processing**: Пакетная обработка данных для обучения моделей
- **API calls**: Параллельные запросы к внешним API и сервисам
- **Data streaming**: Потоковая обработка больших объемов данных
- **Model inference**: Асинхронное выполнение инференса моделей

### Инструменты и библиотеки
- **asyncio**: Стандартная библиотека для асинхронности
- **aiohttp**: HTTP клиент/сервер для асинхронных запросов  
- **aiofiles**: Асинхронная работа с файлами
- **asyncpg**: Асинхронный драйвер для PostgreSQL
- **uvloop**: Быстрая реализация event loop