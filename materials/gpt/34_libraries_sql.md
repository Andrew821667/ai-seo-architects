# Полезные библиотеки и SQL для AI

## Python библиотеки для AI

### Основные ML/AI библиотеки

#### Scikit-learn
```python
# Основная библиотека для машинного обучения
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Пример классификации
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

# Предобработка данных
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

#### TensorFlow/Keras
```python
# Глубокое обучение
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Создание нейронной сети
model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=(input_dim,)),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

# Компиляция и обучение
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Сохранение модели
model.save('my_model.h5')
```

#### PyTorch
```python
# Альтернативный фреймворк для глубокого обучения
import torch
import torch.nn as nn
import torch.optim as optim

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# Инициализация модели
model = NeuralNetwork(input_size=784, hidden_size=500, num_classes=10)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Обучение
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

### NLP библиотеки

#### Transformers (Hugging Face)
```python
# Предобученные трансформеры
from transformers import (
    AutoTokenizer, AutoModel, pipeline,
    BertTokenizer, BertForSequenceClassification
)

# Sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis")
result = sentiment_pipeline("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Классификация текста
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
outputs = model(**inputs)

# Генерация текста
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

input_ids = tokenizer.encode("The future of AI is", return_tensors="pt")
output = model.generate(input_ids, max_length=50, num_return_sequences=1)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
```

#### spaCy
```python
# Обработка естественного языка
import spacy
from spacy import displacy

# Загрузка модели
nlp = spacy.load("en_core_web_sm")

text = "Apple is looking at buying U.K. startup for $1 billion"
doc = nlp(text)

# Извлечение именованных сущностей
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

# POS tagging
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)

# Сходство текстов
doc1 = nlp("I like salty fries and hamburgers.")
doc2 = nlp("Fast food tastes very good.")
similarity = doc1.similarity(doc2)

# Создание пользовательских компонентов
@spacy.component("custom_sentiment")
def sentiment_component(doc):
    # Пользовательская логика анализа настроения
    doc._.sentiment = calculate_sentiment(doc.text)
    return doc

nlp.add_pipe("custom_sentiment")
```

#### NLTK
```python
# Классическая NLP библиотека
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer

# Токенизация
text = "Natural Language Processing with Python is awesome!"
tokens = word_tokenize(text)
sentences = sent_tokenize(text)

# Удаление стоп-слов
stop_words = set(stopwords.words('english'))
filtered_tokens = [w for w in tokens if w.lower() not in stop_words]

# Стемминг и лемматизация
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

stemmed = [stemmer.stem(word) for word in tokens]
lemmatized = [lemmatizer.lemmatize(word) for word in tokens]

# Анализ настроения
sia = SentimentIntensityAnalyzer()
sentiment_scores = sia.polarity_scores(text)
print(sentiment_scores)
# {'neg': 0.0, 'neu': 0.692, 'pos': 0.308, 'compound': 0.6249}
```

### Библиотеки для работы с данными

#### Pandas
```python
# Анализ и обработка данных
import pandas as pd
import numpy as np

# Чтение данных
df = pd.read_csv('data.csv')
df = pd.read_json('data.json')
df = pd.read_sql('SELECT * FROM table', connection)

# Базовая статистика
print(df.describe())
print(df.info())
print(df.head())

# Фильтрация и группировка
filtered_df = df[df['column'] > 100]
grouped = df.groupby('category').agg({
    'sales': 'sum',
    'quantity': 'mean',
    'price': ['min', 'max']
})

# Обработка пропущенных значений
df.fillna(method='forward')
df.dropna()
df['column'].fillna(df['column'].mean())

# Применение функций
df['new_column'] = df['old_column'].apply(lambda x: x * 2)
df['category'] = df['category'].map({'A': 1, 'B': 2, 'C': 3})

# Объединение данных
merged_df = pd.merge(df1, df2, on='key_column', how='inner')
concatenated_df = pd.concat([df1, df2], axis=0)
```

#### NumPy
```python
# Вычисления с массивами
import numpy as np

# Создание массивов
arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
random_arr = np.random.rand(3, 3)

# Математические операции
result = np.dot(arr1, arr2)  # Скалярное произведение
mean_val = np.mean(arr)
std_val = np.std(arr)
max_val = np.max(arr)

# Индексирование и срезы
subset = arr[1:4]
condition_subset = arr[arr > 3]

# Работа с формой массива
reshaped = arr.reshape(5, 1)
transposed = arr.T
flattened = arr.flatten()

# Статистические функции
correlation = np.corrcoef(x, y)
percentile = np.percentile(arr, 75)
```

### Визуализация данных

