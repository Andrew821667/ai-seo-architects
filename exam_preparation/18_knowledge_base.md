# База знаний. Источники базы знаний

## Что такое база знаний

### Определение и назначение
```python
# База знаний (Knowledge Base) - структурированное хранилище информации
# для использования в AI системах, особенно в RAG (Retrieval-Augmented Generation)

# Основные компоненты базы знаний:
knowledge_base_components = {
    "documents": "Исходные документы и тексты",
    "embeddings": "Векторные представления текстов", 
    "metadata": "Метаданные документов (источник, дата, тип)",
    "index": "Индекс для быстрого поиска",
    "retrieval_system": "Система извлечения релевантной информации"
}

# Типы баз знаний:
kb_types = {
    "vector_db": "Векторные базы данных (ChromaDB, Pinecone, Weaviate)",
    "graph_db": "Графовые базы знаний (Neo4j, Amazon Neptune)",
    "hybrid": "Гибридные системы (векторный + традиционный поиск)",
    "structured": "Структурированные базы (SQL с семантическим слоем)"
}
```

### Архитектура современной базы знаний
```python
class KnowledgeBase:
    """Базовая архитектура базы знаний"""
    
    def __init__(self):
        self.documents = []          # Исходные документы
        self.embeddings = []         # Векторные представления
        self.metadata = []           # Метаданные
        self.vector_store = None     # Векторное хранилище
        self.text_splitter = None    # Сплитер текста
        self.embedding_model = None  # Модель эмбеддингов
    
    def add_document(self, document, metadata=None):
        """Добавление документа в базу знаний"""
        # 1. Разбиение на части
        chunks = self.text_splitter.split_text(document)
        
        # 2. Создание эмбеддингов
        embeddings = self.embedding_model.embed_documents(chunks)
        
        # 3. Сохранение в векторном хранилище
        doc_metadata = metadata or {}
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_metadata = {
                **doc_metadata,
                "chunk_id": i,
                "chunk_size": len(chunk)
            }
            self.vector_store.add(
                text=chunk,
                embedding=embedding,
                metadata=chunk_metadata
            )
    
    def search(self, query, top_k=5):
        """Поиск релевантной информации"""
        # 1. Создание эмбеддинга запроса
        query_embedding = self.embedding_model.embed_query(query)
        
        # 2. Поиск похожих документов
        results = self.vector_store.similarity_search(
            query_embedding, 
            k=top_k
        )
        
        return results
    
    def get_context_for_query(self, query, max_context_length=2000):
        """Получение контекста для ответа на запрос"""
        results = self.search(query)
        
        context_parts = []
        current_length = 0
        
        for result in results:
            if current_length + len(result.text) <= max_context_length:
                context_parts.append(result.text)
                current_length += len(result.text)
            else:
                break
        
        return "\n\n".join(context_parts)
```

## Источники данных для базы знаний

### 1. Документы и файлы
```python
import os
import PyPDF2
import docx
from bs4 import BeautifulSoup

class DocumentLoader:
    """Загрузчик различных типов документов"""
    
    @staticmethod
    def load_text_file(file_path, encoding='utf-8'):
        """Загрузка текстового файла"""
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            # Попытка с другой кодировкой
            with open(file_path, 'r', encoding='cp1251') as file:
                return file.read()
    
    @staticmethod
    def load_pdf(file_path):
        """Загрузка PDF файла"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Ошибка загрузки PDF: {e}")
        return text
    
    @staticmethod
    def load_docx(file_path):
        """Загрузка Word документа"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Ошибка загрузки DOCX: {e}")
            return ""
    
    @staticmethod
    def load_html(file_path):
        """Загрузка HTML файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file.read(), 'html.parser')
                
                # Удаляем скрипты и стили
                for script in soup(["script", "style"]):
                    script.decompose()
                
                return soup.get_text()
        except Exception as e:
            print(f"Ошибка загрузки HTML: {e}")
            return ""
    
    def load_directory(self, directory_path):
        """Загрузка всех поддерживаемых файлов из директории"""
        documents = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                metadata = {
                    "source": file_path,
                    "filename": file,
                    "file_type": file_ext,
                    "directory": root
                }
                
                try:
                    if file_ext == '.txt':
                        content = self.load_text_file(file_path)
                    elif file_ext == '.pdf':
                        content = self.load_pdf(file_path)
                    elif file_ext == '.docx':
                        content = self.load_docx(file_path)
                    elif file_ext == '.html':
                        content = self.load_html(file_path)
                    else:
                        continue  # Пропускаем неподдерживаемые форматы
                    
                    if content.strip():  # Только непустые документы
                        documents.append({
                            "content": content,
                            "metadata": metadata
                        })
                        
                except Exception as e:
                    print(f"Ошибка загрузки {file_path}: {e}")
        
        return documents

# Пример использования
loader = DocumentLoader()

# Загрузка отдельных файлов
# pdf_content = loader.load_pdf("document.pdf")
# docx_content = loader.load_docx("report.docx")

# Загрузка всей директории
# documents = loader.load_directory("./knowledge_docs/")
# print(f"Загружено {len(documents)} документов")
```

