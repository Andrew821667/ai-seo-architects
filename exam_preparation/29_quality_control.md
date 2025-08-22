# Тема 29: Контроль качества в ИИ системах

## Основы контроля качества

### Принципы QA в ИИ системах
- **Валидация данных**: Проверка качества входных данных
- **Мониторинг модели**: Отслеживание производительности в production
- **A/B тестирование**: Сравнение различных подходов
- **Обратная связь**: Сбор и анализ пользовательских оценок
- **Непрерывное улучшение**: Итеративная оптимизация системы

### Архитектура системы контроля качества
```python
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import statistics
import uuid

class QualityLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    UNACCEPTABLE = "unacceptable"

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    ACCURACY = "accuracy"
    USER_ACCEPTANCE = "user_acceptance"

@dataclass
class QualityMetric:
    """Метрика качества"""
    name: str
    value: float
    threshold: float
    unit: str
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)
    
    def is_passing(self) -> bool:
        """Проверка прохождения метрики"""
        return self.value >= self.threshold
    
    def get_quality_level(self) -> QualityLevel:
        """Определение уровня качества"""
        ratio = self.value / self.threshold if self.threshold > 0 else 0
        
        if ratio >= 1.2:
            return QualityLevel.EXCELLENT
        elif ratio >= 1.0:
            return QualityLevel.GOOD
        elif ratio >= 0.8:
            return QualityLevel.ACCEPTABLE
        elif ratio >= 0.6:
            return QualityLevel.POOR
        else:
            return QualityLevel.UNACCEPTABLE

@dataclass
class TestResult:
    """Результат тестирования"""
    test_id: str
    test_type: TestType
    test_name: str
    passed: bool
    score: float
    metrics: List[QualityMetric]
    execution_time: float
    timestamp: datetime
    error_message: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

class QualityController:
    """Контроллер качества для ИИ системы"""
    
    def __init__(self):
        self.test_results: List[TestResult] = []
        self.quality_standards = self._initialize_standards()
        self.evaluators = {}
        self.alerts = []
    
    def _initialize_standards(self) -> Dict[str, Dict[str, float]]:
        """Инициализация стандартов качества"""
        return {
            'accuracy': {
                'text_classification': 0.85,
                'sentiment_analysis': 0.80,
                'named_entity_recognition': 0.90,
                'text_generation_relevance': 0.75,
                'translation_quality': 0.85
            },
            'performance': {
                'response_time_ms': 2000,
                'throughput_requests_per_sec': 100,
                'memory_usage_mb': 1000,
                'cpu_utilization_percent': 80,
                'error_rate_percent': 1.0
            },
            'reliability': {
                'uptime_percent': 99.9,
                'availability_percent': 99.5,
                'data_integrity_percent': 100.0,
                'backup_success_rate': 100.0
            },
            'user_experience': {
                'user_satisfaction_score': 4.0,  # из 5
                'task_completion_rate': 0.90,
                'user_retention_rate': 0.80,
                'support_ticket_rate': 0.05
            }
        }
    
    def register_evaluator(self, test_type: str, evaluator_func: Callable):
        """Регистрация функции оценки"""
        self.evaluators[test_type] = evaluator_func
    
    def run_quality_check(self, component: str, test_data: Any, 
                         test_types: List[TestType] = None) -> List[TestResult]:
        """Запуск проверки качества"""
        
        if test_types is None:
            test_types = [TestType.ACCURACY, TestType.PERFORMANCE]
        
        results = []
        
        for test_type in test_types:
            start_time = datetime.now()
            
            try:
                result = self._execute_test(component, test_data, test_type)
                execution_time = (datetime.now() - start_time).total_seconds()
                
                test_result = TestResult(
                    test_id=str(uuid.uuid4()),
                    test_type=test_type,
                    test_name=f"{component}_{test_type.value}_test",
                    passed=result['passed'],
                    score=result['score'],
                    metrics=result['metrics'],
                    execution_time=execution_time,
                    timestamp=start_time,
                    details=result.get('details', {})
                )
                
                results.append(test_result)
                self.test_results.append(test_result)
                
            except Exception as e:
                error_result = TestResult(
                    test_id=str(uuid.uuid4()),
                    test_type=test_type,
                    test_name=f"{component}_{test_type.value}_test",
                    passed=False,
                    score=0.0,
                    metrics=[],
                    execution_time=(datetime.now() - start_time).total_seconds(),
                    timestamp=start_time,
                    error_message=str(e)
                )
                
                results.append(error_result)
                self.test_results.append(error_result)
        
        return results
    
    def _execute_test(self, component: str, test_data: Any, 
                     test_type: TestType) -> Dict[str, Any]:
        """Выполнение конкретного теста"""
        
        if test_type == TestType.ACCURACY:
            return self._test_accuracy(component, test_data)
        elif test_type == TestType.PERFORMANCE:
            return self._test_performance(component, test_data)
        elif test_type == TestType.USER_ACCEPTANCE:
            return self._test_user_acceptance(component, test_data)
        else:
            raise NotImplementedError(f"Тест типа {test_type} не реализован")
    
    def _test_accuracy(self, component: str, test_data: Any) -> Dict[str, Any]:
        """Тестирование точности"""
        
        # Симуляция тестирования точности
        import random
        
        # Генерируем метрики точности
        metrics = []
        
        if component == 'text_classifier':
            accuracy = random.uniform(0.75, 0.95)
            precision = random.uniform(0.70, 0.90)
            recall = random.uniform(0.70, 0.90)
            f1_score = 2 * (precision * recall) / (precision + recall)
            
            metrics = [
                QualityMetric("accuracy", accuracy, 0.85, "ratio", datetime.now()),
                QualityMetric("precision", precision, 0.80, "ratio", datetime.now()),
                QualityMetric("recall", recall, 0.80, "ratio", datetime.now()),
                QualityMetric("f1_score", f1_score, 0.80, "ratio", datetime.now())
            ]
            
            overall_score = statistics.mean([m.value for m in metrics])
            passed = all(m.is_passing() for m in metrics)
            
        elif component == 'text_generator':
            relevance = random.uniform(0.65, 0.85)
            coherence = random.uniform(0.70, 0.90)
            creativity = random.uniform(0.60, 0.85)
            
            metrics = [
                QualityMetric("relevance", relevance, 0.75, "ratio", datetime.now()),
                QualityMetric("coherence", coherence, 0.80, "ratio", datetime.now()),
                QualityMetric("creativity", creativity, 0.70, "ratio", datetime.now())
            ]
            
            overall_score = statistics.mean([m.value for m in metrics])
            passed = all(m.is_passing() for m in metrics)
        
        else:
            # Общий тест
            overall_score = random.uniform(0.70, 0.95)
            metrics = [
                QualityMetric("overall_accuracy", overall_score, 0.80, "ratio", datetime.now())
            ]
            passed = metrics[0].is_passing()
        
        return {
            'passed': passed,
            'score': overall_score,
            'metrics': metrics,
            'details': {
                'test_samples': len(test_data) if hasattr(test_data, '__len__') else 1,
                'component': component
            }
        }
    
    def _test_performance(self, component: str, test_data: Any) -> Dict[str, Any]:
        """Тестирование производительности"""
        import time
        import random
        
        # Симуляция нагрузочного тестирования
        start_time = time.time()
        
        # Имитация выполнения операций
        time.sleep(random.uniform(0.1, 0.5))
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # в миллисекундах
        
        # Генерируем метрики производительности
        throughput = random.uniform(80, 150)  # запросов в секунду
        memory_usage = random.uniform(200, 800)  # МБ
        cpu_usage = random.uniform(20, 70)  # процент
        
        metrics = [
            QualityMetric("response_time", response_time, 2000, "ms", datetime.now()),
            QualityMetric("throughput", throughput, 100, "req/sec", datetime.now()),
            QualityMetric("memory_usage", memory_usage, 1000, "MB", datetime.now()),
            QualityMetric("cpu_usage", cpu_usage, 80, "percent", datetime.now())
        ]
        
        passed = all(m.is_passing() for m in metrics)
        overall_score = statistics.mean([min(m.value / m.threshold, 1.0) for m in metrics])
        
        return {
            'passed': passed,
            'score': overall_score,
            'metrics': metrics,
            'details': {
                'load_duration': end_time - start_time,
                'component': component
            }
        }
    
    def _test_user_acceptance(self, component: str, test_data: Any) -> Dict[str, Any]:
        """Тестирование пользовательского приемлемости"""
        import random
        
        # Симуляция пользовательских оценок
        user_ratings = [random.uniform(3.0, 5.0) for _ in range(20)]
        completion_rates = [random.uniform(0.7, 1.0) for _ in range(20)]
        
        avg_rating = statistics.mean(user_ratings)
        avg_completion = statistics.mean(completion_rates)
        satisfaction_score = (avg_rating / 5.0 + avg_completion) / 2
        
        metrics = [
            QualityMetric("user_rating", avg_rating, 4.0, "stars", datetime.now()),
            QualityMetric("completion_rate", avg_completion, 0.90, "ratio", datetime.now()),
            QualityMetric("satisfaction_score", satisfaction_score, 0.80, "ratio", datetime.now())
        ]
        
        passed = all(m.is_passing() for m in metrics)
        
        return {
            'passed': passed,
            'score': satisfaction_score,
            'metrics': metrics,
            'details': {
                'test_users': len(user_ratings),
                'component': component
            }
        }
    
    def generate_quality_report(self, time_period: timedelta = None) -> Dict[str, Any]:
        """Генерация отчета о качестве"""
        
        if time_period is None:
            time_period = timedelta(days=7)
        
        cutoff_date = datetime.now() - time_period
        recent_results = [r for r in self.test_results if r.timestamp >= cutoff_date]
        
        if not recent_results:
            return {'error': 'Нет данных за указанный период'}
        
        # Группируем по типам тестов
        by_test_type = {}
        for result in recent_results:
            test_type = result.test_type.value
            if test_type not in by_test_type:
                by_test_type[test_type] = []
            by_test_type[test_type].append(result)
        
        # Анализируем каждый тип
        report = {
            'period': f'{time_period.days} дней',
            'total_tests': len(recent_results),
            'overall_pass_rate': sum(1 for r in recent_results if r.passed) / len(recent_results),
            'test_types': {},
            'trends': {},
            'recommendations': []
        }
        
        for test_type, results in by_test_type.items():
            type_analysis = {
                'tests_count': len(results),
                'pass_rate': sum(1 for r in results if r.passed) / len(results),
                'avg_score': statistics.mean([r.score for r in results]),
                'avg_execution_time': statistics.mean([r.execution_time for r in results]),
                'failed_tests': [r.test_name for r in results if not r.passed]
            }
            
            report['test_types'][test_type] = type_analysis
        
        # Генерируем рекомендации
        report['recommendations'] = self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Генерация рекомендаций по улучшению качества"""
        recommendations = []
        
        # Анализ общей успешности
        overall_pass_rate = report['overall_pass_rate']
        
        if overall_pass_rate < 0.9:
            recommendations.append(f"Общая успешность тестов ({overall_pass_rate:.1%}) ниже целевой (90%)")
            recommendations.append("Рассмотрите усиление процедур контроля качества")
        
        # Анализ по типам тестов
        for test_type, analysis in report['test_types'].items():
            if analysis['pass_rate'] < 0.85:
                recommendations.append(f"Низкая успешность {test_type} тестов ({analysis['pass_rate']:.1%})")
                
                if test_type == 'accuracy':
                    recommendations.append("Проверьте качество обучающих данных")
                    recommendations.append("Рассмотрите дополнительное обучение модели")
                elif test_type == 'performance':
                    recommendations.append("Оптимизируйте алгоритмы и инфраструктуру")
                    recommendations.append("Проверьте настройки кэширования")
            
            if analysis['avg_execution_time'] > 5.0:
                recommendations.append(f"Длительное время выполнения {test_type} тестов")
                recommendations.append("Рассмотрите параллельное выполнение тестов")
        
        return recommendations
    
    def setup_continuous_monitoring(self, component: str, 
                                  check_interval: int = 3600) -> str:
        """Настройка непрерывного мониторинга"""
        
        monitor_id = str(uuid.uuid4())
        
        # В реальной системе здесь был бы scheduler
        monitoring_config = {
            'monitor_id': monitor_id,
            'component': component,
            'interval_seconds': check_interval,
            'metrics_to_track': [
                'response_time',
                'error_rate',
                'throughput',
                'accuracy'
            ],
            'alert_thresholds': {
                'response_time': 3000,  # мс
                'error_rate': 0.05,     # 5%
                'throughput': 50,       # req/sec
                'accuracy': 0.75        # 75%
            }
        }
        
        print(f"Настроен мониторинг для {component}")
        print(f"ID мониторинга: {monitor_id}")
        print(f"Интервал проверки: {check_interval} секунд")
        
        return monitor_id

# Демонстрация системы контроля качества
qc = QualityController()

# Пример регистрации пользовательского оценщика
def custom_text_quality_evaluator(generated_text: str, expected_criteria: Dict) -> Dict:
    """Пользовательский оценщик качества текста"""
    
    # Критерии оценки текста
    scores = {}
    
    # Длина текста
    expected_length = expected_criteria.get('target_length', 100)
    actual_length = len(generated_text.split())
    length_score = 1.0 - abs(actual_length - expected_length) / max(expected_length, actual_length)
    scores['length_appropriateness'] = max(0, length_score)
    
    # Наличие ключевых слов
    required_keywords = expected_criteria.get('keywords', [])
    found_keywords = sum(1 for keyword in required_keywords 
                        if keyword.lower() in generated_text.lower())
    keyword_score = found_keywords / max(len(required_keywords), 1)
    scores['keyword_coverage'] = keyword_score
    
    # Читаемость (простая метрика)
    sentences = generated_text.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
    readability_score = 1.0 - max(0, (avg_sentence_length - 15) / 20)  # Оптимально ~15 слов
    scores['readability'] = max(0, readability_score)
    
    # Общий балл
    overall_score = statistics.mean(scores.values())
    
    return {
        'passed': overall_score >= 0.7,
        'score': overall_score,
        'details': scores
    }

qc.register_evaluator('text_quality', custom_text_quality_evaluator)

# Пример запуска тестов
test_data = {
    'input_text': 'Создай описание продукта для онлайн-магазина',
    'generated_output': 'Этот продукт отличается высоким качеством и доступной ценой. Идеально подходит для повседневного использования.',
    'expected_criteria': {
        'target_length': 20,
        'keywords': ['качество', 'цена', 'продукт'],
        'tone': 'professional'
    }
}

# Запускаем проверки качества
results = qc.run_quality_check('text_generator', test_data, [TestType.ACCURACY, TestType.PERFORMANCE])

print("=== РЕЗУЛЬТАТЫ КОНТРОЛЯ КАЧЕСТВА ===")
for result in results:
    print(f"Тест: {result.test_name}")
    print(f"Успешность: {'✅ ПРОЙДЕН' if result.passed else '❌ НЕ ПРОЙДЕН'}")
    print(f"Оценка: {result.score:.2f}")
    print(f"Время выполнения: {result.execution_time:.3f}с")
    
    if result.metrics:
        print("Метрики:")
        for metric in result.metrics:
            status = "✅" if metric.is_passing() else "❌"
            print(f"  {status} {metric.name}: {metric.value:.3f} (порог: {metric.threshold})")
    
    if result.error_message:
        print(f"Ошибка: {result.error_message}")
    
    print()

# Генерируем отчет о качестве
quality_report = qc.generate_quality_report(timedelta(days=1))

print("=== ОТЧЕТ О КАЧЕСТВЕ ===")
print(f"Период: {quality_report['period']}")
print(f"Всего тестов: {quality_report['total_tests']}")
print(f"Общая успешность: {quality_report['overall_pass_rate']:.1%}")

print("\nПо типам тестов:")
for test_type, analysis in quality_report['test_types'].items():
    print(f"  {test_type}:")
    print(f"    Успешность: {analysis['pass_rate']:.1%}")
    print(f"    Средняя оценка: {analysis['avg_score']:.2f}")
    print(f"    Время выполнения: {analysis['avg_execution_time']:.2f}с")

print("\nРекомендации:")
for recommendation in quality_report['recommendations']:
    print(f"  💡 {recommendation}")
```

