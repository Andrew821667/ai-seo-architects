"""
Менеджер баз знаний для AI SEO Architects
Управляет загрузкой, векторизацией и поиском знаний для агентов
"""
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from core.config import config

class KnowledgeManager:
    """Менеджер для работы с базами знаний агентов"""
    
    def __init__(self):
        """Инициализация менеджера знаний"""
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )
        self.vector_stores: Dict[str, Chroma] = {}
        self.knowledge_base_path = Path("knowledge")
        
    def load_agent_knowledge(self, agent_name: str, agent_level: str) -> Chroma:
        """
        Загружает базу знаний для конкретного агента
        
        Args:
            agent_name: Имя агента (например, 'lead_qualification')
            agent_level: Уровень агента ('executive', 'management', 'operational')
            
        Returns:
            Chroma: Векторное хранилище с знаниями агента
        """
        if agent_name in self.vector_stores:
            return self.vector_stores[agent_name]
            
        # Путь к файлам знаний агента
        knowledge_path = self.knowledge_base_path / agent_level
        
        documents = []
        
        # Загружаем markdown файлы с знаниями
        for md_file in knowledge_path.glob("*.md"):
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
        
        # Создаем векторное хранилище
        if documents:
            vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=f"{config.CHROMA_PERSIST_DIR}/{agent_name}",
                collection_name=agent_name
            )
            
            self.vector_stores[agent_name] = vector_store
            return vector_store
        else:
            print(f"⚠️ Знания для агента {agent_name} не найдены в {knowledge_path}")
            return None
    
    def search_knowledge(self, agent_name: str, query: str, k: int = 3) -> List[Document]:
        """
        Поиск релевантных знаний для агента
        
        Args:
            agent_name: Имя агента
            query: Поисковый запрос
            k: Количество результатов
            
        Returns:
            List[Document]: Список релевантных документов
        """
        if agent_name not in self.vector_stores:
            print(f"⚠️ База знаний для агента {agent_name} не загружена")
            return []
            
        return self.vector_stores[agent_name].similarity_search(query, k=k)
    
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
        
        # Добавляем в векторное хранилище
        self.vector_stores[agent_name].add_documents(documents)
        print(f"✅ Добавлены знания для агента {agent_name}")

# Глобальный менеджер знаний
knowledge_manager = KnowledgeManager()
