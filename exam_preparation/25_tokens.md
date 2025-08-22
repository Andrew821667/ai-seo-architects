# Тема 25: Токены в языковых моделях

## Основы токенизации

### Что такое токены
- **Определение**: Базовые единицы обработки текста в языковых моделях
- **Назначение**: Преобразование текста в числовую форму для обработки
- **Типы**: Слова, подслова, символы, специальные токены
- **Влияние**: Качество токенизации влияет на понимание и генерацию текста

### Процесс токенизации
```python
import re
from typing import List, Dict, Tuple, Optional
from collections import Counter
import json

class BasicTokenizer:
    """Базовый токенизатор для демонстрации принципов"""
    
    def __init__(self):
        self.vocab = {}
        self.reverse_vocab = {}
        self.special_tokens = {
            '<PAD>': 0,
            '<UNK>': 1,
            '<BOS>': 2,  # Beginning of sequence
            '<EOS>': 3,  # End of sequence
        }
        self.vocab_size = len(self.special_tokens)
    
    def build_vocab(self, texts: List[str], min_freq: int = 1) -> Dict[str, int]:
        """Построение словаря на основе корпуса текстов"""
        # Подсчет частоты токенов
        token_counts = Counter()
        
        for text in texts:
            tokens = self._basic_tokenize(text)
            token_counts.update(tokens)
        
        # Добавляем специальные токены
        self.vocab = self.special_tokens.copy()
        
        # Добавляем обычные токены с частотой >= min_freq
        for token, count in token_counts.items():
            if count >= min_freq:
                self.vocab[token] = self.vocab_size
                self.vocab_size += 1
        
        # Создаем обратный словарь
        self.reverse_vocab = {v: k for k, v in self.vocab.items()}
        
        return self.vocab
    
    def _basic_tokenize(self, text: str) -> List[str]:
        """Базовая токенизация (по словам и знакам препинания)"""
        # Простая токенизация по пробелам и знакам препинания
        tokens = re.findall(r'\w+|[^\w\s]', text.lower())
        return tokens
    
    def encode(self, text: str) -> List[int]:
        """Кодирование текста в список ID токенов"""
        tokens = self._basic_tokenize(text)
        token_ids = []
        
        for token in tokens:
            if token in self.vocab:
                token_ids.append(self.vocab[token])
            else:
                token_ids.append(self.vocab['<UNK>'])  # Unknown token
        
        return token_ids
    
    def decode(self, token_ids: List[int]) -> str:
        """Декодирование ID токенов обратно в текст"""
        tokens = []
        
        for token_id in token_ids:
            if token_id in self.reverse_vocab:
                token = self.reverse_vocab[token_id]
                if token not in self.special_tokens:
                    tokens.append(token)
        
        return ' '.join(tokens)
    
    def get_vocab_size(self) -> int:
        """Размер словаря"""
        return self.vocab_size
    
    def save_vocab(self, filepath: str):
        """Сохранение словаря"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.vocab, f, ensure_ascii=False, indent=2)
    
    def load_vocab(self, filepath: str):
        """Загрузка словаря"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.vocab = json.load(f)
        
        self.reverse_vocab = {v: k for k, v in self.vocab.items()}
        self.vocab_size = len(self.vocab)

# Пример использования базового токенизатора
texts = [
    "Привет, как дела?",
    "Хорошо, спасибо!",
    "Что нового?",
    "Ничего особенного.",
    "Увидимся позже!"
]

tokenizer = BasicTokenizer()
vocab = tokenizer.build_vocab(texts, min_freq=1)

print("Словарь токенов:")
for token, token_id in list(vocab.items())[:10]:
    print(f"'{token}': {token_id}")

# Кодирование и декодирование
test_text = "Привет, как дела сегодня?"
encoded = tokenizer.encode(test_text)
decoded = tokenizer.decode(encoded)

print(f"\nИсходный текст: {test_text}")
print(f"Закодированный: {encoded}")
print(f"Декодированный: {decoded}")
```

