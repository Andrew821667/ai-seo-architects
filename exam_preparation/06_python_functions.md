# Функции в Python. Встроенные и пользовательские

## Определение функций

### Базовый синтаксис
```python
def function_name(parameters):
    """Документация функции (docstring)"""
    # тело функции
    return result

# Простая функция
def greet():
    print("Привет!")

# Функция с параметром
def greet_person(name):
    print(f"Привет, {name}!")

# Функция с возвращаемым значением
def add_numbers(a, b):
    return a + b

# Вызов функций
greet()                    # Привет!
greet_person("Анна")       # Привет, Анна!
result = add_numbers(5, 3) # 8
```

### Параметры функций

#### Обязательные параметры
```python
def divide(a, b):
    return a / b

result = divide(10, 2)  # 5.0
# divide(10)  # Ошибка! Не хватает параметра
```

#### Параметры по умолчанию
```python
def greet(name, greeting="Привет"):
    return f"{greeting}, {name}!"

print(greet("Анна"))                    # Привет, Анна!
print(greet("Петр", "Добро пожаловать")) # Добро пожаловать, Петр!

# ОСТОРОЖНО с изменяемыми значениями по умолчанию
def add_item(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list
```

#### Именованные аргументы
```python
def create_user(name, age, city="Москва", active=True):
    return {
        "name": name,
        "age": age, 
        "city": city,
        "active": active
    }

# Позиционные аргументы
user1 = create_user("Анна", 25)

# Именованные аргументы
user2 = create_user(name="Петр", age=30, city="СПб")

# Смешанные (позиционные должны быть первыми)
user3 = create_user("Мария", age=28, active=False)
```

#### *args и **kwargs
```python
# *args - произвольное количество позиционных аргументов
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3))        # 6
print(sum_all(1, 2, 3, 4, 5))  # 15

# **kwargs - произвольное количество именованных аргументов
def create_config(**settings):
    config = {"default": True}
    config.update(settings)
    return config

config = create_config(debug=True, port=8080, host="localhost")
print(config)  # {'default': True, 'debug': True, 'port': 8080, 'host': 'localhost'}

# Комбинирование
def flexible_function(required_arg, *args, **kwargs):
    print(f"Обязательный: {required_arg}")
    print(f"Дополнительные: {args}")
    print(f"Именованные: {kwargs}")

flexible_function("test", 1, 2, 3, name="Анна", age=25)
```

## Встроенные функции

### Функции для работы с числами
```python
# Математические функции
print(abs(-5))        # 5 (абсолютное значение)
print(round(3.14159, 2))  # 3.14 (округление)
print(pow(2, 3))      # 8 (возведение в степень)
print(divmod(17, 5))  # (3, 2) (частное и остаток)

# Агрегатные функции
numbers = [1, 5, 3, 9, 2]
print(max(numbers))   # 9
print(min(numbers))   # 1
print(sum(numbers))   # 20
print(len(numbers))   # 5

# Статистические функции (нужен import statistics)
import statistics
print(statistics.mean(numbers))    # 4.0 (среднее)
print(statistics.median(numbers))  # 3 (медиана)
```

### Функции для работы с последовательностями
```python
# range() - генерация последовательностей
for i in range(5):          # 0, 1, 2, 3, 4
    print(i)

numbers = list(range(2, 10, 2))  # [2, 4, 6, 8]

# enumerate() - получение индекса и значения
fruits = ["яблоко", "банан", "апельсин"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# zip() - объединение последовательностей
names = ["Анна", "Петр", "Мария"]
ages = [25, 30, 28]
for name, age in zip(names, ages):
    print(f"{name}: {age} лет")

# Создание словаря через zip
person_dict = dict(zip(names, ages))
# {'Анна': 25, 'Петр': 30, 'Мария': 28}
```

### Функции фильтрации и преобразования
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# filter() - фильтрация
def is_even(x):
    return x % 2 == 0

evens = list(filter(is_even, numbers))  # [2, 4, 6, 8, 10]

# map() - преобразование
def square(x):
    return x ** 2

squares = list(map(square, numbers))  # [1, 4, 9, 16, 25, ...]

# С lambda функциями
evens = list(filter(lambda x: x % 2 == 0, numbers))
squares = list(map(lambda x: x**2, numbers))

# sorted() - сортировка
students = [("Анна", 85), ("Петр", 92), ("Мария", 78)]
by_grade = sorted(students, key=lambda x: x[1], reverse=True)
# [('Петр', 92), ('Анна', 85), ('Мария', 78)]
```

### Функции типов и проверок
```python
# type() и isinstance()
x = 42
print(type(x))              # <class 'int'>
print(isinstance(x, int))   # True
print(isinstance(x, (int, float)))  # True (любой из типов)

