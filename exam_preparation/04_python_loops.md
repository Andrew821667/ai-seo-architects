# Циклы for и while

## Цикл for

### Основы цикла for
```python
# Итерация по последовательности
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Итерация по строке
for char in "Hello":
    print(char)  # H, e, l, l, o

# Итерация по списку
fruits = ["яблоко", "банан", "апельсин"]
for fruit in fruits:
    print(fruit)
```

### Функция range()
```python
# range(stop)
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop)
for i in range(2, 7):
    print(i)  # 2, 3, 4, 5, 6

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Обратная последовательность
for i in range(10, 0, -1):
    print(i)  # 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
```

### Итерация с индексом
```python
items = ["a", "b", "c"]

# Способ 1: enumerate()
for index, item in enumerate(items):
    print(f"{index}: {item}")

# Способ 2: range(len())
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# enumerate с начальным значением
for index, item in enumerate(items, start=1):
    print(f"{index}: {item}")  # 1: a, 2: b, 3: c
```

### Итерация по словарю
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

### Вложенные циклы
```python
# Таблица умножения
for i in range(1, 4):
    for j in range(1, 4):
        result = i * j
        print(f"{i} × {j} = {result}")
    print()  # Пустая строка между таблицами

# Работа с двумерным списком
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in matrix:
    for element in row:
        print(element, end=" ")
    print()  # Новая строка после каждой строки матрицы
```

## Цикл while

### Основы цикла while
```python
# Простой while
count = 0
while count < 5:
    print(f"Счетчик: {count}")
    count += 1

# While с условием
password = ""
while password != "secret":
    password = input("Введите пароль: ")
print("Доступ разрешен!")
```

### Бесконечные циклы
```python
# Осторожно! Бесконечный цикл
# while True:
#     print("Это будет печататься бесконечно")

# Правильное использование бесконечного цикла
while True:
    user_input = input("Введите команду (exit для выхода): ")
    if user_input == "exit":
        break
    print(f"Вы ввели: {user_input}")
```

### Цикл while с else
```python
# else выполняется, если цикл завершился нормально (без break)
count = 0
while count < 3:
    print(f"Итерация {count}")
    count += 1
else:
    print("Цикл завершен нормально")

# Если есть break, else не выполняется
count = 0
while count < 10:
    if count == 3:
        break
    print(f"Итерация {count}")
    count += 1
else:
    print("Это не выполнится")  # Не выполнится из-за break
```

## Управление циклами

### break - выход из цикла
```python
# Поиск элемента
numbers = [1, 3, 5, 7, 9, 2, 4]
target = 7

for num in numbers:
    if num == target:
        print(f"Найден элемент: {num}")
        break
else:
    print("Элемент не найден")

# Выход из вложенного цикла
for i in range(3):
    for j in range(3):
        if i == 1 and j == 1:
            break  # Выходит только из внутреннего цикла
        print(f"i={i}, j={j}")
```

### continue - переход к следующей итерации
```python
# Пропуск четных чисел
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  # Выведет только нечетные: 1, 3, 5, 7, 9

# Обработка только корректных данных
numbers = ["1", "2", "abc", "4", "xyz", "6"]
for num_str in numbers:
    try:
        num = int(num_str)
    except ValueError:
        continue  # Пропускаем некорректные данные
    print(f"Число: {num}")
```

### pass - пустая операция
```python
# Заглушка для будущего кода
for i in range(5):
    if i == 2:
        pass  # TODO: Добавить специальную обработку
    else:
        print(i)

# В условиях
while True:
    user_input = input("Команда: ")
    if user_input == "help":
        pass  # TODO: Показать справку
    elif user_input == "exit":
        break
```

## Практические примеры

### Поиск простых чисел
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Найти все простые числа до 30
primes = []
for num in range(2, 31):
    if is_prime(num):
        primes.append(num)
print(f"Простые числа: {primes}")
```

### Игра "Угадай число"
```python
import random

