# Модели ChatGPT. Отличия моделей

## Семейство моделей GPT от OpenAI

### GPT-3.5 серия
```
- GPT-3.5-turbo: Базовая модель для чатов
- GPT-3.5-turbo-16k: Расширенный контекст (16,384 токена)
- GPT-3.5-turbo-instruct: Оптимизирована для следования инструкциям
```

### GPT-4 серия
```
- GPT-4: Самая мощная текстовая модель
- GPT-4-turbo: Быстрая версия GPT-4 с большим контекстом  
- GPT-4o: Оптимизированная версия (omni-model)
- GPT-4o-mini: Легкая быстрая версия
- GPT-4 Vision: С поддержкой изображений
```

## Основные характеристики моделей

### Размер контекста (Context Window)
```python
model_context = {
    "gpt-3.5-turbo": 4096,      # ~3,000 слов
    "gpt-3.5-turbo-16k": 16384,  # ~12,000 слов  
    "gpt-4": 8192,              # ~6,000 слов
    "gpt-4-turbo": 128000,      # ~96,000 слов
    "gpt-4o": 128000,           # ~96,000 слов
    "gpt-4o-mini": 128000       # ~96,000 слов
}

# Контекст = входные сообщения + ответ модели
# 1 токен ≈ 0.75 слова для английского текста
# 1 токен ≈ 0.5 слова для русского текста
```

### Стоимость использования (примерные цены)
```python
pricing_per_1k_tokens = {
    "gpt-3.5-turbo": {
        "input": 0.0015,   # $0.0015 за 1K входных токенов
        "output": 0.002    # $0.002 за 1K выходных токенов
    },
    "gpt-4": {
        "input": 0.03,     # $0.03 за 1K входных токенов  
        "output": 0.06     # $0.06 за 1K выходных токенов
    },
    "gpt-4o": {
        "input": 0.005,    # $0.005 за 1K входных токенов
        "output": 0.015    # $0.015 за 1K выходных токенов
    },
    "gpt-4o-mini": {
        "input": 0.00015,  # $0.00015 за 1K входных токенов
        "output": 0.0006   # $0.0006 за 1K выходных токенов
    }
}

# GPT-4 примерно в 20 раз дороже GPT-3.5-turbo
```

### Скорость работы
```python
speed_comparison = {
    "gpt-3.5-turbo": "Очень быстро",      # ~1-2 секунды
    "gpt-4o-mini": "Очень быстро",        # ~1-2 секунды  
    "gpt-4o": "Быстро",                   # ~2-4 секунды
    "gpt-4-turbo": "Средне",              # ~3-6 секунд
    "gpt-4": "Медленно"                   # ~5-15 секунд
}
```

## Качественные отличия моделей

### GPT-3.5-turbo
**Преимущества:**
- Быстрая и дешевая
- Хороша для простых задач
- Отлично подходит для чатботов
- Стабильная и надежная

**Недостатки:**
- Менее точная в сложных рассуждениях
- Ограниченный контекст (4K)
- Иногда "выдумывает" факты
- Слабее в математике и логике

**Лучше всего для:**
```python
gpt35_use_cases = [
    "Простые чатботы",
    "Генерация текста", 
    "Перевод",
    "Суммаризация коротких текстов",
    "Базовые вопросы-ответы",
    "Творческое письмо"
]
```

### GPT-4 / GPT-4-turbo
**Преимущества:**
- Лучшие рассуждения и логика
- Более точная в фактах
- Отличная математика
- Лучше понимает сложные инструкции
- Большой контекст (128K для turbo)

**Недостатки:**
- Дорогая (в 20 раз дороже 3.5)
- Медленнее
- Лимиты на запросы

**Лучше всего для:**
```python
gpt4_use_cases = [
    "Сложный анализ и рассуждения",
    "Программирование",
    "Математические задачи", 
    "Работа с длинными документами",
    "Исследовательские задачи",
    "Критическое мышление"
]
```

### GPT-4o (Omni)
**Особенности:**
- Мультимодальная (текст + изображения + звук)
- Оптимизированная версия GPT-4
- Хороший баланс качества и скорости
- Более доступная цена чем GPT-4

