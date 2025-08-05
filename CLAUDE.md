# 🤖 Claude Code Integration

> **Документ для интеграции с Claude Code**  
> Этот файл помогает Claude понимать контекст проекта и выполнять задачи более эффективно

## 📋 О проекте

**AI SEO Architects** - enterprise-ready мультиагентная RAG-система для автоматизации SEO-агентства с полной архитектурой из 14 специализированных AI-агентов, построенная на LangGraph и готовая к production развертыванию.

### 🎯 Текущий статус: 8/14 агентов (57% готовности)

## 🏗️ Полная архитектура 14 агентов

### ✅ **Реализованные агенты (8/14):**

#### Executive Level (2/2):
- **Chief SEO Strategist** - Стратегическое SEO планирование, алгоритмы поисковых систем, архитектура решений
- **Business Development Director** - Enterprise сделки 2.5M+ ₽/MRR, стратегические партнерства

#### Management Level (1/4):
- **Task Coordination Agent** - LangGraph маршрутизация, приоритизация задач

#### Operational Level (5/8):
- **Lead Qualification Agent** - BANT/MEDDIC квалификация с ML scoring
- **Proposal Generation Agent** - Динамическое ценообразование, ROI калькуляции
- **Sales Conversation Agent** - СПИН методология, B2B переговоры с российской спецификой
- **Technical SEO Auditor** - Комплексный технический SEO аудит, Core Web Vitals, crawling
- **Content Strategy Agent** - Keyword research, контентная стратегия, E-E-A-T оптимизация

### 🔄 **Планируемые агенты (6/14):**

#### Management Level (3/4):
- **Sales Operations Manager** - Pipeline velocity, lead scoring, A/B testing email campaigns
- **Technical SEO Operations Manager** - Core Web Vitals, crawling coordination, log file analysis
- **Client Success Manager** - Churn prediction, upselling матрицы, QBR generation

#### Operational Level (3/8):
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
│   └── operational/          # Operational уровень (5/8)
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

### **Последние результаты (8/14 агентов):**
- ✅ **100% success rate** для реализованных агентов
- ✅ **Lead Score: 100/100** (Hot Lead)
- ✅ **Sales Quality: Good** (45-85% close probability)
- ✅ **Proposal Value: 3.2M ₽/год**
- ✅ **Technical SEO Audit: 63/100 score** (Comprehensive quality)
- ✅ **Content Strategy: Comprehensive framework** (Keyword research + E-E-A-T)

## 🎯 Roadmap развития

### **Q4 2024:** ✅ MVP+ (8 агентов) - **ВЫПОЛНЕНО**
### **Q1 2025:** Management Layer (3 агента)
### **Q2 2025:** Operational Expansion (3 агента) 
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

**Последнее обновление:** 2025-08-05  
**Версия документа:** 1.1  
**Claude Code совместимость:** ✅ Verified