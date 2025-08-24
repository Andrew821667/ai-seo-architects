# 🤖 ИИ Поисковые Архитекторы - Детальный справочник функций агентов (Часть 2)

**Продолжение детального описания агентов Уровня Управления и Операционного Уровня**

---

### **5. Менеджер технических операций поисковой оптимизации**

#### **Роль и ответственность**
Менеджер технических операций поисковой оптимизации координирует все технические аспекты оптимизации, управляет техническими аудитами и обеспечивает соответствие сайтов современным стандартам поисковых систем.

#### **Детальные технические функции:**

**`координация_технических_аудитов()`** - Координация технических аудитов поисковой оптимизации
- **Определение области аудита:**
  - **Оценка сканируемости:** robots.txt (файл robots.txt), карты сайта, внутренняя перелинковка
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
- **Performance Optimization Strategies (стратегии оптимизации производительности):**
  - Image optimization and WebP conversion (оптимизация изображений и конверсия в WebP)
  - Critical CSS implementation (реализация критических CSS)
  - JavaScript optimization and code splitting (оптимизация JavaScript и разделение кода)
  - Server-side rendering (SSR) considerations (соображения по серверному рендерингу)

**`управление_бюджетами_сканирования()`** - Управление бюджетами сканирования
- **Оптимизация бюджета сканирования:**
  - **Определение приоритетных страниц:** Высокоценные страницы для поисковых систем
  - **Устранение излишнего сканирования:** Удаление малоценных страниц из сканирования
  - **Оптимизация внутренних ссылок:** Направление сканеров к важному контенту
  - **Оптимизация ответа сервера:** Сокращение времени сканирования и ресурсов
- **Log File Analysis (анализ лог-файлов):**
  - Googlebot and Yandex bot crawling patterns (паттерны сканирования Googlebot и Yandex bot)
  - Crawl frequency by page type (частота сканирования по типам страниц)
  - HTTP status code distribution (распределение HTTP статус-кодов)
  - Crawl depth and path analysis (анализ глубины и путей сканирования)
- **Российская специфика поисковых систем:**
  - **Поведение краулера Яндекса:** Понимание предпочтений робота Яндекса
  - **Региональные паттерны сканирования:** Москва, СПб, региональные различия
  - **Мобильно-первое индексирование:** Адаптация к мобильному индексированию Яндекса

**`optimize_site_performance()`** - Оптимизация производительности сайтов
- **Frontend Optimization (оптимизация фронтенда):**
  - **Critical Rendering Path Optimization (оптимизация критического пути рендеринга)**
  - **Resource Loading Prioritization (приоритизация загрузки ресурсов)**
  - **CSS and JavaScript Minification (минификация CSS и JavaScript)**
  - **Image Lazy Loading Implementation (реализация отложенной загрузки изображений)**
- **Backend Optimization (оптимизация бэкенда):**
  - **Database Query Optimization (оптимизация запросов к базе данных)**
  - **Caching Strategy Implementation (реализация стратегии кэширования)** (Redis, Memcached)
  - **CDN Configuration (конфигурация CDN)** (CloudFlare, Yandex CDN for Russian market (для российского рынка))
  - **Server Response Time Optimization (оптимизация времени отклика сервера)**
- **Mobile Performance (мобильная производительность):**
  - **Responsive Design Optimization (оптимизация адаптивного дизайна)**
  - **Touch Interaction Optimization (оптимизация сенсорного взаимодействия)**
  - **Mobile-Specific Resource Loading (мобильно-специфичная загрузка ресурсов)**
  - **Progressive Web App (PWA) Implementation (реализация прогрессивных веб-приложений)**

#### **Детальные бизнесовые функции:**

