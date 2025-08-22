# Генераторы. Генератор списка, словаря

## Что такое генераторы

### Определение
Генератор - это объект, который создает значения по требованию (lazy evaluation), не создавая все значения сразу в памяти. Это позволяет эффективно работать с большими объемами данных.

### Обычный список vs генератор
```python
# Обычный список - все значения в памяти сразу
normal_list = [x**2 for x in range(1000000)]  # Занимает много памяти

# Генератор - значения создаются по одному
generator = (x**2 for x in range(1000000))    # Занимает минимум памяти

# Сравнение размера
import sys
print(f"Размер списка: {sys.getsizeof(normal_list)} байт")      # ~8+ MB
print(f"Размер генератора: {sys.getsizeof(generator)} байт")    # ~112 байт
```

## Генераторные выражения

### Синтаксис
```python
# Генератор вместо списка
squares_list = [x**2 for x in range(10)]        # Список
squares_gen = (x**2 for x in range(10))         # Генератор

# Использование генератора
for square in squares_gen:
    print(square)  # 0, 1, 4, 9, 16, 25, 36, 49, 64, 81

# Генератор "истощается" после использования
squares_gen = (x**2 for x in range(5))
list1 = list(squares_gen)  # [0, 1, 4, 9, 16]
list2 = list(squares_gen)  # [] - пустой, генератор исчерпан
```

### Генераторы с условиями
```python
# Четные квадраты
even_squares = (x**2 for x in range(20) if x % 2 == 0)
print(list(even_squares))  # [0, 4, 16, 36, 64, 100, 144, 196, 256, 324]

# Обработка текста
text = "Python это отличный язык программирования"
words = text.split()
long_words = (word.upper() for word in words if len(word) > 4)
print(list(long_words))  # ['PYTHON', 'ОТЛИЧНЫЙ', 'ПРОГРАММИРОВАНИЯ']

# Фильтрация и преобразование
numbers = [1, -2, 3, -4, 5, -6]
positive_doubles = (x * 2 for x in numbers if x > 0)
print(list(positive_doubles))  # [2, 6, 10]
```

## Функции-генераторы

### Ключевое слово yield
```python
def count_up_to(max_count):
    """Генератор чисел от 1 до max_count"""
    count = 1
    while count <= max_count:
        yield count  # Возвращает значение и "замораживает" функцию
        count += 1

# Использование
counter = count_up_to(5)
for num in counter:
    print(num)  # 1, 2, 3, 4, 5

# Ручное получение значений
counter = count_up_to(3)
print(next(counter))  # 1
print(next(counter))  # 2
print(next(counter))  # 3
# print(next(counter))  # StopIteration ошибка
```

### Генераторы для чтения файлов
```python
def read_lines(filename):
    """Генератор для чтения файла по строкам"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        print(f"Файл {filename} не найден")

# Эффективно для больших файлов
def process_large_file(filename):
    line_count = 0
    for line in read_lines(filename):
        if line:  # Пропускаем пустые строки
            line_count += 1
            # Обрабатываем строку без загрузки всего файла в память
    return line_count
```

### Генераторы бесконечных последовательностей
```python
def fibonacci():
    """Бесконечная последовательность Фибоначчи"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def primes():
    """Генератор простых чисел"""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1

# Использование бесконечных генераторов
fib = fibonacci()
first_10_fib = [next(fib) for _ in range(10)]
print(first_10_fib)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

prime_gen = primes()
first_5_primes = [next(prime_gen) for _ in range(5)]
print(first_5_primes)  # [2, 3, 5, 7, 11]
```

## Списковые включения (List Comprehensions)

### Базовый синтаксис
```python
# Простое преобразование
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]  # [1, 4, 9, 16, 25]

# С условием
evens = [x for x in range(20) if x % 2 == 0]  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Преобразование с условием
positive_squares = [x**2 for x in range(-5, 6) if x > 0]  # [1, 4, 9, 16, 25]
```

