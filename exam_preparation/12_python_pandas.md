# Библиотека Pandas. Базовые методы

## Введение в Pandas

### Что такое Pandas
```python
# Pandas - библиотека для анализа и обработки данных
# Основные структуры данных: Series (одномерные) и DataFrame (двумерные)

import pandas as pd
import numpy as np

# Проверка версии
print(f"Pandas версия: {pd.__version__}")

# Основные возможности:
# - Чтение и запись данных (CSV, Excel, JSON, SQL)
# - Фильтрация и группировка данных
# - Работа с пропущенными значениями
# - Агрегация и статистика
# - Работа с временными рядами
```

### Установка и импорт
```python
# Установка: pip install pandas
# Обычно импортируется с псевдонимом pd

import pandas as pd
import numpy as np

# Настройки отображения
pd.set_option('display.max_columns', None)  # Показать все колонки
pd.set_option('display.width', None)        # Ширина вывода
pd.set_option('display.max_rows', 20)       # Максимум строк
```

## Series - одномерные данные

### Создание Series
```python
# Из списка
numbers = pd.Series([1, 2, 3, 4, 5])
print(numbers)
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int64

# С пользовательским индексом
grades = pd.Series([85, 92, 78, 94], index=['Анна', 'Петр', 'Мария', 'Иван'])
print(grades)
# Анна     85
# Петр     92
# Мария    78
# Иван     94
# dtype: int64

# Из словаря
population = pd.Series({
    'Москва': 12500000,
    'СПб': 5400000,
    'Новосибирск': 1600000,
    'Екатеринбург': 1500000
})
print(population)

# С явным указанием типа данных
prices = pd.Series([100.5, 200.0, 150.75], dtype='float32')
print(f"Тип данных: {prices.dtype}")
```

### Основные операции с Series
```python
# Доступ к элементам
print(f"Оценка Анны: {grades['Анна']}")           # 85
print(f"Первая оценка: {grades.iloc[0]}")         # 85 (по позиции)
print(f"Несколько оценок: {grades[['Анна', 'Петр']]}")

# Срезы
print(grades['Анна':'Мария'])  # От Анны до Марии включительно
print(grades.iloc[1:3])        # Позиции 1 и 2

# Основные свойства
print(f"Размер: {grades.size}")           # 4
print(f"Форма: {grades.shape}")           # (4,)
print(f"Индекс: {grades.index.tolist()}") # ['Анна', 'Петр', 'Мария', 'Иван']
print(f"Значения: {grades.values}")       # [85 92 78 94]

# Статистика
print(f"Среднее: {grades.mean():.1f}")    # 87.2
print(f"Медиана: {grades.median()}")      # 88.5
print(f"Стандартное отклонение: {grades.std():.1f}")  # 7.0
print(f"Минимум: {grades.min()}")         # 78
print(f"Максимум: {grades.max()}")        # 94
```

### Фильтрация Series
```python
# Логические условия
high_grades = grades[grades > 85]
print("Оценки выше 85:")
print(high_grades)
# Петр    92
# Иван    94

# Множественные условия
good_students = grades[(grades >= 80) & (grades < 95)]
print("Хорошие студенты (80-94):")
print(good_students)

# Использование isin()
selected_students = grades[grades.index.isin(['Анна', 'Иван'])]
print("Выбранные студенты:")
print(selected_students)

# Проверка на пропущенные значения
grades_with_na = pd.Series([85, None, 78, 94], index=['Анна', 'Петр', 'Мария', 'Иван'])
print("Есть пропуски:", grades_with_na.isna().any())
print("Студенты без оценок:", grades_with_na[grades_with_na.isna()].index.tolist())
```

## DataFrame - двумерные данные