**`prioritize_technical_fixes()`** - Приоритизация технических исправлений
- **Business Impact Assessment (оценка бизнес-влияния):**
  - **Revenue Impact (воздействие на доход):** Direct correlation with conversion rates (прямая корреляция с конверсиями)
  - **Traffic Impact (воздействие на трафик):** Potential organic traffic gains (потенциальный прирост органического трафика)
  - **User Experience Impact (воздействие на пользовательский опыт):** Effect on user satisfaction metrics (влияние на метрики удовлетворенности пользователей)
  - **Brand Impact (воздействие на бренд):** Professional appearance and credibility (профессиональный вид и доверие)
- **Implementation Cost Analysis (анализ стоимости реализации):**
  - **Development Time (время разработки):** Required developer hours (необходимые часы разработчика)
  - **Resource Requirements (потребности в ресурсах):** Specialized skills needed (необходимые специализированные навыки)
  - **Testing Requirements (требования к тестированию):** QA and validation time (время контроля качества и валидации)
  - **Risk Assessment (оценка рисков):** Potential negative impacts (потенциальные негативные воздействия)
- **ROI Calculation Framework (схема расчета возврата инвестиций):**
  - Expected traffic increase (ожидаемый прирост трафика) × Conversion rate (конверсия) × Average order value (средний чек)
  - Implementation cost (стоимость реализации) (development + testing + deployment)(разработка + тестирование + развертывание)
  - Payback period calculation (расчет срока окупаемости)
  - Risk-adjusted ROI (скорректированная на риск рентабельность инвестиций)

**`manage_technical_resources()`** - Управление техническими ресурсами
- **Team Resource Allocation (распределение командных ресурсов):**
  - **Frontend Developers (фронтенд-разработчики):** UI/UX optimization, performance improvements (оптимизация UI/UX, улучшение производительности)
  - **Backend Developers (бэкенд-разработчики):** Server optimization, database tuning (оптимизация сервера, настройка базы данных)
  - **DevOps Engineers (инженеры DevOps):** Infrastructure, deployment, monitoring (инфраструктура, развертывание, мониторинг)
  - **SEO Technicians (SEO-техники):** Implementation verification, testing (проверка реализации, тестирование)
- **Tool and Technology Management (управление инструментами и технологиями):**
  - **SEO Tools Budget (бюджет SEO-инструментов):** Screaming Frog, DeepCrawl, Serpstat subscriptions (подписки)
  - **Development Tools (средства разработки):** IDE licenses, testing frameworks (лицензии IDE, фреймворки для тестирования)
  - **Infrastructure Costs (затраты на инфраструктуру):** Servers, CDN, monitoring tools (серверы, CDN, инструменты мониторинга)
  - **Training and Certification (обучение и сертификация):** Team skill development (развитие навыков команды)

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
- **Business Performance Metrics (метрики бизнес-производительности):**
  - **Conversion Rates (конверсия):** Organic traffic to lead/sale conversion (конверсия органического трафика в лиды/продажи)
  - **Revenue Attribution (атрибуция выручки):** SEO's contribution to business revenue (вклад SEO в выручку бизнеса)
  - **Customer Acquisition Cost (стоимость привлечения клиента):** CAC through organic channel (CAC через органический канал)
  - **Lifetime Value (жизненная стоимость):** LTV of customers acquired through SEO (LTV клиентов, привлеченных через SEO)
- **Technical Health Metrics (метрики технического здоровья):**
  - **Core Web Vitals:** Performance trending
  - **Crawl Errors (ошибки сканирования):** Technical issues monitoring (мониторинг технических проблем)
  - **Site Health Score (оценка здоровья сайта):** Overall technical SEO health (общее техническое SEO-здоровье)
  - **Mobile Performance (мобильная производительность):** Mobile-specific metrics

**`implement_health_scoring()`** - Реализация системы оценки здоровья аккаунтов
- **Health Score Components (компоненты оценки здоровья) (100-point scale) (100-балльная шкала):**
  - **Performance (производительность) (40 points) (40 баллов):** Traffic, rankings, conversions (трафик, рейтинги, конверсии)
  - **Engagement (вовлеченность) (25 points) (25 баллов):** Meeting attendance, response rates (посещаемость собраний, частота ответов)
  - **Growth (рост) (20 points) (20 баллов):** Account expansion, additional services (расширение аккаунта, дополнительные услуги)
  - **Satisfaction (удовлетворенность) (15 points) (15 баллов):** Survey scores, feedback quality (оценки опросов, качество обратной связи)
