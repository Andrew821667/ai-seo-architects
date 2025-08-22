# Тема 24: Промпт-инжиниринг для ИИ систем

## Основы промпт-инжиниринга

### Принципы эффективных промптов
- **Clarity**: Четкость и недвусмысленность инструкций
- **Context**: Предоставление необходимого контекста
- **Specificity**: Конкретность требований и ожиданий
- **Structure**: Логическая структура промпта
- **Examples**: Использование примеров для демонстрации

### Анатомия промпта
```python
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

@dataclass
class PromptTemplate:
    """Структура шаблона промпта"""
    system_message: str
    user_instruction: str
    context: Optional[str] = None
    examples: Optional[List[Dict]] = None
    constraints: Optional[List[str]] = None
    output_format: Optional[str] = None
    
    def build_prompt(self, variables: Dict[str, Any] = None) -> str:
        """Построение финального промпта из шаблона"""
        variables = variables or {}
        
        prompt_parts = []
        
        # Системное сообщение
        if self.system_message:
            system_msg = self.system_message.format(**variables)
            prompt_parts.append(f"Система: {system_msg}")
        
        # Контекст
        if self.context:
            context_msg = self.context.format(**variables)
            prompt_parts.append(f"Контекст: {context_msg}")
        
        # Примеры
        if self.examples:
            prompt_parts.append("Примеры:")
            for i, example in enumerate(self.examples, 1):
                formatted_example = {k: str(v).format(**variables) for k, v in example.items()}
                prompt_parts.append(f"Пример {i}:")
                for key, value in formatted_example.items():
                    prompt_parts.append(f"  {key}: {value}")
        
        # Ограничения
        if self.constraints:
            prompt_parts.append("Ограничения:")
            for constraint in self.constraints:
                formatted_constraint = constraint.format(**variables)
                prompt_parts.append(f"- {formatted_constraint}")
        
        # Формат вывода
        if self.output_format:
            format_msg = self.output_format.format(**variables)
            prompt_parts.append(f"Формат ответа: {format_msg}")
        
        # Основная инструкция
        user_msg = self.user_instruction.format(**variables)
        prompt_parts.append(f"Задача: {user_msg}")
        
        return "\n\n".join(prompt_parts)

# Пример создания базового промпта
basic_analysis_prompt = PromptTemplate(
    system_message="Вы эксперт-аналитик, специализирующийся на {domain}",
    context="Данные для анализа: {data}",
    user_instruction="Проанализируйте предоставленные данные и выделите ключевые инсайты",
    constraints=[
        "Ответ должен быть объективным и основанным на данных",
        "Длина ответа не более {max_length} слов",
        "Используйте простой и понятный язык"
    ],
    output_format="JSON с полями: summary, key_insights, recommendations",
    examples=[
        {
            "input": "Данные о продажах за квартал",
            "output": "{'summary': 'Рост продаж на 15%', 'key_insights': ['Увеличение спроса на продукт А'], 'recommendations': ['Расширить линейку продукта А']}"
        }
    ]
)

# Использование шаблона
variables = {
    "domain": "маркетинг",
    "data": "Статистика рекламных кампаний за последний месяц",
    "max_length": "200"
}

final_prompt = basic_analysis_prompt.build_prompt(variables)
print(final_prompt)
```