#### Matplotlib
```python
# Базовая визуализация
import matplotlib.pyplot as plt

# Линейный график
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Data', linewidth=2)
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('My Plot')
plt.legend()
plt.grid(True)
plt.show()

# Гистограмма
plt.hist(data, bins=50, alpha=0.7, color='blue')
plt.title('Distribution')

# Scatter plot
plt.scatter(x, y, c=colors, alpha=0.6)
plt.colorbar()

# Subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].plot(x1, y1)
axes[0, 1].scatter(x2, y2)
axes[1, 0].bar(categories, values)
axes[1, 1].hist(data)
plt.tight_layout()
```

#### Seaborn
```python
# Статистическая визуализация
import seaborn as sns

# Настройка стиля
sns.set_style("whitegrid")
sns.set_palette("husl")

# Распределения
sns.histplot(data=df, x="column", hue="category")
sns.boxplot(data=df, x="category", y="value")
sns.violinplot(data=df, x="category", y="value")

# Корреляции
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

# Регрессии
sns.scatterplot(data=df, x="x", y="y", hue="category")
sns.regplot(data=df, x="x", y="y")

# Парные графики
sns.pairplot(df, hue="target_column")

# Временные ряды
sns.lineplot(data=df, x="date", y="value", hue="category")
```

#### Plotly
```python
# Интерактивная визуализация
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Интерактивный scatter plot
fig = px.scatter(df, x="x", y="y", color="category", 
                size="size", hover_data=["info"])
fig.show()

# 3D plot
fig = px.scatter_3d(df, x="x", y="y", z="z", color="category")
fig.show()

# Временные ряды
fig = px.line(df, x="date", y="value", color="category")
fig.update_layout(title="Time Series")
fig.show()

# Dashboard
fig = make_subplots(rows=2, cols=2, 
                    subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))

fig.add_trace(go.Scatter(x=x, y=y1), row=1, col=1)
fig.add_trace(go.Bar(x=categories, y=values), row=1, col=2)
fig.add_trace(go.Histogram(x=data), row=2, col=1)
fig.add_trace(go.Heatmap(z=matrix), row=2, col=2)

fig.update_layout(height=600, showlegend=False)
fig.show()
```

## SQL для AI проектов

### Работа с данными для обучения

#### Извлечение обучающих данных
```sql
-- Подготовка датасета для классификации
SELECT 
    user_id,
    email_domain,
    registration_date,
    last_login_date,
    total_sessions,
    avg_session_duration,
    total_purchases,
    total_spent,
    days_since_last_purchase,
    CASE 
        WHEN days_since_last_purchase <= 30 THEN 'active'
        WHEN days_since_last_purchase <= 90 THEN 'at_risk'
        ELSE 'churned'
    END as user_status
FROM (
    SELECT 
        u.user_id,
        SUBSTRING(u.email, POSITION('@' IN u.email) + 1) as email_domain,
        u.registration_date,
        MAX(s.session_start) as last_login_date,
        COUNT(s.session_id) as total_sessions,
        AVG(EXTRACT(EPOCH FROM (s.session_end - s.session_start))/60) as avg_session_duration,
        COUNT(DISTINCT o.order_id) as total_purchases,
        COALESCE(SUM(o.total_amount), 0) as total_spent,
        CURRENT_DATE - MAX(o.order_date) as days_since_last_purchase
    FROM users u
    LEFT JOIN sessions s ON u.user_id = s.user_id
    LEFT JOIN orders o ON u.user_id = o.user_id
    WHERE u.registration_date >= '2023-01-01'
    GROUP BY u.user_id, u.email, u.registration_date
) user_metrics;

-- Создание features для рекомендательной системы
WITH user_behavior AS (
    SELECT 
        user_id,
        product_category,
        COUNT(*) as view_count,
        SUM(CASE WHEN action = 'purchase' THEN 1 ELSE 0 END) as purchase_count,
        AVG(time_spent) as avg_time_spent,
        MAX(created_at) as last_interaction
    FROM user_interactions
    WHERE created_at >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY user_id, product_category
),
user_preferences AS (
    SELECT 
        user_id,
        STRING_AGG(
            product_category, 
            ',' ORDER BY view_count DESC
        ) as preferred_categories,
        COUNT(DISTINCT product_category) as category_diversity
    FROM user_behavior
    WHERE view_count >= 3
    GROUP BY user_id
)
SELECT 
    ub.user_id,
    ub.product_category,
    ub.view_count,
    ub.purchase_count,
    ub.avg_time_spent,
    up.preferred_categories,
    up.category_diversity,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - ub.last_interaction))/86400 as days_since_last_interaction
FROM user_behavior ub
JOIN user_preferences up ON ub.user_id = up.user_id;
```

