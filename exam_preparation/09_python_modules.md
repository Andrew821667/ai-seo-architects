# Модули и библиотеки. Модуль re. Модуль os

## Что такое модули

### Определение и назначение
```python
# Модуль - это файл с Python кодом (.py)
# Библиотека - коллекция модулей для решения задач
# Пакет - директория с модулями и файлом __init__.py

# Зачем нужны модули:
# 1. Организация кода
# 2. Повторное использование
# 3. Разделение ответственности
# 4. Пространство имен
```

### Способы импорта
```python
# 1. Импорт всего модуля
import math
result = math.sqrt(16)  # 4.0

# 2. Импорт конкретных функций
from math import sqrt, pi
result = sqrt(16)  # 4.0
print(pi)          # 3.141592653589793

# 3. Импорт с псевдонимом
import datetime as dt
now = dt.datetime.now()

# 4. Импорт всего содержимого (не рекомендуется)
from math import *
result = sqrt(16)  # Может перекрыть существующие имена

# 5. Импорт с псевдонимом для функций
from datetime import datetime as dt_class
now = dt_class.now()
```

### Системные пути модулей
```python
import sys

# Где Python ищет модули
print("Пути поиска модулей:")
for path in sys.path:
    print(f"  {path}")

# Добавление собственного пути
sys.path.append("/path/to/my/modules")

# Информация о модуле
import math
print(f"Расположение модуля math: {math.__file__}")
print(f"Содержимое модуля: {dir(math)}")
```

## Модуль re (регулярные выражения)

### Основные функции
```python
import re

# re.search() - поиск первого совпадения
text = "Мой телефон: +7-123-456-78-90"
pattern = r"\+7-\d{3}-\d{3}-\d{2}-\d{2}"
match = re.search(pattern, text)

if match:
    print(f"Найден телефон: {match.group()}")  # +7-123-456-78-90
    print(f"Позиция: {match.start()}-{match.end()}")  # 13-29

# re.findall() - поиск всех совпадений
text = "Email: anna@gmail.com, peter@yandex.ru"
emails = re.findall(r"\w+@\w+\.\w+", text)
print(emails)  # ['anna@gmail.com', 'peter@yandex.ru']

# re.sub() - замена
text = "Дата: 2024-12-31, время: 15:30:45"
# Заменяем дату на формат DD.MM.YYYY
new_text = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3.\2.\1", text)
print(new_text)  # "Дата: 31.12.2024, время: 15:30:45"
```

### Метасимволы и паттерны
```python
# Основные метасимволы
patterns = {
    r"\d": "любая цифра (0-9)",
    r"\w": "буква, цифра или подчеркивание",
    r"\s": "пробельный символ",
    r".": "любой символ кроме новой строки",
    r"^": "начало строки",
    r"$": "конец строки",
    r"*": "0 или более повторений",
    r"+": "1 или более повторений",
    r"?": "0 или 1 повторение",
    r"{n}": "ровно n повторений",
    r"{n,m}": "от n до m повторений"
}

# Примеры использования
test_strings = [
    "123",           # только цифры
    "abc123",        # буквы и цифры
    "hello@mail.ru", # email
    "+7-900-123-45-67" # телефон
]

# Проверка паттернов
print(re.match(r"^\d+$", "123"))        # Только цифры: Match
print(re.match(r"^\w+@\w+\.\w+$", "hello@mail.ru"))  # Email: Match
```

### Группы в регулярных выражениях
```python
# Группы для извлечения частей
phone_pattern = r"\+7-(\d{3})-(\d{3})-(\d{2})-(\d{2})"
text = "Телефон: +7-123-456-78-90"

match = re.search(phone_pattern, text)
if match:
    print(f"Полный номер: {match.group(0)}")  # +7-123-456-78-90
    print(f"Код города: {match.group(1)}")    # 123
    print(f"Первая часть: {match.group(2)}")  # 456
    print(f"Все группы: {match.groups()}")    # ('123', '456', '78', '90')

# Именованные группы
email_pattern = r"(?P<user>\w+)@(?P<domain>\w+)\.(?P<tld>\w+)"
email = "anna@example.com"
match = re.search(email_pattern, email)

if match:
    print(f"Пользователь: {match.group('user')}")    # anna
    print(f"Домен: {match.group('domain')}")         # example
    print(f"Зона: {match.group('tld')}")            # com
    print(f"Словарь: {match.groupdict()}")          # {'user': 'anna', 'domain': 'example', 'tld': 'com'}
```

