# Technical SEO Auditor - База знаний

> **Operational Level Agent**  
> Комплексный технический SEO аудит, Core Web Vitals, crawling, мобильная оптимизация

## 🎯 Роль и ответственность

### **Основные функции:**
- **Технический SEO аудит** - Полный анализ технических аспектов сайта
- **Core Web Vitals анализ** - LCP, FID, CLS оптимизация
- **Crawling & Indexing** - Анализ доступности для поисковых роботов
- **Mobile-First оптимизация** - Мобильная производительность и UX
- **Structured Data** - Schema.org разметка и rich snippets
- **Performance optimization** - Скорость загрузки и производительность
- **Security & HTTPS** - Анализ безопасности и сертификатов

### **Целевые KPI:**
- **95+ Technical SEO score** - Общий технический балл
- **Core Web Vitals в зеленой зоне** - Все метрики Google
- **<50 технических ошибок** - Критические проблемы
- **85+ Mobile score** - Мобильная оптимизация
- **HTTPS A+ grade** - Безопасность соединения

## 📊 Core Web Vitals стандарты

### **Google Core Web Vitals (2024-2025):**

#### **Основные метрики:**
```yaml
core_web_vitals_thresholds:
  lcp_largest_contentful_paint:
    good: "< 2.5 seconds"
    needs_improvement: "2.5 - 4.0 seconds"
    poor: "> 4.0 seconds"
    
  fid_first_input_delay:
    good: "< 100 milliseconds"
    needs_improvement: "100 - 300 milliseconds"
    poor: "> 300 milliseconds"
    
  cls_cumulative_layout_shift:
    good: "< 0.1"
    needs_improvement: "0.1 - 0.25"
    poor: "> 0.25"
```

#### **Дополнительные метрики:**
```yaml
additional_metrics:
  fcp_first_contentful_paint:
    good: "< 1.8 seconds"
    needs_improvement: "1.8 - 3.0 seconds"
    poor: "> 3.0 seconds"
    
  ttfb_time_to_first_byte:
    good: "< 600 milliseconds"
    needs_improvement: "600 - 1600 milliseconds"
    poor: "> 1600 milliseconds"
    
  speed_index:
    good: "< 3.4 seconds"
    needs_improvement: "3.4 - 5.8 seconds"
    poor: "> 5.8 seconds"
```

#### **Оптимизация Core Web Vitals:**

**LCP (Largest Contentful Paint) оптимизация:**
- Оптимизация изображений (WebP, AVIF)
- Улучшение времени ответа сервера (TTFB)
- Устранение render-blocking ресурсов
- Использование CDN для статических ресурсов
- Preload ключевых ресурсов

**FID (First Input Delay) оптимизация:**
- Минификация и compression JavaScript
- Code splitting и lazy loading
- Оптимизация main thread работы
- Устранение long tasks (>50ms)
- Web Workers для тяжелых вычислений

**CLS (Cumulative Layout Shift) исправление:**
- Указание размеров изображений и видео
- Резервирование места для рекламы
- Избегание динамического контента над fold
- Оптимизация web fonts загрузки
- Стабильные CSS animations

## 🕷️ Crawling & Indexing оптимизация

### **Robots.txt лучшие практики:**

#### **Корректный robots.txt:**
```robots
User-agent: *
Disallow: /admin/
Disallow: /private/
Disallow: /*?*sessionid=
Disallow: /*?*sort=
Allow: /

# Specific bot directives
User-agent: Googlebot
Crawl-delay: 1

User-agent: Yandex
Crawl-delay: 2
Disallow: /search/

# Sitemap location
Sitemap: https://example.com/sitemap.xml
Sitemap: https://example.com/news-sitemap.xml
```

#### **Распространенные ошибки robots.txt:**
- Блокировка CSS/JS файлов
- Неправильные wildcards
- Отсутствие Sitemap директивы
- Блокировка важных страниц
- Синтаксические ошибки

### **XML Sitemap оптимизация:**

#### **Структура XML sitemap:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2025-01-01</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/important-page/</loc>
    <lastmod>2024-12-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

#### **Типы sitemap:**
- **XML Sitemap** - Основной файл карты сайта
- **Image Sitemap** - Для изображений
- **Video Sitemap** - Для видео контента
- **News Sitemap** - Для новостных сайтов
- **Mobile Sitemap** - Мобильные версии (устаревшее)

### **Canonical Tags правила:**

#### **Правильное использование canonical:**
```html
<!-- Self-referencing canonical -->
<link rel="canonical" href="https://example.com/page/" />

<!-- Cross-domain canonical -->
<link rel="canonical" href="https://example.com/original-page/" />

<!-- Parameter handling -->
<link rel="canonical" href="https://example.com/page/" />
<!-- For: https://example.com/page/?utm_source=google -->
```

#### **Canonical ошибки:**
- Множественные canonical теги
- Canonical на несуществующие страницы
- Canonical цепочки
- HTTP/HTTPS несоответствия
- Отсутствие canonical на важных страницах