### Создание DataFrame
```python
# Из словаря
students_data = {
    'Имя': ['Анна', 'Петр', 'Мария', 'Иван'],
    'Возраст': [20, 22, 19, 21],
    'Оценка': [85, 92, 78, 94],
    'Город': ['Москва', 'СПб', 'Казань', 'Москва']
}

df = pd.DataFrame(students_data)
print(df)
#     Имя  Возраст  Оценка   Город
# 0  Анна       20      85  Москва
# 1  Петр       22      92     СПб
# 2 Мария       19      78  Казань
# 3  Иван       21      94  Москва

# Из списка словарей
students_list = [
    {'Имя': 'Анна', 'Возраст': 20, 'Оценка': 85},
    {'Имя': 'Петр', 'Возраст': 22, 'Оценка': 92},
    {'Имя': 'Мария', 'Возраст': 19, 'Оценка': 78}
]
df2 = pd.DataFrame(students_list)

# Из массива NumPy
data_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df3 = pd.DataFrame(data_array, columns=['A', 'B', 'C'])
print(df3)

# Пустой DataFrame с заданной структурой
empty_df = pd.DataFrame(columns=['Имя', 'Возраст', 'Оценка'])
print(f"Пустой DataFrame:\n{empty_df}")
```

### Основная информация о DataFrame
```python
# Размер и форма
print(f"Форма: {df.shape}")        # (4, 4) - строки x колонки
print(f"Размер: {df.size}")        # 16 элементов
print(f"Строки: {len(df)}")        # 4
print(f"Колонки: {len(df.columns)}")  # 4

# Информация о структуре
print("\nИнформация о DataFrame:")
print(df.info())
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 4 entries, 0 to 3
# Data columns (total 4 columns):
#  #   Column   Non-Null Count  Dtype 
# ---  ------   --------------  ----- 
#  0   Имя      4 non-null      object
#  1   Возраст  4 non-null      int64 
#  2   Оценка   4 non-null      int64 
#  3   Город    4 non-null      object
# dtypes: int64(2), object(2)

# Первые и последние строки
print("\nПервые 3 строки:")
print(df.head(3))

print("\nПоследние 2 строки:")
print(df.tail(2))

# Названия колонок и индекс
print(f"\nКолонки: {df.columns.tolist()}")
print(f"Индекс: {df.index.tolist()}")

# Типы данных
print(f"\nТипы данных:\n{df.dtypes}")
```

### Доступ к данным в DataFrame
```python
# Выбор колонок
names = df['Имя']              # Series
print(type(names))             # <class 'pandas.core.series.Series'>

# Несколько колонок
subset = df[['Имя', 'Оценка']] # DataFrame
print(subset)

# Выбор строк по индексу
first_student = df.iloc[0]     # Первая строка (Series)
first_two = df.iloc[0:2]       # Первые две строки (DataFrame)

# Выбор по условию
moscow_students = df[df['Город'] == 'Москва']
print("Студенты из Москвы:")
print(moscow_students)

# Выбор строк и колонок одновременно
moscow_names = df[df['Город'] == 'Москва']['Имя']
print("Имена студентов из Москвы:")
print(moscow_names.tolist())  # ['Анна', 'Иван']

# loc и iloc
# loc - по меткам
# iloc - по позициям
print(df.loc[0, 'Имя'])        # Анна
print(df.iloc[0, 0])           # Анна

# Диапазоны
print(df.loc[0:2, 'Имя':'Возраст'])  # строки 0-2, колонки от Имя до Возраст
print(df.iloc[0:2, 0:2])              # строки 0-1, колонки 0-1
```

## Работа с данными

### Добавление и изменение данных
```python
# Добавление новой колонки
df['Средний_балл'] = df['Оценка'] / 100 * 5  # Перевод в 5-балльную систему
print(df)

# Добавление на основе условий
df['Статус'] = df['Оценка'].apply(lambda x: 'Отлично' if x >= 90 
                                              else 'Хорошо' if x >= 80 
                                              else 'Удовлетворительно')
print(df[['Имя', 'Оценка', 'Статус']])

# Изменение существующих данных
df.loc[df['Имя'] == 'Анна', 'Возраст'] = 21  # Изменяем возраст Анны
print(f"Новый возраст Анны: {df[df['Имя'] == 'Анна']['Возраст'].iloc[0]}")

# Добавление новой строки
new_student = pd.DataFrame({
    'Имя': ['Ольга'],
    'Возраст': [23],
    'Оценка': [88],
    'Город': ['Казань']
})

# Конкатенация (современный способ)
df = pd.concat([df, new_student], ignore_index=True)
print(f"Теперь студентов: {len(df)}")
```