### Компиляция паттернов
```python
# Для многократного использования эффективнее компилировать
email_regex = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
phone_regex = re.compile(r"\+7-\d{3}-\d{3}-\d{2}-\d{2}")

def extract_contacts(text):
    """Извлечение контактов из текста"""
    emails = email_regex.findall(text)
    phones = phone_regex.findall(text)
    
    return {
        "emails": emails,
        "phones": phones
    }

# Тестирование
contact_text = """
Свяжитесь с нами:
Email: info@company.com, support@company.ru
Телефоны: +7-495-123-45-67, +7-812-987-65-43
"""

contacts = extract_contacts(contact_text)
print(contacts)
```

### Валидация данных
```python
def create_validators():
    """Создание валидаторов с компилированными regex"""
    validators = {
        "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
        "phone": re.compile(r"^\+7-\d{3}-\d{3}-\d{2}-\d{2}$"),
        "password": re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"),  # Мин 8 символов, буквы разных регистров, цифра
        "username": re.compile(r"^[a-zA-Z][a-zA-Z0-9_]{2,19}$")  # Начинается с буквы, 3-20 символов
    }
    return validators

def validate_data(data, validators):
    """Валидация данных с помощью regex"""
    results = {}
    
    for field, value in data.items():
        if field in validators:
            is_valid = bool(validators[field].match(str(value)))
            results[field] = {"value": value, "valid": is_valid}
        else:
            results[field] = {"value": value, "valid": None}
    
    return results

# Использование
validators = create_validators()
test_data = {
    "email": "user@example.com",
    "phone": "+7-123-456-78-90",
    "password": "MyPass123",
    "username": "user_name"
}

validation_results = validate_data(test_data, validators)
for field, result in validation_results.items():
    status = "✓" if result["valid"] else "✗"
    print(f"{field}: {result['value']} {status}")
```

## Модуль os

### Работа с путями
```python
import os

# Текущая рабочая директория
current_dir = os.getcwd()
print(f"Текущая директория: {current_dir}")

# Изменение рабочей директории
# os.chdir("/path/to/new/directory")

# Домашняя директория пользователя
home_dir = os.path.expanduser("~")
print(f"Домашняя директория: {home_dir}")

# Переменные окружения
python_path = os.environ.get("PYTHONPATH", "Не установлена")
print(f"PYTHONPATH: {python_path}")

# Установка переменной окружения
os.environ["MY_VAR"] = "test_value"
```

### os.path - работа с путями файлов
```python
import os.path

file_path = "/Users/andrew/documents/report.txt"

# Разбор пути
print(f"Директория: {os.path.dirname(file_path)}")      # /Users/andrew/documents
print(f"Имя файла: {os.path.basename(file_path)}")      # report.txt
print(f"Разделение: {os.path.split(file_path)}")        # ('/Users/andrew/documents', 'report.txt')

# Работа с расширениями
name, ext = os.path.splitext(file_path)
print(f"Имя без расширения: {name}")  # /Users/andrew/documents/report
print(f"Расширение: {ext}")           # .txt

# Построение путей
documents_dir = os.path.join(home_dir, "Documents")
config_file = os.path.join(documents_dir, "config.json")
print(f"Путь к конфигу: {config_file}")

# Проверки существования
print(f"Путь существует: {os.path.exists(file_path)}")
print(f"Это файл: {os.path.isfile(file_path)}")
print(f"Это директория: {os.path.isdir('/Users/andrew')}")

# Абсолютный путь
relative_path = "data/config.json"
absolute_path = os.path.abspath(relative_path)
print(f"Абсолютный путь: {absolute_path}")
```

### Операции с файлами и директориями
```python
# Создание директории
def create_directory(path):
    """Безопасное создание директории"""
    try:
        os.makedirs(path, exist_ok=True)  # exist_ok=True не вызывает ошибку если существует
        print(f"Директория создана: {path}")
    except PermissionError:
        print(f"Нет прав для создания {path}")

# Получение списка файлов
def list_files(directory, extension=None):
    """Список файлов в директории с фильтрацией по расширению"""
    try:
        files = os.listdir(directory)
        
        if extension:
            files = [f for f in files if f.endswith(extension)]
        
        return files
    except FileNotFoundError:
        print(f"Директория {directory} не найдена")
        return []

# Получение информации о файле
def get_file_info(file_path):
    """Информация о файле"""
    if not os.path.exists(file_path):
        return None
    
    stat = os.stat(file_path)
    
    return {
        "size": stat.st_size,
        "modified": stat.st_mtime,
        "created": stat.st_ctime,
        "is_file": os.path.isfile(file_path),
        "is_dir": os.path.isdir(file_path)
    }

# Использование
files = list_files(".", ".py")  # Все .py файлы в текущей директории
print(f"Python файлы: {files}")
```

