# Замыкания и декораторы

## Замыкания (Closures)

### Что такое замыкание
```python
# Замыкание - функция, которая "помнит" переменные из внешней области видимости
def outer_function(x):
    # Внешняя переменная
    multiplier = x
    
    def inner_function(y):
        # Внутренняя функция имеет доступ к multiplier
        return y * multiplier
    
    return inner_function

# Создание замыкания
double = outer_function(2)  # multiplier = 2
triple = outer_function(3)  # multiplier = 3

print(double(5))  # 10 (5 * 2)
print(triple(5))  # 15 (5 * 3)

# Проверим, что переменная действительно "захвачена"
print(double.__closure__)  # (<cell at 0x...: int object at 0x...>,)
print(double.__closure__[0].cell_contents)  # 2
```

### Практические примеры замыканий
```python
# Счетчик с замыканием
def create_counter(start=0):
    """Создает функцию-счетчик"""
    count = start
    
    def counter():
        nonlocal count  # Позволяет изменять переменную из внешней области
        count += 1
        return count
    
    return counter

# Использование
counter1 = create_counter()
counter2 = create_counter(100)

print(counter1())  # 1
print(counter1())  # 2
print(counter2())  # 101
print(counter1())  # 3

# Банковский счет с замыканием
def create_account(initial_balance=0):
    """Создает замкнутый банковский счет"""
    balance = initial_balance
    
    def deposit(amount):
        nonlocal balance
        if amount > 0:
            balance += amount
            return f"Депозит: {amount}. Баланс: {balance}"
        return "Сумма должна быть положительной"
    
    def withdraw(amount):
        nonlocal balance
        if 0 < amount <= balance:
            balance -= amount
            return f"Снятие: {amount}. Баланс: {balance}"
        return "Недостаточно средств или некорректная сумма"
    
    def get_balance():
        return balance
    
    # Возвращаем словарь функций
    return {
        "deposit": deposit,
        "withdraw": withdraw,
        "balance": get_balance
    }

# Использование
account = create_account(1000)
print(account["deposit"](500))   # Депозит: 500. Баланс: 1500
print(account["withdraw"](200))  # Снятие: 200. Баланс: 1300
print(f"Текущий баланс: {account['balance']()}")  # 1300
```

### Замыкания для конфигурации
```python
def create_validator(min_length=0, max_length=100, required_chars=None):
    """Создает валидатор с настройками"""
    required = required_chars or []
    
    def validate(text):
        errors = []
        
        # Проверка длины
        if len(text) < min_length:
            errors.append(f"Минимальная длина: {min_length}")
        
        if len(text) > max_length:
            errors.append(f"Максимальная длина: {max_length}")
        
        # Проверка обязательных символов
        for char_type in required:
            if char_type == "digit" and not any(c.isdigit() for c in text):
                errors.append("Требуется цифра")
            elif char_type == "upper" and not any(c.isupper() for c in text):
                errors.append("Требуется заглавная буква")
            elif char_type == "lower" and not any(c.islower() for c in text):
                errors.append("Требуется строчная буква")
        
        return len(errors) == 0, errors
    
    return validate

# Создание специализированных валидаторов
password_validator = create_validator(
    min_length=8, 
    max_length=50, 
    required_chars=["digit", "upper", "lower"]
)

username_validator = create_validator(
    min_length=3,
    max_length=20
)

# Тестирование
passwords = ["123", "password", "Password", "Password123"]
for pwd in passwords:
    valid, errors = password_validator(pwd)
    print(f"{pwd}: {'✓' if valid else '✗'} {', '.join(errors)}")
```

## Декораторы без параметров

### Базовые декораторы
```python
# Декоратор - функция, которая принимает другую функцию и расширяет её поведение

def my_decorator(func):
    """Простой декоратор"""
    def wrapper(*args, **kwargs):
        print(f"Вызывается функция {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} завершена")
        return result
    return wrapper

# Применение декоратора
@my_decorator
def greet(name):
    return f"Привет, {name}!"

# Эквивалентно: greet = my_decorator(greet)

print(greet("Анна"))
# Вывод:
# Вызывается функция greet
# Функция greet завершена
# Привет, Анна!
```