### Удаление данных
```python
# Удаление колонок
df_without_status = df.drop(['Статус'], axis=1)  # axis=1 для колонок
print("Без колонки Статус:")
print(df_without_status.columns.tolist())

# Удаление строк
df_without_first = df.drop([0], axis=0)  # axis=0 для строк (по умолчанию)
print(f"Без первой строки: {len(df_without_first)} студентов")

# Удаление по условию
df_filtered = df[df['Возраст'] >= 20]  # Оставляем только студентов 20+
print(f"Студенты 20+: {len(df_filtered)}")

# Удаление дубликатов
df_with_duplicates = pd.concat([df, df.iloc[0:1]], ignore_index=True)
print(f"С дубликатами: {len(df_with_duplicates)}")

df_no_duplicates = df_with_duplicates.drop_duplicates()
print(f"Без дубликатов: {len(df_no_duplicates)}")
```

### Сортировка
```python
# Сортировка по одной колонке
df_sorted_by_grade = df.sort_values('Оценка', ascending=False)  # По убыванию
print("Сортировка по оценкам (по убыванию):")
print(df_sorted_by_grade[['Имя', 'Оценка']])

# Сортировка по нескольким колонкам
df_sorted_multi = df.sort_values(['Город', 'Оценка'], ascending=[True, False])
print("\nСортировка по городу, затем по оценке:")
print(df_sorted_multi[['Имя', 'Город', 'Оценка']])

# Сортировка по индексу
df_sorted_by_index = df.sort_index(ascending=True)
print("\nСортировка по индексу:")
print(df_sorted_by_index)

# Получение топ-N
top_students = df.nlargest(2, 'Оценка')  # 2 лучших по оценкам
print("\nТоп-2 студента:")
print(top_students[['Имя', 'Оценка']])
```

## Статистика и агрегация

### Описательная статистика
```python
# Общая статистика для числовых колонок
print("Описательная статистика:")
print(df.describe())
#           Возраст     Оценка  Средний_балл
# count    5.000000   5.000000      5.000000
# mean    21.000000  87.400000      4.370000
# std      1.581139   6.542171      0.327109
# min     19.000000  78.000000      3.900000
# 25%     20.000000  85.000000      4.250000
# 50%     21.000000  88.000000      4.400000
# 75%     22.000000  92.000000      4.600000
# max     23.000000  94.000000      4.700000

# Статистика для конкретной колонки
print(f"\nСтатистика по оценкам:")
print(f"Среднее: {df['Оценка'].mean():.1f}")
print(f"Медиана: {df['Оценка'].median()}")
print(f"Стандартное отклонение: {df['Оценка'].std():.1f}")
print(f"Минимум: {df['Оценка'].min()}")
print(f"Максимум: {df['Оценка'].max()}")

# Подсчет уникальных значений
print(f"\nГорода: {df['Город'].value_counts()}")
# Москва    2
# Казань    2
# СПб       1

# Проверка на пропущенные значения
print(f"\nПропущенные значения:\n{df.isnull().sum()}")
```

### Группировка данных
```python
# Группировка по одной колонке
grouped_by_city = df.groupby('Город')

# Агрегация по группам
city_stats = grouped_by_city.agg({
    'Оценка': ['mean', 'max', 'min', 'count'],
    'Возраст': 'mean'
})
print("Статистика по городам:")
print(city_stats)

# Простая группировка с одной функцией
avg_grade_by_city = df.groupby('Город')['Оценка'].mean()
print("\nСредняя оценка по городам:")
print(avg_grade_by_city)

# Группировка по нескольким колонкам
df['Возрастная_группа'] = df['Возраст'].apply(lambda x: 'Молодые' if x <= 20 else 'Старшие')
multi_group = df.groupby(['Город', 'Возрастная_группа'])['Оценка'].mean()
print("\nСредняя оценка по городам и возрастным группам:")
print(multi_group)

# Применение функции к каждой группе
def group_analysis(group):
    return pd.Series({
        'count': len(group),
        'avg_grade': group['Оценка'].mean(),
        'top_student': group.loc[group['Оценка'].idxmax(), 'Имя']
    })

group_summary = df.groupby('Город').apply(group_analysis)
print("\nАнализ по группам:")
print(group_summary)
```

