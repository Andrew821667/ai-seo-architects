# 🤖 AI SEO Architects - Справочник функций агентов

**Проект:** AI SEO Architects - Мультиагентная RAG система  
**Дата:** Август 2025  
**Автор:** Andrew Popov  
**Цель:** Полное описание технических и бизнесовых функций всех 14 агентов  
**Рынок:** Адаптировано под российский рынок и законодательство

## 🇷🇺 **Российская специфика системы**

### **Ключевые адаптации для российского рынка:**
- **Валюта и налоги:** Все расчеты в рублях с учетом НДС 20%
- **Законодательство:** Соответствие 44-ФЗ, работа с госзаказами
- **Поисковые системы:** Приоритет Яндекса (55% рынка) + Google (44%)
- **Платежи:** Безналичный расчет, ЭДО, интеграция с 1С
- **CRM системы:** amoCRM, Битрикс24, МойСклад как основные
- **SEO инструменты:** Serpstat, Rush Analytics, Топвизор вместо западных
- **Аналитика:** Яндекс.Метрика + Roistat/Calltouch для сквозной аналитики

---

## 📋 Общая архитектура

AI SEO Architects включает **14 специализированных агентов**, организованных в **3-уровневую иерархию**:

- **Executive Level (2 агента)** - стратегическое планирование и принятие решений
- **Management Level (4 агента)** - координация и управление процессами  
- **Operational Level (8 агентов)** - выполнение конкретных задач

---

## 👑 EXECUTIVE LEVEL (2 агента)

### 1. Chief SEO Strategist
**Роль:** Главный стратег SEO, архитектор решений

#### 🔧 Технические функции:
- `analyze_seo_landscape()` - анализ SEO ландшафта и алгоритмов поисковых систем
- `create_strategic_framework()` - создание стратегических SEO фреймворков
- `evaluate_technical_complexity()` - оценка технической сложности проектов
- `design_seo_architecture()` - проектирование SEO архитектуры сайтов
- `assess_keyword_strategy()` - глубокий анализ ключевых слов и семантики
- `monitor_algorithm_changes()` - отслеживание изменений поисковых алгоритмов
- `calculate_seo_roi()` - расчет ROI от SEO инвестиций
- `audit_enterprise_seo()` - комплексный SEO аудит для enterprise клиентов

#### 💼 Бизнесовые функции:
- `develop_market_positioning()` - разработка позиционирования на рынке
- `create_competitive_advantage()` - создание конкурентных преимуществ через SEO
- `plan_budget_allocation()` - планирование бюджета на SEO активности
- `forecast_growth_metrics()` - прогнозирование метрик роста трафика
- `identify_revenue_opportunities()` - выявление возможностей увеличения доходов
- `strategic_partnership_planning()` - планирование стратегических партнерств
- `enterprise_seo_consulting()` - консультирование крупных клиентов
- `board_presentation_preparation()` - подготовка презентаций для совета директоров

**Пороги принятия решений:**
- Strategic Keywords Threshold: 50,000+ ключевых слов
- Enterprise Budget Threshold: 15M+ ₽/год
- Board Approval Threshold: проекты 50M+ ₽

---

### 2. Business Development Director
**Роль:** Директор по развитию бизнеса, стратегические продажи

#### 🔧 Технические функции:
- `assess_enterprise_requirements()` - оценка технических требований enterprise клиентов
- `analyze_deal_complexity()` - анализ сложности сделок и технических решений
- `evaluate_implementation_feasibility()` - оценка возможности реализации проектов
- `calculate_project_resources()` - расчет необходимых ресурсов для проектов
- `design_custom_solutions()` - проектирование кастомных решений
- `integration_planning()` - планирование интеграций с существующими системами
- `technical_due_diligence()` - техническая проверка перед крупными сделками
- `scalability_assessment()` - оценка масштабируемости решений

#### 💼 Бизнесовые функции:
- `identify_enterprise_prospects()` - выявление enterprise перспектив
- `develop_partnership_strategies()` - разработка стратегий партнерства
- `negotiate_enterprise_contracts()` - ведение переговоров по крупным контрактам
- `manage_strategic_accounts()` - управление стратегическими клиентами
- `create_revenue_forecasts()` - создание прогнозов доходов
- `plan_market_expansion()` - планирование расширения на новые рынки
- `build_executive_relationships()` - построение отношений с топ-менеджментом
- `develop_pricing_strategies()` - разработка ценовых стратегий