### Сложные списковые включения
```python
# Обработка строк
words = ["hello", "world", "python", "programming"]
capitalized = [word.capitalize() for word in words if len(word) > 4]
# ['World', 'Python', 'Programming']

# Обработка вложенных структур
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for row in matrix for item in row]  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Создание пар
colors = ["красный", "зеленый", "синий"]
sizes = ["S", "M", "L"]
combinations = [(color, size) for color in colors for size in sizes]
# [('красный', 'S'), ('красный', 'M'), ('красный', 'L'), ...]
```

### Условные выражения в списковых включениях
```python
# Тернарный оператор в включении
numbers = [1, 2, 3, 4, 5, 6]
categories = ["четное" if x % 2 == 0 else "нечетное" for x in numbers]
# ['нечетное', 'четное', 'нечетное', 'четное', 'нечетное', 'четное']

# Множественные условия
grades = [95, 87, 92, 76, 89, 94]
performance = [
    "отлично" if grade >= 90 
    else "хорошо" if grade >= 80 
    else "удовлетворительно" if grade >= 70 
    else "неудовлетворительно"
    for grade in grades
]
```

## Словарные включения (Dict Comprehensions)

### Базовые словарные включения
```python
# Создание словаря из списка
numbers = [1, 2, 3, 4, 5]
squares_dict = {x: x**2 for x in numbers}  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Инвертирование словаря
original = {"a": 1, "b": 2, "c": 3}
inverted = {value: key for key, value in original.items()}  # {1: 'a', 2: 'b', 3: 'c'}

# С условием
words = ["apple", "banana", "cherry", "date"]
word_lengths = {word: len(word) for word in words if len(word) > 4}
# {'apple': 5, 'banana': 6, 'cherry': 6}
```

### Обработка данных
```python
# Группировка по длине
words = ["cat", "dog", "elephant", "ant", "bird", "butterfly"]
by_length = {}
for word in words:
    length = len(word)
    if length not in by_length:
        by_length[length] = []
    by_length[length].append(word)

# То же самое через словарное включение + setdefault
by_length_v2 = {}
for word in words:
    by_length_v2.setdefault(len(word), []).append(word)

# Статистика по символам
text = "python programming"
char_count = {char: text.count(char) for char in set(text) if char != " "}
print(char_count)  # {'p': 2, 'y': 1, 't': 2, 'h': 1, 'o': 3, 'n': 4, ...}
```

## Множественные включения (Set Comprehensions)

### Создание множеств
```python
# Уникальные квадраты
numbers = [1, 2, 2, 3, 3, 4, 5]
unique_squares = {x**2 for x in numbers}  # {1, 4, 9, 16, 25}

# Уникальные символы
text = "programming"
unique_chars = {char.upper() for char in text if char.isalpha()}
print(unique_chars)  # {'P', 'R', 'O', 'G', 'A', 'M', 'I', 'N'}

# Обработка данных
emails = ["anna@gmail.com", "peter@yandex.ru", "maria@gmail.com"]
domains = {email.split("@")[1] for email in emails}
print(domains)  # {'gmail.com', 'yandex.ru'}
```

## Практические применения генераторов

### Обработка больших данных
```python
def process_csv_file(filename):
    """Генератор для обработки CSV файла по строкам"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            header = file.readline().strip().split(',')
            
            for line in file:
                values = line.strip().split(',')
                if len(values) == len(header):
                    yield dict(zip(header, values))
    except FileNotFoundError:
        print(f"Файл {filename} не найден")

# Использование (эффективно для больших файлов)
def analyze_sales_data(filename):
    total_sales = 0
    product_count = {}
    
    for record in process_csv_file(filename):
        # Обрабатываем каждую запись без загрузки всего файла
        if "amount" in record:
            total_sales += float(record["amount"])
        
        product = record.get("product", "unknown")
        product_count[product] = product_count.get(product, 0) + 1
    
    return total_sales, product_count
```

