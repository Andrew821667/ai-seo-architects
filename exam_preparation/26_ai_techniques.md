# Тема 26: Техники работы с ИИ

## Продвинутые техники промптинга

### Chain-of-Thought (CoT) рассуждения
- **Принцип**: Пошаговое объяснение логики решения
- **Применение**: Сложные задачи, требующие рассуждений
- **Виды**: Zero-shot CoT, Few-shot CoT, Auto-CoT
- **Эффективность**: Повышает точность на логических задачах

```python
from typing import List, Dict, Any, Optional
import re
import json

class ChainOfThoughtPrompting:
    """Реализация техники Chain-of-Thought"""
    
    @staticmethod
    def zero_shot_cot(problem: str) -> str:
        """Zero-shot Chain-of-Thought промпт"""
        return f"""
Решите следующую задачу пошагово.

Задача: {problem}

Давайте подумаем пошагово:
"""
    
    @staticmethod
    def few_shot_cot(problem: str, examples: List[Dict[str, str]]) -> str:
        """Few-shot Chain-of-Thought с примерами"""
        prompt_parts = ["Решите задачи пошагово, показав все рассуждения.\n"]
        
        # Добавляем примеры с решениями
        for i, example in enumerate(examples, 1):
            prompt_parts.append(f"Пример {i}:")
            prompt_parts.append(f"Задача: {example['problem']}")
            prompt_parts.append(f"Решение: {example['solution']}")
            prompt_parts.append("")
        
        # Добавляем новую задачу
        prompt_parts.append(f"Теперь решите:")
        prompt_parts.append(f"Задача: {problem}")
        prompt_parts.append("Решение:")
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def structured_cot(problem: str, steps: List[str]) -> str:
        """Структурированный CoT с заданными этапами"""
        prompt_parts = [f"Задача: {problem}\n"]
        prompt_parts.append("Решите задачу, следуя этим этапам:")
        
        for i, step in enumerate(steps, 1):
            prompt_parts.append(f"{i}. {step}")
        
        prompt_parts.append("\nПошаговое решение:")
        
        return "\n".join(prompt_parts)

# Примеры использования CoT
cot = ChainOfThoughtPrompting()

# Математическая задача
math_problem = "У Анны было 15 яблок. Она дала 3 яблока Борису и 5 яблок Веронике. Затем купила еще 8 яблок. Сколько яблок у неё стало?"

zero_shot_prompt = cot.zero_shot_cot(math_problem)
print("Zero-shot CoT:")
print(zero_shot_prompt)
print()

# Few-shot с примерами
examples = [
    {
        "problem": "У Петра было 10 конфет. Он съел 3 и дал 2 другу. Сколько осталось?",
        "solution": "Начальное количество: 10 конфет\nСъел: 3 конфеты\nДал другу: 2 конфеты\nВсего потратил: 3 + 2 = 5 конфет\nОсталось: 10 - 5 = 5 конфет"
    }
]

few_shot_prompt = cot.few_shot_cot(math_problem, examples)
print("Few-shot CoT:")
print(few_shot_prompt[:300] + "...")
```