### Техники структурирования промптов
```python
class PromptStructure:
    """Различные техники структурирования промптов"""
    
    @staticmethod
    def zero_shot_prompt(task: str, context: str = "") -> str:
        """Zero-shot промпт без примеров"""
        prompt = f"""
Задача: {task}
{f"Контекст: {context}" if context else ""}

Выполните задачу максимально качественно.
"""
        return prompt.strip()
    
    @staticmethod
    def few_shot_prompt(task: str, examples: List[Dict], 
                       new_input: str) -> str:
        """Few-shot промпт с примерами"""
        prompt_parts = [f"Задача: {task}", ""]
        
        # Добавляем примеры
        for i, example in enumerate(examples, 1):
            prompt_parts.append(f"Пример {i}:")
            prompt_parts.append(f"Вход: {example['input']}")
            prompt_parts.append(f"Выход: {example['output']}")
            prompt_parts.append("")
        
        # Добавляем новый запрос
        prompt_parts.append("Теперь выполните задачу для:")
        prompt_parts.append(f"Вход: {new_input}")
        prompt_parts.append("Выход:")
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def chain_of_thought_prompt(problem: str, show_reasoning: bool = True) -> str:
        """Chain-of-Thought промпт для пошагового рассуждения"""
        if show_reasoning:
            prompt = f"""
Решите следующую задачу пошагово, объяснив каждый шаг:

Задача: {problem}

Пожалуйста, покажите ваши рассуждения:
1. Сначала определите, что нужно найти
2. Затем определите данные, которые у вас есть  
3. Выберите подходящий метод решения
4. Выполните вычисления пошагово
5. Проверьте результат

Решение:
"""
        else:
            prompt = f"""
Решите задачу: {problem}

Ответ:
"""
        return prompt.strip()
    
    @staticmethod
    def role_based_prompt(role: str, task: str, expertise_areas: List[str] = None) -> str:
        """Промпт с назначением роли"""
        expertise = ""
        if expertise_areas:
            expertise = f" со специализацией в {', '.join(expertise_areas)}"
        
        prompt = f"""
Вы {role}{expertise}.

Ваша задача: {task}

Отвечайте, используя ваши профессиональные знания и опыт. 
Будьте конкретны и практичны в своих рекомендациях.
"""
        return prompt.strip()
    
    @staticmethod
    def constraint_based_prompt(task: str, constraints: Dict[str, Any]) -> str:
        """Промпт с четкими ограничениями"""
        prompt_parts = [f"Задача: {task}", ""]
        
        if constraints:
            prompt_parts.append("Ограничения:")
            for key, value in constraints.items():
                if key == "length":
                    prompt_parts.append(f"- Длина ответа: {value}")
                elif key == "format":
                    prompt_parts.append(f"- Формат: {value}")
                elif key == "style":
                    prompt_parts.append(f"- Стиль: {value}")
                elif key == "language":
                    prompt_parts.append(f"- Язык: {value}")
                elif key == "audience":
                    prompt_parts.append(f"- Целевая аудитория: {value}")
                else:
                    prompt_parts.append(f"- {key}: {value}")
            prompt_parts.append("")
        
        prompt_parts.append("Выполните задачу с соблюдением всех ограничений.")
        
        return "\n".join(prompt_parts)

# Примеры использования различных техник
examples = [
    {"input": "Написать план маркетинговой кампании", 
     "output": "1. Анализ целевой аудитории\n2. Выбор каналов продвижения\n3. Бюджетирование\n4. KPI и метрики"},
    {"input": "Создать контент-план", 
     "output": "1. Исследование тем\n2. Календарь публикаций\n3. Форматы контента\n4. Каналы распространения"}
]

# Zero-shot
zero_shot = PromptStructure.zero_shot_prompt(
    "Создайте план запуска нового продукта",
    "IT-стартап разрабатывает мобильное приложение"
)

# Few-shot  
few_shot = PromptStructure.few_shot_prompt(
    "Создайте план",
    examples,
    "Запуск нового продукта в IT-сфере"
)

# Chain of Thought
cot = PromptStructure.chain_of_thought_prompt(
    "Как рассчитать ROI рекламной кампании с бюджетом 100,000 руб и конверсией 2%?"
)

# Role-based
role_based = PromptStructure.role_based_prompt(
    "опытный маркетолог",
    "разработать стратегию продвижения B2B продукта",
    ["цифровой маркетинг", "B2B продажи"]
)

# Constraint-based
constraints = {
    "length": "не более 300 слов",
    "format": "маркированный список",
    "style": "профессиональный",
    "audience": "топ-менеджмент"
}

constraint_based = PromptStructure.constraint_based_prompt(
    "Подготовить презентацию результатов квартала",
    constraints
)
```

## Продвинутые техники промпт-инжиниринга