#### Временные ряды и тренды
```sql
-- Подготовка данных для прогнозирования временных рядов
SELECT 
    DATE_TRUNC('day', created_at) as date,
    product_category,
    COUNT(*) as daily_orders,
    SUM(total_amount) as daily_revenue,
    AVG(total_amount) as avg_order_value,
    COUNT(DISTINCT user_id) as unique_customers,
    -- Moving averages
    AVG(COUNT(*)) OVER (
        PARTITION BY product_category 
        ORDER BY DATE_TRUNC('day', created_at) 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma_7_orders,
    AVG(SUM(total_amount)) OVER (
        PARTITION BY product_category 
        ORDER BY DATE_TRUNC('day', created_at) 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma_7_revenue,
    -- Seasonal features
    EXTRACT(DOW FROM created_at) as day_of_week,
    EXTRACT(MONTH FROM created_at) as month,
    EXTRACT(QUARTER FROM created_at) as quarter,
    -- Lag features
    LAG(COUNT(*), 1) OVER (
        PARTITION BY product_category 
        ORDER BY DATE_TRUNC('day', created_at)
    ) as orders_lag_1,
    LAG(COUNT(*), 7) OVER (
        PARTITION BY product_category 
        ORDER BY DATE_TRUNC('day', created_at)
    ) as orders_lag_7
FROM orders
WHERE created_at >= '2023-01-01'
GROUP BY DATE_TRUNC('day', created_at), product_category
ORDER BY date, product_category;

-- Anomaly detection features
WITH daily_metrics AS (
    SELECT 
        DATE_TRUNC('day', timestamp) as date,
        COUNT(*) as daily_events,
        AVG(response_time) as avg_response_time,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time) as p95_response_time,
        COUNT(DISTINCT user_id) as unique_users
    FROM system_logs
    WHERE timestamp >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY DATE_TRUNC('day', timestamp)
),
metrics_with_stats AS (
    SELECT 
        *,
        AVG(daily_events) OVER () as mean_events,
        STDDEV(daily_events) OVER () as stddev_events,
        AVG(avg_response_time) OVER () as mean_response_time,
        STDDEV(avg_response_time) OVER () as stddev_response_time
    FROM daily_metrics
)
SELECT 
    date,
    daily_events,
    avg_response_time,
    p95_response_time,
    unique_users,
    -- Z-scores for anomaly detection
    (daily_events - mean_events) / NULLIF(stddev_events, 0) as events_zscore,
    (avg_response_time - mean_response_time) / NULLIF(stddev_response_time, 0) as response_time_zscore,
    -- Anomaly flags
    CASE 
        WHEN ABS((daily_events - mean_events) / NULLIF(stddev_events, 0)) > 2 THEN true
        ELSE false
    END as is_events_anomaly,
    CASE 
        WHEN ABS((avg_response_time - mean_response_time) / NULLIF(stddev_response_time, 0)) > 2 THEN true
        ELSE false
    END as is_response_time_anomaly
FROM metrics_with_stats
ORDER BY date;
```

### Feature Engineering в SQL

