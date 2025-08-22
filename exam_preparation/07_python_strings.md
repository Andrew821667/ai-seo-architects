# Работа с текстами. Операции над строками

## Создание строк

### Различные способы создания
```python
# Одинарные и двойные кавычки
single_quote = 'Привет мир'
double_quote = "Привет мир"
with_apostrophe = "Don't worry"
with_quotes = 'Он сказал: "Привет!"'

# Тройные кавычки (многострочные)
multiline = """
Это многострочная
строка с переносами
и отступами
"""

# Экранирование символов
escaped = "Строка с \"кавычками\" и \\ слэшем"
path = r"C:\Users\Andrew\Documents"  # raw строка (r-строка)
```

### Строковые литералы
```python
name = "Анна"
age = 25

# f-строки (Python 3.6+) - рекомендуемый способ
greeting = f"Привет, {name}! Тебе {age} лет."

# .format() метод
greeting = "Привет, {}! Тебе {} лет.".format(name, age)
greeting = "Привет, {name}! Тебе {age} лет.".format(name=name, age=age)

# % форматирование (старый способ)
greeting = "Привет, %s! Тебе %d лет." % (name, age)
```

## Базовые операции со строками

### Конкатенация и повторение
```python
first_name = "Анна"
last_name = "Иванова"

# Конкатенация
full_name = first_name + " " + last_name  # "Анна Иванова"
full_name = " ".join([first_name, last_name])

# Повторение
separator = "-" * 20  # "--------------------"
laugh = "ха" * 3      # "хахаха"

# Сложение списка строк
parts = ["Python", "это", "отличный", "язык"]
sentence = " ".join(parts)  # "Python это отличный язык"
```

### Доступ к символам
```python
text = "Python"

# По индексу
print(text[0])    # "P" (первый символ)
print(text[-1])   # "n" (последний символ)

# Срезы
print(text[1:4])  # "yth"
print(text[:3])   # "Pyt"
print(text[2:])   # "thon"
print(text[::2])  # "Pto" (каждый второй)
print(text[::-1]) # "nohtyP" (обратный порядок)

# Строки неизменяемы!
# text[0] = "J"  # Ошибка! Нельзя изменить символ
```

## Методы строк

### Методы поиска
```python
text = "Python это мощный язык программирования"

# Поиск подстроки
print(text.find("мощный"))      # 12 (индекс начала)
print(text.find("Java"))        # -1 (не найдено)
print(text.index("Python"))     # 0 (ошибка если не найдено)

# Проверки содержания
print("Python" in text)         # True
print(text.startswith("Python")) # True
print(text.endswith("ния"))      # True

# Подсчет вхождений
print(text.count("о"))          # 4
print(text.count("Python"))     # 1
```

### Методы преобразования регистра
```python
text = "PyThOn ПрОгРаМмИрОвАнИе"

# Регистр
print(text.lower())      # "python программирование"
print(text.upper())      # "PYTHON ПРОГРАММИРОВАНИЕ"
print(text.capitalize()) # "Python программирование"
print(text.title())      # "Python Программирование"

# Проверки регистра
print("HELLO".isupper())   # True
print("hello".islower())   # True
print("Hello".istitle())   # True

# Инверсия регистра
print("Hello".swapcase())  # "hELLO"
```

### Методы очистки и форматирования
```python
# Удаление пробелов
text = "  Много пробелов  \n\t"
print(text.strip())       # "Много пробелов"
print(text.lstrip())      # "Много пробелов  \n\t"
print(text.rstrip())      # "  Много пробелов"

# Удаление конкретных символов
text = "...Hello!!!"
print(text.strip(".!"))   # "Hello"

# Выравнивание
word = "Python"
print(word.center(10))    # "  Python  "
print(word.ljust(10))     # "Python    "
print(word.rjust(10))     # "    Python"
print(word.zfill(8))      # "00Python" (дополнение нулями)
```