### 2. Веб-страницы и API
```python
import requests
from urllib.parse import urljoin, urlparse
import time
import json

class WebContentLoader:
    """Загрузчик контента из веб-источников"""
    
    def __init__(self, delay=1):
        self.delay = delay  # Задержка между запросами
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def load_single_page(self, url):
        """Загрузка одной веб-страницы"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Удаляем ненужные элементы
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Извлекаем заголовок
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Извлекаем основной контент
            content = soup.get_text()
            
            # Очистка текста
            lines = [line.strip() for line in content.splitlines()]
            content = '\n'.join(line for line in lines if line)
            
            metadata = {
                "source": url,
                "title": title_text,
                "url": url,
                "content_type": "web_page"
            }
            
            return {"content": content, "metadata": metadata}
            
        except Exception as e:
            print(f"Ошибка загрузки {url}: {e}")
            return None
    
    def load_sitemap(self, sitemap_url, max_pages=100):
        """Загрузка страниц из sitemap"""
        try:
            response = self.session.get(sitemap_url)
            soup = BeautifulSoup(response.content, 'xml')
            
            urls = []
            for loc in soup.find_all('loc'):
                urls.append(loc.get_text())
                if len(urls) >= max_pages:
                    break
            
            documents = []
            for url in urls:
                doc = self.load_single_page(url)
                if doc:
                    documents.append(doc)
                time.sleep(self.delay)  # Вежливая пауза
            
            return documents
            
        except Exception as e:
            print(f"Ошибка загрузки sitemap: {e}")
            return []
    
    def load_api_content(self, api_endpoint, headers=None, params=None):
        """Загрузка контента через API"""
        try:
            response = self.session.get(
                api_endpoint, 
                headers=headers or {}, 
                params=params or {}
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Преобразуем JSON в текст для поиска
            content = json.dumps(data, ensure_ascii=False, indent=2)
            
            metadata = {
                "source": api_endpoint,
                "content_type": "api_response",
                "api_endpoint": api_endpoint
            }
            
            return {"content": content, "metadata": metadata}
            
        except Exception as e:
            print(f"Ошибка загрузки API: {e}")
            return None

# Пример загрузки веб-контента
web_loader = WebContentLoader(delay=2)

# Загрузка отдельной страницы
# page_doc = web_loader.load_single_page("https://example.com/article")

# Загрузка через API (пример с GitHub API)
# github_doc = web_loader.load_api_content(
#     "https://api.github.com/repos/microsoft/vscode",
#     headers={"Accept": "application/vnd.github.v3+json"}
# )
```

