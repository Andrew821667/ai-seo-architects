# Самостоятельно написанные модули. Функция open(). Контекстный менеджер with

## Создание собственных модулей

### Простой модуль
```python
# Файл: calculator.py
"""
Модуль калькулятора с базовыми операциями
"""

def add(a, b):
    """Сложение двух чисел"""
    return a + b

def subtract(a, b):
    """Вычитание"""
    return a - b

def multiply(a, b):
    """Умножение"""
    return a * b

def divide(a, b):
    """Деление с проверкой на ноль"""
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b

# Константы модуля
VERSION = "1.0.0"
AUTHOR = "Student Name"

# Тестирование модуля при прямом запуске
if __name__ == "__main__":
    print(f"Тестирование модуля calculator v{VERSION}")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")
    print(f"15 / 3 = {divide(15, 3)}")
```

### Использование модуля
```python
# Файл: main.py
import calculator

# Использование функций модуля
result = calculator.add(10, 5)
print(f"Результат: {result}")

# Альтернативные способы импорта
from calculator import add, multiply
result = add(10, 5)

# Импорт с псевдонимом
import calculator as calc
result = calc.divide(20, 4)

# Информация о модуле
print(f"Версия калькулятора: {calculator.VERSION}")
print(f"Автор: {calculator.AUTHOR}")
print(f"Доступные функции: {[name for name in dir(calculator) if not name.startswith('_')]}")
```

### Модуль с классами
```python
# Файл: geometry.py
"""
Модуль для геометрических вычислений
"""
import math

class Point:
    """Точка в 2D пространстве"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def distance_to(self, other):
        """Расстояние до другой точки"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"

class Circle:
    """Окружность"""
    def __init__(self, center, radius):
        self.center = center  # Point объект
        self.radius = radius
    
    def area(self):
        """Площадь окружности"""
        return math.pi * self.radius**2
    
    def circumference(self):
        """Длина окружности"""
        return 2 * math.pi * self.radius
    
    def contains_point(self, point):
        """Проверка, содержит ли окружность точку"""
        distance = self.center.distance_to(point)
        return distance <= self.radius

# Утилитарные функции
def calculate_triangle_area(a, b, c):
    """Площадь треугольника по формуле Герона"""
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))

# Константы
PI = math.pi
E = math.e

# Тестирование
if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    print(f"Расстояние: {p1.distance_to(p2)}")  # 5.0
    
    circle = Circle(Point(0, 0), 5)
    print(f"Площадь круга: {circle.area():.2f}")
    print(f"Точка внутри круга: {circle.contains_point(p2)}")  # True
```

## Функция open()

### Основы открытия файлов
```python
# Синтаксис: open(file, mode, buffering, encoding, errors, newline, closefd, opener)

# Режимы открытия файлов
modes = {
    "r": "чтение (по умолчанию)",
    "w": "запись (перезаписывает файл)",
    "a": "добавление в конец файла",
    "x": "создание нового файла (ошибка если существует)",
    "b": "бинарный режим (rb, wb, ab)",
    "t": "текстовый режим (по умолчанию)",
    "+": "чтение и запись (r+, w+, a+)"
}

# Базовые примеры
file = open("data.txt", "r", encoding="utf-8")
content = file.read()
file.close()

# Запись в файл
file = open("output.txt", "w", encoding="utf-8")
file.write("Привет, мир!")
file.close()
```

### Различные режимы работы
```python
# Чтение
def read_examples():
    # Читаем весь файл
    with open("data.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Читаем по строкам
    with open("data.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()  # Список всех строк
    
    # Читаем построчно (эффективно для больших файлов)
    with open("data.txt", "r", encoding="utf-8") as f:
        for line in f:
            print(line.strip())
    
    # Читаем определенное количество символов
    with open("data.txt", "r", encoding="utf-8") as f:
        chunk = f.read(100)  # Первые 100 символов

# Запись
def write_examples():
    # Перезапись файла
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("Новое содержимое\n")
        f.write("Вторая строка\n")
    
    # Добавление в конец
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write("Добавленная строка\n")
    
    # Запись списка строк
    lines = ["Строка 1\n", "Строка 2\n", "Строка 3\n"]
    with open("output.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)
```

