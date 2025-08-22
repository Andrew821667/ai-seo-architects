# Сплитеры и их отличия

## Что такое сплитеры (Text Splitters)

### Определение и назначение
```python
# Сплитеры - инструменты для разбиения длинного текста на части (chunks)
# Используются для:
# 1. Обхода ограничений контекста LLM
# 2. Создания векторных эмбеддингов
# 3. Улучшения качества поиска в RAG системах
# 4. Оптимизации обработки больших документов

# Основные принципы:
# - Сохранение смыслового единства
# - Минимизация потери контекста
# - Оптимальный размер частей
# - Перекрытие между частями
```

### Основные параметры сплитеров
```python
# Ключевые параметры всех сплитеров:

chunk_size = 1000        # Максимальный размер части (в символах/токенах)
chunk_overlap = 200      # Перекрытие между частями
length_function = len    # Функция измерения длины
separators = ["\n\n", "\n", " ", ""]  # Разделители по приоритету

# Пример базовой структуры:
class BaseSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text):
        """Базовый метод разбиения текста"""
        chunks = []
        # Логика разбиения...
        return chunks
```

## Типы сплитеров

### 1. Character Text Splitter (Посимвольный)
```python
from langchain.text_splitter import CharacterTextSplitter

# Простейший сплитер - делит по символам
character_splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separator="\n\n"  # Основной разделитель
)

# Пример текста
long_text = """
Искусственный интеллект представляет собой область информатики, 
которая занимается созданием интеллектуальных машин.

Машинное обучение является подмножеством ИИ, которое фокусируется 
на создании алгоритмов, способных обучаться на данных.

Глубокое обучение - это подмножество машинного обучения, 
использующее нейронные сети с множественными слоями.
"""

# Разбиение
chunks = character_splitter.split_text(long_text)
print(f"Количество частей: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"Часть {i+1}: {len(chunk)} символов")
    print(f"Содержимое: {chunk[:100]}...")
    print()
```

### 2. Recursive Character Text Splitter (Рекурсивный)
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Самый популярный сплитер - пытается сохранить структуру
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]  # Приоритет разделителей
)

# Пример с различными структурами
structured_text = """
# Глава 1: Введение в ИИ

Искусственный интеллект - это важная область.

## Подраздел 1.1: История

ИИ начался в 1950-х годах. Алан Тьюринг предложил тест Тьюринга.

## Подраздел 1.2: Современность

Сегодня ИИ используется повсеместно:
- В поисковых системах
- В рекомендательных системах  
- В автономных автомобилях
- В медицинской диагностике

# Глава 2: Машинное обучение

Машинное обучение позволяет компьютерам учиться без явного программирования.
"""

chunks = recursive_splitter.split_text(structured_text)
print("Рекурсивное разбиение:")
for i, chunk in enumerate(chunks):
    print(f"Часть {i+1} ({len(chunk)} символов):")
    print(chunk)
    print("-" * 50)
```

### 3. Token-based Splitter (На основе токенов)
```python
# Для точного подсчета токенов (важно для API ограничений)
import tiktoken

class TokenTextSplitter:
    def __init__(self, model_name="gpt-3.5-turbo", chunk_size=500, chunk_overlap=100):
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def count_tokens(self, text):
        """Подсчет количества токенов"""
        return len(self.encoding.encode(text))
    
    def split_text(self, text):
        """Разбиение по токенам"""
        # Кодируем весь текст
        tokens = self.encoding.encode(text)
        chunks = []
        
        start = 0
        while start < len(tokens):
            # Определяем конец текущего куска
            end = min(start + self.chunk_size, len(tokens))
            
            # Декодируем токены обратно в текст
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            # Учитываем перекрытие
            start = end - self.chunk_overlap
            if start <= 0:
                start = end
        
        return chunks

# Использование
token_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
token_chunks = token_splitter.split_text(long_text)

print("Разбиение по токенам:")
for i, chunk in enumerate(token_chunks):
    token_count = token_splitter.count_tokens(chunk)
    print(f"Часть {i+1}: {token_count} токенов")
    print(f"Содержимое: {chunk}")
    print()
