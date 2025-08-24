# 🤖 ИИ Поисковые Архитекторы - Детальный справочник функций агентов (Часть 3)

**Продолжение агентов Операционного Уровня: Генерация Предложений, Технический Аудитор, Контентная Стратегия**

---

### **9. Агент генерации предложений**

#### **Роль и ответственность**
Агент генерации предложений создает персонализированные коммерческие предложения, разрабатывает ценовые модели и обеспечивает высокий уровень конверсии предложений в заключенные сделки.

#### **Детальные технические функции:**

**`реализация_динамического_ценообразования()`** - Реализация динамического ценообразования
- **Матрица ценообразующих факторов:**
  - **Фактор размера клиента (25% влияния на цену):**
    - Стартап (0-50 сотрудников): Базовая цена × 0.7
    - Малый бизнес (51-250 сотрудников): Базовая цена × 1.0
    - Средний рынок (251-1000 сотрудников): Базовая цена × 1.5
    - Корпорация (1000+ сотрудников): Базовая цена × 2.5-5.0
  - **Фактор сложности (30% влияния на цену):**
    - Простой сайт (<1000 страниц): Базовая цена × 0.8
    - Средний сайт (1000-10000 страниц): Базовая цена × 1.0
    - Сложный сайт (10000-100000 страниц): Базовая цена × 2.0
    - Корпоративный сайт (100000+ страниц): Базовая цена × 3.0-5.0
  - **Competition Factor (фактор конкуренции) (20% влияния на цену):**
    - No current SEO (отсутствие текущей поисковой оптимизации): Base price (базовая цена) × 1.2 (premium for greenfield (премиум за новый проект))
    - Underperforming agency (неэффективное агентство): Base price (базовая цена) × 1.0 (standard rate (стандартная ставка))
    - Strong competitor (сильный конкурент): Base price (базовая цена) × 0.8 (competitive pricing (конкурентное ценообразование))
    - In-house team (внутренняя команда): Base price (базовая цена) × 0.9 (value positioning (ценовое позиционирование))
  - **Urgency Factor (фактор срочности) (15% влияния на цену):**
    - Standard timeline (стандартные сроки): Base price (базовая цена) × 1.0
    - Expedited (rush) (ускоренно (срочно)): Base price (базовая цена) × 1.3
    - Emergency project (экстренный проект): Base price (базовая цена) × 1.5-2.0
  - **Relationship Factor (фактор отношений) (10% влияния на цену):**
    - New client (новый клиент): Base price (базовая цена) × 1.0
    - Referral (рекомендация): Base price (базовая цена) × 0.95
    - Existing client expansion (расширение существующего клиента): Base price (базовая цена) × 0.9
    - Strategic partnership (стратегическое партнерство): Base price (базовая цена) × 0.85

**`calculate_roi_projections()`** - Расчет прогнозов ROI
- **Traffic Projection Methodology (методология прогнозирования трафика):**
  - **Baseline Traffic Analysis (анализ базового трафика):** Current organic traffic levels (текущие уровни органического трафика)
  - **Keyword Opportunity Assessment (оценка возможностей ключевых слов):** Potential traffic from target keywords (потенциальный трафик от целевых ключевых слов)
  - **Competition Analysis (конкурентный анализ):** Market share potential based on competitors (потенциал рыночной доли на основе конкурентов)
  - **Seasonality Factors (сезонные факторы):** Seasonal traffic variations and adjustments (сезонные колебания трафика и корректировки)
  - **Growth Timeline (временная линия роста):** Month-by-month traffic growth projections (помесячные прогнозы роста трафика)
- **Conversion Rate Optimization Factors (факторы оптимизации коэффициента конверсии):**
  - **Current Conversion Baseline (текущий базовый уровень конверсии):** Existing organic traffic conversion rates (существующие коэффициенты конверсии органического трафика)
  - **Industry Benchmarks (отраслевые бенчмарки):** Typical conversion rates for the industry (типичные коэффициенты конверсии для отрасли)
  - **Technical Improvements (технические улучшения):** Expected conversion lift from technical SEO (ожидаемый рост конверсии от технической поисковой оптимизации)
  - **Content Quality Improvements (улучшения качества контента):** Conversion impact of better content (влияние лучшего контента на конверсию)
  - **User Experience Enhancements (улучшения пользовательского опыта):** UX improvements affecting conversions (улучшения пользовательского опыта, влияющие на конверсии)