### 3. Базы данных
```python
import sqlite3
import psycopg2
import pandas as pd

class DatabaseLoader:
    """Загрузчик данных из баз данных"""
    
    def __init__(self, db_type, connection_params):
        self.db_type = db_type
        self.connection_params = connection_params
        self.connection = None
    
    def connect(self):
        """Подключение к базе данных"""
        try:
            if self.db_type == 'sqlite':
                self.connection = sqlite3.connect(self.connection_params['database'])
            elif self.db_type == 'postgresql':
                self.connection = psycopg2.connect(**self.connection_params)
            else:
                raise ValueError(f"Неподдерживаемый тип БД: {self.db_type}")
            return True
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            return False
    
    def load_table_as_text(self, table_name, text_columns, max_rows=1000):
        """Загрузка таблицы как текстовых документов"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            # Формируем запрос
            columns_str = ", ".join(text_columns)
            query = f"SELECT {columns_str} FROM {table_name} LIMIT {max_rows}"
            
            # Выполняем запрос
            df = pd.read_sql_query(query, self.connection)
            
            documents = []
            for index, row in df.iterrows():
                # Объединяем текстовые колонки
                content_parts = []
                for col in text_columns:
                    if pd.notna(row[col]):
                        content_parts.append(f"{col}: {row[col]}")
                
                content = "\n".join(content_parts)
                
                metadata = {
                    "source": f"database_{table_name}",
                    "table": table_name,
                    "row_id": index,
                    "content_type": "database_record"
                }
                
                documents.append({
                    "content": content,
                    "metadata": metadata
                })
            
            return documents
            
        except Exception as e:
            print(f"Ошибка загрузки из БД: {e}")
            return []
    
    def load_custom_query(self, query, content_template):
        """Загрузка по кастомному запросу"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            df = pd.read_sql_query(query, self.connection)
            
            documents = []
            for index, row in df.iterrows():
                # Используем шаблон для форматирования контента
                content = content_template.format(**row.to_dict())
                
                metadata = {
                    "source": "database_custom_query",
                    "content_type": "database_query_result",
                    "row_id": index
                }
                
                documents.append({
                    "content": content,
                    "metadata": metadata
                })
            
            return documents
            
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []
    
    def close(self):
        """Закрытие соединения"""
        if self.connection:
            self.connection.close()

# Пример использования
# sqlite_loader = DatabaseLoader('sqlite', {'database': 'knowledge.db'})
# 
# # Загрузка таблицы статей
# articles = sqlite_loader.load_table_as_text(
#     'articles', 
#     ['title', 'content', 'summary'],
#     max_rows=500
# )
# 
# # Кастомный запрос
# template = "Статья: {title}\nАвтор: {author}\nСодержание: {content}"
# custom_docs = sqlite_loader.load_custom_query(
#     "SELECT title, author, content FROM articles WHERE category = 'AI'",
#     template
# )
# 
# sqlite_loader.close()
```