### Методы разделения и объединения
```python
# split() - разделение строки
sentence = "Python это отличный язык"
words = sentence.split()           # ["Python", "это", "отличный", "язык"]
words = sentence.split(" ")        # То же самое

# Разделение по другому символу
csv_data = "name,age,city"
fields = csv_data.split(",")       # ["name", "age", "city"]

# splitlines() - разделение по строкам
multiline = "строка1\nстрока2\nстрока3"
lines = multiline.splitlines()     # ["строка1", "строка2", "строка3"]

# partition() - разделение на 3 части
email = "user@example.com"
local, sep, domain = email.partition("@")  # ("user", "@", "example.com")

# join() - объединение
words = ["Python", "это", "круто"]
sentence = " ".join(words)         # "Python это круто"
csv_line = ",".join(["Анна", "25", "Москва"])  # "Анна,25,Москва"
```

### Методы замены
```python
text = "Python это отличный язык программирования"

# replace() - замена подстроки
new_text = text.replace("Python", "Java")
new_text = text.replace("о", "О", 2)  # Заменить только первые 2 вхождения

# translate() - замена символов
# Создание таблицы замен
translation_table = str.maketrans("аеиоу", "АЕИОУ")
result = text.translate(translation_table)
```

## Проверка типов символов

### Методы проверки
```python
# Проверки типов символов
text = "Python123"
print(text.isalpha())     # False (есть цифры)
print(text.isdigit())     # False (есть буквы)
print(text.isalnum())     # True (буквы и цифры)

# Отдельные символы
char = "5"
print(char.isdigit())     # True
print(char.isnumeric())   # True

char = "a"
print(char.isalpha())     # True
print(char.islower())     # True

# Проверки содержимого
print("HELLO".isupper())  # True
print("hello world".islower())  # True
print(" \t\n".isspace())  # True (только пробельные символы)
```

### Практическая валидация
```python
def validate_password(password):
    """Валидация пароля"""
    if len(password) < 8:
        return False, "Минимум 8 символов"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not has_upper:
        return False, "Нужна заглавная буква"
    if not has_lower:
        return False, "Нужна строчная буква"
    if not has_digit:
        return False, "Нужна цифра"
    
    return True, "Пароль корректный"

# Тестирование
passwords = ["123", "password", "Password", "Password123"]
for pwd in passwords:
    valid, message = validate_password(pwd)
    print(f"{pwd}: {message}")
```

## Форматирование строк

### f-строки (современный способ)
```python
name = "Анна"
age = 25
pi = 3.141592653589793

# Базовое форматирование
message = f"Привет, {name}! Тебе {age} лет."

# Форматирование чисел
formatted = f"Число π = {pi:.2f}"  # "Число π = 3.14"
percentage = f"Прогресс: {0.875:.1%}"  # "Прогресс: 87.5%"

# Выравнивание
name = "Python"
formatted = f"|{name:>10}|"  # "|    Python|" (правое выравнивание)
formatted = f"|{name:<10}|"  # "|Python    |" (левое выравнивание)
formatted = f"|{name:^10}|"  # "|  Python  |" (центрирование)

# Заполнение символами
formatted = f"{42:0>5}"      # "00042"
formatted = f"{'test':*^10}" # "***test***"

# Выражения внутри f-строк
numbers = [1, 2, 3, 4, 5]
result = f"Сумма: {sum(numbers)}, Среднее: {sum(numbers)/len(numbers):.1f}"
```

### .format() метод
```python
# Позиционные аргументы
template = "Привет, {}! Тебе {} лет."
result = template.format("Анна", 25)

# Именованные аргументы
template = "Привет, {name}! Тебе {age} лет."
result = template.format(name="Анна", age=25)

# Индексы
template = "Координаты: ({0}, {1}). Точка {0} по X."
result = template.format(10, 20)  # "Координаты: (10, 20). Точка 10 по X."

# Форматирование чисел
pi = 3.141592653589793
formatted = "π = {:.3f}".format(pi)  # "π = 3.142"
```

## Регулярные выражения (введение)