- **Revenue Calculation Framework (фреймворк расчета доходов):**
  ```
  Projected Monthly Revenue (прогнозируемый месячный доход) = 
  (Projected Monthly Traffic (прогнозируемый месячный трафик) × Conversion Rate (коэффициент конверсии) × Average Order Value (средняя стоимость заказа)) - 
  (Current Monthly Traffic (текущий месячный трафик) × Current Conversion Rate (текущий коэффициент конверсии) × Current AOV (текущая средняя стоимость заказа))
  
  ROI (рентабельность инвестиций) = (Additional Annual Revenue (дополнительный годовой доход) - Annual SEO Investment (годовые инвестиции в поисковую оптимизацию)) / Annual SEO Investment (годовые инвестиции в поисковую оптимизацию) × 100%
  ```
- **Conservative vs Optimistic Scenarios (консервативные против оптимистичных сценариев):**
  - **Conservative (консервативный) (80% probability (вероятность)):** 50-100% traffic increase (увеличение трафика) over 12 months (за 12 месяцев)
  - **Realistic (реалистичный) (60% probability (вероятность)):** 100-200% traffic increase (увеличение трафика) over 12 months (за 12 месяцев)
  - **Optimistic (оптимистичный) (30% probability (вероятность)):** 200-400% traffic increase (увеличение трафика) over 12 months (за 12 месяцев)

**`generate_custom_proposals()`** - Генерация кастомных предложений
- **Proposal Structure Template (шаблон структуры предложения):**
  - **Executive Summary (исполнительное резюме) (10% документа):**
    - Client situation analysis (анализ ситуации клиента)
    - Proposed solution overview (обзор предлагаемого решения)
    - Expected outcomes and ROI (ожидаемые результаты и рентабельность инвестиций)
    - Investment summary (резюме инвестиций)
  - **Situation Analysis (анализ ситуации) (15% документа):**
    - Current SEO performance audit (аудит текущей производительности поисковой оптимизации)
    - Competitive landscape assessment (оценка конкурентного ландшафта)
    - Market opportunity identification (выявление рыночных возможностей)
    - Gap analysis and priorities (анализ пробелов и приоритеты)
  - **Proposed Solution (предлагаемое решение) (40% документа):**
    - Service scope and deliverables (объем услуг и результаты)
    - Implementation methodology (методология внедрения)
    - Timeline and milestones (временные рамки и вехи)
    - Team structure and responsibilities (структура команды и обязанности)
  - **Expected Outcomes (ожидаемые результаты) (20% документа):**
    - Traffic and ranking projections (прогнозы трафика и позиций)
    - Business impact forecasts (прогнозы влияния на бизнес)
    - ROI calculations and scenarios (расчеты рентабельности инвестиций и сценарии)
    - Success metrics and KPIs (метрики успеха и ключевые показатели эффективности)
  - **Investment and Terms (инвестиции и условия) (15% документа):**
    - Pricing structure and justification (структура цен и обоснование)
    - Payment terms and schedules (условия оплаты и графики)
    - Contract terms and conditions (условия и положения контракта)
    - Next steps and decision timeline (следующие шаги и временные рамки принятия решений)

#### **Российские ценовые модели:**

**Модель фиксированной цены:**
- **Применение:** Проекты с четким объемом и сроками
- **Структура:** Единовременная оплата или поэтапная по milestones
- **НДС учет:** 20% НДС включается в стоимость или добавляется отдельно
- **Риски:** Scope creep, неожиданные сложности
- **Преимущества:** Предсказуемость бюджета для клиента

**Модель абонентской платы:**
- **Применение:** Долгосрочные кампании поисковой оптимизации, постоянная оптимизация
- **Структура:** Ежемесячная фиксированная плата
- **Российская специфика:** Популярна из-за налогового планирования
- **Ценовые диапазоны:**
  - SMB: 150,000-500,000 ₽/месяц
  - Mid-market: 500,000-1,500,000 ₽/месяц
  - Enterprise: 1,500,000-5,000,000 ₽/месяц
- **Включенные услуги:** Определенный объем работ в месяц
- **Overage policy (политика превышения):** Дополнительные работы сверх ретейнера