## 📱 Mobile-First оптимизация

### **Mobile-First Indexing требования:**

#### **Viewport meta tag:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

#### **Responsive design принципы:**
```css
/* Mobile-first approach */
.container {
  width: 100%;
  padding: 10px;
}

/* Tablet styles */
@media (min-width: 768px) {
  .container {
    max-width: 750px;
    margin: 0 auto;
  }
}

/* Desktop styles */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    padding: 20px;
  }
}
```

#### **Touch элементы стандарты:**
- Минимальный размер: 44x44px
- Расстояние между элементами: 8px+
- Легкодоступные навигационные элементы
- Оптимизированные формы для мобильных

### **Mobile Performance оптимизация:**

#### **Критические факторы:**
- Compressed images (WebP, AVIF)
- Минимизированный CSS/JS
- Critical CSS inlining
- Lazy loading изображений
- Service Workers кэширование

#### **Mobile-specific проблемы:**
- Медленные 3G соединения
- Ограниченный CPU mobile устройств
- Батарея и энергопотребление
- Варьирующиеся размеры экранов
- Touch vs mouse взаимодействие

## 🔗 Structured Data & Schema.org

### **Основные Schema.org типы:**

#### **Organization Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-123-4567",
    "contactType": "customer service"
  },
  "sameAs": [
    "https://www.facebook.com/example",
    "https://twitter.com/example",
    "https://www.linkedin.com/company/example"
  ]
}
```

#### **Product Schema (E-commerce):**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "description": "Product description",
  "image": "https://example.com/product-image.jpg",
  "sku": "12345",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "price": "99.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "Example Store"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "123"
  }
}
```

#### **Article Schema (Content):**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "description": "Article description",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2025-01-01",
  "dateModified": "2025-01-02",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/article/"
  }
}
```

### **Rich Snippets возможности:**

#### **По типам контента:**
```yaml
rich_snippets_opportunities:
  ecommerce:
    - Product rich snippets
    - Review stars
    - Price and availability
    - Shipping information
    
  content_sites:
    - Article snippets
    - Author information
    - Publication date
    - Breadcrumbs
    
  local_business:
    - Business information
    - Reviews and ratings
    - Hours of operation
    - Location and map
    
  service_providers:
    - Service descriptions
    - FAQ sections
    - How-to guides
    - Contact information
```

## 🔧 Technical Foundation чеклист

### **HTML/CSS/JS Validation:**

#### **HTML5 Validation:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <!-- Proper HTML structure -->
</head>
<body>
  <!-- Semantic HTML5 elements -->
  <header>
    <nav><!-- Navigation --></nav>
  </header>
  <main>
    <article><!-- Main content --></article>
    <aside><!-- Sidebar --></aside>
  </main>
  <footer><!-- Footer --></footer>
</body>
</html>
```

#### **CSS Optimization:**
```css
/* Critical CSS inlining */
.above-fold {
  /* Styles for above-the-fold content */
}

/* Non-critical CSS loading */
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

#### **JavaScript Optimization:**
```javascript
// Async/defer loading
<script src="script.js" async></script>
<script src="script.js" defer></script>

// Code splitting
const module = await import('./module.js');

// Service Worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

### **Image Optimization стандарты:**

#### **Современные форматы:**
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description" loading="lazy">
</picture>
```

#### **Responsive Images:**
```html
<img srcset="small.jpg 480w, medium.jpg 800w, large.jpg 1200w"
     sizes="(max-width: 480px) 100vw, (max-width: 800px) 50vw, 25vw"
     src="fallback.jpg" alt="Description">
```

## 🔒 Security & HTTPS лучшие практики

### **SSL/TLS Configuration:**

#### **SSL Grade A+ требования:**
- TLS 1.2+ (TLS 1.3 recommended)
- Strong cipher suites
- HSTS (HTTP Strict Transport Security)
- Certificate transparency
- OCSP stapling

#### **Security Headers:**
```nginx
# HTTPS redirect
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# Content Security Policy
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'";

# Other security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

### **Mixed Content Issues:**
- HTTP resources на HTTPS страницах
- Insecure forms
- HTTP redirects
- Third-party HTTP widgets
- Legacy hardcoded HTTP links

## 🌍 International SEO оптимизация

### **Hreflang Implementation:**

#### **HTML hreflang tags:**
```html
<link rel="alternate" hreflang="en" href="https://example.com/en/" />
<link rel="alternate" hreflang="es" href="https://example.com/es/" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/" />
<link rel="alternate" hreflang="x-default" href="https://example.com/" />
```

#### **XML Sitemap hreflang:**
```xml
<url>
  <loc>https://example.com/en/</loc>
  <xhtml:link rel="alternate" hreflang="en" href="https://example.com/en/"/>
  <xhtml:link rel="alternate" hreflang="es" href="https://example.com/es/"/>
  <xhtml:link rel="alternate" hreflang="fr" href="https://example.com/fr/"/>
</url>
```