**Пороги принятия решений:**
- Minimum Enterprise Deal: 2,500,000 ₽/месяц
- Strategic Partnership Threshold: 10M+ ₽/год
- CEO Approval Threshold: сделки 25M+ ₽

---

## ⚙️ MANAGEMENT LEVEL (4 агента)

### 3. Task Coordination Agent
**Роль:** Координатор задач, маршрутизация workflow

#### 🔧 Технические функции:
- `route_tasks_efficiently()` - эффективная маршрутизация задач между агентами
- `manage_workflow_dependencies()` - управление зависимостями в workflow
- `optimize_resource_allocation()` - оптимизация распределения ресурсов
- `monitor_task_progress()` - мониторинг прогресса выполнения задач
- `handle_error_recovery()` - обработка ошибок и восстановление workflow
- `implement_priority_queues()` - реализация очередей приоритетов
- `coordinate_parallel_processing()` - координация параллельной обработки
- `manage_task_scheduling()` - управление расписанием задач

#### 💼 Бизнесовые функции:
- `prioritize_client_requests()` - приоритизация запросов клиентов
- `ensure_deadline_compliance()` - обеспечение соблюдения дедлайнов
- `optimize_team_productivity()` - оптимизация продуктивности команды
- `manage_client_expectations()` - управление ожиданиями клиентов
- `coordinate_cross_team_projects()` - координация межкомандных проектов
- `track_project_milestones()` - отслеживание этапов проектов
- `manage_workload_distribution()` - управление распределением нагрузки
- `ensure_quality_standards()` - обеспечение стандартов качества

---

### 4. Sales Operations Manager
**Роль:** Менеджер по операциям продаж, аналитика воронки

#### 🔧 Технические функции:
- `analyze_pipeline_velocity()` - анализ скорости движения по воронке продаж
- `implement_lead_scoring()` - реализация системы скоринга лидов
- `optimize_conversion_funnels()` - оптимизация воронок конверсии
- `automate_sales_processes()` - автоматизация процессов продаж
- `integrate_crm_systems()` - интеграция CRM систем
- `track_sales_metrics()` - отслеживание метрик продаж
- `implement_ab_testing()` - реализация A/B тестирования в продажах
- `analyze_customer_behavior()` - анализ поведения клиентов

#### 💼 Бизнесовые функции:
- `forecast_sales_revenue()` - прогнозирование доходов от продаж
- `optimize_sales_cycles()` - оптимизация циклов продаж
- `manage_sales_quotas()` - управление планами продаж
- `develop_pricing_models()` - разработка ценовых моделей
- `analyze_market_trends()` - анализ трендов рынка
- `improve_win_rates()` - улучшение показателей успешности сделок
- `manage_sales_territories()` - управление территориями продаж
- `optimize_commission_structures()` - оптимизация структур комиссий

---

### 5. Technical SEO Operations Manager
**Роль:** Менеджер технических SEO операций, координация аудитов

#### 🔧 Технические функции:
- `coordinate_technical_audits()` - координация технических SEO аудитов
- `monitor_core_web_vitals()` - мониторинг Core Web Vitals
- `manage_crawling_budgets()` - управление краулинговыми бюджетами
- `optimize_site_performance()` - оптимизация производительности сайтов
- `implement_structured_data()` - внедрение структурированных данных
- `manage_indexing_strategies()` - управление стратегиями индексации
- `coordinate_log_analysis()` - координация анализа лог-файлов
- `monitor_technical_health()` - мониторинг технического здоровья сайтов

#### 💼 Бизнесовые функции:
- `prioritize_technical_fixes()` - приоритизация технических исправлений
- `manage_technical_resources()` - управление техническими ресурсами
- `coordinate_client_implementations()` - координация внедрений у клиентов
- `report_technical_progress()` - отчетность по техническому прогрессу
- `manage_technical_budgets()` - управление техническими бюджетами
- `ensure_compliance_standards()` - обеспечение соответствия стандартам
- `coordinate_emergency_fixes()` - координация экстренных исправлений
- `plan_technical_roadmaps()` - планирование технических дорожных карт

---

### 6. Client Success Manager
**Роль:** Менеджер успеха клиентов, retention и upselling

