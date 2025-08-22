# Тема 21: Множественные модели в ИИ системах

## Концепция множественных моделей

### Причины использования нескольких моделей
- **Специализация**: Разные модели для разных задач
- **Резервирование**: Запасные модели при отказах
- **Балансировка нагрузки**: Распределение запросов
- **Оптимизация затрат**: Дешевые модели для простых задач
- **Качество**: Ансамбли для повышения точности

### Архитектуры множественных моделей
```python
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
import time

class ModelType(Enum):
    FAST_CHEAP = "fast_cheap"
    BALANCED = "balanced"
    ADVANCED = "advanced"
    SPECIALIZED = "specialized"

@dataclass
class ModelConfig:
    name: str
    model_type: ModelType
    max_tokens: int
    cost_per_token: float
    avg_response_time: float
    specialization: Optional[str] = None
    fallback_models: List[str] = None

class ModelManager:
    def __init__(self):
        self.models = {}
        self.usage_stats = {}
        self.load_balancer = LoadBalancer()
    
    def register_model(self, model_config: ModelConfig):
        """Регистрация модели в системе"""
        self.models[model_config.name] = model_config
        self.usage_stats[model_config.name] = {
            'requests': 0,
            'total_tokens': 0,
            'total_cost': 0,
            'avg_response_time': 0,
            'errors': 0
        }
    
    def select_model(self, task_type: str, complexity: str, 
                    budget_limit: float = None) -> str:
        """Выбор оптимальной модели для задачи"""
        
        # Фильтрация по специализации
        suitable_models = []
        for name, config in self.models.items():
            if config.specialization == task_type or config.specialization is None:
                suitable_models.append((name, config))
        
        if not suitable_models:
            raise ValueError(f"No models available for task type: {task_type}")
        
        # Выбор по сложности и бюджету
        if complexity == "simple" and budget_limit:
            # Выбираем самую дешевую подходящую модель
            return min(suitable_models, 
                      key=lambda x: x[1].cost_per_token)[0]
        
        elif complexity == "complex":
            # Выбираем самую продвинутую модель
            advanced_models = [m for m in suitable_models 
                             if m[1].model_type == ModelType.ADVANCED]
            if advanced_models:
                return advanced_models[0][0]
        
        # По умолчанию - сбалансированная модель
        balanced_models = [m for m in suitable_models 
                          if m[1].model_type == ModelType.BALANCED]
        return balanced_models[0][0] if balanced_models else suitable_models[0][0]

# Настройка моделей
model_manager = ModelManager()

# Регистрация различных моделей
model_manager.register_model(ModelConfig(
    name="gpt-3.5-turbo",
    model_type=ModelType.FAST_CHEAP,
    max_tokens=4096,
    cost_per_token=0.001,
    avg_response_time=1.5
))

model_manager.register_model(ModelConfig(
    name="gpt-4",
    model_type=ModelType.ADVANCED,
    max_tokens=8192,
    cost_per_token=0.03,
    avg_response_time=3.0
))

model_manager.register_model(ModelConfig(
    name="claude-3-haiku",
    model_type=ModelType.FAST_CHEAP,
    max_tokens=200000,
    cost_per_token=0.002,
    avg_response_time=2.0
))

# Выбор модели для разных задач
simple_task_model = model_manager.select_model("general", "simple", budget_limit=0.01)
complex_task_model = model_manager.select_model("analysis", "complex")

print(f"Для простой задачи: {simple_task_model}")
print(f"Для сложной задачи: {complex_task_model}")
```

## Балансировка нагрузки