### Типы токенизации
```python
import tiktoken  # Библиотека OpenAI для токенизации
from transformers import AutoTokenizer
import sentencepiece as spm

class TokenizationComparison:
    """Сравнение различных подходов к токенизации"""
    
    def __init__(self):
        # Различные токенизаторы для сравнения
        self.tokenizers = {}
        
        # GPT токенизатор (если доступен)
        try:
            self.tokenizers['gpt'] = tiktoken.get_encoding("cl100k_base")
        except:
            print("tiktoken недоступен")
        
        # Hugging Face токенизатор
        try:
            self.tokenizers['bert'] = AutoTokenizer.from_pretrained('bert-base-multilingual-cased')
        except:
            print("transformers недоступен")
    
    def compare_tokenization(self, text: str) -> Dict[str, Dict]:
        """Сравнение токенизации разными методами"""
        results = {}
        
        # Пословная токенизация
        word_tokens = text.split()
        results['word_based'] = {
            'tokens': word_tokens,
            'count': len(word_tokens),
            'method': 'Разделение по пробелам'
        }
        
        # Посимвольная токенизация
        char_tokens = list(text)
        results['char_based'] = {
            'tokens': char_tokens[:20],  # Первые 20 для краткости
            'count': len(char_tokens),
            'method': 'Каждый символ - отдельный токен'
        }
        
        # GPT токенизация
        if 'gpt' in self.tokenizers:
            gpt_tokens = self.tokenizers['gpt'].encode(text)
            gpt_decoded = [self.tokenizers['gpt'].decode([token]) for token in gpt_tokens]
            results['gpt_bpe'] = {
                'tokens': gpt_decoded[:20],
                'count': len(gpt_tokens),
                'method': 'BPE (Byte Pair Encoding) от OpenAI'
            }
        
        # BERT токенизация
        if 'bert' in self.tokenizers:
            bert_tokens = self.tokenizers['bert'].tokenize(text)
            results['bert_wordpiece'] = {
                'tokens': bert_tokens[:20],
                'count': len(bert_tokens),
                'method': 'WordPiece от Google'
            }
        
        return results
    
    def analyze_efficiency(self, texts: List[str]) -> Dict[str, Dict]:
        """Анализ эффективности разных методов токенизации"""
        analysis = {}
        
        for method_name in ['word_based', 'char_based', 'gpt_bpe', 'bert_wordpiece']:
            total_tokens = 0
            total_chars = 0
            
            for text in texts:
                comparison = self.compare_tokenization(text)
                if method_name in comparison:
                    total_tokens += comparison[method_name]['count']
                    total_chars += len(text)
            
            if total_tokens > 0:
                analysis[method_name] = {
                    'avg_tokens_per_text': total_tokens / len(texts),
                    'compression_ratio': total_chars / total_tokens,
                    'tokens_per_char': total_tokens / total_chars
                }
        
        return analysis

# Демонстрация различных подходов
comparison = TokenizationComparison()

test_texts = [
    "Привет, как дела?",
    "Искусственный интеллект развивается быстро.",
    "Machine learning is transforming technology.",
    "Это предложение содержит числа: 123, даты: 2024-01-15, и email: test@example.com"
]

print("Сравнение методов токенизации:")
print("=" * 50)

for i, text in enumerate(test_texts[:2]):  # Первые 2 текста для краткости
    print(f"\nТекст {i+1}: {text}")
    print("-" * 30)
    
    results = comparison.compare_tokenization(text)
    
    for method, data in results.items():
        print(f"{data['method']}:")
        print(f"  Количество токенов: {data['count']}")
        print(f"  Первые токены: {data['tokens'][:10]}")
        print()

# Анализ эффективности
efficiency = comparison.analyze_efficiency(test_texts)
print("Анализ эффективности:")
print("-" * 30)

for method, stats in efficiency.items():
    print(f"{method}:")
    print(f"  Среднее токенов на текст: {stats['avg_tokens_per_text']:.2f}")
    print(f"  Коэффициент сжатия: {stats['compression_ratio']:.2f}")
    print(f"  Токенов на символ: {stats['tokens_per_char']:.3f}")
    print()
```

## Управление контекстом и ограничениями

