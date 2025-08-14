"""
Менеджер баз знаний для AI SEO Architects с ChromaDB
Управляет загрузкой, векторизацией и поиском знаний для агентов с ChromaDB и OpenAI Embeddings
"""
import os
import uuid
from typing import Dict, List, Optional, Any
from pathlib import Path
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from core.config import config


class ChromaVectorStore:
    """ChromaDB-based векторная база с OpenAI Embeddings"""
    
    def __init__(self, collection_name: str, embeddings_model: Optional[OpenAIEmbeddings]):
        self.collection_name = collection_name
        self.embeddings_model = embeddings_model
        
        # Инициализируем ChromaDB клиент
        chroma_settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=config.VECTOR_STORE_PATH,
            anonymized_telemetry=False
        )
        
        self.client = chromadb.Client(chroma_settings)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self._get_embedding_function()
        )
        
        print(f"✅ ChromaDB коллекция '{collection_name}' инициализирована")
    
    def _get_embedding_function(self):
        """Создает embedding функцию для ChromaDB"""
        if self.embeddings_model is None:
            # Используем встроенную функцию ChromaDB
            return None
        
        # Обертка для OpenAI Embeddings
        class OpenAIEmbeddingFunction:
            def __init__(self, embeddings_model):
                self.embeddings_model = embeddings_model
            
            def __call__(self, texts):
                if isinstance(texts, str):
                    texts = [texts]
                return self.embeddings_model.embed_documents(texts)
        
        return OpenAIEmbeddingFunction(self.embeddings_model)
    
    def add_documents(self, documents: List[Document]):
        """Добавляет документы в ChromaDB коллекцию"""
        try:
            # Подготавливаем данные для ChromaDB
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            ids = [str(uuid.uuid4()) for _ in documents]
            
            # Добавляем в коллекцию
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ Добавлено {len(documents)} документов в ChromaDB коллекцию '{self.collection_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка добавления документов в ChromaDB: {e}")
            return False
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Поиск похожих документов в ChromaDB"""
        try:
            # Выполняем поиск в ChromaDB
            results = self.collection.query(
                query_texts=[query],
                n_results=min(k, self.collection.count())
            )
            
            # Преобразуем результаты в Document объекты
            documents = []
            if results['documents'] and len(results['documents'][0]) > 0:
                for i in range(len(results['documents'][0])):
                    doc = Document(
                        page_content=results['documents'][0][i],
                        metadata=results['metadatas'][0][i] if results['metadatas'][0] else {}
                    )
                    documents.append(doc)
            
            return documents
            
        except Exception as e:
            print(f"❌ Ошибка поиска в ChromaDB: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Получает статистику коллекции"""
        try:
            count = self.collection.count()
            return {
                "name": self.collection_name,
                "documents_count": count,
                "status": "active"
            }
        except Exception as e:
            return {
                "name": self.collection_name,
                "error": str(e),
                "status": "error"
            }


class ChromaKnowledgeManager:
    """Менеджер для работы с базами знаний агентов через ChromaDB"""
    
    def __init__(self):
        """Инициализация менеджера знаний с ChromaDB"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.RAG_CHUNK_SIZE,
            chunk_overlap=config.RAG_CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        self.vector_stores: Dict[str, ChromaVectorStore] = {}
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
    
    def load_agent_knowledge(self, agent_name: str, agent_level: str) -> ChromaVectorStore:
        """
        Загружает базу знаний для конкретного агента в ChromaDB
        
        Args:
            agent_name: Имя агента (например, 'lead_qualification')
            agent_level: Уровень агента ('executive', 'management', 'operational')
            
        Returns:
            ChromaVectorStore: Векторное хранилище с знаниями агента
        """
        if agent_name in self.vector_stores:
            return self.vector_stores[agent_name]
        
        # Создаем ChromaDB коллекцию для агента
        collection_name = f"{agent_level}_{agent_name}"
        vector_store = ChromaVectorStore(collection_name, self.embeddings)
        
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
        
        # Добавляем документы в ChromaDB
        if documents:
            success = vector_store.add_documents(documents)
            if success:
                self.vector_stores[agent_name] = vector_store
                print(f"✅ Создано ChromaDB векторное хранилище для {agent_name} ({len(documents)} документов)")
                return vector_store
            else:
                print(f"❌ Ошибка создания ChromaDB хранилища для {agent_name}")
                return None
        else:
            print(f"⚠️ Знания для агента {agent_name} не найдены в {knowledge_path}")
            return None
    
    def search_knowledge(self, agent_name: str, query: str, k: int = None) -> List[Document]:
        """
        Поиск релевантных знаний для агента через ChromaDB
        
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
            results = self.vector_stores[agent_name].similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"⚠️ Ошибка поиска знаний для {agent_name}: {e}")
            return []
    
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
        Инициализирует базы знаний для всех агентов в ChromaDB
        
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
        
        print("🔄 Инициализация баз знаний для всех агентов в ChromaDB...")
        
        for agent_name, agent_level in agent_mappings.items():
            try:
                vector_store = self.load_agent_knowledge(agent_name, agent_level)
                results[agent_name] = vector_store is not None
            except Exception as e:
                print(f"❌ Ошибка инициализации знаний для {agent_name}: {e}")
                results[agent_name] = False
        
        successful_count = sum(results.values())
        total_count = len(results)
        
        print(f"📊 Инициализация ChromaDB завершена: {successful_count}/{total_count} агентов")
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Получает общую статистику ChromaDB менеджера"""
        stats = {
            "vector_stores_count": len(self.vector_stores),
            "embeddings_available": self.embeddings is not None,
            "stores": {}
        }
        
        for agent_name, store in self.vector_stores.items():
            stats["stores"][agent_name] = store.get_collection_stats()
        
        return stats


# Глобальный менеджер знаний с ChromaDB
knowledge_manager = ChromaKnowledgeManager()