### Стратегии распределения запросов
```python
import random
import heapq
from collections import defaultdict
from datetime import datetime, timedelta

class LoadBalancer:
    def __init__(self):
        self.model_queues = defaultdict(list)  # Очереди запросов для каждой модели
        self.model_load = defaultdict(int)     # Текущая нагрузка
        self.response_times = defaultdict(list) # История времени ответа
        
    def round_robin_selection(self, available_models: List[str]) -> str:
        """Круговой алгоритм выбора модели"""
        if not hasattr(self, '_round_robin_index'):
            self._round_robin_index = 0
        
        model = available_models[self._round_robin_index % len(available_models)]
        self._round_robin_index += 1
        return model
    
    def least_loaded_selection(self, available_models: List[str]) -> str:
        """Выбор наименее загруженной модели"""
        return min(available_models, key=lambda m: self.model_load[m])
    
    def weighted_random_selection(self, available_models: List[str], 
                                 weights: Dict[str, float]) -> str:
        """Взвешенный случайный выбор"""
        total_weight = sum(weights.get(model, 1.0) for model in available_models)
        r = random.uniform(0, total_weight)
        
        cumulative_weight = 0
        for model in available_models:
            cumulative_weight += weights.get(model, 1.0)
            if r <= cumulative_weight:
                return model
        
        return available_models[-1]
    
    def adaptive_selection(self, available_models: List[str]) -> str:
        """Адаптивный выбор на основе производительности"""
        # Вычисляем скор для каждой модели
        model_scores = {}
        
        for model in available_models:
            # Факторы: загрузка, время ответа, количество ошибок
            load_factor = 1.0 / (1.0 + self.model_load[model])
            
            recent_times = self.response_times[model][-10:]  # Последние 10 запросов
            avg_time = sum(recent_times) / len(recent_times) if recent_times else 1.0
            time_factor = 1.0 / avg_time
            
            # Комбинированный скор
            model_scores[model] = load_factor * 0.7 + time_factor * 0.3
        
        # Выбираем модель с лучшим скором
        return max(model_scores.items(), key=lambda x: x[1])[0]
    
    def update_model_stats(self, model: str, response_time: float, success: bool):
        """Обновление статистики модели"""
        self.response_times[model].append(response_time)
        
        # Ограничиваем историю
        if len(self.response_times[model]) > 100:
            self.response_times[model] = self.response_times[model][-50:]
        
        if success:
            self.model_load[model] = max(0, self.model_load[model] - 1)
        else:
            # Увеличиваем "нагрузку" при ошибках
            self.model_load[model] += 2

# Пример использования
load_balancer = LoadBalancer()
available_models = ["gpt-3.5-turbo", "gpt-4", "claude-3-haiku"]

# Имитация запросов
for i in range(10):
    selected_model = load_balancer.adaptive_selection(available_models)
    print(f"Запрос {i+1}: выбрана модель {selected_model}")
    
    # Имитация выполнения запроса
    response_time = random.uniform(1.0, 5.0)
    success = random.random() > 0.1  # 90% успешных запросов
    
    load_balancer.update_model_stats(selected_model, response_time, success)
```

### Система fallback моделей
```python
class FallbackModelSystem:
    def __init__(self):
        self.primary_models = {}
        self.fallback_chains = {}
        self.circuit_breakers = {}
    
    def configure_fallback_chain(self, task_type: str, model_chain: List[str]):
        """Настройка цепочки резервных моделей"""
        self.fallback_chains[task_type] = model_chain
        
        # Инициализация circuit breakers
        for model in model_chain:
            if model not in self.circuit_breakers:
                self.circuit_breakers[model] = CircuitBreaker(
                    failure_threshold=5,
                    recovery_timeout=60
                )
    
    async def execute_with_fallback(self, task_type: str, request_data: Dict) -> Dict:
        """Выполнение запроса с fallback логикой"""
        model_chain = self.fallback_chains.get(task_type, [])
        
        if not model_chain:
            raise ValueError(f"No models configured for task type: {task_type}")
        
        last_error = None
        
        for model_name in model_chain:
            circuit_breaker = self.circuit_breakers[model_name]
            
            # Проверяем состояние circuit breaker
            if circuit_breaker.is_open():
                print(f"Circuit breaker открыт для {model_name}, пропускаем")
                continue
            
            try:
                # Выполняем запрос к модели
                result = await self._call_model(model_name, request_data)
                circuit_breaker.record_success()
                
                return {
                    'result': result,
                    'model_used': model_name,
                    'fallback_level': model_chain.index(model_name)
                }
                
            except Exception as e:
                print(f"Ошибка в модели {model_name}: {e}")
                circuit_breaker.record_failure()
                last_error = e
                continue
        
        # Все модели недоступны
        raise Exception(f"Все модели недоступны. Последняя ошибка: {last_error}")
    
    async def _call_model(self, model_name: str, request_data: Dict) -> str:
        """Имитация вызова модели"""
        # Имитация сетевого запроса
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Имитация возможных ошибок
        if random.random() < 0.2:  # 20% вероятность ошибки
            raise Exception(f"Ошибка модели {model_name}")
        
        return f"Ответ от модели {model_name}: {request_data.get('prompt', 'test')}"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def is_open(self) -> bool:
        if self.state == 'OPEN':
            # Проверяем, не пора ли перейти в HALF_OPEN
            if (datetime.now() - self.last_failure_time).seconds > self.recovery_timeout:
                self.state = 'HALF_OPEN'
                return False
            return True
        return False
    
    def record_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'

# Пример настройки fallback системы
fallback_system = FallbackModelSystem()

# Настройка цепочек для разных типов задач
fallback_system.configure_fallback_chain("text_generation", [
    "gpt-4",           # Основная модель
    "gpt-3.5-turbo",   # Быстрая запасная
    "claude-3-haiku"   # Последний резерв
])

fallback_system.configure_fallback_chain("simple_qa", [
    "gpt-3.5-turbo",
    "claude-3-haiku"
])

# Пример использования
async def test_fallback():
    request = {"prompt": "Напиши короткий рассказ", "max_tokens": 200}
    
    try:
        result = await fallback_system.execute_with_fallback("text_generation", request)
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Все модели недоступны: {e}")

# asyncio.run(test_fallback())
```