### Рекурсивная работа с директориями
```python
def find_files_recursive(directory, pattern="*"):
    """Рекурсивный поиск файлов"""
    import glob
    
    # glob.glob() для простых паттернов
    search_pattern = os.path.join(directory, "**", pattern)
    files = glob.glob(search_pattern, recursive=True)
    
    return files

def walk_directory(directory):
    """Обход директорий с os.walk"""
    for root, dirs, files in os.walk(directory):
        print(f"Директория: {root}")
        print(f"  Поддиректории: {dirs}")
        print(f"  Файлы: {files[:5]}")  # Первые 5 файлов
        if len(files) > 5:
            print(f"  ... и еще {len(files) - 5} файлов")
        print()

def analyze_directory_structure(directory):
    """Анализ структуры директории"""
    total_files = 0
    total_size = 0
    file_types = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Подсчет файлов
            total_files += 1
            
            # Подсчет размера
            try:
                size = os.path.getsize(file_path)
                total_size += size
            except OSError:
                continue
            
            # Подсчет типов файлов
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
    
    return {
        "total_files": total_files,
        "total_size": total_size,
        "file_types": file_types
    }

# Пример использования
# analysis = analyze_directory_structure(".")
# print(f"Всего файлов: {analysis['total_files']}")
# print(f"Общий размер: {analysis['total_size'] / 1024:.1f} KB")
```

## Полезные встроенные модули

### datetime - работа с датой и временем
```python
from datetime import datetime, date, time, timedelta

# Текущая дата и время
now = datetime.now()
today = date.today()
current_time = datetime.now().time()

print(f"Сейчас: {now}")
print(f"Сегодня: {today}")
print(f"Время: {current_time}")

# Создание конкретных дат
birthday = date(1990, 5, 15)
meeting = datetime(2024, 12, 31, 14, 30, 0)

# Арифметика с датами
tomorrow = today + timedelta(days=1)
week_ago = now - timedelta(weeks=1)
in_6_months = now + timedelta(days=180)

# Форматирование дат
formatted = now.strftime("%Y-%m-%d %H:%M:%S")  # "2024-12-31 15:30:45"
formatted = now.strftime("%d.%m.%Y")           # "31.12.2024"

# Парсинг дат из строк
date_string = "2024-12-31"
parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
```

### json - работа с JSON
```python
import json

# Python объект в JSON
data = {
    "name": "Анна",
    "age": 25,
    "skills": ["Python", "JavaScript", "SQL"],
    "active": True
}

# Сериализация в JSON строку
json_string = json.dumps(data, ensure_ascii=False, indent=2)
print(json_string)

# Запись в файл
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Чтение из JSON строки
parsed_data = json.loads(json_string)
print(parsed_data["name"])

# Чтение из файла
with open("data.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
```

### random - генерация случайных значений
```python
import random

# Случайные числа
print(random.random())          # [0.0, 1.0)
print(random.randint(1, 10))    # [1, 10]
print(random.uniform(1.5, 10.5))  # [1.5, 10.5)

# Выбор из последовательности
colors = ["красный", "зеленый", "синий"]
print(random.choice(colors))     # Случайный цвет
print(random.choices(colors, k=3))  # 3 случайных цвета (с повторениями)
print(random.sample(colors, 2))  # 2 уникальных цвета

# Перемешивание
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)  # Изменяет исходный список
print(numbers)

# Генерация данных
def generate_test_users(count):
    names = ["Анна", "Петр", "Мария", "Иван", "Ольга"]
    for i in range(count):
        yield {
            "id": i + 1,
            "name": random.choice(names),
            "age": random.randint(18, 65),
            "score": round(random.uniform(0, 100), 1)
        }

users = list(generate_test_users(5))
for user in users:
    print(user)
```

### collections - расширенные типы данных
```python
from collections import Counter, defaultdict, OrderedDict, namedtuple

# Counter - подсчет элементов
text = "python programming"
char_count = Counter(text)
print(char_count)  # Counter({'p': 2, 'r': 3, 'o': 2, 'g': 2, 'm': 2, ...})
print(char_count.most_common(3))  # Топ 3 символа

# defaultdict - словарь с значениями по умолчанию
groups = defaultdict(list)
students = [("Анна", "математика"), ("Петр", "физика"), ("Анна", "химия")]

for name, subject in students:
    groups[name].append(subject)

print(dict(groups))  # {'Анна': ['математика', 'химия'], 'Петр': ['физика']}

# namedtuple - именованные кортежи
Point = namedtuple("Point", ["x", "y"])
person = namedtuple("Person", ["name", "age", "city"])

p1 = Point(10, 20)
print(f"Координаты: x={p1.x}, y={p1.y}")

student = person("Анна", 20, "Москва")
print(f"Студент: {student.name}, {student.age} лет, город {student.city}")
```

