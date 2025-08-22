# Тема 31: AI-продажи - Искусственный интеллект в продажах

## Основы AI в продажах

### Применение ИИ в продажных процессах
- **Lead Generation**: Автоматическое привлечение потенциальных клиентов
- **Lead Scoring**: Оценка и приоритизация лидов
- **Sales Forecasting**: Прогнозирование продаж
- **Customer Segmentation**: Сегментация клиентов
- **Personalization**: Персонализация предложений
- **Churn Prevention**: Предотвращение оттока клиентов

### Архитектура AI-продажной системы
```python
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import statistics
import json
import uuid

class LeadStatus(Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class CustomerSegment(Enum):
    ENTERPRISE = "enterprise"
    SMB = "smb"
    STARTUP = "startup"
    INDIVIDUAL = "individual"

class SalesStage(Enum):
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    DECISION = "decision"
    RETENTION = "retention"
    EXPANSION = "expansion"

@dataclass
class Lead:
    """Потенциальный клиент"""
    id: str
    company: str
    contact_person: str
    email: str
    phone: Optional[str]
    industry: str
    company_size: int  # Количество сотрудников
    annual_revenue: Optional[int]
    source: str  # Источник лида
    created_at: datetime
    status: LeadStatus = LeadStatus.NEW
    score: Optional[float] = None
    segment: Optional[CustomerSegment] = None
    interactions: List[Dict] = field(default_factory=list)

@dataclass
class SalesOpportunity:
    """Продажная возможность"""
    id: str
    lead_id: str
    product: str
    estimated_value: float
    probability: float
    expected_close_date: datetime
    stage: SalesStage
    sales_rep: str
    activities: List[Dict] = field(default_factory=list)
    competitors: List[str] = field(default_factory=list)

@dataclass
class Customer:
    """Клиент"""
    id: str
    company: str
    segment: CustomerSegment
    lifetime_value: float
    churn_risk: float
    satisfaction_score: float
    last_purchase_date: datetime
    purchase_history: List[Dict] = field(default_factory=list)

class LeadScoringEngine:
    """Движок оценки лидов"""
    
    def __init__(self):
        self.scoring_model = self._initialize_scoring_model()
        self.feature_weights = self._initialize_feature_weights()
    
    def _initialize_scoring_model(self) -> Dict[str, Any]:
        """Инициализация модели оценки"""
        return {
            'demographic': {
                'company_size': {
                    'small': 0.3,      # 1-50 сотрудников
                    'medium': 0.7,     # 51-500
                    'large': 1.0,      # 500+
                    'enterprise': 1.0  # 1000+
                },
                'industry': {
                    'technology': 0.9,
                    'finance': 0.8,
                    'healthcare': 0.7,
                    'education': 0.6,
                    'retail': 0.5,
                    'other': 0.4
                },
                'revenue': {
                    'startup': 0.4,     # < 1M
                    'growing': 0.7,     # 1M-10M
                    'established': 0.9, # 10M-100M
                    'enterprise': 1.0   # 100M+
                }
            },
            'behavioral': {
                'email_engagement': {
                    'opened': 0.3,
                    'clicked': 0.6,
                    'replied': 0.9,
                    'forwarded': 1.0
                },
                'website_activity': {
                    'visited': 0.2,
                    'multiple_pages': 0.5,
                    'pricing_page': 0.8,
                    'demo_request': 1.0
                },
                'content_engagement': {
                    'downloaded_whitepaper': 0.6,
                    'attended_webinar': 0.8,
                    'requested_trial': 1.0
                }
            },
            'firmographic': {
                'technology_stack': {
                    'compatible': 0.8,
                    'needs_integration': 0.6,
                    'incompatible': 0.2
                },
                'budget_signals': {
                    'budget_confirmed': 1.0,
                    'budget_likely': 0.7,
                    'budget_unknown': 0.4,
                    'no_budget': 0.1
                }
            }
        }
    
    def _initialize_feature_weights(self) -> Dict[str, float]:
        """Инициализация весов признаков"""
        return {
            'demographic': 0.25,
            'behavioral': 0.40,
            'firmographic': 0.20,
            'temporal': 0.15
        }
    
    def calculate_lead_score(self, lead: Lead, 
                           additional_data: Dict[str, Any] = None) -> float:
        """Расчет оценки лида"""
        
        if additional_data is None:
            additional_data = {}
        
        # Демографическая оценка
        demographic_score = self._calculate_demographic_score(lead)
        
        # Поведенческая оценка
        behavioral_score = self._calculate_behavioral_score(lead, additional_data)
        
        # Фирмографическая оценка
        firmographic_score = self._calculate_firmographic_score(lead, additional_data)
        
        # Временная оценка (свежесть лида)
        temporal_score = self._calculate_temporal_score(lead)
        
        # Взвешенная итоговая оценка
        total_score = (
            demographic_score * self.feature_weights['demographic'] +
            behavioral_score * self.feature_weights['behavioral'] +
            firmographic_score * self.feature_weights['firmographic'] +
            temporal_score * self.feature_weights['temporal']
        )
        
        return min(total_score * 100, 100)  # Нормализуем до 0-100
    
    def _calculate_demographic_score(self, lead: Lead) -> float:
        """Расчет демографической оценки"""
        scores = []
        
        # Размер компании
        if lead.company_size <= 50:
            company_size_score = self.scoring_model['demographic']['company_size']['small']
        elif lead.company_size <= 500:
            company_size_score = self.scoring_model['demographic']['company_size']['medium']
        elif lead.company_size <= 1000:
            company_size_score = self.scoring_model['demographic']['company_size']['large']
        else:
            company_size_score = self.scoring_model['demographic']['company_size']['enterprise']
        
        scores.append(company_size_score)
        
        # Индустрия
        industry_score = self.scoring_model['demographic']['industry'].get(
            lead.industry.lower(), 
            self.scoring_model['demographic']['industry']['other']
        )
        scores.append(industry_score)
        
        # Выручка
        if lead.annual_revenue:
            if lead.annual_revenue < 1000000:
                revenue_score = self.scoring_model['demographic']['revenue']['startup']
            elif lead.annual_revenue < 10000000:
                revenue_score = self.scoring_model['demographic']['revenue']['growing']
            elif lead.annual_revenue < 100000000:
                revenue_score = self.scoring_model['demographic']['revenue']['established']
            else:
                revenue_score = self.scoring_model['demographic']['revenue']['enterprise']
            
            scores.append(revenue_score)
        
        return statistics.mean(scores) if scores else 0.5
    
    def _calculate_behavioral_score(self, lead: Lead, 
                                  additional_data: Dict[str, Any]) -> float:
        """Расчет поведенческой оценки"""
        
        behavior_data = additional_data.get('behavior', {})
        scores = []
        
        # Email активность
        email_actions = behavior_data.get('email_actions', [])
        email_score = 0
        for action in email_actions:
            action_score = self.scoring_model['behavioral']['email_engagement'].get(action, 0)
            email_score = max(email_score, action_score)
        scores.append(email_score)
        
        # Активность на сайте
        website_actions = behavior_data.get('website_actions', [])
        website_score = 0
        for action in website_actions:
            action_score = self.scoring_model['behavioral']['website_activity'].get(action, 0)
            website_score = max(website_score, action_score)
        scores.append(website_score)
        
        # Взаимодействие с контентом
        content_actions = behavior_data.get('content_actions', [])
        content_score = 0
        for action in content_actions:
            action_score = self.scoring_model['behavioral']['content_engagement'].get(action, 0)
            content_score = max(content_score, action_score)
        scores.append(content_score)
        
        return statistics.mean(scores) if scores else 0.3
    
    def _calculate_firmographic_score(self, lead: Lead, 
                                    additional_data: Dict[str, Any]) -> float:
        """Расчет фирмографической оценки"""
        
        firmographic_data = additional_data.get('firmographic', {})
        scores = []
        
        # Технологический стек
        tech_compatibility = firmographic_data.get('tech_compatibility', 'unknown')
        tech_score = self.scoring_model['firmographic']['technology_stack'].get(
            tech_compatibility, 0.5
        )
        scores.append(tech_score)
        
        # Бюджетные сигналы
        budget_signal = firmographic_data.get('budget_signal', 'unknown')
        budget_score = self.scoring_model['firmographic']['budget_signals'].get(
            budget_signal, 0.4
        )
        scores.append(budget_score)
        
        return statistics.mean(scores) if scores else 0.5
    
    def _calculate_temporal_score(self, lead: Lead) -> float:
        """Расчет временной оценки (свежесть лида)"""
        
        days_old = (datetime.now() - lead.created_at).days
        
        # Свежие лиды ценнее
        if days_old <= 1:
            return 1.0
        elif days_old <= 7:
            return 0.8
        elif days_old <= 30:
            return 0.6
        elif days_old <= 90:
            return 0.4
        else:
            return 0.2
    
    def batch_score_leads(self, leads: List[Lead], 
                         additional_data: Dict[str, Dict] = None) -> List[Tuple[Lead, float]]:
        """Массовая оценка лидов"""
        
        scored_leads = []
        
        for lead in leads:
            lead_additional_data = additional_data.get(lead.id, {}) if additional_data else {}
            score = self.calculate_lead_score(lead, lead_additional_data)
            
            # Обновляем оценку в объекте лида
            lead.score = score
            
            scored_leads.append((lead, score))
        
        # Сортируем по убыванию оценки
        scored_leads.sort(key=lambda x: x[1], reverse=True)
        
        return scored_leads
    
    def get_priority_leads(self, leads: List[Lead], top_n: int = 10) -> List[Lead]:
        """Получение приоритетных лидов"""
        
        scored_leads = self.batch_score_leads(leads)
        return [lead for lead, score in scored_leads[:top_n]]

# Демонстрация системы оценки лидов
print("=== СИСТЕМА ОЦЕНКИ ЛИДОВ ===")

lead_scoring = LeadScoringEngine()

# Создаем тестовые лиды
test_leads = [
    Lead(
        id="lead_001",
        company="TechCorp",
        contact_person="Анна Технова",
        email="anna@techcorp.com",
        phone="+7 (495) 123-45-67",
        industry="technology",
        company_size=150,
        annual_revenue=5000000,
        source="webinar",
        created_at=datetime.now() - timedelta(days=2)
    ),
    Lead(
        id="lead_002",
        company="SmallBiz LLC",
        contact_person="Петр Малый",
        email="petr@smallbiz.com",
        phone=None,
        industry="retail",
        company_size=25,
        annual_revenue=800000,
        source="google_ads",
        created_at=datetime.now() - timedelta(days=15)
    ),
    Lead(
        id="lead_003",
        company="Enterprise Solutions",
        contact_person="Мария Корпоратова",
        email="maria@enterprise.com",
        phone="+7 (495) 987-65-43",
        industry="finance",
        company_size=2000,
        annual_revenue=150000000,
        source="referral",
        created_at=datetime.now() - timedelta(days=1)
    )
]

# Дополнительные данные о поведении лидов
additional_behavior_data = {
    "lead_001": {
        'behavior': {
            'email_actions': ['opened', 'clicked'],
            'website_actions': ['visited', 'pricing_page'],
            'content_actions': ['attended_webinar']
        },
        'firmographic': {
            'tech_compatibility': 'compatible',
            'budget_signal': 'budget_likely'
        }
    },
    "lead_002": {
        'behavior': {
            'email_actions': ['opened'],
            'website_actions': ['visited'],
            'content_actions': []
        },
        'firmographic': {
            'tech_compatibility': 'needs_integration',
            'budget_signal': 'budget_unknown'
        }
    },
    "lead_003": {
        'behavior': {
            'email_actions': ['opened', 'clicked', 'replied'],
            'website_actions': ['visited', 'multiple_pages', 'demo_request'],
            'content_actions': ['downloaded_whitepaper', 'requested_trial']
        },
        'firmographic': {
            'tech_compatibility': 'compatible',
            'budget_signal': 'budget_confirmed'
        }
    }
}

# Оцениваем лиды
scored_leads = lead_scoring.batch_score_leads(test_leads, additional_behavior_data)

print("Результаты оценки лидов:")
for lead, score in scored_leads:
    print(f"{lead.company}: {score:.1f} баллов")
    print(f"  Контакт: {lead.contact_person} ({lead.email})")
    print(f"  Индустрия: {lead.industry}, Размер: {lead.company_size} сотр.")
    print(f"  Источник: {lead.source}, Возраст: {(datetime.now() - lead.created_at).days} дней")
    print()

# Получаем приоритетных лидов
priority_leads = lead_scoring.get_priority_leads(test_leads, top_n=2)
print(f"Приоритетные лиды для работы:")
for lead in priority_leads:
    print(f"  🎯 {lead.company} (оценка: {lead.score:.1f})")
```

