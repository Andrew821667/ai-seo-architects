# 🤖 Claude Code Integration

> **Документ для интеграции с Claude Code**  
> Этот файл помогает Claude понимать контекст проекта и выполнять задачи более эффективно

## 📋 О проекте

**AI SEO Architects** - мультиагентная RAG-система для автоматизации SEO-агентства с архитектурой из 14 специализированных AI-агентов.

### 🎯 Текущий статус: 5/14 агентов (35.7% готовности)

## 🏗️ Архитектура агентов

### ✅ **Реализованные агенты (5/14):**
- **Business Development Director** (Executive) - Стратегический анализ enterprise клиентов
- **Task Coordination Agent** (Management) - Маршрутизация задач и приоритизация
- **Lead Qualification Agent** (Operational) - BANT/MEDDIC квалификация лидов
- **Proposal Generation Agent** (Operational) - Динамическое ценообразование и ROI
- **Sales Conversation Agent** (Operational) - СПИН методология и B2B переговоры

### 🔄 **Планируемые агенты (9/14):**
#### Executive Level:
- **Chief SEO Strategist** - Главный SEO стратег и архитектор решений

#### Management Level:
- **Sales Operations Manager** - Управление воронкой продаж
- **Technical SEO Operations Manager** - Управление техническими SEO проектами  
- **Client Success Manager** - Онбординг и удержание клиентов

#### Operational Level:
- **Technical SEO Auditor** - Технический аудит сайтов
- **Content Strategy Agent** - Контент планирование и семантика
- **Link Building Agent** - Линкбилдинг стратегии и outreach
- **Competitive Analysis Agent** - Анализ конкурентов и gap analysis
- **Reporting Agent** - Автоматические отчеты и KPI tracking

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
│   ├── executive/            # Executive уровень (1/2)
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

### **Q4 2024:** ✅ MVP (5 агентов) - **ВЫПОЛНЕНО**
### **Q1 2025:** Management Layer (4 агента)
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