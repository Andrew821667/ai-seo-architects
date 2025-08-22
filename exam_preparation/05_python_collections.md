# Списки, кортежи, словари

## Списки (Lists)

### Создание списков
```python
# Пустой список
empty_list = []
empty_list = list()

# Список с элементами
numbers = [1, 2, 3, 4, 5]
fruits = ["яблоко", "банан", "апельсин"]
mixed = [1, "hello", 3.14, True]

# Список из range
numbers = list(range(1, 6))  # [1, 2, 3, 4, 5]
```

### Операции со списками
```python
fruits = ["яблоко", "банан"]

# Добавление элементов
fruits.append("апельсин")          # В конец
fruits.insert(1, "груша")          # По индексу
fruits.extend(["виноград", "киви"]) # Несколько элементов

print(fruits)  # ['яблоко', 'груша', 'банан', 'апельсин', 'виноград', 'киви']

# Удаление элементов
fruits.remove("банан")     # По значению
deleted = fruits.pop()     # Последний элемент
deleted = fruits.pop(0)    # По индексу
del fruits[1]              # По индексу

# Очистка списка
fruits.clear()
```

### Доступ к элементам
```python
numbers = [10, 20, 30, 40, 50]

# По индексу
print(numbers[0])    # 10 (первый)
print(numbers[-1])   # 50 (последний)
print(numbers[-2])   # 40 (второй с конца)

# Срезы (slicing)
print(numbers[1:4])   # [20, 30, 40]
print(numbers[:3])    # [10, 20, 30]
print(numbers[2:])    # [30, 40, 50]
print(numbers[::2])   # [10, 30, 50] (каждый второй)
print(numbers[::-1])  # [50, 40, 30, 20, 10] (обратный порядок)
```

### Методы списков
```python
numbers = [3, 1, 4, 1, 5, 9, 2]

# Поиск
print(numbers.index(4))     # 2 (индекс первого вхождения)
print(numbers.count(1))     # 2 (количество вхождений)
print(4 in numbers)         # True
print(10 in numbers)        # False

# Сортировка
numbers.sort()              # На месте
print(numbers)              # [1, 1, 2, 3, 4, 5, 9]

sorted_nums = sorted([3, 1, 4])  # Новый список [1, 3, 4]

# Обратный порядок
numbers.reverse()
reversed_nums = numbers[::-1]
```

### Списковые включения (List Comprehensions)
```python
# Базовый синтаксис
squares = [x**2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]

# С условием
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# Преобразование строк
words = ["hello", "world", "python"]
uppercase = [word.upper() for word in words]  # ['HELLO', 'WORLD', 'PYTHON']

# Вложенные списки
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

## Кортежи (Tuples)

### Создание кортежей
```python
# Пустой кортеж
empty_tuple = ()
empty_tuple = tuple()

# Кортеж с элементами
coordinates = (10, 20)
person = ("Анна", 25, "Москва")

# Кортеж из одного элемента (запятая обязательна!)
single = (42,)
single = 42,
```

### Особенности кортежей
```python
# Неизменяемость
point = (1, 2, 3)
# point[0] = 5  # Ошибка! Кортежи неизменяемы

# Доступ к элементам (как в списках)
print(point[0])     # 1
print(point[-1])    # 3
print(point[1:])    # (2, 3)

# Распаковка
x, y, z = point
print(f"x={x}, y={y}, z={z}")

# Частичная распаковка
first, *rest = (1, 2, 3, 4, 5)
print(first)  # 1
print(rest)   # [2, 3, 4, 5]
```

### Применение кортежей
```python
# Возврат нескольких значений из функции
def get_name_age():
    return "Анна", 25

name, age = get_name_age()

# Обмен значений переменных
a, b = 10, 20
a, b = b, a  # Меняем местами

# Координаты
points = [(0, 0), (1, 2), (3, 4)]
for x, y in points:
    print(f"Точка: ({x}, {y})")