# all() и any()
numbers = [2, 4, 6, 8]
print(all(x % 2 == 0 for x in numbers))  # True (все четные)
print(any(x > 5 for x in numbers))       # True (есть > 5)

# Проверки на пустоту
data = []
if not data:
    print("Список пуст")

# hasattr() - проверка атрибута
class Person:
    def __init__(self, name):
        self.name = name

person = Person("Анна")
print(hasattr(person, "name"))  # True
print(hasattr(person, "age"))   # False
```

## Область видимости переменных

### Локальные и глобальные переменные
```python
global_var = "Я глобальная"

def test_scope():
    local_var = "Я локальная"
    print(f"Внутри функции: {global_var}")  # Доступна
    print(f"Внутри функции: {local_var}")   # Доступна

test_scope()
print(f"Снаружи: {global_var}")  # Доступна
# print(local_var)  # Ошибка! Локальная переменная недоступна

# Изменение глобальной переменной
counter = 0

def increment():
    global counter
    counter += 1

increment()
print(counter)  # 1
```

### Замыкания (Closures)
```python
def outer_function(x):
    def inner_function(y):
        return x + y  # Обращается к x из внешней функции
    return inner_function

# Создаем замыкание
add_5 = outer_function(5)
result = add_5(3)  # 8

# Практический пример - создание конфигураторов
def create_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

### Nonlocal переменные
```python
def outer():
    x = 10
    
    def inner():
        nonlocal x
        x += 1  # Изменяем переменную из внешней функции
        print(f"Внутри inner: x = {x}")
    
    inner()
    print(f"Внутри outer: x = {x}")

outer()
# Внутри inner: x = 11
# Внутри outer: x = 11
```

## Лямбда-функции

### Синтаксис и использование
```python
# Синтаксис: lambda аргументы: выражение
square = lambda x: x**2
print(square(5))  # 25

# Несколько аргументов
add = lambda x, y: x + y
print(add(3, 4))  # 7

# С условиями
abs_value = lambda x: x if x >= 0 else -x
print(abs_value(-5))  # 5
```

### Практическое применение
```python
# Сортировка сложных структур
students = [
    {"name": "Анна", "grade": 85},
    {"name": "Петр", "grade": 92}, 
    {"name": "Мария", "grade": 78}
]

# Сортировка по оценке
by_grade = sorted(students, key=lambda s: s["grade"])

# Сортировка по имени
by_name = sorted(students, key=lambda s: s["name"])

# Фильтрация
high_achievers = list(filter(lambda s: s["grade"] >= 85, students))

# Преобразование
names_upper = list(map(lambda s: s["name"].upper(), students))
```

## Рекурсия

### Базовые примеры
```python
def factorial(n):
    """Вычисление факториала рекурсивно"""
    if n <= 1:  # Базовый случай
        return 1
    else:
        return n * factorial(n - 1)  # Рекурсивный вызов

print(factorial(5))  # 120

def fibonacci(n):
    """Числа Фибоначчи"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(7))  # 13
```

### Рекурсия с аккумулятором (эффективнее)
```python
def factorial_acc(n, acc=1):
    """Факториал с аккумулятором (tail recursion)"""
    if n <= 1:
        return acc
    return factorial_acc(n-1, acc * n)

def fibonacci_efficient(n, a=0, b=1):
    """Эффективный Фибоначчи"""
    if n == 0:
        return a
    return fibonacci_efficient(n-1, b, a + b)
```

### Рекурсия для структур данных
```python
def sum_nested_list(nested_list):
    """Сумма всех чисел во вложенном списке"""
    total = 0
    for item in nested_list:
        if isinstance(item, list):
            total += sum_nested_list(item)  # Рекурсивный вызов
        else:
            total += item
    return total

nested = [1, [2, 3], [4, [5, 6]], 7]
print(sum_nested_list(nested))  # 28
```

## Продвинутые возможности

### Аннотации типов
```python
from typing import List, Dict, Optional, Union

def process_numbers(numbers: List[int]) -> Dict[str, float]:
    """Обработка списка чисел с возвращением статистики"""
    return {
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers),
        "max": max(numbers),
        "min": min(numbers)
    }

def find_user(user_id: int) -> Optional[Dict[str, str]]:
    """Поиск пользователя, может вернуть None"""
    users_db = {1: {"name": "Анна"}, 2: {"name": "Петр"}}
    return users_db.get(user_id)

def format_value(value: Union[int, float, str]) -> str:
    """Форматирование значения разных типов"""
    return str(value)
```