**Лучше всего для:**
```python
gpt4o_use_cases = [
    "Анализ изображений",
    "Создание контента",
    "Интерактивные приложения",
    "Обработка смешанного контента",
    "Образовательные задачи"
]
```

### GPT-4o-mini
**Особенности:**
- Самая дешевая из качественных моделей
- Очень быстрая
- Хорошее качество для простых задач
- Большой контекст (128K)

**Лучше всего для:**
```python
gpt4o_mini_use_cases = [
    "Массовая обработка текстов",
    "Экономичные чатботы",
    "Быстрые API интеграции",
    "Прототипирование",
    "Задачи где нужен баланс цена/качество"
]
```

## Выбор модели для задач

### Матрица выбора модели
```python
def choose_model(task_complexity, budget, speed_requirement, context_length):
    """
    Помощник выбора модели
    
    task_complexity: "simple", "medium", "complex"
    budget: "low", "medium", "high" 
    speed_requirement: "fast", "medium", "slow"
    context_length: количество токенов
    """
    
    if context_length > 16000:
        # Нужен большой контекст
        if budget == "low":
            return "gpt-4o-mini"
        elif task_complexity == "complex":
            return "gpt-4-turbo"
        else:
            return "gpt-4o"
    
    if task_complexity == "simple":
        if budget == "low":
            return "gpt-3.5-turbo"
        else:
            return "gpt-4o-mini"
    
    if task_complexity == "complex":
        if budget == "high":
            return "gpt-4"
        else:
            return "gpt-4o"
    
    # Medium complexity
    if speed_requirement == "fast" and budget == "low":
        return "gpt-4o-mini"
    else:
        return "gpt-4o"

# Примеры использования
print(choose_model("simple", "low", "fast", 1000))    # gpt-3.5-turbo
print(choose_model("complex", "medium", "medium", 50000))  # gpt-4o
print(choose_model("complex", "high", "slow", 5000))  # gpt-4
```

### Конкретные примеры задач

#### Простой чатбот
```python
simple_chatbot = {
    "модель": "gpt-3.5-turbo",
    "причина": "Дешево, быстро, достаточно качественно",
    "альтернатива": "gpt-4o-mini для лучшего качества"
}
```

#### Анализ длинных документов
```python
document_analysis = {
    "модель": "gpt-4-turbo", 
    "причина": "Большой контекст + высокое качество рассуждений",
    "альтернатива": "gpt-4o для баланса цены и качества"
}
```

#### Генерация кода
```python
code_generation = {
    "модель": "gpt-4o",
    "причина": "Хорошее качество кода, разумная цена",
    "альтернатива": "gpt-4 для сложного кода, gpt-4o-mini для простого"
}
```

#### Массовая обработка
```python
bulk_processing = {
    "модель": "gpt-4o-mini",
    "причина": "Самая экономичная при хорошем качестве",
    "альтернатива": "gpt-3.5-turbo если качество менее критично"
}
```

## Технические параметры

### Температура (Temperature)
```python
temperature_effects = {
    0.0: "Детерминированные ответы, одинаковые каждый раз",
    0.3: "Слегка случайные, хорошо для фактических ответов", 
    0.7: "Сбалансированная креативность (по умолчанию)",
    1.0: "Очень креативные, но менее точные ответы",
    2.0: "Максимальная случайность, может быть бессвязно"
}

# Рекомендации по температуре для разных моделей
model_temperature_recommendations = {
    "gpt-3.5-turbo": {
        "факты": 0.0-0.3,
        "общение": 0.5-0.7,
        "творчество": 0.7-1.0
    },
    "gpt-4": {
        "анализ": 0.0-0.2, 
        "рассуждения": 0.3-0.5,
        "креатив": 0.7-0.9
    }
}
```

### Максимальные токены (Max Tokens)
```python
max_tokens_guidelines = {
    "короткие_ответы": 150,      # Да/нет, простые факты
    "параграф": 300,             # Объяснение концепции  
    "статья": 1000,              # Подробная статья
    "длинный_анализ": 2000,      # Глубокий анализ
    "без_ограничений": None      # Модель решает сама
}
```