### Работа с кодировками
```python
# Явное указание кодировки
def read_with_encoding(filename):
    """Чтение файла с разными кодировками"""
    encodings = ["utf-8", "cp1251", "utf-16"]
    
    for encoding in encodings:
        try:
            with open(filename, "r", encoding=encoding) as f:
                content = f.read()
            print(f"Успешно прочитано с кодировкой: {encoding}")
            return content
        except UnicodeDecodeError:
            print(f"Не удалось прочитать с кодировкой: {encoding}")
            continue
    
    return None

# Обработка ошибок кодирования
def safe_read_file(filename):
    """Безопасное чтение файла с обработкой ошибок"""
    try:
        with open(filename, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except PermissionError:
        print(f"Нет прав на чтение файла {filename}")
        return None
```

## Контекстный менеджер with

### Зачем нужен контекстный менеджер
```python
# ПЛОХО - файл может остаться открытым при ошибке
def bad_file_handling():
    file = open("data.txt", "r")
    data = file.read()
    # Если здесь произойдет ошибка, файл не закроется!
    result = process_data(data)  # Может вызвать исключение
    file.close()  # Может не выполниться
    return result

# ХОРОШО - файл закроется автоматически
def good_file_handling():
    with open("data.txt", "r", encoding="utf-8") as file:
        data = file.read()
        return process_data(data)
    # Файл автоматически закроется даже при ошибке
```

### Как работает with
```python
# Контекстный менеджер вызывает два специальных метода:
# __enter__() - при входе в блок with
# __exit__() - при выходе из блока (даже при ошибке)

class FileManager:
    """Простой контекстный менеджер для демонстрации"""
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"Открываем файл {self.filename}")
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Закрываем файл {self.filename}")
        if self.file:
            self.file.close()
        
        # Если вернуть True, исключение будет подавлено
        if exc_type:
            print(f"Произошла ошибка: {exc_value}")
        return False  # Не подавляем исключения

# Использование
with FileManager("test.txt", "w") as f:
    f.write("Тестовые данные")
# Файл автоматически закроется
```

### Множественные контекстные менеджеры
```python
# Несколько файлов одновременно
def copy_file(source, destination):
    """Копирование файла"""
    with open(source, "r", encoding="utf-8") as src, \
         open(destination, "w", encoding="utf-8") as dst:
        dst.write(src.read())

# Альтернативный синтаксис (более читаемый)
def copy_file_v2(source, destination):
    with open(source, "r", encoding="utf-8") as src:
        with open(destination, "w", encoding="utf-8") as dst:
            dst.write(src.read())

# Использование contextlib
from contextlib import ExitStack

def process_multiple_files(filenames):
    """Обработка нескольких файлов"""
    with ExitStack() as stack:
        files = [stack.enter_context(open(fname, "r", encoding="utf-8")) 
                 for fname in filenames]
        
        for i, file in enumerate(files):
            print(f"Файл {i+1}: {len(file.read())} символов")
```

## Работа с различными форматами файлов

### CSV файлы
```python
import csv

def write_csv(filename, data, headers):
    """Запись данных в CSV файл"""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

def read_csv(filename):
    """Чтение CSV файла"""
    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Первая строка - заголовки
        
        data = []
        for row in reader:
            # Создаем словарь для каждой строки
            row_dict = dict(zip(headers, row))
            data.append(row_dict)
        
        return data

# Пример использования
employees = [
    ["Анна", "разработчик", 80000],
    ["Петр", "менеджер", 120000],
    ["Мария", "дизайнер", 70000]
]

headers = ["Имя", "Должность", "Зарплата"]
write_csv("employees.csv", employees, headers)

# Чтение обратно
data = read_csv("employees.csv")
for employee in data:
    print(f"{employee['Имя']}: {employee['Зарплата']} руб.")
```