- **Risk Indicators (индикаторы рисков):**
  - **Red Flags (красные флажки) (0-50 points) (0-50 баллов):** High churn risk, immediate intervention needed (высокий риск оттока, нужно немедленное вмешательство)
  - **Yellow Flags (желтые флажки) (51-70 points) (51-70 баллов):** At-risk, proactive engagement required (в группе риска, требуется проактивное взаимодействие)
  - **Green Status (зеленый статус) (71-100 points) (71-100 баллов):** Healthy account, expansion opportunity (здоровый аккаунт, возможность расширения)
- **Automated Alerting (автоматические оповещения):**
  - Score drop triggers for immediate action (триггеры падения оценки для немедленных действий)
  - Trend analysis for predictive insights (анализ трендов для прогнозных инсайтов)
  - Escalation procedures for critical accounts (процедуры эскалации для критичных аккаунтов)

**`automate_success_workflows()`** - Автоматизация workflow успеха клиентов
- **Onboarding Automation (автоматизация ввода в курс дела):**
  - **Welcome Sequence (приветственная последовательность):** Automated email series for new clients (автоматическая серия писем для новых клиентов)
  - **Goal Setting Process (процесс постановки целей):** Structured approach to KPI definition (структурированный подход к определению KPI)
  - **Initial Setup (первоначальная настройка):** Account configuration and baseline establishment (конфигурация аккаунта и установка базовой линии)
  - **First Value Delivery (первая ценность):** Quick wins to demonstrate value (быстрые победы для демонстрации ценности)
- **Ongoing Success Workflows (текущие рабочие процессы успеха):**
  - **Regular Check-ins (регулярные проверки):** Automated scheduling and reminder systems (автоматическое планирование и системы напоминаний)
  - **Performance Reporting (отчетность по производительности):** Automated report generation and delivery (автоматическое создание и доставка отчетов)
  - **Issue Detection (обнаружение проблем):** Proactive problem identification and alerting (проактивная идентификация проблем и оповещение)
  - **Renewal Preparation (подготовка к продлению):** Automated renewal timeline and materials (автоматические сроки и материалы для продления)

#### **Детальные бизнесовые функции:**

**`develop_retention_strategies()`** - Разработка стратегий удержания
- **Retention Strategy Framework (схема стратегии удержания):**
  - **Value Demonstration (демонстрация ценности):** Regular ROI reporting and success story sharing (регулярная отчетность по ROI и дельж историями успеха)
  - **Proactive Support (проактивная поддержка):** Anticipating needs before problems arise (предвосхищение потребностей до возникновения проблем)
  - **Relationship Building (построение отношений):** Personal connections beyond business transactions (личные связи выше бизнес-транзакций)
  - **Continuous Improvement (непрерывное совершенствование):** Ongoing service enhancement and optimization (постоянное улучшение и оптимизация услуг)
- **Risk Mitigation Strategies (стратегии снижения рисков):**
  - **Early Warning System (система раннего предупреждения):** Behavioral indicators of potential churn (поведенческие индикаторы потенциального оттока)
  - **Intervention Protocols (протоколы вмешательства):** Specific actions for different risk levels (конкретные действия для разных уровней риска)
  - **Win-back Campaigns (кампании возврата):** Strategies for re-engaging disengaged clients (стратегии повторного вовлечения отстранившихся клиентов)
  - **Competitive Defense (конкурентная защита):** Protecting against competitor poaching (защита от атак конкурентов)