```

### 4. Sentence Splitter (По предложениям)
```python
import re

class SentenceSplitter:
    def __init__(self, chunk_size=3, chunk_overlap=1):
        self.chunk_size = chunk_size  # Количество предложений
        self.chunk_overlap = chunk_overlap
    
    def split_into_sentences(self, text):
        """Разбиение на предложения"""
        # Простой regex для разделения предложений
        sentence_pattern = r'(?<=[.!?])\s+'
        sentences = re.split(sentence_pattern, text.strip())
        return [s.strip() for s in sentences if s.strip()]
    
    def split_text(self, text):
        """Разбиение по группам предложений"""
        sentences = self.split_into_sentences(text)
        chunks = []
        
        start = 0
        while start < len(sentences):
            end = min(start + self.chunk_size, len(sentences))
            chunk_sentences = sentences[start:end]
            chunk = " ".join(chunk_sentences)
            chunks.append(chunk)
            
            # Учитываем перекрытие
            start = end - self.chunk_overlap
            if start <= 0:
                start = end
        
        return chunks

# Пример использования
sentence_text = """
Машинное обучение - это метод анализа данных. Оно автоматизирует построение аналитических моделей. 
Это ветвь искусственного интеллекта. МО основано на идее, что системы могут учиться на данных. 
Они могут выявлять закономерности и принимать решения. При этом требуется минимальное вмешательство человека.
"""

sentence_splitter = SentenceSplitter(chunk_size=2, chunk_overlap=1)
sentence_chunks = sentence_splitter.split_text(sentence_text)

print("Разбиение по предложениям:")
for i, chunk in enumerate(sentence_chunks):
    print(f"Часть {i+1}: {chunk}")
    print()
```

## Специализированные сплитеры

### 1. Markdown Splitter
```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

# Для разбиения Markdown документов с сохранением структуры
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
)

markdown_text = """
# Введение в Data Science

Data Science объединяет статистику, программирование и знание предметной области.

## Основные этапы

### 1. Сбор данных
Первый этап - получение релевантных данных из различных источников.

### 2. Очистка данных
Данные часто содержат ошибки, пропуски и несоответствия.

## Инструменты

### Python
Основной язык для Data Science с богатой экосистемой библиотек.

### R
Специализированный язык для статистического анализа.

# Заключение

Data Science - быстро развивающаяся область с большими возможностями.
"""

md_chunks = markdown_splitter.split_text(markdown_text)
print("Разбиение Markdown:")
for chunk in md_chunks:
    print(f"Заголовок: {chunk.metadata}")
    print(f"Содержимое: {chunk.page_content}")
    print("-" * 50)
```

### 2. Code Splitter
```python
from langchain.text_splitter import PythonCodeTextSplitter

# Специально для кода - сохраняет синтаксическую структуру
code_splitter = PythonCodeTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

python_code = """
import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
    
    def load_data(self):
        \"\"\"Загрузка данных из файла\"\"\"
        try:
            self.data = pd.read_csv(self.data_path)
            print(f"Загружено {len(self.data)} строк")
        except FileNotFoundError:
            print("Файл не найден")
            return False
        return True
    
    def clean_data(self):
        \"\"\"Очистка данных\"\"\"
        if self.data is None:
            return False
        
        # Удаление пропусков
        initial_rows = len(self.data)
        self.data = self.data.dropna()
        removed_rows = initial_rows - len(self.data)
        
        print(f"Удалено {removed_rows} строк с пропусками")
        return True
    
    def analyze(self):
        \"\"\"Базовый анализ данных\"\"\"
        if self.data is None:
            return None
        
        return {
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'memory_usage': self.data.memory_usage(deep=True).sum()
        }

# Использование класса
processor = DataProcessor("data.csv")
if processor.load_data():
    processor.clean_data()
    stats = processor.analyze()
    print(stats)
"""

code_chunks = code_splitter.split_text(python_code)
print("Разбиение кода:")
for i, chunk in enumerate(code_chunks):
    print(f"Часть {i+1}:")
    print(chunk)
    print("-" * 50)
```

### 3. HTML/XML Splitter
```python
from bs4 import BeautifulSoup
import re

class HTMLSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_html(self, html):
        """Извлечение текста из HTML с сохранением структуры"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Удаляем скрипты и стили
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Извлекаем текст с разделителями
        text_parts = []
        
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'li']):
            if element.get_text(strip=True):
                text_parts.append(element.get_text(strip=True))
        
        return '\n\n'.join(text_parts)
    
    def split_html(self, html):
        """Разбиение HTML документа"""
        text = self.extract_text_from_html(html)
        
        # Используем рекурсивный сплитер для текста
        recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        return recursive_splitter.split_text(text)

# Пример HTML
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Машинное обучение</title>
</head>
<body>
    <h1>Введение в машинное обучение</h1>
    <p>Машинное обучение - это подраздел искусственного интеллекта, 
    который фокусируется на разработке алгоритмов и статистических моделей.</p>
    
    <h2>Типы машинного обучения</h2>
    
    <h3>Обучение с учителем</h3>
    <p>Алгоритм обучается на размеченных данных, где известны правильные ответы.</p>
    <ul>
        <li>Классификация - предсказание категорий</li>
        <li>Регрессия - предсказание числовых значений</li>
    </ul>
    
    <h3>Обучение без учителя</h3>
    <p>Алгоритм ищет скрытые закономерности в данных без размеченных примеров.</p>
    
    <script>console.log("Этот скрипт будет удален");</script>
</body>
</html>
"""

html_splitter = HTMLSplitter(chunk_size=400, chunk_overlap=50)
html_chunks = html_splitter.split_html(html_content)

print("Разбиение HTML:")
for i, chunk in enumerate(html_chunks):
    print(f"Часть {i+1}:")
    print(chunk)
    print("-" * 50)
```

## Выбор оптимального сплитера

### Сравнение сплитеров
```python
def compare_splitters(text, chunk_size=500):
    """Сравнение разных сплитеров на одном тексте"""
    
    splitters = {
        "Character": CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100),
        "Recursive": RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100),
        "Sentence": SentenceSplitter(chunk_size=3, chunk_overlap=1),
        "Token": TokenTextSplitter(chunk_size=chunk_size//4, chunk_overlap=25)  # Примерно 4 символа = 1 токен
    }
    
    results = {}
    
    for name, splitter in splitters.items():
        try:
            if name == "Token":
                chunks = splitter.split_text(text)
                token_counts = [splitter.count_tokens(chunk) for chunk in chunks]
                results[name] = {
                    "chunks_count": len(chunks),
                    "avg_length": sum(len(chunk) for chunk in chunks) / len(chunks),
                    "avg_tokens": sum(token_counts) / len(token_counts) if token_counts else 0,
                    "chunks": chunks[:2]  # Первые 2 для примера
                }
            else:
                chunks = splitter.split_text(text)
                results[name] = {
                    "chunks_count": len(chunks),
                    "avg_length": sum(len(chunk) for chunk in chunks) / len(chunks),
                    "chunks": chunks[:2]  # Первые 2 для примера
                }
        except Exception as e:
            results[name] = {"error": str(e)}
    
    return results

# Тестовый текст
test_text = """
Глубокое обучение - это подмножество машинного обучения в искусственном интеллекте. 
Оно имеет сети, способные к обучению без учителя на данных, которые являются неструктурированными или немаркированными.

Также известное как глубокое структурированное обучение, оно является частью более широкого семейства методов машинного обучения. 
Обучение может быть контролируемым, полуконтролируемым или неконтролируемым.

Архитектуры глубокого обучения, такие как глубокие нейронные сети, глубокие сети доверия, глубокие сети доверия, 
рекуррентные нейронные сети и сверточные нейронные сети, были применены к таким областям, как компьютерное зрение, 
распознавание речи, обработка естественного языка, машинный перевод, биоинформатика и разработка лекарств.
"""

comparison = compare_splitters(test_text)

print("Сравнение сплитеров:")
print("=" * 60)
for name, results in comparison.items():
    if "error" in results:
        print(f"{name}: Ошибка - {results['error']}")
        continue
    
    print(f"\n{name}:")
    print(f"  Количество частей: {results['chunks_count']}")
    print(f"  Средняя длина: {results['avg_length']:.0f} символов")
    if "avg_tokens" in results:
        print(f"  Средняя длина: {results['avg_tokens']:.0f} токенов")
    
    print(f"  Первая часть: {results['chunks'][0][:100]}...")