### Tree of Thoughts (ToT) - Дерево мыслей
```python
class TreeOfThoughts:
    """Реализация техники Tree of Thoughts"""
    
    def __init__(self, max_depth: int = 3, max_branches: int = 3):
        self.max_depth = max_depth
        self.max_branches = max_branches
        self.thought_tree = {}
    
    def generate_thoughts(self, problem: str, current_thoughts: List[str] = None) -> List[str]:
        """Генерация альтернативных направлений мышления"""
        if current_thoughts is None:
            current_thoughts = []
        
        base_prompt = f"""
Задача: {problem}

Текущие рассуждения: {' -> '.join(current_thoughts) if current_thoughts else 'Начало'}

Предложите {self.max_branches} различных подхода к решению или следующих шагов:
1.
2.
3.
"""
        return base_prompt
    
    def evaluate_thoughts(self, thoughts: List[str], problem: str) -> Dict[str, float]:
        """Оценка качества каждого направления мышления"""
        evaluation_prompt = f"""
Задача: {problem}

Оцените следующие подходы по шкале от 0 до 1 (где 1 - наиболее перспективный):

"""
        
        for i, thought in enumerate(thoughts, 1):
            evaluation_prompt += f"{i}. {thought}\n"
        
        evaluation_prompt += "\nОценки (в формате 'номер: оценка'):"
        
        # Здесь должен быть вызов к модели
        # Для демонстрации возвращаем случайные оценки
        import random
        return {f"thought_{i}": random.uniform(0.3, 1.0) for i in range(len(thoughts))}
    
    def build_solution_tree(self, problem: str) -> Dict:
        """Построение дерева решений"""
        tree = {
            'problem': problem,
            'depth': 0,
            'thoughts': [],
            'children': []
        }
        
        def expand_node(node: Dict, depth: int):
            if depth >= self.max_depth:
                return
            
            # Генерируем мысли для текущего узла
            current_path = self._get_path_to_node(node)
            thoughts_prompt = self.generate_thoughts(problem, current_path)
            
            # Симуляция генерации мыслей
            sample_thoughts = [
                f"Подход {i+1} на глубине {depth}" 
                for i in range(self.max_branches)
            ]
            
            # Оцениваем каждую мысль
            evaluations = self.evaluate_thoughts(sample_thoughts, problem)
            
            # Создаем дочерние узлы для лучших мыслей
            for i, thought in enumerate(sample_thoughts):
                eval_score = evaluations.get(f"thought_{i}", 0.5)
                
                if eval_score > 0.6:  # Порог для продолжения ветки
                    child_node = {
                        'thought': thought,
                        'score': eval_score,
                        'depth': depth + 1,
                        'children': []
                    }
                    
                    node['children'].append(child_node)
                    expand_node(child_node, depth + 1)
        
        expand_node(tree, 0)
        return tree
    
    def _get_path_to_node(self, node: Dict) -> List[str]:
        """Получение пути от корня до узла"""
        # Упрощенная версия - в реальности нужно отслеживать путь
        return [node.get('thought', 'Начало')]
    
    def find_best_path(self, tree: Dict) -> List[Dict]:
        """Поиск наилучшего пути в дереве"""
        def dfs_best_path(node: Dict, current_path: List[Dict]) -> Tuple[List[Dict], float]:
            current_path = current_path + [node]
            
            if not node.get('children'):
                # Листовой узел
                avg_score = sum(n.get('score', 0.5) for n in current_path) / len(current_path)
                return current_path, avg_score
            
            best_path = current_path
            best_score = 0
            
            for child in node['children']:
                path, score = dfs_best_path(child, current_path)
                if score > best_score:
                    best_path = path
                    best_score = score
            
            return best_path, best_score
        
        path, score = dfs_best_path(tree, [])
        return path

# Демонстрация Tree of Thoughts
tot = TreeOfThoughts(max_depth=2, max_branches=2)

complex_problem = "Как эффективно внедрить ИИ в небольшую компанию с ограниченным бюджетом?"

solution_tree = tot.build_solution_tree(complex_problem)
best_path = tot.find_best_path(solution_tree)

print("Tree of Thoughts - лучший путь решения:")
for i, node in enumerate(best_path):
    thought = node.get('thought', 'Корень')
    score = node.get('score', 0)
    print(f"Шаг {i}: {thought} (оценка: {score:.2f})")
```