# Словарь с кортежами-ключами
distances = {
    ("Москва", "СПб"): 635,
    ("Москва", "Казань"): 719,
    ("СПб", "Казань"): 1143
}
```

## Словари (Dictionaries)

### Создание словарей
```python
# Пустой словарь
empty_dict = {}
empty_dict = dict()

# Словарь с элементами
student = {
    "name": "Анна",
    "age": 20,
    "grade": "A",
    "subjects": ["математика", "физика"]
}

# Создание через dict()
student2 = dict(name="Петр", age=22, grade="B")

# Создание из списка кортежей
pairs = [("a", 1), ("b", 2), ("c", 3)]
letters = dict(pairs)  # {'a': 1, 'b': 2, 'c': 3}
```

### Операции со словарями
```python
student = {"name": "Анна", "age": 20}

# Доступ к элементам
print(student["name"])           # "Анна"
print(student.get("age"))        # 20
print(student.get("city", "Неизвестно"))  # "Неизвестно" (значение по умолчанию)

# Добавление/изменение
student["city"] = "Москва"       # Добавляем новый ключ
student["age"] = 21              # Изменяем существующий

# Обновление несколькими значениями
student.update({"grade": "A+", "course": 2})

# Удаление
del student["city"]              # Удаляем ключ
grade = student.pop("grade")     # Удаляем и возвращаем значение
last_item = student.popitem()    # Удаляем последний элемент (Python 3.7+)
```

### Методы словарей
```python
student = {"name": "Анна", "age": 20, "grade": "A"}

# Получение ключей, значений, пар
keys = student.keys()        # dict_keys(['name', 'age', 'grade'])
values = student.values()    # dict_values(['Анна', 20, 'A'])
items = student.items()      # dict_items([('name', 'Анна'), ('age', 20), ('grade', 'A')])

# Преобразование в списки
keys_list = list(student.keys())
values_list = list(student.values())

# Проверка наличия ключа
print("name" in student)     # True
print("city" in student)     # False

# Копирование
student_copy = student.copy()
```

### Итерация по словарям
```python
student = {"name": "Анна", "age": 20, "grade": "A"}

# По ключам (по умолчанию)
for key in student:
    print(f"{key}: {student[key]}")

# Явно по ключам
for key in student.keys():
    print(key)

# По значениям
for value in student.values():
    print(value)

# По парам ключ-значение
for key, value in student.items():
    print(f"{key}: {value}")
```

### Словарные включения (Dict Comprehensions)
```python
# Создание словаря
numbers = [1, 2, 3, 4, 5]
squares = {x: x**2 for x in numbers}  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# С условием
even_squares = {x: x**2 for x in numbers if x % 2 == 0}  # {2: 4, 4: 16}

# Преобразование существующего словаря
prices = {"apple": 100, "banana": 50, "orange": 80}
expensive = {fruit: price for fruit, price in prices.items() if price > 60}
```

## Множества (Sets)

### Создание множеств
```python
# Пустое множество
empty_set = set()  # НЕ {} - это словарь!

# Множество с элементами
numbers = {1, 2, 3, 4, 5}
letters = set("hello")  # {'h', 'e', 'l', 'o'} - дубли удалены

# Из списка
unique_numbers = set([1, 2, 2, 3, 3, 4])  # {1, 2, 3, 4}
```

### Операции с множествами
```python
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

# Объединение
union = set1 | set2           # {1, 2, 3, 4, 5, 6}
union = set1.union(set2)

# Пересечение
intersection = set1 & set2    # {3, 4}
intersection = set1.intersection(set2)

# Разность
difference = set1 - set2      # {1, 2}
difference = set1.difference(set2)

# Симметрическая разность
sym_diff = set1 ^ set2        # {1, 2, 5, 6}
sym_diff = set1.symmetric_difference(set2)
```

### Методы множеств
```python
fruits = {"яблоко", "банан", "апельсин"}

# Добавление
fruits.add("груша")
fruits.update(["киви", "манго"])