### Функции высшего порядка
```python
def apply_operation(numbers, operation):
    """Применить операцию к каждому числу"""
    return [operation(num) for num in numbers]

def square(x):
    return x ** 2

def cube(x):
    return x ** 3

numbers = [1, 2, 3, 4, 5]
squared = apply_operation(numbers, square)  # [1, 4, 9, 16, 25]
cubed = apply_operation(numbers, cube)      # [1, 8, 27, 64, 125]

# Функция, возвращающая функцию
def create_power_function(power):
    def power_function(x):
        return x ** power
    return power_function

square_func = create_power_function(2)
cube_func = create_power_function(3)

print(square_func(4))  # 16
print(cube_func(4))    # 64
```

### Функции как объекты
```python
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

# Словарь функций
operations = {
    "+": add,
    "*": multiply,
    "/": divide
}

# Использование
result = operations["+"](5, 3)  # 8
result = operations["*"](4, 6)  # 24

# Список функций
math_functions = [add, multiply, divide]
for func in math_functions:
    print(f"{func.__name__}(10, 2) = {func(10, 2)}")
```

## Встроенные функции

### Функции преобразования типов
```python
# Преобразование в числа
x = int("42")        # 42
y = float("3.14")    # 3.14
z = complex("1+2j")  # (1+2j)

# Преобразование в строки
s = str(42)          # "42"
b = bin(10)          # "0b1010" (двоичная)
h = hex(255)         # "0xff" (шестнадцатеричная)
o = oct(8)           # "0o10" (восьмеричная)

# Преобразование в коллекции
l = list("hello")    # ['h', 'e', 'l', 'l', 'o']
t = tuple([1, 2, 3]) # (1, 2, 3)
s = set([1, 2, 2, 3]) # {1, 2, 3}
```

### Функции для работы с итерируемыми объектами
```python
numbers = [1, 2, 3, 4, 5]

# Проверки
print(all([True, True, False]))   # False
print(any([False, False, True]))  # True

# Агрегация
print(sum(numbers))     # 15
print(max(numbers))     # 5
print(min(numbers))     # 1
print(len(numbers))     # 5

# Преобразование в последовательности
print(list(range(5)))           # [0, 1, 2, 3, 4]
print(list(reversed(numbers)))  # [5, 4, 3, 2, 1]
print(list(enumerate(["a", "b", "c"])))  # [(0, 'a'), (1, 'b'), (2, 'c')]
```

### Функции для проверки типов
```python
# Проверки типов
print(isinstance(42, int))        # True
print(isinstance("hello", str))   # True
print(isinstance([1, 2], list))   # True

# Проверки возможностей
print(callable(print))            # True (можно вызвать)
print(callable(42))               # False

print(hasattr("hello", "upper"))  # True
print(hasattr(42, "upper"))       # False

# Информация об объектах
print(id([1, 2, 3]))              # Уникальный идентификатор объекта
print(type(42))                   # <class 'int'>
```

## Функциональное программирование

### map(), filter(), reduce()
```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map() - применение функции к каждому элементу
squares = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]

# filter() - фильтрация элементов
evens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]

# reduce() - свертка последовательности к одному значению
product = reduce(lambda x, y: x * y, numbers)  # 120 (произведение)

# Практический пример
words = ["hello", "world", "python"]
lengths = list(map(len, words))              # [5, 5, 6]
long_words = list(filter(lambda w: len(w) > 4, words))  # ['hello', 'world', 'python']
```

### Partial функции
```python
from functools import partial

def multiply(x, y):
    return x * y

# Создаем частичную функцию
double = partial(multiply, 2)  # Фиксируем x = 2
triple = partial(multiply, 3)  # Фиксируем x = 3

print(double(5))  # 10 (2 * 5)
print(triple(4))  # 12 (3 * 4)

# Практический пример
def log_message(level, message):
    print(f"[{level}] {message}")

# Создаем специализированные логгеры
info = partial(log_message, "INFO")
error = partial(log_message, "ERROR")

info("Система запущена")    # [INFO] Система запущена
error("Ошибка подключения") # [ERROR] Ошибка подключения
```

## Практические примеры