### Self-Consistency - Самосогласованность
```python
class SelfConsistency:
    """Техника самосогласованности для повышения надежности"""
    
    def __init__(self, num_samples: int = 5):
        self.num_samples = num_samples
    
    def generate_multiple_solutions(self, problem: str, temperature: float = 0.8) -> List[str]:
        """Генерация множественных решений одной задачи"""
        base_prompt = f"""
Решите следующую задачу:

{problem}

Покажите пошаговое решение:
"""
        
        solutions = []
        for i in range(self.num_samples):
            # В реальности здесь был бы вызов к модели с разными температурами
            # Для демонстрации создаем вариации решения
            solution = f"Решение {i+1}: {base_prompt} [Вариация решения с температурой {temperature}]"
            solutions.append(solution)
        
        return solutions
    
    def extract_final_answers(self, solutions: List[str]) -> List[Any]:
        """Извлечение финальных ответов из решений"""
        answers = []
        
        for solution in solutions:
            # Простая эвристика для извлечения ответа
            # В реальности нужен более сложный парсинг
            answer_match = re.search(r'ответ[:\s]+([^\n.]+)', solution, re.IGNORECASE)
            if answer_match:
                answers.append(answer_match.group(1).strip())
            else:
                # Попытка найти числовой ответ
                numbers = re.findall(r'\b\d+(?:\.\d+)?\b', solution)
                if numbers:
                    answers.append(numbers[-1])  # Последнее число как ответ
                else:
                    answers.append("Не удалось извлечь ответ")
        
        return answers
    
    def find_consensus_answer(self, answers: List[Any]) -> Dict[str, Any]:
        """Поиск консенсусного ответа"""
        from collections import Counter
        
        # Подсчитываем частоту каждого ответа
        answer_counts = Counter(str(answer) for answer in answers)
        
        # Находим наиболее частый ответ
        most_common = answer_counts.most_common(1)[0]
        consensus_answer = most_common[0]
        consensus_count = most_common[1]
        
        # Вычисляем уверенность
        confidence = consensus_count / len(answers)
        
        return {
            'consensus_answer': consensus_answer,
            'confidence': confidence,
            'answer_distribution': dict(answer_counts),
            'total_attempts': len(answers)
        }
    
    def solve_with_consensus(self, problem: str) -> Dict[str, Any]:
        """Решение задачи с использованием консенсуса"""
        # Генерируем множественные решения
        solutions = self.generate_multiple_solutions(problem)
        
        # Извлекаем ответы
        answers = self.extract_final_answers(solutions)
        
        # Находим консенсус
        consensus = self.find_consensus_answer(answers)
        
        return {
            'problem': problem,
            'solutions': solutions,
            'extracted_answers': answers,
            'consensus': consensus
        }

# Демонстрация самосогласованности
consistency = SelfConsistency(num_samples=5)

math_problem = "Магазин продает яблоки по 50 рублей за килограмм. Покупатель купил 3.5 кг яблок и заплатил 200 рублей. Сколько сдачи он должен получить?"

result = consistency.solve_with_consensus(math_problem)

print("Self-Consistency результат:")
print(f"Задача: {result['problem']}")
print(f"Консенсусный ответ: {result['consensus']['consensus_answer']}")
print(f"Уверенность: {result['consensus']['confidence']:.2f}")
print(f"Распределение ответов: {result['consensus']['answer_distribution']}")
```

## Техники оптимизации и fine-tuning