## Создание собственных модулей

### Структура модуля
```python
# Файл: my_math.py
"""
Модуль для математических операций
"""

__version__ = "1.0.0"
__author__ = "Andrew"

# Константы модуля
PI = 3.141592653589793
E = 2.718281828459045

# Функции модуля
def factorial(n):
    """Вычисление факториала"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def is_prime(n):
    """Проверка простого числа"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a, b):
    """Наибольший общий делитель"""
    while b:
        a, b = b, a % b
    return a

# Приватная функция (начинается с _)
def _helper_function():
    """Вспомогательная функция для внутреннего использования"""
    pass

# Код, выполняемый при запуске модуля напрямую
if __name__ == "__main__":
    print("Тестирование модуля my_math")
    print(f"5! = {factorial(5)}")
    print(f"17 простое? {is_prime(17)}")
    print(f"НОД(48, 18) = {gcd(48, 18)}")
```

### Использование собственного модуля
```python
# Импорт собственного модуля
import my_math

# Использование функций
result = my_math.factorial(5)
print(f"5! = {result}")

# Доступ к константам
print(f"π ≈ {my_math.PI}")

# Информация о модуле
print(f"Версия: {my_math.__version__}")
print(f"Автор: {my_math.__author__}")

# Список содержимого модуля
print("Содержимое модуля:")
for item in dir(my_math):
    if not item.startswith("_"):  # Пропускаем приватные элементы
        print(f"  {item}")
```

## Пакеты

### Структура пакета
```python
# Структура директорий:
# mypackage/
#   __init__.py
#   math_utils.py
#   string_utils.py
#   data/
#     __init__.py
#     processors.py

# Файл: mypackage/__init__.py
"""
Мой пакет для различных утилит
"""

__version__ = "1.0.0"

# Импорт основных функций для удобства
from .math_utils import factorial, is_prime
from .string_utils import clean_text, validate_email

# Определение того, что доступно при from mypackage import *
__all__ = ["factorial", "is_prime", "clean_text", "validate_email"]
```

### Импорт из пакетов
```python
# Различные способы импорта из пакета
import mypackage
from mypackage import factorial
from mypackage.math_utils import gcd
from mypackage.data.processors import process_csv

# Относительные импорты (внутри пакета)
# В файле mypackage/string_utils.py:
# from .math_utils import factorial  # Из того же пакета
# from ..otherpackage import something  # Из родительского пакета
```

## Управление зависимостями

### requirements.txt
```python
# Создание файла зависимостей
# pip freeze > requirements.txt

# Пример requirements.txt:
"""
requests==2.31.0
beautifulsoup4==4.12.2
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
"""

# Установка зависимостей
# pip install -r requirements.txt
```

### Виртуальные окружения
```bash
# Создание виртуального окружения
python -m venv myproject_env

# Активация (Windows)
myproject_env\Scripts\activate

# Активация (macOS/Linux)
source myproject_env/bin/activate

# Деактивация
deactivate
```

## Обработка ошибок при импорте

### try/except для импорта
```python
# Опциональная зависимость
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Pandas не установлен. Некоторые функции недоступны.")

def analyze_data(data):
    """Анализ данных с опциональным pandas"""
    if HAS_PANDAS:
        df = pd.DataFrame(data)
        return df.describe().to_dict()
    else:
        # Альтернативная реализация без pandas
        return {
            "count": len(data),
            "mean": sum(data) / len(data) if data else 0
        }

# Проверка версии модуля
def check_module_version(module_name, min_version):
    """Проверка версии модуля"""
    try:
        module = __import__(module_name)
        current_version = getattr(module, "__version__", "неизвестна")
        print(f"{module_name}: версия {current_version}")
        return current_version
    except ImportError:
        print(f"Модуль {module_name} не установлен")
        return None

# Примеры проверок
check_module_version("requests", "2.0.0")
check_module_version("pandas", "1.0.0")
```

## Практические примеры

