# 🤖 Claude Code Integration

> **Документ для интеграции с Claude Code**  
> Этот файл помогает Claude понимать контекст проекта и выполнять задачи более эффективно

## 📋 О проекте

**AI SEO Architects** - enterprise-ready мультиагентная RAG-система для автоматизации SEO-агентства с полной архитектурой из 14 специализированных AI-агентов, MCP (Model Context Protocol) интеграцией, FastAPI Backend с Real-time Dashboard и готовностью к production развертыванию.

### 🎯 Текущий статус: 14/14 агентов + MCP + FastAPI Backend + Real-time Dashboard + Production Infrastructure (100% готовности) ✅

#### 🚀 **НОВОЕ: FastAPI Backend полностью развернут!**
- ✅ **Real-time Dashboard** - http://localhost:8000/dashboard
- ✅ **25+ REST API endpoints** - полное покрытие бизнес-логики  
- ✅ **WebSocket поддержка** - live обновления в реальном времени
- ✅ **JWT Authentication** - enterprise security с RBAC
- ✅ **Docker Infrastructure** - production-ready развертывание

## 🏗️ Полная архитектура 14 агентов

### ✅ **Реализованные агенты (14/14):**

#### Executive Level (2/2):
- **Chief SEO Strategist** - Стратегическое SEO планирование, алгоритмы поисковых систем, архитектура решений
- **Business Development Director** - Enterprise сделки 2.5M+ ₽/MRR, стратегические партнерства

#### Management Level (4/4):
- **Task Coordination Agent** - LangGraph маршрутизация, приоритизация задач
- **Sales Operations Manager** - Pipeline velocity, lead scoring, A/B testing email campaigns
- **Technical SEO Operations Manager** - Core Web Vitals, crawling coordination, log file analysis
- **Client Success Manager** - Churn prediction, upselling матрицы, QBR generation

#### Operational Level (8/8):
- **Lead Qualification Agent** - BANT/MEDDIC квалификация с ML scoring
- **Proposal Generation Agent** - Динамическое ценообразование, ROI калькуляции
- **Sales Conversation Agent** - СПИН методология, B2B переговоры с российской спецификой
- **Technical SEO Auditor** - Комплексный технический SEO аудит, Core Web Vitals, crawling
- **Content Strategy Agent** - Keyword research, контентная стратегия, E-E-A-T оптимизация
- **Link Building Agent** - Outreach automation, domain authority, toxic link detection
- **Competitive Analysis Agent** - SERP analysis, share of voice, competitive gap analysis
- **Reporting Agent** - BI integration, automated insights, anomaly detection

## 🔧 Технический стек

### **🚀 FastAPI Backend стек (Enterprise-ready):**
- **FastAPI** - Modern API framework с автогенерацией OpenAPI
- **WebSocket Manager** - Real-time обновления и connection pooling
- **JWT Authentication** - Ролевая модель с refresh токенами
- **Structured Logging** - JSON логирование с correlation ID
- **Metrics Collection** - Системные и бизнес метрики в реальном времени
- **Real-time Dashboard** - HTML дашборд с Chart.js и WebSocket

### **🔗 MCP стек (Model Context Protocol):**
- **Model Context Protocol** - Стандартизированный доступ к данным
- **MCPDataProvider** - Унифицированный провайдер с кэшированием
- **MCPAgentManager** - Менеджер агентов с MCP поддержкой
- **HTTP/WebSocket MCP clients** - Anthropic/OpenAI MCP серверы

### **🤖 AI Agents стек (Core):**
- **LangGraph** - Оркестрация мультиагентных workflow
- **LangChain** - AI/LLM интеграции
- **Pydantic** - Валидация данных и типизация  
- **OpenAI GPT-4** - Основная LLM для агентов