**Модель оплаты по результату:**
- **Базовая модель:** Небольшая фиксированная часть + бонус за KPI
- **KPI варианты:**
  - Traffic growth (рост трафика): Бонус за каждые 10% роста трафика
  - Ranking improvements (улучшения позиций): Оплата за достижение топ-3 позиций
  - Revenue attribution (атрибуция доходов): % от дополнительного дохода через SEO
- **Валютные ограничения:** Соблюдение российского валютного законодательства
- **Risk-sharing (риск-шеринг):** Клиент и исполнитель делят риски и выгоды

**Гибридная модель:**
- **Структура:** Фикс (60-70%) + переменная часть (30-40%)
- **Применение:** Крупные проекты с неопределенными результатами
- **Российская адаптация:** 
  - Фиксированная часть покрывает операционные расходы
  - Переменная часть мотивирует на результат
  - Соответствие налоговому законодательству

#### **Детальные бизнесовые функции:**

**`create_executive_summaries()`** - Создание executive summary
- **Key Components for Russian Market:**
  - **Business Context (Бизнес-контекст):**
    - Company position in Russian market
    - Current digital presence assessment
    - Competitive landscape in Russia
    - Market opportunity quantification
  - **SEO Situation Analysis:**
    - Current organic visibility in Yandex and Google
    - Technical health assessment
    - Content quality evaluation
    - Backlink profile analysis
  - **Proposed Solution Overview:**
    - Strategic approach tailored to Russian market
    - Integration with existing Russian business systems
    - Compliance with Russian regulations and standards
    - Local market expertise and insights
  - **Expected Business Impact:**
    - Revenue growth projections in rubles
    - Market share expansion opportunities
    - Brand visibility improvements
    - Competitive advantage development
  - **Investment Summary:**
    - Total investment required (including VAT)
    - Payment schedule adapted to Russian practices
    - ROI projections and payback period
    - Risk mitigation and guarantees

### **10. Технический аудитор поисковой оптимизации**

#### **Роль и ответственность**
Технический аудитор поисковой оптимизации проводит комплексные технические аудиты сайтов, выявляет технические проблемы, влияющие на поисковую оптимизацию, и разрабатывает детальные планы по их устранению.

#### **Детальные технические функции:**

**`анализ_архитектуры_сайта()`** - Анализ архитектуры сайта
- **Анализ структуры адресов:**
  - **Оценка семантических адресов:** Говорящие адреса vs техническое написание
  - **Оптимизация длины адреса:** Рекомендуемая длина до 75 символов
  - **Обработка параметров:** Параметры ГЕТ, идентификаторы сессий, коды отслеживания
  - **Реализация канонических адресов:** Правильная настройка канонических тегов
  - **Логика иерархии адресов:** Логическая структура вложенности страниц
- **Site Navigation Assessment (оценка навигации сайта):**
  - **Main Navigation Structure (структура основной навигации):** Горизонтальное меню и его логика
  - **Breadcrumb Implementation (реализация хлебных крошек):** Хлебные крошки и schema markup (схемная разметка)
  - **Footer Navigation (навигация в подвале):** Дополнительные навигационные элементы
  - **Sidebar Navigation (боковая навигация):** Боковые меню и их SEO влияние
  - **Search Functionality (функциональность поиска):** Внутренний поиск и его оптимизация
- **Internal Linking Analysis (анализ внутренних ссылок):**
  - **Link Distribution (распределение ссылок):** Распределение внутренних ссылок по сайту
  - **Anchor Text Optimization (оптимизация анкорных текстов):** Анкорные тексты внутренних ссылок
  - **Link Depth Analysis (анализ глубины ссылок):** Глубина вложенности страниц от главной
  - **Orphaned Pages Detection (обнаружение сиротских страниц):** Страницы без входящих внутренних ссылок
  - **Link Equity Flow (поток ссылочного веса):** Передача ссылочного веса по сайту