## Чтение и запись данных

### Работа с CSV файлами
```python
# Сохранение в CSV
df.to_csv('students.csv', index=False, encoding='utf-8')
print("Данные сохранены в students.csv")

# Чтение из CSV
df_from_csv = pd.read_csv('students.csv', encoding='utf-8')
print("Данные загружены из CSV:")
print(df_from_csv.head())

# Чтение с дополнительными параметрами
df_custom = pd.read_csv(
    'students.csv',
    encoding='utf-8',
    sep=',',                    # Разделитель
    header=0,                   # Строка с заголовками
    names=['Name', 'Age', 'Grade', 'City', 'Avg', 'Status', 'AgeGroup'],  # Переименование
    usecols=['Name', 'Age', 'Grade'],  # Только нужные колонки
    dtype={'Age': 'int32', 'Grade': 'float64'}  # Типы данных
)
```

### Работа с Excel
```python
# Сохранение в Excel
df.to_excel('students.xlsx', sheet_name='Студенты', index=False)
print("Данные сохранены в Excel")

# Чтение из Excel
try:
    df_from_excel = pd.read_excel('students.xlsx', sheet_name='Студенты')
    print("Данные загружены из Excel:")
    print(df_from_excel.head())
except ImportError:
    print("Для работы с Excel установите: pip install openpyxl")

# Работа с несколькими листами
# with pd.ExcelWriter('multiple_sheets.xlsx') as writer:
#     df.to_excel(writer, sheet_name='Студенты', index=False)
#     df.groupby('Город').mean().to_excel(writer, sheet_name='Статистика_по_городам')
```

### Работа с JSON
```python
# Сохранение в JSON
df.to_json('students.json', orient='records', force_ascii=False, indent=2)
print("Данные сохранены в JSON")

# Чтение из JSON
df_from_json = pd.read_json('students.json', orient='records')
print("Данные загружены из JSON:")
print(df_from_json.head())

# Различные форматы JSON
print("\nРазличные форматы JSON:")
print("Records:", df.head(2).to_json(orient='records', force_ascii=False))
print("Index:", df.head(2).to_json(orient='index', force_ascii=False))
print("Values:", df.head(2).to_json(orient='values', force_ascii=False))
```

## Обработка пропущенных значений

### Работа с NaN
```python
# Создание DataFrame с пропущенными значениями
data_with_nan = {
    'Имя': ['Анна', 'Петр', 'Мария', 'Иван', 'Ольга'],
    'Возраст': [20, 22, None, 21, 23],
    'Оценка': [85, None, 78, 94, 88],
    'Город': ['Москва', 'СПб', 'Казань', None, 'Казань']
}

df_nan = pd.DataFrame(data_with_nan)
print("DataFrame с пропущенными значениями:")
print(df_nan)

# Проверка пропущенных значений
print(f"\nПропущенные значения по колонкам:\n{df_nan.isnull().sum()}")
print(f"\nВсего пропущенных значений: {df_nan.isnull().sum().sum()}")
print(f"\nСтроки с пропусками:\n{df_nan[df_nan.isnull().any(axis=1)]}")

# Удаление строк с пропусками
df_dropped_rows = df_nan.dropna()  # Удаляет строки с любыми пропусками
print(f"\nПосле удаления строк с пропусками: {len(df_dropped_rows)} строк")

df_dropped_cols = df_nan.dropna(axis=1)  # Удаляет колонки с пропусками
print(f"После удаления колонок с пропусками: {len(df_dropped_cols.columns)} колонок")

# Заполнение пропущенных значений
df_filled = df_nan.copy()

# Заполнение константами
df_filled['Город'].fillna('Неизвестно', inplace=True)

# Заполнение средними значениями
df_filled['Возраст'].fillna(df_filled['Возраст'].mean(), inplace=True)
df_filled['Оценка'].fillna(df_filled['Оценка'].median(), inplace=True)

print("\nПосле заполнения пропусков:")
print(df_filled)
```