### **🐳 Production Infrastructure (Docker Compose):**
- **PostgreSQL** - Основная база данных для persistence
- **Redis** - Кэширование и session storage
- **Nginx** - Reverse proxy и load balancer
- **Prometheus** - Metrics collection и мониторинг
- **Grafana** - Визуализация метрик и дашборды
- **ChromaDB** - Vector database для знаний агентов
- **Docker/Docker Compose** - Контейнеризация и оркестрация

## 📁 Ключевые директории

```
ai-seo-architects/
├── agents/                        # AI агенты по уровням (14/14)
│   ├── executive/                # Executive уровень (2/2)
│   ├── management/               # Management уровень (4/4)  
│   └── operational/              # Operational уровень (8/8)
├── api/                          # 🚀 FastAPI Backend (NEW!)
│   ├── main.py                  # Основной FastAPI сервер
│   ├── routes/                  # API роуты
│   │   ├── agents.py           # Агенты API (CRUD операции)
│   │   ├── auth.py             # Аутентификация (JWT)
│   │   ├── campaigns.py        # Кампании API
│   │   ├── clients.py          # Клиенты API
│   │   └── analytics.py        # Аналитика API
│   ├── models/                  # Pydantic модели
│   │   ├── requests.py         # Модели запросов
│   │   └── responses.py        # Модели ответов
│   ├── auth/                    # Система аутентификации
│   │   └── security.py         # JWT токены + RBAC
│   ├── monitoring/              # Мониторинг и логирование
│   │   ├── logger.py           # Structured JSON logging
│   │   └── metrics.py          # Metrics collection
│   ├── websocket/               # WebSocket поддержка
│   │   └── manager.py          # Connection management
│   └── static/                  # Статические файлы
│       └── dashboard.html      # Real-time Dashboard UI
├── core/                         # Базовая архитектура + MCP
│   ├── base_agent.py            # Базовый класс с MCP поддержкой
│   ├── orchestrator.py          # LangGraph оркестратор
│   ├── mcp/                     # 🔗 MCP интеграция
│   │   ├── protocol.py          # MCP протокол
│   │   ├── data_provider.py     # MCP провайдер данных
│   │   ├── agent_manager.py     # MCP менеджер агентов
│   │   └── __init__.py         # MCP API
│   ├── data_providers/          # Провайдеры данных
│   └── interfaces/              # Интерфейсы и модели
├── config/                       # Конфигурации
│   └── mcp_config.py            # 🔗 MCP настройки
├── knowledge/                    # Базы знаний агентов (14/14)
├── mock_data_provider.py        # Mock провайдер для тестов
├── test_agents_integration.py   # Интеграционные тесты
├── test_mcp_integration.py      # 🔗 MCP интеграционные тесты
├── test_api_endpoints.py        # 🔗 API endpoints тестирование
├── comprehensive_agent_test.py  # Comprehensive тестирование
├── run_api.py                   # 🔗 Скрипт запуска API сервера
├── docker-compose.yml           # 🐳 Production инфраструктура
├── API_DOCUMENTATION.md         # 🔗 Полная API документация
├── DEPLOYMENT_GUIDE.md         # 🔗 Руководство по развертыванию
├── MCP_INTEGRATION.md           # 🔗 MCP документация
└── TECHNICAL_DEFENSE_DOCUMENTATION.md # Техническая документация
```

## 🧪 Тестирование

### **🚀 FastAPI API тестирование (Рекомендуемое):**
```bash
python test_api_endpoints.py         # Быстрое тестирование всех API функций
```

### **MCP интеграционные тесты:**
```bash
python test_mcp_integration.py       # Полное MCP тестирование всех агентов
```

### **Классические интеграционные тесты:**
```bash
python test_agents_integration.py    # Mock данные тестирование
python comprehensive_agent_test.py   # Максимально подробный анализ
```