### JSON файлы
```python
import json

def save_config(config, filename):
    """Сохранение конфигурации в JSON"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def load_config(filename, default=None):
    """Загрузка конфигурации из JSON"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return default or {}
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON: {e}")
        return default or {}

# Пример использования
app_config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp"
    },
    "api": {
        "version": "1.0",
        "debug": True
    },
    "features": ["auth", "analytics", "notifications"]
}

save_config(app_config, "config.json")
loaded_config = load_config("config.json")
print(f"База данных: {loaded_config['database']['host']}")
```

### Бинарные файлы
```python
# Работа с изображениями и другими бинарными файлами
def copy_binary_file(source, destination):
    """Копирование бинарного файла"""
    with open(source, "rb") as src:
        with open(destination, "wb") as dst:
            # Копируем по блокам для больших файлов
            while True:
                chunk = src.read(8192)  # 8KB блоки
                if not chunk:
                    break
                dst.write(chunk)

def get_file_signature(filename):
    """Получение сигнатуры файла (первые байты)"""
    try:
        with open(filename, "rb") as f:
            signature = f.read(8)
            return signature.hex()
    except Exception as e:
        return f"Ошибка: {e}"

# Определение типа файла по сигнатуре
def detect_file_type(filename):
    """Определение типа файла по magic bytes"""
    signatures = {
        "89504e47": "PNG",
        "ffd8ffe0": "JPEG",
        "25504446": "PDF",
        "504b0304": "ZIP"
    }
    
    signature = get_file_signature(filename)
    if signature:
        file_type = signatures.get(signature[:8].lower(), "Неизвестный")
        return file_type
    return None
```

## Продвинутые контекстные менеджеры

### Создание собственного контекстного менеджера
```python
class TimedOperation:
    """Контекстный менеджер для измерения времени выполнения"""
    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        print(f"Начинаем операцию: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        import time
        end_time = time.time()
        duration = end_time - self.start_time
        
        if exc_type:
            print(f"Операция {self.operation_name} завершилась с ошибкой за {duration:.2f}с")
        else:
            print(f"Операция {self.operation_name} завершена за {duration:.2f}с")
        
        return False  # Не подавляем исключения

# Использование
with TimedOperation("Обработка файла"):
    time.sleep(1)  # Имитация работы
    # Дополнительная работа
```

### Использование contextlib
```python
from contextlib import contextmanager, closing
import sqlite3

@contextmanager
def database_connection(db_path):
    """Контекстный менеджер для подключения к базе данных"""
    conn = None
    try:
        print(f"Подключаемся к базе {db_path}")
        conn = sqlite3.connect(db_path)
        yield conn
    except Exception as e:
        print(f"Ошибка работы с базой: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
            print("Соединение с базой закрыто")

# Использование
with database_connection("test.db") as db:
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'Анна')")
    db.commit()

# Автоматическое закрытие ресурсов
import urllib.request

with closing(urllib.request.urlopen("http://example.com")) as response:
    data = response.read()
```

