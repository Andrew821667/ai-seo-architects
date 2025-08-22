# Тема 20: Диалоги в ИИ системах

## Основы диалоговых систем

### Типы диалогов
- **Task-oriented dialogs**: Целевые диалоги для выполнения задач
- **Open-domain dialogs**: Свободные беседы без конкретной цели
- **Question-answering**: Системы вопрос-ответ
- **Multi-turn conversations**: Многоходовые диалоги с контекстом

### Архитектура диалоговых систем
```python
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    metadata: Optional[Dict] = None

@dataclass
class Dialog:
    dialog_id: str
    messages: List[Message]
    context: Dict
    status: str = 'active'  # 'active', 'completed', 'aborted'
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Добавление сообщения в диалог"""
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.messages.append(message)
    
    def get_conversation_history(self, max_messages: int = 10) -> List[Dict]:
        """Получение истории диалога для модели"""
        recent_messages = self.messages[-max_messages:]
        return [
            {"role": msg.role, "content": msg.content}
            for msg in recent_messages
        ]
    
    def get_context_summary(self) -> str:
        """Получение краткого содержания контекста"""
        user_messages = [msg.content for msg in self.messages if msg.role == 'user']
        return f"Диалог содержит {len(self.messages)} сообщений. " \
               f"Пользователь задал {len(user_messages)} вопросов."

# Пример создания диалога
dialog = Dialog(
    dialog_id="conv_001",
    messages=[],
    context={"user_id": "user123", "topic": "technical_support"}
)

dialog.add_message("user", "Привет! У меня проблема с приложением.")
dialog.add_message("assistant", "Здравствуйте! Расскажите подробнее о проблеме.")
dialog.add_message("user", "Приложение зависает при загрузке.")
```

## Управление контекстом диалога

### Хранение и обновление контекста
```python
import json
from typing import Any

class ConversationContextManager:
    def __init__(self):
        self.context = {}
        self.max_context_length = 10000  # максимальная длина контекста
    
    def update_context(self, key: str, value: Any):
        """Обновление контекста"""
        self.context[key] = value
    
    def get_context(self, key: str, default=None):
        """Получение значения из контекста"""
        return self.context.get(key, default)
    
    def extract_entities_from_message(self, message: str) -> Dict:
        """Извлечение сущностей из сообщения"""
        # Простой пример извлечения сущностей
        entities = {}
        
        # Извлечение имен (начинаются с заглавной буквы)
        import re
        names = re.findall(r'\b[А-ЯA-Z][а-яa-z]+\b', message)
        if names:
            entities['names'] = names
        
        # Извлечение дат
        dates = re.findall(r'\d{1,2}\.\d{1,2}\.\d{4}', message)
        if dates:
            entities['dates'] = dates
        
        # Извлечение номеров телефонов
        phones = re.findall(r'\+?\d[\d\s\-\(\)]{8,}\d', message)
        if phones:
            entities['phones'] = phones
        
        return entities
    
    def update_context_from_message(self, message: str, role: str):
        """Обновление контекста на основе сообщения"""
        entities = self.extract_entities_from_message(message)
        
        # Обновление контекста извлеченными сущностями
        for entity_type, values in entities.items():
            current_values = self.get_context(entity_type, [])
            updated_values = list(set(current_values + values))
            self.update_context(entity_type, updated_values)
        
        # Обновление счетчиков сообщений
        message_count = self.get_context(f'{role}_message_count', 0)
        self.update_context(f'{role}_message_count', message_count + 1)
    
    def get_context_for_prompt(self) -> str:
        """Формирование контекста для промпта"""
        context_parts = []
        
        # Добавление информации о пользователе
        if self.get_context('names'):
            context_parts.append(f"Имена в диалоге: {', '.join(self.get_context('names'))}")
        
        # Добавление статистики диалога
        user_count = self.get_context('user_message_count', 0)
        assistant_count = self.get_context('assistant_message_count', 0)
        context_parts.append(f"Сообщений пользователя: {user_count}, ответов ассистента: {assistant_count}")
        
        return " | ".join(context_parts)

# Пример использования
context_manager = ConversationContextManager()
context_manager.update_context_from_message("Меня зовут Анна, у меня проблема", "user")
context_manager.update_context_from_message("Привет, Анна! Как дела?", "assistant")

print(context_manager.get_context_for_prompt())
```

