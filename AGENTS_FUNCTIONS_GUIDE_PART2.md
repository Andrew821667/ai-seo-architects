# 🤖 ИИ Поисковые Архитекторы - Детальный справочник функций агентов (Часть 2)

**Продолжение детального описания агентов Уровня Управления и Операционного Уровня**

---

### **5. Менеджер технических операций поисковой оптимизации**

#### **Роль и ответственность**
Менеджер технических операций поисковой оптимизации координирует все технические аспекты оптимизации, управляет техническими аудитами и обеспечивает соответствие сайтов современным стандартам поисковых систем.

#### **Детальные технические функции:**

**`координация_технических_аудитов()`** - Координация технических аудитов поисковой оптимизации
- **Определение области аудита:**
  - **Оценка сканируемости:** robots.txt, карты сайта, внутренняя перелинковка
  - **Анализ индексируемости:** Мета-роботы, канонические теги, дублированные страницы
  - **Обзор архитектуры сайта:** Структура адресов, навигация, хлебные крошки
  - **Оптимизация производительности:** Основные веб-показатели, скорость страницы, мобильная оптимизация
  - **Техническая реализация:** Структурированная разметка, мультиязычность, безопасное соединение
- **Методология аудита:**
  - Автоматизированное сканирование с инструментами (ПиксельТулс, Нетпик Спайдер, Серпстат)
  - Ручная проверка критических проблем
  - Анализ логов сервера для паттернов сканирования
  - Тестирование производительности на разных устройствах и сетях
- **Матрица приоритизации проблем:**
  - **Критические (П0):** Проблемы, ломающие сайт, крупные проблемы индексирования
  - **Высокие (П1):** Проблемы производительности, отсутствие структурированных данных
  - **Средние (П2):** Возможности оптимизации, мелкие технические долги
  - **Низкие (П3):** Желательные улучшения, будущие рассмотрения

**`мониторинг_основных_веб_показателей()`** - Мониторинг основных веб-показателей
- **Мониторинг реальных пользователей:**
  - **Отслеживание ВОКЭ:** Измерение времени отрисовки крупнейшего элемента
    - Хорошо: ≤ 2.5 секунд
    - Нуждается в улучшении: 2.5 - 4.0 секунд  
    - Плохо: > 4.0 секунд
  - **Мониторинг ЗПВ/ВВСО:** Задержка первого ввода / Время взаимодействия до следующей отрисовки
    - Хорошая ЗПВ: ≤ 100 миллисекунд
    - Хорошое ВВСО: ≤ 200 миллисекунд
  - **Измерение ССМ:** Совокупное смещение макета
    - Хорошо: ≤ 0.1
    - Нуждается в улучшении: 0.1 - 0.25
    - Плохо: > 0.25
- **Анализ лабораторных данных:**
  - Интеграция с Пагспид Инсайтс
  - Реализация Лайтхаус НПИ
  - Автоматизация ВебПагеТест
  - Кастомные бюджеты производительности
- **Performance Optimization Strategies:**
  - Image optimization and WebP conversion
  - Critical CSS implementation
  - JavaScript optimization and code splitting
  - Server-side rendering (SSR) considerations

**`управление_бюджетами_сканирования()`** - Управление бюджетами сканирования
- **Оптимизация бюджета сканирования:**
  - **Определение приоритетных страниц:** Высокоценные страницы для поисковых систем
  - **Устранение излишнего сканирования:** Удаление малоценных страниц из сканирования
  - **Оптимизация внутренних ссылок:** Направление сканеров к важному контенту
  - **Оптимизация ответа сервера:** Сокращение времени сканирования и ресурсов
- **Log File Analysis:**
  - Googlebot and Yandex bot crawling patterns
  - Crawl frequency by page type
  - HTTP status code distribution
  - Crawl depth and path analysis
- **Российская специфика поисковых систем:**
  - **Поведение краулера Яндекса:** Понимание предпочтений робота Яндекса
  - **Региональные паттерны сканирования:** Москва, СПб, региональные различия
  - **Мобильно-первое индексирование:** Адаптация к мобильному индексированию Яндекса

**`optimize_site_performance()`** - Оптимизация производительности сайтов
- **Frontend Optimization:**
  - **Critical Rendering Path Optimization**
  - **Resource Loading Prioritization**
  - **CSS and JavaScript Minification**
  - **Image Lazy Loading Implementation**
- **Backend Optimization:**
  - **Database Query Optimization**
  - **Caching Strategy Implementation** (Redis, Memcached)
  - **CDN Configuration** (CloudFlare, Yandex CDN for Russian market)
  - **Server Response Time Optimization**