### Обработка ошибок в контекстных менеджерах
```python
class SafeFileProcessor:
    """Безопасный обработчик файлов с детальным логированием"""
    def __init__(self, filename, mode="r", backup=False):
        self.filename = filename
        self.mode = mode
        self.backup = backup
        self.file = None
        self.backup_file = None
    
    def __enter__(self):
        # Создаем backup если нужно
        if self.backup and os.path.exists(self.filename):
            backup_name = f"{self.filename}.backup"
            with open(self.filename, "rb") as src:
                with open(backup_name, "wb") as dst:
                    dst.write(src.read())
            self.backup_file = backup_name
            print(f"Создан backup: {backup_name}")
        
        try:
            self.file = open(self.filename, self.mode, encoding="utf-8")
            print(f"Файл открыт: {self.filename}")
            return self.file
        except Exception as e:
            print(f"Ошибка открытия файла: {e}")
            raise
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
            print(f"Файл закрыт: {self.filename}")
        
        if exc_type:
            print(f"Ошибка при работе с файлом: {exc_value}")
            # Восстанавливаем из backup при ошибке записи
            if self.backup_file and "w" in self.mode:
                try:
                    os.replace(self.backup_file, self.filename)
                    print("Файл восстановлен из backup")
                except:
                    pass
        else:
            # Удаляем backup при успешном выполнении
            if self.backup_file:
                try:
                    os.remove(self.backup_file)
                    print("Backup удален")
                except:
                    pass
        
        return False  # Не подавляем исключения

# Использование
try:
    with SafeFileProcessor("important.txt", "w", backup=True) as f:
        f.write("Важные данные\n")
        f.write("Вторая строка\n")
        # raise Exception("Имитация ошибки")  # Раскомментировать для тестирования
except Exception as e:
    print(f"Операция не выполнена: {e}")
```

## Обработка больших файлов

### Чтение по частям
```python
def process_large_file(filename, chunk_size=8192):
    """Эффективная обработка больших файлов"""
    total_chars = 0
    line_count = 0
    
    with open(filename, "r", encoding="utf-8") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            total_chars += len(chunk)
            line_count += chunk.count('\n')
    
    return {"chars": total_chars, "lines": line_count}

def process_large_file_by_lines(filename):
    """Обработка больших файлов построчно"""
    stats = {"lines": 0, "words": 0, "empty_lines": 0}
    
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            stats["lines"] += 1
            
            if line.strip():
                stats["words"] += len(line.split())
            else:
                stats["empty_lines"] += 1
    
    return stats

# Генератор для строк файла
def read_file_lines(filename):
    """Генератор для чтения файла по строкам"""
    with open(filename, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            yield line_num, line.strip()

# Использование генератора
def find_in_file(filename, search_term):
    """Поиск строки в файле"""
    matches = []
    for line_num, line in read_file_lines(filename):
        if search_term.lower() in line.lower():
            matches.append((line_num, line))
    return matches
```

### Потоковая обработка
```python
def stream_process_csv(input_file, output_file, transform_func):
    """Потоковая обработка CSV файла"""
    import csv
    
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:
        
        reader = csv.DictReader(infile)
        
        # Получаем заголовки (могут измениться после трансформации)
        first_row = next(reader)
        transformed_first = transform_func(first_row)
        headers = list(transformed_first.keys())
        
        writer = csv.DictWriter(outfile, fieldnames=headers)
        writer.writeheader()
        writer.writerow(transformed_first)
        
        # Обрабатываем остальные строки
        for row in reader:
            transformed_row = transform_func(row)
            writer.writerow(transformed_row)

# Пример трансформации
def transform_employee_data(row):
    """Трансформация данных сотрудника"""
    salary = float(row.get("salary", 0))
    return {
        "name": row["name"].title(),
        "position": row["position"],
        "salary": salary,
        "annual_salary": salary * 12,
        "tax": salary * 0.13
    }

# Использование
# stream_process_csv("input.csv", "output.csv", transform_employee_data)
```

## Конфигурационные файлы