### Интерполяция и forward/backward fill
```python
# Создание временного ряда с пропусками
dates = pd.date_range('2024-01-01', periods=10, freq='D')
ts_data = pd.Series([10, 12, None, None, 18, 20, None, 25, 27, 30], index=dates)

print("Временной ряд с пропусками:")
print(ts_data)

# Forward fill (заполнение предыдущим значением)
ts_ffill = ts_data.fillna(method='ffill')
print("\nForward fill:")
print(ts_ffill)

# Backward fill (заполнение следующим значением)
ts_bfill = ts_data.fillna(method='bfill')
print("\nBackward fill:")
print(ts_bfill)

# Линейная интерполяция
ts_interpolated = ts_data.interpolate(method='linear')
print("\nЛинейная интерполяция:")
print(ts_interpolated)
```

## Объединение данных

### Concatenation (конкатенация)
```python
# Создание дополнительных данных
new_students = pd.DataFrame({
    'Имя': ['Елена', 'Дмитрий'],
    'Возраст': [24, 25],
    'Оценка': [89, 91],
    'Город': ['Москва', 'СПб']
})

# Вертикальная конкатенация (добавление строк)
df_combined = pd.concat([df.iloc[:3], new_students], ignore_index=True)
print("Объединенные данные:")
print(df_combined)

# Горизонтальная конкатенация (добавление колонок)
additional_info = pd.DataFrame({
    'Специальность': ['ИТ', 'Экономика', 'Математика'],
    'Курс': [2, 3, 1]
})

df_horizontal = pd.concat([df.iloc[:3], additional_info], axis=1)
print("\nГоризонтальное объединение:")
print(df_horizontal)
```

### Merge (слияние)
```python
# Создание связанных таблиц
students_grades = pd.DataFrame({
    'student_id': [1, 2, 3, 4],
    'Имя': ['Анна', 'Петр', 'Мария', 'Иван'],
    'Возраст': [20, 22, 19, 21]
})

courses_grades = pd.DataFrame({
    'student_id': [1, 1, 2, 2, 3, 4, 4],
    'Предмет': ['Математика', 'Физика', 'Математика', 'Химия', 'Физика', 'Математика', 'Информатика'],
    'Оценка': [85, 90, 92, 88, 78, 94, 96]
})

# Inner join (внутреннее соединение)
inner_merged = pd.merge(students_grades, courses_grades, on='student_id')
print("Inner join:")
print(inner_merged)

# Left join (левое соединение)
all_students = pd.DataFrame({
    'student_id': [1, 2, 3, 4, 5],
    'Имя': ['Анна', 'Петр', 'Мария', 'Иван', 'Ольга']
})

left_merged = pd.merge(all_students, courses_grades, on='student_id', how='left')
print("\nLeft join (все студенты, даже без оценок):")
print(left_merged)

# Группировка после слияния
student_performance = inner_merged.groupby(['student_id', 'Имя']).agg({
    'Оценка': ['mean', 'count']
}).round(1)
print("\nУспеваемость студентов:")
print(student_performance)
```

## Применение функций

### Apply метод
```python
# Применение функции к колонке
df['Возраст_категория'] = df['Возраст'].apply(
    lambda x: 'Молодой' if x <= 20 else 'Средний' if x <= 22 else 'Старший'
)

# Применение функции к нескольким колонкам
def categorize_student(row):
    if row['Оценка'] >= 90 and row['Возраст'] <= 21:
        return 'Талантливый молодой'
    elif row['Оценка'] >= 85:
        return 'Хороший студент'
    else:
        return 'Обычный студент'

df['Категория'] = df.apply(categorize_student, axis=1)
print("Категоризация студентов:")
print(df[['Имя', 'Возраст', 'Оценка', 'Категория']])

# Применение функции к каждому элементу (applymap) - только для DataFrame
numeric_df = df[['Возраст', 'Оценка']].copy()
normalized_df = numeric_df.applymap(lambda x: round(x / numeric_df.max().max(), 3))
print("\nНормализованные данные:")
print(normalized_df)
```