- **Mobile Performance:**
  - **Responsive Design Optimization**
  - **Touch Interaction Optimization**
  - **Mobile-Specific Resource Loading**
  - **Progressive Web App (PWA) Implementation**

#### **Детальные бизнесовые функции:**

**`prioritize_technical_fixes()`** - Приоритизация технических исправлений
- **Business Impact Assessment:**
  - **Revenue Impact:** Direct correlation with conversion rates
  - **Traffic Impact:** Potential organic traffic gains
  - **User Experience Impact:** Effect on user satisfaction metrics
  - **Brand Impact:** Professional appearance and credibility
- **Implementation Cost Analysis:**
  - **Development Time:** Required developer hours
  - **Resource Requirements:** Specialized skills needed
  - **Testing Requirements:** QA and validation time
  - **Risk Assessment:** Potential negative impacts
- **ROI Calculation Framework:**
  - Expected traffic increase × Conversion rate × Average order value
  - Implementation cost (development + testing + deployment)
  - Payback period calculation
  - Risk-adjusted ROI

**`manage_technical_resources()`** - Управление техническими ресурсами
- **Team Resource Allocation:**
  - **Frontend Developers:** UI/UX optimization, performance improvements
  - **Backend Developers:** Server optimization, database tuning
  - **DevOps Engineers:** Infrastructure, deployment, monitoring
  - **SEO Technicians:** Implementation verification, testing
- **Tool and Technology Management:**
  - **SEO Tools Budget:** Screaming Frog, DeepCrawl, Serpstat subscriptions
  - **Development Tools:** IDE licenses, testing frameworks
  - **Infrastructure Costs:** Servers, CDN, monitoring tools
  - **Training and Certification:** Team skill development

### **6. Менеджер по успеху клиентов**

#### **Роль и ответственность**
Менеджер по успеху клиентов обеспечивает долгосрочный успех клиентов, максимизирует удержание, выявляет возможности для роста аккаунтов и поддерживает высокий уровень удовлетворенности.

#### **Детальные технические функции:**

**`мониторинг_метрик_клиентов()`** - Мониторинг метрик клиентов
- **Метрики эффективности поисковой оптимизации:**
  - **Рост органического трафика:** Помесячные, годовые тренды
  - **Рейтинг ключевых слов:** Отслеживание позиций для целевых ключевых слов
  - **Функции выдачи:** Рекомендуемые сниппеты, панели знаний, местные выборки
  - **Коэффициент кликабельности:** Оптимизация КК и отслеживание
- **Business Performance Metrics:**
  - **Conversion Rates:** Organic traffic to lead/sale conversion
  - **Revenue Attribution:** SEO's contribution to business revenue
  - **Customer Acquisition Cost:** CAC through organic channel
  - **Lifetime Value:** LTV of customers acquired through SEO
- **Technical Health Metrics:**
  - **Core Web Vitals:** Performance trending
  - **Crawl Errors:** Technical issues monitoring
  - **Site Health Score:** Overall technical SEO health
  - **Mobile Performance:** Mobile-specific metrics

**`implement_health_scoring()`** - Реализация системы оценки здоровья аккаунтов
- **Health Score Components (100-point scale):**
  - **Performance (40 points):** Traffic, rankings, conversions
  - **Engagement (25 points):** Meeting attendance, response rates
  - **Growth (20 points):** Account expansion, additional services
  - **Satisfaction (15 points):** Survey scores, feedback quality
- **Risk Indicators:**
  - **Red Flags (0-50 points):** High churn risk, immediate intervention needed
  - **Yellow Flags (51-70 points):** At-risk, proactive engagement required
  - **Green Status (71-100 points):** Healthy account, expansion opportunity
- **Automated Alerting:**
  - Score drop triggers for immediate action
  - Trend analysis for predictive insights
  - Escalation procedures for critical accounts

**`automate_success_workflows()`** - Автоматизация workflow успеха клиентов
- **Onboarding Automation:**
  - **Welcome Sequence:** Automated email series for new clients
  - **Goal Setting Process:** Structured approach to KPI definition
  - **Initial Setup:** Account configuration and baseline establishment
  - **First Value Delivery:** Quick wins to demonstrate value
- **Ongoing Success Workflows:**
  - **Regular Check-ins:** Automated scheduling and reminder systems
  - **Performance Reporting:** Automated report generation and delivery
  - **Issue Detection:** Proactive problem identification and alerting
  - **Renewal Preparation:** Automated renewal timeline and materials