def guess_number():
    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    
    print("Угадайте число от 1 до 100!")
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"Попытка {attempts + 1}: "))
            attempts += 1
            
            if guess == secret:
                print(f"Поздравляю! Вы угадали за {attempts} попыток!")
                break
            elif guess < secret:
                print("Загаданное число больше")
            else:
                print("Загаданное число меньше")
                
        except ValueError:
            print("Введите корректное число!")
            attempts -= 1  # Не считаем некорректный ввод
    else:
        print(f"Попытки закончились. Загаданное число: {secret}")

guess_number()
```

### Обработка списка с проверками
```python
def process_numbers(numbers):
    result = []
    skipped = 0
    
    for i, num in enumerate(numbers):
        # Пропускаем отрицательные числа
        if num < 0:
            print(f"Пропущено отрицательное число: {num}")
            skipped += 1
            continue
            
        # Останавливаемся на первом числе больше 1000
        if num > 1000:
            print(f"Остановка на числе {num} (позиция {i})")
            break
            
        # Обрабатываем корректные числа
        processed = num ** 2
        result.append(processed)
    
    print(f"Обработано чисел: {len(result)}")
    print(f"Пропущено: {skipped}")
    return result

test_numbers = [1, -2, 3, 4, -5, 6, 1500, 7, 8]
processed = process_numbers(test_numbers)
print(f"Результат: {processed}")
```

### Валидация ввода с повторными попытками
```python
def get_valid_input():
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        try:
            value = int(input("Введите число от 1 до 10: "))
            
            if 1 <= value <= 10:
                return value
            else:
                print("Число должно быть от 1 до 10!")
                
        except ValueError:
            print("Введите корректное число!")
            
        attempts += 1
        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"Осталось попыток: {remaining}")
    
    print("Превышено количество попыток!")
    return None

result = get_valid_input()
if result is not None:
    print(f"Введено число: {result}")
```

## Оптимизация циклов

### Избегание лишних вычислений
```python
# ПЛОХО - вычисляем len() на каждой итерации
numbers = [1, 2, 3, 4, 5]
i = 0
while i < len(numbers):  # len() вызывается каждый раз
    print(numbers[i])
    i += 1

# ХОРОШО - вычисляем len() один раз
numbers = [1, 2, 3, 4, 5]
length = len(numbers)
i = 0
while i < length:
    print(numbers[i])
    i += 1

# ЕЩЕ ЛУЧШЕ - используем for
for num in numbers:
    print(num)
```

### Раннее завершение
```python
# Поиск с ранним завершением
def find_item(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i  # Найдено - выходим сразу
    return -1  # Не найдено

# Проверка условий
def all_positive(numbers):
    for num in numbers:
        if num <= 0:
            return False  # Нашли неположительное - сразу False
    return True
```

## Частые ошибки

1. **Бесконечные циклы**
```python
# ОШИБКА - забыли изменить переменную
count = 0
while count < 5:
    print(count)
    # count += 1  # Забыли это!

# ПРАВИЛЬНО
count = 0
while count < 5:
    print(count)
    count += 1
```

2. **Изменение списка во время итерации**
```python
# ПЛОХО - изменяем список во время итерации
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)  # Может пропустить элементы

# ХОРОШО - создаем новый список
numbers = [1, 2, 3, 4, 5]
odd_numbers = [num for num in numbers if num % 2 != 0]

# ИЛИ итерируем в обратном порядке
numbers = [1, 2, 3, 4, 5]
for i in range(len(numbers) - 1, -1, -1):
    if numbers[i] % 2 == 0:
        numbers.pop(i)
```

3. **Неправильное использование break во вложенных циклах**
```python
# break выходит только из внутреннего цикла
found = False
for i in range(3):
    for j in range(3):
        if i == 1 and j == 1:
            found = True
            break
    if found:
        break  # Выходим и из внешнего цикла
```

## Ключевые моменты для экзамена

- `for` - для итерации по последовательностям
- `while` - для циклов с условием
- `range(start, stop, step)` - генерация последовательности чисел
- `enumerate()` - получение индекса и значения
- `break` - выход из цикла
- `continue` - переход к следующей итерации
- `pass` - пустая операция
- `else` в циклах выполняется при нормальном завершении (без break)
- Избегать изменения списка во время итерации
- Осторожность с бесконечными циклами