### 4. Документооборот и CRM системы
```python
class CRMLoader:
    """Загрузчик данных из CRM и систем документооборота"""
    
    def __init__(self, system_type, api_credentials):
        self.system_type = system_type
        self.credentials = api_credentials
        self.session = requests.Session()
    
    def load_salesforce_data(self):
        """Загрузка данных из Salesforce"""
        # Аутентификация в Salesforce
        auth_url = f"{self.credentials['instance_url']}/services/oauth2/token"
        auth_data = {
            'grant_type': 'password',
            'client_id': self.credentials['client_id'],
            'client_secret': self.credentials['client_secret'],
            'username': self.credentials['username'],
            'password': self.credentials['password']
        }
        
        try:
            auth_response = self.session.post(auth_url, data=auth_data)
            auth_response.raise_for_status()
            token = auth_response.json()['access_token']
            
            # Настройка заголовков
            self.session.headers.update({
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            })
            
            # Загрузка данных
            documents = []
            
            # Загружаем аккаунты
            accounts = self._query_salesforce("SELECT Id, Name, Description FROM Account LIMIT 100")
            for account in accounts:
                content = f"Компания: {account['Name']}\nОписание: {account.get('Description', '')}"
                documents.append({
                    "content": content,
                    "metadata": {
                        "source": "salesforce_account",
                        "record_id": account['Id'],
                        "record_type": "Account"
                    }
                })
            
            # Загружаем возможности (Opportunities)
            opportunities = self._query_salesforce("SELECT Id, Name, Description, StageName FROM Opportunity LIMIT 100")
            for opp in opportunities:
                content = f"Сделка: {opp['Name']}\nСтадия: {opp['StageName']}\nОписание: {opp.get('Description', '')}"
                documents.append({
                    "content": content,
                    "metadata": {
                        "source": "salesforce_opportunity",
                        "record_id": opp['Id'],
                        "record_type": "Opportunity"
                    }
                })
            
            return documents
            
        except Exception as e:
            print(f"Ошибка загрузки из Salesforce: {e}")
            return []
    
    def _query_salesforce(self, soql_query):
        """Выполнение SOQL запроса"""
        query_url = f"{self.credentials['instance_url']}/services/data/v52.0/query/"
        response = self.session.get(query_url, params={'q': soql_query})
        response.raise_for_status()
        return response.json()['records']
    
    def load_confluence_pages(self):
        """Загрузка страниц из Confluence"""
        base_url = self.credentials['base_url']
        auth = (self.credentials['username'], self.credentials['api_token'])
        
        try:
            # Получаем список страниц
            pages_url = f"{base_url}/rest/api/content"
            params = {
                'expand': 'body.storage,metadata.labels',
                'limit': 100
            }
            
            response = self.session.get(pages_url, auth=auth, params=params)
            response.raise_for_status()
            
            pages_data = response.json()
            documents = []
            
            for page in pages_data['results']:
                # Извлекаем контент
                title = page['title']
                body = page['body']['storage']['value']
                
                # Очищаем HTML
                soup = BeautifulSoup(body, 'html.parser')
                clean_content = soup.get_text()
                
                content = f"Заголовок: {title}\n\nСодержание:\n{clean_content}"
                
                # Извлекаем метки
                labels = [label['name'] for label in page.get('metadata', {}).get('labels', {}).get('results', [])]
                
                documents.append({
                    "content": content,
                    "metadata": {
                        "source": "confluence",
                        "page_id": page['id'],
                        "title": title,
                        "labels": labels,
                        "content_type": "confluence_page"
                    }
                })
            
            return documents
            
        except Exception as e:
            print(f"Ошибка загрузки из Confluence: {e}")
            return []

# Пример настройки CRM загрузчика
# salesforce_config = {
#     'instance_url': 'https://your-org.salesforce.com',
#     'client_id': 'your_client_id',
#     'client_secret': 'your_client_secret',
#     'username': 'your_username',
#     'password': 'your_password'
# }
# 
# confluence_config = {
#     'base_url': 'https://your-org.atlassian.net/wiki',
#     'username': 'your_email',
#     'api_token': 'your_api_token'
# }
# 
# crm_loader = CRMLoader('salesforce', salesforce_config)
# salesforce_docs = crm_loader.load_salesforce_data()
```

## Создание и управление базой знаний