### Map метод
```python
# Создание маппинга
city_mapping = {
    'Москва': 'Центр',
    'СПб': 'Северо-Запад', 
    'Казань': 'Поволжье',
    'Екатеринбург': 'Урал'
}

df['Регион'] = df['Город'].map(city_mapping)
print("Маппинг городов на регионы:")
print(df[['Город', 'Регион']])

# Обработка отсутствующих значений в маппинге
df['Регион'] = df['Город'].map(city_mapping).fillna('Другой')
```

## Временные ряды

### Работа с датами
```python
# Создание DataFrame с датами
date_range = pd.date_range('2024-01-01', periods=30, freq='D')
sales_data = pd.DataFrame({
    'Дата': date_range,
    'Продажи': np.random.randint(100, 1000, 30),
    'Расходы': np.random.randint(50, 500, 30)
})

# Установка даты как индекса
sales_data.set_index('Дата', inplace=True)
print("Данные продаж:")
print(sales_data.head())

# Извлечение компонентов даты
sales_data['Год'] = sales_data.index.year
sales_data['Месяц'] = sales_data.index.month
sales_data['День_недели'] = sales_data.index.day_name()

print("\nКомпоненты даты:")
print(sales_data[['Продажи', 'Год', 'Месяц', 'День_недели']].head())

# Группировка по времени
weekly_sales = sales_data['Продажи'].resample('W').sum()  # По неделям
print("\nПродажи по неделям:")
print(weekly_sales)

# Скользящее среднее
sales_data['MA_7'] = sales_data['Продажи'].rolling(window=7).mean()
print("\n7-дневное скользящее среднее:")
print(sales_data[['Продажи', 'MA_7']].tail())
```

### Фильтрация по времени
```python
# Фильтрация по диапазону дат
january_sales = sales_data['2024-01-01':'2024-01-15']
print(f"Продажи за первую половину января: {len(january_sales)} дней")

# Фильтрация по дням недели
weekend_sales = sales_data[sales_data['День_недели'].isin(['Saturday', 'Sunday'])]
print(f"Продажи в выходные: средние {weekend_sales['Продажи'].mean():.0f}")

# Сравнение периодов
first_half = sales_data['2024-01-01':'2024-01-15']['Продажи'].sum()
second_half = sales_data['2024-01-16':'2024-01-31']['Продажи'].sum()
print(f"Первая половина месяца: {first_half}")
print(f"Вторая половина месяца: {second_half}")
```

## Практические примеры

### Анализ успеваемости
```python
# Создание более сложного датасета
students_extended = pd.DataFrame({
    'Имя': ['Анна', 'Петр', 'Мария', 'Иван', 'Ольга', 'Сергей', 'Елена'],
    'Группа': ['ИТ-1', 'ИТ-1', 'ИТ-2', 'ИТ-1', 'ИТ-2', 'ИТ-2', 'ИТ-1'],
    'Математика': [85, 92, 78, 94, 88, 76, 89],
    'Физика': [82, 88, 80, 91, 85, 74, 87],
    'Информатика': [90, 95, 75, 97, 92, 72, 91],
    'Семестр': [1, 1, 1, 1, 2, 2, 2]
})

print("Расширенные данные о студентах:")
print(students_extended)

# Анализ по группам
group_analysis = students_extended.groupby('Группа').agg({
    'Математика': ['mean', 'std'],
    'Физика': ['mean', 'std'], 
    'Информатика': ['mean', 'std']
}).round(1)

print("\nАнализ по группам:")
print(group_analysis)

# Преобразование в длинный формат для анализа
subjects_melted = pd.melt(
    students_extended, 
    id_vars=['Имя', 'Группа', 'Семестр'],
    value_vars=['Математика', 'Физика', 'Информатика'],
    var_name='Предмет',
    value_name='Оценка'
)

print("\nДанные в длинном формате:")
print(subjects_melted.head(10))

# Анализ по предметам
subject_stats = subjects_melted.groupby('Предмет')['Оценка'].agg([
    'count', 'mean', 'std', 'min', 'max'
]).round(1)

print("\nСтатистика по предметам:")
print(subject_stats)
```