### Подсчет и оптимизация токенов
```python
class TokenOptimizer:
    """Оптимизация использования токенов"""
    
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except:
            self.tokenizer = None
    
    def count_tokens(self, text: str) -> int:
        """Подсчет количества токенов в тексте"""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Приблизительная оценка: 1 токен ≈ 4 символа для английского
            # Для русского может быть меньше
            return len(text) // 3
    
    def truncate_text(self, text: str, max_tokens: int = None) -> str:
        """Обрезка текста до указанного количества токенов"""
        if max_tokens is None:
            max_tokens = self.max_tokens
        
        if self.tokenizer:
            tokens = self.tokenizer.encode(text)
            if len(tokens) <= max_tokens:
                return text
            
            truncated_tokens = tokens[:max_tokens]
            return self.tokenizer.decode(truncated_tokens)
        else:
            # Приблизительная обрезка по символам
            estimated_chars = max_tokens * 3
            return text[:estimated_chars]
    
    def smart_truncate(self, text: str, max_tokens: int = None, 
                      preserve_end: bool = False) -> str:
        """Умная обрезка с сохранением структуры"""
        if max_tokens is None:
            max_tokens = self.max_tokens
        
        current_tokens = self.count_tokens(text)
        
        if current_tokens <= max_tokens:
            return text
        
        # Разбиваем на предложения
        sentences = re.split(r'[.!?]+', text)
        
        if preserve_end:
            # Сохраняем конец, обрезаем начало
            sentences.reverse()
        
        result_sentences = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            sentence_tokens = self.count_tokens(sentence)
            
            if current_length + sentence_tokens <= max_tokens:
                result_sentences.append(sentence)
                current_length += sentence_tokens
            else:
                break
        
        if preserve_end:
            result_sentences.reverse()
        
        result = '. '.join(result_sentences)
        if result and not result.endswith('.'):
            result += '.'
        
        return result
    
    def optimize_prompt(self, system_prompt: str, user_message: str, 
                       context: str = "", max_total_tokens: int = None) -> Dict[str, str]:
        """Оптимизация промпта с учетом ограничений на токены"""
        if max_total_tokens is None:
            max_total_tokens = self.max_tokens
        
        # Подсчитываем токены для каждой части
        system_tokens = self.count_tokens(system_prompt)
        user_tokens = self.count_tokens(user_message)
        context_tokens = self.count_tokens(context) if context else 0
        
        total_tokens = system_tokens + user_tokens + context_tokens
        
        # Если укладываемся в лимит, возвращаем как есть
        if total_tokens <= max_total_tokens:
            return {
                'system_prompt': system_prompt,
                'user_message': user_message,
                'context': context,
                'token_usage': {
                    'system': system_tokens,
                    'user': user_tokens,
                    'context': context_tokens,
                    'total': total_tokens
                }
            }
        
        # Нужно оптимизировать
        # Приоритеты: system_prompt (неизменный) > user_message > context
        
        available_tokens = max_total_tokens - system_tokens
        
        if available_tokens <= 0:
            raise ValueError("System prompt слишком длинный")
        
        # Распределяем оставшиеся токены
        if user_tokens <= available_tokens // 2:
            # User message помещается в половину, остальное для context
            optimized_user = user_message
            remaining_tokens = available_tokens - user_tokens
            optimized_context = self.smart_truncate(context, remaining_tokens) if context else ""
        else:
            # Делим поровну между user и context
            user_allocation = available_tokens // 2
            context_allocation = available_tokens - user_allocation
            
            optimized_user = self.smart_truncate(user_message, user_allocation)
            optimized_context = self.smart_truncate(context, context_allocation) if context else ""
        
        return {
            'system_prompt': system_prompt,
            'user_message': optimized_user,
            'context': optimized_context,
            'token_usage': {
                'system': system_tokens,
                'user': self.count_tokens(optimized_user),
                'context': self.count_tokens(optimized_context),
                'total': system_tokens + self.count_tokens(optimized_user) + self.count_tokens(optimized_context)
            }
        }
    
    def chunk_text(self, text: str, chunk_size: int, overlap: int = 0) -> List[str]:
        """Разбиение текста на чанки с учетом токенов"""
        if self.tokenizer:
            tokens = self.tokenizer.encode(text)
            chunks = []
            
            i = 0
            while i < len(tokens):
                # Определяем конец чанка
                end = min(i + chunk_size, len(tokens))
                chunk_tokens = tokens[i:end]
                
                # Декодируем чанк
                chunk_text = self.tokenizer.decode(chunk_tokens)
                chunks.append(chunk_text)
                
                # Сдвигаемся с учетом overlap
                i += chunk_size - overlap
            
            return chunks
        else:
            # Приблизительное разбиение по символам
            estimated_chars_per_chunk = chunk_size * 3
            overlap_chars = overlap * 3
            
            chunks = []
            i = 0
            while i < len(text):
                end = min(i + estimated_chars_per_chunk, len(text))
                chunk = text[i:end]
                chunks.append(chunk)
                i += estimated_chars_per_chunk - overlap_chars
            
            return chunks

# Пример использования оптимизатора токенов
optimizer = TokenOptimizer(max_tokens=100)  # Маленький лимит для демонстрации

# Длинный текст для тестирования
long_text = """
Искусственный интеллект (ИИ) представляет собой одну из самых революционных технологий нашего времени. 
Он охватывает широкий спектр методов и подходов, от машинного обучения и глубоких нейронных сетей до 
обработки естественного языка и компьютерного зрения. ИИ уже сегодня применяется в различных областях: 
от медицины и финансов до транспорта и развлечений. Эта технология обещает кардинально изменить способы 
работы, обучения и взаимодействия людей с окружающим миром. Однако вместе с огромными возможностями 
ИИ приносит и новые вызовы, связанные с этикой, безопасностью и влиянием на рынок труда.
"""

print(f"Исходный текст: {optimizer.count_tokens(long_text)} токенов")
print(f"Текст: {long_text[:100]}...")

# Обычная обрезка
truncated = optimizer.truncate_text(long_text, 50)
print(f"\nОбычная обрезка (50 токенов): {optimizer.count_tokens(truncated)} токенов")
print(f"Текст: {truncated}")

# Умная обрезка
smart_truncated = optimizer.smart_truncate(long_text, 50)
print(f"\nУмная обрезка (50 токенов): {optimizer.count_tokens(smart_truncated)} токенов")
print(f"Текст: {smart_truncated}")

# Разбиение на чанки
chunks = optimizer.chunk_text(long_text, 30, overlap=5)
print(f"\nРазбиение на чанки (30 токенов, overlap 5):")
for i, chunk in enumerate(chunks):
    print(f"Чанк {i+1} ({optimizer.count_tokens(chunk)} токенов): {chunk[:60]}...")
```