### Сжатие длинных диалогов
```python
class DialogCompressor:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
    
    def estimate_tokens(self, text: str) -> int:
        """Приблизительная оценка количества токенов"""
        # Простая эвристика: 1 токен ≈ 4 символа для русского языка
        return len(text) // 3
    
    def compress_messages(self, messages: List[Dict]) -> List[Dict]:
        """Сжатие диалога с сохранением важной информации"""
        if not messages:
            return messages
        
        total_tokens = sum(self.estimate_tokens(msg['content']) for msg in messages)
        
        if total_tokens <= self.max_tokens:
            return messages
        
        # Сохраняем последние сообщения и системные промпты
        compressed = []
        current_tokens = 0
        
        # Сначала добавляем системные сообщения
        for msg in messages:
            if msg['role'] == 'system':
                compressed.append(msg)
                current_tokens += self.estimate_tokens(msg['content'])
        
        # Затем добавляем последние сообщения
        for msg in reversed(messages):
            if msg['role'] != 'system':
                msg_tokens = self.estimate_tokens(msg['content'])
                if current_tokens + msg_tokens <= self.max_tokens:
                    compressed.insert(-len([m for m in compressed if m['role'] == 'system']), msg)
                    current_tokens += msg_tokens
                else:
                    break
        
        # Добавляем сводку пропущенных сообщений
        if len(compressed) < len(messages):
            skipped_count = len(messages) - len(compressed)
            summary_msg = {
                'role': 'system',
                'content': f'[Пропущено {skipped_count} сообщений из-за ограничения длины]'
            }
            compressed.insert(1, summary_msg)
        
        return compressed
    
    def create_conversation_summary(self, messages: List[Dict]) -> str:
        """Создание краткого содержания диалога"""
        user_messages = [msg['content'] for msg in messages if msg['role'] == 'user']
        assistant_messages = [msg['content'] for msg in messages if msg['role'] == 'assistant']
        
        # Извлечение ключевых тем
        topics = set()
        keywords = ['проблема', 'вопрос', 'помощь', 'ошибка', 'настройка']
        
        for msg in user_messages:
            for keyword in keywords:
                if keyword in msg.lower():
                    topics.add(keyword)
        
        summary = f"""Диалог содержит:
        - {len(user_messages)} сообщений пользователя
        - {len(assistant_messages)} ответов ассистента
        - Основные темы: {', '.join(topics) if topics else 'общение'}"""
        
        return summary

# Пример использования
compressor = DialogCompressor(max_tokens=1000)

long_dialog = [
    {'role': 'system', 'content': 'Вы полезный ассистент.'},
    {'role': 'user', 'content': 'Привет, у меня вопрос про настройку системы.'},
    {'role': 'assistant', 'content': 'Здравствуйте! Расскажите подробнее о проблеме.'},
    # ... много сообщений
]

compressed = compressor.compress_messages(long_dialog)
```

## Паттерны диалогов