### Prompt Engineering для specific domains
```python
class DomainSpecificPrompting:
    """Промпт-инжиниринг для специфических областей"""
    
    def __init__(self):
        self.domain_templates = {
            'medical': {
                'prefix': "Как медицинский эксперт,",
                'constraints': [
                    "Основывайтесь только на проверенных медицинских данных",
                    "Рекомендуйте консультацию с врачом для диагностики",
                    "Избегайте категорических утверждений о диагнозах"
                ],
                'format': "Симптомы -> Возможные причины -> Рекомендации"
            },
            'legal': {
                'prefix': "Как юридический консультант,",
                'constraints': [
                    "Ссылайтесь на соответствующие законы и регуляции",
                    "Указывайте юрисдикцию применимости",
                    "Рекомендуйте профессиональную юридическую помощь"
                ],
                'format': "Ситуация -> Применимое право -> Рекомендации"
            },
            'technical': {
                'prefix': "Как технический эксперт,",
                'constraints': [
                    "Предоставляйте конкретные технические детали",
                    "Включайте примеры кода при необходимости",
                    "Упоминайте совместимость и ограничения"
                ],
                'format': "Проблема -> Техническое решение -> Реализация"
            },
            'business': {
                'prefix': "Как бизнес-консультант,",
                'constraints': [
                    "Фокусируйтесь на ROI и практической применимости",
                    "Учитывайте рыночные условия",
                    "Предлагайте измеримые KPI"
                ],
                'format': "Ситуация -> Анализ -> Стратегия -> Метрики"
            }
        }
    
    def create_domain_prompt(self, domain: str, query: str, context: str = "") -> str:
        """Создание промпта для специфической области"""
        if domain not in self.domain_templates:
            raise ValueError(f"Неподдерживаемая область: {domain}")
        
        template = self.domain_templates[domain]
        
        prompt_parts = []
        
        # Префикс роли
        prompt_parts.append(template['prefix'])
        
        # Контекст
        if context:
            prompt_parts.append(f"Контекст: {context}")
        
        # Ограничения
        prompt_parts.append("Важные принципы:")
        for constraint in template['constraints']:
            prompt_parts.append(f"- {constraint}")
        
        # Формат ответа
        prompt_parts.append(f"Структура ответа: {template['format']}")
        
        # Запрос
        prompt_parts.append(f"Запрос: {query}")
        
        return "\n\n".join(prompt_parts)
    
    def optimize_for_accuracy(self, base_prompt: str, domain: str) -> str:
        """Оптимизация промпта для повышения точности"""
        accuracy_enhancers = {
            'medical': [
                "Укажите уровень доказательности для каждого утверждения",
                "Разделите факты и предположения",
                "Включите статистику и исследования"
            ],
            'legal': [
                "Цитируйте конкретные статьи законов",
                "Укажите судебную практику",
                "Отметьте актуальность информации"
            ],
            'technical': [
                "Предоставьте работающие примеры кода",
                "Укажите версии технологий",
                "Включите тестовые случаи"
            ],
            'business': [
                "Подкрепите данными и исследованиями",
                "Включите анализ рисков",
                "Предоставьте временные рамки"
            ]
        }
        
        enhancers = accuracy_enhancers.get(domain, [])
        
        enhanced_prompt = base_prompt + "\n\nДополнительные требования для точности:\n"
        for enhancer in enhancers:
            enhanced_prompt += f"- {enhancer}\n"
        
        return enhanced_prompt

# Демонстрация domain-specific prompting
domain_prompting = DomainSpecificPrompting()

# Медицинский запрос
medical_query = "У пациента головная боль, температура 38.5°C и тошнота"
medical_context = "Пациент: мужчина 35 лет, симптомы появились 2 дня назад"

medical_prompt = domain_prompting.create_domain_prompt('medical', medical_query, medical_context)
print("Медицинский промпт:")
print(medical_prompt)
print()

# Техническая консультация
tech_query = "Как оптимизировать производительность SQL запросов в PostgreSQL?"
tech_context = "База данных содержит 10 млн записей, время выполнения запросов превышает 30 секунд"

tech_prompt = domain_prompting.create_domain_prompt('technical', tech_query, tech_context)
optimized_tech_prompt = domain_prompting.optimize_for_accuracy(tech_prompt, 'technical')

print("Оптимизированный технический промпт:")
print(optimized_tech_prompt[:300] + "...")
```