### Модуль re
```python
import re

# Простой поиск
text = "Мой email: anna@example.com"
email_pattern = r"\w+@\w+\.\w+"
match = re.search(email_pattern, text)

if match:
    print(f"Найден email: {match.group()}")  # anna@example.com

# Найти все совпадения
text = "Телефоны: +7-123-456-78-90, +7-987-654-32-10"
phone_pattern = r"\+7-\d{3}-\d{3}-\d{2}-\d{2}"
phones = re.findall(phone_pattern, text)
print(phones)  # ['+7-123-456-78-90', '+7-987-654-32-10']

# Замена
text = "Дата: 2024-12-31"
new_text = re.sub(r"\d{4}-\d{2}-\d{2}", "YYYY-MM-DD", text)
print(new_text)  # "Дата: YYYY-MM-DD"
```

### Валидация с регулярными выражениями
```python
def validate_phone(phone):
    """Проверка российского номера телефона"""
    pattern = r"^\+7-\d{3}-\d{3}-\d{2}-\d{2}$"
    return re.match(pattern, phone) is not None

def validate_email(email):
    """Простая проверка email"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

# Тестирование
phones = ["+7-123-456-78-90", "123-456-78-90", "+7-123-456"]
for phone in phones:
    print(f"{phone}: {validate_phone(phone)}")
```

## Обработка текстовых данных

### Очистка и нормализация
```python
def clean_text(text):
    """Очистка и нормализация текста"""
    # Удаление лишних пробелов
    text = " ".join(text.split())
    
    # Приведение к нижнему регистру
    text = text.lower()
    
    # Удаление пунктуации
    import string
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    return text

# Пример
messy_text = "  Привет,    МИР!!!   Как   дела???  "
clean = clean_text(messy_text)
print(clean)  # "привет мир как дела"
```

### Работа с CSV данными
```python
def parse_csv_line(line):
    """Простой парсер CSV строки"""
    # Разделяем по запятым
    fields = line.strip().split(",")
    
    # Очищаем пробелы
    fields = [field.strip() for field in fields]
    
    return fields

def create_csv_line(fields):
    """Создание CSV строки из полей"""
    # Экранируем поля с запятыми
    escaped_fields = []
    for field in fields:
        field_str = str(field)
        if "," in field_str:
            field_str = f'"{field_str}"'
        escaped_fields.append(field_str)
    
    return ",".join(escaped_fields)

# Примеры
csv_line = "Анна, Иванова, 25, Москва"
fields = parse_csv_line(csv_line)
print(fields)  # ['Анна', 'Иванова', '25', 'Москва']

new_line = create_csv_line(["Петр", "Петров, мл.", 30, "СПб"])
print(new_line)  # Петр,"Петров, мл.",30,СПб
```

### Извлечение данных из текста
```python
def extract_numbers(text):
    """Извлечение всех чисел из текста"""
    import re
    pattern = r"-?\d+\.?\d*"
    numbers = re.findall(pattern, text)
    return [float(num) for num in numbers]

def extract_words(text, min_length=3):
    """Извлечение слов минимальной длины"""
    import re
    # Только буквы (включая русские)
    pattern = r"[a-zA-Zа-яА-Я]+"
    words = re.findall(pattern, text)
    return [word for word in words if len(word) >= min_length]

# Примеры
text = "Цена товара: 1250.50 руб. Скидка: 15%"
numbers = extract_numbers(text)
print(numbers)  # [1250.5, 15.0]

text = "Python - это отличный язык для начинающих!"
words = extract_words(text, min_length=4)
print(words)  # ['Python', 'отличный', 'язык', 'начинающих']
```

## Шаблоны и форматирование

### Создание шаблонов
```python
# Шаблон для email
email_template = """
Уважаемый(ая) {name}!

Спасибо за регистрацию на нашем сайте.
Ваш логин: {username}
Дата регистрации: {date}

С уважением,
Команда поддержки
"""

# Использование шаблона
user_data = {
    "name": "Анна Иванова",
    "username": "anna_ivanova",
    "date": "2024-12-31"
}

email = email_template.format(**user_data)
print(email)
```