## Автоматизированное тестирование

### Unit тесты для ИИ компонентов
```python
import unittest
from unittest.mock import Mock, patch
import numpy as np

class AIComponentTester:
    """Тестировщик ИИ компонентов"""
    
    def __init__(self):
        self.test_datasets = {}
        self.baseline_results = {}
    
    def create_test_dataset(self, component_type: str, 
                          samples: List[Dict]) -> str:
        """Создание тестового набора данных"""
        dataset_id = f"{component_type}_test_{len(self.test_datasets)}"
        
        self.test_datasets[dataset_id] = {
            'component_type': component_type,
            'samples': samples,
            'created_at': datetime.now(),
            'validated': False
        }
        
        return dataset_id
    
    def validate_test_dataset(self, dataset_id: str) -> bool:
        """Валидация тестового набора"""
        if dataset_id not in self.test_datasets:
            return False
        
        dataset = self.test_datasets[dataset_id]
        samples = dataset['samples']
        
        # Проверки валидности
        checks = [
            len(samples) >= 10,  # Минимум 10 образцов
            all('input' in sample for sample in samples),  # Все имеют входы
            all('expected_output' in sample for sample in samples),  # Все имеют ожидаемые выходы
            len(set(str(s['input']) for s in samples)) > len(samples) * 0.8  # Разнообразие >= 80%
        ]
        
        is_valid = all(checks)
        dataset['validated'] = is_valid
        
        return is_valid
    
    def run_regression_tests(self, component, dataset_id: str) -> Dict[str, Any]:
        """Запуск регрессионных тестов"""
        
        if dataset_id not in self.test_datasets:
            raise ValueError(f"Тестовый набор {dataset_id} не найден")
        
        dataset = self.test_datasets[dataset_id]
        
        if not dataset['validated']:
            raise ValueError(f"Тестовый набор {dataset_id} не валидирован")
        
        test_results = []
        
        for i, sample in enumerate(dataset['samples']):
            try:
                # Выполняем тест
                actual_output = self._execute_component(component, sample['input'])
                expected_output = sample['expected_output']
                
                # Сравниваем результаты
                similarity_score = self._compare_outputs(actual_output, expected_output)
                
                test_results.append({
                    'sample_id': i,
                    'input': sample['input'],
                    'expected': expected_output,
                    'actual': actual_output,
                    'similarity': similarity_score,
                    'passed': similarity_score >= 0.8
                })
                
            except Exception as e:
                test_results.append({
                    'sample_id': i,
                    'input': sample['input'],
                    'error': str(e),
                    'passed': False
                })
        
        # Анализ результатов
        passed_tests = sum(1 for r in test_results if r.get('passed', False))
        pass_rate = passed_tests / len(test_results)
        
        avg_similarity = statistics.mean([
            r.get('similarity', 0) for r in test_results 
            if 'similarity' in r
        ]) if any('similarity' in r for r in test_results) else 0
        
        return {
            'dataset_id': dataset_id,
            'total_tests': len(test_results),
            'passed_tests': passed_tests,
            'pass_rate': pass_rate,
            'avg_similarity': avg_similarity,
            'detailed_results': test_results,
            'regression_detected': pass_rate < 0.9  # Регрессия если < 90%
        }
    
    def _execute_component(self, component, input_data) -> Any:
        """Выполнение компонента (заглушка)"""
        # В реальности здесь был бы вызов к компоненту
        if hasattr(component, 'predict') or hasattr(component, '__call__'):
            return component(input_data)
        else:
            # Имитация обработки
            if isinstance(input_data, str):
                return f"Обработанный результат для: {input_data[:50]}..."
            else:
                return {"result": "processed_data"}
    
    def _compare_outputs(self, actual: Any, expected: Any) -> float:
        """Сравнение выходных данных"""
        
        if isinstance(actual, str) and isinstance(expected, str):
            # Для текста используем простую схожесть
            actual_words = set(actual.lower().split())
            expected_words = set(expected.lower().split())
            
            if not expected_words:
                return 1.0 if not actual_words else 0.0
            
            intersection = len(actual_words & expected_words)
            union = len(actual_words | expected_words)
            
            return intersection / union if union > 0 else 0.0
        
        elif isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            # Для чисел используем относительную ошибку
            if expected == 0:
                return 1.0 if actual == 0 else 0.0
            
            relative_error = abs(actual - expected) / abs(expected)
            return max(0, 1.0 - relative_error)
        
        elif isinstance(actual, dict) and isinstance(expected, dict):
            # Для словарей сравниваем ключи и значения
            all_keys = set(actual.keys()) | set(expected.keys())
            if not all_keys:
                return 1.0
            
            matching_score = 0
            for key in all_keys:
                if key in actual and key in expected:
                    matching_score += self._compare_outputs(actual[key], expected[key])
                elif key in actual or key in expected:
                    matching_score += 0.0  # Несоответствие
            
            return matching_score / len(all_keys)
        
        else:
            # Простое сравнение
            return 1.0 if actual == expected else 0.0

# Пример unit тестов для ИИ компонентов
class TestAIComponents(unittest.TestCase):
    """Unit тесты для ИИ компонентов"""
    
    def setUp(self):
        self.tester = AIComponentTester()
        self.mock_classifier = Mock()
        self.mock_generator = Mock()
    
    def test_text_classifier(self):
        """Тест классификатора текста"""
        
        # Настройка мок объекта
        self.mock_classifier.return_value = {
            'label': 'positive',
            'confidence': 0.85
        }
        
        # Создание тестового набора
        test_samples = [
            {
                'input': 'Этот продукт просто замечательный!',
                'expected_output': {'label': 'positive', 'confidence': 0.8}
            },
            {
                'input': 'Ужасное качество, не рекомендую.',
                'expected_output': {'label': 'negative', 'confidence': 0.8}
            }
        ]
        
        dataset_id = self.tester.create_test_dataset('text_classifier', test_samples)
        self.assertTrue(self.tester.validate_test_dataset(dataset_id))
        
        # Запуск тестов
        results = self.tester.run_regression_tests(self.mock_classifier, dataset_id)
        
        self.assertGreaterEqual(results['pass_rate'], 0.8)
        self.assertFalse(results['regression_detected'])
    
    def test_text_generator_quality(self):
        """Тест качества генератора текста"""
        
        # Настройка мок генератора
        self.mock_generator.side_effect = [
            "Высококачественный продукт с отличными характеристиками",
            "Инновационное решение для современных потребностей"
        ]
        
        test_samples = [
            {
                'input': 'Опишите смартфон',
                'expected_output': 'описание технических характеристик смартфона'
            },
            {
                'input': 'Напишите о наушниках',
                'expected_output': 'обзор функций и качества наушников'
            }
        ]
        
        dataset_id = self.tester.create_test_dataset('text_generator', test_samples)
        results = self.tester.run_regression_tests(self.mock_generator, dataset_id)
        
        self.assertIsInstance(results['pass_rate'], float)
        self.assertGreaterEqual(results['avg_similarity'], 0.0)
    
    def test_performance_requirements(self):
        """Тест требований производительности"""
        
        # Имитация медленного компонента
        def slow_component(input_data):
            import time
            time.sleep(0.1)  # Имитация обработки
            return f"Результат для {input_data}"
        
        start_time = datetime.now()
        result = slow_component("тестовые данные")
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Проверяем, что время выполнения в пределах нормы
        self.assertLess(execution_time, 1.0, "Компонент работает слишком медленно")
        self.assertIsNotNone(result, "Компонент должен возвращать результат")

# Пример запуска тестов
if __name__ == "__main__":
    # Создаем и запускаем тесты
    print("=== ЗАПУСК UNIT ТЕСТОВ ===")
    
    # Создаем test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAIComponents)
    runner = unittest.TextTestRunner(verbosity=2)
    
    # В реальности тесты запускались бы так:
    # runner.run(suite)
    
    # Для демонстрации просто показываем структуру
    print("Структура тестов:")
    print("  ✓ test_text_classifier")
    print("  ✓ test_text_generator_quality") 
    print("  ✓ test_performance_requirements")
    print()
    
    # Демонстрация создания тестового набора
    tester = AIComponentTester()
    
    sentiment_samples = [
        {'input': 'Отличный сервис!', 'expected_output': 'positive'},
        {'input': 'Ужасно разочарован', 'expected_output': 'negative'},
        {'input': 'Обычный товар', 'expected_output': 'neutral'}
    ]
    
    dataset_id = tester.create_test_dataset('sentiment_analysis', sentiment_samples)
    is_valid = tester.validate_test_dataset(dataset_id)
    
    print(f"Создан тестовый набор: {dataset_id}")
    print(f"Валидность: {'✅' if is_valid else '❌'}")
```