#### 🔧 Технические функции:
- `monitor_client_metrics()` - мониторинг метрик клиентов
- `implement_health_scoring()` - реализация системы оценки здоровья аккаунтов
- `automate_success_workflows()` - автоматизация workflow успеха клиентов
- `track_product_usage()` - отслеживание использования продуктов
- `analyze_churn_patterns()` - анализ паттернов оттока клиентов
- `implement_early_warning_systems()` - внедрение систем раннего предупреждения
- `optimize_onboarding_processes()` - оптимизация процессов онбординга
- `measure_customer_satisfaction()` - измерение удовлетворенности клиентов

#### 💼 Бизнесовые функции:
- `develop_retention_strategies()` - разработка стратегий удержания
- `identify_upselling_opportunities()` - выявление возможностей для upselling
- `manage_client_relationships()` - управление отношениями с клиентами
- `conduct_business_reviews()` - проведение бизнес-ревью с клиентами
- `plan_account_growth()` - планирование роста аккаунтов
- `manage_contract_renewals()` - управление продлением контрактов
- `coordinate_expansion_sales()` - координация продаж расширений
- `ensure_customer_advocacy()` - обеспечение адвокации клиентов

---

## 🔧 OPERATIONAL LEVEL (8 агентов)

### 7. Lead Qualification Agent
**Роль:** Квалификация лидов, BANT анализ

#### 🔧 Технические функции:
- `implement_bant_scoring()` - реализация BANT скоринга (Budget, Authority, Need, Timeline)
- `analyze_lead_sources()` - анализ источников лидов
- `implement_meddic_framework()` - применение MEDDIC методологии
- `automate_qualification_workflows()` - автоматизация workflow квалификации
- `integrate_lead_intelligence()` - интеграция данных о лидах
- `track_qualification_metrics()` - отслеживание метрик квалификации
- `implement_predictive_scoring()` - внедрение предиктивного скоринга
- `optimize_qualification_processes()` - оптимизация процессов квалификации

#### 💼 Бизнесовые функции:
- `assess_budget_authority()` - оценка бюджета и полномочий лида
- `identify_decision_makers()` - выявление лиц, принимающих решения
- `evaluate_business_needs()` - оценка бизнес-потребностей
- `determine_purchase_timeline()` - определение временных рамок покупки
- `prioritize_sales_efforts()` - приоритизация усилий продаж
- `qualify_enterprise_prospects()` - квалификация enterprise перспектив
- `assess_competitive_landscape()` - оценка конкурентной среды клиента
- `evaluate_fit_score()` - оценка соответствия клиента продукту

**Квалификационные критерии:**
- Budget Range: 500,000₽ - 50,000,000₽/год
- Authority Levels: Manager, Director, VP, C-Level
- Need Assessment: Low, Medium, High, Critical
- Timeline: Immediate, 3 months, 6 months, 12+ months

---

### 8. Sales Conversation Agent  
**Роль:** Ведение продажных разговоров, СПИН методология

#### 🔧 Технические функции:
- `implement_spin_methodology()` - применение СПИН методологии (Situation, Problem, Implication, Need-payoff)
- `analyze_conversation_patterns()` - анализ паттернов разговоров
- `optimize_objection_handling()` - оптимизация работы с возражениями
- `track_conversation_metrics()` - отслеживание метрик разговоров
- `implement_conversation_intelligence()` - внедрение анализа разговоров
- `automate_follow_up_sequences()` - автоматизация последующих контактов
- `analyze_sentiment_patterns()` - анализ эмоциональных паттернов
- `optimize_closing_techniques()` - оптимизация техник закрытия сделок

#### 💼 Бизнесовые функции:
- `conduct_discovery_calls()` - проведение звонков-исследований
- `identify_business_pain_points()` - выявление болевых точек бизнеса
- `present_value_propositions()` - презентация ценностных предложений
- `handle_pricing_discussions()` - обсуждение ценообразования
- `negotiate_contract_terms()` - переговоры по условиям контрактов
- `manage_sales_objections()` - работа с возражениями в продажах
- `build_rapport_with_prospects()` - построение раппорта с перспективами
- `guide_decision_making_process()` - руководство процессом принятия решений

**Методологии:**
- **СПИН:** Ситуация → Проблема → Извлечение → Выгода
- **Валюта:** ₽ (российский рынок)
- **Российская специфика:** 44-ФЗ, работа с госзаказами, НДС учет
- **Типы возражений:** Цена, Полномочия, Потребность, Доверие, Сроки
- **Техники закрытия:** Предположительное, Альтернативное, Срочность
- **Интеграции:** amoCRM, Битрикс24, Calltouch для учета звонков