#### Создание признаков
```sql
-- RFM анализ для сегментации клиентов
WITH customer_rfm AS (
    SELECT 
        customer_id,
        -- Recency (дни с последней покупки)
        CURRENT_DATE - MAX(order_date) as recency,
        -- Frequency (количество заказов)
        COUNT(DISTINCT order_id) as frequency,
        -- Monetary (общая сумма покупок)
        SUM(order_total) as monetary
    FROM orders
    WHERE order_date >= '2023-01-01'
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency,
        frequency,
        monetary,
        -- Создание квинтилей для каждой метрики
        NTILE(5) OVER (ORDER BY recency DESC) as recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) as frequency_score,
        NTILE(5) OVER (ORDER BY monetary ASC) as monetary_score
    FROM customer_rfm
)
SELECT 
    customer_id,
    recency,
    frequency,
    monetary,
    recency_score,
    frequency_score,
    monetary_score,
    -- Комбинированный RFM скор
    CAST(recency_score AS VARCHAR) || 
    CAST(frequency_score AS VARCHAR) || 
    CAST(monetary_score AS VARCHAR) as rfm_segment,
    -- Категоризация клиентов
    CASE 
        WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
        WHEN recency_score >= 3 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'Loyal Customers'
        WHEN recency_score >= 3 AND frequency_score <= 2 AND monetary_score >= 3 THEN 'Big Spenders'
        WHEN recency_score >= 4 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'New Customers'
        WHEN recency_score <= 2 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'At Risk'
        WHEN recency_score <= 2 AND frequency_score <= 2 AND monetary_score >= 3 THEN 'Cannot Lose Them'
        WHEN recency_score <= 2 AND frequency_score <= 2 AND monetary_score <= 2 THEN 'Hibernating'
        ELSE 'Others'
    END as customer_segment
FROM rfm_scores;

-- Создание текстовых features для NLP
SELECT 
    ticket_id,
    subject,
    description,
    category,
    priority,
    -- Длина текста
    LENGTH(description) as text_length,
    LENGTH(description) - LENGTH(REPLACE(description, ' ', '')) + 1 as word_count,
    -- Наличие специальных слов
    CASE WHEN LOWER(description) LIKE '%urgent%' THEN 1 ELSE 0 END as has_urgent,
    CASE WHEN LOWER(description) LIKE '%error%' THEN 1 ELSE 0 END as has_error,
    CASE WHEN LOWER(description) LIKE '%api%' THEN 1 ELSE 0 END as has_api,
    CASE WHEN description ~ '\d+' THEN 1 ELSE 0 END as has_numbers,
    -- Количество восклицательных знаков (индикатор эмоций)
    LENGTH(description) - LENGTH(REPLACE(description, '!', '')) as exclamation_count,
    -- Время создания features
    EXTRACT(HOUR FROM created_at) as hour_of_day,
    EXTRACT(DOW FROM created_at) as day_of_week,
    -- Email domain клиента
    SPLIT_PART(customer_email, '@', 2) as email_domain
FROM support_tickets
WHERE created_at >= '2023-01-01';
```

#### Агрегированные признаки
```sql
-- Создание пользовательских агрегатов
WITH user_aggregates AS (
    SELECT 
        user_id,
        -- Поведенческие метрики за последние 30 дней
        COUNT(CASE WHEN action_date >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) as actions_30d,
        COUNT(CASE WHEN action_date >= CURRENT_DATE - INTERVAL '7 days' THEN 1 END) as actions_7d,
        COUNT(CASE WHEN action_date >= CURRENT_DATE - INTERVAL '1 day' THEN 1 END) as actions_1d,
        
        -- Типы активности
        COUNT(CASE WHEN action_type = 'page_view' THEN 1 END) as page_views,
        COUNT(CASE WHEN action_type = 'click' THEN 1 END) as clicks,
        COUNT(CASE WHEN action_type = 'purchase' THEN 1 END) as purchases,
        
        -- Временные паттерны
        MODE() WITHIN GROUP (ORDER BY EXTRACT(HOUR FROM action_timestamp)) as favorite_hour,
        COUNT(DISTINCT DATE(action_timestamp)) as active_days,
        
        -- Последовательности действий
        STRING_AGG(
            action_type, 
            '->' ORDER BY action_timestamp
        ) as action_sequence,
        
        -- Статистики по времени между действиями
        AVG(
            EXTRACT(EPOCH FROM (
                action_timestamp - LAG(action_timestamp) 
                OVER (PARTITION BY user_id ORDER BY action_timestamp)
            ))
        ) as avg_time_between_actions
        
    FROM user_actions
    WHERE action_date >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY user_id
),
session_aggregates AS (
    SELECT 
        user_id,
        AVG(session_duration) as avg_session_duration,
        MAX(session_duration) as max_session_duration,
        COUNT(*) as total_sessions,
        AVG(pages_per_session) as avg_pages_per_session,
        SUM(CASE WHEN bounce_rate = 1 THEN 1 ELSE 0 END) / COUNT(*)::FLOAT as bounce_rate
    FROM sessions
    WHERE session_date >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY user_id
)
SELECT 
    ua.*,
    sa.avg_session_duration,
    sa.max_session_duration,
    sa.total_sessions,
    sa.avg_pages_per_session,
    sa.bounce_rate,
    -- Производные features
    CASE WHEN ua.actions_30d = 0 THEN 0 
         ELSE ua.purchases::FLOAT / ua.actions_30d 
    END as conversion_rate,
    ua.actions_7d::FLOAT / NULLIF(ua.actions_30d, 0) as recent_activity_ratio
FROM user_aggregates ua
LEFT JOIN session_aggregates sa ON ua.user_id = sa.user_id;
```

### Мониторинг моделей