## Мониторинг в production

### Real-time мониторинг качества
```python
import asyncio
from collections import deque
import time

class ProductionQualityMonitor:
    """Мониторинг качества в production среде"""
    
    def __init__(self, alert_thresholds: Dict[str, float]):
        self.alert_thresholds = alert_thresholds
        self.metrics_buffer = deque(maxlen=1000)  # Буфер последних 1000 метрик
        self.alerts_history = []
        self.is_monitoring = False
        
        # Скользящие окна для анализа трендов
        self.sliding_windows = {
            'short_term': deque(maxlen=50),   # Последние 50 запросов
            'medium_term': deque(maxlen=200), # Последние 200 запросов
            'long_term': deque(maxlen=1000)   # Последние 1000 запросов
        }
    
    async def start_monitoring(self, component_name: str):
        """Запуск мониторинга"""
        self.is_monitoring = True
        self.component_name = component_name
        
        print(f"🔍 Запуск мониторинга для {component_name}")
        
        # Запускаем асинхронные задачи мониторинга
        tasks = [
            asyncio.create_task(self._monitor_performance()),
            asyncio.create_task(self._monitor_accuracy()),
            asyncio.create_task(self._analyze_trends()),
            asyncio.create_task(self._check_alerts())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            print("Мониторинг остановлен")
        finally:
            self.is_monitoring = False
    
    async def _monitor_performance(self):
        """Мониторинг производительности"""
        while self.is_monitoring:
            try:
                # Симуляция сбора метрик производительности
                await asyncio.sleep(1)  # Проверка каждую секунду
                
                performance_metrics = {
                    'timestamp': datetime.now(),
                    'response_time': np.random.normal(1500, 300),  # мс
                    'cpu_usage': np.random.normal(45, 10),         # %
                    'memory_usage': np.random.normal(512, 100),    # МБ
                    'requests_per_sec': np.random.normal(120, 20)
                }
                
                self._record_metrics('performance', performance_metrics)
                
            except Exception as e:
                print(f"Ошибка мониторинга производительности: {e}")
                await asyncio.sleep(5)
    
    async def _monitor_accuracy(self):
        """Мониторинг точности"""
        while self.is_monitoring:
            try:
                await asyncio.sleep(10)  # Проверка каждые 10 секунд
                
                # Симуляция оценки точности на батче запросов
                accuracy_metrics = {
                    'timestamp': datetime.now(),
                    'accuracy': np.random.normal(0.85, 0.05),
                    'precision': np.random.normal(0.82, 0.04),
                    'recall': np.random.normal(0.88, 0.03),
                    'user_satisfaction': np.random.normal(4.2, 0.3)  # из 5
                }
                
                self._record_metrics('accuracy', accuracy_metrics)
                
            except Exception as e:
                print(f"Ошибка мониторинга точности: {e}")
                await asyncio.sleep(15)
    
    async def _analyze_trends(self):
        """Анализ трендов"""
        while self.is_monitoring:
            try:
                await asyncio.sleep(60)  # Анализ каждую минуту
                
                for window_name, window_data in self.sliding_windows.items():
                    if len(window_data) >= 10:  # Минимум данных для анализа
                        trend_analysis = self._calculate_trends(window_data)
                        
                        if trend_analysis['degradation_detected']:
                            await self._trigger_alert(
                                'performance_degradation',
                                f"Обнаружена деградация производительности в {window_name} окне",
                                trend_analysis
                            )
                
            except Exception as e:
                print(f"Ошибка анализа трендов: {e}")
                await asyncio.sleep(60)
    
    async def _check_alerts(self):
        """Проверка пороговых значений для алертов"""
        while self.is_monitoring:
            try:
                await asyncio.sleep(5)  # Проверка каждые 5 секунд
                
                if len(self.metrics_buffer) == 0:
                    continue
                
                latest_metrics = self.metrics_buffer[-1]
                
                # Проверяем пороговые значения
                for metric_name, threshold in self.alert_thresholds.items():
                    if metric_name in latest_metrics:
                        value = latest_metrics[metric_name]
                        
                        # Разные типы проверок для разных метрик
                        alert_triggered = False
                        
                        if metric_name == 'response_time' and value > threshold:
                            alert_triggered = True
                        elif metric_name == 'accuracy' and value < threshold:
                            alert_triggered = True
                        elif metric_name == 'error_rate' and value > threshold:
                            alert_triggered = True
                        elif metric_name == 'cpu_usage' and value > threshold:
                            alert_triggered = True
                        
                        if alert_triggered:
                            await self._trigger_alert(
                                'threshold_violation',
                                f"{metric_name} превысил порог: {value:.2f} > {threshold:.2f}",
                                {'metric': metric_name, 'value': value, 'threshold': threshold}
                            )
                
            except Exception as e:
                print(f"Ошибка проверки алертов: {e}")
                await asyncio.sleep(10)
    
    def _record_metrics(self, category: str, metrics: Dict[str, Any]):
        """Запись метрик"""
        metrics['category'] = category
        
        # Добавляем в основной буфер
        self.metrics_buffer.append(metrics)
        
        # Добавляем в скользящие окна
        for window in self.sliding_windows.values():
            window.append(metrics)
    
    def _calculate_trends(self, window_data: deque) -> Dict[str, Any]:
        """Расчет трендов"""
        if len(window_data) < 10:
            return {'degradation_detected': False}
        
        # Анализируем тренд времени ответа
        recent_data = list(window_data)[-10:]
        earlier_data = list(window_data)[-20:-10] if len(window_data) >= 20 else recent_data
        
        # Извлекаем response_time для анализа
        recent_response_times = [d.get('response_time') for d in recent_data 
                               if d.get('response_time') is not None]
        earlier_response_times = [d.get('response_time') for d in earlier_data 
                                if d.get('response_time') is not None]
        
        if recent_response_times and earlier_response_times:
            recent_avg = statistics.mean(recent_response_times)
            earlier_avg = statistics.mean(earlier_response_times)
            
            # Деградация если время ответа увеличилось на 20%
            degradation_detected = recent_avg > earlier_avg * 1.2
            
            return {
                'degradation_detected': degradation_detected,
                'recent_avg_response_time': recent_avg,
                'earlier_avg_response_time': earlier_avg,
                'degradation_percent': ((recent_avg - earlier_avg) / earlier_avg) * 100
            }
        
        return {'degradation_detected': False}
    
    async def _trigger_alert(self, alert_type: str, message: str, 
                           details: Dict[str, Any]):
        """Отправка алерта"""
        alert = {
            'id': str(uuid.uuid4()),
            'type': alert_type,
            'message': message,
            'component': self.component_name,
            'timestamp': datetime.now(),
            'details': details,
            'status': 'active'
        }
        
        self.alerts_history.append(alert)
        
        # В реальной системе здесь была бы отправка в Slack, email, etc.
        print(f"🚨 АЛЕРТ [{alert_type.upper()}]: {message}")
        
        # Автоматические действия при критических алертах
        if alert_type == 'threshold_violation' and details.get('metric') == 'accuracy':
            if details.get('value', 0) < 0.6:  # Критическое снижение точности
                print("🔧 Автоматическое действие: переключение на резервную модель")
                await self._execute_fallback_procedure()
    
    async def _execute_fallback_procedure(self):
        """Выполнение процедуры отката"""
        print("Выполняется процедура отката...")
        await asyncio.sleep(1)  # Имитация времени переключения
        print("✅ Переключение на резервную систему завершено")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Получение текущего статуса здоровья системы"""
        if not self.metrics_buffer:
            return {'status': 'unknown', 'reason': 'Нет данных'}
        
        latest_metrics = self.metrics_buffer[-1]
        
        # Проверяем ключевые метрики
        health_checks = {}
        overall_healthy = True
        
        for metric_name, threshold in self.alert_thresholds.items():
            if metric_name in latest_metrics:
                value = latest_metrics[metric_name]
                
                if metric_name in ['response_time', 'error_rate', 'cpu_usage']:
                    is_healthy = value <= threshold
                else:  # accuracy, availability, etc.
                    is_healthy = value >= threshold
                
                health_checks[metric_name] = {
                    'value': value,
                    'threshold': threshold,
                    'healthy': is_healthy
                }
                
                if not is_healthy:
                    overall_healthy = False
        
        # Проверяем недавние алерты
        recent_alerts = [a for a in self.alerts_history 
                        if a['timestamp'] > datetime.now() - timedelta(minutes=5)]
        
        status = 'healthy' if overall_healthy and not recent_alerts else 'degraded'
        if any(not check['healthy'] for check in health_checks.values()):
            status = 'unhealthy'
        
        return {
            'status': status,
            'health_checks': health_checks,
            'recent_alerts_count': len(recent_alerts),
            'last_check': latest_metrics['timestamp'],
            'uptime_status': 'operational'  # В реальности рассчитывалось бы из метрик
        }

# Демонстрация production мониторинга
async def demo_production_monitoring():
    """Демонстрация мониторинга в production"""
    
    # Настраиваем пороги алертов
    alert_thresholds = {
        'response_time': 2000,  # мс
        'accuracy': 0.8,        # 80%
        'cpu_usage': 85,        # %
        'memory_usage': 900,    # МБ
        'error_rate': 0.05      # 5%
    }
    
    monitor = ProductionQualityMonitor(alert_thresholds)
    
    # Запускаем мониторинг на короткое время для демонстрации
    monitoring_task = asyncio.create_task(monitor.start_monitoring('ai_text_processor'))
    
    # Даем поработать 10 секунд
    await asyncio.sleep(10)
    
    # Останавливаем мониторинг
    monitoring_task.cancel()
    
    try:
        await monitoring_task
    except asyncio.CancelledError:
        pass
    
    # Показываем результаты
    health_status = monitor.get_health_status()
    
    print("\n=== СТАТУС ЗДОРОВЬЯ СИСТЕМЫ ===")
    print(f"Общий статус: {health_status['status'].upper()}")
    print(f"Последняя проверка: {health_status.get('last_check', 'N/A')}")
    print(f"Недавние алерты: {health_status.get('recent_alerts_count', 0)}")
    
    print("\nПроверки здоровья:")
    for metric, check in health_status.get('health_checks', {}).items():
        status_icon = "✅" if check['healthy'] else "❌"
        print(f"  {status_icon} {metric}: {check['value']:.2f} (порог: {check['threshold']})")
    
    print(f"\nВсего алертов за сессию: {len(monitor.alerts_history)}")
    
    # Показываем последние алерты
    if monitor.alerts_history:
        print("Последние алерты:")
        for alert in monitor.alerts_history[-3:]:  # Последние 3
            print(f"  🚨 {alert['timestamp'].strftime('%H:%M:%S')}: {alert['message']}")

# Запуск демонстрации
print("=== ДЕМОНСТРАЦИЯ PRODUCTION МОНИТОРИНГА ===")
# asyncio.run(demo_production_monitoring())

# Настройка мониторинга
monitor_id = qc.setup_continuous_monitoring('ai_video_generator', check_interval=1800)
print(f"\nНастроен мониторинг с ID: {monitor_id}")
```