### Генераторы для API пагинации
```python
def paginated_data(total_items, page_size=10):
    """Генератор для постраничной обработки данных"""
    for start in range(0, total_items, page_size):
        end = min(start + page_size, total_items)
        yield {
            "page": start // page_size + 1,
            "start": start,
            "end": end,
            "items": list(range(start, end))  # Имитация данных
        }

# Использование
for page_data in paginated_data(25, 7):
    print(f"Страница {page_data['page']}: {page_data['items']}")

# Генератор для веб-скрапинга
def scrape_pages(base_url, max_pages):
    """Генератор для постепенного скрапинга страниц"""
    for page_num in range(1, max_pages + 1):
        url = f"{base_url}?page={page_num}"
        # В реальности здесь был бы HTTP запрос
        yield {
            "page": page_num,
            "url": url,
            "data": f"Данные со страницы {page_num}"
        }
```

### Пайплайны обработки данных
```python
def read_numbers(data):
    """Шаг 1: Извлечение чисел из данных"""
    for item in data:
        if isinstance(item, (int, float)):
            yield item
        elif isinstance(item, str) and item.isdigit():
            yield int(item)

def filter_positive(numbers):
    """Шаг 2: Фильтрация положительных чисел"""
    for num in numbers:
        if num > 0:
            yield num

def square_numbers(numbers):
    """Шаг 3: Возведение в квадрат"""
    for num in numbers:
        yield num ** 2

# Создание пайплайна
raw_data = [1, "2", -3, "4", "abc", 5.5, 0]
pipeline = square_numbers(filter_positive(read_numbers(raw_data)))

result = list(pipeline)
print(result)  # [1, 4, 16, 30.25]

# Альтернативный синтаксис через композицию
def process_pipeline(data):
    return square_numbers(filter_positive(read_numbers(data)))

result = list(process_pipeline(raw_data))
```

## Продвинутые генераторы

### Генераторы с состоянием
```python
def running_average():
    """Генератор скользящего среднего"""
    values = []
    total = 0
    
    while True:
        value = yield total / len(values) if values else 0
        if value is not None:
            values.append(value)
            total += value

# Использование
avg_gen = running_average()
next(avg_gen)  # Запускаем генератор

avg = avg_gen.send(10)  # Отправляем значение
print(f"Среднее: {avg}")  # 10.0

avg = avg_gen.send(20)
print(f"Среднее: {avg}")  # 15.0

avg = avg_gen.send(30)
print(f"Среднее: {avg}")  # 20.0
```

### Генераторы для имитации данных
```python
import random
from datetime import datetime, timedelta

def generate_user_data(count):
    """Генератор тестовых пользователей"""
    first_names = ["Анна", "Петр", "Мария", "Иван", "Ольга"]
    last_names = ["Иванов", "Петров", "Сидоров", "Козлов", "Попов"]
    
    for i in range(count):
        yield {
            "id": i + 1,
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "age": random.randint(18, 65),
            "email": f"user{i+1}@example.com",
            "registration_date": datetime.now() - timedelta(days=random.randint(0, 365))
        }

def generate_sales_data(days):
    """Генератор данных продаж"""
    base_date = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        current_date = base_date + timedelta(days=day)
        daily_sales = random.randint(5, 50)
        
        for sale in range(daily_sales):
            yield {
                "date": current_date.strftime("%Y-%m-%d"),
                "product": f"Product_{random.randint(1, 10)}",
                "amount": round(random.uniform(100, 5000), 2),
                "customer_id": random.randint(1, 1000)
            }

# Анализ данных через генераторы
def analyze_sales(sales_generator):
    total_revenue = 0
    product_sales = {}
    transaction_count = 0
    
    for sale in sales_generator:
        total_revenue += sale["amount"]
        product = sale["product"]
        product_sales[product] = product_sales.get(product, 0) + sale["amount"]
        transaction_count += 1
    
    return {
        "total_revenue": total_revenue,
        "transaction_count": transaction_count,
        "top_products": sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    }

# Использование
sales_gen = generate_sales_data(30)  # 30 дней данных
analysis = analyze_sales(sales_gen)
print(f"Общая выручка: {analysis['total_revenue']:.2f}")
print(f"Количество транзакций: {analysis['transaction_count']}")
```

## Методы генераторов

