"""
Менеджер баз знаний для AI SEO Architects
Управляет загрузкой, векторизацией и поиском знаний для агентов с FAISS и OpenAI Embeddings
"""
import os
import pickle
import numpy as np
from typing import Dict, List, Optional, Any
from pathlib import Path
import faiss
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from core.config import config

class FAISSVectorStore:
    """FAISS-based векторная база с OpenAI Embeddings"""
    
    def __init__(self, documents: List[Document], embeddings_model: Optional[OpenAIEmbeddings]):
        self.documents = documents
        self.embeddings_model = embeddings_model
        self.index = None
        self.embeddings_cache = None
        self.dimension = 1536  # OpenAI text-embedding-ada-002 dimension
        
        if documents:
            self._build_index()
    
    def _build_index(self):
        """Строим FAISS индекс с OpenAI эмбеддингами"""
        print(f"🔄 Создание эмбеддингов для {len(self.documents)} документов...")
        
        # Проверяем доступность OpenAI Embeddings
        if self.embeddings_model is None:
            print("⚠️ OpenAI Embeddings недоступны, используем простой поиск")
            self._build_simple_index()
            return
        
        try:
            # Получаем тексты для эмбеддинга
            texts = [doc.page_content for doc in self.documents]
            
            # Создаем эмбеддинги через OpenAI
            embeddings_list = self.embeddings_model.embed_documents(texts)
            
            # Конвертируем в numpy array
            self.embeddings_cache = np.array(embeddings_list).astype('float32')
            
            # Создаем FAISS индекс (L2 distance)
            self.index = faiss.IndexFlatL2(self.dimension)
            
            # Добавляем эмбеддинги в индекс
            self.index.add(self.embeddings_cache)
            
            print(f"✅ FAISS индекс создан: {self.index.ntotal} векторов")
            
        except Exception as e:
            print(f"❌ Ошибка создания FAISS индекса: {e}")
            # Fallback к простому поиску
            self._build_simple_index()
    
    def _build_simple_index(self):
        """Fallback к простому поиску если OpenAI API недоступен"""
        print("🔄 Используем fallback к простому поиску...")
        self.simple_index = {}
        for i, doc in enumerate(self.documents):
            words = set(doc.page_content.lower().split())
            self.simple_index[i] = words
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Поиск похожих документов"""
        if self.index is not None:
            return self._faiss_search(query, k)
        else:
            return self._simple_search(query, k)
    
    def _faiss_search(self, query: str, k: int) -> List[Document]:
        """FAISS поиск с эмбеддингами"""
        if self.embeddings_model is None:
            return self._simple_search(query, k)
            
        try:
            # Создаем эмбеддинг для запроса
            query_embedding = self.embeddings_model.embed_query(query)
            query_vector = np.array([query_embedding]).astype('float32')
            
            # Поиск в FAISS индексе
            scores, indices = self.index.search(query_vector, min(k, len(self.documents)))
            
            # Формируем результаты
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx != -1 and idx < len(self.documents):  # Валидный индекс
                    results.append(self.documents[idx])
            
            return results
            
        except Exception as e:
            print(f"⚠️ Ошибка FAISS поиска: {e}")
            return self._simple_search(query, k)
    
    def _simple_search(self, query: str, k: int) -> List[Document]:
        """Простой поиск как fallback"""
        if not hasattr(self, 'simple_index'):
            self._build_simple_index()
        
        query_words = set(query.lower().split())
        scores = []
        
        for i, doc_words in self.simple_index.items():
            intersection = query_words & doc_words
            if intersection:
                score = len(intersection) / len(query_words | doc_words)
                scores.append((score, i))
        
        # Сортируем и берем топ-k
        scores.sort(reverse=True)
        results = []
        for score, i in scores[:k]:
            if score > 0.1:
                results.append(self.documents[i])
        
        return results
    
    def save_index(self, path: str):
        """Сохранение FAISS индекса на диск"""
        try:
            if self.index is not None:
                faiss.write_index(self.index, f"{path}/faiss.index")
                
                # Сохраняем метаданные
                metadata = {
                    'documents': self.documents,
                    'embeddings': self.embeddings_cache.tolist() if self.embeddings_cache is not None else None
                }
                
                with open(f"{path}/metadata.pkl", 'wb') as f:
                    pickle.dump(metadata, f)
                
                print(f"✅ FAISS индекс сохранен в {path}")
            
        except Exception as e:
            print(f"⚠️ Ошибка сохранения индекса: {e}")
    
    def load_index(self, path: str) -> bool:
        """Загрузка FAISS индекса с диска"""
        try:
            index_path = f"{path}/faiss.index"
            metadata_path = f"{path}/metadata.pkl"
            
            if os.path.exists(index_path) and os.path.exists(metadata_path):
                # Загружаем индекс
                self.index = faiss.read_index(index_path)
                
                # Загружаем метаданные
                with open(metadata_path, 'rb') as f:
                    metadata = pickle.load(f)
                
                self.documents = metadata['documents']
                if metadata['embeddings']:
                    self.embeddings_cache = np.array(metadata['embeddings']).astype('float32')
                
                print(f"✅ FAISS индекс загружен из {path}")
                return True
            
        except Exception as e:
            print(f"⚠️ Ошибка загрузки индекса: {e}")
        
        return False


class KnowledgeManager:
    """Менеджер для работы с базами знаний агентов"""
    
    def __init__(self):
        """Инициализация менеджера знаний"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.RAG_CHUNK_SIZE,
            chunk_overlap=config.RAG_CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        self.vector_stores: Dict[str, FAISSVectorStore] = {}
        self.knowledge_base_path = Path(config.KNOWLEDGE_BASE_PATH)
        
        # Инициализируем OpenAI Embeddings
        try:
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=config.OPENAI_API_KEY,
                model="text-embedding-ada-002"
            )
            print("✅ OpenAI Embeddings инициализированы")
        except Exception as e:
            print(f"⚠️ Ошибка инициализации OpenAI Embeddings: {e}")
            self.embeddings = None
        
        # Создаем директории если их нет
        os.makedirs(config.VECTOR_STORE_PATH, exist_ok=True)
        
    def load_agent_knowledge(self, agent_name: str, agent_level: str) -> FAISSVectorStore:
        """
        Загружает базу знаний для конкретного агента
        
        Args:
            agent_name: Имя агента (например, 'lead_qualification')
            agent_level: Уровень агента ('executive', 'management', 'operational')
            
        Returns:
            FAISSVectorStore: Векторное хранилище с знаниями агента
        """
        if agent_name in self.vector_stores:
            return self.vector_stores[agent_name]
            
        # Путь к файлам знаний агента
        knowledge_path = self.knowledge_base_path / agent_level
        
        documents = []
        
        # Загружаем markdown файлы с знаниями
        for md_file in knowledge_path.glob("*.md"):
            # Проверяем соответствие файла агенту
            if agent_name in md_file.stem or md_file.stem.replace('_', '') in agent_name.replace('_', ''):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Разбиваем на чанки
                        chunks = self.text_splitter.split_text(content)
                        
                        # Создаем документы
                        for i, chunk in enumerate(chunks):
                            doc = Document(
                                page_content=chunk,
                                metadata={
                                    "agent": agent_name,
                                    "level": agent_level,
                                    "source": md_file.name,
                                    "chunk_id": i
                                }
                            )
                            documents.append(doc)
                            
                        print(f"📄 Загружен файл {md_file.name}: {len(chunks)} чанков")
                        
                except Exception as e:
                    print(f"⚠️ Ошибка чтения файла {md_file}: {e}")
        
        # Создаем FAISS векторное хранилище
        if documents:
            if self.embeddings is None:
                print(f"⚠️ OpenAI Embeddings недоступны, используем fallback")
                # Создаем FAISSVectorStore без embeddings (будет использован simple fallback)
                vector_store = FAISSVectorStore(documents, None)
            else:
                vector_store = FAISSVectorStore(documents, self.embeddings)
                
            self.vector_stores[agent_name] = vector_store
            print(f"✅ Создано FAISS векторное хранилище для {agent_name} ({len(documents)} документов)")
            
            # Попытка загрузить сохраненный индекс
            index_path = f"{config.VECTOR_STORE_PATH}/{agent_name}"
            if vector_store.load_index(index_path):
                print(f"📦 Загружен сохраненный индекс для {agent_name}")
            else:
                # Сохраняем новый индекс
                os.makedirs(index_path, exist_ok=True)
                vector_store.save_index(index_path)
                print(f"💾 Сохранен новый индекс для {agent_name}")
            
            return vector_store
        else:
            print(f"⚠️ Знания для агента {agent_name} не найдены в {knowledge_path}")
            return None
    
    def search_knowledge(self, agent_name: str, query: str, k: int = None) -> List[Document]:
        """
        Поиск релевантных знаний для агента
        
        Args:
            agent_name: Имя агента
            query: Поисковый запрос
            k: Количество результатов (по умолчанию из конфигурации)
            
        Returns:
            List[Document]: Список релевантных документов
        """
        if agent_name not in self.vector_stores:
            print(f"⚠️ База знаний для агента {agent_name} не загружена")
            return []
            
        k = k or config.RAG_TOP_K
        
        try:
            # Используем простой поиск
            results = self.vector_stores[agent_name].similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"⚠️ Ошибка поиска знаний для {agent_name}: {e}")
            return []
    
    def add_knowledge(self, agent_name: str, content: str, metadata: Dict[str, Any]) -> None:
        """
        Добавляет новые знания в базу агента
        
        Args:
            agent_name: Имя агента
            content: Содержимое знаний
            metadata: Метаданные
        """
        if agent_name not in self.vector_stores:
            print(f"⚠️ База знаний для агента {agent_name} не найдена")
            return
            
        # Разбиваем на чанки
        chunks = self.text_splitter.split_text(content)
        
        documents = []
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={**metadata, "chunk_id": i}
            )
            documents.append(doc)
        
        # Добавляем документы в существующий список
        current_docs = self.vector_stores[agent_name].documents
        current_docs.extend(documents)
        
        # Пересоздаем FAISS индекс
        if self.embeddings is not None:
            self.vector_stores[agent_name] = FAISSVectorStore(current_docs, self.embeddings)
        else:
            self.vector_stores[agent_name] = FAISSVectorStore(current_docs, None)
        
        # Сохраняем обновленный индекс
        index_path = f"{config.VECTOR_STORE_PATH}/{agent_name}"
        os.makedirs(index_path, exist_ok=True)
        self.vector_stores[agent_name].save_index(index_path)
        
        print(f"✅ Добавлены знания для агента {agent_name}, индекс обновлен")
    
    def get_knowledge_context(self, agent_name: str, query: str, k: int = None) -> str:
        """
        Получает контекст знаний в виде строки для использования в промпте
        
        Args:
            agent_name: Имя агента
            query: Поисковый запрос
            k: Количество результатов
            
        Returns:
            str: Форматированный контекст знаний
        """
        relevant_docs = self.search_knowledge(agent_name, query, k)
        
        if not relevant_docs:
            return ""
        
        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            source = doc.metadata.get('source', 'unknown')
            content = doc.page_content.strip()
            context_parts.append(f"[Источник {i}: {source}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def initialize_all_agents_knowledge(self) -> Dict[str, bool]:
        """
        Инициализирует базы знаний для всех агентов
        
        Returns:
            Dict[str, bool]: Результаты инициализации для каждого агента
        """
        results = {}
        
        # Словарь соответствия агентов и их уровней
        agent_mappings = {
            # Executive level
            'chief_seo_strategist': 'executive',
            'business_development_director': 'executive',
            
            # Management level  
            'task_coordination': 'management',
            'sales_operations_manager': 'management',
            'technical_seo_operations_manager': 'management', 
            'client_success_manager': 'management',
            
            # Operational level
            'lead_qualification': 'operational',
            'sales_conversation': 'operational',
            'proposal_generation': 'operational',
            'technical_seo_auditor': 'operational',
            'content_strategy': 'operational',
            'link_building': 'operational',
            'competitive_analysis': 'operational',
            'reporting': 'operational'
        }
        
        print("🔄 Инициализация баз знаний для всех агентов...")
        
        for agent_name, agent_level in agent_mappings.items():
            try:
                vector_store = self.load_agent_knowledge(agent_name, agent_level)
                results[agent_name] = vector_store is not None
            except Exception as e:
                print(f"❌ Ошибка инициализации знаний для {agent_name}: {e}")
                results[agent_name] = False
        
        successful_count = sum(results.values())
        total_count = len(results)
        
        print(f"📊 Инициализация завершена: {successful_count}/{total_count} агентов")
        
        return results

# Глобальный менеджер знаний
knowledge_manager = KnowledgeManager()