### Полная система базы знаний
```python
from datetime import datetime
import hashlib
import json

class ComprehensiveKnowledgeBase:
    """Комплексная система управления базой знаний"""
    
    def __init__(self, storage_path="./knowledge_base"):
        self.storage_path = storage_path
        self.documents = {}  # document_id -> document
        self.metadata_index = {}  # source -> [document_ids]
        self.content_hashes = {}  # hash -> document_id (для дедупликации)
        self.loaders = {
            'files': DocumentLoader(),
            'web': WebContentLoader(),
            'database': None,  # Инициализируется при необходимости
            'crm': None
        }
        
        # Создаем директорию если не существует
        os.makedirs(storage_path, exist_ok=True)
        
        # Загружаем существующую базу
        self.load_index()
    
    def add_documents_from_source(self, source_type, source_config):
        """Добавление документов из различных источников"""
        documents = []
        
        if source_type == 'directory':
            documents = self.loaders['files'].load_directory(source_config['path'])
            
        elif source_type == 'web_pages':
            for url in source_config['urls']:
                doc = self.loaders['web'].load_single_page(url)
                if doc:
                    documents.append(doc)
                    
        elif source_type == 'sitemap':
            documents = self.loaders['web'].load_sitemap(
                source_config['sitemap_url'],
                source_config.get('max_pages', 100)
            )
            
        elif source_type == 'database':
            if not self.loaders['database']:
                self.loaders['database'] = DatabaseLoader(
                    source_config['db_type'],
                    source_config['connection_params']
                )
            
            documents = self.loaders['database'].load_table_as_text(
                source_config['table'],
                source_config['text_columns'],
                source_config.get('max_rows', 1000)
            )
        
        # Добавляем документы в базу
        added_count = 0
        for doc in documents:
            if self.add_document(doc['content'], doc['metadata']):
                added_count += 1
        
        print(f"Добавлено {added_count} новых документов из {len(documents)} загруженных")
        return added_count
    
    def add_document(self, content, metadata=None):
        """Добавление отдельного документа"""
        # Создаем хэш контента для дедупликации
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        if content_hash in self.content_hashes:
            print(f"Документ уже существует: {metadata.get('source', 'unknown')}")
            return False
        
        # Генерируем уникальный ID
        doc_id = f"doc_{len(self.documents)}_{int(datetime.now().timestamp())}"
        
        # Подготавливаем метаданные
        doc_metadata = {
            "doc_id": doc_id,
            "added_date": datetime.now().isoformat(),
            "content_hash": content_hash,
            "content_length": len(content),
            **(metadata or {})
        }
        
        # Сохраняем документ
        document = {
            "id": doc_id,
            "content": content,
            "metadata": doc_metadata
        }
        
        self.documents[doc_id] = document
        self.content_hashes[content_hash] = doc_id
        
        # Обновляем индекс по источникам
        source = doc_metadata.get('source', 'unknown')
        if source not in self.metadata_index:
            self.metadata_index[source] = []
        self.metadata_index[source].append(doc_id)
        
        return True
    
    def search_documents(self, query, source_filter=None, content_type_filter=None):
        """Поиск документов по содержимому и метаданным"""
        results = []
        query_lower = query.lower()
        
        for doc_id, document in self.documents.items():
            metadata = document['metadata']
            
            # Применяем фильтры
            if source_filter and source_filter not in metadata.get('source', ''):
                continue
                
            if content_type_filter and metadata.get('content_type') != content_type_filter:
                continue
            
            # Простой текстовый поиск
            if query_lower in document['content'].lower():
                # Вычисляем релевантность (простая)
                relevance = document['content'].lower().count(query_lower)
                
                results.append({
                    "document": document,
                    "relevance": relevance,
                    "preview": self._get_preview(document['content'], query, 200)
                })
        
        # Сортируем по релевантности
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results
    
    def _get_preview(self, content, query, max_length=200):
        """Создание превью с выделением ключевых слов"""
        query_lower = query.lower()
        content_lower = content.lower()
        
        # Находим первое вхождение
        index = content_lower.find(query_lower)
        if index == -1:
            return content[:max_length] + "..."
        
        # Создаем превью вокруг найденного текста
        start = max(0, index - max_length // 2)
        end = min(len(content), start + max_length)
        
        preview = content[start:end]
        if start > 0:
            preview = "..." + preview
        if end < len(content):
            preview += "..."
        
        return preview
    
    def get_statistics(self):
        """Статистика базы знаний"""
        total_docs = len(self.documents)
        total_content_length = sum(len(doc['content']) for doc in self.documents.values())
        
        # Статистика по источникам
        source_stats = {}
        for source, doc_ids in self.metadata_index.items():
            source_stats[source] = len(doc_ids)
        
        # Статистика по типам контента
        content_type_stats = {}
        for doc in self.documents.values():
            content_type = doc['metadata'].get('content_type', 'unknown')
            content_type_stats[content_type] = content_type_stats.get(content_type, 0) + 1
        
        return {
            "total_documents": total_docs,
            "total_content_length": total_content_length,
            "average_doc_length": total_content_length / total_docs if total_docs > 0 else 0,
            "sources": source_stats,
            "content_types": content_type_stats
        }
    
    def save_index(self):
        """Сохранение индекса базы знаний"""
        index_data = {
            "documents": {doc_id: doc['metadata'] for doc_id, doc in self.documents.items()},
            "metadata_index": self.metadata_index,
            "content_hashes": self.content_hashes,
            "last_updated": datetime.now().isoformat()
        }
        
        index_path = os.path.join(self.storage_path, "index.json")
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
        
        # Сохраняем содержимое документов отдельно
        for doc_id, document in self.documents.items():
            doc_path = os.path.join(self.storage_path, f"{doc_id}.txt")
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(document['content'])
    
    def load_index(self):
        """Загрузка существующего индекса"""
        index_path = os.path.join(self.storage_path, "index.json")
        
        if not os.path.exists(index_path):
            return
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            self.metadata_index = index_data.get('metadata_index', {})
            self.content_hashes = index_data.get('content_hashes', {})
            
            # Загружаем документы
            for doc_id, metadata in index_data.get('documents', {}).items():
                doc_path = os.path.join(self.storage_path, f"{doc_id}.txt")
                if os.path.exists(doc_path):
                    with open(doc_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    self.documents[doc_id] = {
                        "id": doc_id,
                        "content": content,
                        "metadata": metadata
                    }
            
            print(f"Загружено {len(self.documents)} документов из базы знаний")
            
        except Exception as e:
            print(f"Ошибка загрузки индекса: {e}")

# Пример использования комплексной системы
kb = ComprehensiveKnowledgeBase("./my_knowledge_base")

# Добавление документов из разных источников
sources_config = [
    {
        'type': 'directory',
        'config': {'path': './documents/'}
    },
    {
        'type': 'web_pages',
        'config': {'urls': ['https://example.com/page1', 'https://example.com/page2']}
    }
]

for source in sources_config:
    kb.add_documents_from_source(source['type'], source['config'])

# Сохранение базы знаний
kb.save_index()

# Поиск в базе знаний
search_results = kb.search_documents("машинное обучение", source_filter="web")
print(f"Найдено {len(search_results)} документов")

# Статистика
stats = kb.get_statistics()
print("Статистика базы знаний:")
for key, value in stats.items():
    print(f"  {key}: {value}")
```