---

### 9. Proposal Generation Agent
**Роль:** Генерация коммерческих предложений, ценообразование

#### 🔧 Технические функции:
- `implement_dynamic_pricing()` - реализация динамического ценообразования
- `calculate_roi_projections()` - расчет прогнозов ROI
- `generate_custom_proposals()` - генерация кастомных предложений
- `optimize_pricing_models()` - оптимизация ценовых моделей
- `implement_value_based_pricing()` - внедрение ценообразования на основе ценности
- `automate_proposal_generation()` - автоматизация генерации предложений
- `track_proposal_performance()` - отслеживание эффективности предложений
- `analyze_competitive_pricing()` - анализ конкурентного ценообразования

#### 💼 Бизнесовые функции:
- `create_executive_summaries()` - создание executive summary
- `develop_implementation_timelines()` - разработка временных планов внедрения
- `calculate_business_impact()` - расчет влияния на бизнес
- `present_investment_options()` - презентация вариантов инвестиций
- `customize_service_packages()` - кастомизация пакетов услуг
- `negotiate_payment_terms()` - переговоры по условиям оплаты
- `create_risk_assessments()` - создание оценок рисков
- `develop_success_metrics()` - разработка метрик успеха

**Ценовые модели (российский рынок):**
- **Fixed Price:** фиксированная стоимость проекта с НДС 20%
- **Ретейнер:** ежемесячный абонент (популярно в РФ)
- **Performance-based:** оплата по KPI (с учетом валютного законодательства)
- **Hybrid:** комбинированная модель (фикс + бонус за результат)
- **Российская специфика:** работа через ИП/ООО, безналичный расчет, ЭДО

---

### 10. Technical SEO Auditor
**Роль:** Технический SEO аудитор, анализ сайтов

#### 🔧 Технические функции:
- `analyze_site_architecture()` - анализ архитектуры сайта
- `audit_core_web_vitals()` - аудит Core Web Vitals (LCP, FID, CLS)
- `check_indexing_status()` - проверка статуса индексации
- `analyze_crawlability()` - анализ краулинга сайта
- `audit_structured_data()` - аудит структурированных данных
- `check_mobile_optimization()` - проверка мобильной оптимизации
- `analyze_page_speed()` - анализ скорости загрузки страниц
- `audit_internal_linking()` - аудит внутренней перелинковки
- `check_duplicate_content()` - проверка дублированного контента
- `analyze_log_files()` - анализ лог-файлов сервера

#### 💼 Бизнесовые функции:
- `prioritize_technical_issues()` - приоритизация технических проблем
- `estimate_implementation_costs()` - оценка стоимости внедрения исправлений
- `calculate_traffic_impact()` - расчет влияния на трафик
- `create_technical_roadmaps()` - создание технических дорожных карт
- `report_competitive_gaps()` - отчет о конкурентных пробелах
- `assess_business_impact()` - оценка влияния на бизнес
- `recommend_technology_stack()` - рекомендации по технологическому стеку
- `plan_migration_strategies()` - планирование стратегий миграции

**Аудит категории:**
- Technical Health: общее техническое здоровье
- Performance: производительность и скорость
- Mobile Experience: мобильный опыт
- Indexing & Crawling: индексация и краулинг
- Content Quality: качество контента
- Security & HTTPS: безопасность

---

### 11. Content Strategy Agent
**Роль:** Стратегия контента, keyword research

#### 🔧 Технические функции:
- `conduct_keyword_research()` - проведение исследования ключевых слов
- `analyze_content_gaps()` - анализ пробелов в контенте
- `implement_topic_clustering()` - реализация кластеризации тем
- `optimize_content_structure()` - оптимизация структуры контента
- `analyze_search_intent()` - анализ поискового намерения
- `implement_eeat_optimization()` - внедрение E-E-A-T оптимизации
- `track_content_performance()` - отслеживание эффективности контента
- `optimize_content_distribution()` - оптимизация распространения контента

#### 💼 Бизнесовые функции:
- `develop_content_calendars()` - разработка контент-календарей
- `create_editorial_guidelines()` - создание редакционных руководств
- `plan_content_budgets()` - планирование бюджетов на контент
- `identify_content_opportunities()` - выявление возможностей для контента
- `manage_content_teams()` - управление командами контента
- `measure_content_roi()` - измерение ROI контента
- `develop_brand_voice()` - разработка голоса бренда
- `plan_content_localization()` - планирование локализации контента