## Прогнозирование продаж

### Sales Forecasting с машинным обучением
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SalesForecastingEngine:
    """Движок прогнозирования продаж"""
    
    def __init__(self):
        self.historical_data = []
        self.forecast_models = {}
        self.seasonality_factors = {}
        
    def prepare_training_data(self, sales_data: List[Dict]) -> pd.DataFrame:
        """Подготовка данных для обучения"""
        
        df = pd.DataFrame(sales_data)
        
        # Добавляем временные признаки
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['day_of_week'] = df['date'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6])
        
        # Добавляем лаговые признаки
        df = df.sort_values('date')
        df['sales_lag_7'] = df['sales'].shift(7)    # Продажи 7 дней назад
        df['sales_lag_30'] = df['sales'].shift(30)  # 30 дней назад
        df['sales_rolling_7'] = df['sales'].rolling(window=7).mean()   # Среднее за 7 дней
        df['sales_rolling_30'] = df['sales'].rolling(window=30).mean() # Среднее за 30 дней
        
        # Добавляем внешние факторы
        df['is_holiday'] = df['date'].dt.strftime('%m-%d').isin([
            '01-01', '01-07', '02-23', '03-08', '05-01', '05-09', '06-12', '11-04', '12-31'
        ])
        
        return df
    
    def train_forecast_model(self, df: pd.DataFrame, target_column: str = 'sales') -> Dict[str, Any]:
        """Обучение модели прогнозирования"""
        
        # Простая линейная модель для демонстрации
        # В реальности использовались бы ARIMA, Prophet, LSTM и др.
        
        feature_columns = [
            'month', 'quarter', 'day_of_week', 'is_weekend', 'is_holiday',
            'sales_lag_7', 'sales_lag_30', 'sales_rolling_7', 'sales_rolling_30'
        ]
        
        # Удаляем строки с NaN (из-за лагов)
        df_clean = df.dropna()
        
        X = df_clean[feature_columns]
        y = df_clean[target_column]
        
        # Простая модель: средневзвешенная по признакам
        feature_importance = {
            'month': 0.15,
            'quarter': 0.10,
            'day_of_week': 0.05,
            'is_weekend': 0.05,
            'is_holiday': 0.10,
            'sales_lag_7': 0.20,
            'sales_lag_30': 0.15,
            'sales_rolling_7': 0.10,
            'sales_rolling_30': 0.10
        }
        
        # Вычисляем базовые статистики для предсказания
        model_params = {
            'feature_means': X.mean().to_dict(),
            'feature_stds': X.std().to_dict(),
            'target_mean': y.mean(),
            'target_std': y.std(),
            'feature_importance': feature_importance,
            'seasonal_patterns': self._extract_seasonal_patterns(df_clean)
        }
        
        # Оценка качества модели (упрощенная)
        predictions = []
        for _, row in df_clean.iterrows():
            pred = self._simple_predict(row[feature_columns].to_dict(), model_params)
            predictions.append(pred)
        
        mae = np.mean(np.abs(np.array(predictions) - y.values))
        mape = np.mean(np.abs((y.values - np.array(predictions)) / y.values)) * 100
        
        model_info = {
            'parameters': model_params,
            'training_samples': len(df_clean),
            'mae': mae,
            'mape': mape,
            'features': feature_columns
        }
        
        self.forecast_models[target_column] = model_info
        
        return model_info
    
    def _extract_seasonal_patterns(self, df: pd.DataFrame) -> Dict[str, float]:
        """Извлечение сезонных паттернов"""
        
        patterns = {}
        
        # Паттерны по месяцам
        monthly_avg = df.groupby('month')['sales'].mean()
        yearly_avg = df['sales'].mean()
        
        for month in range(1, 13):
            if month in monthly_avg.index:
                patterns[f'month_{month}_factor'] = monthly_avg[month] / yearly_avg
            else:
                patterns[f'month_{month}_factor'] = 1.0
        
        # Паттерны по дням недели
        daily_avg = df.groupby('day_of_week')['sales'].mean()
        
        for day in range(7):
            if day in daily_avg.index:
                patterns[f'day_{day}_factor'] = daily_avg[day] / yearly_avg
            else:
                patterns[f'day_{day}_factor'] = 1.0
        
        return patterns
    
    def _simple_predict(self, features: Dict[str, Any], 
                       model_params: Dict[str, Any]) -> float:
        """Простое предсказание"""
        
        base_prediction = model_params['target_mean']
        
        # Применяем сезонные факторы
        seasonal_patterns = model_params['seasonal_patterns']
        month = features.get('month', 1)
        day_of_week = features.get('day_of_week', 0)
        
        seasonal_factor = seasonal_patterns.get(f'month_{month}_factor', 1.0) * \
                         seasonal_patterns.get(f'day_{day_of_week}_factor', 1.0)
        
        # Применяем лаговые значения
        lag_7 = features.get('sales_lag_7', base_prediction)
        lag_30 = features.get('sales_lag_30', base_prediction)
        
        # Взвешенное предсказание
        prediction = (
            base_prediction * 0.3 +
            lag_7 * 0.3 +
            lag_30 * 0.2 +
            base_prediction * seasonal_factor * 0.2
        )
        
        # Корректировки на выходные и праздники
        if features.get('is_weekend', False):
            prediction *= 0.7  # Снижение на выходных
        
        if features.get('is_holiday', False):
            prediction *= 0.3  # Значительное снижение в праздники
        
        return max(0, prediction)
    
    def forecast_sales(self, periods: int, base_date: datetime = None) -> List[Dict]:
        """Прогнозирование продаж на N периодов вперед"""
        
        if 'sales' not in self.forecast_models:
            raise ValueError("Модель не обучена. Сначала вызовите train_forecast_model()")
        
        if base_date is None:
            base_date = datetime.now()
        
        model = self.forecast_models['sales']
        forecasts = []
        
        # Получаем последние известные значения для лагов
        last_known_sales = model['parameters']['target_mean']  # Упрощение
        
        for i in range(periods):
            forecast_date = base_date + timedelta(days=i)
            
            # Создаем признаки для предсказания
            features = {
                'month': forecast_date.month,
                'quarter': (forecast_date.month - 1) // 3 + 1,
                'day_of_week': forecast_date.weekday(),
                'is_weekend': forecast_date.weekday() >= 5,
                'is_holiday': forecast_date.strftime('%m-%d') in [
                    '01-01', '01-07', '02-23', '03-08', '05-01', '05-09', 
                    '06-12', '11-04', '12-31'
                ],
                'sales_lag_7': last_known_sales,  # Упрощение: используем базовое значение
                'sales_lag_30': last_known_sales,
                'sales_rolling_7': last_known_sales,
                'sales_rolling_30': last_known_sales
            }
            
            # Делаем предсказание
            predicted_sales = self._simple_predict(features, model['parameters'])
            
            # Добавляем доверительный интервал
            confidence_interval = predicted_sales * 0.2  # ±20%
            
            forecast = {
                'date': forecast_date,
                'predicted_sales': predicted_sales,
                'lower_bound': predicted_sales - confidence_interval,
                'upper_bound': predicted_sales + confidence_interval,
                'confidence': 0.8  # 80% уверенность
            }
            
            forecasts.append(forecast)
        
        return forecasts
    
    def analyze_forecast_accuracy(self, actual_sales: List[Dict], 
                                forecasts: List[Dict]) -> Dict[str, float]:
        """Анализ точности прогнозов"""
        
        if len(actual_sales) != len(forecasts):
            raise ValueError("Количество актуальных продаж должно совпадать с прогнозами")
        
        errors = []
        percentage_errors = []
        
        for actual, forecast in zip(actual_sales, forecasts):
            actual_value = actual['sales']
            predicted_value = forecast['predicted_sales']
            
            error = abs(actual_value - predicted_value)
            percentage_error = (error / actual_value) * 100 if actual_value > 0 else 0
            
            errors.append(error)
            percentage_errors.append(percentage_error)
        
        return {
            'mae': statistics.mean(errors),  # Mean Absolute Error
            'mape': statistics.mean(percentage_errors),  # Mean Absolute Percentage Error
            'rmse': np.sqrt(np.mean(np.array(errors) ** 2)),  # Root Mean Square Error
            'accuracy': max(0, 100 - statistics.mean(percentage_errors))  # Точность в процентах
        }