```

### Рекомендации по выбору
```python
def recommend_splitter(content_type, use_case, document_length):
    """Рекомендации по выбору сплитера"""
    
    recommendations = {
        "general_text": {
            "small": "CharacterTextSplitter - простой и быстрый",
            "medium": "RecursiveCharacterTextSplitter - сохраняет структуру",
            "large": "RecursiveCharacterTextSplitter с большими chunks"
        },
        "code": {
            "any": "PythonCodeTextSplitter или language-specific splitter"
        },
        "markdown": {
            "any": "MarkdownHeaderTextSplitter - сохраняет заголовки"
        },
        "html": {
            "any": "HTMLSplitter - извлекает чистый текст"
        },
        "academic": {
            "any": "SentenceSplitter - сохраняет смысловые единицы"
        },
        "api_usage": {
            "any": "TokenTextSplitter - точный контроль токенов"
        }
    }
    
    size_category = (
        "small" if document_length < 5000 
        else "medium" if document_length < 50000 
        else "large"
    )
    
    if content_type in recommendations:
        if size_category in recommendations[content_type]:
            return recommendations[content_type][size_category]
        else:
            return recommendations[content_type]["any"]
    
    return recommendations["general_text"][size_category]

# Примеры рекомендаций
test_cases = [
    ("general_text", "rag_system", 3000),
    ("code", "documentation", 10000),
    ("markdown", "wiki", 25000),
    ("api_usage", "chatbot", 15000)
]

print("Рекомендации по выбору сплитера:")
for content_type, use_case, length in test_cases:
    recommendation = recommend_splitter(content_type, use_case, length)
    print(f"{content_type} ({use_case}, {length} символов): {recommendation}")
```

## Продвинутые техники

### Семантический сплитер
```python
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSplitter:
    def __init__(self, model_name='all-MiniLM-L6-v2', similarity_threshold=0.7):
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = similarity_threshold
    
    def split_by_semantic_similarity(self, text):
        """Разбиение на основе семантического сходства"""
        # Разбиваем на предложения
        sentence_splitter = SentenceSplitter(chunk_size=1, chunk_overlap=0)
        sentences = sentence_splitter.split_into_sentences(text)
        
        if len(sentences) <= 1:
            return [text]
        
        # Получаем эмбеддинги для каждого предложения
        embeddings = self.model.encode(sentences)
        
        # Находим точки разрыва на основе семантического сходства
        chunks = []
        current_chunk = [sentences[0]]
        
        for i in range(1, len(sentences)):
            # Вычисляем сходство с предыдущим предложением
            similarity = cosine_similarity(
                embeddings[i-1].reshape(1, -1),
                embeddings[i].reshape(1, -1)
            )[0][0]
            
            if similarity >= self.similarity_threshold:
                # Высокое сходство - добавляем к текущему куску
                current_chunk.append(sentences[i])
            else:
                # Низкое сходство - начинаем новый кусок
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentences[i]]
        
        # Добавляем последний кусок
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

# Пример с разнородным текстом
mixed_text = """
Машинное обучение использует алгоритмы для анализа данных. Эти алгоритмы могут выявлять закономерности в больших наборах данных.

Вчера я ходил в магазин за продуктами. Купил хлеб, молоко и яйца для завтрака.

Нейронные сети - это основа глубокого обучения. Они состоят из множества связанных узлов, имитирующих работу мозга.

Моя кошка очень любит спать на солнце. Она может лежать у окна часами, греясь в лучах.

Искусственный интеллект развивается быстрыми темпами. Каждый год появляются новые прорывы в этой области.
"""

try:
    semantic_splitter = SemanticSplitter(similarity_threshold=0.5)
    semantic_chunks = semantic_splitter.split_by_semantic_similarity(mixed_text)
    
    print("Семантическое разбиение:")
    for i, chunk in enumerate(semantic_chunks):
        print(f"Семантический блок {i+1}:")
        print(chunk)
        print("-" * 50)
