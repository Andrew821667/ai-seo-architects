"""
Менеджер баз знаний для AI SEO Architects
Управляет загрузкой, векторизацией и поиском знаний для агентов
"""
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from core.config import config

# Простая in-memory векторная база для демонстрации
import re
import math

class SimpleVectorStore:
    """Простая in-memory векторная база для демонстрации"""
    
    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.index = {}
        self._build_index()
    
    def _build_index(self):
        """Строим простой индекс на основе TF-IDF"""
        for i, doc in enumerate(self.documents):
            words = re.findall(r'\b\w+\b', doc.page_content.lower())
            self.index[i] = set(words)
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Улучшенный поиск по пересечению слов с расширенным scoring"""
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        scores = []
        
        for i, doc_words in self.index.items():
            doc_content = self.documents[i].page_content.lower()
            
            # 1. Жакардово сходство
            intersection = query_words & doc_words
            union = query_words | doc_words
            jaccard_score = len(intersection) / len(union) if union else 0
            
            # 2. Прямое вхождение слов (более высокий вес)
            direct_matches = sum(1 for word in query_words if word in doc_content)
            direct_score = direct_matches / len(query_words) if query_words else 0
            
            # 3. Бонус за точные фразы
            phrase_bonus = 0
            query_text = query.lower()
            if query_text in doc_content:
                phrase_bonus = 0.3
            
            # Комбинированный скор
            final_score = (jaccard_score * 0.4) + (direct_score * 0.5) + phrase_bonus
            scores.append((final_score, i))
        
        # Сортируем по скору и берем топ-k
        scores.sort(reverse=True)
        results = []
        for score, i in scores[:k]:
            if score > 0.05:  # Снижаем threshold для более гибкого поиска
                results.append(self.documents[i])
        
        return results


class KnowledgeManager:
    """Менеджер для работы с базами знаний агентов"""
    
    def __init__(self):
        """Инициализация менеджера знаний"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.RAG_CHUNK_SIZE,
            chunk_overlap=config.RAG_CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        self.vector_stores: Dict[str, SimpleVectorStore] = {}
        self.knowledge_base_path = Path(config.KNOWLEDGE_BASE_PATH)
        
        # Создаем директории если их нет
        os.makedirs(os.path.dirname(config.CHROMA_PERSIST_DIR), exist_ok=True)
        
    def load_agent_knowledge(self, agent_name: str, agent_level: str) -> SimpleVectorStore:
        """
        Загружает базу знаний для конкретного агента
        
        Args:
            agent_name: Имя агента (например, 'lead_qualification')
            agent_level: Уровень агента ('executive', 'management', 'operational')
            
        Returns:
            SimpleVectorStore: Векторное хранилище с знаниями агента
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
        
        # Создаем векторное хранилище
        if documents:
            vector_store = SimpleVectorStore(documents)
            self.vector_stores[agent_name] = vector_store
            print(f"✅ Создано векторное хранилище для {agent_name} ({len(documents)} документов)")
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
        
        # Пересоздаем индекс
        self.vector_stores[agent_name] = SimpleVectorStore(current_docs)
        print(f"✅ Добавлены знания для агента {agent_name}")
    
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