### Структурированные диалоги с состояниями
```python
from enum import Enum
from typing import Callable

class DialogState(Enum):
    GREETING = "greeting"
    COLLECTING_INFO = "collecting_info"
    PROCESSING = "processing"
    PROVIDING_ANSWER = "providing_answer"
    CLOSING = "closing"

class StatefulDialog:
    def __init__(self):
        self.state = DialogState.GREETING
        self.collected_info = {}
        self.required_fields = ['name', 'email', 'issue']
    
    def handle_message(self, user_message: str) -> str:
        """Обработка сообщения в зависимости от текущего состояния"""
        
        if self.state == DialogState.GREETING:
            return self._handle_greeting(user_message)
        elif self.state == DialogState.COLLECTING_INFO:
            return self._handle_info_collection(user_message)
        elif self.state == DialogState.PROCESSING:
            return self._handle_processing(user_message)
        elif self.state == DialogState.PROVIDING_ANSWER:
            return self._handle_answer(user_message)
        elif self.state == DialogState.CLOSING:
            return self._handle_closing(user_message)
    
    def _handle_greeting(self, message: str) -> str:
        self.state = DialogState.COLLECTING_INFO
        return "Привет! Чтобы помочь вам, мне нужна некоторая информация. Как вас зовут?"
    
    def _handle_info_collection(self, message: str) -> str:
        # Определяем, какую информацию пользователь предоставил
        if 'name' not in self.collected_info:
            self.collected_info['name'] = message.strip()
            return "Спасибо! Теперь укажите ваш email для связи."
        
        elif 'email' not in self.collected_info:
            if '@' in message:
                self.collected_info['email'] = message.strip()
                return "Отлично! Теперь опишите вашу проблему."
            else:
                return "Пожалуйста, укажите корректный email адрес."
        
        elif 'issue' not in self.collected_info:
            self.collected_info['issue'] = message.strip()
            self.state = DialogState.PROCESSING
            return "Спасибо за информацию! Обрабатываю ваш запрос..."
    
    def _handle_processing(self, message: str) -> str:
        # Имитация обработки
        self.state = DialogState.PROVIDING_ANSWER
        return f"Здравствуйте, {self.collected_info['name']}! " \
               f"По вашей проблеме '{self.collected_info['issue']}' " \
               f"рекомендую следующее решение..."
    
    def _handle_answer(self, message: str) -> str:
        if any(word in message.lower() for word in ['спасибо', 'thanks', 'понятно']):
            self.state = DialogState.CLOSING
            return "Рад помочь! Есть ли у вас еще вопросы?"
        else:
            return "Нужны ли дополнительные пояснения по решению?"
    
    def _handle_closing(self, message: str) -> str:
        if any(word in message.lower() for word in ['нет', 'no', 'все']):
            return "Отлично! Хорошего дня!"
        else:
            self.state = DialogState.COLLECTING_INFO
            return "Конечно! Расскажите, чем еще могу помочь?"

# Пример использования
dialog = StatefulDialog()
print(dialog.handle_message("Привет"))
print(dialog.handle_message("Иван"))
print(dialog.handle_message("ivan@example.com"))
print(dialog.handle_message("Не работает принтер"))
```

### Диалоги с намерениями (Intent Recognition)
```python
import re
from typing import Tuple

class IntentClassifier:
    def __init__(self):
        self.intent_patterns = {
            'technical_support': [
                r'(не работает|проблема|ошибка|сломалось)',
                r'(как настроить|как установить|как исправить)',
                r'(помогите|поддержка|техподдержка)'
            ],
            'information_request': [
                r'(что такое|расскажите|объясните)',
                r'(где найти|где посмотреть|где скачать)',
                r'(какой|какая|какие|сколько)'
            ],
            'greeting': [
                r'(привет|здравствуйте|добро пожаловать)',
                r'(как дела|как поживаете)',
                r'(доброе утро|добрый день|добрый вечер)'
            ],
            'goodbye': [
                r'(пока|до свидания|увидимся)',
                r'(спасибо|благодарю)',
                r'(все|хватит|достаточно)'
            ]
        }
    
    def classify_intent(self, message: str) -> Tuple[str, float]:
        """Классификация намерения пользователя"""
        message = message.lower()
        best_intent = 'unknown'
        best_score = 0.0
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message):
                    score += 1
            
            # Нормализация по количеству паттернов
            normalized_score = score / len(patterns)
            
            if normalized_score > best_score:
                best_score = normalized_score
                best_intent = intent
        
        return best_intent, best_score
    
    def extract_entities(self, message: str, intent: str) -> Dict:
        """Извлечение сущностей в зависимости от намерения"""
        entities = {}
        
        if intent == 'technical_support':
            # Извлечение названий продуктов/устройств
            devices = re.findall(r'(принтер|компьютер|телефон|приложение|программа)', message.lower())
            if devices:
                entities['device'] = devices[0]
        
        elif intent == 'information_request':
            # Извлечение тем запроса
            topics = re.findall(r'(настройка|установка|обновление|функция)', message.lower())
            if topics:
                entities['topic'] = topics[0]
        
        return entities

class IntentBasedDialog:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.context = {}
    
    def handle_message(self, message: str) -> str:
        """Обработка сообщения на основе намерения"""
        intent, confidence = self.classifier.classify_intent(message)
        entities = self.classifier.extract_entities(message, intent)
        
        # Сохранение контекста
        self.context['last_intent'] = intent
        self.context['entities'] = entities
        
        # Генерация ответа в зависимости от намерения
        if intent == 'greeting':
            return "Здравствуйте! Как дела? Чем могу помочь?"
        
        elif intent == 'technical_support':
            device = entities.get('device', 'устройство')
            return f"Понял, у вас проблема с {device}. Опишите подробнее, что именно не работает?"
        
        elif intent == 'information_request':
            topic = entities.get('topic', 'этой теме')
            return f"Конечно! Расскажу вам о {topic}. Что именно вас интересует?"
        
        elif intent == 'goodbye':
            return "До свидания! Обращайтесь, если понадобится помощь!"
        
        else:
            return "Извините, не совсем понял ваш запрос. Можете переформулировать?"

# Пример использования
dialog = IntentBasedDialog()
print(dialog.handle_message("Привет! Как дела?"))
print(dialog.handle_message("У меня не работает принтер"))
print(dialog.handle_message("Расскажите про настройку WiFi"))
```