except ImportError:
    print("Для семантического сплитера установите: pip install sentence-transformers")
```

### Адаптивный сплитер
```python
class AdaptiveSplitter:
    def __init__(self, min_chunk_size=200, max_chunk_size=1000, overlap=100):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def analyze_text_structure(self, text):
        """Анализ структуры текста для выбора стратегии"""
        structure_info = {
            "has_headers": bool(re.search(r'^#{1,6}\s', text, re.MULTILINE)),
            "has_code": bool(re.search(r'```|`\w+`|def\s+\w+\(', text)),
            "has_lists": bool(re.search(r'^\s*[-*+]\s|^\s*\d+\.\s', text, re.MULTILINE)),
            "paragraph_count": len(re.findall(r'\n\n+', text)) + 1,
            "avg_paragraph_length": len(text) // (len(re.findall(r'\n\n+', text)) + 1)
        }
        return structure_info
    
    def adaptive_split(self, text):
        """Адаптивное разбиение на основе структуры"""
        structure = self.analyze_text_structure(text)
        
        # Выбираем стратегию на основе структуры
        if structure["has_code"]:
            # Используем code splitter
            return self._split_code_aware(text)
        elif structure["has_headers"]:
            # Используем markdown splitter
            return self._split_by_headers(text)
        elif structure["avg_paragraph_length"] > self.max_chunk_size:
            # Длинные параграфы - агрессивное разбиение
            return self._split_aggressive(text)
        else:
            # Стандартное разбиение
            return self._split_standard(text)
    
    def _split_standard(self, text):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.max_chunk_size,
            chunk_overlap=self.overlap
        )
        return splitter.split_text(text)
    
    def _split_by_headers(self, text):
        # Простая реализация split по заголовкам
        sections = re.split(r'\n(?=#)', text)
        chunks = []
        
        for section in sections:
            if len(section) > self.max_chunk_size:
                # Дополнительное разбиение длинных секций
                sub_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=self.max_chunk_size,
                    chunk_overlap=self.overlap
                )
                chunks.extend(sub_splitter.split_text(section))
            else:
                chunks.append(section.strip())
        
        return [chunk for chunk in chunks if chunk]
    
    def _split_code_aware(self, text):
        # Разбиение с учетом кода
        code_blocks = re.findall(r'```[\s\S]*?```', text)
        
        if code_blocks:
            # Сохраняем блоки кода целыми
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.max_chunk_size * 2,  # Больше размер для кода
                chunk_overlap=self.overlap,
                separators=["\n\n", "\n", " ", ""]
            )
        else:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.max_chunk_size,
                chunk_overlap=self.overlap
            )
        
        return splitter.split_text(text)
    
    def _split_aggressive(self, text):
        # Агрессивное разбиение для очень длинных параграфов
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.min_chunk_size,
            chunk_overlap=self.overlap // 2,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        return splitter.split_text(text)

# Тестирование адаптивного сплитера
adaptive_splitter = AdaptiveSplitter()

test_texts = {
    "markdown": """
# Глава 1
Это введение в тему.

## Подраздел 1.1
Детальное описание.

# Глава 2  
Продолжение темы.
""",
    "code": """
Вот пример кода:

```python
def hello_world():
    print("Hello, World!")
```

Этот код выводит приветствие.
""",
    "long_paragraphs": """
Это очень длинный параграф, который содержит много информации и должен быть разбит на более мелкие части для лучшего понимания и обработки системами машинного обучения, поскольку слишком длинные тексты могут быть проблематичными для анализа и векторизации, особенно когда мы работаем с ограничениями контекста различных языковых моделей и систем обработки естественного языка.
"""
}