### send(), throw(), close()
```python
def echo_generator():
    """Генератор-эхо с обработкой отправленных значений"""
    try:
        value = None
        while True:
            received = yield f"Получено: {value}"
            value = received
    except GeneratorExit:
        print("Генератор закрывается")
    except Exception as e:
        print(f"Ошибка в генераторе: {e}")
        yield "Ошибка обработана"

# Использование
gen = echo_generator()
print(next(gen))           # Получено: None
print(gen.send("Привет"))  # Получено: Привет
print(gen.send(123))       # Получено: 123

# Закрытие генератора
gen.close()
```

### Генераторы с исключениями
```python
def robust_data_processor(data):
    """Устойчивый к ошибкам генератор обработки данных"""
    for item in data:
        try:
            if isinstance(item, str):
                yield item.upper()
            elif isinstance(item, (int, float)):
                yield item * 2
            else:
                yield f"Неизвестный тип: {type(item).__name__}"
        except Exception as e:
            yield f"Ошибка обработки {item}: {e}"

# Тестирование
mixed_data = ["hello", 42, 3.14, None, [1, 2, 3], "world"]
processed = list(robust_data_processor(mixed_data))
print(processed)
```

## Производительность и оптимизация

### Сравнение производительности
```python
import time
import sys

def measure_time_and_memory():
    # Списковое включение
    start_time = time.time()
    squares_list = [x**2 for x in range(1000000)]
    list_time = time.time() - start_time
    list_memory = sys.getsizeof(squares_list)
    
    # Генераторное выражение
    start_time = time.time()
    squares_gen = (x**2 for x in range(1000000))
    gen_time = time.time() - start_time
    gen_memory = sys.getsizeof(squares_gen)
    
    print(f"Список: {list_time:.4f}с, {list_memory:,} байт")
    print(f"Генератор: {gen_time:.6f}с, {gen_memory} байт")
    
    # Потребление генератора
    start_time = time.time()
    consumed = sum(squares_gen)
    consumption_time = time.time() - start_time
    print(f"Потребление генератора: {consumption_time:.4f}с")

measure_time_and_memory()
```

### Ленивые вычисления
```python
def expensive_operation(x):
    """Имитация дорогой операции"""
    time.sleep(0.01)  # Имитация задержки
    return x ** 3

def lazy_processing(data):
    """Ленивая обработка - вычисления по требованию"""
    for item in data:
        yield expensive_operation(item)

def eager_processing(data):
    """Жадная обработка - все вычисления сразу"""
    return [expensive_operation(item) for item in data]

# Сравнение
data = range(100)

# Ленивая обработка - начинается мгновенно
start = time.time()
lazy_gen = lazy_processing(data)
print(f"Ленивая инициализация: {time.time() - start:.4f}с")

# Получение первых 5 результатов
first_5 = [next(lazy_gen) for _ in range(5)]
print(f"Первые 5 результатов получены")

# Жадная обработка - ждем все вычисления
start = time.time()
eager_result = eager_processing(range(10))  # Меньше данных для демонстрации
print(f"Жадная обработка: {time.time() - start:.4f}с")
```

## Практические задачи

### Обработка лог-файлов
```python
def parse_log_entries(log_data):
    """Генератор для парсинга записей лога"""
    for line in log_data:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        # Простой формат: timestamp level message
        parts = line.split(" ", 2)
        if len(parts) >= 3:
            yield {
                "timestamp": parts[0],
                "level": parts[1],
                "message": parts[2]
            }

def filter_log_level(log_entries, level):
    """Фильтрация записей по уровню"""
    for entry in log_entries:
        if entry["level"] == level:
            yield entry

# Использование
log_data = [
    "2024-12-31T10:00:00 INFO Система запущена",
    "2024-12-31T10:05:00 WARNING Низкая память",
    "2024-12-31T10:10:00 ERROR Ошибка подключения",
    "2024-12-31T10:15:00 INFO Подключение восстановлено"
]

# Цепочка генераторов
parsed = parse_log_entries(log_data)
errors = filter_log_level(parsed, "ERROR")
error_list = list(errors)
print(error_list)
```