### Стратегии экономии токенов
```python
class TokenEconomyStrategies:
    """Стратегии экономии токенов"""
    
    @staticmethod
    def compress_prompt(prompt: str) -> str:
        """Сжатие промпта без потери смысла"""
        # Удаление лишних пробелов и переносов строк
        compressed = re.sub(r'\s+', ' ', prompt.strip())
        
        # Сокращение стандартных фраз
        replacements = {
            'пожалуйста': 'плз',
            'пожалуйста,': '',
            'будьте добры': '',
            'не могли бы вы': '',
            'я хотел бы попросить вас': '',
            'можете ли вы': '',
            'не могли бы': ''
        }
        
        for long_form, short_form in replacements.items():
            compressed = compressed.replace(long_form, short_form)
        
        # Удаление повторений
        words = compressed.split()
        deduplicated = []
        for word in words:
            if not deduplicated or word != deduplicated[-1]:
                deduplicated.append(word)
        
        return ' '.join(deduplicated).strip()
    
    @staticmethod
    def use_abbreviations(text: str) -> str:
        """Использование аббревиатур и сокращений"""
        abbreviations = {
            'искусственный интеллект': 'ИИ',
            'машинное обучение': 'МО',
            'нейронная сеть': 'НС',
            'обработка естественного языка': 'NLP',
            'большая языковая модель': 'LLM',
            'программирование': 'прогр.',
            'разработка': 'разраб.',
            'приложение': 'прил.',
            'документация': 'док.',
            'конфигурация': 'конф.',
            'администрирование': 'админ.'
        }
        
        result = text
        for full_form, abbr in abbreviations.items():
            result = result.replace(full_form, abbr)
        
        return result
    
    @staticmethod
    def prioritize_content(content_blocks: Dict[str, str], 
                          priorities: Dict[str, int]) -> str:
        """Приоритизация контента по важности"""
        # Сортируем блоки по приоритету (меньше число = выше приоритет)
        sorted_blocks = sorted(content_blocks.items(), 
                             key=lambda x: priorities.get(x[0], 999))
        
        result_parts = []
        for block_name, block_content in sorted_blocks:
            if block_content.strip():
                result_parts.append(f"{block_name}: {block_content}")
        
        return '\n'.join(result_parts)
    
    @staticmethod
    def template_approach(template: str, variables: Dict[str, str]) -> str:
        """Использование шаблонов для экономии токенов"""
        # Компактный шаблон вместо длинных повторяющихся инструкций
        return template.format(**variables)
    
    @staticmethod
    def reference_compression(text: str, reference_dict: Dict[str, str]) -> Tuple[str, Dict[str, str]]:
        """Сжатие через ссылки на повторяющиеся элементы"""
        # Находим повторяющиеся фразы длиной более 10 символов
        words = text.split()
        
        # Ищем фразы длиной 3-8 слов
        phrase_counts = Counter()
        for i in range(len(words)):
            for length in range(3, min(9, len(words) - i + 1)):
                phrase = ' '.join(words[i:i+length])
                if len(phrase) > 15:  # Только длинные фразы
                    phrase_counts[phrase] += 1
        
        # Создаем ссылки для часто встречающихся фраз
        ref_counter = len(reference_dict)
        compressed_text = text
        
        for phrase, count in phrase_counts.items():
            if count > 1:
                ref_key = f"[REF{ref_counter}]"
                reference_dict[ref_key] = phrase
                compressed_text = compressed_text.replace(phrase, ref_key)
                ref_counter += 1
        
        return compressed_text, reference_dict

# Демонстрация стратегий экономии
strategies = TokenEconomyStrategies()

# Исходный промпт
original_prompt = """
Пожалуйста, будьте добры, проанализируйте следующие данные по искусственному интеллекту и машинному обучению. 
Я хотел бы попросить вас предоставить детальный анализ применения нейронных сетей в обработке естественного языка. 
Пожалуйста, не могли бы вы также включить информацию о разработке приложений с использованием больших языковых моделей.
"""

print("Исходный промпт:")
print(original_prompt)
print(f"Длина: {len(original_prompt)} символов\n")

# Сжатие промпта
compressed = strategies.compress_prompt(original_prompt)
print("Сжатый промпт:")
print(compressed)
print(f"Длина: {len(compressed)} символов\n")

# Использование аббревиатур
abbreviated = strategies.use_abbreviations(compressed)
print("С аббревиатурами:")
print(abbreviated)
print(f"Длина: {len(abbreviated)} символов\n")

# Шаблонный подход
template = "Анализ: {topic}. Включить: {requirements}. Формат: {format}"
variables = {
    'topic': 'ИИ и МО данные',
    'requirements': 'НС в NLP, LLM прил.',
    'format': 'детальный'
}

templated = strategies.template_approach(template, variables)
print("Шаблонный подход:")
print(templated)
print(f"Длина: {len(templated)} символов\n")

# Приоритизация контента
content_blocks = {
    'основная_задача': 'анализ данных ИИ',
    'дополнительно': 'информация о НС',
    'формат': 'детальный отчет',
    'примеры': 'кейсы использования'
}

priorities = {
    'основная_задача': 1,
    'формат': 2,
    'дополнительно': 3,
    'примеры': 4
}

prioritized = strategies.prioritize_content(content_blocks, priorities)
print("Приоритизированный контент:")
print(prioritized)
print(f"Длина: {len(prioritized)} символов")
```