### Анализ продаж
```python
# Создание данных о продажах
products_sales = pd.DataFrame({
    'Продукт': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 'Mouse', 'Keyboard'],
    'Категория': ['Компьютеры', 'Аксессуары', 'Аксессуары', 'Компьютеры', 'Компьютеры', 'Аксессуары', 'Аксессуары'],
    'Цена': [50000, 1500, 3000, 25000, 55000, 1200, 2800],
    'Количество': [2, 10, 5, 3, 1, 15, 8],
    'Дата': pd.to_datetime(['2024-01-15', '2024-01-16', '2024-01-16', '2024-01-17', 
                           '2024-01-18', '2024-01-18', '2024-01-19'])
})

# Расчет выручки
products_sales['Выручка'] = products_sales['Цена'] * products_sales['Количество']

print("Данные о продажах:")
print(products_sales)

# Анализ по категориям
category_analysis = products_sales.groupby('Категория').agg({
    'Выручка': ['sum', 'mean'],
    'Количество': 'sum',
    'Продукт': 'count'  # Количество транзакций
}).round(0)

category_analysis.columns = ['Общая_выручка', 'Средняя_выручка', 'Общее_количество', 'Транзакций']
print("\nАнализ по категориям:")
print(category_analysis)

# Топ продуктов
top_products = products_sales.groupby('Продукт')['Выручка'].sum().sort_values(ascending=False)
print("\nТоп продуктов по выручке:")
print(top_products)

# Динамика продаж по дням
daily_sales = products_sales.groupby('Дата')['Выручка'].sum()
print("\nДинамика продаж по дням:")
print(daily_sales)
```

## Полезные методы и функции

### Часто используемые методы
```python
# Создание сводной таблицы
pivot_table = students_extended.pivot_table(
    values=['Математика', 'Физика', 'Информатика'],
    index='Группа',
    columns='Семестр',
    aggfunc='mean'
).round(1)

print("Сводная таблица оценок:")
print(pivot_table)

# Ранжирование
students_extended['Ранг_математика'] = students_extended['Математика'].rank(ascending=False)
students_extended['Ранг_общий'] = students_extended[['Математика', 'Физика', 'Информатика']].mean(axis=1).rank(ascending=False)

print("\nРанжирование студентов:")
print(students_extended[['Имя', 'Математика', 'Ранг_математика', 'Ранг_общий']])

# Квантили
print("\nКвантили оценок по математике:")
quantiles = students_extended['Математика'].quantile([0.25, 0.5, 0.75])
print(quantiles)

# Корреляция
correlation_matrix = students_extended[['Математика', 'Физика', 'Информатика']].corr()
print("\nКорреляция между предметами:")
print(correlation_matrix.round(3))
```

### Работа со строками
```python
# Создание данных с текстом
text_data = pd.DataFrame({
    'Имя_Фамилия': ['Анна Иванова', 'Петр Петров', 'Мария Сидорова'],
    'Email': ['anna.ivanova@email.com', 'PETER.PETROV@EMAIL.COM', 'maria.sidorova@email.com'],
    'Телефон': ['+7-123-456-78-90', '8(987)654-32-10', '+7 800 555 35 35']
})

# Разделение строк
text_data[['Имя', 'Фамилия']] = text_data['Имя_Фамилия'].str.split(' ', expand=True)

# Преобразование регистра
text_data['Email_lower'] = text_data['Email'].str.lower()
text_data['Имя_upper'] = text_data['Имя'].str.upper()

# Извлечение информации
text_data['Домен'] = text_data['Email'].str.extract(r'@(.+\.com)', expand=False)

# Замена и очистка
text_data['Телефон_clean'] = text_data['Телефон'].str.replace(r'[^\d]', '', regex=True)

print("Обработка текстовых данных:")
print(text_data[['Имя', 'Фамилия', 'Email_lower', 'Домен', 'Телефон_clean']])

# Проверка на содержание
gmail_users = text_data[text_data['Email'].str.contains('gmail', case=False)]
print(f"\nПользователи Gmail: {len(gmail_users)}")
```