# Создаем тестовые исторические данные продаж
historical_sales = []
base_sales = 100000

for i in range(90):  # 90 дней истории
    date = datetime.now() - timedelta(days=90-i)
    
    # Базовые продажи с трендом роста
    daily_sales = base_sales * (1 + i * 0.01)  # Рост 1% в день
    
    # Сезонные колебания
    seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365)
    daily_sales *= seasonal_factor
    
    # Случайные колебания
    daily_sales *= np.random.uniform(0.8, 1.2)
    
    # Снижение в выходные
    if date.weekday() >= 5:
        daily_sales *= 0.7
    
    historical_sales.append({
        'date': date.strftime('%Y-%m-%d'),
        'sales': int(daily_sales)
    })

# Обучаем модель прогнозирования
forecasting_engine = SalesForecastingEngine()

# Подготавливаем данные
df = forecasting_engine.prepare_training_data(historical_sales)
print(f"Подготовлено {len(df)} записей для обучения")

# Обучаем модель
model_info = forecasting_engine.train_forecast_model(df)
print(f"Модель обучена. MAE: {model_info['mae']:.0f}, MAPE: {model_info['mape']:.1f}%")

# Делаем прогноз на 7 дней
forecast_results = forecasting_engine.forecast_sales(7)

print(f"\n=== ПРОГНОЗ ПРОДАЖ НА 7 ДНЕЙ ===")
for forecast in forecast_results:
    date_str = forecast['date'].strftime('%Y-%m-%d (%a)')
    sales = forecast['predicted_sales']
    lower = forecast['lower_bound'] 
    upper = forecast['upper_bound']
    
    print(f"{date_str}: {sales:,.0f} руб (диапазон: {lower:,.0f} - {upper:,.0f})")