## Оптимизация и качество базы знаний

### Очистка и обработка данных
```python
import re
from collections import Counter

class KnowledgeBaseOptimizer:
    """Оптимизатор для улучшения качества базы знаний"""
    
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
    
    def clean_documents(self):
        """Очистка документов от мусора"""
        cleaned_count = 0
        
        for doc_id, document in self.kb.documents.items():
            original_content = document['content']
            cleaned_content = self._clean_text(original_content)
            
            if cleaned_content != original_content:
                document['content'] = cleaned_content
                document['metadata']['cleaned'] = True
                cleaned_count += 1
        
        print(f"Очищено {cleaned_count} документов")
        return cleaned_count
    
    def _clean_text(self, text):
        """Очистка текста"""
        # Удаляем лишние пробелы и переносы
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Удаляем HTML сущности
        text = re.sub(r'&[a-zA-Z0-9#]+;', '', text)
        
        # Удаляем URLs (опционально)
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Удаляем email адреса (опционально)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        return text.strip()
    
    def detect_duplicates(self, similarity_threshold=0.9):
        """Обнаружение дублирующихся документов"""
        from difflib import SequenceMatcher
        
        duplicates = []
        doc_ids = list(self.kb.documents.keys())
        
        for i in range(len(doc_ids)):
            for j in range(i + 1, len(doc_ids)):
                doc1 = self.kb.documents[doc_ids[i]]
                doc2 = self.kb.documents[doc_ids[j]]
                
                # Вычисляем сходство
                similarity = SequenceMatcher(None, doc1['content'], doc2['content']).ratio()
                
                if similarity >= similarity_threshold:
                    duplicates.append({
                        'doc1_id': doc_ids[i],
                        'doc2_id': doc_ids[j],
                        'similarity': similarity,
                        'doc1_source': doc1['metadata'].get('source', 'unknown'),
                        'doc2_source': doc2['metadata'].get('source', 'unknown')
                    })
        
        return duplicates
    
    def analyze_content_quality(self):
        """Анализ качества контента"""
        quality_issues = []
        
        for doc_id, document in self.kb.documents.items():
            content = document['content']
            metadata = document['metadata']
            
            issues = []
            
            # Проверка длины
            if len(content) < 100:
                issues.append("too_short")
            elif len(content) > 50000:
                issues.append("too_long")
            
            # Проверка на читаемость
            words = content.split()
            if len(words) < 10:
                issues.append("too_few_words")
            
            # Проверка на повторяющийся контент
            word_freq = Counter(words)
            most_common_word_freq = word_freq.most_common(1)[0][1] if word_freq else 0
            if most_common_word_freq > len(words) * 0.1:  # Одно слово больше 10% от всех
                issues.append("repetitive_content")
            
            # Проверка кодировки и спецсимволов
            if len(re.findall(r'[^\x00-\x7F]+', content)) > len(content) * 0.5:
                issues.append("encoding_issues")
            
            if issues:
                quality_issues.append({
                    'doc_id': doc_id,
                    'source': metadata.get('source', 'unknown'),
                    'issues': issues,
                    'content_length': len(content)
                })
        
        return quality_issues
    
    def suggest_improvements(self):
        """Предложения по улучшению базы знаний"""
        suggestions = []
        
        # Анализ дублей
        duplicates = self.detect_duplicates()
        if duplicates:
            suggestions.append({
                'type': 'duplicates',
                'count': len(duplicates),
                'action': 'Удалить дублирующиеся документы',
                'details': duplicates[:5]  # Показываем первые 5
            })
        
        # Анализ качества
        quality_issues = self.analyze_content_quality()
        if quality_issues:
            issue_types = Counter()
            for issue in quality_issues:
                for issue_type in issue['issues']:
                    issue_types[issue_type] += 1
            
            suggestions.append({
                'type': 'quality_issues',
                'count': len(quality_issues),
                'action': 'Исправить проблемы качества',
                'issue_breakdown': dict(issue_types)
            })
        
        # Анализ покрытия тем
        all_words = []
        for document in self.kb.documents.values():
            all_words.extend(document['content'].lower().split())
        
        word_freq = Counter(all_words)
        most_common = word_freq.most_common(20)
        
        suggestions.append({
            'type': 'topic_coverage',
            'action': 'Анализ покрытия тем',
            'top_terms': most_common
        })
        
        return suggestions

# Пример оптимизации базы знаний
optimizer = KnowledgeBaseOptimizer(kb)

# Очистка документов
optimizer.clean_documents()

# Анализ качества
quality_issues = optimizer.analyze_content_quality()
print(f"Найдено {len(quality_issues)} документов с проблемами качества")

# Поиск дублей
duplicates = optimizer.detect_duplicates()
print(f"Найдено {len(duplicates)} пар дублирующихся документов")

# Получение предложений по улучшению
suggestions = optimizer.suggest_improvements()
print("\nПредложения по улучшению:")
for suggestion in suggestions:
    print(f"- {suggestion['action']}: {suggestion.get('count', 'N/A')} элементов")
```

