# Векторная база. Создание и использование

## Что такое векторная база данных

### Определение
Векторная база данных - это специализированная система хранения и поиска, которая работает с векторными представлениями данных (эмбеддингами). Она позволяет находить семантически похожие объекты по их векторным представлениям.

### Основные концепции
```python
# Вектор (эмбеддинг) - числовое представление текста/данных
text = "Привет, как дела?"
vector = [0.1, -0.3, 0.8, 0.2, -0.1, ...]  # Например, 1536 чисел для OpenAI

# Семантическое сходство через расстояние между векторами
similar_texts = [
    "Привет, как дела?",      # Расстояние: 0.0 (тот же текст)
    "Привет, как поживаешь?", # Расстояние: 0.2 (похожий смысл)
    "Собака бежит по парку"   # Расстояние: 0.9 (разный смысл)
]
```

## Популярные векторные базы данных

### 1. ChromaDB
```python
import chromadb

# Создание клиента
client = chromadb.Client()

# Создание коллекции
collection = client.create_collection(
    name="my_documents",
    metadata={"description": "Коллекция документов"}
)

# Добавление документов
collection.add(
    documents=["Это первый документ", "Это второй документ"],
    metadatas=[{"source": "file1.txt"}, {"source": "file2.txt"}],
    ids=["doc1", "doc2"]
)

# Поиск
results = collection.query(
    query_texts=["документ"],
    n_results=2
)
```

### 2. Pinecone
```python
import pinecone

# Инициализация
pinecone.init(api_key="your-api-key", environment="us-west1-gcp")

# Создание индекса
index = pinecone.Index("example-index")

# Добавление векторов
index.upsert([
    ("doc1", [0.1, 0.2, 0.3, ...], {"text": "Первый документ"}),
    ("doc2", [0.4, 0.5, 0.6, ...], {"text": "Второй документ"})
])

# Поиск
results = index.query(
    vector=[0.1, 0.2, 0.3, ...],
    top_k=5,
    include_metadata=True
)
```

### 3. Weaviate
```python
import weaviate

# Подключение
client = weaviate.Client("http://localhost:8080")

# Создание схемы
schema = {
    "classes": [{
        "class": "Document",
        "properties": [
            {"name": "content", "dataType": ["text"]},
            {"name": "source", "dataType": ["string"]}
        ]
    }]
}
client.schema.create(schema)

# Добавление данных
client.data_object.create({
    "content": "Содержимое документа",
    "source": "file.txt"
}, "Document")
```

### 4. FAISS (Facebook AI Similarity Search)
```python
import faiss
import numpy as np

# Создание индекса
dimension = 768  # Размерность векторов
index = faiss.IndexFlatL2(dimension)

# Добавление векторов
vectors = np.random.random((1000, dimension)).astype('float32')
index.add(vectors)

# Поиск
query_vector = np.random.random((1, dimension)).astype('float32')
distances, indices = index.search(query_vector, k=5)
```

## Создание эмбеддингов

### OpenAI Embeddings
```python
import openai

def get_openai_embedding(text, model="text-embedding-ada-002"):
    """Получить эмбеддинг через OpenAI API"""
    response = openai.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

# Пример использования
text = "Машинное обучение - это подраздел искусственного интеллекта"
embedding = get_openai_embedding(text)
print(f"Размерность вектора: {len(embedding)}")  # 1536 для ada-002
```

### Sentence Transformers
```python
from sentence_transformers import SentenceTransformer

# Загрузка модели
model = SentenceTransformer('all-MiniLM-L6-v2')

# Создание эмбеддингов
sentences = [
    "Это первое предложение",
    "Это второе предложение", 
    "Совершенно другая тема"
]

embeddings = model.encode(sentences)
print(f"Форма массива эмбеддингов: {embeddings.shape}")  # (3, 384)

# Вычисление сходства
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix = cosine_similarity(embeddings)
print(similarity_matrix)
```

### Многоязычные модели
```python
# Русскоязычная модель
russian_model = SentenceTransformer('cointegrated/rubert-tiny2')

russian_texts = [
    "Машинное обучение",
    "Искусственный интеллект", 
    "Котёнок играет с мячиком"
]

russian_embeddings = russian_model.encode(russian_texts)
```

## Практическая реализация векторной базы