#### A/B тестирование моделей
```sql
-- Сравнение производительности моделей
WITH model_predictions AS (
    SELECT 
        prediction_id,
        user_id,
        model_version,
        predicted_value,
        actual_value,
        prediction_timestamp,
        -- Абсолютная ошибка
        ABS(predicted_value - actual_value) as absolute_error,
        -- Квадратичная ошибка
        POWER(predicted_value - actual_value, 2) as squared_error,
        -- Процентная ошибка
        ABS(predicted_value - actual_value) / NULLIF(actual_value, 0) as percentage_error
    FROM ml_predictions
    WHERE prediction_timestamp >= CURRENT_DATE - INTERVAL '7 days'
      AND actual_value IS NOT NULL
),
model_metrics AS (
    SELECT 
        model_version,
        COUNT(*) as prediction_count,
        -- Регрессионные метрики
        AVG(absolute_error) as mae,
        SQRT(AVG(squared_error)) as rmse,
        AVG(percentage_error) * 100 as mape,
        -- R-squared
        1 - (SUM(squared_error) / 
             SUM(POWER(actual_value - AVG(actual_value) OVER (), 2))) as r_squared,
        -- Временные метрики
        AVG(
            EXTRACT(EPOCH FROM (
                CURRENT_TIMESTAMP - prediction_timestamp
            ))
        ) as avg_prediction_latency
    FROM model_predictions
    GROUP BY model_version
)
SELECT 
    model_version,
    prediction_count,
    ROUND(mae::NUMERIC, 4) as mae,
    ROUND(rmse::NUMERIC, 4) as rmse,
    ROUND(mape::NUMERIC, 2) as mape_percent,
    ROUND(r_squared::NUMERIC, 4) as r_squared,
    ROUND(avg_prediction_latency::NUMERIC, 2) as avg_latency_seconds,
    -- Ранжирование моделей
    RANK() OVER (ORDER BY rmse ASC) as rmse_rank,
    RANK() OVER (ORDER BY mape ASC) as mape_rank
FROM model_metrics
ORDER BY rmse ASC;

-- Drift detection
WITH recent_data AS (
    SELECT 
        DATE_TRUNC('day', created_at) as date,
        AVG(feature_1) as avg_feature_1,
        STDDEV(feature_1) as std_feature_1,
        AVG(feature_2) as avg_feature_2,
        STDDEV(feature_2) as std_feature_2,
        COUNT(*) as sample_count
    FROM production_data
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY DATE_TRUNC('day', created_at)
),
training_baseline AS (
    SELECT 
        AVG(feature_1) as baseline_avg_feature_1,
        STDDEV(feature_1) as baseline_std_feature_1,
        AVG(feature_2) as baseline_avg_feature_2,
        STDDEV(feature_2) as baseline_std_feature_2
    FROM training_data
),
drift_analysis AS (
    SELECT 
        rd.date,
        rd.avg_feature_1,
        rd.std_feature_1,
        rd.sample_count,
        tb.baseline_avg_feature_1,
        tb.baseline_std_feature_1,
        -- Расчет drift scores
        ABS(rd.avg_feature_1 - tb.baseline_avg_feature_1) / 
        NULLIF(tb.baseline_std_feature_1, 0) as feature_1_drift_score,
        ABS(rd.avg_feature_2 - tb.baseline_avg_feature_2) / 
        NULLIF(tb.baseline_std_feature_2, 0) as feature_2_drift_score
    FROM recent_data rd
    CROSS JOIN training_baseline tb
)
SELECT 
    date,
    avg_feature_1,
    baseline_avg_feature_1,
    feature_1_drift_score,
    feature_2_drift_score,
    CASE 
        WHEN feature_1_drift_score > 2 OR feature_2_drift_score > 2 THEN 'HIGH_DRIFT'
        WHEN feature_1_drift_score > 1 OR feature_2_drift_score > 1 THEN 'MEDIUM_DRIFT'
        ELSE 'NO_DRIFT'
    END as drift_status
FROM drift_analysis
WHERE date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY date DESC;
```

### Optimized запросы для больших данных

#### Работа с партицированными таблицами
```sql
-- Создание партицированной таблицы для ML данных
CREATE TABLE ml_features (
    id BIGSERIAL,
    user_id BIGINT,
    feature_date DATE,
    feature_vector JSONB,
    target_value FLOAT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (feature_date);

-- Создание партиций
CREATE TABLE ml_features_2024_01 PARTITION OF ml_features
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE ml_features_2024_02 PARTITION OF ml_features
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Индексы для оптимизации
CREATE INDEX idx_ml_features_user_date ON ml_features (user_id, feature_date);
CREATE INDEX idx_ml_features_model_version ON ml_features (model_version);
CREATE INDEX idx_ml_features_target ON ml_features (target_value) WHERE target_value IS NOT NULL;

-- Эффективное извлечение features
SELECT 
    user_id,
    feature_vector,
    target_value
FROM ml_features
WHERE feature_date >= '2024-02-01'
  AND feature_date < '2024-03-01'
  AND model_version = 'v2.1'
  AND target_value IS NOT NULL;
```