print("Адаптивное разбиение:")
for text_type, text in test_texts.items():
    print(f"\n{text_type.upper()}:")
    structure = adaptive_splitter.analyze_text_structure(text)
    print(f"Структура: {structure}")
    
    chunks = adaptive_splitter.adaptive_split(text)
    print(f"Количество частей: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"  Часть {i+1}: {len(chunk)} символов")
```

## Оптимизация качества разбиения

### Метрики качества
```python
def evaluate_chunks_quality(original_text, chunks):
    """Оценка качества разбиения"""
    metrics = {}
    
    # 1. Покрытие (весь текст сохранен)
    combined_chunks = " ".join(chunks)
    coverage = len(combined_chunks) / len(original_text)
    metrics["coverage"] = coverage
    
    # 2. Равномерность размеров
    chunk_sizes = [len(chunk) for chunk in chunks]
    size_std = np.std(chunk_sizes)
    size_mean = np.mean(chunk_sizes)
    size_cv = size_std / size_mean if size_mean > 0 else 0
    metrics["size_consistency"] = 1 / (1 + size_cv)  # Чем меньше вариация, тем лучше
    
    # 3. Сохранение границ предложений
    sentence_breaks_preserved = 0
    for chunk in chunks:
        if chunk.strip().endswith(('.', '!', '?', '\n')):
            sentence_breaks_preserved += 1
    
    metrics["sentence_boundary_preservation"] = sentence_breaks_preserved / len(chunks)
    
    # 4. Отсутствие слишком коротких частей
    min_acceptable_size = 50
    acceptable_chunks = sum(1 for size in chunk_sizes if size >= min_acceptable_size)
    metrics["chunk_adequacy"] = acceptable_chunks / len(chunks)
    
    # Общая оценка (взвешенная)
    weights = {
        "coverage": 0.3,
        "size_consistency": 0.2,
        "sentence_boundary_preservation": 0.3,
        "chunk_adequacy": 0.2
    }
    
    overall_score = sum(metrics[key] * weights[key] for key in weights.keys())
    metrics["overall_score"] = overall_score
    
    return metrics

# Сравнение качества разных сплитеров
def compare_splitting_quality(text):
    """Сравнение качества разных сплитеров"""
    
    splitters_config = {
        "Character": CharacterTextSplitter(chunk_size=500, chunk_overlap=100),
        "Recursive": RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100),
        "Sentence (2)": SentenceSplitter(chunk_size=2, chunk_overlap=0),
        "Sentence (3)": SentenceSplitter(chunk_size=3, chunk_overlap=1),
    }
    
    results = {}
    
    for name, splitter in splitters_config.items():
        chunks = splitter.split_text(text)
        quality = evaluate_chunks_quality(text, chunks)
        results[name] = {
            "chunks_count": len(chunks),
            "quality_metrics": quality
        }
    
    return results

# Тестирование качества
quality_test_text = """
Искусственный интеллект (ИИ) — это область компьютерных наук, которая занимается созданием интеллектуальных машин. 
Эти машины способны выполнять задачи, которые обычно требуют человеческого интеллекта. 
К таким задачам относятся распознавание речи, принятие решений, визуальное восприятие и языковой перевод.

Машинное обучение является подмножеством ИИ. Оно фокусируется на идее того, что мы можем дать машинам доступ к данным. 
Затем позволить им учиться самостоятельно. Глубокое обучение, в свою очередь, является подмножеством машинного обучения. 
Оно использует нейронные сети с тремя или более слоями.

Применения ИИ включают экспертные системы, обработку естественного языка, распознавание речи и машинное зрение. 
По мере того как технологии развиваются, предыдущие эталоны того, что определяет ИИ, становятся устаревшими. 
Например, оптическое распознавание символов больше не считается примером искусственного интеллекта.
"""

quality_comparison = compare_splitting_quality(quality_test_text)

print("Сравнение качества разбиения:")
print("=" * 70)
for splitter_name, results in quality_comparison.items():
    print(f"\n{splitter_name}:")
    print(f"  Количество частей: {results['chunks_count']}")
    
    metrics = results['quality_metrics']
    print(f"  Покрытие: {metrics['coverage']:.2f}")
    print(f"  Равномерность: {metrics['size_consistency']:.2f}")
    print(f"  Границы предложений: {metrics['sentence_boundary_preservation']:.2f}")
    print(f"  Адекватность размера: {metrics['chunk_adequacy']:.2f}")
    print(f"  Общая оценка: {metrics['overall_score']:.2f}")
