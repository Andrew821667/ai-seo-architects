# Функции ввода/вывода данных Python (print(), input())

## print() - вывод данных

### Основы
```python
print("Привет, мир!")  # Простой вывод
print(42)              # Вывод числа
print(3.14)            # Вывод float
```

### Параметры print()
```python
# sep - разделитель между элементами
print("a", "b", "c", sep="-")  # Выводит: a-b-c

# end - что печатать в конце (по умолчанию \n)
print("Первая строка", end=" ")
print("Продолжение")  # Выводит: Первая строка Продолжение

# file - куда выводить (по умолчанию sys.stdout)
with open("output.txt", "w") as f:
    print("Текст в файл", file=f)

# flush - принудительная очистка буфера
print("Сообщение", flush=True)
```

### Форматирование вывода
```python
# f-строки (Python 3.6+)
name = "Анна"
age = 25
print(f"Меня зовут {name}, мне {age} лет")

# .format()
print("Меня зовут {}, мне {} лет".format(name, age))
print("Меня зовут {name}, мне {age} лет".format(name=name, age=age))

# % форматирование (старый способ)
print("Меня зовут %s, мне %d лет" % (name, age))
```

## input() - ввод данных

### Основы
```python
# Всегда возвращает строку!
name = input("Введите ваше имя: ")
print(f"Привет, {name}!")

# Ввод чисел требует преобразования типов
age = int(input("Введите ваш возраст: "))
height = float(input("Введите ваш рост: "))
```

### Обработка ошибок ввода
```python
try:
    number = int(input("Введите число: "))
    print(f"Вы ввели: {number}")
except ValueError:
    print("Это не число!")
```

### Проверка ввода
```python
def get_positive_number():
    while True:
        try:
            num = float(input("Введите положительное число: "))
            if num > 0:
                return num
            else:
                print("Число должно быть положительным!")
        except ValueError:
            print("Введите корректное число!")

number = get_positive_number()
```

## Практические примеры

### Калькулятор
```python
def calculator():
    try:
        a = float(input("Введите первое число: "))
        operation = input("Введите операцию (+, -, *, /): ")
        b = float(input("Введите второе число: "))
        
        if operation == "+":
            result = a + b
        elif operation == "-":
            result = a - b
        elif operation == "*":
            result = a * b
        elif operation == "/":
            if b != 0:
                result = a / b
            else:
                print("Деление на ноль!")
                return
        else:
            print("Неизвестная операция!")
            return
            
        print(f"Результат: {a} {operation} {b} = {result}")
    except ValueError:
        print("Ошибка ввода!")

calculator()
```

### Ввод списка
```python
# Ввод списка чисел через пробел
numbers = list(map(int, input("Введите числа через пробел: ").split()))
print(f"Вы ввели: {numbers}")

# Ввод списка построчно
def input_list():
    items = []
    print("Вводите элементы (пустая строка для завершения):")
    while True:
        item = input()
        if item == "":
            break
        items.append(item)
    return items

my_list = input_list()
print(f"Список: {my_list}")
```

## Частые ошибки

1. **Забывают, что input() возвращает строку**
```python
# НЕПРАВИЛЬНО
age = input("Возраст: ")
if age > 18:  # Ошибка! Сравнение строки с числом

# ПРАВИЛЬНО
age = int(input("Возраст: "))
if age > 18:
    print("Совершеннолетний")
```

2. **Не обрабатывают исключения**
```python
# НЕПРАВИЛЬНО
number = int(input("Число: "))  # Упадет, если ввести не число

# ПРАВИЛЬНО
try:
    number = int(input("Число: "))
except ValueError:
    print("Некорректный ввод!")
```

## Ключевые моменты для экзамена

- `print()` - функция вывода с параметрами sep, end, file, flush
- `input()` - функция ввода, всегда возвращает строку
- f-строки - современный способ форматирования
- Обязательно проверять и обрабатывать пользовательский ввод
- `input()` + преобразование типов для ввода чисел