## Работа с API

### Базовый пример запроса
```python
import openai

def call_gpt_model(model, prompt, temperature=0.7, max_tokens=1000):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Ты полезный помощник."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

# Сравнение моделей на одной задаче
task = "Объясни квантовую физику простыми словами"

gpt35_answer = call_gpt_model("gpt-3.5-turbo", task)
gpt4_answer = call_gpt_model("gpt-4", task)
gpt4o_answer = call_gpt_model("gpt-4o", task)
```

### Мониторинг использования токенов
```python
def get_token_usage(response):
    usage = response.usage
    return {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens, 
        "total_tokens": usage.total_tokens,
        "cost_estimate": calculate_cost(usage, model)
    }

def calculate_cost(usage, model):
    pricing = pricing_per_1k_tokens[model]
    input_cost = (usage.prompt_tokens / 1000) * pricing["input"]
    output_cost = (usage.completion_tokens / 1000) * pricing["output"]
    return input_cost + output_cost
```

## Ограничения и лимиты

### Rate Limits (лимиты запросов)
```python
rate_limits = {
    "gpt-3.5-turbo": {
        "requests_per_minute": 3500,
        "tokens_per_minute": 90000
    },
    "gpt-4": {
        "requests_per_minute": 500,
        "tokens_per_minute": 40000  
    },
    "gpt-4o": {
        "requests_per_minute": 5000,
        "tokens_per_minute": 450000
    }
}
```

### Обработка лимитов
```python
import time
from openai import RateLimitError

def call_with_retry(model, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return openai.chat.completions.create(
                model=model,
                messages=messages
            )
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Экспоненциальная задержка
                time.sleep(wait_time)
            else:
                raise
```

## Новые возможности моделей

### Function Calling
```python
# GPT-4 и новые модели поддерживают вызов функций
function_schema = {
    "name": "get_weather", 
    "description": "Получить погоду для города",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "Название города"}
        },
        "required": ["city"]
    }
}

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Какая погода в Москве?"}],
    functions=[function_schema],
    function_call="auto"
)
```

### JSON Mode
```python
# Принудительный JSON ответ (GPT-4-turbo и новее)
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Отвечай только в формате JSON"},
        {"role": "user", "content": "Опиши собаку"}
    ],
    response_format={"type": "json_object"}
)
```

## Частые ошибки при выборе модели

### 1. Переплата за качество
```python
# ПЛОХО - используем GPT-4 для простых задач
expensive_task = "Переведи 'Hello' на русский"  # GPT-3.5 справится

# ХОРОШО - выбираем модель по сложности задачи
simple_translation = "gpt-3.5-turbo"
complex_analysis = "gpt-4"
```

### 2. Недооценка контекста
```python
# ПЛОХО - не учитываем размер контекста
long_document = "Проанализируй этот документ на 50,000 слов"
model = "gpt-3.5-turbo"  # Контекст только 4K токенов!

# ХОРОШО
if document_length > 15000:
    model = "gpt-4-turbo"  # 128K контекст
```

### 3. Игнорирование скорости
```python
# ПЛОХО - используем медленную модель для real-time чата
chatbot_model = "gpt-4"  # Медленно для пользователей

# ХОРОШО - быстрые модели для интерактивных задач  
chatbot_model = "gpt-4o-mini"  # Быстро и качественно
```

## Ключевые моменты для экзамена

- **GPT-3.5-turbo** - быстро, дешево, для простых задач
- **GPT-4** - лучшее качество, дорого, для сложных задач
- **GPT-4o** - баланс цены и качества, мультимодальная
- **GPT-4o-mini** - экономичная альтернатива с хорошим качеством
- **Контекст** - GPT-4-turbo и новее поддерживают 128K токенов
- **Цена** - GPT-4 в ~20 раз дороже GPT-3.5-turbo
- **Скорость** - GPT-3.5 и GPT-4o-mini самые быстрые
- **Выбор модели** зависит от: сложности задачи, бюджета, требований к скорости, размера контекста