## Ключевые моменты для экзамена

### Компоненты системы контроля качества
1. **Метрики качества**: Accuracy, precision, recall, F1-score, user satisfaction
2. **Типы тестирования**: Unit, integration, performance, user acceptance
3. **Мониторинг**: Real-time отслеживание в production среде
4. **Алертинг**: Автоматические уведомления о проблемах

### Методы оценки качества
- **Автоматизированные тесты**: Регрессионные тесты, smoke tests
- **Пользовательская обратная связь**: Рейтинги, отзывы, поведенческие метрики
- **A/B тестирование**: Сравнение различных подходов
- **Benchmark тестирование**: Сравнение с эталонными результатами

### Стратегии обеспечения качества
- **Непрерывная интеграция**: Автоматические тесты при каждом изменении
- **Постепенное развертывание**: Canary deployments и blue-green deployments
- **Fallback механизмы**: Автоматическое переключение при деградации
- **Data validation**: Проверка качества входных данных

### Метрики и KPI
- **Технические метрики**: Response time, throughput, error rate, uptime
- **Качественные метрики**: Accuracy, relevance, coherence, user satisfaction  
- **Бизнес метрики**: Conversion rate, user retention, task completion rate
- **Операционные метрики**: Alert frequency, MTTR, MTBF

### Инструменты и технологии
- **Мониторинг**: Prometheus, Grafana, DataDog, New Relic
- **Тестирование**: pytest, unittest, MLflow, Weights & Biases
- **Алертинг**: PagerDuty, Slack integrations, email notifications
- **Аналитика**: Custom dashboards, ML experiment tracking