### Продвинутое форматирование
```python
# Форматирование чисел
price = 1234567.89
formatted_price = f"{price:,.2f} ₽"  # "1,234,567.89 ₽"

# Дата и время
from datetime import datetime
now = datetime.now()
formatted_date = f"{now:%Y-%m-%d %H:%M:%S}"  # "2024-12-31 15:30:45"

# Таблица
def format_table(data, headers):
    """Форматирование данных в виде таблицы"""
    # Определяем ширину колонок
    col_widths = []
    for i, header in enumerate(headers):
        max_width = len(header)
        for row in data:
            max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width + 2)
    
    # Заголовок
    header_line = "|".join(f"{header:^{width}}" for header, width in zip(headers, col_widths))
    separator = "|".join("-" * width for width in col_widths)
    
    # Строки данных
    data_lines = []
    for row in data:
        line = "|".join(f"{str(item):^{width}}" for item, width in zip(row, col_widths))
        data_lines.append(line)
    
    return "\n".join([header_line, separator] + data_lines)

# Пример использования
headers = ["Имя", "Возраст", "Город"]
data = [
    ["Анна", 25, "Москва"],
    ["Петр", 30, "СПб"],
    ["Мария", 28, "Казань"]
]

table = format_table(data, headers)
print(table)
```

## Продвинутые операции

### Строковые методы для валидации
```python
def validate_username(username):
    """Валидация имени пользователя"""
    # Длина
    if not (3 <= len(username) <= 20):
        return False, "Длина должна быть от 3 до 20 символов"
    
    # Только буквы, цифры и подчеркивания
    if not username.replace("_", "").isalnum():
        return False, "Только буквы, цифры и подчеркивания"
    
    # Начинается с буквы
    if not username[0].isalpha():
        return False, "Должно начинаться с буквы"
    
    # Не заканчивается подчеркиванием
    if username.endswith("_"):
        return False, "Не должно заканчиваться подчеркиванием"
    
    return True, "Корректное имя пользователя"

# Тестирование
usernames = ["anna", "user_123", "123user", "_invalid", "a", "very_long_username_that_exceeds_limit"]
for username in usernames:
    valid, message = validate_username(username)
    print(f"{username}: {message}")
```

### Парсинг структурированного текста
```python
def parse_log_line(line):
    """Парсинг строки лога"""
    # Пример: "2024-12-31 15:30:45 [ERROR] Connection failed"
    parts = line.strip().split(" ", 3)
    
    if len(parts) < 4:
        return None
    
    date = parts[0]
    time = parts[1]
    level = parts[2].strip("[]")
    message = parts[3]
    
    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message
    }

def parse_config_file(content):
    """Парсинг простого конфигурационного файла"""
    config = {}
    
    for line in content.splitlines():
        line = line.strip()
        
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith("#"):
            continue
        
        # Ищем пары ключ=значение
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            
            # Попытка преобразовать в число или булево
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            elif value.isdigit():
                value = int(value)
            elif "." in value and value.replace(".", "").isdigit():
                value = float(value)
            
            config[key] = value
    
    return config

# Пример использования
config_text = """
# Настройки приложения
debug = true
port = 8080
host = localhost
timeout = 30.5
"""

config = parse_config_file(config_text)
print(config)  # {'debug': True, 'port': 8080, 'host': 'localhost', 'timeout': 30.5}
```

## Работа с Unicode и кодировками

### Кодирование и декодирование
```python
# Строка в байты
text = "Привет мир!"
bytes_utf8 = text.encode("utf-8")
bytes_cp1251 = text.encode("cp1251")

print(bytes_utf8)   # b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82 \xd0\xbc\xd0\xb8\xd1\x80!'

# Байты в строку
decoded = bytes_utf8.decode("utf-8")
print(decoded)      # "Привет мир!"

# Обработка ошибок кодирования
def safe_decode(data, encoding="utf-8"):
    try:
        return data.decode(encoding)
    except UnicodeDecodeError:
        return data.decode(encoding, errors="replace")  # Заменить на �
```

### Работа с различными языками
```python
# Проверка на кириллицу
def is_cyrillic(text):
    """Проверка, содержит ли текст кириллицу"""
    return any("\u0400" <= char <= "\u04FF" for char in text)

# Транслитерация (упрощенная)
CYRILLIC_TO_LATIN = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "е": "e", "ё": "yo", "ж": "zh", "з": "z", "и": "i",
    "й": "y", "к": "k", "л": "l", "м": "m", "н": "n",
    "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch",
    "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "",
    "э": "e", "ю": "yu", "я": "ya"
}

def transliterate(text):
    """Простая транслитерация с кириллицы"""
    result = ""
    for char in text.lower():
        result += CYRILLIC_TO_LATIN.get(char, char)
    return result

print(transliterate("Привет мир"))  # "privet mir"
```