**`audit_core_web_vitals()`** - Аудит Core Web Vitals
- **Largest Contentful Paint (LCP) Analysis (анализ наибольшей отрисовки контента):**
  - **LCP Element Identification (идентификация элемента LCP):** Определение элемента LCP на страницах
  - **Resource Loading Optimization (оптимизация загрузки ресурсов):**
    - Critical resource prioritization (приоритизация критических ресурсов)
    - Preload directives for key resources (директивы предзагрузки для ключевых ресурсов)
    - Image optimization and WebP implementation (оптимизация изображений и внедрение WebP)
    - Font loading optimization (оптимизация загрузки шрифтов)
  - **Server Response Time Optimization (оптимизация времени отклика сервера):**
    - TTFB (Time to First Byte) measurement (измерение времени до первого байта)
    - Server-side caching implementation (реализация серверного кэширования)
    - Database query optimization (оптимизация запросов базы данных)
    - CDN configuration for Russian market (настройка CDN для российского рынка)
  - **LCP Improvement Strategies (стратегии улучшения LCP):**
    - Above-the-fold content prioritization (приоритизация контента в видимой области)
    - Hero image optimization (оптимизация главного изображения)
    - Critical CSS inlining (встраивание критического CSS)
    - JavaScript execution optimization (оптимизация выполнения JavaScript)
- **First Input Delay / Interaction to Next Paint (FID/INP) Analysis (анализ задержки первого ввода / взаимодействия до следующей отрисовки):**
  - **JavaScript Execution Optimization (оптимизация выполнения JavaScript):**
    - Main thread blocking time reduction (сокращение времени блокировки основного потока)
    - Long task identification and splitting (идентификация и разбиение долгих задач)
    - Third-party script optimization (оптимизация сторонних скриптов)
    - Code splitting and lazy loading (разбиение кода и ленивая загрузка)
  - **Event Handler Optimization (оптимизация обработчиков событий):**
    - Input responsiveness improvement (улучшение отзывчивости ввода)
    - Event delegation patterns (шаблоны делегирования событий)
    - Passive event listeners (пассивные обработчики событий)
    - Touch interaction optimization (оптимизация сенсорного взаимодействия)
- **Cumulative Layout Shift (CLS) Analysis:**
  - **Layout Stability Assessment:**
    - Image dimension specification
    - Font loading impact on layout
    - Dynamic content insertion handling
    - Advertisement placement optimization
  - **CLS Improvement Strategies:**
    - Placeholder implementation for dynamic content
    - Proper image and video sizing
    - Font-display optimization
    - Animation and transition optimization

**`check_indexing_status()`** - Проверка статуса индексации
- **Index Coverage Analysis:**
  - **Google Search Console Integration:**
    - Index coverage report analysis
    - Valid pages vs errors and warnings
    - Excluded pages reasoning and optimization
    - Crawl budget utilization assessment
  - **Yandex Webmaster Integration (Российская специфика):**
    - Индексирование в Яндексе
    - Статистика обхода Яндекс.Ботом
    - Качество индексирования по регионам
    - Мобильная версия индексирования
- **Technical Indexing Factors:**
  - **Robots.txt Analysis:**
    - Proper directive implementation
    - Crawl budget optimization
    - Disallow pattern effectiveness
    - Sitemap reference inclusion
  - **Meta Robots Assessment:**
    - Noindex directive usage and reasoning
    - Nofollow implementation strategy
    - X-Robots-Tag header analysis
    - Canonical directive conflicts
- **XML Sitemap Optimization:**
  - **Sitemap Structure Analysis:**
    - URL inclusion completeness
    - Priority and change frequency accuracy
    - Image and video sitemap implementation
    - News sitemap for relevant sites
  - **Sitemap Technical Health:**
    - Size limitations compliance (50MB, 50,000 URLs)
    - Gzip compression implementation
    - HTTP status code validation
    - Last modification date accuracy

**`analyze_crawlability()`** - Анализ краулинга сайта
- **Crawl Accessibility Assessment:**
  - **Server Response Analysis:**
    - HTTP status code distribution
    - Redirect chain analysis and optimization
    - Server error identification and resolution
    - Response time consistency across pages
  - **Internal Linking Assessment:**
    - Crawlable link detection (avoiding JavaScript-only links)
    - Link equity distribution effectiveness
    - Crawl depth optimization
    - Faceted navigation handling
- **Crawl Budget Optimization:**
  - **Priority Page Identification:**
    - High business value page prioritization
    - Conversion-focused page emphasis
    - Fresh content crawling frequency
    - Seasonal content crawl scheduling
  - **Crawl Waste Elimination:**
    - Low-value page identification
    - Duplicate content consolidation
    - Parameter handling optimization
    - Pagination best practices implementation