### Многоэтапные промпты и цепочки
```python
class MultiStagePrompting:
    """Многоэтапное промптирование для сложных задач"""
    
    def __init__(self, model_api):
        self.model_api = model_api
        self.conversation_history = []
    
    async def execute_chain(self, stages: List[Dict]) -> Dict:
        """Выполнение цепочки промптов"""
        results = {}
        context = {}
        
        for i, stage in enumerate(stages):
            stage_name = stage.get('name', f'stage_{i}')
            prompt_template = stage['prompt']
            
            # Подставляем результаты предыдущих этапов
            formatted_prompt = prompt_template.format(**context)
            
            # Выполняем запрос
            response = await self.model_api.generate(formatted_prompt)
            
            # Сохраняем результат
            results[stage_name] = response
            
            # Обновляем контекст для следующих этапов
            if 'context_key' in stage:
                context[stage['context_key']] = response
            
            # Дополнительная обработка результата
            if 'processor' in stage:
                processed_result = stage['processor'](response)
                context[f"{stage_name}_processed"] = processed_result
        
        return results
    
    def create_analysis_chain(self, data: str) -> List[Dict]:
        """Создание цепочки для анализа данных"""
        return [
            {
                'name': 'data_summary',
                'prompt': f"""
                Проанализируйте следующие данные и создайте краткую сводку:
                
                Данные: {data}
                
                Сводка должна включать:
                1. Основные характеристики данных
                2. Выявленные паттерны
                3. Потенциальные проблемы
                
                Сводка:
                """,
                'context_key': 'summary'
            },
            {
                'name': 'insights_extraction',
                'prompt': """
                На основе следующей сводки данных, выделите ключевые инсайты:
                
                Сводка: {summary}
                
                Инсайты должны быть:
                1. Конкретными и actionable
                2. Основанными на данных
                3. Релевантными для бизнеса
                
                Ключевые инсайты:
                """,
                'context_key': 'insights'
            },
            {
                'name': 'recommendations',
                'prompt': """
                На основе сводки и инсайтов, предложите конкретные рекомендации:
                
                Сводка: {summary}
                Инсайты: {insights}
                
                Рекомендации должны быть:
                1. Практичными и выполнимыми
                2. Приоритизированными
                3. С указанием ожидаемого результата
                
                Рекомендации:
                """
            }
        ]
    
    def create_content_generation_chain(self, topic: str, audience: str) -> List[Dict]:
        """Цепочка для создания контента"""
        return [
            {
                'name': 'research',
                'prompt': f"""
                Проведите исследование по теме "{topic}" для аудитории "{audience}".
                
                Определите:
                1. Ключевые аспекты темы
                2. Интересы целевой аудитории
                3. Актуальные тренды
                4. Потенциальные вопросы аудитории
                
                Результат исследования:
                """,
                'context_key': 'research'
            },
            {
                'name': 'outline',
                'prompt': """
                На основе исследования создайте подробный план контента:
                
                Исследование: {research}
                
                План должен включать:
                1. Основные разделы
                2. Ключевые моменты каждого раздела
                3. Примеры и кейсы
                4. Call-to-action
                
                План контента:
                """,
                'context_key': 'outline'
            },
            {
                'name': 'content',
                'prompt': """
                Напишите полный контент на основе плана:
                
                План: {outline}
                Исследование: {research}
                
                Контент должен быть:
                1. Структурированным согласно плану
                2. Интересным для целевой аудитории
                3. Содержать практические советы
                4. Иметь четкий call-to-action
                
                Готовый контент:
                """
            }
        ]

# Пример использования многоэтапных промптов
class MockModelAPI:
    """Заглушка API модели для демонстрации"""
    async def generate(self, prompt: str) -> str:
        # Имитация ответа модели
        return f"[Ответ модели на промпт длиной {len(prompt)} символов]"

async def demonstrate_multi_stage():
    model_api = MockModelAPI()
    multi_stage = MultiStagePrompting(model_api)
    
    # Пример анализа данных
    sample_data = "Статистика продаж за Q1: рост на 15%, но снижение в марте на 5%"
    analysis_stages = multi_stage.create_analysis_chain(sample_data)
    
    analysis_results = await multi_stage.execute_chain(analysis_stages)
    print("Результаты анализа:")
    for stage, result in analysis_results.items():
        print(f"{stage}: {result}")
    
    # Пример создания контента
    content_stages = multi_stage.create_content_generation_chain(
        "Искусственный интеллект в маркетинге",
        "маркетологи среднего звена"
    )
    
    content_results = await multi_stage.execute_chain(content_stages)
    print("\nРезультаты создания контента:")
    for stage, result in content_results.items():
        print(f"{stage}: {result}")

# asyncio.run(demonstrate_multi_stage())
```