### Генератор комбинаций
```python
def generate_combinations(items, r):
    """Генератор сочетаний без повторений"""
    from itertools import combinations
    for combo in combinations(items, r):
        yield combo

def password_variations(base_word):
    """Генератор вариаций пароля"""
    # Замены символов
    replacements = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$"}
    
    # Исходный вариант
    yield base_word
    
    # С заглавными буквами
    yield base_word.capitalize()
    yield base_word.upper()
    
    # С заменами символов
    for char, replacement in replacements.items():
        if char in base_word.lower():
            yield base_word.replace(char, replacement)
    
    # С добавлением цифр
    for num in range(10):
        yield f"{base_word}{num}"
        yield f"{num}{base_word}"

# Генерация вариантов
base = "password"
variations = list(password_variations(base))
print(f"Сгенерировано {len(variations)} вариантов")
print(variations[:10])  # Первые 10
```

## Встроенные генераторы и итераторы

### itertools модуль
```python
import itertools

# count() - бесконечный счетчик
counter = itertools.count(start=1, step=2)  # 1, 3, 5, 7, 9, ...
first_5_odds = [next(counter) for _ in range(5)]
print(first_5_odds)  # [1, 3, 5, 7, 9]

# cycle() - бесконечное повторение
colors = itertools.cycle(["красный", "зеленый", "синий"])
first_7_colors = [next(colors) for _ in range(7)]
print(first_7_colors)  # ['красный', 'зеленый', 'синий', 'красный', ...]

# chain() - объединение итераторов
list1 = [1, 2, 3]
list2 = [4, 5, 6]
chained = itertools.chain(list1, list2)
print(list(chained))  # [1, 2, 3, 4, 5, 6]

# groupby() - группировка
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# A: [('A', 1), ('A', 2)]
# B: [('B', 3), ('B', 4)]
# A: [('A', 5)]
```

### Комбинаторика
```python
# permutations() - размещения
from itertools import permutations, combinations, combinations_with_replacement

items = ["A", "B", "C"]

# Размещения (порядок важен)
perms = list(permutations(items, 2))
print(perms)  # [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

# Сочетания (порядок не важен)
combs = list(combinations(items, 2))
print(combs)  # [('A', 'B'), ('A', 'C'), ('B', 'C')]

# Сочетания с повторениями
combs_rep = list(combinations_with_replacement(items, 2))
print(combs_rep)  # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
```

## Создание собственных итераторов

### Класс-итератор
```python
class CountDown:
    """Итератор обратного отсчета"""
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

# Использование
countdown = CountDown(5)
for num in countdown:
    print(num)  # 5, 4, 3, 2, 1

# Альтернатива через генератор (проще)
def countdown_generator(start):
    while start > 0:
        yield start
        start -= 1

for num in countdown_generator(5):
    print(num)  # 5, 4, 3, 2, 1
```

### Итератор для файлов
```python
class FileLineIterator:
    """Итератор для чтения файла по строкам с фильтрацией"""
    def __init__(self, filename, filter_func=None):
        self.filename = filename
        self.filter_func = filter_func or (lambda x: True)
        self.file = None
    
    def __iter__(self):
        self.file = open(self.filename, 'r', encoding='utf-8')
        return self
    
    def __next__(self):
        while True:
            line = self.file.readline()
            if not line:  # Конец файла
                self.file.close()
                raise StopIteration
            
            line = line.strip()
            if self.filter_func(line):
                return line
    
    def __del__(self):
        if self.file and not self.file.closed:
            self.file.close()

# Использование
# iterator = FileLineIterator("data.txt", lambda line: line and not line.startswith("#"))
# for line in iterator:
#     print(line)
```

## Ключевые моменты для экзамена

- **Генераторы** - создают значения по требованию, экономят память
- **Генераторное выражение** - `(x for x in data)` вместо `[x for x in data]`
- **yield** - ключевое слово для создания функций-генераторов
- **Списковые включения** - `[выражение for элемент in итератор if условие]`
- **Словарные включения** - `{ключ: значение for элемент in итератор}`
- **Множественные включения** - `{выражение for элемент in итератор}`
- **Ленивые вычисления** - генераторы вычисляют только по требованию
- **Одноразовость** - генераторы "истощаются" после полного прохода
- **itertools** - модуль с полезными генераторами и итераторами
- **Производительность** - генераторы эффективнее для больших данных