## Работа с различными типами токенов

### Специальные токены и их использование
```python
class SpecialTokensManager:
    """Управление специальными токенами"""
    
    def __init__(self):
        self.special_tokens = {
            # Структурные токены
            '<BOS>': 'Beginning of Sequence',
            '<EOS>': 'End of Sequence', 
            '<PAD>': 'Padding',
            '<UNK>': 'Unknown',
            '<MASK>': 'Masked token',
            
            # Токены ролей для диалогов
            '<USER>': 'User message',
            '<ASSISTANT>': 'Assistant response',
            '<SYSTEM>': 'System message',
            
            # Токены форматирования
            '<CODE>': 'Code block start',
            '</CODE>': 'Code block end',
            '<LIST>': 'List start',
            '</LIST>': 'List end',
            
            # Токены состояния
            '<THINKING>': 'Reasoning process',
            '</THINKING>': 'End reasoning',
            '<CONFIDENT>': 'High confidence',
            '<UNCERTAIN>': 'Low confidence'
        }
    
    def format_conversation(self, messages: List[Dict[str, str]]) -> str:
        """Форматирование диалога с использованием специальных токенов"""
        formatted_parts = ['<BOS>']
        
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            
            if role == 'system':
                formatted_parts.append(f'<SYSTEM>{content}</SYSTEM>')
            elif role == 'user':
                formatted_parts.append(f'<USER>{content}</USER>')
            elif role == 'assistant':
                formatted_parts.append(f'<ASSISTANT>{content}</ASSISTANT>')
        
        formatted_parts.append('<EOS>')
        return ''.join(formatted_parts)
    
    def format_structured_content(self, content: Dict) -> str:
        """Форматирование структурированного контента"""
        formatted_parts = []
        
        for section, data in content.items():
            if section == 'code':
                formatted_parts.append(f'<CODE>{data}</CODE>')
            elif section == 'list':
                formatted_parts.append(f'<LIST>{data}</LIST>')
            elif section == 'reasoning':
                formatted_parts.append(f'<THINKING>{data}</THINKING>')
            else:
                formatted_parts.append(data)
        
        return ''.join(formatted_parts)
    
    def add_confidence_markers(self, text: str, confidence_level: float) -> str:
        """Добавление маркеров уверенности"""
        if confidence_level >= 0.8:
            return f'<CONFIDENT>{text}</CONFIDENT>'
        elif confidence_level <= 0.4:
            return f'<UNCERTAIN>{text}</UNCERTAIN>'
        else:
            return text
    
    def extract_special_content(self, text: str) -> Dict[str, List[str]]:
        """Извлечение контента, помеченного специальными токенами"""
        extracted = {}
        
        # Паттерны для извлечения контента между токенами
        patterns = {
            'code': r'<CODE>(.*?)</CODE>',
            'reasoning': r'<THINKING>(.*?)</THINKING>',
            'confident': r'<CONFIDENT>(.*?)</CONFIDENT>',
            'uncertain': r'<UNCERTAIN>(.*?)</UNCERTAIN>',
            'lists': r'<LIST>(.*?)</LIST>'
        }
        
        for content_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                extracted[content_type] = matches
        
        return extracted

# Демонстрация работы со специальными токенами
token_manager = SpecialTokensManager()

# Пример диалога
conversation = [
    {'role': 'system', 'content': 'Вы помощник программиста'},
    {'role': 'user', 'content': 'Как создать функцию сортировки?'},
    {'role': 'assistant', 'content': 'Вот пример функции сортировки на Python'}
]

formatted_conversation = token_manager.format_conversation(conversation)
print("Форматированный диалог:")
print(formatted_conversation)
print()

# Структурированный контент
structured_content = {
    'reasoning': 'Нужно использовать алгоритм быстрой сортировки',
    'code': 'def quicksort(arr): return sorted(arr)',
    'list': 'Шаги: 1. Выбрать опорный элемент 2. Разделить массив 3. Рекурсивно отсортировать'
}

formatted_content = token_manager.format_structured_content(structured_content)
print("Структурированный контент:")
print(formatted_content)
print()

# Маркеры уверенности
high_confidence_text = "Python является интерпретируемым языком"
low_confidence_text = "Возможно, этот подход будет работать"

marked_high = token_manager.add_confidence_markers(high_confidence_text, 0.9)
marked_low = token_manager.add_confidence_markers(low_confidence_text, 0.3)

print("С маркерами уверенности:")
print(f"Высокая: {marked_high}")
print(f"Низкая: {marked_low}")
print()

# Извлечение специального контента
sample_text = """
<THINKING>Пользователь спрашивает про сортировку. Лучше показать простой пример.</THINKING>
<CONFIDENT>Функция sorted() в Python очень эффективна</CONFIDENT>
<CODE>numbers = [3, 1, 4, 1, 5]
sorted_numbers = sorted(numbers)</CODE>
<UNCERTAIN>Возможно, стоит также упомянуть другие алгоритмы</UNCERTAIN>
"""

extracted = token_manager.extract_special_content(sample_text)
print("Извлеченный контент:")
for content_type, items in extracted.items():
    print(f"{content_type}: {items}")
```