### Простой конфигурационный модуль
```python
# Файл: settings.py
"""
Модуль настроек приложения
"""
import os
import json

# Базовые настройки
DEFAULT_CONFIG = {
    "app_name": "My Application",
    "version": "1.0.0",
    "debug": False,
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "myapp"
    },
    "logging": {
        "level": "INFO",
        "file": "app.log"
    }
}

class Settings:
    """Класс для управления настройками"""
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = DEFAULT_CONFIG.copy()
        self.load_config()
    
    def load_config(self):
        """Загрузка настроек из файла"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                    self._merge_config(file_config)
                print(f"Настройки загружены из {self.config_file}")
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")
        
        # Переопределение из переменных окружения
        self._load_from_env()
    
    def _merge_config(self, new_config):
        """Слияние конфигураций"""
        def merge_dict(base, update):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
        
        merge_dict(self.config, new_config)
    
    def _load_from_env(self):
        """Загрузка настроек из переменных окружения"""
        env_mappings = {
            "DEBUG": ("debug", lambda x: x.lower() == "true"),
            "DB_HOST": ("database.host", str),
            "DB_PORT": ("database.port", int),
            "LOG_LEVEL": ("logging.level", str)
        }
        
        for env_var, (config_path, converter) in env_mappings.items():
            value = os.environ.get(env_var)
            if value:
                self._set_nested_value(config_path, converter(value))
    
    def _set_nested_value(self, path, value):
        """Установка вложенного значения по пути"""
        keys = path.split(".")
        current = self.config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def get(self, path, default=None):
        """Получение настройки по пути"""
        keys = path.split(".")
        current = self.config
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default
    
    def save_config(self):
        """Сохранение текущих настроек"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

# Использование
settings = Settings()
print(f"Приложение: {settings.get('app_name')}")
print(f"База данных: {settings.get('database.host')}:{settings.get('database.port')}")
print(f"Отладка: {settings.get('debug')}")
```

## Логирование в файлы

### Настройка логирования в модуле
```python
# Файл: logger_utils.py
"""
Утилиты для логирования
"""
import logging
import os
from datetime import datetime

class CustomFormatter(logging.Formatter):
    """Кастомный форматтер для логов"""
    
    COLORS = {
        logging.DEBUG: '\033[36m',    # Cyan
        logging.INFO: '\033[32m',     # Green  
        logging.WARNING: '\033[33m',  # Yellow
        logging.ERROR: '\033[31m',    # Red
        logging.CRITICAL: '\033[35m'  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Цвет для консоли
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Базовое форматирование
        formatted = super().format(record)
        
        # Добавляем цвет только для консольного вывода
        if hasattr(record, 'console_output'):
            return f"{color}{formatted}{self.RESET}"
        return formatted

def setup_logger(name, log_file=None, level=logging.INFO):
    """Настройка логгера с файловым и консольным выводом"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Избегаем дублирования handlers
    if logger.handlers:
        return logger
    
    # Форматтер
    formatter = CustomFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Консольный handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Файловый handler
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Ротация логов
def setup_rotating_logger(name, log_file, max_bytes=1024*1024, backup_count=5):
    """Логгер с ротацией файлов"""
    from logging.handlers import RotatingFileHandler
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Ротирующий файловый handler
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Использование в модуле
logger = setup_logger(__name__, "my_module.log")

def risky_operation(data):
    """Операция с логированием"""
    logger.info(f"Начинаем обработку {len(data)} элементов")
    
    try:
        result = []
        for i, item in enumerate(data):
            if i % 100 == 0:
                logger.debug(f"Обработано {i} элементов")
            
            # Имитация обработки
            processed = item * 2
            result.append(processed)
        
        logger.info(f"Обработка завершена успешно")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка обработки: {e}")
        raise
```

## Модульная архитектура

### Организация проекта
```python
# Структура проекта:
# myproject/
#   __init__.py
#   config/
#     __init__.py
#     settings.py
#   utils/
#     __init__.py
#     file_utils.py
#     string_utils.py
#   models/
#     __init__.py
#     user.py
#     product.py
#   main.py

# Файл: myproject/__init__.py
"""
Главный пакет приложения
"""
__version__ = "1.0.0"

# Экспорт основных компонентов
from .config.settings import Settings
from .utils.file_utils import safe_read_file, safe_write_file

# Упрощение импорта для пользователей
__all__ = ["Settings", "safe_read_file", "safe_write_file"]

# Файл: myproject/utils/__init__.py
"""
Пакет утилит
"""
from .file_utils import *
from .string_utils import *
```