total_forecast = sum(f['predicted_sales'] for f in forecast_results)
print(f"\nОбщий прогноз за неделю: {total_forecast:,.0f} руб")
```

### Персонализация предложений
```python
class PersonalizationEngine:
    """Движок персонализации предложений"""
    
    def __init__(self):
        self.customer_profiles = {}
        self.product_catalog = self._initialize_product_catalog()
        self.recommendation_rules = self._initialize_recommendation_rules()
    
    def _initialize_product_catalog(self) -> Dict[str, Dict]:
        """Инициализация каталога продуктов"""
        return {
            'crm_basic': {
                'name': 'CRM Базовый',
                'price': 50000,
                'target_segments': ['smb', 'startup'],
                'features': ['контакты', 'сделки', 'отчеты'],
                'implementation_time': 30,  # дней
                'roi_expectation': 1.5
            },
            'crm_professional': {
                'name': 'CRM Профессиональный',
                'price': 150000,
                'target_segments': ['smb', 'enterprise'],
                'features': ['контакты', 'сделки', 'отчеты', 'автоматизация', 'интеграции'],
                'implementation_time': 60,
                'roi_expectation': 2.0
            },
            'crm_enterprise': {
                'name': 'CRM Корпоративный',
                'price': 500000,
                'target_segments': ['enterprise'],
                'features': ['все функции', 'кастомизация', 'dedicated поддержка'],
                'implementation_time': 120,
                'roi_expectation': 3.0
            },
            'analytics_addon': {
                'name': 'Модуль Аналитики',
                'price': 75000,
                'target_segments': ['smb', 'enterprise'],
                'features': ['advanced отчеты', 'BI панели', 'предиктивная аналитика'],
                'implementation_time': 45,
                'roi_expectation': 2.5
            }
        }
    
    def _initialize_recommendation_rules(self) -> Dict[str, List[Dict]]:
        """Инициализация правил рекомендаций"""
        return {
            'segment_based': [
                {
                    'condition': {'segment': 'startup'},
                    'recommendations': ['crm_basic'],
                    'messaging': 'Быстрый старт с минимальными вложениями'
                },
                {
                    'condition': {'segment': 'smb'},
                    'recommendations': ['crm_professional', 'analytics_addon'],
                    'messaging': 'Масштабируемое решение для растущего бизнеса'
                },
                {
                    'condition': {'segment': 'enterprise'},
                    'recommendations': ['crm_enterprise', 'analytics_addon'],
                    'messaging': 'Корпоративное решение с полной кастомизацией'
                }
            ],
            'behavior_based': [
                {
                    'condition': {'visited_pricing': True},
                    'recommendations': ['discount_offer'],
                    'messaging': 'Специальное предложение для вас'
                },
                {
                    'condition': {'downloaded_whitepaper': True},
                    'recommendations': ['demo_booking'],
                    'messaging': 'Увидьте решение в действии'
                },
                {
                    'condition': {'multiple_visits': True},
                    'recommendations': ['personal_consultation'],
                    'messaging': 'Персональная консультация эксперта'
                }
            ],
            'industry_based': [
                {
                    'condition': {'industry': 'technology'},
                    'recommendations': ['crm_professional', 'analytics_addon'],
                    'messaging': 'Технологичное решение для IT-компаний'
                },
                {
                    'condition': {'industry': 'finance'},
                    'recommendations': ['crm_enterprise'],
                    'messaging': 'Безопасное решение с соблюдением регуляций'
                }
            ]
        }
    
    def create_customer_profile(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание профиля клиента"""
        
        profile = {
            'customer_id': customer_data['id'],
            'segment': self._determine_segment(customer_data),
            'preferences': self._analyze_preferences(customer_data),
            'behavioral_signals': self._extract_behavioral_signals(customer_data),
            'purchase_power': self._estimate_purchase_power(customer_data),
            'decision_timeline': self._estimate_decision_timeline(customer_data),
            'pain_points': self._identify_pain_points(customer_data)
        }
        
        self.customer_profiles[customer_data['id']] = profile
        
        return profile
    
    def _determine_segment(self, customer_data: Dict[str, Any]) -> CustomerSegment:
        """Определение сегмента клиента"""
        
        company_size = customer_data.get('company_size', 0)
        annual_revenue = customer_data.get('annual_revenue', 0)
        
        if company_size > 1000 or annual_revenue > 100000000:
            return CustomerSegment.ENTERPRISE
        elif company_size > 50 or annual_revenue > 5000000:
            return CustomerSegment.SMB
        elif annual_revenue > 0:
            return CustomerSegment.STARTUP
        else:
            return CustomerSegment.INDIVIDUAL
    
    def _analyze_preferences(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ предпочтений клиента"""
        
        preferences = {
            'price_sensitivity': 'medium',
            'feature_priority': 'standard',
            'implementation_urgency': 'medium',
            'support_level': 'standard'
        }
        
        # Анализ на основе поведения
        if customer_data.get('visited_pricing_multiple_times', False):
            preferences['price_sensitivity'] = 'high'
        
        if customer_data.get('downloaded_technical_docs', False):
            preferences['feature_priority'] = 'advanced'
        
        if customer_data.get('requested_urgent_demo', False):
            preferences['implementation_urgency'] = 'high'
        
        return preferences
    
    def _extract_behavioral_signals(self, customer_data: Dict[str, Any]) -> List[str]:
        """Извлечение поведенческих сигналов"""
        
        signals = []
        
        interactions = customer_data.get('interactions', [])
        
        for interaction in interactions:
            interaction_type = interaction.get('type', '')
            
            if interaction_type == 'email_opened':
                signals.append('email_engagement')
            elif interaction_type == 'website_visit':
                if 'pricing' in interaction.get('page', ''):
                    signals.append('price_research')
                elif 'demo' in interaction.get('page', ''):
                    signals.append('demo_interest')
            elif interaction_type == 'content_download':
                signals.append('information_seeking')
        
        return list(set(signals))  # Уникальные сигналы
    
    def _estimate_purchase_power(self, customer_data: Dict[str, Any]) -> str:
        """Оценка покупательной способности"""
        
        annual_revenue = customer_data.get('annual_revenue', 0)
        company_size = customer_data.get('company_size', 0)
        
        if annual_revenue > 50000000 or company_size > 500:
            return 'high'
        elif annual_revenue > 5000000 or company_size > 50:
            return 'medium'
        else:
            return 'low'
    
    def _estimate_decision_timeline(self, customer_data: Dict[str, Any]) -> str:
        """Оценка временных рамок принятия решения"""
        
        # Анализ поведенческих сигналов
        signals = customer_data.get('behavioral_signals', [])
        
        urgent_signals = ['demo_request', 'pricing_inquiry', 'competitor_comparison']
        moderate_signals = ['whitepaper_download', 'webinar_attendance']
        
        if any(signal in signals for signal in urgent_signals):
            return 'short'  # 1-4 недели
        elif any(signal in signals for signal in moderate_signals):
            return 'medium'  # 1-3 месяца
        else:
            return 'long'   # 3+ месяца
    
    def _identify_pain_points(self, customer_data: Dict[str, Any]) -> List[str]:
        """Выявление болевых точек клиента"""
        
        pain_points = []
        
        # Анализ индустрии
        industry = customer_data.get('industry', '').lower()
        
        if industry == 'technology':
            pain_points.extend(['быстрый рост', 'масштабирование', 'интеграции'])
        elif industry == 'finance':
            pain_points.extend(['compliance', 'безопасность', 'отчетность'])
        elif industry == 'retail':
            pain_points.extend(['сезонность', 'inventory', 'customer experience'])
        
        # Анализ размера компании
        company_size = customer_data.get('company_size', 0)
        
        if company_size < 50:
            pain_points.extend(['ограниченный бюджет', 'простота использования'])
        elif company_size > 500:
            pain_points.extend(['сложная структура', 'кастомизация', 'интеграция'])
        
        return pain_points
    
    def generate_personalized_proposal(self, customer_id: str) -> Dict[str, Any]:
        """Генерация персонализированного предложения"""
        
        if customer_id not in self.customer_profiles:
            raise ValueError(f"Профиль клиента {customer_id} не найден")
        
        profile = self.customer_profiles[customer_id]
        
        # Выбираем подходящие продукты
        recommended_products = self._select_products_for_profile(profile)
        
        # Создаем персонализированное сообщение
        messaging = self._create_personalized_messaging(profile, recommended_products)
        
        # Рассчитываем ценовое предложение
        pricing = self._calculate_personalized_pricing(profile, recommended_products)
        
        # Определяем следующие шаги
        next_steps = self._suggest_next_steps(profile)
        
        proposal = {
            'customer_id': customer_id,
            'recommended_products': recommended_products,
            'personalized_messaging': messaging,
            'pricing_proposal': pricing,
            'next_steps': next_steps,
            'proposal_valid_until': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
            'expected_close_probability': self._estimate_close_probability(profile)
        }
        
        return proposal
    
    def _select_products_for_profile(self, profile: Dict[str, Any]) -> List[str]:
        """Выбор продуктов на основе профиля"""
        
        segment = profile['segment']
        purchase_power = profile['purchase_power']
        preferences = profile['preferences']
        
        recommendations = []
        
        # Базовая рекомендация по сегменту
        if segment == CustomerSegment.STARTUP:
            recommendations.append('crm_basic')
        elif segment == CustomerSegment.SMB:
            recommendations.append('crm_professional')
            if purchase_power in ['medium', 'high']:
                recommendations.append('analytics_addon')
        elif segment == CustomerSegment.ENTERPRISE:
            recommendations.append('crm_enterprise')
            recommendations.append('analytics_addon')
        
        # Корректировка по предпочтениям
        if preferences['feature_priority'] == 'advanced' and 'analytics_addon' not in recommendations:
            recommendations.append('analytics_addon')
        
        return recommendations
    
    def _create_personalized_messaging(self, profile: Dict[str, Any], 
                                     products: List[str]) -> Dict[str, str]:
        """Создание персонализированного сообщения"""
        
        pain_points = profile['pain_points']
        segment = profile['segment']
        
        # Основное сообщение
        if segment == CustomerSegment.STARTUP:
            main_message = "Быстрое решение для растущей компании"
        elif segment == CustomerSegment.SMB:
            main_message = "Масштабируемая платформа для среднего бизнеса"
        else:
            main_message = "Корпоративное решение уровня enterprise"
        
        # Адресация болевых точек
        pain_point_messages = []
        for pain in pain_points[:3]:  # Топ-3 болевые точки
            if pain == 'быстрый рост':
                pain_point_messages.append("Поддержит рост без замены системы")
            elif pain == 'ограниченный бюджет':
                pain_point_messages.append("Доступная цена с быстрой окупаемостью")
            elif pain == 'интеграции':
                pain_point_messages.append("Легко интегрируется с существующими системами")
        
        # Призыв к действию
        if profile['decision_timeline'] == 'short':
            cta = "Запишитесь на демо уже сегодня!"
        elif profile['decision_timeline'] == 'medium':
            cta = "Получите персональную презентацию решения"
        else:
            cta = "Изучите возможности в удобном темпе"
        
        return {
            'main_message': main_message,
            'pain_point_address': ' | '.join(pain_point_messages),
            'call_to_action': cta,
            'value_proposition': self._create_value_proposition(products, profile)
        }
    
    def _create_value_proposition(self, products: List[str], 
                                profile: Dict[str, Any]) -> str:
        """Создание ценностного предложения"""
        
        # Собираем преимущества выбранных продуктов
        benefits = []
        total_roi = 0
        
        for product_id in products:
            product = self.product_catalog[product_id]
            total_roi += product['roi_expectation']
            
            if product_id == 'crm_basic':
                benefits.append("быстрое внедрение")
            elif product_id == 'crm_professional':
                benefits.append("автоматизация процессов")
            elif product_id == 'crm_enterprise':
                benefits.append("полная кастомизация")
            elif product_id == 'analytics_addon':
                benefits.append("data-driven решения")
        
        avg_roi = total_roi / len(products) if products else 1.0
        
        return f"Получите {', '.join(benefits)} с ROI {avg_roi:.1f}x за первый год"
    
    def _calculate_personalized_pricing(self, profile: Dict[str, Any], 
                                      products: List[str]) -> Dict[str, Any]:
        """Расчет персонализированного ценового предложения"""
        
        base_price = sum(self.product_catalog[p]['price'] for p in products)
        
        # Скидки на основе профиля
        discount_factors = []
        
        # Скидка по сегменту
        if profile['segment'] == CustomerSegment.STARTUP:
            discount_factors.append(('startup_discount', 0.2))  # 20% скидка
        elif profile['segment'] == CustomerSegment.ENTERPRISE:
            if len(products) > 1:
                discount_factors.append(('bundle_discount', 0.15))  # 15% за комплект
        
        # Скидка за быстрое принятие решения
        if profile['decision_timeline'] == 'short':
            discount_factors.append(('quick_decision', 0.1))
        
        # Скидка для чувствительных к цене клиентов
        if profile['preferences']['price_sensitivity'] == 'high':
            discount_factors.append(('price_sensitive', 0.1))
        
        # Применяем скидки
        total_discount = sum(factor[1] for factor in discount_factors)
        total_discount = min(total_discount, 0.4)  # Максимум 40% скидка
        
        final_price = base_price * (1 - total_discount)
        
        return {
            'base_price': base_price,
            'discount_factors': discount_factors,
            'total_discount_percent': total_discount * 100,
            'final_price': final_price,
            'savings': base_price - final_price,
            'payment_terms': self._suggest_payment_terms(profile)
        }
    
    def _suggest_payment_terms(self, profile: Dict[str, Any]) -> str:
        """Предложение условий оплаты"""
        
        purchase_power = profile['purchase_power']
        segment = profile['segment']
        
        if purchase_power == 'low' or segment == CustomerSegment.STARTUP:
            return "Помесячная оплата или отсрочка первого платежа"
        elif purchase_power == 'high':
            return "Скидка за годовую предоплату"
        else:
            return "Гибкие условия оплаты: месячно или квартально"
    
    def _suggest_next_steps(self, profile: Dict[str, Any]) -> List[str]:
        """Предложение следующих шагов"""
        
        timeline = profile['decision_timeline']
        behavioral_signals = profile['behavioral_signals']
        
        if timeline == 'short':
            return [
                "Записаться на демо на этой неделе",
                "Подготовить техническое задание",
                "Согласовать бюджет с руководством"
            ]
        elif timeline == 'medium':
            return [
                "Изучить детальную презентацию решения",
                "Протестировать trial версию",
                "Провести оценку ROI",
                "Запланировать встречу с командой"
            ]
        else:
            return [
                "Подписаться на образовательные материалы",
                "Посетить вебинар о лучших практиках",
                "Получить консультацию эксперта"
            ]
    
    def _estimate_close_probability(self, profile: Dict[str, Any]) -> float:
        """Оценка вероятности закрытия сделки"""
        
        base_probability = 0.2  # Базовая вероятность 20%
        
        # Факторы увеличения вероятности
        if profile['decision_timeline'] == 'short':
            base_probability += 0.3
        elif profile['decision_timeline'] == 'medium':
            base_probability += 0.15
        
        if profile['purchase_power'] == 'high':
            base_probability += 0.2
        elif profile['purchase_power'] == 'medium':
            base_probability += 0.1
        
        if 'demo_interest' in profile['behavioral_signals']:
            base_probability += 0.25
        
        if 'price_research' in profile['behavioral_signals']:
            base_probability += 0.15
        
        return min(base_probability, 0.95)  # Максимум 95%

# Демонстрация персонализации
personalization = PersonalizationEngine()

# Создаем тестового клиента
test_customer = {
    'id': 'cust_001',
    'company': 'TechStartup Inc',
    'industry': 'technology',
    'company_size': 75,
    'annual_revenue': 8000000,
    'interactions': [
        {'type': 'email_opened', 'timestamp': datetime.now() - timedelta(days=2)},
        {'type': 'website_visit', 'page': 'pricing', 'timestamp': datetime.now() - timedelta(days=1)},
        {'type': 'content_download', 'item': 'crm_guide', 'timestamp': datetime.now()}
    ],
    'visited_pricing_multiple_times': True,
    'downloaded_technical_docs': True,
    'requested_urgent_demo': False
}

# Создаем профиль клиента
customer_profile = personalization.create_customer_profile(test_customer)

print("=== ПРОФИЛЬ КЛИЕНТА ===")
print(f"Сегмент: {customer_profile['segment'].value}")
print(f"Покупательная способность: {customer_profile['purchase_power']}")
print(f"Временные рамки решения: {customer_profile['decision_timeline']}")
print(f"Поведенческие сигналы: {customer_profile['behavioral_signals']}")
print(f"Болевые точки: {customer_profile['pain_points']}")

# Генерируем персонализированное предложение
proposal = personalization.generate_personalized_proposal('cust_001')

print(f"\n=== ПЕРСОНАЛИЗИРОВАННОЕ ПРЕДЛОЖЕНИЕ ===")
print(f"Рекомендуемые продукты: {proposal['recommended_products']}")
print(f"Основное сообщение: {proposal['personalized_messaging']['main_message']}")
print(f"Адресация проблем: {proposal['personalized_messaging']['pain_point_address']}")
print(f"Ценностное предложение: {proposal['personalized_messaging']['value_proposition']}")

print(f"\n=== ЦЕНОВОЕ ПРЕДЛОЖЕНИЕ ===")
pricing = proposal['pricing_proposal']
print(f"Базовая цена: {pricing['base_price']:,} руб")
print(f"Скидка: {pricing['total_discount_percent']:.1f}%")
print(f"Итоговая цена: {pricing['final_price']:,} руб")
print(f"Экономия: {pricing['savings']:,} руб")
print(f"Условия оплаты: {pricing['payment_terms']}")

print(f"\n=== СЛЕДУЮЩИЕ ШАГИ ===")
for step in proposal['next_steps']:
    print(f"  📋 {step}")

print(f"\nВероятность закрытия: {proposal['expected_close_probability']:.1%}")
print(f"Предложение действует до: {proposal['proposal_valid_until']}")
```

## Автоматизация продажных процессов

### CRM интеграция и автоматизация
```python
class SalesCRMIntegration:
    """Интеграция с CRM системами"""
    
    def __init__(self, crm_type: str = "mock"):
        self.crm_type = crm_type
        self.automation_rules = []
        self.lead_routing_rules = {}
        self.task_templates = {}
        
    def setup_automation_rules(self):
        """Настройка правил автоматизации"""
        
        self.automation_rules = [
            {
                'name': 'hot_lead_assignment',
                'trigger': {'lead_score': {'>=': 80}},
                'actions': [
                    {'type': 'assign_to_sales_rep', 'priority': 'high'},
                    {'type': 'send_notification', 'urgency': 'immediate'},
                    {'type': 'schedule_follow_up', 'delay_hours': 2}
                ]
            },
            {
                'name': 'demo_request_workflow',
                'trigger': {'behavior': 'demo_requested'},
                'actions': [
                    {'type': 'create_calendar_event', 'within_hours': 24},
                    {'type': 'send_demo_preparation_email'},
                    {'type': 'notify_technical_team'}
                ]
            },
            {
                'name': 'long_inactive_lead',
                'trigger': {'days_inactive': {'>=': 30}},
                'actions': [
                    {'type': 'send_reactivation_email'},
                    {'type': 'update_lead_status', 'status': 'cold'},
                    {'type': 'schedule_quarterly_check'}
                ]
            },
            {
                'name': 'price_objection_handler',
                'trigger': {'objection_type': 'price'},
                'actions': [
                    {'type': 'send_roi_calculator'},
                    {'type': 'schedule_budget_discussion'},
                    {'type': 'prepare_discount_options'}
                ]
            }
        ]
        
        self.lead_routing_rules = {
            'enterprise': 'senior_sales_rep',
            'smb': 'standard_sales_rep', 
            'startup': 'inside_sales_rep',
            'inbound_high_score': 'senior_sales_rep',
            'outbound': 'business_development_rep'
        }
    
    def process_new_lead(self, lead: Lead, behavior_data: Dict = None) -> Dict[str, Any]:
        """Обработка нового лида"""
        
        processing_results = {
            'lead_id': lead.id,
            'actions_taken': [],
            'assignments': [],
            'scheduled_tasks': [],
            'notifications_sent': []
        }
        
        # Оценка лида
        lead_scoring = LeadScoringEngine()
        lead_score = lead_scoring.calculate_lead_score(lead, behavior_data or {})
        lead.score = lead_score
        
        # Сегментация
        if lead.company_size > 1000:
            lead.segment = CustomerSegment.ENTERPRISE
        elif lead.company_size > 50:
            lead.segment = CustomerSegment.SMB
        else:
            lead.segment = CustomerSegment.STARTUP
        
        # Маршрутизация лида
        assigned_rep = self._route_lead(lead)
        if assigned_rep:
            processing_results['assignments'].append({
                'sales_rep': assigned_rep,
                'lead_id': lead.id,
                'priority': 'high' if lead_score >= 80 else 'normal'
            })
        
        # Применение правил автоматизации
        for rule in self.automation_rules:
            if self._check_rule_trigger(rule['trigger'], lead, behavior_data):
                executed_actions = self._execute_rule_actions(rule['actions'], lead)
                processing_results['actions_taken'].extend(executed_actions)
        
        # Создание первоначальных задач
        initial_tasks = self._create_initial_tasks(lead)
        processing_results['scheduled_tasks'].extend(initial_tasks)
        
        return processing_results
    
    def _route_lead(self, lead: Lead) -> Optional[str]:
        """Маршрутизация лида к менеджеру"""
        
        # Определяем тип лида
        if lead.segment == CustomerSegment.ENTERPRISE:
            return self.lead_routing_rules['enterprise']
        elif lead.segment == CustomerSegment.SMB:
            return self.lead_routing_rules['smb']
        elif lead.segment == CustomerSegment.STARTUP:
            return self.lead_routing_rules['startup']
        
        # Дополнительные правила
        if lead.score and lead.score >= 80:
            return self.lead_routing_rules['inbound_high_score']
        
        if lead.source in ['cold_email', 'linkedin_outreach']:
            return self.lead_routing_rules['outbound']
        
        return self.lead_routing_rules['smb']  # По умолчанию
    
    def _check_rule_trigger(self, trigger: Dict, lead: Lead, 
                          behavior_data: Dict = None) -> bool:
        """Проверка срабатывания правила"""
        
        for condition, criteria in trigger.items():
            if condition == 'lead_score':
                if not lead.score:
                    return False
                
                for operator, value in criteria.items():
                    if operator == '>=' and lead.score < value:
                        return False
                    elif operator == '<=' and lead.score > value:
                        return False
                    elif operator == '==' and lead.score != value:
                        return False
            
            elif condition == 'behavior':
                if not behavior_data:
                    return False
                
                required_behavior = criteria
                user_behaviors = behavior_data.get('recent_behaviors', [])
                
                if required_behavior not in user_behaviors:
                    return False
            
            elif condition == 'days_inactive':
                days_inactive = (datetime.now() - lead.created_at).days
                
                for operator, value in criteria.items():
                    if operator == '>=' and days_inactive < value:
                        return False
        
        return True
    
    def _execute_rule_actions(self, actions: List[Dict], lead: Lead) -> List[str]:
        """Выполнение действий правила"""
        
        executed_actions = []
        
        for action in actions:
            action_type = action['type']
            
            if action_type == 'assign_to_sales_rep':
                # Логика назначения менеджера
                executed_actions.append(f"Назначен менеджер для {lead.company}")
                
            elif action_type == 'send_notification':
                urgency = action.get('urgency', 'normal')
                executed_actions.append(f"Отправлено уведомление ({urgency})")
                
            elif action_type == 'schedule_follow_up':
                delay = action.get('delay_hours', 24)
                follow_up_date = datetime.now() + timedelta(hours=delay)
                executed_actions.append(f"Запланирован follow-up на {follow_up_date.strftime('%Y-%m-%d %H:%M')}")
                
            elif action_type == 'send_demo_preparation_email':
                executed_actions.append("Отправлен email с подготовкой к демо")
                
            elif action_type == 'create_calendar_event':
                within_hours = action.get('within_hours', 48)
                executed_actions.append(f"Создано событие в календаре (в течение {within_hours}ч)")
                
            elif action_type == 'send_reactivation_email':
                executed_actions.append("Отправлен email реактивации")
                
            elif action_type == 'send_roi_calculator':
                executed_actions.append("Отправлен ROI калькулятор")
        
        return executed_actions
    
    def _create_initial_tasks(self, lead: Lead) -> List[Dict]:
        """Создание первоначальных задач"""
        
        tasks = []
        
        # Базовые задачи для всех лидов
        tasks.append({
            'title': f'Первичный контакт с {lead.company}',
            'description': f'Связаться с {lead.contact_person} для квалификации',
            'due_date': datetime.now() + timedelta(hours=24),
            'priority': 'high' if lead.score and lead.score >= 70 else 'medium',
            'type': 'outreach'
        })
        
        # Специфичные задачи по сегментам
        if lead.segment == CustomerSegment.ENTERPRISE:
            tasks.append({
                'title': 'Исследование компании',
                'description': f'Изучить структуру и потребности {lead.company}',
                'due_date': datetime.now() + timedelta(hours=48),
                'priority': 'medium',
                'type': 'research'
            })
        
        if lead.source in ['webinar', 'whitepaper']:
            tasks.append({
                'title': 'Отправка релевантного контента',
                'description': f'Послать материалы по теме интереса',
                'due_date': datetime.now() + timedelta(hours=12),
                'priority': 'medium',
                'type': 'nurturing'
            })
        
        return tasks

# Демонстрация CRM автоматизации
crm_integration = SalesCRMIntegration()
crm_integration.setup_automation_rules()

# Создаем новый лид с поведенческими данными
new_lead = Lead(
    id="lead_004",
    company="FastGrow Corp",
    contact_person="Александр Растущий",
    email="alex@fastgrow.com",
    phone="+7 (495) 555-77-88",
    industry="technology",
    company_size=120,
    annual_revenue=12000000,
    source="webinar",
    created_at=datetime.now()
)

behavior_data = {
    'recent_behaviors': ['demo_requested'],
    'email_actions': ['opened', 'clicked'],
    'website_actions': ['pricing_page', 'demo_request']
}

# Обрабатываем нового лида
processing_result = crm_integration.process_new_lead(new_lead, behavior_data)

print("=== ОБРАБОТКА НОВОГО ЛИДА ===")
print(f"Лид: {new_lead.company}")
print(f"Оценка: {new_lead.score:.1f} баллов")
print(f"Сегмент: {new_lead.segment.value}")

print(f"\nНазначения:")
for assignment in processing_result['assignments']:
    print(f"  👤 {assignment['sales_rep']} (приоритет: {assignment['priority']})")

print(f"\nВыполненные действия:")
for action in processing_result['actions_taken']:
    print(f"  ⚡ {action}")

print(f"\nЗапланированные задачи:")
for task in processing_result['scheduled_tasks']:
    print(f"  📅 {task['title']}")
    print(f"      Срок: {task['due_date'].strftime('%Y-%m-%d %H:%M')}")
    print(f"      Приоритет: {task['priority']}")
```

## Анализ эффективности продаж

### Sales Analytics и KPI мониторинг
```python
class SalesAnalytics:
    """Аналитика продаж"""
    
    def __init__(self):
        self.kpi_definitions = {
            'conversion_rate': 'Процент лидов, превратившихся в клиентов',
            'average_deal_size': 'Средний размер сделки',
            'sales_cycle_length': 'Средняя длительность цикла продаж',
            'win_rate': 'Процент выигранных сделок',
            'pipeline_velocity': 'Скорость движения по воронке',
            'customer_acquisition_cost': 'Стоимость привлечения клиента',
            'customer_lifetime_value': 'Жизненная ценность клиента'
        }
        
        self.benchmarks = {
            'technology_industry': {
                'conversion_rate': 0.03,    # 3%
                'win_rate': 0.25,           # 25%
                'avg_deal_size': 250000,    # 250k руб
                'sales_cycle_days': 90,     # 90 дней
                'cac': 15000,               # 15k руб
                'clv': 500000               # 500k руб
            }
        }
    
    def calculate_sales_kpis(self, sales_data: List[Dict], 
                           period_days: int = 30) -> Dict[str, Any]:
        """Расчет KPI продаж"""
        
        cutoff_date = datetime.now() - timedelta(days=period_days)
        
        # Фильтруем данные по периоду
        period_data = [d for d in sales_data 
                      if datetime.fromisoformat(d['date']) >= cutoff_date]
        
        if not period_data:
            return {'error': 'Нет данных за указанный период'}
        
        kpis = {}
        
        # Конверсия лидов
        total_leads = len([d for d in period_data if d.get('stage') == 'lead'])
        total_customers = len([d for d in period_data if d.get('stage') == 'customer'])
        
        kpis['conversion_rate'] = total_customers / max(total_leads, 1)
        
        # Средний размер сделки
        closed_deals = [d for d in period_data if d.get('status') == 'closed_won']
        if closed_deals:
            kpis['average_deal_size'] = statistics.mean([d['amount'] for d in closed_deals])
        else:
            kpis['average_deal_size'] = 0
        
        # Win rate
        all_closed = [d for d in period_data if d.get('status', '').startswith('closed_')]
        if all_closed:
            won_deals = [d for d in all_closed if d['status'] == 'closed_won']
            kpis['win_rate'] = len(won_deals) / len(all_closed)
        else:
            kpis['win_rate'] = 0
        
        # Длительность цикла продаж
        completed_cycles = []
        for deal in closed_deals:
            if 'created_date' in deal and 'closed_date' in deal:
                created = datetime.fromisoformat(deal['created_date'])
                closed = datetime.fromisoformat(deal['closed_date'])
                cycle_length = (closed - created).days
                completed_cycles.append(cycle_length)
        
        if completed_cycles:
            kpis['sales_cycle_length'] = statistics.mean(completed_cycles)
        else:
            kpis['sales_cycle_length'] = 0
        
        # Скорость воронки (Pipeline Velocity)
        if kpis['average_deal_size'] > 0 and kpis['sales_cycle_length'] > 0:
            kpis['pipeline_velocity'] = (
                kpis['average_deal_size'] * kpis['win_rate'] / 
                max(kpis['sales_cycle_length'], 1)
            )
        else:
            kpis['pipeline_velocity'] = 0
        
        # Стоимость привлечения клиента (упрощенный расчет)
        marketing_spend = sum(d.get('marketing_cost', 0) for d in period_data)
        if total_customers > 0:
            kpis['customer_acquisition_cost'] = marketing_spend / total_customers
        else:
            kpis['customer_acquisition_cost'] = 0
        
        return kpis
    
    def compare_with_benchmarks(self, kpis: Dict[str, float], 
                              industry: str = 'technology_industry') -> Dict[str, Any]:
        """Сравнение с отраслевыми бенчмарками"""
        
        if industry not in self.benchmarks:
            return {'error': f'Бенчмарки для индустрии {industry} не найдены'}
        
        benchmarks = self.benchmarks[industry]
        comparison = {}
        
        for kpi_name, kpi_value in kpis.items():
            if kpi_name in benchmarks:
                benchmark_value = benchmarks[kpi_name]
                
                if kpi_name in ['conversion_rate', 'win_rate']:
                    # Для ставок: выше = лучше
                    performance_ratio = kpi_value / benchmark_value if benchmark_value > 0 else 0
                elif kpi_name in ['sales_cycle_days', 'cac']:
                    # Для временных и стоимостных метрик: ниже = лучше
                    performance_ratio = benchmark_value / kpi_value if kpi_value > 0 else 0
                else:
                    # Для размера сделок и CLV: выше = лучше
                    performance_ratio = kpi_value / benchmark_value if benchmark_value > 0 else 0
                
                if performance_ratio >= 1.2:
                    performance_status = 'excellent'
                elif performance_ratio >= 1.0:
                    performance_status = 'good'
                elif performance_ratio >= 0.8:
                    performance_status = 'acceptable'
                else:
                    performance_status = 'needs_improvement'
                
                comparison[kpi_name] = {
                    'current_value': kpi_value,
                    'benchmark_value': benchmark_value,
                    'performance_ratio': performance_ratio,
                    'status': performance_status,
                    'gap': kpi_value - benchmark_value
                }
        
        return comparison
    
    def generate_sales_insights(self, kpis: Dict[str, float], 
                              comparison: Dict[str, Any]) -> List[str]:
        """Генерация инсайтов по продажам"""
        
        insights = []
        
        # Анализ конверсии
        if 'conversion_rate' in comparison:
            conv_data = comparison['conversion_rate']
            if conv_data['status'] == 'excellent':
                insights.append(f"🎯 Отличная конверсия ({conv_data['current_value']:.1%}) - в {conv_data['performance_ratio']:.1f}x выше среднего")
            elif conv_data['status'] == 'needs_improvement':
                insights.append(f"⚠️ Низкая конверсия ({conv_data['current_value']:.1%}) - нужно улучшить качество лидов")
        
        # Анализ размера сделок
        if 'average_deal_size' in comparison:
            deal_data = comparison['average_deal_size']
            if deal_data['status'] == 'excellent':
                insights.append(f"💰 Высокий средний чек ({deal_data['current_value']:,.0f} руб)")
            elif deal_data['status'] == 'needs_improvement':
                insights.append(f"📈 Работайте над увеличением среднего чека - потенциал {deal_data['gap']:,.0f} руб")
        
        # Анализ цикла продаж
        if 'sales_cycle_length' in comparison:
            cycle_data = comparison['sales_cycle_length']
            if cycle_data['status'] == 'excellent':
                insights.append(f"⚡ Быстрый цикл продаж ({cycle_data['current_value']:.0f} дней)")
            elif cycle_data['status'] == 'needs_improvement':
                insights.append(f"🐌 Длинный цикл продаж - оптимизируйте процесс квалификации")
        
        # Анализ win rate
        if 'win_rate' in comparison:
            win_data = comparison['win_rate']
            if win_data['status'] == 'needs_improvement':
                insights.append(f"🎯 Низкий win rate ({win_data['current_value']:.1%}) - улучшите презентацию ценности")
        
        # Рекомендации по оптимизации
        if kpis.get('conversion_rate', 0) < 0.02:
            insights.append("💡 Рекомендация: Внедрите lead scoring для фокуса на качественных лидах")
        
        if kpis.get('sales_cycle_length', 0) > 120:
            insights.append("💡 Рекомендация: Автоматизируйте процесс квалификации и нутуринга")
        
        return insights

# Демонстрация аналитики продаж
analytics = SalesAnalytics()

# Создаем тестовые данные продаж
test_sales_data = [
    {
        'date': '2024-01-15',
        'stage': 'lead',
        'amount': 0,
        'status': 'new',
        'marketing_cost': 5000
    },
    {
        'date': '2024-01-20',
        'stage': 'customer',
        'amount': 200000,
        'status': 'closed_won',
        'created_date': '2024-01-15',
        'closed_date': '2024-01-20',
        'marketing_cost': 0
    },
    {
        'date': '2024-01-25',
        'stage': 'lead',
        'amount': 0,
        'status': 'closed_lost',
        'created_date': '2024-01-10',
        'closed_date': '2024-01-25',
        'marketing_cost': 3000
    },
    {
        'date': '2024-01-30',
        'stage': 'customer', 
        'amount': 350000,
        'status': 'closed_won',
        'created_date': '2024-01-05',
        'closed_date': '2024-01-30',
        'marketing_cost': 0
    }
]

# Рассчитываем KPI
kpis = analytics.calculate_sales_kpis(test_sales_data, period_days=30)

print("=== KPI ПРОДАЖ ЗА 30 ДНЕЙ ===")
for kpi_name, value in kpis.items():
    if kpi_name != 'error':
        if kpi_name in ['conversion_rate', 'win_rate']:
            print(f"{kpi_name}: {value:.1%}")
        elif kpi_name in ['average_deal_size', 'customer_acquisition_cost']:
            print(f"{kpi_name}: {value:,.0f} руб")
        elif kpi_name == 'sales_cycle_length':
            print(f"{kpi_name}: {value:.1f} дней")
        else:
            print(f"{kpi_name}: {value:.2f}")

# Сравнение с бенчмарками
benchmark_comparison = analytics.compare_with_benchmarks(kpis, 'technology_industry')

print(f"\n=== СРАВНЕНИЕ С БЕНЧМАРКАМИ ===")
for kpi_name, comparison_data in benchmark_comparison.items():
    if isinstance(comparison_data, dict):
        status_icon = {
            'excellent': '🟢',
            'good': '🟡', 
            'acceptable': '🟠',
            'needs_improvement': '🔴'
        }.get(comparison_data['status'], '⚪')
        
        print(f"{status_icon} {kpi_name}: {comparison_data['status']}")
        print(f"    Текущее: {comparison_data['current_value']:.2f}")
        print(f"    Бенчмарк: {comparison_data['benchmark_value']:.2f}")
        print(f"    Отклонение: {comparison_data['performance_ratio']:.2f}x")

# Генерируем инсайты
insights = analytics.generate_sales_insights(kpis, benchmark_comparison)

print(f"\n=== ИНСАЙТЫ И РЕКОМЕНДАЦИИ ===")
for insight in insights:
    print(f"  {insight}")
```

## Ключевые моменты для экзамена

### Основные компоненты AI-продаж
1. **Lead Scoring**: Автоматическая оценка и приоритизация потенциальных клиентов
2. **Sales Forecasting**: Прогнозирование объемов продаж с использованием ML
3. **Personalization**: Персонализация предложений на основе профиля клиента
4. **Process Automation**: Автоматизация рутинных продажных процессов

### Технические решения
- **Scoring algorithms**: Алгоритмы оценки лидов по множественным факторам
- **Predictive models**: Модели прогнозирования продаж (ARIMA, Prophet, ML)
- **Customer segmentation**: Автоматическая сегментация клиентов
- **Behavioral tracking**: Отслеживание и анализ поведения покупателей

### Метрики и аналитика
- **Conversion funnel**: Анализ воронки продаж по этапам
- **Sales velocity**: Скорость движения сделок по воронке
- **Win/Loss analysis**: Анализ выигранных и проигранных сделок
- **ROI measurement**: Измерение возврата инвестиций в продажи

### Автоматизация процессов
- **Lead routing**: Автоматическое распределение лидов между менеджерами
- **Follow-up scheduling**: Планирование последующих контактов
- **Email automation**: Автоматические email кампании
- **Task management**: Автоматическое создание задач для менеджеров

### Практические преимущества
- Увеличение конверсии лидов в клиентов
- Сокращение цикла продаж
- Повышение эффективности работы менеджеров
- Улучшение прогнозируемости продаж
- Персонализация клиентского опыта