## Интеграция с языковыми моделями

### Промпт-инжиниринг для диалогов
```python
class DialogPromptBuilder:
    def __init__(self):
        self.system_prompt = """Вы полезный ассистент, который ведет диалог с пользователем.
        
        Правила поведения:
        1. Будьте вежливы и профессиональны
        2. Задавайте уточняющие вопросы при необходимости
        3. Предоставляйте конкретные и полезные ответы
        4. Помните контекст предыдущих сообщений
        5. Если не знаете ответа, честно об этом скажите
        """
    
    def build_conversation_prompt(self, dialog_history: List[Dict], 
                                 user_context: str = "") -> List[Dict]:
        """Построение промпта для модели на основе истории диалога"""
        
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Добавление контекста пользователя
        if user_context:
            context_message = {
                "role": "system", 
                "content": f"Дополнительный контекст: {user_context}"
            }
            messages.append(context_message)
        
        # Добавление истории диалога
        messages.extend(dialog_history)
        
        return messages
    
    def add_persona(self, persona: str):
        """Добавление персоны ассистента"""
        self.system_prompt += f"\n\nВаша роль: {persona}"
    
    def add_domain_knowledge(self, domain: str, knowledge: str):
        """Добавление знаний о предметной области"""
        domain_prompt = f"\n\nЗнания в области '{domain}':\n{knowledge}"
        self.system_prompt += domain_prompt

# Пример создания специализированного диалога
tech_support_prompt = DialogPromptBuilder()
tech_support_prompt.add_persona("Специалист технической поддержки с 5-летним опытом")
tech_support_prompt.add_domain_knowledge(
    "Компьютерная техника",
    "Знаете устройство ПК, операционные системы Windows/Linux/MacOS, "
    "основные проблемы с оборудованием и программным обеспечением"
)

dialog_history = [
    {"role": "user", "content": "Привет! У меня проблема с компьютером."},
    {"role": "assistant", "content": "Здравствуйте! Расскажите подробнее о проблеме."},
    {"role": "user", "content": "Компьютер очень медленно загружается."}
]

prompt = tech_support_prompt.build_conversation_prompt(
    dialog_history, 
    "Пользователь: Windows 10, 8GB RAM, SSD диск"
)
```

## Ключевые моменты для экзамена

### Компоненты диалоговых систем
1. **Управление состоянием** - отслеживание этапов диалога
2. **Контекстная память** - сохранение информации между сообщениями  
3. **Классификация намерений** - понимание целей пользователя
4. **Извлечение сущностей** - выделение ключевой информации
5. **Генерация ответов** - формирование релевантных реплик

### Архитектурные паттерны
- **Конечные автоматы** для структурированных диалогов
- **Slot-filling** для сбора информации
- **Multi-turn reasoning** для сложных диалогов
- **Context compression** для длинных разговоров

### Практические навыки
- Проектирование схем диалогов
- Управление контекстом и памятью
- Интеграция с языковыми моделями
- Обработка ошибок и неоднозначностей
- Персонализация диалогов

### Технические решения
- Хранение состояния диалога в базе данных
- Кэширование контекста для производительности
- Асинхронная обработка сообщений
- Логирование и аналитика диалогов
- A/B тестирование разных стратегий