- **Success Metrics (метрики успеха):**
  - **Net Revenue Retention (NRR) (чистое удержание выручки):** >100% target through expansion (>100% цель через расширение)
  - **Gross Revenue Retention (GRR) (валовое удержание выручки):** >90% target for healthy retention (>90% цель для здорового удержания)
  - **Customer Satisfaction Score (CSAT) (оценка удовлетворенности клиентов):** >4.5/5.0 target (>4.5/5.0 цель)
  - **Net Promoter Score (NPS) (индекс потребительской лояльности):** >50 target for advocacy (>50 цель для рекомендаций)

**`identify_upselling_opportunities()`** - Выявление возможностей для upselling
- **Expansion Opportunity Mapping (картирование возможностей расширения):**
  - **Service Gaps (пробелы в услугах):** Areas where additional SEO services could help (области, где могут помочь дополнительные SEO-услуги)
  - **Performance Plateaus (плато производительности):** Situations requiring advanced strategies (ситуации, требующие продвинутых стратегий)
  - **New Business Initiatives (новые бизнес-инициативы):** Client growth creating new needs (рост клиента, создающий новые потребности)
  - **Competitive Pressures (конкурентное давление):** Market changes requiring enhanced services (изменения рынка, требующие расширенных услуг)
- **Upselling Categories (категории upselling):**
  - **Service Expansion (расширение услуг):** Additional SEO services (дополнительные SEO-услуги) (local, international, e-commerce) (локальные, международные, электронная коммерция)
  - **Technology Upgrades (обновления технологий):** Advanced tools and platforms (продвинутые инструменты и платформы)
  - **Consulting Services (консалтинговые услуги):** Strategic guidance and specialized expertise (стратегическое руководство и специализированная экспертиза)
  - **Training and Education (обучение и образование):** Client team capability building (создание компетенций команды клиента)
- **Timing and Approach (время и подход):**
  - **Success-Based Timing (время на основе успеха):** Upselling during positive performance periods (допродажи в периоды позитивных показателей)
  - **Need-Based Timing (время на основе потребностей):** Responding to specific business challenges (ответ на конкретные бизнес-вызовы)
  - **Relationship-Based Approach (подход на основе отношений):** Leveraging strong client relationships (использование сильных отношений с клиентами)
  - **Value-First Presentation (презентация с акцентом на ценность):** Leading with client benefit, not vendor need (начало с выгоды клиента, а не поставщика)

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
- **Source Performance Analysis (анализ производительности источников):**
  - **Organic Search (органический поиск):** Quality score, conversion rates, lifetime value (оценка качества, конверсия, жизненная стоимость)
  - **Paid Advertising (платная реклама):** Google Ads, Yandex.Direct, social media ads (реклама в соцсетях)
  - **Content Marketing (контент-маркетинг):** Blog posts, whitepapers, webinars (статьи в блогах, технические доклады, вебинары)
  - **Referrals (рекомендации):** Partner referrals, client referrals, word-of-mouth (рекомендации партнеров, клиентов, из уст в уста)
  - **Events (мероприятия):** Conferences, trade shows, networking events (конференции, выставки, нетворкинг-мероприятия)
- **Source Quality Metrics (метрики качества источников):**
  - **Lead-to-Opportunity Conversion (конверсия лид в возможность):** % of leads becoming qualified opportunities (% лидов, становящихся квалифицированными возможностями)
  - **Opportunity-to-Customer Conversion (конверсия возможность в клиента):** % of opportunities closing (% закрывающихся возможностей)
  - **Customer Lifetime Value (жизненная стоимость клиента):** Average LTV by source (средняя LTV по источникам)
  - **Cost Per Acquisition (стоимость привлечения):** Total cost to acquire customer by source (общая стоимость привлечения клиента по источникам)