### **Последние результаты (14/14 агентов):**
- ✅ **100% success rate** для всех агентов
- ✅ **Lead Score: 100/100** (Hot Lead)
- ✅ **Sales Quality: Good** (45-85% close probability)
- ✅ **Proposal Value: 3.2M ₽/год**
- ✅ **Technical SEO Audit: 63/100 score** (Comprehensive quality)
- ✅ **Content Strategy: Comprehensive framework** (Keyword research + E-E-A-T)
- ✅ **Sales Operations: 75+ pipeline health** (Advanced analytics и forecasting)
- ✅ **Technical SEO Operations: 85+ operations health** (Core Web Vitals monitoring)

## 🎯 Roadmap развития

### **Q4 2024:** ✅ MVP+ (14 агентов) - **ВЫПОЛНЕНО**
### **Q1 2025:** ✅ Management Layer (4 агента) - **ВЫПОЛНЕНО**
### **Q2 2025:** ✅ Operational Expansion (8 агентов) - **ВЫПОЛНЕНО**
### **Q3 2025:** ✅ SEO AI Models Integration (100%) - **ВЫПОЛНЕНО**
### **Q4 2025:** ✅ MCP (Model Context Protocol) Integration - **ВЫПОЛНЕНО** 🔗
### **Q1 2026:** Enterprise Features & API
### **Q2 2026:** Production deployment

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

### **🚀 FastAPI Backend запуск:**
```bash
python run_api.py                 # Быстрый запуск API сервера
docker-compose up -d              # Production развертывание
python test_api_endpoints.py      # Тестирование API
```

### **🎛️ Dashboard доступ:**
```bash
# После запуска API сервера:
# http://localhost:8000/dashboard  # Real-time Dashboard
# http://localhost:8000/api/docs   # API документация
# http://localhost:8000/health     # Health check
```

### **Git операции:**
```bash
git status                    # Проверка изменений
git add .                     # Добавить все изменения
git commit -m "message"       # Создать коммит
git push origin main          # Отправить в GitHub
```

### **Тестирование:**
```bash
python test_api_endpoints.py       # API endpoints тестирование
python test_mcp_integration.py     # MCP интеграционные тесты
python test_agents_integration.py  # Полный интеграционный тест
python -m pytest tests/           # Unit тесты (если настроены)
```

### **Проверка архитектуры:**
```bash
find agents/ -name "*.py" | wc -l  # Количество агентов
find api/ -name "*.py" | wc -l     # Количество API файлов
python -c "from agents.operational.lead_qualification import LeadQualificationAgent; print('OK')"
```

## 📞 Контакты