#### **Российская специфика технического SEO:**

**Yandex-Specific Factors:**
- **Поведенческие факторы:** Влияние пользовательского поведения на ранжирование
- **Региональность:** Оптимизация для региональной выдачи Яндекса
- **Турбо-страницы:** Технология быстрой загрузки для мобильных устройств
- **Коммерческие факторы:** Особенности ранжирования коммерческих запросов

**Compliance Requirements:**
- **ГОСТ Р 52872-2019:** Стандарты доступности для государственных сайтов
- **152-ФЗ:** Соблюдение законодательства о персональных данных
- **Доступность:** Адаптация сайтов для людей с ограниченными возможностями

### **11. Агент контентной стратегии**

#### **Роль и ответственность**
Агент контентной стратегии разрабатывает комплексные контентные стратегии, проводит исследования ключевых слов, создает контентные календари и обеспечивает соответствие контента принципам О-Э-А-Д.

#### **Детальные технические функции:**

**`проведение_исследования_ключевых_слов()`** - Проведение исследования ключевых слов
- **Процесс обнаружения ключевых слов:**
  - **Определение базовых ключевых слов:**
    - Core business terms and services
    - Product and service categorization
    - Brand-related keyword variations
    - Industry-specific terminology
  - **Методы расширения ключевых слов:**
    - Интеграция Планировщика ключевых слов Гугла
    - Исследование ключевых слов через Серпстат для российского рынка
    - Анализ Яндекс.Вордстат для российских запросов
    - Анализ пробелов в ключевых словах конкурентов
    - Обнаружение длиннохвостых ключевых слов через автодополнение
- **Классификация намерений поиска:**
  - **Информационные намерения (30-40% целевых ключевых слов):**
    - Инструкции: "как сделать аудит поисковой оптимизации"
    - Определения: "что такое Основные Веб Показатели"
    - Сравнения: "Гугл Аналитикс vs Яндекс.Метрика"
    - Обучающие запросы: "настройка robots.txt"
  - **Навигационные намерения (20-25% целевых ключевых слов):**
    - Брендовые запросы: "[Название бренда] + поисковая оптимизация"
    - Поиск продуктов: "Серпстат цены"
    - Поиск услуг: "агентство поисковой оптимизации Москва"
    - Местные запросы: "услуги поисковой оптимизации СПб"
  - **Transactional Intent (25-35% of target keywords):**
    - Service purchase: "заказать SEO продвижение"
    - Price inquiries: "стоимость SEO аудита"
    - Comparison shopping: "сравнить SEO агентства"
    - Local services: "SEO агентство рядом"
  - **Commercial Investigation (10-15% of target keywords):**
    - Review searches: "отзывы о SEO агентстве"
    - Best-of searches: "лучшие SEO инструменты"
    - Versus comparisons: "SEMrush vs Serpstat"
    - Feature comparisons: "функции Screaming Frog"

**`analyze_content_gaps()`** - Анализ пробелов в контенте
- **Content Gap Analysis Methodology:**
  - **Competitor Content Audit:**
    - Top-performing competitor pages identification
    - Content themes and topics coverage analysis
    - Content format and structure assessment
    - Content depth and comprehensiveness evaluation
  - **SERP Analysis for Target Keywords:**
    - Top 10 ranking pages content analysis
    - Featured snippet content examination
    - People Also Ask (PAA) questions compilation
    - Related searches and suggested topics
  - **User Intent Satisfaction Assessment:**
    - Content alignment with search intent
    - Information completeness evaluation
    - User experience and readability assessment
    - Conversion pathway effectiveness
- **Gap Prioritization Framework:**
  - **Business Impact Scoring (40%):**
    - Revenue potential from gap filling
    - Strategic importance to business goals
    - Brand authority building opportunity
    - Competitive advantage potential
  - **Effort Required Scoring (30%):**
    - Content creation complexity
    - Required expertise and resources
    - Time investment estimation
    - Technical implementation difficulty
  - **Ranking Opportunity Scoring (30%):**
    - Keyword difficulty assessment
    - Competition level analysis
    - Current domain authority advantage
    - Ranking timeline estimation