#### **Детальные бизнесовые функции:**

**`develop_retention_strategies()`** - Разработка стратегий удержания
- **Retention Strategy Framework:**
  - **Value Demonstration:** Regular ROI reporting and success story sharing
  - **Proactive Support:** Anticipating needs before problems arise
  - **Relationship Building:** Personal connections beyond business transactions
  - **Continuous Improvement:** Ongoing service enhancement and optimization
- **Risk Mitigation Strategies:**
  - **Early Warning System:** Behavioral indicators of potential churn
  - **Intervention Protocols:** Specific actions for different risk levels
  - **Win-back Campaigns:** Strategies for re-engaging disengaged clients
  - **Competitive Defense:** Protecting against competitor poaching
- **Success Metrics:**
  - **Net Revenue Retention (NRR):** >100% target through expansion
  - **Gross Revenue Retention (GRR):** >90% target for healthy retention
  - **Customer Satisfaction Score (CSAT):** >4.5/5.0 target
  - **Net Promoter Score (NPS):** >50 target for advocacy

**`identify_upselling_opportunities()`** - Выявление возможностей для upselling
- **Expansion Opportunity Mapping:**
  - **Service Gaps:** Areas where additional SEO services could help
  - **Performance Plateaus:** Situations requiring advanced strategies
  - **New Business Initiatives:** Client growth creating new needs
  - **Competitive Pressures:** Market changes requiring enhanced services
- **Upselling Categories:**
  - **Service Expansion:** Additional SEO services (local, international, e-commerce)
  - **Technology Upgrades:** Advanced tools and platforms
  - **Consulting Services:** Strategic guidance and specialized expertise
  - **Training and Education:** Client team capability building
- **Timing and Approach:**
  - **Success-Based Timing:** Upselling during positive performance periods
  - **Need-Based Timing:** Responding to specific business challenges
  - **Relationship-Based Approach:** Leveraging strong client relationships
  - **Value-First Presentation:** Leading with client benefit, not vendor need

---

## 🔧 **ОПЕРАЦИОННЫЙ УРОВЕНЬ - ДЕТАЛЬНОЕ ОПИСАНИЕ**

### **7. Агент квалификации лидов**

#### **Роль и ответственность**
Агент квалификации лидов отвечает за эффективную оценку входящих лидов, применение международных методологий квалификации (БАНТ, МЭДДИК) и обеспечение высокого качества передаваемых в продажи лидов.

#### **Детальные технические функции:**

**`реализация_бант_оценивания()`** - Реализация БАНТ оценивания
- **Оценка бюджета (25% от общего скора):**
  - **Явная информация о бюджете:** Прямые заявления о бюджете
    - High Score (20-25): >5M ₽/год открыто заявлен
    - Medium Score (10-19): 1-5M ₽/год или косвенные индикаторы
    - Low Score (0-9): <1M ₽/год или бюджет не определен
  - **Косвенные индикаторы бюджета:** Косвенные признаки бюджета
    - Размер компании и доходы
    - Индикаторы текущих маркетинговых расходов
    - Сложность технологического стека
    - Предыдущие отношения с поставщиками и расходы
- **Authority Assessment (25% от общего скора):**
  - **Decision-Making Level Identification:**
    - C-Level (20-25 points): CEO, CMO, CTO direct involvement
    - Director Level (15-19 points): Marketing Director, IT Director
    - Manager Level (10-14 points): SEO Manager, Digital Marketing Manager
    - Specialist Level (0-9 points): Individual contributors, analysts
  - **Decision-Making Process Mapping:**
    - Single decision maker vs committee decisions
    - Budget approval process understanding
    - Influencer identification and engagement
- **Need Assessment (25% от общего скора):**
  - **Pain Point Severity:**
    - Critical (20-25): Business-threatening SEO issues
    - High (15-19): Significant growth obstacles
    - Medium (10-14): Optimization opportunities
    - Low (0-9): Nice-to-have improvements
  - **Current Solution Gaps:**
    - No current SEO efforts (high need)
    - In-house team limitations (medium-high need)
    - Agency underperformance (medium need)
    - Basic optimization complete (low need)
- **Timeline Assessment (25% от общего скора):**
  - **Urgency Indicators:**
    - Immediate (20-25): Active evaluation, decision within 30 days
    - Short-term (15-19): Planning for 1-3 months
    - Medium-term (10-14): 3-6 months timeline
    - Long-term (0-9): >6 months or undefined