### Модуль с конфигурацией
```python
# Файл: myproject/config/settings.py
"""
Настройки приложения
"""
import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).parent.parent  # Корень проекта
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Создаем необходимые директории
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Настройки приложения
class AppConfig:
    """Конфигурация приложения"""
    
    # Основные настройки
    APP_NAME = "My Project"
    VERSION = "1.0.0"
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    
    # Пути
    DATA_DIR = DATA_DIR
    LOGS_DIR = LOGS_DIR
    CONFIG_FILE = BASE_DIR / "config.json"
    
    # База данных
    DATABASE_URL = os.environ.get(
        "DATABASE_URL", 
        f"sqlite:///{DATA_DIR}/app.db"
    )
    
    # Логирование
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "app.log"
    
    @classmethod
    def get_config_dict(cls):
        """Получение всех настроек в виде словаря"""
        return {
            key: getattr(cls, key) 
            for key in dir(cls) 
            if not key.startswith("_") and not callable(getattr(cls, key))
        }

# Использование конфигурации
config = AppConfig()
print(f"Приложение: {config.APP_NAME}")
print(f"Директория данных: {config.DATA_DIR}")
```

## Практические задачи

### Менеджер файлов
```python
# Файл: file_manager.py
"""
Менеджер файлов с различными операциями
"""
import os
import shutil
import hashlib
from datetime import datetime

class FileManager:
    """Класс для управления файлами"""
    
    def __init__(self, base_directory="."):
        self.base_dir = os.path.abspath(base_directory)
        self.logger = setup_logger("FileManager", "file_operations.log")
    
    def list_files(self, pattern="*", recursive=False):
        """Список файлов с фильтрацией"""
        import glob
        
        if recursive:
            search_pattern = os.path.join(self.base_dir, "**", pattern)
            files = glob.glob(search_pattern, recursive=True)
        else:
            search_pattern = os.path.join(self.base_dir, pattern)
            files = glob.glob(search_pattern)
        
        return [os.path.relpath(f, self.base_dir) for f in files if os.path.isfile(f)]
    
    def get_file_hash(self, filename):
        """Вычисление хэша файла"""
        file_path = os.path.join(self.base_dir, filename)
        
        if not os.path.exists(file_path):
            return None
        
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        
        return hash_md5.hexdigest()
    
    def safe_delete(self, filename, backup=True):
        """Безопасное удаление файла с backup"""
        file_path = os.path.join(self.base_dir, filename)
        
        if not os.path.exists(file_path):
            self.logger.warning(f"Файл не существует: {filename}")
            return False
        
        try:
            if backup:
                backup_dir = os.path.join(self.base_dir, ".backups")
                os.makedirs(backup_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{filename}.backup_{timestamp}"
                backup_path = os.path.join(backup_dir, backup_name)
                
                shutil.copy2(file_path, backup_path)
                self.logger.info(f"Создан backup: {backup_name}")
            
            os.remove(file_path)
            self.logger.info(f"Файл удален: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка удаления файла {filename}: {e}")
            return False
    
    def organize_by_extension(self):
        """Организация файлов по расширениям"""
        files = self.list_files("*")
        
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                ext_dir = os.path.join(self.base_dir, ext[1:].lower())  # Убираем точку
                os.makedirs(ext_dir, exist_ok=True)
                
                src = os.path.join(self.base_dir, file)
                dst = os.path.join(ext_dir, os.path.basename(file))
                
                try:
                    shutil.move(src, dst)
                    self.logger.info(f"Перемещен {file} в {ext_dir}")
                except Exception as e:
                    self.logger.error(f"Ошибка перемещения {file}: {e}")

# Использование
fm = FileManager("./test_directory")
files = fm.list_files("*.txt")
print(f"Текстовые файлы: {files}")
```

