# Тема 19: Обработка данных для ИИ систем

## Основные концепции

### Жизненный цикл данных
- **Сбор данных**: Веб-скрепинг, API, базы данных, файлы
- **Очистка данных**: Удаление дубликатов, исправление ошибок
- **Трансформация**: Нормализация, структурирование, форматирование
- **Валидация**: Проверка качества и целостности данных
- **Загрузка**: Подготовка для использования в моделях

### Типы данных для ИИ
```python
# Структурированные данные
import pandas as pd

# CSV данные
df = pd.read_csv('data.csv')
print(df.info())
print(df.describe())

# JSON данные
import json
with open('data.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Базы данных
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql_query("SELECT * FROM table", conn)
```

```python
# Неструктурированные данные
import os
from pathlib import Path

# Текстовые файлы
def process_text_files(directory):
    text_data = []
    for file_path in Path(directory).glob('*.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            text_data.append({
                'filename': file_path.name,
                'content': content,
                'size': len(content)
            })
    return text_data

# Изображения
from PIL import Image
import numpy as np

def process_images(directory):
    images = []
    for img_path in Path(directory).glob('*.{jpg,png,jpeg}'):
        img = Image.open(img_path)
        img_array = np.array(img)
        images.append({
            'filename': img_path.name,
            'size': img.size,
            'mode': img.mode,
            'data': img_array
        })
    return images
```

## Предобработка текстовых данных

### Очистка текста
```python
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def clean_text(text):
    # Приведение к нижнему регистру
    text = text.lower()
    
    # Удаление HTML тегов
    text = re.sub(r'<[^>]+>', '', text)
    
    # Удаление URL
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Удаление специальных символов
    text = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', '', text)
    
    # Удаление лишних пробелов
    text = ' '.join(text.split())
    
    return text

# Пример использования
dirty_text = """
<p>Привет! Это текст с HTML тегами.</p>
Ссылка: https://example.com
Специальные символы: @#$%^&*()
"""

clean_text_result = clean_text(dirty_text)
print(clean_text_result)
```

### Токенизация и нормализация
```python
import spacy
from collections import Counter

# Загрузка модели spaCy
nlp = spacy.load('ru_core_news_sm')

def advanced_text_processing(text):
    doc = nlp(text)
    
    # Извлечение лемм (базовых форм слов)
    lemmas = [token.lemma_ for token in doc 
              if not token.is_stop and not token.is_punct]
    
    # Извлечение именованных сущностей
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Извлечение ключевых слов по частям речи
    keywords = [token.text for token in doc 
                if token.pos_ in ['NOUN', 'ADJ', 'VERB']]
    
    return {
        'lemmas': lemmas,
        'entities': entities,
        'keywords': keywords,
        'word_count': len([token for token in doc if not token.is_space])
    }

# Пример обработки
text = "Компания OpenAI разработала модель GPT-4 в Сан-Франциско."
result = advanced_text_processing(text)
print(result)
```

## Работа с большими объемами данных

### Потоковая обработка
```python
import pandas as pd
from typing import Iterator

def process_large_csv(filename: str, chunk_size: int = 1000) -> Iterator[pd.DataFrame]:
    """Обработка больших CSV файлов по частям"""
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        # Обработка каждого чанка
        processed_chunk = chunk.dropna()  # Удаление пустых значений
        processed_chunk = processed_chunk.drop_duplicates()  # Удаление дубликатов
        yield processed_chunk

# Пример использования
def aggregate_large_file(filename: str):
    total_rows = 0
    unique_values = set()
    
    for chunk in process_large_csv(filename):
        total_rows += len(chunk)
        unique_values.update(chunk['column_name'].unique())
    
    return {
        'total_rows': total_rows,
        'unique_values_count': len(unique_values)
    }
```

### Параллельная обработка
```python
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_single_file(file_path):
    """Функция для обработки одного файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Имитация обработки
            processed = content.upper()
            return {
                'file': file_path,
                'size': len(content),
                'status': 'success'
            }
    except Exception as e:
        return {
            'file': file_path,
            'error': str(e),
            'status': 'error'
        }

def parallel_file_processing(file_paths, max_workers=None):
    """Параллельная обработка файлов"""
    if max_workers is None:
        max_workers = cpu_count()
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Отправка задач на выполнение
        future_to_file = {
            executor.submit(process_single_file, path): path 
            for path in file_paths
        }
        
        # Сбор результатов
        for future in as_completed(future_to_file):
            result = future.result()
            results.append(result)
    
    return results

# Пример использования
file_paths = ['file1.txt', 'file2.txt', 'file3.txt']
results = parallel_file_processing(file_paths)
```

## Валидация и контроль качества данных

### Схемы валидации
```python
from pydantic import BaseModel, validator, ValidationError
from typing import List, Optional
from datetime import datetime

class DataRecord(BaseModel):
    id: int
    title: str
    content: str
    category: str
    created_at: datetime
    tags: List[str]
    score: Optional[float] = None
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @validator('score')
    def score_must_be_valid(cls, v):
        if v is not None and (v < 0 or v > 1):
            raise ValueError('Score must be between 0 and 1')
        return v
    
    @validator('category')
    def category_must_be_valid(cls, v):
        allowed_categories = ['news', 'blog', 'review', 'tutorial']
        if v not in allowed_categories:
            raise ValueError(f'Category must be one of {allowed_categories}')
        return v

# Пример валидации данных
def validate_dataset(data_list):
    validated_data = []
    errors = []
    
    for i, item in enumerate(data_list):
        try:
            validated_record = DataRecord(**item)
            validated_data.append(validated_record.dict())
        except ValidationError as e:
            errors.append({
                'index': i,
                'item': item,
                'errors': e.errors()
            })
    
    return validated_data, errors
```