## Интеграция с векторными базами данных

### Подключение к ChromaDB
```python
import chromadb
from sentence_transformers import SentenceTransformer

class VectorKnowledgeBase:
    """База знаний с векторным поиском"""
    
    def __init__(self, collection_name="knowledge_base", model_name="all-MiniLM-L6-v2"):
        self.client = chromadb.Client()
        self.collection_name = collection_name
        self.model = SentenceTransformer(model_name)
        
        # Создаем или получаем коллекцию
        try:
            self.collection = self.client.get_collection(collection_name)
        except:
            self.collection = self.client.create_collection(collection_name)
    
    def add_document(self, content, metadata=None, doc_id=None):
        """Добавление документа с векторизацией"""
        # Создаем эмбеддинг
        embedding = self.model.encode(content).tolist()
        
        # Генерируем ID если не предоставлен
        if not doc_id:
            doc_id = f"doc_{len(self.collection.get()['ids'])}"
        
        # Добавляем в коллекцию
        self.collection.add(
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        
        return doc_id
    
    def search(self, query, n_results=5, where_filter=None):
        """Семантический поиск"""
        # Создаем эмбеддинг запроса
        query_embedding = self.model.encode(query).tolist()
        
        # Выполняем поиск
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        return {
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0],
            'ids': results['ids'][0]
        }
    
    def get_collection_stats(self):
        """Статистика коллекции"""
        data = self.collection.get()
        return {
            'total_documents': len(data['ids']),
            'sample_metadata': data['metadatas'][:3] if data['metadatas'] else []
        }

# Интеграция традиционной и векторной базы знаний
class HybridKnowledgeBase:
    """Гибридная база знаний с текстовым и векторным поиском"""
    
    def __init__(self, storage_path="./hybrid_kb"):
        self.traditional_kb = ComprehensiveKnowledgeBase(storage_path)
        self.vector_kb = VectorKnowledgeBase("hybrid_collection")
    
    def add_document(self, content, metadata=None):
        """Добавление документа в обе системы"""
        # Добавляем в традиционную базу
        success = self.traditional_kb.add_document(content, metadata)
        
        if success:
            # Добавляем в векторную базу
            doc_id = list(self.traditional_kb.documents.keys())[-1]  # Последний добавленный
            self.vector_kb.add_document(content, metadata, doc_id)
            
        return success
    
    def hybrid_search(self, query, text_weight=0.3, vector_weight=0.7, max_results=10):
        """Гибридный поиск с комбинированием результатов"""
        # Текстовый поиск
        text_results = self.traditional_kb.search_documents(query)
        
        # Векторный поиск
        vector_results = self.vector_kb.search(query, n_results=max_results)
        
        # Комбинируем результаты
        combined_results = {}
        
        # Добавляем результаты текстового поиска
        for i, result in enumerate(text_results[:max_results]):
            doc_id = result['document']['id']
            score = text_weight * (1.0 - i / len(text_results))
            combined_results[doc_id] = {
                'document': result['document'],
                'score': score,
                'sources': ['text']
            }
        
        # Добавляем результаты векторного поиска
        for i, doc_id in enumerate(vector_results['ids']):
            # Конвертируем distance в similarity (меньшее расстояние = больше сходство)
            similarity = 1.0 / (1.0 + vector_results['distances'][i])
            score = vector_weight * similarity
            
            if doc_id in combined_results:
                combined_results[doc_id]['score'] += score
                combined_results[doc_id]['sources'].append('vector')
            else:
                # Получаем документ из традиционной базы
                if doc_id in self.traditional_kb.documents:
                    combined_results[doc_id] = {
                        'document': self.traditional_kb.documents[doc_id],
                        'score': score,
                        'sources': ['vector']
                    }
        
        # Сортируем по итоговому скору
        sorted_results = sorted(
            combined_results.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return sorted_results[:max_results]

# Пример использования гибридной системы
# hybrid_kb = HybridKnowledgeBase("./hybrid_knowledge")
# 
# # Добавление документов
# sample_docs = [
#     ("Машинное обучение - это область искусственного интеллекта", {"topic": "AI"}),
#     ("Python - популярный язык программирования для науки о данных", {"topic": "Programming"}),
#     ("Глубокое обучение использует нейронные сети", {"topic": "AI"})
# ]
# 
# for content, metadata in sample_docs:
#     hybrid_kb.add_document(content, metadata)
# 
# # Гибридный поиск
# results = hybrid_kb.hybrid_search("искусственный интеллект")
# print(f"Найдено {len(results)} результатов гибридного поиска")
```

## Ключевые моменты для экзамена

- **База знаний** - структурированное хранилище информации для AI систем
- **Источники данных** - документы, веб-страницы, API, базы данных, CRM системы
- **Форматы загрузки** - PDF, DOCX, HTML, TXT, JSON, CSV, XML
- **Веб-скрапинг** - извлечение контента из сайтов через BeautifulSoup
- **API интеграция** - загрузка данных через REST API и системы документооборота
- **Дедупликация** - устранение дублирующихся документов по хэшу контента
- **Метаданные** - информация о источнике, типе, дате добавления документа
- **Очистка данных** - удаление HTML тегов, лишних пробелов, спецсимволов
- **Векторизация** - создание эмбеддингов для семантического поиска
- **Гибридный поиск** - комбинирование текстового и векторного поиска
- **Индексация** - создание индексов для быстрого поиска и фильтрации
- **Качество данных** - анализ и улучшение качества контента в базе знаний