# Удаление
fruits.remove("банан")          # Ошибка если элемента нет
fruits.discard("виноград")      # Без ошибки если элемента нет
deleted = fruits.pop()          # Удаляем случайный элемент

# Проверки
print("яблоко" in fruits)       # True
print(len(fruits))              # Количество элементов
```

## Практические примеры

### Подсчет частоты слов
```python
def count_words(text):
    words = text.lower().split()
    word_count = {}
    
    for word in words:
        # Убираем пунктуацию
        clean_word = word.strip(".,!?;:")
        
        # Подсчитываем
        if clean_word in word_count:
            word_count[clean_word] += 1
        else:
            word_count[clean_word] = 1
    
    return word_count

# Альтернатива через get()
def count_words_v2(text):
    words = text.lower().split()
    word_count = {}
    
    for word in words:
        clean_word = word.strip(".,!?;:")
        word_count[clean_word] = word_count.get(clean_word, 0) + 1
    
    return word_count

text = "Python это отличный язык. Python легко изучать."
counts = count_words(text)
print(counts)  # {'python': 2, 'это': 1, 'отличный': 1, ...}
```

### Группировка данных
```python
# Группировка студентов по оценкам
students = [
    {"name": "Анна", "grade": "A"},
    {"name": "Петр", "grade": "B"},
    {"name": "Мария", "grade": "A"},
    {"name": "Иван", "grade": "C"}
]

# Группировка в словарь
by_grade = {}
for student in students:
    grade = student["grade"]
    if grade not in by_grade:
        by_grade[grade] = []
    by_grade[grade].append(student["name"])

print(by_grade)  # {'A': ['Анна', 'Мария'], 'B': ['Петр'], 'C': ['Иван']}

# Альтернатива через setdefault()
by_grade_v2 = {}
for student in students:
    grade = student["grade"]
    by_grade_v2.setdefault(grade, []).append(student["name"])
```

### Удаление дубликатов с сохранением порядка
```python
def remove_duplicates(items):
    seen = set()
    result = []
    
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result

# Пример
numbers = [1, 2, 2, 3, 1, 4, 5, 4]
unique = remove_duplicates(numbers)
print(unique)  # [1, 2, 3, 4, 5]