### Декоратор для измерения времени
```python
import time
import functools

def measure_time(func):
    """Декоратор для измерения времени выполнения"""
    @functools.wraps(func)  # Сохраняет метаданные оригинальной функции
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"{func.__name__} выполнена за {execution_time:.4f} секунд")
        return result
    
    return wrapper

@measure_time
def slow_function():
    """Медленная функция для демонстрации"""
    time.sleep(1)
    return "Готово"

@measure_time
def calculate_sum(n):
    """Вычисление суммы от 1 до n"""
    return sum(range(1, n + 1))

# Использование
result = slow_function()  # slow_function выполнена за 1.0012 секунд
sum_result = calculate_sum(1000000)  # calculate_sum выполнена за 0.0234 секунд
```

### Декоратор для логирования
```python
import functools
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def log_calls(func):
    """Декоратор для логирования вызовов функций"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Форматируем аргументы для логирования
        args_str = ", ".join(map(str, args))
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        
        logger.info(f"Вызов {func.__name__}({all_args})")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} завершена успешно")
            return result
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__}: {e}")
            raise
    
    return wrapper

@log_calls
def divide(a, b):
    """Деление с логированием"""
    if b == 0:
        raise ValueError("Деление на ноль")
    return a / b

@log_calls
def process_data(data, multiplier=2):
    """Обработка данных с логированием"""
    return [x * multiplier for x in data]

# Использование
result = divide(10, 2)  # Логирует вызов и результат
data = process_data([1, 2, 3], multiplier=3)  # Логирует с kwargs
# divide(10, 0)  # Логирует ошибку
```

## Декораторы с параметрами

### Создание параметризованных декораторов
```python
def retry(max_attempts=3, delay=1):
    """Декоратор для повторных попыток выполнения функции"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(f"{func.__name__} успешно выполнена с {attempt + 1} попытки")
                    return result
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"Попытка {attempt + 1} неудачна, повтор через {delay}с...")
                        time.sleep(delay)
                    else:
                        print(f"Все {max_attempts} попыток исчерпаны")
            
            raise last_exception
        
        return wrapper
    return decorator

# Использование с параметрами
@retry(max_attempts=3, delay=0.5)
def unreliable_function():
    """Функция, которая может завершиться ошибкой"""
    import random
    if random.random() < 0.7:  # 70% вероятность ошибки
        raise Exception("Случайная ошибка")
    return "Успех!"

# Вызов
try:
    result = unreliable_function()
    print(f"Результат: {result}")
except Exception as e:
    print(f"Окончательная ошибка: {e}")
```

### Декоратор кэширования
```python
def cache(max_size=128):
    """Декоратор для кэширования результатов функции"""
    def decorator(func):
        cache_dict = {}
        access_order = []
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Создаем ключ из аргументов
            key = str(args) + str(sorted(kwargs.items()))
            
            # Проверяем кэш
            if key in cache_dict:
                # Обновляем порядок доступа
                access_order.remove(key)
                access_order.append(key)
                print(f"Кэш попадание для {func.__name__}")
                return cache_dict[key]
            
            # Вычисляем результат
            result = func(*args, **kwargs)
            
            # Добавляем в кэш
            cache_dict[key] = result
            access_order.append(key)
            
            # Удаляем старые элементы если превышен размер
            while len(cache_dict) > max_size:
                oldest_key = access_order.pop(0)
                del cache_dict[oldest_key]
            
            print(f"Результат кэширован для {func.__name__}")
            return result
        
        # Добавляем методы для управления кэшем
        wrapper.cache_clear = lambda: cache_dict.clear() or access_order.clear()
        wrapper.cache_info = lambda: {"size": len(cache_dict), "max_size": max_size}
        
        return wrapper
    return decorator

@cache(max_size=10)
def fibonacci(n):
    """Числа Фибоначчи с кэшированием"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

@cache(max_size=5)
def expensive_calculation(x, y):
    """Дорогое вычисление"""
    time.sleep(0.1)  # Имитация сложных вычислений
    return x ** y + y ** x

# Тестирование
print(f"fibonacci(10) = {fibonacci(10)}")  # Много кэшированных вызовов
print(f"fibonacci(10) = {fibonacci(10)}")  # Кэш попадание
print(f"Кэш информация: {fibonacci.cache_info()}")

print(expensive_calculation(2, 3))  # Вычисление
print(expensive_calculation(2, 3))  # Кэш попадание
```