**E-E-A-T Framework:**
- Experience: опыт автора/бренда
- Expertise: экспертность в теме
- Authoritativeness: авторитетность источника
- Trustworthiness: доверие к контенту

---

### 12. Link Building Agent
**Роль:** Построение ссылочной массы, outreach

#### 🔧 Технические функции:
- `analyze_backlink_profiles()` - анализ профилей обратных ссылок
- `implement_outreach_automation()` - автоматизация outreach кампаний
- `track_domain_authority()` - отслеживание Domain Authority
- `detect_toxic_links()` - обнаружение токсичных ссылок
- `optimize_anchor_text_distribution()` - оптимизация распределения анкорных текстов
- `implement_link_prospecting()` - внедрение поиска ссылочных возможностей
- `track_link_velocity()` - отслеживание скорости получения ссылок
- `analyze_competitor_links()` - анализ ссылок конкурентов

#### 💼 Бизнесовые функции:
- `develop_outreach_strategies()` - разработка стратегий outreach
- `build_industry_relationships()` - построение отношений в индустрии
- `manage_link_budgets()` - управление бюджетами на линкбилдинг
- `create_link_worthy_content()` - создание контента, достойного ссылок
- `negotiate_link_placements()` - переговоры о размещении ссылок
- `measure_link_building_roi()` - измерение ROI линкбилдинга
- `manage_brand_mentions()` - управление упоминаниями бренда
- `develop_partnership_opportunities()` - развитие партнерских возможностей

**Типы ссылок (российский рынок):**
- **Редакционные ссылки:** естественные упоминания в статьях
- **Гостевые публикации:** статьи на российских тематических сайтах
- **Ресурсные страницы:** каталоги, справочники, полезные ссылки
- **Упоминания бренда:** мониторинг через Яндекс.Вордстат, Brand Analytics
- **Партнерские ссылки:** B2B партнерства, совместные проекты
- **Российская специфика:** соблюдение требований Яндекса, работа с .ru/.рф доменами

---

### 13. Competitive Analysis Agent
**Роль:** Конкурентный анализ, SERP мониторинг

#### 🔧 Технические функции:
- `analyze_serp_positions()` - анализ позиций в поисковой выдаче
- `track_competitor_keywords()` - отслеживание ключевых слов конкурентов
- `monitor_content_strategies()` - мониторинг контентных стратегий
- `analyze_technical_implementations()` - анализ технических реализаций
- `track_backlink_acquisitions()` - отслеживание приобретения обратных ссылок
- `monitor_page_speed_benchmarks()` - мониторинг бенчмарков скорости страниц
- `analyze_mobile_experiences()` - анализ мобильного опыта
- `track_feature_snippet_ownership()` - отслеживание владения featured snippets

#### 💼 Бизнесовые функции:
- `identify_market_opportunities()` - выявление рыночных возможностей
- `analyze_competitive_positioning()` - анализ конкурентного позиционирования
- `assess_market_share()` - оценка доли рынка
- `identify_content_gaps()` - выявление пробелов в контенте
- `monitor_pricing_strategies()` - мониторинг ценовых стратегий
- `analyze_brand_perception()` - анализ восприятия бренда
- `track_market_trends()` - отслеживание трендов рынка
- `develop_competitive_advantages()` - развитие конкурентных преимуществ

**Анализируемые метрики (российский рынок):**
- **Share of Voice:** доля голоса в Яндексе и Google (российский поиск)
- **Keyword Gap Analysis:** анализ через Serpstat, Rush Analytics, Топвизор
- **Content Gap Analysis:** контентные пробелы с учетом российской аудитории
- **Technical SEO Benchmarking:** соответствие требованиям Яндекса
- **Российская специфика:** Яндекс.Метрика, анализ мобильной выдачи Яндекса

---

### 14. Reporting Agent
**Роль:** Отчетность и аналитика, BI интеграция

#### 🔧 Технические функции:
- `integrate_analytics_platforms()` - интеграция аналитических платформ
- `automate_report_generation()` - автоматизация генерации отчетов
- `implement_data_visualization()` - реализация визуализации данных
- `create_custom_dashboards()` - создание кастомных дашбордов
- `implement_anomaly_detection()` - внедрение обнаружения аномалий
- `automate_alert_systems()` - автоматизация систем оповещений
- `integrate_business_intelligence()` - интеграция бизнес-аналитики
- `optimize_data_pipelines()` - оптимизация конвейеров данных