#### Пакетная обработка для ML
```sql
-- Batch processing для feature engineering
WITH RECURSIVE date_series AS (
    SELECT '2024-01-01'::DATE as process_date
    UNION ALL
    SELECT process_date + INTERVAL '1 day'
    FROM date_series
    WHERE process_date < '2024-03-01'::DATE
),
daily_features AS (
    SELECT 
        ds.process_date,
        u.user_id,
        -- Feature engineering с window functions
        COUNT(a.action_id) OVER (
            PARTITION BY u.user_id 
            ORDER BY ds.process_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as actions_last_7_days,
        
        SUM(CASE WHEN a.action_type = 'purchase' THEN a.value ELSE 0 END) OVER (
            PARTITION BY u.user_id 
            ORDER BY ds.process_date 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) as revenue_last_30_days,
        
        ROW_NUMBER() OVER (
            PARTITION BY u.user_id, ds.process_date 
            ORDER BY a.action_timestamp DESC
        ) as rn
        
    FROM date_series ds
    CROSS JOIN users u
    LEFT JOIN actions a ON u.user_id = a.user_id 
        AND a.action_date = ds.process_date
)
-- Вставка только уникальных записей
INSERT INTO ml_features (user_id, feature_date, feature_vector)
SELECT 
    user_id,
    process_date,
    jsonb_build_object(
        'actions_7d', actions_last_7_days,
        'revenue_30d', revenue_last_30_days
    )
FROM daily_features
WHERE rn = 1  -- Дедупликация
ON CONFLICT (user_id, feature_date) DO UPDATE SET
    feature_vector = EXCLUDED.feature_vector,
    updated_at = CURRENT_TIMESTAMP;

-- Batch prediction scoring
WITH batch_predictions AS (
    SELECT 
        user_id,
        feature_date,
        -- Простая модель скоринга (в реальности это был бы ML pipeline)
        CASE 
            WHEN (feature_vector->>'revenue_30d')::FLOAT > 1000 
                 AND (feature_vector->>'actions_7d')::INT > 10 THEN 'high_value'
            WHEN (feature_vector->>'revenue_30d')::FLOAT > 500 
                 AND (feature_vector->>'actions_7d')::INT > 5 THEN 'medium_value'
            ELSE 'low_value'
        END as predicted_segment,
        
        -- Confidence score
        CASE 
            WHEN (feature_vector->>'revenue_30d')::FLOAT > 1000 THEN 0.9
            WHEN (feature_vector->>'revenue_30d')::FLOAT > 500 THEN 0.7
            ELSE 0.5
        END as confidence_score
        
    FROM ml_features
    WHERE feature_date = CURRENT_DATE
      AND feature_vector IS NOT NULL
)
INSERT INTO model_predictions (user_id, prediction_date, predicted_segment, confidence)
SELECT user_id, feature_date, predicted_segment, confidence_score
FROM batch_predictions;
```

## Практические шаблоны

### Data Pipeline для ML
```python
# Пример ETL pipeline для ML данных
class MLDataPipeline:
    def __init__(self, db_connection, feature_store):
        self.db = db_connection
        self.feature_store = feature_store
        
    def extract_raw_data(self, start_date, end_date):
        """Извлечение сырых данных"""
        query = """
        SELECT 
            user_id,
            action_timestamp,
            action_type,
            page_url,
            session_id,
            device_type,
            referrer
        FROM user_events
        WHERE action_timestamp >= %s AND action_timestamp < %s
        ORDER BY user_id, action_timestamp
        """
        
        return pd.read_sql(query, self.db, params=[start_date, end_date])
    
    def transform_features(self, raw_data):
        """Преобразование в признаки"""
        
        # Временные признаки
        raw_data['hour'] = raw_data['action_timestamp'].dt.hour
        raw_data['day_of_week'] = raw_data['action_timestamp'].dt.dayofweek
        
        # Пользовательские агрегаты
        user_features = raw_data.groupby('user_id').agg({
            'action_timestamp': ['count', 'nunique'],
            'session_id': 'nunique',
            'page_url': lambda x: len(set(x)),
            'hour': lambda x: x.value_counts().index[0] if len(x) > 0 else None
        }).round(4)
        
        user_features.columns = [
            'total_actions', 'unique_days', 'unique_sessions', 
            'unique_pages', 'favorite_hour'
        ]
        
        # Поведенческие паттерны
        sequences = raw_data.groupby('user_id')['action_type'].apply(
            lambda x: '->'.join(x.head(10))
        ).reset_index()
        sequences.columns = ['user_id', 'action_sequence']
        
        # Объединение признаков
        features = user_features.merge(sequences, on='user_id')
        
        return features
    
    def load_to_feature_store(self, features, date):
        """Загрузка в feature store"""
        
        features['feature_date'] = date
        features['created_at'] = datetime.now()
        
        # Запись в базу данных
        features.to_sql(
            'ml_features', 
            self.db, 
            if_exists='append', 
            index=False,
            method='multi'
        )
        
        # Обновление feature store для real-time inference
        for _, row in features.iterrows():
            self.feature_store.set(
                f"user_features:{row['user_id']}", 
                row.to_json()
            )
    
    def run_pipeline(self, date):
        """Запуск полного pipeline"""
        
        try:
            # Extract
            raw_data = self.extract_raw_data(date, date + timedelta(days=1))
            
            # Transform
            features = self.transform_features(raw_data)
            
            # Load
            self.load_to_feature_store(features, date)
            
            return {
                'status': 'success',
                'processed_users': len(features),
                'date': date.isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'date': date.isoformat()
            }

# Использование
pipeline = MLDataPipeline(db_connection, redis_client)
result = pipeline.run_pipeline(datetime(2024, 2, 1))
```