**`analyze_lead_sources()`** - Анализ источников лидов
- **Source Performance Analysis:**
  - **Organic Search:** Quality score, conversion rates, lifetime value
  - **Paid Advertising:** Google Ads, Yandex.Direct, social media ads
  - **Content Marketing:** Blog posts, whitepapers, webinars
  - **Referrals:** Partner referrals, client referrals, word-of-mouth
  - **Events:** Conferences, trade shows, networking events
- **Source Quality Metrics:**
  - **Lead-to-Opportunity Conversion:** % of leads becoming qualified opportunities
  - **Opportunity-to-Customer Conversion:** % of opportunities closing
  - **Customer Lifetime Value:** Average LTV by source
  - **Cost Per Acquisition:** Total cost to acquire customer by source
- **Russian Market Source Specifics:**
  - **Yandex Ecosystem:** Yandex.Direct, Yandex.Market presence
  - **Local Business Networks:** Russian B2B platforms and directories
  - **Industry Events:** Russian marketing conferences and SEO events
  - **Professional Communities:** SEO and digital marketing groups

**`implement_meddic_framework()`** - Применение MEDDIC методологии
- **Metrics (20% от MEDDIC скора):**
  - **Quantifiable Business Metrics:** Revenue, traffic, conversion rates
  - **Success Criteria Definition:** Specific, measurable outcomes
  - **Baseline Establishment:** Current performance measurement
  - **Target Goals:** Desired improvement levels and timelines
- **Economic Buyer (20% от MEDDIC скора):**
  - **Budget Authority Identification:** Who controls the budget
  - **Financial Decision Process:** How budget decisions are made
  - **ROI Requirements:** Expected return on investment thresholds
  - **Budget Cycle Understanding:** When budget decisions are made
- **Decision Criteria (15% от MEDDIC скора):**
  - **Evaluation Criteria:** How vendor selection decisions are made
  - **Weighting Factors:** Which criteria are most important
  - **Competitive Factors:** What differentiates vendor options
  - **Risk Tolerance:** Acceptable levels of implementation risk
- **Decision Process (15% от MEDDIC скора):**
  - **Process Mapping:** Steps in the decision-making process
  - **Stakeholder Involvement:** Who participates in decisions
  - **Timeline Understanding:** How long the process takes
  - **Approval Requirements:** What approvals are needed
- **Identify Pain (15% от MEDDIC скора):**
  - **Business Impact:** How problems affect business outcomes
  - **Urgency Level:** How quickly problems need resolution
  - **Previous Attempts:** What solutions have been tried
  - **Cost of Inaction:** What happens if problems aren't solved
- **Champion (15% от MEDDIC скора):**
  - **Internal Advocate Identification:** Who supports the solution internally
  - **Influence Level:** How much influence the champion has
  - **Relationship Quality:** Strength of relationship with champion
  - **Champion Development:** How to strengthen champion support

#### **Детальные бизнесовые функции:**

**`assess_budget_authority()`** - Оценка бюджета и полномочий лида
- **Budget Discovery Techniques:**
  - **Direct Questioning:** "What budget range are you considering for SEO?"
  - **Indirect Approaches:** "What did you invest in marketing last year?"
  - **Benchmark Comparisons:** "Companies your size typically invest X in SEO"
  - **Value-Based Discussions:** "What would a 50% traffic increase be worth?"
- **Authority Verification Methods:**
  - **Role Confirmation:** LinkedIn verification, company website checks
  - **Decision Process Understanding:** "How are vendor decisions made?"
  - **Budget Approval Process:** "Who needs to approve this investment?"
  - **Stakeholder Mapping:** "Who else would be involved in this decision?"
- **Russian Business Culture Considerations:**
  - **Hierarchical Decision Making:** Understanding Russian corporate structures
  - **Relationship Importance:** Building trust and personal connections
  - **Formal vs Informal Authority:** Recognizing both official and unofficial influence
  - **State Enterprise Specifics:** Understanding government sector decision processes

**`identify_decision_makers()`** - Выявление лиц, принимающих решения
- **Stakeholder Mapping Framework:**
  - **Economic Buyer:** Controls budget and final approval
  - **Technical Buyer:** Evaluates technical aspects and implementation
  - **User Buyer:** Will use the service and affected by outcomes
  - **Coach/Champion:** Internal advocate supporting the purchase
- **Influence Assessment:**
  - **High Influence:** Can drive or veto the decision
  - **Medium Influence:** Significant input into the decision
  - **Low Influence:** Minimal impact on final outcome
  - **Influencing Factors:** What motivates each stakeholder