#### 💼 Бизнесовые функции:
- `create_executive_dashboards()` - создание executive дашбордов
- `generate_client_reports()` - генерация клиентских отчетов
- `track_business_kpis()` - отслеживание бизнес-KPI
- `provide_actionable_insights()` - предоставление действенных инсайтов
- `forecast_performance_trends()` - прогнозирование трендов эффективности
- `measure_campaign_effectiveness()` - измерение эффективности кампаний
- `create_stakeholder_communications()` - создание коммуникаций для стейкхолдеров
- `support_strategic_decisions()` - поддержка стратегических решений

**Типы отчетов (российский рынок):**
- **Performance Reports:** отчеты через Яндекс.Метрику и Google Analytics
- **Traffic Analysis:** анализ с фокусом на Яндекс и российскую аудиторию
- **Conversion Reports:** отчеты с интеграцией Roistat, Calltouch
- **ROI Analysis:** анализ в рублях с учетом НДС и налогообложения
- **Competitive Intelligence:** мониторинг через российские SEO инструменты
- **Российская специфика:** отчеты для 44-ФЗ, интеграция с 1С, ЕГРН данные

---

## 🔄 Интеграция и взаимодействие агентов

### **Workflow координация:**
1. **Task Coordination Agent** маршрутизирует задачи
2. **Executive агенты** принимают стратегические решения
3. **Management агенты** координируют выполнение
4. **Operational агенты** выполняют конкретные задачи
5. **Reporting Agent** собирает и анализирует результаты

### **Технологический стек:**
- **LLM Models:** GPT-4 (Executive), GPT-4o-mini (Management/Operational)
- **Vector Database:** ChromaDB для RAG функциональности
- **Framework:** LangChain + LangGraph для оркестрации
- **Knowledge Base:** Markdown файлы с экспертными знаниями
- **API Integration:** OpenAI API, FastAPI backend

### **RAG система:**
- **Chunk Size:** 512 токенов (оптимальный баланс)
- **Embedding Model:** OpenAI text-embedding-ada-002
- **Top-K Retrieval:** 3 наиболее релевантных фрагмента
- **Knowledge Updates:** Автоматическая векторизация при изменениях

---

## 📊 Бизнес-метрики системы

### **Производительность:**
- **14/14 агентов** функционируют со 100% успешностью
- **Executive качество:** 79.2/100 (GPT-4)
- **Management качество:** 88.8/100 (GPT-4o-mini)
- **Operational качество:** 86.4/100 (GPT-4o-mini)

### **Экономическая эффективность:**
- **Стоимость за запрос:** ~$0.0883 для полного цикла
- **Executive (GPT-4):** 91% от общих затрат (стратегические решения)
- **Management + Operational (GPT-4o-mini):** 9% (оперативные задачи)

### **Масштабируемость:**
- **Время инициализации:** ~66.4 секунды
- **Параллельная обработка:** До 14 агентов одновременно
- **Пропускная способность:** 1000+ запросов/час

---

## 🎯 Практическое применение

### **Типичный workflow для клиента:**
1. **Lead Qualification** → оценка перспективы
2. **Sales Conversation** → выявление потребностей
3. **Proposal Generation** → создание предложения
4. **Technical SEO Audit** → анализ текущего состояния
5. **Content Strategy** → планирование контента
6. **Competitive Analysis** → анализ конкурентов
7. **Link Building** → стратегия ссылочной массы
8. **Reporting** → отслеживание результатов

### **Интеграция с существующими системами:**
- **CRM:** amoCRM, Битрикс24, МойСклад, RetailCRM
- **Analytics:** Яндекс.Метрика, Google Analytics, Roistat, Calltouch
- **SEO Tools:** Serpstat, Rush Analytics, Be1, JustMagic, Топвизор
- **Project Management:** Битрикс24, Pyrus, ПланФикс, YouTrack, Kaiten

---

**📞 Контакты:**  
**Автор:** Andrew Popov  
**Email:** a.popov.gv@gmail.com  
**GitHub:** https://github.com/Andrew821667/ai-seo-architects  
**Версия документа:** 1.1 (адаптировано под российский рынок)  
**Дата:** Август 2025