```

## Практические рекомендации

### Лучшие практики
```python
class SplittingBestPractices:
    """Лучшие практики для разбиения текста"""
    
    @staticmethod
    def get_optimal_chunk_size(model_type, use_case):
        """Рекомендуемые размеры частей"""
        
        recommendations = {
            "gpt-3.5-turbo": {
                "embedding": 512,      # Для создания эмбеддингов
                "qa": 1000,           # Для вопросов-ответов
                "summarization": 2000  # Для суммаризации
            },
            "gpt-4": {
                "embedding": 1024,
                "qa": 2000,
                "summarization": 4000
            },
            "text-embedding-ada-002": {
                "embedding": 512,
                "search": 256
            }
        }
        
        return recommendations.get(model_type, {}).get(use_case, 1000)
    
    @staticmethod
    def calculate_optimal_overlap(chunk_size):
        """Рассчет оптимального перекрытия"""
        # Правило: 10-20% от размера части
        return max(50, min(200, chunk_size // 5))
    
    @staticmethod
    def validate_chunks(chunks, min_size=50, max_size=None):
        """Валидация качества разбиения"""
        issues = []
        
        for i, chunk in enumerate(chunks):
            # Проверка минимального размера
            if len(chunk) < min_size:
                issues.append(f"Часть {i+1} слишком короткая: {len(chunk)} символов")
            
            # Проверка максимального размера
            if max_size and len(chunk) > max_size:
                issues.append(f"Часть {i+1} слишком длинная: {len(chunk)} символов")
            
            # Проверка на пустые части
            if not chunk.strip():
                issues.append(f"Часть {i+1} пустая")
            
            # Проверка на обрывы слов
            if chunk.strip() and not chunk.strip()[-1] in '.!?':
                words = chunk.strip().split()
                if len(words) > 1 and len(words[-1]) < 3:
                    issues.append(f"Часть {i+1} возможно обрывает слово: '{words[-1]}'")
        
        return issues

# Пример использования лучших практик
def create_optimal_splitter(text_type, model_target, use_case):
    """Создание оптимального сплитера"""
    
    practices = SplittingBestPractices()
    
    # Определяем оптимальные параметры
    chunk_size = practices.get_optimal_chunk_size(model_target, use_case)
    overlap = practices.calculate_optimal_overlap(chunk_size)
    
    # Выбираем тип сплитера
    if text_type == "code":
        splitter = PythonCodeTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    elif text_type == "markdown":
        # Для markdown используем комбинированный подход
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n# ", "\n## ", "\n### ", "\n\n", "\n", " ", ""]
        )
    else:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap
        )
    
    return splitter, {"chunk_size": chunk_size, "overlap": overlap}

# Демонстрация
example_configs = [
    ("general", "gpt-3.5-turbo", "qa"),
    ("markdown", "gpt-4", "summarization"),
    ("code", "text-embedding-ada-002", "embedding")
]

print("Оптимальные конфигурации сплитеров:")
print("=" * 50)

for text_type, model, use_case in example_configs:
    splitter, config = create_optimal_splitter(text_type, model, use_case)
    print(f"\n{text_type.capitalize()} для {model} ({use_case}):")
    print(f"  Размер части: {config['chunk_size']}")
    print(f"  Перекрытие: {config['overlap']}")
    print(f"  Тип сплитера: {type(splitter).__name__}")
```

## Ключевые моменты для экзамена

- **Назначение сплитеров** - разбиение длинного текста на части для LLM и векторизации
- **Основные типы** - Character, Recursive, Token-based, Sentence-based
- **Ключевые параметры** - chunk_size, chunk_overlap, separators
- **RecursiveCharacterTextSplitter** - самый популярный, сохраняет структуру
- **Специализированные** - Markdown, Code, HTML сплитеры для специфического контента
- **Token-based** - точный контроль для API ограничений (tiktoken)
- **Семантическое разбиение** - на основе смыслового сходства предложений
- **Оптимальные размеры** - 512-1024 токена для эмбеддингов, 1000-2000 для QA
- **Перекрытие** - 10-20% от размера части для сохранения контекста
- **Валидация качества** - проверка покрытия, равномерности, границ предложений