### Adaptive Prompting - Адаптивные промпты
```python
class AdaptivePrompting:
    """Система адаптивных промптов"""
    
    def __init__(self):
        self.performance_history = {}
        self.prompt_variants = {}
        self.success_threshold = 0.8
    
    def register_prompt_variant(self, task_type: str, variant_name: str, 
                              prompt_template: str, metadata: Dict = None):
        """Регистрация варианта промпта"""
        if task_type not in self.prompt_variants:
            self.prompt_variants[task_type] = {}
        
        self.prompt_variants[task_type][variant_name] = {
            'template': prompt_template,
            'metadata': metadata or {},
            'usage_count': 0,
            'success_rate': 0.0,
            'avg_response_time': 0.0
        }
    
    def select_best_prompt(self, task_type: str, context: Dict = None) -> str:
        """Выбор лучшего промпта на основе истории производительности"""
        if task_type not in self.prompt_variants:
            raise ValueError(f"Нет зарегистрированных промптов для задачи: {task_type}")
        
        variants = self.prompt_variants[task_type]
        
        # Если нет истории, используем первый доступный
        if not any(v['usage_count'] > 0 for v in variants.values()):
            return list(variants.keys())[0]
        
        # Выбираем на основе success_rate и контекста
        best_variant = None
        best_score = 0
        
        for variant_name, variant_data in variants.items():
            if variant_data['usage_count'] == 0:
                continue
            
            # Базовый скор - успешность
            score = variant_data['success_rate']
            
            # Бонус за скорость (если есть данные)
            if variant_data['avg_response_time'] > 0:
                speed_bonus = 1.0 / (1.0 + variant_data['avg_response_time'] / 10.0)
                score += speed_bonus * 0.2
            
            # Контекстные бонусы
            if context:
                metadata = variant_data['metadata']
                if context.get('complexity') == 'high' and metadata.get('handles_complexity'):
                    score += 0.1
                if context.get('domain') == metadata.get('preferred_domain'):
                    score += 0.15
            
            if score > best_score:
                best_score = score
                best_variant = variant_name
        
        return best_variant or list(variants.keys())[0]
    
    def update_performance(self, task_type: str, variant_name: str, 
                          success: bool, response_time: float = None):
        """Обновление статистики производительности"""
        if task_type not in self.prompt_variants:
            return
        
        if variant_name not in self.prompt_variants[task_type]:
            return
        
        variant = self.prompt_variants[task_type][variant_name]
        
        # Обновляем количество использований
        variant['usage_count'] += 1
        
        # Обновляем success rate (скользящее среднее)
        old_rate = variant['success_rate']
        old_count = variant['usage_count'] - 1
        
        if old_count == 0:
            variant['success_rate'] = 1.0 if success else 0.0
        else:
            # Экспоненциальное сглаживание
            alpha = 0.1  # Фактор обучения
            variant['success_rate'] = (1 - alpha) * old_rate + alpha * (1.0 if success else 0.0)
        
        # Обновляем время ответа
        if response_time is not None:
            old_time = variant['avg_response_time']
            if old_count == 0:
                variant['avg_response_time'] = response_time
            else:
                variant['avg_response_time'] = (1 - alpha) * old_time + alpha * response_time
    
    def get_performance_report(self, task_type: str = None) -> Dict:
        """Отчет о производительности промптов"""
        if task_type:
            if task_type not in self.prompt_variants:
                return {}
            return {task_type: self.prompt_variants[task_type]}
        else:
            return self.prompt_variants
    
    def suggest_improvements(self, task_type: str) -> List[str]:
        """Предложения по улучшению промптов"""
        if task_type not in self.prompt_variants:
            return []
        
        suggestions = []
        variants = self.prompt_variants[task_type]
        
        # Анализируем производительность
        performing_variants = {k: v for k, v in variants.items() 
                             if v['usage_count'] > 0}
        
        if not performing_variants:
            suggestions.append("Недостаточно данных для анализа")
            return suggestions
        
        # Ищем проблемные области
        avg_success = sum(v['success_rate'] for v in performing_variants.values()) / len(performing_variants)
        
        if avg_success < self.success_threshold:
            suggestions.append(f"Общая успешность ({avg_success:.2f}) ниже порога ({self.success_threshold})")
            suggestions.append("Рассмотрите добавление примеров в промпты")
            suggestions.append("Попробуйте более структурированный формат")
        
        # Ищем медленные варианты
        slow_variants = [k for k, v in performing_variants.items() 
                        if v['avg_response_time'] > 10.0]
        
        if slow_variants:
            suggestions.append(f"Медленные варианты: {', '.join(slow_variants)}")
            suggestions.append("Рассмотрите сокращение длины промптов")
        
        return suggestions

# Демонстрация адаптивных промптов
adaptive = AdaptivePrompting()

# Регистрируем варианты для анализа данных
adaptive.register_prompt_variant('data_analysis', 'basic', 
    "Проанализируйте данные: {data}", 
    {'complexity': 'low'})

adaptive.register_prompt_variant('data_analysis', 'detailed',
    "Как эксперт по данным, проведите детальный анализ: {data}. Включите статистику, тренды и рекомендации.",
    {'complexity': 'high', 'handles_complexity': True})

adaptive.register_prompt_variant('data_analysis', 'structured',
    """Проанализируйте данные: {data}
    
    Структура анализа:
    1. Обзор данных
    2. Ключевые метрики  
    3. Выявленные паттерны
    4. Рекомендации""",
    {'complexity': 'medium', 'preferred_domain': 'business'})

# Имитация использования
contexts = [
    {'complexity': 'low', 'domain': 'general'},
    {'complexity': 'high', 'domain': 'business'}, 
    {'complexity': 'medium', 'domain': 'technical'}
]

# Симуляция выбора и обновления производительности
import random

for i in range(10):
    context = random.choice(contexts)
    selected = adaptive.select_best_prompt('data_analysis', context)
    
    # Имитация результата
    success = random.random() > 0.3  # 70% успешность
    response_time = random.uniform(2.0, 15.0)
    
    adaptive.update_performance('data_analysis', selected, success, response_time)
    
    print(f"Итерация {i+1}: выбран '{selected}', успех: {success}, время: {response_time:.1f}с")

# Отчет о производительности
report = adaptive.get_performance_report('data_analysis')
print("\nОтчет о производительности:")
for variant, stats in report['data_analysis'].items():
    print(f"{variant}: использований {stats['usage_count']}, "
          f"успешность {stats['success_rate']:.2f}, "
          f"время {stats['avg_response_time']:.1f}с")

# Предложения по улучшению
suggestions = adaptive.suggest_improvements('data_analysis')
print(f"\nПредложения: {suggestions}")
```