- **Russian Market Source Specifics (специфика источников российского рынка):**
  - **Yandex Ecosystem (экосистема Яндекса):** Yandex.Direct, Yandex.Market presence (присутствие)
  - **Local Business Networks (местные бизнес-сети):** Russian B2B platforms and directories (российские B2B-платформы и каталоги)
  - **Industry Events (отраслевые мероприятия):** Russian marketing conferences and SEO events (российские маркетинговые конференции и SEO-мероприятия)
  - **Professional Communities (профессиональные сообщества):** SEO and digital marketing groups (SEO и диджитал-маркетинг группы)

**`implement_meddic_framework()`** - Применение MEDDIC методологии
- **Metrics (метрики) (20% от MEDDIC скора):**
  - **Quantifiable Business Metrics (количественные бизнес-метрики):** Revenue, traffic, conversion rates (выручка, трафик, конверсии)
  - **Success Criteria Definition (определение критериев успеха):** Specific, measurable outcomes (конкретные, измеримые результаты)
  - **Baseline Establishment (установка базовой линии):** Current performance measurement (измерение текущей производительности)
  - **Target Goals (целевые показатели):** Desired improvement levels and timelines (желаемые уровни улучшения и сроки)
- **Economic Buyer (экономический покупатель) (20% от MEDDIC скора):**
  - **Budget Authority Identification (определение бюджетного руководства):** Who controls the budget (кто контролирует бюджет)
  - **Financial Decision Process (процесс финансовых решений):** How budget decisions are made (как принимаются бюджетные решения)
  - **ROI Requirements (требования к ROI):** Expected return on investment thresholds (ожидаемые пороги возврата инвестиций)
  - **Budget Cycle Understanding (понимание бюджетного цикла):** When budget decisions are made (когда принимаются бюджетные решения)
- **Decision Criteria (критерии решений) (15% от MEDDIC скора):**
  - **Evaluation Criteria (критерии оценки):** How vendor selection decisions are made (как принимаются решения по выбору поставщика)
  - **Weighting Factors (весовые коэффициенты):** Which criteria are most important (какие критерии наиболее важны)
  - **Competitive Factors (конкурентные факторы):** What differentiates vendor options (что отличает варианты поставщиков)
  - **Risk Tolerance (толерантность к рискам):** Acceptable levels of implementation risk (приемлемые уровни риска реализации)
- **Decision Process (процесс принятия решений) (15% от MEDDIC скора):**
  - **Process Mapping (картирование процессов):** Steps in the decision-making process (этапы процесса принятия решений)
  - **Stakeholder Involvement (участие заинтересованных сторон):** Who participates in decisions (кто участвует в принятии решений)
  - **Timeline Understanding (понимание сроков):** How long the process takes (сколько времени занимает процесс)
  - **Approval Requirements (требования к согласованиям):** What approvals are needed (какие согласования необходимы)
- **Identify Pain (выявление болевых точек) (15% от MEDDIC скора):**
  - **Business Impact (бизнес-влияние):** How problems affect business outcomes (как проблемы влияют на бизнес-результаты)
  - **Urgency Level (уровень срочности):** How quickly problems need resolution (как быстро нужно решение проблем)
  - **Previous Attempts (предыдущие попытки):** What solutions have been tried (какие решения пробовали)
  - **Cost of Inaction (стоимость бездействия):** What happens if problems aren't solved (что происходит, если проблемы не решены)
- **Champion (чемпион/сторонник) (15% от MEDDIC скора):**
  - **Internal Advocate Identification (определение внутреннего сторонника):** Who supports the solution internally (кто поддерживает решение внутри компании)
  - **Influence Level (уровень влияния):** How much influence the champion has (какое влияние имеет чемпион)
  - **Relationship Quality (качество отношений):** Strength of relationship with champion (сила отношений с чемпионом)
  - **Champion Development (развитие чемпиона):** How to strengthen champion support (как усилить поддержку чемпиона)

#### **Детальные бизнесовые функции:**