### **Geo-targeting настройка:**
- Google Search Console geo-targeting
- ccTLD vs subdirectory vs subdomain
- Local hosting and CDN
- Currency and language localization
- Local business schema markup

## 🛠️ Инструменты технического аудита

### **Essential Crawling Tools:**

#### **Screaming Frog SEO Spider:**
```yaml
crawling_checks:
  basic_crawl:
    - URL structure analysis
    - Title and meta descriptions
    - H1-H6 headings structure
    - Internal linking analysis
    
  advanced_crawl:
    - JavaScript rendering
    - AMP page validation
    - Structured data extraction
    - Custom extractions
```

#### **Google Tools:**
```yaml
google_tools:
  search_console:
    - Index coverage reports
    - Core Web Vitals data
    - Mobile usability issues
    - Rich results testing
    
  pagespeed_insights:
    - Lab data analysis
    - Field data (CrUX)
    - Optimization suggestions
    - Core Web Vitals scoring
```

### **Performance Testing Tools:**

#### **WebPageTest Configuration:**
```javascript
// Advanced WebPageTest settings
{
  "location": "Dulles:Chrome",
  "connectivity": "3G",
  "runs": 3,
  "firstViewOnly": false,
  "video": true,
  "lighthouse": true
}
```

#### **GTmetrix Monitoring:**
- Performance scores
- PageSpeed and YSlow metrics
- Waterfall analysis
- Historical performance data

### **Validation Tools:**

#### **Schema.org Validators:**
- Google Rich Results Test
- Schema.org Structured Data Testing Tool
- Facebook Open Graph Debugger
- Twitter Card Validator

#### **HTML/CSS Validators:**
- W3C Markup Validator
- W3C CSS Validator
- WAVE Web Accessibility Evaluator
- Lighthouse accessibility audit

## 📋 Audit процессы и шаблоны

### **Full Technical Audit Process:**

#### **Phase 1: Discovery (1-2 дня)**
1. **Site crawl** с Screaming Frog
2. **Google Search Console** анализ
3. **Core Web Vitals** baseline
4. **Mobile-friendliness** проверка
5. **HTTPS/Security** audit

#### **Phase 2: Deep Analysis (3-5 дней)**
1. **Structured data** анализ
2. **International SEO** проверка
3. **Performance** оптимизация
4. **Accessibility** compliance
5. **Competitive** benchmarking

#### **Phase 3: Reporting (1-2 дня)**
1. **Executive summary** создание
2. **Prioritized recommendations**
3. **Implementation timeline**
4. **ROI projections**
5. **Next steps** планирование

### **Critical Issues Priority Matrix:**

#### **Priority Levels:**
```yaml
critical_priority:
  - Core Web Vitals failing
  - Major crawling errors
  - HTTPS implementation missing
  - Mobile-unfriendly pages
  
high_priority:
  - Structured data missing
  - Page speed optimization
  - Canonical issues
  - Broken internal links
  
medium_priority:
  - Image optimization
  - CSS/JS minification
  - Meta descriptions missing
  - H1 tag optimization
  
low_priority:
  - HTML validation errors
  - CSS validation warnings
  - Minor accessibility issues
  - Optional schema markup
```

## 📊 Industry-specific технические требования

### **E-commerce Technical SEO:**
```yaml
ecommerce_priorities:
  critical_elements:
    - Product schema markup
    - Faceted navigation optimization
    - Duplicate content handling
    - Cart and checkout optimization
    
  performance_targets:
    - Product page load: <2 seconds
    - Category page speed: <3 seconds
    - Checkout conversion optimization
    - Mobile commerce experience
```

### **News/Media Sites:**
```yaml
news_media_priorities:
  critical_elements:
    - Article schema markup
    - AMP implementation
    - News sitemap
    - Publishing date accuracy
    
  performance_targets:
    - Article load time: <1.5 seconds
    - Google News compliance
    - Social media optimization
    - Ad loading optimization
```

### **Local Business SEO:**
```yaml
local_business_priorities:
  critical_elements:
    - LocalBusiness schema
    - NAP consistency
    - Google My Business optimization
    - Local citations accuracy
    
  mobile_focus:
    - Click-to-call optimization
    - Maps integration
    - Location-based content
    - Local reviews display
```

## 🔄 Continuous monitoring процедуры

### **Daily Monitoring:**
- Core Web Vitals metrics
- Crawl errors (Search Console)
- Site availability and uptime
- Critical page performance

### **Weekly Monitoring:**
- New indexed pages
- Mobile usability issues
- Security scan results
- Performance trends analysis

### **Monthly Monitoring:**
- Full site crawl analysis
- Competitive performance comparison
- Technical SEO score tracking
- ROI impact measurement

### **Quarterly Monitoring:**
- Complete technical audit
- Industry benchmark comparison
- Tool and process updates
- Strategy refinement

---

**Последнее обновление:** 2025-08-04  
**Версия:** 1.0  
**Ответственный:** Technical SEO Auditor Agent