## Ансамбли моделей

### Консенсус между моделями
```python
from typing import List, Tuple
import statistics

class ModelEnsemble:
    def __init__(self, models: List[str]):
        self.models = models
        self.weights = {model: 1.0 for model in models}  # Равные веса по умолчанию
    
    def set_model_weights(self, weights: Dict[str, float]):
        """Установка весов для моделей"""
        self.weights.update(weights)
    
    async def consensus_generation(self, prompt: str, temperature: float = 0.7) -> Dict:
        """Генерация с консенсусом между моделями"""
        responses = []
        
        # Получаем ответы от всех моделей
        for model in self.models:
            try:
                response = await self._call_model(model, prompt, temperature)
                responses.append({
                    'model': model,
                    'response': response,
                    'weight': self.weights[model]
                })
            except Exception as e:
                print(f"Ошибка модели {model}: {e}")
        
        if not responses:
            raise Exception("Ни одна модель не ответила")
        
        # Анализируем консенсус
        consensus_result = self._analyze_consensus(responses)
        
        return consensus_result
    
    def _analyze_consensus(self, responses: List[Dict]) -> Dict:
        """Анализ консенсуса между ответами"""
        # Простой пример: выбираем наиболее частые элементы
        
        # Разбиваем ответы на токены
        all_tokens = []
        for resp in responses:
            tokens = resp['response'].lower().split()
            weighted_tokens = tokens * int(resp['weight'])  # Учитываем вес
            all_tokens.extend(weighted_tokens)
        
        # Находим наиболее частые токены
        from collections import Counter
        token_counts = Counter(all_tokens)
        most_common = token_counts.most_common(10)
        
        # Оценка согласованности
        total_responses = len(responses)
        agreement_scores = []
        
        for resp in responses:
            other_responses = [r['response'] for r in responses if r != resp]
            similarity = self._calculate_similarity(resp['response'], other_responses)
            agreement_scores.append(similarity)
        
        avg_agreement = statistics.mean(agreement_scores) if agreement_scores else 0
        
        # Выбираем лучший ответ (с учетом веса и согласованности)
        best_response = max(responses, key=lambda r: r['weight'] * agreement_scores[responses.index(r)])
        
        return {
            'consensus_response': best_response['response'],
            'best_model': best_response['model'],
            'agreement_score': avg_agreement,
            'all_responses': responses,
            'common_themes': [token for token, count in most_common[:5]]
        }
    
    def _calculate_similarity(self, response: str, other_responses: List[str]) -> float:
        """Простой расчет схожести ответов"""
        if not other_responses:
            return 0.0
        
        response_tokens = set(response.lower().split())
        similarities = []
        
        for other in other_responses:
            other_tokens = set(other.lower().split())
            intersection = len(response_tokens & other_tokens)
            union = len(response_tokens | other_tokens)
            similarity = intersection / union if union > 0 else 0
            similarities.append(similarity)
        
        return statistics.mean(similarities)
    
    async def _call_model(self, model: str, prompt: str, temperature: float) -> str:
        """Имитация вызова модели"""
        await asyncio.sleep(random.uniform(1, 3))
        
        # Имитация разных ответов от разных моделей
        responses = {
            "gpt-4": f"Детальный ответ от GPT-4 на: {prompt}",
            "gpt-3.5-turbo": f"Быстрый ответ от GPT-3.5 на: {prompt}",
            "claude-3": f"Аналитический ответ от Claude на: {prompt}"
        }
        
        return responses.get(model, f"Ответ от {model}: {prompt}")

# Пример использования ансамбля
ensemble = ModelEnsemble(["gpt-4", "gpt-3.5-turbo", "claude-3"])

# Установка весов (GPT-4 важнее)
ensemble.set_model_weights({
    "gpt-4": 2.0,
    "gpt-3.5-turbo": 1.0,
    "claude-3": 1.5
})

async def test_ensemble():
    result = await ensemble.consensus_generation("Объясни квантовую физику")
    print(f"Консенсус: {result}")

# asyncio.run(test_ensemble())
```