## Оптимизация и производительность

### Эффективные операции
```python
# Создание большого датасета для демонстрации
import time

large_df = pd.DataFrame({
    'A': np.random.randint(1, 100, 100000),
    'B': np.random.randn(100000),
    'C': np.random.choice(['X', 'Y', 'Z'], 100000)
})

# Сравнение производительности

# МЕДЛЕННО - iterrows()
start_time = time.time()
result_slow = []
for index, row in large_df.head(1000).iterrows():
    result_slow.append(row['A'] * row['B'])
slow_time = time.time() - start_time

# БЫСТРО - векторизация
start_time = time.time()
result_fast = large_df.head(1000)['A'] * large_df.head(1000)['B']
fast_time = time.time() - start_time

print(f"Iterrows: {slow_time:.4f}с")
print(f"Векторизация: {fast_time:.4f}с")
print(f"Ускорение: {slow_time/fast_time:.1f}x")

# Эффективная фильтрация
# Используйте query() для сложных условий
filtered_query = large_df.query('A > 50 and C == "X"')
filtered_boolean = large_df[(large_df['A'] > 50) & (large_df['C'] == 'X')]

print(f"\nРезультаты фильтрации одинаковы: {filtered_query.equals(filtered_boolean)}")
```

### Управление памятью
```python
# Информация о памяти
print(f"Размер DataFrame в памяти: {large_df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

# Оптимизация типов данных
large_df['A'] = large_df['A'].astype('int8')  # Вместо int64
large_df['C'] = large_df['C'].astype('category')  # Категориальный тип

print(f"Размер после оптимизации: {large_df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

# Чтение больших файлов по частям
# for chunk in pd.read_csv('large_file.csv', chunksize=10000):
#     processed_chunk = chunk.groupby('column').mean()
#     # Обработка каждого куска отдельно
```

## Частые ошибки и их решения

### Распространенные проблемы
```python
# 1. Проблема с индексами при фильтрации
df_sample = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [10, 20, 30, 40, 50]})
filtered = df_sample[df_sample['A'] > 2]

print("Индексы после фильтрации:", filtered.index.tolist())  # [2, 3, 4]

# Сброс индекса
filtered_reset = filtered.reset_index(drop=True)
print("Индексы после сброса:", filtered_reset.index.tolist())  # [0, 1, 2]

# 2. Проблема с копированием vs представлением
df_sample = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Создание копии
df_copy = df_sample.copy()
df_copy.loc[0, 'A'] = 999
print("Оригинал не изменился:", df_sample.loc[0, 'A'])  # 1

# 3. Проблема с типами данных
mixed_data = pd.DataFrame({'numbers': ['1', '2', '3', 'text']})
print("Тип до преобразования:", mixed_data['numbers'].dtype)  # object

# Безопасное преобразование
mixed_data['numbers_numeric'] = pd.to_numeric(mixed_data['numbers'], errors='coerce')
print("После преобразования:", mixed_data['numbers_numeric'].dtype)  # float64
print("С ошибками:", mixed_data['numbers_numeric'].isna().sum())  # 1
```

## Ключевые моменты для экзамена

- **Series и DataFrame** - основные структуры данных Pandas
- **Индексация** - `.loc[]` (по меткам), `.iloc[]` (по позициям)
- **Фильтрация** - логические условия с `&` и `|` операторами
- **Группировка** - `groupby()` с функциями агрегации
- **Чтение/запись** - `read_csv()`, `to_csv()`, `read_excel()`, `to_json()`
- **Пропущенные значения** - `isna()`, `fillna()`, `dropna()`
- **Объединение** - `concat()`, `merge()` для соединения данных
- **Применение функций** - `apply()`, `map()`, `applymap()`
- **Статистика** - `describe()`, `mean()`, `std()`, `value_counts()`
- **Временные ряды** - работа с датами, `resample()`, `rolling()`