### Model Monitoring
```python
# Система мониторинга моделей
import numpy as np
from scipy import stats
from datetime import datetime, timedelta

class ModelMonitor:
    def __init__(self, db_connection):
        self.db = db_connection
        self.thresholds = {
            'drift_score': 0.1,
            'accuracy_drop': 0.05,
            'latency_increase': 1.5  # x раз
        }
    
    def calculate_drift_score(self, baseline_data, current_data, features):
        """Расчет drift score для признаков"""
        
        drift_scores = {}
        
        for feature in features:
            if feature in baseline_data.columns and feature in current_data.columns:
                
                baseline_values = baseline_data[feature].dropna()
                current_values = current_data[feature].dropna()
                
                if len(baseline_values) > 0 and len(current_values) > 0:
                    # Kolmogorov-Smirnov test
                    ks_stat, p_value = stats.ks_2samp(baseline_values, current_values)
                    
                    # Population Stability Index
                    psi = self._calculate_psi(baseline_values, current_values)
                    
                    drift_scores[feature] = {
                        'ks_statistic': ks_stat,
                        'ks_p_value': p_value,
                        'psi': psi,
                        'drift_detected': psi > 0.1 or p_value < 0.05
                    }
        
        return drift_scores
    
    def _calculate_psi(self, baseline, current, bins=10):
        """Population Stability Index"""
        
        # Создание bins на основе baseline
        bin_edges = np.histogram_bin_edges(baseline, bins=bins)
        
        # Распределения
        baseline_counts, _ = np.histogram(baseline, bins=bin_edges)
        current_counts, _ = np.histogram(current, bins=bin_edges)
        
        # Нормализация
        baseline_pcts = baseline_counts / len(baseline)
        current_pcts = current_counts / len(current)
        
        # PSI calculation
        psi = np.sum((current_pcts - baseline_pcts) * 
                     np.log(current_pcts / (baseline_pcts + 1e-10) + 1e-10))
        
        return psi
    
    def monitor_model_performance(self, model_name, days_back=7):
        """Мониторинг производительности модели"""
        
        query = """
        SELECT 
            DATE(prediction_timestamp) as date,
            AVG(CASE WHEN actual_value IS NOT NULL 
                THEN ABS(predicted_value - actual_value) END) as mae,
            AVG(CASE WHEN actual_value IS NOT NULL 
                THEN POWER(predicted_value - actual_value, 2) END) as mse,
            COUNT(*) as total_predictions,
            COUNT(CASE WHEN actual_value IS NOT NULL THEN 1 END) as predictions_with_actuals,
            AVG(prediction_latency_ms) as avg_latency
        FROM model_predictions
        WHERE model_name = %s
          AND prediction_timestamp >= CURRENT_DATE - INTERVAL '%s days'
        GROUP BY DATE(prediction_timestamp)
        ORDER BY date DESC
        """
        
        performance_data = pd.read_sql(
            query, self.db, params=[model_name, days_back]
        )
        
        if len(performance_data) == 0:
            return {'status': 'no_data'}
        
        # Анализ трендов
        recent_mae = performance_data['mae'].iloc[0] if len(performance_data) > 0 else None
        baseline_mae = performance_data['mae'].iloc[-1] if len(performance_data) > 1 else None
        
        alerts = []
        
        if recent_mae and baseline_mae:
            mae_change = (recent_mae - baseline_mae) / baseline_mae
            if mae_change > self.thresholds['accuracy_drop']:
                alerts.append({
                    'type': 'accuracy_degradation',
                    'severity': 'high' if mae_change > 0.1 else 'medium',
                    'message': f'MAE increased by {mae_change:.2%}',
                    'current_mae': recent_mae,
                    'baseline_mae': baseline_mae
                })
        
        # Проверка latency
        recent_latency = performance_data['avg_latency'].iloc[0]
        baseline_latency = performance_data['avg_latency'].iloc[-1]
        
        if recent_latency / baseline_latency > self.thresholds['latency_increase']:
            alerts.append({
                'type': 'latency_increase',
                'severity': 'medium',
                'message': f'Average latency increased to {recent_latency:.1f}ms',
                'current_latency': recent_latency,
                'baseline_latency': baseline_latency
            })
        
        return {
            'status': 'success',
            'model_name': model_name,
            'performance_data': performance_data.to_dict('records'),
            'alerts': alerts,
            'summary': {
                'current_mae': recent_mae,
                'current_latency': recent_latency,
                'prediction_volume': performance_data['total_predictions'].sum(),
                'coverage': performance_data['predictions_with_actuals'].sum() / 
                           performance_data['total_predictions'].sum()
            }
        }
    
    def generate_monitoring_report(self, model_name):
        """Генерация полного отчета мониторинга"""
        
        # Производительность модели
        performance = self.monitor_model_performance(model_name)
        
        # Feature drift analysis
        baseline_query = """
        SELECT * FROM training_features 
        WHERE model_version = (
            SELECT model_version FROM model_metadata 
            WHERE model_name = %s AND is_active = true
        )
        """
        
        current_query = """
        SELECT * FROM production_features
        WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
        """
        
        baseline_data = pd.read_sql(baseline_query, self.db, params=[model_name])
        current_data = pd.read_sql(current_query, self.db)
        
        feature_columns = [col for col in baseline_data.columns 
                          if col not in ['id', 'created_at', 'model_version']]
        
        drift_analysis = self.calculate_drift_score(
            baseline_data, current_data, feature_columns
        )
        
        return {
            'model_name': model_name,
            'generated_at': datetime.now().isoformat(),
            'performance_monitoring': performance,
            'feature_drift': drift_analysis,
            'recommendations': self._generate_recommendations(performance, drift_analysis)
        }
    
    def _generate_recommendations(self, performance, drift_analysis):
        """Генерация рекомендаций на основе анализа"""
        
        recommendations = []
        
        # Рекомендации по производительности
        if performance.get('alerts'):
            for alert in performance['alerts']:
                if alert['type'] == 'accuracy_degradation':
                    recommendations.append({
                        'type': 'retrain_model',
                        'priority': 'high',
                        'reason': 'Model accuracy degradation detected',
                        'action': 'Schedule model retraining with recent data'
                    })
                elif alert['type'] == 'latency_increase':
                    recommendations.append({
                        'type': 'optimize_inference',
                        'priority': 'medium',
                        'reason': 'Inference latency increased',
                        'action': 'Investigate and optimize prediction pipeline'
                    })
        
        # Рекомендации по drift
        high_drift_features = [
            feature for feature, metrics in drift_analysis.items()
            if metrics.get('drift_detected', False) and metrics.get('psi', 0) > 0.2
        ]
        
        if high_drift_features:
            recommendations.append({
                'type': 'feature_engineering',
                'priority': 'high',
                'reason': f'High drift detected in features: {", ".join(high_drift_features)}',
                'action': 'Review and update feature engineering pipeline'
            })
        
        return recommendations

# Использование
monitor = ModelMonitor(db_connection)
report = monitor.generate_monitoring_report('churn_prediction_v2')
```

## Практические упражнения

1. **Feature Engineering**: Создай SQL скрипты для извлечения признаков из своих данных
2. **Model Pipeline**: Построй end-to-end pipeline от данных до предсказаний
3. **Monitoring System**: Реализуй систему мониторинга дрифта и производительности
4. **Data Quality**: Создай checks для валидации данных в ML pipeline
5. **A/B Testing**: Настрой сравнение моделей с помощью SQL и Python

## Лучшие практики

### Работа с данными
- Версионирование данных и моделей
- Автоматизация data quality checks
- Мониторинг дрифта признаков
- Backup и recovery стратегии
- Документирование data lineage

### Производительность
- Индексирование для ML запросов
- Партиционирование больших таблиц
- Кеширование часто используемых признаков
- Batch processing для feature engineering
- Оптимизация inference latency

### Безопасность и compliance
- Защита персональных данных
- Audit trails для моделей
- Access control для данных
- GDPR compliance в ML pipeline
- Secure model deployment