### Создание конфигурационного модуля
```python
# Файл: config.py
"""
Конфигурационный модуль приложения
"""
import os
from datetime import datetime

# Базовые настройки
APP_NAME = "My Application"
VERSION = "1.0.0"
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Настройки базы данных
DATABASE_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "5432")),
    "name": os.environ.get("DB_NAME", "myapp"),
    "user": os.environ.get("DB_USER", "user"),
    "password": os.environ.get("DB_PASSWORD", "password")
}

# Логирование
LOG_CONFIG = {
    "level": os.environ.get("LOG_LEVEL", "INFO"),
    "file": os.environ.get("LOG_FILE", "app.log"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

def get_database_url():
    """Генерация URL подключения к базе данных"""
    config = DATABASE_CONFIG
    return f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['name']}"

def print_config():
    """Вывод текущей конфигурации"""
    print(f"Приложение: {APP_NAME} v{VERSION}")
    print(f"Режим отладки: {DEBUG}")
    print(f"База данных: {DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}")
    print(f"Уровень логирования: {LOG_CONFIG['level']}")
```

### Утилиты для работы с файлами
```python
# Файл: file_utils.py
"""
Утилиты для работы с файлами
"""
import os
import json
import csv
from datetime import datetime

def ensure_directory(directory):
    """Убедиться что директория существует"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Создана директория: {directory}")

def backup_file(file_path):
    """Создание backup копии файла"""
    if not os.path.exists(file_path):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    
    import shutil
    shutil.copy2(file_path, backup_path)
    return backup_path

def read_config_file(file_path):
    """Чтение конфигурационного файла (JSON или простой)"""
    if not os.path.exists(file_path):
        return {}
    
    try:
        # Пробуем как JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Если не JSON, читаем как простой конфиг
        config = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        return config

def safe_write_file(file_path, content, backup=True):
    """Безопасная запись файла с backup"""
    if backup and os.path.exists(file_path):
        backup_path = backup_file(file_path)
        print(f"Создан backup: {backup_path}")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Файл записан: {file_path}")
        return True
    except Exception as e:
        print(f"Ошибка записи файла: {e}")
        return False
```

### Логирование
```python
import logging
import os
from datetime import datetime

# Настройка логирования
def setup_logging(log_file="app.log", level=logging.INFO):
    """Настройка системы логирования"""
    
    # Создаем formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Консольный handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Файловый handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Настройка root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Использование логирования
def example_function():
    logger = logging.getLogger(__name__)
    
    logger.info("Функция запущена")
    
    try:
        result = 10 / 2
        logger.info(f"Результат вычисления: {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка в вычислениях: {e}")
        raise

# Настройка и использование
setup_logging("my_app.log")
example_function()
```

## Частые ошибки

### 1. Циклический импорт
```python
# module_a.py
import module_b
def function_a():
    return module_b.function_b()

# module_b.py  
import module_a  # Циклический импорт!
def function_b():
    return module_a.function_a()

# РЕШЕНИЕ: перенести общий код в третий модуль
# или использовать импорт внутри функции
def function_b():
    import module_a  # Локальный импорт
    return module_a.function_a()
```

### 2. Неправильные пути
```python
# ПЛОХО - жестко заданные пути
file_path = "C:\\Users\\Andrew\\data.txt"  # Не работает на других системах

# ХОРОШО - кроссплатформенные пути
import os
user_home = os.path.expanduser("~")
file_path = os.path.join(user_home, "data.txt")

# Относительно текущего модуля
current_dir = os.path.dirname(__file__)
config_path = os.path.join(current_dir, "config.json")
```

### 3. Забывание закрывать файлы
```python
# ПЛОХО - файл может остаться открытым
file = open("data.txt", "r")
data = file.read()
file.close()  # Может не выполниться при ошибке

# ХОРОШО - контекстный менеджер
with open("data.txt", "r", encoding="utf-8") as file:
    data = file.read()
# Файл автоматически закрывается
```

## Ключевые моменты для экзамена

- **Модули** - файлы с Python кодом для организации и переиспользования
- **Импорт** - `import`, `from ... import`, псевдонимы через `as`
- **re модуль** - регулярные выражения для поиска и замены в тексте
- **os модуль** - работа с операционной системой, файлами и директориями
- **os.path** - кроссплатформенная работа с путями файлов
- **Встроенные модули** - datetime, json, random, collections
- **sys.path** - список путей поиска модулей
- **__name__ == "__main__"** - код, выполняемый только при прямом запуске
- **Пакеты** - директории с модулями и `__init__.py`
- **Виртуальные окружения** - изоляция зависимостей проекта