**`implement_topic_clustering()`** - Реализация кластеризации тем
- **Topic Cluster Architecture:**
  - **Pillar Content Strategy:**
    - Core topic identification (5-10 main pillars)
    - Comprehensive pillar page creation (3000-5000 words)
    - Subtopic and supporting content mapping
    - Internal linking strategy between pillars and clusters
  - **Cluster Content Development:**
    - Supporting article identification (10-20 per pillar)
    - Content depth and angle variation
    - Keyword distribution across cluster
    - Content format diversification (guides, lists, comparisons)
- **Semantic Keyword Grouping:**
  - **Primary Keyword Assignment:** One main keyword per content piece
  - **Semantic Variations Inclusion:** Related terms and synonyms
  - **LSI Keywords Integration:** Latent semantic indexing terms
  - **Question-Based Content Creation:** FAQ and question-targeting content
- **Russian Language Specifics:**
  - **Morphological Variations:** Russian word form variations
  - **Regional Language Differences:** Moscow vs regional terminology
  - **Transliteration Handling:** English terms in Cyrillic
  - **Cultural Context Integration:** Russian business culture references

#### **Реализация фреймворка О-Э-А-Д:**

**Опыт - 25% от общего скора:**
- **First-Hand Experience Demonstration:**
  - Case study presentations with real results
  - Personal anecdotes and lessons learned
  - Behind-the-scenes content and processes
  - Real client testimonials and feedback
- **Practical Knowledge Showcase:**
  - Step-by-step tutorials with screenshots
  - Tool reviews based on actual usage
  - Industry insights from direct involvement
  - Troubleshooting guides from real problems
- **Experience Validation Methods:**
  - Portfolio showcasing with metrics
  - Industry recognition and awards
  - Speaking engagements and conferences
  - Published research and whitepapers

**Экспертность - 25% от общего скора:**
- **Subject Matter Authority:**
  - In-depth technical knowledge demonstration
  - Advanced topic coverage beyond basics
  - Industry trend analysis and predictions
  - Complex problem-solving examples
- **Credentials and Qualifications:**
  - Professional certifications (Google, Yandex)
  - Educational background relevance
  - Industry association memberships
  - Continuing education and training
- **Expertise Demonstration Tactics:**
  - Advanced technical content creation
  - Industry terminology proper usage
  - Complex concept explanation ability
  - Cutting-edge technique implementation

**Авторитетность - 25% от общего скора:**
- **Industry Recognition:**
  - Media citations and mentions
  - Peer recognition and references
  - Industry award recognition
  - Speaking opportunities at conferences
- **Content Distribution and Reach:**
  - Publication on authoritative sites
  - Social media following and engagement
  - Email list size and engagement rates
  - Content sharing and viral potential
- **Authority Building Strategies:**
  - Guest posting on industry publications
  - Podcast appearances and hosting
  - Webinar hosting and participation
  - Industry survey and research publication

**Доверие - 25% от общего скора:**
- **Transparency and Honesty:**
  - Clear author identification and bio
  - Conflict of interest disclosure
  - Methodology transparency in research
  - Error correction and update policies
- **Social Proof and Validation:**
  - Client testimonials and reviews
  - Third-party verification and validation
  - Professional references and recommendations
  - Independent audit results and certifications
- **Trust Building Elements:**
  - Contact information prominence
  - Privacy policy and terms of service
  - Secure website implementation (HTTPS)
  - Regular content updates and maintenance

#### **Российская специфика контентной стратегии:**

**Language and Cultural Adaptation:**
- **Russian Language Optimization:**
  - Proper Russian grammar and syntax
  - Regional terminology preferences
  - Formal vs informal tone selection
  - Cultural reference appropriateness
- **Local Market Understanding:**
  - Russian business culture integration
  - Local case studies and examples
  - Regional market specifics inclusion
  - Government regulation compliance

**Каналы распространения контента:**
- **Российские социальные платформы:**
  - Оптимизация контента для ВКонтакте
  - Стратегия телеграм-каналов
  - Вовлечение аудитории Одноклассников
  - Стратегия публикаций Яндекс.Дзен
- **Местные контентные партнерства:**
  - Отношения с российскими сМИ
  - Сотрудничество с отраслевыми изданиями
  - Возможности партнерства с блогерами
  - Вовлечение профессиональных сообществ

---

*Это третья часть детального справочника. Продолжение следует в AGENTS_FUNCTIONS_GUIDE_PART4.md*