### Специализированные модели для разных задач
```python
class SpecializedModelRouter:
    def __init__(self):
        self.task_models = {}
        self.model_capabilities = {}
    
    def register_specialized_model(self, task_type: str, model_name: str, 
                                 capabilities: Dict):
        """Регистрация специализированной модели"""
        if task_type not in self.task_models:
            self.task_models[task_type] = []
        
        self.task_models[task_type].append(model_name)
        self.model_capabilities[model_name] = capabilities
    
    def route_request(self, request: Dict) -> str:
        """Маршрутизация запроса к подходящей модели"""
        task_type = request.get('task_type')
        requirements = request.get('requirements', {})
        
        # Получаем доступные модели для задачи
        available_models = self.task_models.get(task_type, [])
        
        if not available_models:
            raise ValueError(f"No models available for task: {task_type}")
        
        # Фильтруем по требованиям
        suitable_models = []
        for model in available_models:
            capabilities = self.model_capabilities[model]
            
            # Проверяем соответствие требованиям
            if self._check_requirements(capabilities, requirements):
                suitable_models.append((model, capabilities))
        
        if not suitable_models:
            # Если нет подходящих, берем первую доступную
            return available_models[0]
        
        # Выбираем лучшую модель по критериям
        best_model = self._select_best_model(suitable_models, requirements)
        return best_model
    
    def _check_requirements(self, capabilities: Dict, requirements: Dict) -> bool:
        """Проверка соответствия возможностей требованиям"""
        for req, value in requirements.items():
            if req == 'max_tokens' and capabilities.get('max_tokens', 0) < value:
                return False
            elif req == 'languages' and not set(value).issubset(set(capabilities.get('languages', []))):
                return False
            elif req == 'speed' and capabilities.get('speed_score', 0) < value:
                return False
        
        return True
    
    def _select_best_model(self, suitable_models: List[Tuple], 
                          requirements: Dict) -> str:
        """Выбор лучшей модели по критериям"""
        # Простая система скоринга
        best_score = 0
        best_model = suitable_models[0][0]
        
        for model_name, capabilities in suitable_models:
            score = 0
            
            # Скор по скорости
            if 'speed' in requirements:
                score += capabilities.get('speed_score', 0) * 0.3
            
            # Скор по качеству
            score += capabilities.get('quality_score', 0) * 0.4
            
            # Скор по стоимости (инвертируем)
            cost = capabilities.get('cost_per_token', 1.0)
            score += (1.0 / cost) * 0.3
            
            if score > best_score:
                best_score = score
                best_model = model_name
        
        return best_model

# Настройка специализированного роутера
router = SpecializedModelRouter()

# Регистрация моделей для разных задач
router.register_specialized_model("code_generation", "codex", {
    'max_tokens': 8000,
    'languages': ['python', 'javascript', 'java', 'cpp'],
    'speed_score': 8,
    'quality_score': 9,
    'cost_per_token': 0.02
})

router.register_specialized_model("text_generation", "gpt-4", {
    'max_tokens': 8192,
    'languages': ['ru', 'en', 'es', 'fr'],
    'speed_score': 6,
    'quality_score': 10,
    'cost_per_token': 0.03
})

router.register_specialized_model("text_generation", "gpt-3.5-turbo", {
    'max_tokens': 4096,
    'languages': ['ru', 'en', 'es'],
    'speed_score': 9,
    'quality_score': 7,
    'cost_per_token': 0.001
})

router.register_specialized_model("translation", "opus-mt", {
    'max_tokens': 2048,
    'languages': ['ru', 'en', 'de', 'fr', 'es'],
    'speed_score': 10,
    'quality_score': 8,
    'cost_per_token': 0.0005
})

# Примеры маршрутизации
code_request = {
    'task_type': 'code_generation',
    'requirements': {
        'max_tokens': 4000,
        'languages': ['python'],
        'speed': 7
    }
}

text_request = {
    'task_type': 'text_generation',
    'requirements': {
        'max_tokens': 2000,
        'languages': ['ru'],
        'speed': 8
    }
}

print(f"Для генерации кода: {router.route_request(code_request)}")
print(f"Для генерации текста: {router.route_request(text_request)}")
```

## Ключевые моменты для экзамена

### Стратегии использования множественных моделей
1. **Специализация по задачам** - разные модели для разных типов запросов
2. **Иерархия по сложности** - простые модели для простых задач
3. **Географическое распределение** - модели в разных регионах
4. **Временное планирование** - разные модели для разного времени суток

### Технические решения
- **Load Balancing**: Round-robin, least-loaded, adaptive
- **Circuit Breakers**: Защита от каскадных отказов
- **Fallback Chains**: Цепочки резервных моделей
- **Model Ensembles**: Консенсус и голосование моделей

### Оптимизация и мониторинг
- Метрики производительности каждой модели
- Стоимость и ROI различных моделей
- Качество ответов и пользовательская удовлетворенность
- Время отклика и доступность сервисов

### Практические преимущества
- **Надежность**: Снижение единых точек отказа
- **Производительность**: Распределение нагрузки
- **Гибкость**: Адаптация к разным требованиям
- **Экономия**: Оптимальное использование ресурсов