## Техники работы с контекстом

### Context Window Management
```python
class ContextWindowManager:
    """Управление окном контекста"""
    
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.token_counter = self._create_token_counter()
    
    def _create_token_counter(self):
        """Создание функции подсчета токенов"""
        try:
            import tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")
            return lambda text: len(encoding.encode(text))
        except:
            # Fallback: приблизительный подсчет
            return lambda text: len(text.split()) * 1.3
    
    def sliding_window_context(self, messages: List[Dict], 
                             window_size: int = None) -> List[Dict]:
        """Скользящее окно контекста"""
        if window_size is None:
            window_size = self.max_tokens // 2
        
        # Всегда сохраняем системное сообщение
        system_messages = [msg for msg in messages if msg.get('role') == 'system']
        other_messages = [msg for msg in messages if msg.get('role') != 'system']
        
        # Считаем токены для системных сообщений
        system_tokens = sum(self.token_counter(msg['content']) for msg in system_messages)
        available_tokens = window_size - system_tokens
        
        if available_tokens <= 0:
            return system_messages  # Только системные сообщения
        
        # Добавляем сообщения с конца, пока не превысим лимит
        selected_messages = []
        current_tokens = 0
        
        for message in reversed(other_messages):
            message_tokens = self.token_counter(message['content'])
            
            if current_tokens + message_tokens <= available_tokens:
                selected_messages.append(message)
                current_tokens += message_tokens
            else:
                break
        
        # Возвращаем в правильном порядке
        return system_messages + list(reversed(selected_messages))
    
    def hierarchical_summarization(self, messages: List[Dict], 
                                 summary_ratio: float = 0.3) -> List[Dict]:
        """Иерархическая суммаризация старых сообщений"""
        if len(messages) <= 5:
            return messages
        
        # Разделяем на группы: системные, старые, недавние
        system_messages = [msg for msg in messages if msg.get('role') == 'system']
        conversation_messages = [msg for msg in messages if msg.get('role') != 'system']
        
        if len(conversation_messages) <= 3:
            return messages
        
        # Определяем границу для суммаризации
        split_point = int(len(conversation_messages) * summary_ratio)
        old_messages = conversation_messages[:split_point]
        recent_messages = conversation_messages[split_point:]
        
        # Создаем суммарный контекст из старых сообщений
        old_content = []
        for msg in old_messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            old_content.append(f"{role.title()}: {content}")
        
        summary_prompt = f"""
Кратко суммируйте следующую часть диалога в 2-3 предложениях:

{chr(10).join(old_content)}

Краткая суммария:"""
        
        # В реальности здесь был бы вызов к модели для создания суммарии
        summary_content = f"[Суммарный контекст: диалог содержал {len(old_messages)} сообщений о различных темах]"
        
        summary_message = {
            'role': 'system',
            'content': f"Предыдущий контекст: {summary_content}"
        }
        
        return system_messages + [summary_message] + recent_messages
    
    def priority_based_retention(self, messages: List[Dict], 
                                priorities: Dict[str, float]) -> List[Dict]:
        """Сохранение сообщений на основе приоритетов"""
        # Присваиваем приоритеты сообщениям
        prioritized_messages = []
        
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            
            # Базовый приоритет по роли
            base_priority = priorities.get(role, 0.5)
            
            # Дополнительные факторы приоритета
            content_lower = content.lower()
            
            # Высокий приоритет для важных ключевых слов
            high_priority_keywords = ['ошибка', 'проблема', 'важно', 'срочно', 'критично']
            priority_boost = sum(0.1 for keyword in high_priority_keywords 
                                if keyword in content_lower)
            
            # Приоритет по длине (более длинные сообщения важнее)
            length_factor = min(len(content) / 1000, 0.2)
            
            final_priority = min(base_priority + priority_boost + length_factor, 1.0)
            
            prioritized_messages.append({
                **msg,
                '_priority': final_priority,
                '_token_count': self.token_counter(content)
            })
        
        # Сортируем по приоритету
        prioritized_messages.sort(key=lambda x: x['_priority'], reverse=True)
        
        # Отбираем сообщения в пределах лимита токенов
        selected_messages = []
        current_tokens = 0
        
        for msg in prioritized_messages:
            msg_tokens = msg['_token_count']
            
            if current_tokens + msg_tokens <= self.max_tokens:
                # Удаляем служебные поля
                clean_msg = {k: v for k, v in msg.items() 
                           if not k.startswith('_')}
                selected_messages.append(clean_msg)
                current_tokens += msg_tokens
        
        # Возвращаем в хронологическом порядке
        return sorted(selected_messages, 
                     key=lambda x: messages.index(next(m for m in messages 
                                                      if m['content'] == x['content'])))

# Демонстрация управления контекстом
context_manager = ContextWindowManager(max_tokens=200)  # Маленький лимит для демонстрации

# Пример диалога
sample_messages = [
    {'role': 'system', 'content': 'Вы помощник программиста'},
    {'role': 'user', 'content': 'Привет! Как дела?'},
    {'role': 'assistant', 'content': 'Привет! Всё хорошо, готов помочь с программированием.'},
    {'role': 'user', 'content': 'У меня критичная ошибка в коде Python'},
    {'role': 'assistant', 'content': 'Расскажите подробнее об ошибке, покажите код.'},
    {'role': 'user', 'content': 'Вот код: def func(): return x + y'},
    {'role': 'assistant', 'content': 'Проблема в том, что переменные x и y не определены.'},
    {'role': 'user', 'content': 'Спасибо, исправил!'},
    {'role': 'assistant', 'content': 'Отлично! Есть ли другие вопросы?'}
]

print("Исходный диалог:")
for i, msg in enumerate(sample_messages):
    print(f"{i+1}. {msg['role']}: {msg['content']}")

print(f"\nВсего токенов: {sum(context_manager.token_counter(msg['content']) for msg in sample_messages)}")

# Скользящее окно
sliding_result = context_manager.sliding_window_context(sample_messages, window_size=100)
print(f"\nСкользящее окно ({len(sliding_result)} сообщений):")
for msg in sliding_result:
    print(f"- {msg['role']}: {msg['content'][:50]}...")

# Приоритетная система
priorities = {
    'system': 1.0,
    'user': 0.7,
    'assistant': 0.5
}

priority_result = context_manager.priority_based_retention(sample_messages, priorities)
print(f"\nПриоритетное сохранение ({len(priority_result)} сообщений):")
for msg in priority_result:
    print(f"- {msg['role']}: {msg['content'][:50]}...")
```

## Ключевые моменты для экзамена

### Продвинутые техники промптинга
1. **Chain-of-Thought**: Пошаговое рассуждение для сложных задач
2. **Tree of Thoughts**: Исследование множественных путей решения
3. **Self-Consistency**: Повышение надежности через консенсус
4. **Zero/Few-shot learning**: Обучение на малом количестве примеров

### Оптимизация производительности
- **Domain-specific prompting**: Специализированные промпты для областей
- **Adaptive prompting**: Автоматическая оптимизация на основе результатов
- **Context window management**: Эффективное использование ограниченного контекста
- **Token optimization**: Сокращение затрат при сохранении качества

### Управление контекстом
- Sliding window для диалогов
- Hierarchical summarization для длинных разговоров
- Priority-based retention для важной информации
- Context compression techniques

### Метрики и оценка
- Success rate и accuracy измерения
- Response time оптимизация
- Token efficiency анализ
- A/B тестирование промптов

### Практические применения
- Автоматизация сложных рабочих процессов
- Создание интеллектуальных помощников
- Анализ и обработка больших объемов данных
- Персонализация пользовательского опыта