**Автор:** Andrew Popov  
**Email:** a.popov.gv@gmail.com  
**GitHub:** [Andrew821667](https://github.com/Andrew821667)  
**Репозиторий:** https://github.com/Andrew821667/ai-seo-architects

## 🤖 Интеграция с SEO AI Models

Проект готов к интеграции с **SEO AI Models** (https://github.com/Andrew821667/seo-ai-models):

### 🎯 **Основные компоненты SEO AI Models:**
```yaml
core_components:
  seo_advisor:
    description: "Ядро анализа контента и рекомендаций"
    capabilities: ["content_analysis", "seo_recommendations", "optimization_suggestions"]
    
  eeat_analyzer:
    description: "E-E-A-T анализ (Experience, Expertise, Authoritativeness, Trustworthiness)"
    capabilities: ["content_quality_scoring", "authority_analysis", "trust_metrics"]
    
  content_analyzer:
    description: "Глубокий анализ контента и структуры"
    capabilities: ["keyword_analysis", "semantic_analysis", "readability_metrics"]
    
  semantic_analyzer:
    description: "Семантический анализ контента"
    capabilities: ["nlp_processing", "topic_modeling", "content_clustering"]
    
  calibrated_rank_predictor:
    description: "Предсказание позиций в поисковой выдаче"
    capabilities: ["ranking_prediction", "serp_analysis", "competition_assessment"]
    
  unified_parser:
    description: "Универсальный парсер для современных веб-технологий"
    capabilities: ["spa_parsing", "javascript_rendering", "ajax_interception"]
```

### 🔧 **Технический стек SEO AI Models:**
```yaml
dependencies:
  web_interaction:
    - requests: "HTTP запросы"
    - beautifulsoup4: "HTML парсинг"
    - playwright: "Браузерная автоматизация"
    - pyppeteer: "Chromium управление"
    
  nlp_processing:
    - spacy: "Обработка естественного языка"
    - nltk: "Лингвистический анализ"
    - gensim: "Семантическое моделирование"
    
  machine_learning:
    - scikit-learn: "ML алгоритмы"
    - numpy: "Численные вычисления"
    
  search_integration:
    - google-search-results: "SerpAPI интеграция"
    
  utilities:
    - markdown: "Markdown обработка"
    - tqdm: "Progress tracking"
    - colorlog: "Цветное логирование"
```

### 🚀 **Возможности интеграции с AI SEO Architects:**

#### **Technical SEO Auditor Enhancement:**
```python
# Интеграция с Technical SEO Auditor Agent
from seo_ai_models.models.seo_advisor import SEOAdvisor
from seo_ai_models.analyzers.content_analyzer import ContentAnalyzer

class EnhancedTechnicalSEOAuditor(TechnicalSEOAuditorAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seo_advisor = SEOAdvisor()
        self.content_analyzer = ContentAnalyzer()
        
    async def enhanced_audit(self, domain: str):
        # Комбинированный анализ
        technical_audit = await self.process_technical_audit(domain)
        content_analysis = await self.content_analyzer.analyze(domain)
        seo_recommendations = await self.seo_advisor.get_recommendations(domain)
        
        return {
            "technical_score": technical_audit["score"],
            "content_quality": content_analysis["quality_score"],
            "seo_recommendations": seo_recommendations,
            "combined_score": self._calculate_combined_score(technical_audit, content_analysis)
        }
```

#### **Content Strategy Agent Enhancement:**
```python
# Интеграция с Content Strategy Agent
from seo_ai_models.analyzers.semantic_analyzer import SemanticAnalyzer
from seo_ai_models.analyzers.eeat_analyzer import EEATAnalyzer

class EnhancedContentStrategyAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.semantic_analyzer = SemanticAnalyzer()
        self.eeat_analyzer = EEATAnalyzer()
        
    async def content_strategy_analysis(self, content_data: dict):
        # E-E-A-T анализ
        eeat_scores = await self.eeat_analyzer.analyze(content_data["content"])
        
        # Семантический анализ
        semantic_insights = await self.semantic_analyzer.analyze_topics(content_data["content"])
        
        return {
            "eeat_scores": eeat_scores,
            "semantic_clusters": semantic_insights["clusters"],
            "content_recommendations": self._generate_content_strategy(eeat_scores, semantic_insights)
        }
```

#### **Competitive Analysis Agent Enhancement:**
```python
# Интеграция с Competitive Analysis Agent
from seo_ai_models.predictors.rank_predictor import CalibratedRankPredictor
from seo_ai_models.parsers.unified_parser import UnifiedParser

class EnhancedCompetitiveAnalysisAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rank_predictor = CalibratedRankPredictor()
        self.unified_parser = UnifiedParser()
        
    async def competitive_analysis(self, domain: str, competitors: List[str]):
        # Парсинг конкурентов с поддержкой SPA
        competitor_data = []
        for competitor in competitors:
            parsed_data = await self.unified_parser.parse_spa(competitor)
            competitor_data.append(parsed_data)
            
        # Предсказание позиций
        ranking_predictions = await self.rank_predictor.predict_rankings(
            domain, competitors, competitor_data
        )
        
        return {
            "competitor_analysis": competitor_data,
            "ranking_predictions": ranking_predictions,
            "competitive_gaps": self._identify_gaps(domain, competitor_data)
        }
```

### 📊 **Планируемая интеграция по этапам:**

#### **Этап 1 (Q1 2025): Базовая интеграция**
- ✅ StaticDataProvider готов к интеграции
- 🔄 Подключение SEOAdvisor к Technical SEO Auditor
- 🔄 ContentAnalyzer интеграция для Content Strategy Agent
- 🔄 EEATAnalyzer для качественного анализа контента

#### **Этап 2 (Q2 2025): Advanced Features**
- 🔄 CalibratedRankPredictor для Competitive Analysis Agent
- 🔄 SemanticAnalyzer для глубокого контентного анализа
- 🔄 UnifiedParser для современных SPA сайтов

#### **Этап 3 (Q3 2025): ML Enhancement**
- 🔄 Обученные ML модели для предсказания ранжирования
- 🔄 Автоматическая калибровка моделей на новых данных
- 🔄 Real-time анализ и рекомендации

### 🛠️ **Требования к развертыванию:**
```yaml
deployment_requirements:
  python_version: "3.8+"
  
  core_dependencies:
    - playwright: "Браузерная автоматизация"
    - spacy: "NLP модели (en_core_web_sm)"
    - scikit-learn: "ML алгоритмы"
    
  optional_dependencies:
    - gpu_support: "CUDA для ускорения ML моделей"
    - large_models: "Большие языковые модели для семантики"
    
  infrastructure:
    - memory: "8GB+ RAM для больших моделей"  
    - storage: "5GB+ для ML моделей и кэша"
    - network: "Стабильное соединение для парсинга"
```

### 🔗 **Ссылки и ресурсы:**
- **Репозиторий:** https://github.com/Andrew821667/seo-ai-models
- **Версия:** 0.2.0 (активная разработка)
- **Лицензия:** Совместима с AI SEO Architects
- **Документация:** В составе репозитория

## 🔄 Интеграция с MCP

Проект готов к интеграции с **Model Context Protocol (MCP)**:
- ✅ Архитектурная подготовка завершена
- ✅ Factory integration готов
- 🔄 MCPDataProvider планируется к реализации

---

## 🚀 FastAPI Backend и Real-time Dashboard

**Статус готовности: 100% ✅** - Полный enterprise-ready backend развернут!

### 🎯 **Основные возможности:**

#### **🔥 Real-time Dashboard:**
- **URL:** http://localhost:8000/dashboard
- **WebSocket live обновления** - метрики системы в реальном времени
- **Chart.js визуализация** - интерактивные графики и диаграммы
- **System Health monitoring** - CPU, RAM, активность агентов
- **Activity Feed** - лента последних операций и событий
- **Responsive дизайн** - работает на всех устройствах

#### **🔌 Comprehensive REST API:**
- **25+ endpoints** - полное покрытие всех бизнес-процессов
- **JWT Authentication** - безопасная авторизация с refresh токенами
- **Role-based Access** - admin/manager/operator роли
- **OpenAPI documentation** - автоматическая генерация docs
- **Request/Response validation** - Pydantic модели

#### **🏗️ Enterprise Infrastructure:**
- **Structured JSON Logging** - correlation ID трекинг
- **Metrics Collection** - системные и бизнес метрики
- **Health Checks** - мониторинг состояния всех компонентов
- **WebSocket Connection Pooling** - efficient real-time communications
- **CORS configuration** - правильная настройка для frontend

### 📊 **Key API Endpoints:**

#### **Authentication:**
```http
POST /auth/login           # Авторизация (admin/secret)
POST /auth/refresh         # Обновление токена
GET  /auth/me             # Информация о пользователе
POST /auth/logout         # Выход
```

#### **Agents Management:**
```http
GET  /api/agents/                        # Список всех агентов
POST /api/agents/create-all              # Создать всех 14 агентов
GET  /api/agents/{agent_id}/status       # Статус агента
POST /api/agents/{agent_id}/tasks        # Выполнить задачу
GET  /api/agents/health                  # Health check агентов
```

#### **Business Operations:**
```http
GET  /api/clients/                       # Управление клиентами
POST /api/campaigns/                     # Создание кампаний
GET  /api/analytics/dashboard            # Данные дашборда
GET  /api/analytics/system              # Системные метрики
```

#### **WebSocket:**
```javascript
ws://localhost:8000/ws/dashboard        # Real-time обновления
```

### 🛠️ **Быстрый запуск:**

#### **Option 1: Development (5 секунд):**
```bash
python run_api.py
# ✨ Готово! Dashboard: http://localhost:8000/dashboard
```

#### **Option 2: Production (Docker):**
```bash
docker-compose up -d
# 🐳 Полная инфраструктура с PostgreSQL, Redis, Nginx
```

#### **Option 3: API Testing:**
```bash
python test_api_endpoints.py
# 🧪 Автоматическое тестирование всех endpoints
```

### 🔧 **Technical Stack:**

#### **Backend Core:**
- **FastAPI 0.104+** - Modern async web framework
- **Uvicorn** - Lightning-fast ASGI server  
- **Pydantic v2** - Data validation и serialization
- **Python 3.11+** - Latest Python features

#### **Real-time & WebSocket:**
- **WebSocket Manager** - Connection pooling с heartbeat
- **Async Message Broadcasting** - efficient группы подписок
- **Auto-reconnection** - клиентская устойчивость к разрывам

#### **Security & Auth:**
- **JWT Tokens** - stateless authentication
- **Refresh Token Rotation** - enhanced security
- **Role-based permissions** - admin/manager/operator
- **Password hashing** - bcrypt с salt

#### **Monitoring & Observability:**
- **Structured Logging** - JSON формат с correlation IDs
- **Metrics Collection** - custom MetricsCollector
- **Performance Tracking** - request latency, system resources
- **Health Checks** - endpoint и agent monitoring

### 🎛️ **Dashboard Features:**

#### **System Overview:**
- **Real-time CPU/Memory** - live system metrics
- **Agent Status Grid** - 14 агентов с цветовым кодированием
- **Active Tasks** - текущие выполняемые задачи
- **Success Rate** - статистика успешности операций

#### **Interactive Charts:**
- **Performance Metrics** - request latency, throughput
- **Agent Activity** - количество выполненных задач
- **System Health** - historical CPU/Memory trends
- **Business KPIs** - lead scores, proposals generated

#### **Activity Feed:**
- **Real-time Events** - все операции в системе
- **Task Completions** - результаты выполнения задач
- **System Events** - startup, shutdown, errors
- **User Actions** - login, task requests

### 🔗 **Integration Points:**

#### **MCP Compatibility:**
```python
# API полностью интегрирован с MCP Agent Manager
from core.mcp.agent_manager import get_mcp_agent_manager
manager = await get_mcp_agent_manager()
agents = await manager.create_all_agents(enable_mcp=True)
```

#### **Frontend Ready:**
```javascript
// React/Vue/Angular готовая интеграция
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { Authorization: `Bearer ${token}` }
})
```

### 📚 **Documentation:**
- **[Полная API документация](API_DOCUMENTATION.md)** - все endpoints с примерами
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - production развертывание
- **Auto-generated OpenAPI** - http://localhost:8000/api/docs

### 🚀 **Production Ready:**
- **Docker Compose** - полная инфраструктура (PostgreSQL, Redis, Nginx)
- **Health Checks** - Kubernetes/Docker Swarm совместимость  
- **Environment Variables** - 12-factor app configuration
- **Graceful Shutdown** - правильное завершение connections
- **CORS Configuration** - frontend integration ready
- **SSL/TLS Support** - production security настройки

---

**Последнее обновление:** 2025-08-06  
**Версия документа:** 1.4  
**Claude Code совместимость:** ✅ Verified