### Простая векторная база на Python
```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import json

class SimpleVectorDB:
    def __init__(self):
        self.vectors = []
        self.documents = []
        self.metadata = []
        self.ids = []
    
    def add(self, doc_id, text, vector, metadata=None):
        """Добавить документ в базу"""
        self.ids.append(doc_id)
        self.documents.append(text)
        self.vectors.append(vector)
        self.metadata.append(metadata or {})
    
    def search(self, query_vector, top_k=5):
        """Поиск похожих документов"""
        if not self.vectors:
            return []
        
        # Вычисляем сходство со всеми векторами
        similarities = cosine_similarity(
            [query_vector], 
            self.vectors
        )[0]
        
        # Сортируем по убыванию сходства
        indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in indices:
            results.append({
                'id': self.ids[idx],
                'text': self.documents[idx],
                'similarity': similarities[idx],
                'metadata': self.metadata[idx]
            })
        
        return results
    
    def save(self, filepath):
        """Сохранить базу в файл"""
        data = {
            'vectors': self.vectors,
            'documents': self.documents,
            'metadata': self.metadata,
            'ids': self.ids
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, filepath):
        """Загрузить базу из файла"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.vectors = data['vectors']
        self.documents = data['documents'] 
        self.metadata = data['metadata']
        self.ids = data['ids']

# Пример использования
db = SimpleVectorDB()

# Добавляем документы
documents = [
    "Python - популярный язык программирования",
    "Машинное обучение использует алгоритмы для анализа данных",
    "Веб-разработка включает создание сайтов и приложений"
]

# Получаем эмбеддинги (упрощенный пример)
for i, doc in enumerate(documents):
    # В реальности здесь был бы вызов модели эмбеддингов
    fake_vector = np.random.random(384).tolist()
    db.add(f"doc_{i}", doc, fake_vector, {"category": "tech"})

# Поиск
query_vector = np.random.random(384).tolist()
results = db.search(query_vector, top_k=2)
```

### Интеграция с OpenAI
```python
class OpenAIVectorDB(SimpleVectorDB):
    def __init__(self, openai_model="text-embedding-ada-002"):
        super().__init__()
        self.openai_model = openai_model
    
    def add_text(self, doc_id, text, metadata=None):
        """Добавить текст с автоматическим созданием эмбеддинга"""
        vector = get_openai_embedding(text, self.openai_model)
        self.add(doc_id, text, vector, metadata)
    
    def search_text(self, query_text, top_k=5):
        """Поиск по текстовому запросу"""
        query_vector = get_openai_embedding(query_text, self.openai_model)
        return self.search(query_vector, top_k)

# Использование
ai_db = OpenAIVectorDB()

# Добавляем документы
knowledge_base = [
    "FastAPI - современный веб-фреймворк для Python",
    "Django - полнофункциональный веб-фреймворк",
    "Flask - легковесный микрофреймворк для веб-разработки",
    "NumPy - библиотека для работы с массивами в Python",
    "Pandas - инструмент для анализа и обработки данных"
]

for i, doc in enumerate(knowledge_base):
    ai_db.add_text(f"kb_{i}", doc, {"domain": "python"})

# Поиск
results = ai_db.search_text("веб-фреймворк для создания API", top_k=3)
for result in results:
    print(f"Сходство: {result['similarity']:.3f} - {result['text']}")
```

## Продвинутые возможности

### Чанкинг (разбиение текста)
```python
def chunk_text(text, chunk_size=500, overlap=50):
    """Разбить текст на перекрывающиеся части"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
    
    return chunks

# Пример
long_text = "Очень длинный текст..." * 100
chunks = chunk_text(long_text)
print(f"Разбито на {len(chunks)} частей")

# Добавляем чанки в векторную базу
for i, chunk in enumerate(chunks):
    ai_db.add_text(f"chunk_{i}", chunk, {"source": "long_document"})
```