### Модуль для работы с данными
```python
# Файл: data_processor.py
"""
Модуль для обработки различных форматов данных
"""
import json
import csv
import os
from contextlib import contextmanager

class DataProcessor:
    """Универсальный обработчик данных"""
    
    @staticmethod
    @contextmanager
    def safe_file_operation(filename, mode="r"):
        """Контекстный менеджер для безопасной работы с файлами"""
        file_obj = None
        try:
            file_obj = open(filename, mode, encoding="utf-8")
            yield file_obj
        except FileNotFoundError:
            print(f"Файл не найден: {filename}")
            yield None
        except PermissionError:
            print(f"Нет прав доступа к файлу: {filename}")
            yield None
        except Exception as e:
            print(f"Ошибка работы с файлом {filename}: {e}")
            yield None
        finally:
            if file_obj:
                file_obj.close()
    
    @classmethod
    def load_data(cls, filename):
        """Универсальная загрузка данных по расширению файла"""
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        if ext == ".json":
            return cls.load_json(filename)
        elif ext == ".csv":
            return cls.load_csv(filename)
        elif ext == ".txt":
            return cls.load_text(filename)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {ext}")
    
    @classmethod
    def load_json(cls, filename):
        """Загрузка JSON данных"""
        with cls.safe_file_operation(filename, "r") as f:
            if f:
                return json.load(f)
            return None
    
    @classmethod
    def load_csv(cls, filename):
        """Загрузка CSV данных"""
        with cls.safe_file_operation(filename, "r") as f:
            if f:
                reader = csv.DictReader(f)
                return list(reader)
            return None
    
    @classmethod
    def load_text(cls, filename):
        """Загрузка текстовых данных"""
        with cls.safe_file_operation(filename, "r") as f:
            if f:
                return f.read()
            return None
    
    @classmethod
    def save_data(cls, data, filename):
        """Универсальное сохранение данных"""
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        if ext == ".json":
            return cls.save_json(data, filename)
        elif ext == ".csv":
            return cls.save_csv(data, filename)
        elif ext == ".txt":
            return cls.save_text(str(data), filename)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {ext}")
    
    @classmethod
    def save_json(cls, data, filename):
        """Сохранение в JSON"""
        with cls.safe_file_operation(filename, "w") as f:
            if f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                return True
            return False
    
    @classmethod
    def save_csv(cls, data, filename):
        """Сохранение в CSV"""
        if not data:
            return False
        
        with cls.safe_file_operation(filename, "w") as f:
            if f:
                if isinstance(data[0], dict):
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    writer = csv.writer(f)
                    writer.writerows(data)
                return True
            return False
    
    @classmethod
    def save_text(cls, data, filename):
        """Сохранение текста"""
        with cls.safe_file_operation(filename, "w") as f:
            if f:
                f.write(data)
                return True
            return False

# Использование
processor = DataProcessor()

# Загрузка разных форматов
json_data = processor.load_data("config.json")
csv_data = processor.load_data("employees.csv")
text_data = processor.load_data("readme.txt")

# Сохранение данных
sample_data = [
    {"name": "Анна", "age": 25},
    {"name": "Петр", "age": 30}
]

processor.save_data(sample_data, "users.json")
processor.save_data(sample_data, "users.csv")
```

## Ключевые моменты для экзамена

- **Модули** - файлы .py для организации кода и переиспользования
- **Импорт** - `import`, `from module import name`, псевдонимы через `as`
- **__name__ == "__main__"** - код выполняется только при прямом запуске
- **open()** - функция для работы с файлами, режимы r/w/a/x/b/t/+
- **with** - контекстный менеджер для автоматического управления ресурсами
- **Кодировки** - обязательно указывать `encoding="utf-8"`
- **Обработка ошибок** - try/except для FileNotFoundError, PermissionError
- **Большие файлы** - читать по частям или построчно
- **Контекстные менеджеры** - `__enter__()` и `__exit__()` методы
- **Модульная архитектура** - разделение по функциональности, пакеты с `__init__.py`