# Через dict (Python 3.7+)
unique_v2 = list(dict.fromkeys(numbers))
```

### Пересечение списков
```python
def find_common_elements(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    return list(set1 & set2)

# Пример
friends_anna = ["Петр", "Мария", "Иван", "Ольга"]
friends_peter = ["Анна", "Мария", "Сергей", "Ольга"] 

common_friends = find_common_elements(friends_anna, friends_peter)
print(common_friends)  # ['Мария', 'Ольга']
```

## Вложенные структуры данных

### Список словарей
```python
employees = [
    {"name": "Анна", "position": "developer", "salary": 80000},
    {"name": "Петр", "position": "manager", "salary": 120000},
    {"name": "Мария", "position": "designer", "salary": 70000}
]

# Поиск по условию
def find_by_position(employees, position):
    return [emp for emp in employees if emp["position"] == position]

developers = find_by_position(employees, "developer")

# Сортировка по зарплате
sorted_by_salary = sorted(employees, key=lambda x: x["salary"], reverse=True)
```

### Словарь списков
```python
# Расписание занятий
schedule = {
    "понедельник": ["математика", "физика", "английский"],
    "вторник": ["история", "литература"],
    "среда": ["информатика", "химия", "физкультура"]
}

# Добавление предмета
if "четверг" not in schedule:
    schedule["четверг"] = []
schedule["четверг"].append("биология")

# Поиск предмета
def find_subject_day(schedule, subject):
    for day, subjects in schedule.items():
        if subject in subjects:
            return day
    return None

day = find_subject_day(schedule, "физика")
print(f"Физика в {day}")
```

### Словарь словарей
```python
# База данных пользователей
users_db = {
    "user1": {
        "name": "Анна Иванова",
        "email": "anna@example.com",
        "preferences": {"theme": "dark", "language": "ru"}
    },
    "user2": {
        "name": "Петр Петров", 
        "email": "peter@example.com",
        "preferences": {"theme": "light", "language": "en"}
    }
}

# Глубокий доступ
def get_user_preference(users_db, user_id, preference_key, default=None):
    return users_db.get(user_id, {}).get("preferences", {}).get(preference_key, default)

theme = get_user_preference(users_db, "user1", "theme")
print(theme)  # "dark"
```

## Выбор подходящей коллекции

### Когда использовать списки
```python
# Когда нужен порядок и дубликаты
shopping_list = ["хлеб", "молоко", "яйца", "молоко"]  # дубли важны
history = ["page1", "page2", "page1"]  # порядок важен

# Когда нужна индексация
menu_items = ["Салат", "Суп", "Основное", "Десерт"]
selected = menu_items[2]  # Выбираем по номеру
```

### Когда использовать кортежи
```python
# Неизменяемые данные
RGB_RED = (255, 0, 0)
coordinates = (55.7558, 37.6176)  # Москва

# Ключи словаря (должны быть неизменяемыми)
game_scores = {
    ("Анна", "Петр"): "2:1",
    ("Мария", "Иван"): "0:3"
}

# Возврат нескольких значений
def divmod_custom(a, b):
    return a // b, a % b  # частное, остаток
```

### Когда использовать словари
```python
# Связь ключ-значение
phone_book = {"Анна": "+7-123-456-78-90", "Петр": "+7-987-654-32-10"}

# Настройки и конфигурации
config = {
    "debug": True,
    "database_url": "postgresql://...",
    "max_connections": 100
}

# Счетчики и группировка
votes = {"кандидат_А": 1250, "кандидат_Б": 980, "кандидат_В": 1100}
```

### Когда использовать множества
```python
# Уникальные элементы
unique_visitors = {"user1", "user2", "user3"}

# Математические операции
python_students = {"Анна", "Петр", "Мария"}
java_students = {"Петр", "Иван", "Ольга"}
both_languages = python_students & java_students  # {"Петр"}

# Проверка принадлежности (быстрее чем в списке)
valid_extensions = {".jpg", ".png", ".gif", ".webp"}
if file_extension in valid_extensions:
    print("Валидное изображение")
```

## Частые ошибки

### 1. Изменение списка во время итерации
```python
# ПЛОХО
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Может пропустить элементы

# ХОРОШО
numbers = [1, 2, 3, 4, 5]
numbers = [num for num in numbers if num % 2 != 0]
```

### 2. Изменение значений по умолчанию
```python
# ПЛОХО - опасное значение по умолчанию
def add_item(item, target_list=[]):
    target_list.append(item)
    return target_list

list1 = add_item(1)  # [1]
list2 = add_item(2)  # [1, 2] - неожиданно!

# ХОРОШО
def add_item(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list
```

### 3. Неправильное копирование
```python
# ПОВЕРХНОСТНОЕ копирование
original = [[1, 2], [3, 4]]
shallow_copy = original.copy()
shallow_copy[0][0] = 999
print(original)  # [[999, 2], [3, 4]] - изменился!

# ГЛУБОКОЕ копирование
import copy
original = [[1, 2], [3, 4]]
deep_copy = copy.deepcopy(original)
deep_copy[0][0] = 999
print(original)  # [[1, 2], [3, 4]] - не изменился
```

## Ключевые моменты для экзамена

- **Списки** - изменяемые, упорядоченные, с дубликатами
- **Кортежи** - неизменяемые, упорядоченные, с дубликатами  
- **Словари** - изменяемые, неупорядоченные (Python 3.7+ сохраняют порядок), уникальные ключи
- **Множества** - изменяемые, неупорядоченные, уникальные элементы
- **Методы доступа:** `[]` (ошибка если нет), `.get()` (безопасно для словарей)
- **Включения** - краткий способ создания коллекций с условиями
- **Операции множеств** - объединение `|`, пересечение `&`, разность `-`
- **Выбор типа** зависит от потребности в порядке, изменяемости и уникальности