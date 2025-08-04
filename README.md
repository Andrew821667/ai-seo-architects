# 🤖 AI SEO Architects

> **Мультиагентная RAG-система для автоматизации SEO-агентства**  
> Интеллектуальная архитектура из 5 специализированных AI-агентов с 3-уровневой иерархией на LangGraph

## 📋 Описание проекта

AI SEO Architects — это продвинутая мультиагентная система для полной автоматизации бизнес-процессов SEO-агентства. Система использует иерархическую архитектуру агентов для обработки всего цикла: от квалификации лидов до генерации коммерческих предложений.

### 🎯 **Основные возможности:**
- **Автоматическая квалификация лидов** с BANT/MEDDIC методологиями
- **AI-powered генерация предложений** с динамическим ценообразованием  
- **Автоматизация B2B продаж** с СПИН-техниками
- **Стратегический анализ** для enterprise клиентов
- **Интеллектуальная координация задач** между агентами

## 🏗️ Архитектура системы

### **3-уровневая иерархия агентов:**

#### 🎯 **Executive Level (1 агент)**
- **Business Development Director** - Стратегический анализ и enterprise assessment

#### 🎛️ **Management Level (1 агент)**  
- **Task Coordination Agent** - Маршрутизация задач и приоритизация

#### ⚙️ **Operational Level (3 агента)**
- **Lead Qualification Agent** - Квалификация и scoring лидов
- **Proposal Generation Agent** - Автогенерация коммерческих предложений
- **Sales Conversation Agent** - Автоматизация продажных переговоров

## 🚀 Быстрый старт

### Системные требования
- Python 3.8+
- pip или conda
- Интернет-соединение для AI моделей

### Установка

```bash
# Клонирование репозитория
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# Установка зависимостей
pip install -r requirements.txt

# Запуск интеграционных тестов
python test_agents_integration.py
```

### ⚡ Базовое использование

```python
from agents.operational.lead_qualification import LeadQualificationAgent
from mock_data_provider import MockDataProvider

# Инициализация агента
provider = MockDataProvider()
agent = LeadQualificationAgent(data_provider=provider)

# Квалификация лида
lead_data = {
    "company_name": "TechCorp",
    "email": "ceo@techcorp.ru", 
    "industry": "fintech",
    "budget_range": "5000000-10000000"
}

result = await agent.process_task({"input_data": lead_data})
print(f"Lead Score: {result['lead_score']}/100")
print(f"Qualification: {result['qualification']}")
```

## 📁 Структура проекта

```
ai-seo-architects/
├── agents/                     # AI агенты
│   ├── executive/              # Executive уровень
│   │   └── business_development_director.py
│   ├── management/             # Management уровень  
│   │   └── task_coordination.py
│   └── operational/            # Operational уровень
│       ├── lead_qualification.py
│       ├── proposal_generation.py
│       └── sales_conversation.py
├── core/                       # Базовая архитектура
│   ├── base_agent.py          # Базовый класс агентов
│   ├── orchestrator.py        # LangGraph оркестратор
│   ├── data_providers/        # Провайдеры данных
│   └── interfaces/            # Интерфейсы и модели
├── knowledge/                  # Базы знаний агентов
│   ├── executive/             # KB для executive агентов
│   ├── management/            # KB для management агентов  
│   └── operational/           # KB для operational агентов
├── mock_data_provider.py      # Mock провайдер для тестов
├── test_agents_integration.py # Интеграционные тесты
└── requirements.txt           # Зависимости Python
```

## 🧪 Тестирование

### Интеграционные тесты
```bash
python test_agents_integration.py
```

**Результаты последнего тестирования:**
- ✅ **100% success rate** 
- ✅ **5/5 агентов работают**
- ✅ **Lead Score: 100/100** (Hot Lead)
- ✅ **Sales Quality: Good** (70% close probability)
- ✅ **Proposal Value: 3.2M ₽/год**

## 🔧 Технические детали

### Используемые технологии
- **LangGraph** - Оркестрация мультиагентных workflow
- **LangChain** - AI/LLM интеграции
- **Pydantic** - Валидация данных и типизация
- **FastAPI** - Web API (планируется)
- **OpenAI GPT-4** - Основная LLM для агентов

### Ключевые компоненты
- **BaseAgent** - Базовый класс для всех агентов
- **MockDataProvider** - Тестовый провайдер данных
- **AgentMetrics** - Система метрик производительности
- **LeadData/LeadOutput** - Pydantic модели для типизации

## 📊 Возможности агентов

### Lead Qualification Agent
- **BANT/MEDDIC** квалификация
- **Агрессивный scoring** (до 100 баллов)
- **Отраслевая специализация** (FinTech, E-commerce, B2B)
- **Enterprise detection** (+25 баллов бонус)

### Proposal Generation Agent  
- **Динамическое ценообразование** по отраслям
- **ROI проекции** на 6/12/24 месяца
- **Пакетные предложения** со скидками
- **Персонализация** под industry/company size

### Sales Conversation Agent
- **СПИН методология** для discovery calls
- **Работа с возражениями** (500+ готовых ответов)
- **Российская B2B специфика**
- **Multi-industry подходы**

## 🎯 Планы развития

### В разработке
- [ ] Web UI для управления агентами
- [ ] Интеграция с реальными CRM системами
- [ ] Расширение до 14 агентов согласно roadmap
- [ ] ML-модели для улучшения scoring
- [ ] API для внешних интеграций

### Roadmap
- **Q1 2025:** Web интерфейс и API
- **Q2 2025:** CRM интеграции (HubSpot, Salesforce)
- **Q3 2025:** Дополнительные агенты (Content, Analytics, etc.)
- **Q4 2025:** ML pipeline и advanced analytics

## 📞 Контакты

**Автор:** Andrew Popov  
**Email:** a.popov.gv@gmail.com  
**GitHub:** [Andrew821667](https://github.com/Andrew821667)

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

---

⭐ **Если проект полезен, поставьте звездочку!**