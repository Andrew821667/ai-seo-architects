# Логические условия и условный оператор

## Логические значения

### Bool тип
```python
is_sunny = True
is_raining = False

# Преобразование в bool
bool(1)        # True
bool(0)        # False
bool("")       # False (пустая строка)
bool("text")   # True
bool([])       # False (пустой список)
bool([1, 2])   # True
bool(None)     # False
```

## Операторы сравнения

### Основные операторы
```python
a = 10
b = 5

# Равенство
a == b    # False
a != b    # True

# Сравнение
a > b     # True
a < b     # False
a >= b    # True
a <= b    # False
```

### Сравнение строк
```python
# Лексикографическое сравнение
"apple" < "banana"    # True
"Apple" < "apple"     # True (заглавные буквы меньше)

# Сравнение длины
len("hello") == 5     # True

# Проверка содержания
"el" in "hello"       # True
"hi" not in "hello"   # True
```

## Логические операторы

### Основные операторы
```python
# and - логическое И
True and True    # True
True and False   # False
False and True   # False
False and False  # False

# or - логическое ИЛИ
True or True     # True
True or False    # True
False or True    # True
False or False   # False

# not - логическое НЕ
not True         # False
not False        # True
```

### Приоритет логических операторов
```python
# Приоритет (от высшего к низшему):
# 1. not
# 2. and
# 3. or

result = True or False and not True  # True
# Эквивалентно: True or (False and (not True))
```

### Короткие вычисления (short-circuit)
```python
# and - если первое False, второе не вычисляется
False and print("Это не выполнится")  # False

# or - если первое True, второе не вычисляется
True or print("Это не выполнится")    # True

# Практическое применение
def safe_divide(a, b):
    return b != 0 and a / b  # Деление только если b != 0
```

## Условный оператор if

### Базовый синтаксис
```python
age = 18

if age >= 18:
    print("Совершеннолетний")
    print("Можно голосовать")
```

### if-else
```python
temperature = 25

if temperature > 30:
    print("Жарко")
else:
    print("Нормальная температура")
```

### if-elif-else
```python
score = 85

if score >= 90:
    grade = "Отлично"
elif score >= 80:
    grade = "Хорошо"
elif score >= 70:
    grade = "Удовлетворительно"
else:
    grade = "Неудовлетворительно"

print(f"Оценка: {grade}")
```

## Сложные условия

### Множественные условия
```python
age = 25
has_license = True
has_car = False

# Сложное условие
if age >= 18 and has_license and has_car:
    print("Может водить")
elif age >= 18 and has_license:
    print("Может водить, но нет машины")
else:
    print("Не может водить")
```

### Проверка диапазонов
```python
temperature = 25

# Проверка диапазона
if 20 <= temperature <= 30:
    print("Комфортная температура")

# Эквивалентно:
if temperature >= 20 and temperature <= 30:
    print("Комфортная температура")
```

### Проверка принадлежности
```python
vowels = "aeiou"
letter = "a"

if letter in vowels:
    print("Гласная буква")

# Проверка в списке
valid_grades = ["A", "B", "C", "D", "F"]
student_grade = "B"

if student_grade in valid_grades:
    print("Корректная оценка")
```

## Тернарный оператор

### Краткая запись условия
```python
age = 20

# Обычный способ
if age >= 18:
    status = "взрослый"
else:
    status = "ребенок"

# Тернарный оператор
status = "взрослый" if age >= 18 else "ребенок"

# Другие примеры
max_value = a if a > b else b
message = "Четное" if number % 2 == 0 else "Нечетное"
```

## Вложенные условия

### Структура
```python
weather = "sunny"
temperature = 25

if weather == "sunny":
    if temperature > 30:
        print("Жарко и солнечно")
    elif temperature > 20:
        print("Тепло и солнечно")
    else:
        print("Прохладно, но солнечно")
else:
    print("Не солнечно")
```

### Упрощение вложенных условий
```python
# Вместо вложенных условий
if user_authenticated:
    if user_has_permission:
        if resource_available:
            print("Доступ разрешен")

# Лучше использовать and
if user_authenticated and user_has_permission and resource_available:
    print("Доступ разрешен")
```

## Практические примеры

### Проверка високосного года
```python
def is_leap_year(year):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False

# Или более краткая версия
def is_leap_year_short(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)
```

### Определение сезона
```python
def get_season(month):
    if month in [12, 1, 2]:
        return "Зима"
    elif month in [3, 4, 5]:
        return "Весна"
    elif month in [6, 7, 8]:
        return "Лето"
    elif month in [9, 10, 11]:
        return "Осень"
    else:
        return "Некорректный месяц"

season = get_season(6)  # "Лето"
```

### Классификация возраста
```python
def classify_age(age):
    if age < 0:
        return "Некорректный возраст"
    elif age < 13:
        return "Ребенок"
    elif age < 20:
        return "Подросток"
    elif age < 60:
        return "Взрослый"
    else:
        return "Пожилой"
```

### Валидация пароля
```python
def validate_password(password):
    if len(password) < 8:
        return False, "Пароль слишком короткий"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not (has_upper and has_lower and has_digit):
        return False, "Пароль должен содержать заглавные, строчные буквы и цифры"
    
    return True, "Пароль корректный"

is_valid, message = validate_password("MyPass123")
```

## Частые ошибки

1. **Использование = вместо ==**
```python
# ОШИБКА
if x = 5:  # SyntaxError
    print("x равен 5")

# ПРАВИЛЬНО
if x == 5:
    print("x равен 5")
```

2. **Сравнение с bool**
```python
# ПЛОХО
if is_active == True:
    pass

# ХОРОШО
if is_active:
    pass

# ПЛОХО
if is_active == False:
    pass

# ХОРОШО
if not is_active:
    pass
```

3. **Цепочки сравнений**
```python
# ОШИБКА
if 10 < x < 20 and x < 15:  # Избыточное условие

# ПРАВИЛЬНО
if 10 < x < 15:
    pass
```

## Ключевые моменты для экзамена

- Логические операторы: and, or, not
- Операторы сравнения: ==, !=, <, >, <=, >=
- Условный оператор: if, elif, else
- Тернарный оператор: `value = a if condition else b`
- Проверка принадлежности: in, not in
- Проверка диапазонов: `a <= x <= b`
- Короткие вычисления (short-circuit evaluation)
- bool() преобразование и "ложные" значения: False, 0, "", [], None