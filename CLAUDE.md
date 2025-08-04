# 🤖 Claude Code Integration

> **Документ для интеграции с Claude Code**  
> Этот файл помогает Claude понимать контекст проекта и выполнять задачи более эффективно

## 📋 О проекте

**AI SEO Architects** - enterprise-ready мультиагентная RAG-система для автоматизации SEO-агентства с полной архитектурой из 14 специализированных AI-агентов, построенная на LangGraph и готовая к production развертыванию.

### 🎯 Текущий статус: 6/14 агентов (42.9% готовности)

## 🏗️ Полная архитектура 14 агентов

### ✅ **Реализованные агенты (6/14):**

#### Executive Level (2/2):
- **Chief SEO Strategist** - Стратегическое SEO планирование, алгоритмы поисковых систем, архитектура решений
- **Business Development Director** - Enterprise сделки 2.5M+ ₽/MRR, стратегические партнерства

#### Management Level (1/4):
- **Task Coordination Agent** - LangGraph маршрутизация, приоритизация задач

#### Operational Level (3/8):
- **Lead Qualification Agent** - BANT/MEDDIC квалификация с ML scoring
- **Proposal Generation Agent** - Динамическое ценообразование, ROI калькуляции
- **Sales Conversation Agent** - СПИН методология, B2B переговоры с российской спецификой

### 🔄 **Планируемые агенты (8/14):**

#### Management Level (3/4):
- **Sales Operations Manager** - Pipeline velocity, lead scoring, A/B testing email campaigns
- **Technical SEO Operations Manager** - Core Web Vitals, crawling coordination, log file analysis
- **Client Success Manager** - Churn prediction, upselling матрицы, QBR generation

#### Operational Level (5/8):
- **Technical SEO Auditor** - Crawling (Screaming Frog API), Core Web Vitals, JS SEO
- **Content Strategy Agent** - Keyword research (SEMrush/Ahrefs API), TF-IDF analysis, E-E-A-T
- **Link Building Agent** - Outreach automation, domain authority, toxic link detection
- **Competitive Analysis Agent** - SERP analysis, share of voice, competitive gap analysis
- **Reporting Agent** - BI integration, automated insights, anomaly detection

## 🔧 Технический стек

### **Текущий (MVP):**
- **LangGraph** - Оркестрация мультиагентных workflow
- **LangChain** - AI/LLM интеграции
- **Pydantic** - Валидация данных и типизация  
- **OpenAI GPT-4** - Основная LLM для агентов

### **Планируемый (Enterprise):**
- **FastAPI** - REST API backend
- **PostgreSQL** - Основная база данных
- **Redis** - Кэширование и сессии
- **Chroma/Pinecone** - Vector storage для RAG
- **Docker/Kubernetes** - Контейнеризация

## 📁 Ключевые директории

```
ai-seo-architects/
├── agents/                    # AI агенты по уровням
│   ├── executive/            # Executive уровень (2/2)
│   ├── management/           # Management уровень (1/4)  
│   └── operational/          # Operational уровень (3/8)
├── core/                     # Базовая архитектура
│   ├── base_agent.py        # Базовый класс агентов
│   ├── orchestrator.py      # LangGraph оркестратор
│   └── data_providers/      # Провайдеры данных
├── knowledge/               # Базы знаний агентов
├── mock_data_provider.py    # Mock провайдер для тестов
└── test_agents_integration.py # Интеграционные тесты
```

## 🧪 Тестирование

### **Запуск интеграционных тестов:**
```bash
python test_agents_integration.py
```

### **Последние результаты:**
- ✅ **100% success rate** для реализованных агентов
- ✅ **Lead Score: 100/100** (Hot Lead)
- ✅ **Sales Quality: Good** (45-85% close probability)
- ✅ **Proposal Value: 3.2M ₽/год**

## 🎯 Roadmap развития

### **Q4 2024:** ✅ MVP+ (6 агентов) - **ВЫПОЛНЕНО**
### **Q1 2025:** Management Layer (3 агента)
### **Q2 2025:** Operational Expansion (5 агентов) 
### **Q3 2025:** Enterprise Features & API
### **Q4 2025:** Production deployment

## 🔍 Для разработчиков

### **Создание нового агента:**
1. Наследовать от `BaseAgent` класса
2. Реализовать `process_task()` метод
3. Добавить knowledge base в `/knowledge/`
4. Обновить интеграционные тесты
5. Добавить в orchestrator workflow

### **Архитектурные принципы:**
- **Модульность** - каждый агент независим
- **Расширяемость** - легко добавлять новых агентов
- **Тестируемость** - полное покрытие тестами
- **Production-ready** - готовность к масштабированию

## 🚨 Важные команды

### **Git операции:**
```bash
git status                    # Проверка изменений
git add .                     # Добавить все изменения
git commit -m "message"       # Создать коммит
git push origin main          # Отправить в GitHub
```

### **Тестирование:**
```bash
python test_agents_integration.py  # Полный интеграционный тест
python -m pytest tests/           # Unit тесты (если настроены)
```

### **Проверка архитектуры:**
```bash
find agents/ -name "*.py" | wc -l  # Количество агентов
python -c "from agents.operational.lead_qualification import LeadQualificationAgent; print('OK')"
```

## 📞 Контакты

**Автор:** Andrew Popov  
**Email:** a.popov.gv@gmail.com  
**GitHub:** [Andrew821667](https://github.com/Andrew821667)  
**Репозиторий:** https://github.com/Andrew821667/ai-seo-architects

## 🔄 Интеграция с MCP

Проект готов к интеграции с **Model Context Protocol (MCP)**:
- ✅ Архитектурная подготовка завершена
- ✅ Factory integration готов
- 🔄 MCPDataProvider планируется к реализации

---

**Последнее обновление:** 2025-08-04  
**Версия документа:** 1.0  
**Claude Code совместимость:** ✅ Verified