### Декоратор авторизации
```python
def require_auth(required_role=None):
    """Декоратор для проверки авторизации"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем текущего пользователя (имитация)
            current_user = getattr(wrapper, 'current_user', None)
            
            if not current_user:
                raise PermissionError("Требуется авторизация")
            
            if required_role and current_user.get('role') != required_role:
                raise PermissionError(f"Требуется роль: {required_role}")
            
            print(f"Доступ разрешен для {current_user['name']}")
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

# Функции с разными уровнями доступа
@require_auth()
def view_profile():
    return "Профиль пользователя"

@require_auth(required_role="admin")
def delete_user():
    return "Пользователь удален"

@require_auth(required_role="moderator")
def moderate_content():
    return "Контент модерирован"

# Имитация системы авторизации
def set_current_user(user):
    """Установка текущего пользователя для всех защищенных функций"""
    for func in [view_profile, delete_user, moderate_content]:
        func.current_user = user

# Тестирование
try:
    view_profile()  # Ошибка - не авторизован
except PermissionError as e:
    print(f"Ошибка: {e}")

# Авторизация как обычный пользователь
set_current_user({"name": "Анна", "role": "user"})
print(view_profile())  # Успех

try:
    delete_user()  # Ошибка - недостаточно прав
except PermissionError as e:
    print(f"Ошибка: {e}")

# Авторизация как админ
set_current_user({"name": "Админ", "role": "admin"})
print(delete_user())  # Успех
```

## Встроенные декораторы

### @property
```python
class Circle:
    """Класс окружности с использованием property"""
    
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Получение радиуса"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Установка радиуса с валидацией"""
        if value <= 0:
            raise ValueError("Радиус должен быть положительным")
        self._radius = value
    
    @property
    def area(self):
        """Вычисляемое свойство - площадь"""
        import math
        return math.pi * self._radius ** 2
    
    @property
    def circumference(self):
        """Вычисляемое свойство - длина окружности"""
        import math
        return 2 * math.pi * self._radius

# Использование
circle = Circle(5)
print(f"Радиус: {circle.radius}")
print(f"Площадь: {circle.area:.2f}")
print(f"Длина: {circle.circumference:.2f}")

# Изменение радиуса
circle.radius = 10
print(f"Новая площадь: {circle.area:.2f}")

# Валидация
try:
    circle.radius = -5  # Ошибка
except ValueError as e:
    print(f"Ошибка: {e}")
```

### @staticmethod и @classmethod
```python
class MathUtils:
    """Утилиты для математических операций"""
    
    # Константа класса
    PI = 3.141592653589793
    
    @staticmethod
    def add(a, b):
        """Статический метод - не имеет доступа к self или cls"""
        return a + b
    
    @staticmethod
    def is_prime(n):
        """Проверка простого числа"""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    @classmethod
    def circle_area(cls, radius):
        """Метод класса - имеет доступ к cls"""
        return cls.PI * radius ** 2
    
    @classmethod
    def from_string(cls, math_expression):
        """Альтернативный конструктор"""
        # Простой парсер для демонстрации
        if "+" in math_expression:
            a, b = map(float, math_expression.split("+"))
            return cls.add(a, b)
        return None

# Использование
# Статические методы можно вызывать без создания объекта
print(MathUtils.add(5, 3))  # 8
print(MathUtils.is_prime(17))  # True

# Методы класса также можно вызывать без объекта
print(MathUtils.circle_area(5))  # 78.54

# Альтернативный конструктор
result = MathUtils.from_string("10.5 + 5.5")
print(result)  # 16.0
```

### @functools.lru_cache
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci_cached(n):
    """Оптимизированные числа Фибоначчи с встроенным кэшем"""
    if n <= 1:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

@lru_cache(maxsize=None)  # Безлимитный кэш
def factorial_cached(n):
    """Факториал с кэшированием"""
    if n <= 1:
        return 1
    return n * factorial_cached(n-1)

# Тестирование производительности
import time