## Частые ошибки

### 1. Попытка изменить строку
```python
# ОШИБКА - строки неизменяемы
text = "hello"
# text[0] = "H"  # TypeError!

# ПРАВИЛЬНО
text = "H" + text[1:]  # "Hello"
text = text.replace("h", "H")  # "Hello"
```

### 2. Неправильное сравнение строк
```python
# Регистрозависимое сравнение
name1 = "анна"
name2 = "Анна"
print(name1 == name2)  # False

# Правильное сравнение
print(name1.lower() == name2.lower())  # True

# Проблемы с пробелами
user_input = "  Анна  "
if user_input.strip().lower() == "анна":
    print("Имя найдено")
```

### 3. Неэффективная конкатенация в циклах
```python
# ПЛОХО - медленно для больших объемов
result = ""
for i in range(1000):
    result += str(i) + " "

# ХОРОШО - используем join()
parts = []
for i in range(1000):
    parts.append(str(i))
result = " ".join(parts)

# ЕЩЕ ЛУЧШЕ - генератор
result = " ".join(str(i) for i in range(1000))
```

## Практические задачи

### Проверка палиндрома
```python
def is_palindrome(text):
    """Проверка, является ли текст палиндромом"""
    # Очищаем текст
    clean_text = "".join(char.lower() for char in text if char.isalnum())
    
    # Сравниваем с обращенным
    return clean_text == clean_text[::-1]

# Тестирование
test_texts = [
    "А роза упала на лапу Азора",
    "Madam",
    "race a car",
    "12321"
]

for text in test_texts:
    print(f"'{text}': {is_palindrome(text)}")
```

### Извлечение доменов из email
```python
def extract_domains(emails):
    """Извлечение доменов из списка email адресов"""
    domains = set()
    
    for email in emails:
        if "@" in email:
            domain = email.split("@")[1]
            domains.add(domain.lower())
    
    return sorted(list(domains))

# Пример
emails = [
    "anna@gmail.com",
    "peter@yandex.ru", 
    "maria@GMAIL.com",
    "invalid-email",
    "john@company.com"
]

domains = extract_domains(emails)
print(domains)  # ['company.com', 'gmail.com', 'yandex.ru']
```

### Генерация паролей
```python
import random
import string

def generate_password(length=12, include_symbols=True):
    """Генерация безопасного пароля"""
    # Базовые символы
    chars = string.ascii_letters + string.digits
    
    if include_symbols:
        chars += "!@#$%^&*"
    
    # Обеспечиваем наличие всех типов символов
    password = [
        random.choice(string.ascii_lowercase),  # строчная буква
        random.choice(string.ascii_uppercase),  # заглавная буква
        random.choice(string.digits)            # цифра
    ]
    
    if include_symbols:
        password.append(random.choice("!@#$%^&*"))
    
    # Дополняем до нужной длины
    for _ in range(length - len(password)):
        password.append(random.choice(chars))
    
    # Перемешиваем
    random.shuffle(password)
    
    return "".join(password)

# Генерация нескольких паролей
for _ in range(3):
    print(generate_password(10))
```

## Ключевые моменты для экзамена

- **Строки неизменяемы** - любая "модификация" создает новую строку
- **f-строки** - современный способ форматирования `f"Hello {name}"`
- **Методы строк** - `.split()`, `.join()`, `.replace()`, `.strip()`
- **Проверки** - `.startswith()`, `.endswith()`, `.isdigit()`, `.isalpha()`
- **Регистр** - `.lower()`, `.upper()`, `.capitalize()`, `.title()`
- **Поиск** - `.find()`, `.index()`, `.count()`, `in` оператор
- **Срезы** - `text[start:end:step]` для извлечения подстрок
- **join() vs +=** - для множественной конкатенации используйте `.join()`
- **Регулярные выражения** - модуль `re` для сложного поиска и замены
- **Кодировки** - `.encode()` и `.decode()` для работы с байтами