### Фильтрация по метаданным
```python
class FilterableVectorDB(OpenAIVectorDB):
    def search_with_filter(self, query_text, metadata_filter=None, top_k=5):
        """Поиск с фильтрацией по метаданным"""
        query_vector = get_openai_embedding(query_text, self.openai_model)
        
        if not self.vectors:
            return []
        
        # Применяем фильтр
        valid_indices = []
        for i, meta in enumerate(self.metadata):
            if metadata_filter is None:
                valid_indices.append(i)
            else:
                match = True
                for key, value in metadata_filter.items():
                    if meta.get(key) != value:
                        match = False
                        break
                if match:
                    valid_indices.append(i)
        
        if not valid_indices:
            return []
        
        # Вычисляем сходство только для отфильтрованных документов
        filtered_vectors = [self.vectors[i] for i in valid_indices]
        similarities = cosine_similarity([query_vector], filtered_vectors)[0]
        
        # Сортируем и возвращаем результаты
        sorted_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in sorted_indices:
            original_idx = valid_indices[idx]
            results.append({
                'id': self.ids[original_idx],
                'text': self.documents[original_idx],
                'similarity': similarities[idx],
                'metadata': self.metadata[original_idx]
            })
        
        return results

# Использование фильтрации
filtered_db = FilterableVectorDB()

# Добавляем документы с разными категориями
docs_with_categories = [
    ("Python основы", {"category": "programming", "level": "beginner"}),
    ("Python продвинутый", {"category": "programming", "level": "advanced"}),
    ("Готовка борща", {"category": "cooking", "level": "beginner"}),
    ("Молекулярная кухня", {"category": "cooking", "level": "advanced"})
]

for i, (text, metadata) in enumerate(docs_with_categories):
    filtered_db.add_text(f"doc_{i}", text, metadata)

# Поиск только среди документов по программированию
programming_results = filtered_db.search_with_filter(
    "изучение Python",
    metadata_filter={"category": "programming"},
    top_k=2
)
```

### Гибридный поиск (семантический + лексический)
```python
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse

class HybridVectorDB(FilterableVectorDB):
    def __init__(self, openai_model="text-embedding-ada-002"):
        super().__init__(openai_model)
        self.tfidf = TfidfVectorizer(max_features=1000)
        self.tfidf_matrix = None
    
    def build_tfidf_index(self):
        """Построить TF-IDF индекс для лексического поиска"""
        if self.documents:
            self.tfidf_matrix = self.tfidf.fit_transform(self.documents)
    
    def hybrid_search(self, query_text, alpha=0.7, top_k=5):
        """
        Гибридный поиск: семантический + лексический
        alpha: вес семантического поиска (0-1)
        """
        if not self.documents:
            return []
        
        # Семантический поиск
        semantic_vector = get_openai_embedding(query_text, self.openai_model)
        semantic_scores = cosine_similarity([semantic_vector], self.vectors)[0]
        
        # Лексический поиск (TF-IDF)
        if self.tfidf_matrix is None:
            self.build_tfidf_index()
        
        query_tfidf = self.tfidf.transform([query_text])
        lexical_scores = cosine_similarity(query_tfidf, self.tfidf_matrix)[0]
        
        # Комбинируем оценки
        combined_scores = alpha * semantic_scores + (1 - alpha) * lexical_scores
        
        # Сортируем и возвращаем результаты
        indices = np.argsort(combined_scores)[::-1][:top_k]
        
        results = []
        for idx in indices:
            results.append({
                'id': self.ids[idx],
                'text': self.documents[idx],
                'hybrid_score': combined_scores[idx],
                'semantic_score': semantic_scores[idx],
                'lexical_score': lexical_scores[idx],
                'metadata': self.metadata[idx]
            })
        
        return results

# Пример гибридного поиска
hybrid_db = HybridVectorDB()

# Добавляем документы
tech_docs = [
    "FastAPI это современный веб-фреймворк для Python",
    "Django предоставляет полный набор инструментов для веб-разработки",
    "Machine learning алгоритмы используются для анализа данных",
    "API интерфейсы позволяют взаимодействовать с веб-сервисами"
]

for i, doc in enumerate(tech_docs):
    hybrid_db.add_text(f"tech_{i}", doc, {"type": "documentation"})

# Гибридный поиск
results = hybrid_db.hybrid_search("веб API разработка", alpha=0.6, top_k=3)
for result in results:
    print(f"Гибридная оценка: {result['hybrid_score']:.3f}")
    print(f"Семантическая: {result['semantic_score']:.3f}")
    print(f"Лексическая: {result['lexical_score']:.3f}")
    print(f"Текст: {result['text']}\n")
```

## Оптимизация производительности