- **Engagement Strategy by Role:**
  - **Executive Engagement:** Strategic value, ROI, competitive advantage
  - **Technical Engagement:** Implementation details, integration, security
  - **User Engagement:** Ease of use, training, support
  - **Champion Development:** Internal selling tools, success stories

### **8. Агент продажных разговоров**

#### **Роль и ответственность**
Агент продажных разговоров ведет продажные разговоры, применяет СПИН методологию, обрабатывает возражения и направляет потенциальных клиентов через процесс принятия решений.

#### **Детальные технические функции:**

**`применение_методологии_спин()`** - Применение методологии СПИН
- **Situation Questions (Ситуационные вопросы) - 25% времени разговора:**
  - **Current State Assessment:** "Как сейчас организованы ваши SEO процессы?"
  - **Existing Solutions:** "Какие инструменты вы используете для SEO?"
  - **Team Structure:** "Кто в вашей команде отвечает за SEO?"
  - **Performance Baseline:** "Какие результаты вы получаете от текущих усилий?"
  - **Process Understanding:** "Как выглядит ваш типичный проект по оптимизации?"
- **Problem Questions (Проблемные вопросы) - 35% времени разговора:**
  - **Pain Point Discovery:** "С какими сложностями вы сталкиваетесь в SEO?"
  - **Gap Identification:** "Где вы видите наибольшие упущенные возможности?"
  - **Resource Constraints:** "Что мешает вам масштабировать SEO усилия?"
  - **Competition Challenges:** "Как конкуренты обходят вас в поиске?"
  - **Technical Limitations:** "Какие технические ограничения замедляют рост?"
- **Implication Questions (Извлекающие вопросы) - 25% времени разговора:**
  - **Business Impact:** "Как текущие SEO проблемы влияют на ваши продажи?"
  - **Cost of Inaction:** "Что произойдет, если ситуация не изменится?"
  - **Competitive Disadvantage:** "Как отставание в SEO влияет на долю рынка?"
  - **Opportunity Cost:** "Сколько потенциальных клиентов вы теряете?"
  - **Future Implications:** "Как эти проблемы будут развиваться со временем?"
- **Need-Payoff Questions (Направляющие вопросы) - 15% времени разговора:**
  - **Solution Value:** "Насколько ценным было бы решение этих проблем?"
  - **ROI Potential:** "Какую прибыль принесло бы удвоение органического трафика?"
  - **Capability Benefits:** "Как улучшенные SEO процессы помогли бы команде?"
  - **Competitive Advantage:** "Какие преимущества дало бы лидерство в поиске?"
  - **Future State Vision:** "Как бы выглядел ваш идеальный SEO результат?"

**`анализ_паттернов_разговоров()`** - Анализ паттернов разговоров
- **Conversation Flow Analysis:**
  - **Opening Effectiveness:** How well conversations start and engage prospects
  - **Question Sequence Optimization:** Most effective order of SPIN questions
  - **Transition Smoothness:** How well conversations flow between topics
  - **Closing Strength:** Effectiveness of moving to next steps
- **Language Pattern Recognition:**
  - **Buying Signals:** Words and phrases indicating purchase intent
  - **Objection Patterns:** Common objection themes and timing
  - **Engagement Indicators:** Verbal cues showing interest levels
  - **Decision-Making Language:** Phrases indicating evaluation processes
- **Outcome Prediction Modeling:**
  - **Conversation Quality Scoring:** Based on SPIN methodology application
  - **Progression Probability:** Likelihood of moving to next sales stage
  - **Deal Size Indicators:** Conversation elements correlating with larger deals
  - **Timeline Prediction:** Expected decision-making timeframes

#### **Российская специфика методологии СПИН:**

**Культурные адаптации:**
- **Построение отношений:** Больше времени на личные связи
- **Уважение иерархии:** Признание статуса и позиции
- **Прямая против косвенная коммуникация:** Баланс между прямотой и дипломатичностью
- **Построение доверия:** Подчеркивание надежности и стабильности

**Бизнес-контекст России:**
- **State Regulations (Государственное регулирование):** 44-ФЗ, валютное законодательство
- **Economic Environment (Экономическая среда):** Влияние санкций, импортозамещение
- **Local Competition (Местная конкуренция):** Российские vs международные решения
- **Payment Preferences (Предпочтения по оплате):** Безналичный расчет, рублевые операции

---

*Это вторая часть детального справочника. Продолжение следует в AGENTS_FUNCTIONS_GUIDE_PART3.md*