### Промпты для специализированных задач
```python
class SpecializedPrompts:
    """Коллекция промптов для специализированных задач"""
    
    @staticmethod
    def data_extraction_prompt(text: str, fields: List[str]) -> str:
        """Промпт для извлечения структурированных данных"""
        fields_list = "', '".join(fields)
        
        return f"""
Извлеките следующую информацию из текста и верните в формате JSON:

Поля для извлечения: ['{fields_list}']

Текст для анализа:
{text}

Правила:
1. Если информация не найдена, используйте null
2. Для дат используйте формат YYYY-MM-DD
3. Для чисел используйте числовой тип данных
4. Для текста используйте строки

JSON результат:
"""
    
    @staticmethod
    def sentiment_analysis_prompt(text: str, scale: str = "positive/negative/neutral") -> str:
        """Промпт для анализа тональности"""
        return f"""
Проанализируйте тональность следующего текста.

Текст: {text}

Шкала оценки: {scale}

Результат должен включать:
1. Общая тональность
2. Уверенность в оценке (0-100%)
3. Ключевые слова, влияющие на тональность
4. Краткое объяснение

Анализ тональности:
"""
    
    @staticmethod
    def summarization_prompt(text: str, max_length: int = 100, 
                           style: str = "neutral") -> str:
        """Промпт для суммаризации текста"""
        return f"""
Создайте краткую сводку следующего текста.

Исходный текст:
{text}

Требования:
- Максимальная длина: {max_length} слов
- Стиль: {style}
- Сохраните ключевые моменты
- Исключите второстепенные детали

Краткая сводка:
"""
    
    @staticmethod
    def classification_prompt(text: str, categories: List[str], 
                            multi_label: bool = False) -> str:
        """Промпт для классификации текста"""
        categories_str = "', '".join(categories)
        classification_type = "одну или несколько" if multi_label else "одну"
        
        return f"""
Классифицируйте следующий текст в {classification_type} из предложенных категорий.

Текст: {text}

Доступные категории: ['{categories_str}']

Правила:
1. Выберите наиболее подходящую категорию(-и)
2. Если текст не подходит ни к одной категории, укажите "other"
3. Объясните выбор

Результат классификации:
"""
    
    @staticmethod
    def translation_prompt(text: str, source_lang: str, target_lang: str,
                          style: str = "formal") -> str:
        """Промпт для перевода с учетом стиля"""
        return f"""
Переведите следующий текст с {source_lang} на {target_lang}.

Исходный текст:
{text}

Требования к переводу:
- Стиль: {style}
- Сохраните смысл и тон оригинала
- Адаптируйте культурные отсылки при необходимости
- Используйте естественную речь целевого языка

Перевод:
"""
    
    @staticmethod
    def creative_writing_prompt(genre: str, characters: List[str], 
                              setting: str, length: int = 500) -> str:
        """Промпт для творческого письма"""
        characters_str = ", ".join(characters)
        
        return f"""
Напишите {genre} с следующими параметрами:

Персонажи: {characters_str}
Место действия: {setting}
Желаемая длина: около {length} слов

Требования:
1. Создайте увлекательный сюжет
2. Развивайте характеры персонажей
3. Используйте живые описания
4. Создайте соответствующую атмосферу

История:
"""

# Пример системы управления промптами
class PromptManager:
    """Система управления промптами"""
    
    def __init__(self):
        self.templates = {}
        self.history = []
    
    def register_template(self, name: str, template: PromptTemplate):
        """Регистрация шаблона промпта"""
        self.templates[name] = template
    
    def generate_prompt(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Генерация промпта из шаблона"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        prompt = template.build_prompt(variables)
        
        # Сохраняем в историю
        self.history.append({
            'template_name': template_name,
            'variables': variables,
            'prompt': prompt,
            'timestamp': time.time()
        })
        
        return prompt
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Получение истории промптов"""
        return self.history[-limit:]
    
    def optimize_template(self, template_name: str, feedback: Dict):
        """Оптимизация шаблона на основе обратной связи"""
        # Здесь можно реализовать логику оптимизации
        # на основе результатов и обратной связи
        pass

# Настройка менеджера промптов
prompt_manager = PromptManager()

# Регистрация шаблонов
seo_analysis_template = PromptTemplate(
    system_message="Вы SEO-эксперт с 10-летним опытом",
    context="Сайт: {website_url}\nКлючевые слова: {keywords}",
    user_instruction="Проведите SEO-аудит сайта и предложите рекомендации",
    constraints=[
        "Фокус на технических аспектах",
        "Конкретные и выполнимые рекомендации",
        "Приоритизация по важности"
    ],
    output_format="Структурированный отчет с разделами: технические проблемы, контент, ссылки, рекомендации"
)

prompt_manager.register_template("seo_audit", seo_analysis_template)

# Использование
seo_prompt = prompt_manager.generate_prompt("seo_audit", {
    "website_url": "example.com",
    "keywords": "интернет-маркетинг, SEO, продвижение"
})

print(seo_prompt)
```

