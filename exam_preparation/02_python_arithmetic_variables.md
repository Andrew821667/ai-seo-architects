# Арифметические операции, переменные, типы данных

## Переменные

### Создание и присваивание
```python
# Простое присваивание
x = 10
name = "Алексей"
is_student = True

# Множественное присваивание
a, b, c = 1, 2, 3
x = y = z = 0

# Обмен значениями
a, b = b, a
```

### Правила именования переменных
```python
# ПРАВИЛЬНО
user_name = "Иван"
age2 = 25
_private_var = "секрет"
camelCase = "стиль"

# НЕПРАВИЛЬНО
# 2age = 25        # Нельзя начинать с цифры
# user-name = "Иван"  # Нельзя использовать дефис
# class = "A"      # Нельзя использовать зарезервированные слова
```

## Типы данных

### Числовые типы
```python
# int - целые числа
age = 25
big_number = 1000000
negative = -42

# float - числа с плавающей точкой
pi = 3.14159
temperature = -15.5
scientific = 1.23e-4  # 0.000123

# complex - комплексные числа
z = 3 + 4j
z2 = complex(2, 5)  # 2 + 5j
```

### Строки (str)
```python
# Различные способы создания
single_quotes = 'Привет'
double_quotes = "Мир"
multiline = """Многострочная
строка"""

# Экранирование
escaped = "Он сказал: \"Привет!\""
path = r"C:\Users\Name"  # raw string
```

### Логический тип (bool)
```python
is_true = True
is_false = False

# Преобразование в bool
bool(1)      # True
bool(0)      # False
bool("")     # False
bool("text") # True
bool([])     # False
bool([1])    # True
```

## Арифметические операции

### Основные операторы
```python
a = 10
b = 3

# Сложение
result = a + b  # 13

# Вычитание
result = a - b  # 7

# Умножение
result = a * b  # 30

# Деление (возвращает float)
result = a / b  # 3.3333...

# Целочисленное деление
result = a // b  # 3

# Остаток от деления
result = a % b  # 1

# Возведение в степень
result = a ** b  # 1000
```

### Приоритет операций
```python
# Приоритет (от высшего к низшему):
# 1. ** (возведение в степень)
# 2. *, /, //, % (умножение, деление)
# 3. +, - (сложение, вычитание)

result = 2 + 3 * 4    # 14, не 20
result = (2 + 3) * 4  # 20
result = 2 ** 3 * 4   # 32 (2^3 * 4)
```

### Операторы присваивания
```python
x = 10

x += 5   # x = x + 5  → 15
x -= 3   # x = x - 3  → 12
x *= 2   # x = x * 2  → 24
x /= 4   # x = x / 4  → 6.0
x //= 2  # x = x // 2 → 3.0
x %= 2   # x = x % 2  → 1.0
x **= 3  # x = x ** 3 → 1.0
```

## Преобразование типов

### Явное преобразование
```python
# В целое число
int("123")    # 123
int(3.14)     # 3
int(True)     # 1

# В число с плавающей точкой
float("3.14") # 3.14
float(5)      # 5.0
float(True)   # 1.0

# В строку
str(123)      # "123"
str(3.14)     # "3.14"
str(True)     # "True"

# В логический тип
bool(1)       # True
bool(0)       # False
bool("text")  # True
bool("")      # False
```

### Проверка типов
```python
x = 42
print(type(x))           # <class 'int'>
print(isinstance(x, int)) # True

# Проверка нескольких типов
isinstance(x, (int, float)) # True
```

## Операции со строками

### Арифметические операции
```python
# Конкатенация (сложение)
first_name = "Анна"
last_name = "Петрова"
full_name = first_name + " " + last_name  # "Анна Петрова"

# Повторение (умножение)
pattern = "abc" * 3  # "abcabcabc"
separator = "-" * 20  # "--------------------"
```

## Практические примеры

### Калькулятор площади
```python
def rectangle_area():
    length = float(input("Длина: "))
    width = float(input("Ширина: "))
    area = length * width
    perimeter = 2 * (length + width)
    
    print(f"Площадь: {area}")
    print(f"Периметр: {perimeter}")

rectangle_area()
```

### Конвертер температуры
```python
def celsius_to_fahrenheit(celsius):
    fahrenheit = celsius * 9/5 + 32
    return fahrenheit

def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    return celsius

temp_c = 25
temp_f = celsius_to_fahrenheit(temp_c)
print(f"{temp_c}°C = {temp_f}°F")
```

### Работа с временем
```python
# Перевод секунд в часы, минуты, секунды
total_seconds = 3661

hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60

print(f"{total_seconds} секунд = {hours}ч {minutes}м {seconds}с")
```

## Частые ошибки

1. **Деление целых чисел**
```python
# Python 3 - деление всегда возвращает float
result = 10 / 2  # 5.0, не 5

# Для целочисленного деления используйте //
result = 10 // 3  # 3
```

2. **Смешивание типов**
```python
# ОШИБКА
# age = "25"
# next_year = age + 1  # TypeError

# ПРАВИЛЬНО
age = int("25")
next_year = age + 1
```

3. **Операторы присваивания**
```python
# ОШИБКА
# x =+ 5  # Это x = +5, а не x += 5

# ПРАВИЛЬНО
x += 5
```

## Ключевые моменты для экзамена

- Переменные создаются при первом присваивании
- Python - динамически типизированный язык
- Основные типы: int, float, str, bool
- Деление `/` всегда возвращает float, `//` - целочисленное деление
- Операторы присваивания: +=, -=, *=, /=, //=, %=, **=
- Приоритет операций: ** → *, /, //, % → +, -
- Функции преобразования: int(), float(), str(), bool()
- type() и isinstance() для проверки типов