### Метрики качества данных
```python
import pandas as pd
import numpy as np

class DataQualityAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def completeness_check(self):
        """Проверка полноты данных"""
        total_cells = self.df.size
        missing_cells = self.df.isnull().sum().sum()
        completeness = (total_cells - missing_cells) / total_cells
        
        return {
            'overall_completeness': completeness,
            'column_completeness': (1 - self.df.isnull().sum() / len(self.df)).to_dict()
        }
    
    def uniqueness_check(self):
        """Проверка уникальности данных"""
        duplicate_rows = self.df.duplicated().sum()
        total_rows = len(self.df)
        uniqueness = (total_rows - duplicate_rows) / total_rows
        
        return {
            'row_uniqueness': uniqueness,
            'duplicate_count': duplicate_rows
        }
    
    def consistency_check(self):
        """Проверка согласованности данных"""
        inconsistencies = {}
        
        for column in self.df.select_dtypes(include=[object]).columns:
            # Проверка различных форматов одного значения
            value_counts = self.df[column].value_counts()
            similar_values = []
            
            for value in value_counts.index:
                if isinstance(value, str):
                    similar = [v for v in value_counts.index 
                              if v != value and value.lower() in v.lower()]
                    if similar:
                        similar_values.append({value: similar})
            
            if similar_values:
                inconsistencies[column] = similar_values
        
        return inconsistencies
    
    def generate_report(self):
        """Генерация отчета о качестве данных"""
        report = {
            'dataset_shape': self.df.shape,
            'data_types': self.df.dtypes.to_dict(),
            'completeness': self.completeness_check(),
            'uniqueness': self.uniqueness_check(),
            'consistency': self.consistency_check()
        }
        
        return report

# Пример использования
df = pd.DataFrame({
    'name': ['John', 'Jane', 'john', None, 'Bob'],
    'age': [25, 30, 25, 35, None],
    'city': ['New York', 'Los Angeles', 'NEW YORK', 'Chicago', 'Miami']
})

analyzer = DataQualityAnalyzer(df)
quality_report = analyzer.generate_report()
print(quality_report)
```

## Подготовка данных для машинного обучения

### Кодирование категориальных переменных
```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
import pandas as pd

class MLDataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.one_hot_encoder = None
        self.feature_columns = None
    
    def encode_categorical_features(self, df, categorical_columns, method='onehot'):
        """Кодирование категориальных признаков"""
        df_encoded = df.copy()
        
        if method == 'label':
            for column in categorical_columns:
                le = LabelEncoder()
                df_encoded[column] = le.fit_transform(df[column].astype(str))
                self.label_encoders[column] = le
        
        elif method == 'onehot':
            # One-hot encoding
            encoded_features = pd.get_dummies(
                df[categorical_columns], 
                prefix=categorical_columns
            )
            
            # Удаление исходных категориальных колонок
            df_encoded = df_encoded.drop(columns=categorical_columns)
            
            # Добавление закодированных признаков
            df_encoded = pd.concat([df_encoded, encoded_features], axis=1)
        
        return df_encoded
    
    def normalize_numerical_features(self, df, numerical_columns):
        """Нормализация числовых признаков"""
        from sklearn.preprocessing import StandardScaler
        
        scaler = StandardScaler()
        df_normalized = df.copy()
        df_normalized[numerical_columns] = scaler.fit_transform(df[numerical_columns])
        
        return df_normalized, scaler
    
    def prepare_train_test_split(self, df, target_column, test_size=0.2):
        """Подготовка данных для обучения"""
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        return X_train, X_test, y_train, y_test

# Пример использования
data = {
    'category': ['A', 'B', 'A', 'C', 'B'],
    'size': ['small', 'large', 'medium', 'small', 'large'],
    'price': [100, 200, 150, 80, 220],
    'rating': [4.5, 3.8, 4.2, 4.0, 3.5],
    'popular': [1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)
preprocessor = MLDataPreprocessor()

# Кодирование категориальных признаков
categorical_cols = ['category', 'size']
df_encoded = preprocessor.encode_categorical_features(df, categorical_cols)

# Нормализация числовых признаков
numerical_cols = ['price', 'rating']
df_normalized, scaler = preprocessor.normalize_numerical_features(df_encoded, numerical_cols)

print(df_normalized.head())
```

## Ключевые моменты для экзамена

### Этапы обработки данных
1. **Сбор и извлечение данных** из различных источников
2. **Очистка и предобработка** текстовых и числовых данных
3. **Валидация и контроль качества** с помощью схем и метрик
4. **Трансформация и кодирование** для машинного обучения
5. **Оптимизация производительности** для больших объемов данных

### Практические навыки
- Работа с pandas для структурированных данных
- Использование регулярных выражений для очистки текста
- Применение параллельной обработки для ускорения
- Валидация данных с помощью pydantic
- Подготовка данных для моделей машинного обучения

### Инструменты и библиотеки
- **pandas**: Основная библиотека для работы с данными
- **numpy**: Численные вычисления и массивы
- **scikit-learn**: Предобработка для машинного обучения
- **spacy/nltk**: Обработка естественного языка
- **pydantic**: Валидация данных
- **multiprocessing**: Параллельная обработка

### Метрики качества данных
- **Полнота**: Процент заполненных значений
- **Уникальность**: Отсутствие дубликатов
- **Согласованность**: Единообразие форматов
- **Точность**: Корректность значений
- **Актуальность**: Свежесть данных