## Ключевые моменты для экзамена

### Основы токенизации
1. **Определение токенов**: Базовые единицы обработки текста в LLM
2. **Типы токенизации**: Слова, подслова (BPE, WordPiece), символы
3. **Словарь токенов**: Маппинг между токенами и их числовыми ID
4. **Специальные токены**: Служебные токены для структурирования

### Практические аспекты
- **Подсчет токенов**: Оценка длины текста для API вызовов
- **Оптимизация промптов**: Сокращение без потери смысла
- **Управление контекстом**: Работа с ограничениями длины
- **Chunking**: Разбиение длинных текстов на части

### Стратегии экономии токенов
- Сжатие промптов и удаление избыточности
- Использование аббревиатур и сокращений
- Шаблонный подход вместо повторений
- Приоритизация контента по важности
- Ссылочное сжатие для повторяющихся элементов

### Влияние на качество и стоимость
- Качество токенизации влияет на понимание моделью
- Количество токенов определяет стоимость API вызовов
- Разные модели используют разные токенизаторы
- Мультиязычные аспекты токенизации

### Инструменты и библиотеки
- **tiktoken**: Токенизатор OpenAI для GPT моделей
- **transformers**: Hugging Face токенизаторы
- **sentencepiece**: Универсальный токенизатор от Google
- **Custom tokenizers**: Создание собственных токенизаторов