### Валидация данных
```python
def validate_email(email):
    """Простая валидация email"""
    if "@" not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    local, domain = parts
    return len(local) > 0 and len(domain) > 0 and "." in domain

def validate_user_data(user_data):
    """Валидация данных пользователя"""
    errors = []
    
    # Проверка имени
    if "name" not in user_data or len(user_data["name"]) < 2:
        errors.append("Имя должно содержать минимум 2 символа")
    
    # Проверка возраста
    if "age" not in user_data or not isinstance(user_data["age"], int):
        errors.append("Возраст должен быть числом")
    elif user_data["age"] < 0 or user_data["age"] > 150:
        errors.append("Возраст должен быть от 0 до 150")
    
    # Проверка email
    if "email" not in user_data or not validate_email(user_data["email"]):
        errors.append("Некорректный email")
    
    return len(errors) == 0, errors

# Тестирование
user1 = {"name": "Анна", "age": 25, "email": "anna@example.com"}
valid, errors = validate_user_data(user1)
print(f"Валидные данные: {valid}")  # True
```

### Кэширование результатов
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(n):
    """Дорогая вычислительная операция с кэшированием"""
    print(f"Вычисляем для {n}...")  # Покажет что вызывается
    result = 0
    for i in range(n):
        result += i ** 2
    return result

# Первый вызов - выполняется вычисление
print(expensive_calculation(1000))  # Вычисляем для 1000...

# Второй вызов - результат из кэша (быстро)
print(expensive_calculation(1000))  # Результат сразу

# Мануальное кэширование
calculation_cache = {}

def cached_fibonacci(n):
    if n in calculation_cache:
        return calculation_cache[n]
    
    if n <= 1:
        result = n
    else:
        result = cached_fibonacci(n-1) + cached_fibonacci(n-2)
    
    calculation_cache[n] = result
    return result
```

### Обработка ошибок в функциях
```python
def safe_divide(a, b):
    """Безопасное деление с обработкой ошибок"""
    try:
        result = a / b
        return {"success": True, "result": result}
    except ZeroDivisionError:
        return {"success": False, "error": "Деление на ноль"}
    except TypeError:
        return {"success": False, "error": "Некорректные типы данных"}

# Использование
result1 = safe_divide(10, 2)    # {"success": True, "result": 5.0}
result2 = safe_divide(10, 0)    # {"success": False, "error": "Деление на ноль"}

def parse_number(value, default=None):
    """Безопасное преобразование в число"""
    try:
        if isinstance(value, (int, float)):
            return value
        return float(value)
    except (ValueError, TypeError):
        return default

print(parse_number("42"))      # 42.0
print(parse_number("abc", 0))  # 0
```

## Документирование функций

### Docstrings
```python
def calculate_bmi(weight, height):
    """
    Вычисляет индекс массы тела (BMI).
    
    Args:
        weight (float): Вес в килограммах
        height (float): Рост в метрах
        
    Returns:
        float: Значение BMI
        
    Raises:
        ValueError: Если вес или рост <= 0
        
    Example:
        >>> calculate_bmi(70, 1.75)
        22.86
    """
    if weight <= 0 or height <= 0:
        raise ValueError("Вес и рост должны быть положительными")
    
    return weight / (height ** 2)

# Доступ к документации
print(calculate_bmi.__doc__)
help(calculate_bmi)
```

### Аннотации и валидация
```python
from typing import List, Tuple, Optional

def analyze_grades(grades: List[float]) -> Tuple[float, float, str]:
    """
    Анализ оценок студента.
    
    Args:
        grades: Список оценок от 0 до 100
        
    Returns:
        Кортеж (средняя_оценка, максимальная_оценка, буквенная_оценка)
    """
    if not grades:
        return 0.0, 0.0, "F"
    
    avg = sum(grades) / len(grades)
    max_grade = max(grades)
    
    # Определение буквенной оценки
    if avg >= 90:
        letter = "A"
    elif avg >= 80:
        letter = "B"
    elif avg >= 70:
        letter = "C"
    elif avg >= 60:
        letter = "D"
    else:
        letter = "F"
    
    return avg, max_grade, letter

# Использование
grades = [85, 92, 78, 88, 94]
avg, max_val, letter = analyze_grades(grades)
print(f"Средняя: {avg:.1f}, Максимальная: {max_val}, Оценка: {letter}")
```

## Ключевые моменты для экзамена

- **Определение функции** - `def name(params): return result`
- **Параметры** - обязательные, по умолчанию, *args, **kwargs
- **Область видимости** - local, global, nonlocal
- **Встроенные функции** - len(), max(), min(), sum(), map(), filter()
- **Лямбда-функции** - анонимные функции для простых операций
- **Рекурсия** - функция вызывает сама себя, нужен базовый случай
- **Аннотации типов** - улучшают читаемость и помогают в отладке
- **Docstrings** - документация функций в тройных кавычках
- **Функции высшего порядка** - принимают или возвращают другие функции