def measure_performance(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start

# Без кэша (обычная рекурсия)
def fibonacci_normal(n):
    if n <= 1:
        return n
    return fibonacci_normal(n-1) + fibonacci_normal(n-2)

# Сравнение
n = 35
result1, time1 = measure_performance(fibonacci_normal, n)
result2, time2 = measure_performance(fibonacci_cached, n)

print(f"Без кэша: {result1} за {time1:.4f}с")
print(f"С кэшем: {result2} за {time2:.6f}с")
print(f"Ускорение: {time1/time2:.0f}x")

# Информация о кэше
print(f"Статистика кэша: {fibonacci_cached.cache_info()}")
```

## Декораторы классов

### Декоратор для класса
```python
def add_string_representation(cls):
    """Декоратор, добавляющий строковое представление к классу"""
    def __str__(self):
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                attrs.append(f"{key}={value}")
        return f"{cls.__name__}({', '.join(attrs)})"
    
    cls.__str__ = __str__
    return cls

def add_equality(cls):
    """Декоратор, добавляющий сравнение объектов"""
    def __eq__(self, other):
        if not isinstance(other, cls):
            return False
        return self.__dict__ == other.__dict__
    
    cls.__eq__ = __eq__
    return cls

@add_string_representation
@add_equality
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

@add_string_representation
@add_equality
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Использование
person1 = Person("Анна", 25)
person2 = Person("Анна", 25)
person3 = Person("Петр", 30)

print(person1)  # Person(name=Анна, age=25)
print(person1 == person2)  # True
print(person1 == person3)  # False

product = Product("Laptop", 50000)
print(product)  # Product(name=Laptop, price=50000)
```

### Декоратор dataclass (введение)
```python
# Современный способ создания классов данных
from dataclasses import dataclass, field
from typing import List

@dataclass
class Student:
    """Студент с автоматически генерируемыми методами"""
    name: str
    age: int
    grades: List[float] = field(default_factory=list)
    active: bool = True
    
    def add_grade(self, grade: float):
        """Добавление оценки"""
        self.grades.append(grade)
    
    @property
    def average_grade(self) -> float:
        """Средняя оценка"""
        return sum(self.grades) / len(self.grades) if self.grades else 0.0

# Использование
student1 = Student("Анна", 20)
student2 = Student("Анна", 20)

print(student1)  # Student(name='Анна', age=20, grades=[], active=True)
print(student1 == student2)  # True (автоматическое сравнение)

student1.add_grade(4.5)
student1.add_grade(5.0)
print(f"Средняя оценка: {student1.average_grade}")  # 4.75
```

## Множественные декораторы

### Порядок применения декораторов
```python
def decorator_a(func):
    print("Применяется декоратор A")
    def wrapper(*args, **kwargs):
        print("A: до выполнения")
        result = func(*args, **kwargs)
        print("A: после выполнения")
        return result
    return wrapper

def decorator_b(func):
    print("Применяется декоратор B")
    def wrapper(*args, **kwargs):
        print("B: до выполнения")
        result = func(*args, **kwargs)
        print("B: после выполнения")
        return result
    return wrapper

def decorator_c(func):
    print("Применяется декоратор C")
    def wrapper(*args, **kwargs):
        print("C: до выполнения")
        result = func(*args, **kwargs)
        print("C: после выполнения")
        return result
    return wrapper

# Порядок применения: снизу вверх
@decorator_a
@decorator_b
@decorator_c
def my_function():
    print("Выполняется основная функция")

# Вызов функции покажет порядок выполнения
print("--- Вызов функции ---")
my_function()

# Вывод показывает:
# Применяется декоратор C
# Применяется декоратор B  
# Применяется декоратор A
# --- Вызов функции ---
# A: до выполнения
# B: до выполнения
# C: до выполнения
# Выполняется основная функция
# C: после выполнения
# B: после выполнения
# A: после выполнения
```

### Комбинирование полезных декораторов
```python
@measure_time
@log_calls
@retry(max_attempts=2)
@cache(max_size=50)
def complex_calculation(n):
    """Сложное вычисление с множественными декораторами"""
    import random
    
    # Иногда "падает" для демонстрации retry
    if random.random() < 0.3:
        raise Exception("Случайная ошибка вычисления")
    
    # Медленное вычисление
    time.sleep(0.1)
    result = sum(i**2 for i in range(n))
    return result

# Тестирование
try:
    result1 = complex_calculation(100)  # Возможны повторы, логирование, измерение времени
    result2 = complex_calculation(100)  # Кэш попадание
    result3 = complex_calculation(200)  # Новое вычисление
except Exception as e:
    print(f"Окончательная ошибка: {e}")
```

## Практические применения

### Декоратор для API
```python
def api_endpoint(method="GET", path=None):
    """Декоратор для создания API endpoints"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Имитация HTTP запроса
            print(f"API {method} {path or func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                return {
                    "status": "success",
                    "data": result,
                    "code": 200
                }
            except ValueError as e:
                return {
                    "status": "error", 
                    "message": str(e),
                    "code": 400
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": "Внутренняя ошибка сервера",
                    "code": 500
                }
        
        # Добавляем метаданные для роутинга
        wrapper.method = method
        wrapper.path = path or func.__name__
        
        return wrapper
    return decorator

# Использование
@api_endpoint("GET", "/users")
def get_users():
    """Получение списка пользователей"""
    return [
        {"id": 1, "name": "Анна"},
        {"id": 2, "name": "Петр"}
    ]

@api_endpoint("POST", "/users")
def create_user(name, email):
    """Создание пользователя"""
    if not name or not email:
        raise ValueError("Имя и email обязательны")
    
    return {"id": 3, "name": name, "email": email}

# Тестирование API
response1 = get_users()
print(response1)

response2 = create_user("Мария", "maria@example.com")
print(response2)

response3 = create_user("", "")  # Ошибка валидации
print(response3)
```

### Декоратор для тестирования
```python
def test_case(description):
    """Декоратор для создания тестовых случаев"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"\n🧪 Тест: {description}")
            
            try:
                result = func(*args, **kwargs)
                print(f"✅ ПРОЙДЕН: {description}")
                return result
            except AssertionError as e:
                print(f"❌ ПРОВАЛЕН: {description}")
                print(f"   Ошибка: {e}")
                return False
            except Exception as e:
                print(f"💥 ОШИБКА: {description}")
                print(f"   Исключение: {e}")
                return False
        
        return wrapper
    return decorator

def assert_equal(actual, expected, message=""):
    """Простая функция утверждения"""
    if actual != expected:
        raise AssertionError(f"Ожидалось {expected}, получено {actual}. {message}")

# Создание тестов
@test_case("Проверка сложения")
def test_addition():
    result = 2 + 2
    assert_equal(result, 4, "Базовое сложение")

@test_case("Проверка деления на ноль")
def test_division_by_zero():
    try:
        result = 10 / 0
        assert False, "Ожидалось исключение"
    except ZeroDivisionError:
        pass  # Ожидаемое поведение

@test_case("Проверка работы со строками")
def test_string_operations():
    text = "Python"
    assert_equal(text.upper(), "PYTHON", "Преобразование в верхний регистр")
    assert_equal(len(text), 6, "Длина строки")

# Запуск тестов
def run_tests(*test_functions):
    """Запуск всех тестов"""
    results = []
    for test_func in test_functions:
        result = test_func()
        results.append(result)
    
    passed = sum(1 for r in results if r is not False)
    total = len(results)
    print(f"\n📊 Результаты: {passed}/{total} тестов пройдено")

# Выполнение всех тестов
run_tests(test_addition, test_division_by_zero, test_string_operations)
```

### Декоратор для профилирования
```python
import functools
import time
import tracemalloc
from collections import defaultdict

class Profiler:
    """Профилировщик для отслеживания производительности"""
    
    def __init__(self):
        self.stats = defaultdict(list)
    
    def profile(self, func):
        """Декоратор профилирования"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Начало отслеживания памяти
            tracemalloc.start()
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # Измерения
                end_time = time.time()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                # Сохранение статистики
                self.stats[func.__name__].append({
                    "time": end_time - start_time,
                    "memory_current": current,
                    "memory_peak": peak,
                    "args_count": len(args) + len(kwargs)
                })
                
                return result
                
            except Exception as e:
                tracemalloc.stop()
                raise
        
        return wrapper
    
    def get_stats(self, func_name=None):
        """Получение статистики"""
        if func_name:
            return self.stats.get(func_name, [])
        return dict(self.stats)
    
    def print_summary(self):
        """Вывод сводки профилирования"""
        print("\n📈 Профилирование функций:")
        print("-" * 60)
        
        for func_name, calls in self.stats.items():
            if not calls:
                continue
                
            avg_time = sum(call["time"] for call in calls) / len(calls)
            max_memory = max(call["memory_peak"] for call in calls)
            call_count = len(calls)
            
            print(f"Функция: {func_name}")
            print(f"  Вызовов: {call_count}")
            print(f"  Среднее время: {avg_time:.4f}с")
            print(f"  Пик памяти: {max_memory / 1024:.1f} KB")
            print()

# Создание глобального профилировщика
profiler = Profiler()

@profiler.profile
def memory_intensive_task(size):
    """Задача, потребляющая память"""
    big_list = [i ** 2 for i in range(size)]
    return sum(big_list)

@profiler.profile
def cpu_intensive_task(n):
    """CPU-интенсивная задача"""
    result = 0
    for i in range(n):
        result += i ** 0.5
    return result

# Тестирование
for i in range(3):
    memory_intensive_task(10000)
    cpu_intensive_task(100000)

# Вывод статистики
profiler.print_summary()
```

## Сохранение метаданных функции

### Проблема с метаданными
```python
def simple_decorator(func):
    """Декоратор без сохранения метаданных"""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@simple_decorator
def documented_function(x, y):
    """Эта функция складывает два числа"""
    return x + y

# Метаданные потеряны
print(f"Имя: {documented_function.__name__}")  # wrapper
print(f"Документация: {documented_function.__doc__}")  # None
```

### Правильное сохранение метаданных
```python
import functools

def proper_decorator(func):
    """Декоратор с сохранением метаданных"""
    @functools.wraps(func)  # Ключевая строка!
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@proper_decorator
def documented_function_v2(x, y):
    """Эта функция складывает два числа"""
    return x + y

# Метаданные сохранены
print(f"Имя: {documented_function_v2.__name__}")  # documented_function_v2
print(f"Документация: {documented_function_v2.__doc__}")  # Эта функция складывает два числа
print(f"Модуль: {documented_function_v2.__module__}")  # __main__

# Проверка сигнатуры
import inspect
signature = inspect.signature(documented_function_v2)
print(f"Сигнатура: {signature}")  # (x, y)
```

## Частые ошибки с декораторами

### 1. Забывание functools.wraps
```python
# ПЛОХО - теряем метаданные
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# ХОРОШО - сохраняем метаданные
def good_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 2. Неправильная работа с аргументами декоратора
```python
# ОШИБКА - декоратор с опциональными параметрами
def bad_optional_decorator(func=None, *, param=None):
    # Проблема: неясно, вызван ли декоратор с параметрами или без
    pass

# ПРАВИЛЬНО - явное разделение
def good_optional_decorator(param=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Используем param
            return func(*args, **kwargs)
        return wrapper
    
    if callable(param):  # Вызван без скобок @decorator
        func = param
        param = None
        return decorator(func)
    else:  # Вызван со скобками @decorator(param=value)
        return decorator
```

### 3. Проблемы с состоянием в декораторах
```python
# ОШИБКА - разделяемое состояние между экземплярами
def bad_counter_decorator(func):
    count = 0  # Разделяется между всеми функциями!
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"Вызов #{count}")
        return func(*args, **kwargs)
    return wrapper

# ПРАВИЛЬНО - каждая функция имеет свой счетчик
def good_counter_decorator(func):
    count = 0  # Уникальный для каждой декорируемой функции
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"{func.__name__} вызов #{count}")
        return func(*args, **kwargs)
    
    wrapper.call_count = lambda: count  # Доступ к счетчику
    return wrapper

@good_counter_decorator
def func_a():
    pass

@good_counter_decorator  
def func_b():
    pass

func_a()  # func_a вызов #1
func_a()  # func_a вызов #2
func_b()  # func_b вызов #1
print(f"func_a вызвана {func_a.call_count()} раз")  # 2
```

## Ключевые моменты для экзамена

- **Замыкания** - функции, "помнящие" переменные из внешней области видимости
- **nonlocal** - ключевое слово для изменения переменных из внешней области
- **Декораторы** - функции, которые принимают и возвращают другие функции
- **@functools.wraps** - обязательно использовать для сохранения метаданных
- **Декораторы с параметрами** - возвращают декоратор, который возвращает wrapper
- **Встроенные декораторы** - @property, @staticmethod, @classmethod, @lru_cache
- **Множественные декораторы** - применяются снизу вверх
- **Практическое применение** - логирование, кэширование, авторизация, измерение времени
- ***args, **kwargs** - для передачи произвольных аргументов в wrapper
- **Порядок выполнения** - decorator(func) эквивалентно @decorator перед функцией