### Индексирование
```python
import faiss

class OptimizedVectorDB:
    def __init__(self, dimension=1536):
        self.dimension = dimension
        # Используем более быстрый индекс для больших коллекций
        self.index = faiss.IndexIVFFlat(
            faiss.IndexFlatL2(dimension), 
            dimension, 
            100  # количество кластеров
        )
        self.is_trained = False
        self.documents = []
        self.metadata = []
        self.ids = []
    
    def add_batch(self, vectors, documents, ids, metadata):
        """Добавить пакет векторов эффективно"""
        vectors_array = np.array(vectors).astype('float32')
        
        # Тренируем индекс если нужно
        if not self.is_trained and len(vectors) >= 100:
            self.index.train(vectors_array)
            self.is_trained = True
        
        if self.is_trained:
            self.index.add(vectors_array)
        
        self.documents.extend(documents)
        self.ids.extend(ids)
        self.metadata.extend(metadata)
    
    def search_fast(self, query_vector, top_k=5):
        """Быстрый поиск с использованием FAISS"""
        if not self.is_trained:
            return []
        
        query_array = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_array, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0:  # FAISS возвращает -1 для пустых результатов
                results.append({
                    'id': self.ids[idx],
                    'text': self.documents[idx],
                    'distance': distances[0][i],
                    'metadata': self.metadata[idx]
                })
        
        return results
```

### Кэширование
```python
import hashlib
from functools import lru_cache

class CachedVectorDB(SimpleVectorDB):
    def __init__(self, cache_size=1000):
        super().__init__()
        self.embedding_cache = {}
        self.cache_size = cache_size
    
    def _hash_text(self, text):
        """Создать хэш для текста"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get_cached_embedding(self, text):
        """Получить эмбеддинг с кэшированием"""
        text_hash = self._hash_text(text)
        
        if text_hash in self.embedding_cache:
            return self.embedding_cache[text_hash]
        
        # Получаем новый эмбеддинг
        embedding = get_openai_embedding(text)
        
        # Кэшируем (с ограничением размера)
        if len(self.embedding_cache) >= self.cache_size:
            # Удаляем старейший элемент (простая стратегия)
            oldest_key = next(iter(self.embedding_cache))
            del self.embedding_cache[oldest_key]
        
        self.embedding_cache[text_hash] = embedding
        return embedding
```

## Частые проблемы и решения

### 1. Размерность векторов
```python
# ПРОБЛЕМА: разные модели дают разные размерности
openai_dim = 1536  # text-embedding-ada-002
sentence_transformer_dim = 384  # all-MiniLM-L6-v2

# РЕШЕНИЕ: нормализация размерности
def normalize_vector_dimension(vector, target_dim):
    current_dim = len(vector)
    if current_dim == target_dim:
        return vector
    elif current_dim > target_dim:
        # Обрезаем
        return vector[:target_dim]
    else:
        # Дополняем нулями
        return vector + [0.0] * (target_dim - current_dim)
```

### 2. Качество поиска
```python
# ПРОБЛЕМА: плохое качество поиска
# РЕШЕНИЯ:
# 1. Лучшая модель эмбеддингов
# 2. Предобработка текста
# 3. Гибридный поиск
# 4. Правильное чанкинг

def preprocess_text(text):
    """Предобработка текста для лучшего поиска"""
    # Удаляем лишние пробелы
    text = ' '.join(text.split())
    
    # Приводим к нижнему регистру
    text = text.lower()
    
    # Удаляем специальные символы (опционально)
    import re
    text = re.sub(r'[^\w\s\u0400-\u04FF]', ' ', text)
    
    return text
```

### 3. Масштабирование
```python
# ПРОБЛЕМА: медленный поиск в больших базах
# РЕШЕНИЯ:
# 1. Используйте специализированные векторные БД (Pinecone, Weaviate)
# 2. Индексирование (FAISS, Annoy)
# 3. Фильтрация перед поиском
# 4. Кластеризация документов

def cluster_documents(vectors, n_clusters=10):
    """Кластеризация для ускорения поиска"""
    from sklearn.cluster import KMeans
    
    kmeans = KMeans(n_clusters=n_clusters)
    cluster_labels = kmeans.fit_predict(vectors)
    
    return cluster_labels, kmeans
```

## Ключевые моменты для экзамена

- **Векторная база** хранит числовые представления (эмбеддинги) текстов/объектов
- **Семантический поиск** находит похожие по смыслу документы, не только по ключевым словам
- **Эмбеддинги** создаются специальными моделями (OpenAI, Sentence Transformers)
- **Популярные БД**: ChromaDB, Pinecone, Weaviate, FAISS
- **Метрики сходства**: косинусное расстояние, евклидово расстояние
- **Чанкинг** - разбиение длинных текстов на части для лучшего поиска
- **Гибридный поиск** - комбинация семантического и лексического поиска
- **Метаданные** позволяют фильтровать результаты поиска
- **Кэширование** эмбеддингов экономит время и деньги
- **Индексирование** (FAISS) ускоряет поиск в больших коллекциях