## Оптимизация и тестирование промптов

### A/B тестирование промптов
```python
import random
import statistics
from typing import List, Dict, Callable

class PromptABTester:
    """Система A/B тестирования промптов"""
    
    def __init__(self):
        self.experiments = {}
        self.results = {}
    
    def create_experiment(self, experiment_name: str, 
                         prompt_variants: Dict[str, str],
                         evaluation_metrics: List[str]):
        """Создание A/B эксперимента"""
        self.experiments[experiment_name] = {
            'variants': prompt_variants,
            'metrics': evaluation_metrics,
            'results': {variant: [] for variant in prompt_variants.keys()}
        }
    
    def run_test(self, experiment_name: str, test_cases: List[Dict],
                model_api, evaluator: Callable) -> Dict:
        """Запуск A/B теста"""
        if experiment_name not in self.experiments:
            raise ValueError(f"Experiment '{experiment_name}' not found")
        
        experiment = self.experiments[experiment_name]
        results = {}
        
        for test_case in test_cases:
            # Случайно выбираем вариант промпта
            variant_name = random.choice(list(experiment['variants'].keys()))
            prompt_template = experiment['variants'][variant_name]
            
            # Форматируем промпт
            formatted_prompt = prompt_template.format(**test_case)
            
            # Получаем ответ модели
            response = model_api.generate(formatted_prompt)
            
            # Оцениваем результат
            evaluation = evaluator(response, test_case)
            
            # Сохраняем результат
            experiment['results'][variant_name].append({
                'test_case': test_case,
                'response': response,
                'evaluation': evaluation
            })
        
        # Анализируем результаты
        analysis = self._analyze_results(experiment_name)
        return analysis
    
    def _analyze_results(self, experiment_name: str) -> Dict:
        """Анализ результатов A/B теста"""
        experiment = self.experiments[experiment_name]
        analysis = {}
        
        for variant_name, results in experiment['results'].items():
            if not results:
                continue
            
            # Вычисляем средние значения метрик
            metrics_values = {}
            for metric in experiment['metrics']:
                values = [r['evaluation'].get(metric, 0) for r in results]
                if values:
                    metrics_values[metric] = {
                        'mean': statistics.mean(values),
                        'median': statistics.median(values),
                        'std': statistics.stdev(values) if len(values) > 1 else 0,
                        'count': len(values)
                    }
            
            analysis[variant_name] = metrics_values
        
        # Определяем лучший вариант
        if len(analysis) >= 2:
            best_variant = self._find_best_variant(analysis, experiment['metrics'])
            analysis['best_variant'] = best_variant
        
        return analysis
    
    def _find_best_variant(self, analysis: Dict, metrics: List[str]) -> str:
        """Определение лучшего варианта"""
        variant_scores = {}
        
        for variant_name, variant_metrics in analysis.items():
            if variant_name == 'best_variant':
                continue
                
            score = 0
            for metric in metrics:
                if metric in variant_metrics:
                    score += variant_metrics[metric]['mean']
            
            variant_scores[variant_name] = score / len(metrics)
        
        return max(variant_scores.items(), key=lambda x: x[1])[0]

# Пример оценщика промптов
class PromptEvaluator:
    """Оценщик качества промптов"""
    
    @staticmethod
    def evaluate_response(response: str, test_case: Dict) -> Dict:
        """Оценка ответа модели"""
        metrics = {}
        
        # Длина ответа
        metrics['length'] = len(response.split())
        
        # Релевантность (упрощенная проверка)
        expected_keywords = test_case.get('expected_keywords', [])
        found_keywords = sum(1 for keyword in expected_keywords 
                           if keyword.lower() in response.lower())
        metrics['relevance'] = found_keywords / max(len(expected_keywords), 1)
        
        # Структурированность (наличие списков, разделов)
        structure_indicators = ['\n-', '\n1.', '\n2.', '##', '**']
        structure_score = sum(1 for indicator in structure_indicators 
                            if indicator in response)
        metrics['structure'] = min(structure_score / 3, 1.0)  # Нормализуем до 1
        
        # Конкретность (отсутствие общих фраз)
        vague_phrases = ['в целом', 'как правило', 'обычно', 'возможно']
        vague_count = sum(1 for phrase in vague_phrases 
                         if phrase in response.lower())
        metrics['specificity'] = max(0, 1 - vague_count / 10)
        
        return metrics

# Пример A/B тестирования
def demonstrate_ab_testing():
    tester = PromptABTester()
    evaluator = PromptEvaluator()
    
    # Создаем эксперимент
    prompt_variants = {
        'direct': """
        Проанализируйте следующие данные: {data}
        Предоставьте анализ и рекомендации.
        """,
        'structured': """
        Проанализируйте данные: {data}
        
        Пожалуйста, предоставьте:
        1. Ключевые инсайты
        2. Выявленные паттерны  
        3. Конкретные рекомендации
        4. Следующие шаги
        """,
        'role_based': """
        Как опытный аналитик данных, проанализируйте: {data}
        
        Используя ваш профессиональный опыт, предоставьте:
        - Детальный анализ
        - Практические рекомендации
        - План действий
        """
    }
    
    tester.create_experiment(
        'analysis_prompts',
        prompt_variants,
        ['relevance', 'structure', 'specificity', 'length']
    )
    
    # Тестовые случаи
    test_cases = [
        {
            'data': 'Продажи Q1: +15%, Q2: +8%, Q3: -2%',
            'expected_keywords': ['рост', 'снижение', 'тренд', 'рекомендации']
        },
        {
            'data': 'Трафик сайта: 50% органический, 30% реклама, 20% прямой',
            'expected_keywords': ['SEO', 'реклама', 'оптимизация', 'источники']
        }
    ]
    
    # Имитация API модели
    class MockAPI:
        def generate(self, prompt):
            return f"Анализ данных на основе промпта длиной {len(prompt)} символов"
    
    # Запуск теста
    api = MockAPI()
    results = tester.run_test('analysis_prompts', test_cases, api, evaluator.evaluate_response)
    
    print("Результаты A/B тестирования:")
    for variant, metrics in results.items():
        print(f"\n{variant}:")
        if isinstance(metrics, dict):
            for metric, values in metrics.items():
                print(f"  {metric}: {values}")

# demonstrate_ab_testing()
```

## Ключевые моменты для экзамена

### Принципы эффективных промптов
1. **Четкость инструкций**: Недвусмысленные и конкретные задачи
2. **Контекст**: Предоставление необходимой информации
3. **Структура**: Логическая организация промпта
4. **Примеры**: Демонстрация ожидаемого результата
5. **Ограничения**: Четкие границы и требования

### Техники промпт-инжиниринга
- **Zero-shot**: Выполнение задач без примеров
- **Few-shot**: Обучение на малом количестве примеров
- **Chain-of-Thought**: Пошаговое рассуждение
- **Role-playing**: Назначение роли модели
- **Multi-stage**: Многоэтапные промпты

### Оптимизация промптов
- A/B тестирование различных вариантов
- Метрики оценки качества ответов
- Итеративное улучшение промптов
- Анализ результатов и обратная связь

### Практические применения
- Анализ данных и извлечение инсайтов
- Создание контента и копирайтинг
- Классификация и категоризация
- Суммаризация и реферирование
- Переводы и адаптация контента