**`assess_budget_authority()`** - Оценка бюджета и полномочий лида
- **Budget Discovery Techniques (методы выявления бюджета):**
  - **Direct Questioning (прямые вопросы):" "What budget range are you considering for SEO?" ("Какой бюджет вы рассматриваете для SEO?")
  - **Indirect Approaches (косвенные подходы):" "What did you invest in marketing last year?" ("Сколько вы инвестировали в маркетинг в прошлом году?")
  - **Benchmark Comparisons (сравнение с эталонами):" "Companies your size typically invest X in SEO" ("Компании вашего размера обычно инвестируют X в SEO")
  - **Value-Based Discussions (обсуждение на основе ценности):" "What would a 50% traffic increase be worth?" ("Чего стоило бы увеличение трафика на 50%?")
- **Authority Verification Methods (методы проверки полномочий):**
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
- **Stakeholder Mapping Framework (схема картирования заинтересованных сторон):**
  - **Economic Buyer (экономический покупатель):** Controls budget and final approval (контролирует бюджет и окончательное утверждение)
  - **Technical Buyer (технический покупатель):** Evaluates technical aspects and implementation (оценивает технические аспекты и реализацию)
  - **User Buyer (пользовательский покупатель):** Will use the service and affected by outcomes (будет использовать услугу и повлияет на результаты)
  - **Coach/Champion (тренер/чемпион):** Internal advocate supporting the purchase (внутренний сторонник, поддерживающий покупку)
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
- **Conversation Flow Analysis (анализ потока разговора):**
  - **Opening Effectiveness (эффективность открытия):** How well conversations start and engage prospects (насколько хорошо начинаются разговоры и вовлекают проспекты)
  - **Question Sequence Optimization (оптимизация последовательности вопросов):** Most effective order of SPIN questions (наиболее эффективная последовательность SPIN-вопросов)
  - **Transition Smoothness (плавность переходов):** How well conversations flow between topics (насколько хорошо разговоры перетекают между темами)
  - **Closing Strength (сила закрытия):** Effectiveness of moving to next steps (эффективность перехода к следующим шагам)
- **Language Pattern Recognition (распознавание языковых паттернов):**
  - **Buying Signals (сигналы покупки):** Words and phrases indicating purchase intent (слова и фразы, указывающие на намерение купить)
  - **Objection Patterns (паттерны возражений):** Common objection themes and timing (общие темы возражений и время)
  - **Engagement Indicators (индикаторы вовлеченности):** Verbal cues showing interest levels (вербальные сигналы, показывающие уровень интереса)
  - **Decision-Making Language (язык принятия решений):** Phrases indicating evaluation processes (фразы, указывающие на процессы оценки)
- **Outcome Prediction Modeling (моделирование прогноза результатов):**
  - **Conversation Quality Scoring (оценка качества разговора):** Based on SPIN methodology application (на основе применения методологии SPIN)
  - **Progression Probability (вероятность прогресса):** Likelihood of moving to next sales stage (вероятность перехода к следующему этапу продаж)
  - **Deal Size Indicators (индикаторы размера сделки):** Conversation elements correlating with larger deals (элементы разговора, коррелирующие с крупными сделками)
  - **Timeline Prediction (прогноз сроков):** Expected decision-making timeframes (ожидаемые сроки принятия решений)

#### **Российская специфика методологии СПИН:**

**Культурные адаптации:**
- **Построение отношений:** Больше времени на личные связи
- **Уважение иерархии:** Признание статуса и позиции
- **Прямая против косвенная коммуникация:** Баланс между прямотой и дипломатичностью
- **Построение доверия:** Подчеркивание надежности и стабильности

**Бизнес-контекст России:**
- **State Regulations (государственное регулирование):** 44-ФЗ, валютное законодательство
- **Economic Environment (экономическая среда):** Влияние санкций, импортозамещение
- **Local Competition (местная конкуренция):** Российские vs международные решения
- **Payment Preferences (предпочтения по оплате):** Безналичный расчет, рублевые операции

---

*Это вторая часть детального справочника. Продолжение следует в AGENTS_FUNCTIONS_GUIDE_PART3.md*