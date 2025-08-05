# 🔗 Link Building Agent - Knowledge Base

## 📋 Роль и ответственности

**Link Building Agent** - операционный агент, специализирующийся на стратегиях наращивания ссылочной массы, outreach automation и анализе качества ссылок для улучшения позиций в поисковых системах.

### 🎯 **Основные задачи:**
- **Link prospect identification** - поиск и квалификация потенциальных доноров
- **Outreach automation** - автоматизация работы с аутрич-кампаниями
- **Link quality assessment** - анализ качества получаемых ссылок
- **Toxic link detection** - выявление вредных ссылок для дизавуа
- **Competitor backlink analysis** - анализ ссылочного профиля конкурентов

## 🔧 Технические возможности

### **Link Quality Scoring System:**
```python
quality_factors = {
    "domain_authority": {"weight": 0.25, "min_threshold": 30},
    "page_authority": {"weight": 0.20, "min_threshold": 25},
    "traffic_volume": {"weight": 0.15, "min_threshold": 5000},  # monthly organic
    "content_relevance": {"weight": 0.15, "min_threshold": 70},  # similarity %
    "spam_score": {"weight": 0.10, "max_threshold": 15},        # Moz spam score
    "trust_flow": {"weight": 0.10, "min_threshold": 20},        # Majestic metric
    "citation_flow": {"weight": 0.05, "min_threshold": 15}      # Majestic metric
}

link_quality_tiers = {
    "premium": {"score_range": [80, 100], "price": "50000-150000 ₽"},
    "high": {"score_range": [60, 79], "price": "25000-50000 ₽"},
    "medium": {"score_range": [40, 59], "price": "10000-25000 ₽"},
    "low": {"score_range": [20, 39], "price": "5000-10000 ₽"},
    "toxic": {"score_range": [0, 19], "action": "disavow"}
}
```

### **Outreach Strategy Framework:**
```yaml
outreach_strategies:
  guest_posting:
    description: "Guest articles на релевантных сайтах"
    success_rate: "15-25%"
    average_da: "40-60"
    timeline: "4-8 weeks"
    cost_per_link: "15000-35000 ₽"
    
  resource_page:
    description: "Размещение в подборках ресурсов"
    success_rate: "20-30%"
    average_da: "35-55"
    timeline: "2-4 weeks"
    cost_per_link: "8000-20000 ₽"
    
  broken_link_building:
    description: "Замена битых ссылок"
    success_rate: "10-15%"
    average_da: "45-65"
    timeline: "3-6 weeks"
    cost_per_link: "12000-28000 ₽"
    
  skyscraper_technique:
    description: "Контент лучше конкурентов"
    success_rate: "8-12%"
    average_da: "50-70"
    timeline: "8-12 weeks"
    cost_per_link: "25000-60000 ₽"
    
  haro_pr:
    description: "Help A Reporter Out"
    success_rate: "5-10%"
    average_da: "60-80"
    timeline: "2-8 weeks"
    cost_per_link: "0-15000 ₽"
    
  digital_pr:
    description: "Пресс-релизы и PR кампании"
    success_rate: "12-18%"
    average_da: "55-75"
    timeline: "4-10 weeks"
    cost_per_link: "20000-80000 ₽"
```

### **Link Prospecting Criteria:**
```python
prospect_filters = {
    "domain_metrics": {
        "min_da": 30,
        "min_pa": 25,
        "max_spam_score": 15,
        "min_traffic": 5000,
        "min_trust_flow": 20
    },
    "content_relevance": {
        "topic_match": 70,        # % similarity
        "language": "ru",
        "geo_relevance": "russia",
        "industry_match": True
    },
    "technical_health": {
        "site_speed": 3.0,        # seconds LCP
        "mobile_friendly": True,
        "https_enabled": True,
        "indexation_rate": 80     # % indexed pages
    },
    "outreach_potential": {
        "contact_info_available": True,
        "social_media_active": True,
        "content_update_frequency": "weekly",
        "guest_posts_accepted": True
    }
}
```

## 📊 Link Building Strategies

### **Tier-Based Link Building:**
```yaml
tier_1_links:
  description: "Высокоавторитетные прямые ссылки"
  targets:
    - da_range: "70-90+"
    - traffic: "100,000+ monthly"
    - industries: ["news", "government", "education"]
  cost_per_link: "50,000-200,000 ₽"
  monthly_target: "2-5 links"
  
tier_2_links:
  description: "Качественные нишевые сайты"
  targets:
    - da_range: "40-70"
    - traffic: "20,000-100,000 monthly"
    - industries: ["business", "tech", "industry-specific"]
  cost_per_link: "15,000-50,000 ₽"
  monthly_target: "5-15 links"
  
tier_3_links:
  description: "Массовые релевантные ссылки"
  targets:
    - da_range: "20-40"
    - traffic: "5,000-20,000 monthly"
    - industries: ["blogs", "forums", "directories"]
  cost_per_link: "3,000-15,000 ₽"
  monthly_target: "15-30 links"
```

### **Content-Based Link Attraction:**
```python
content_types_for_links = {
    "research_studies": {
        "link_magnet_power": 9.5,
        "average_links": 150,
        "production_cost": "300,000-800,000 ₽",
        "timeline": "8-12 weeks"
    },
    "industry_reports": {
        "link_magnet_power": 8.5,
        "average_links": 85,
        "production_cost": "200,000-500,000 ₽", 
        "timeline": "6-10 weeks"
    },
    "infographics": {
        "link_magnet_power": 7.5,
        "average_links": 45,
        "production_cost": "50,000-150,000 ₽",
        "timeline": "2-4 weeks"
    },
    "tools_calculators": {
        "link_magnet_power": 8.0,
        "average_links": 120,
        "production_cost": "400,000-1,000,000 ₽",
        "timeline": "8-16 weeks"
    },
    "expert_interviews": {
        "link_magnet_power": 6.5,
        "average_links": 25,
        "production_cost": "100,000-300,000 ₽",
        "timeline": "4-6 weeks"
    }
}
```

## 🚨 Toxic Link Detection

### **Red Flags для Disavow:**
```python
toxic_signals = {
    "domain_level": {
        "spam_score": "> 50",
        "malware_detected": True,
        "adult_content": True,
        "gambling_pharma": True,
        "private_blog_network": True,
        "link_farm": True
    },
    "page_level": {
        "excessive_outbound_links": "> 100",
        "irrelevant_content": True,
        "poor_user_experience": True,
        "auto_generated_content": True,
        "comment_spam": True
    },
    "link_attributes": {
        "anchor_text_over_optimization": "> 80%",
        "sitewide_links": True,
        "footer_sidebar_links": True,
        "hidden_links": True,
        "redirect_chains": "> 3"
    },
    "behavioral_signals": {
        "sudden_link_velocity": "> 1000 links/month",
        "low_quality_neighbors": "> 70%",
        "geographic_mismatch": True,
        "suspicious_link_patterns": True
    }
}
```

### **Disavow Strategy:**
```yaml
disavow_process:
  identification:
    tools: ["Google Search Console", "Ahrefs", "Majestic"]
    frequency: "Monthly review"
    criteria: "Spam score >30 OR manual penalty risk"
    
  documentation:
    format: "Detailed spreadsheet with reasons"
    categories: ["Spam", "Malware", "PBN", "Unnatural", "Irrelevant"]
    evidence: "Screenshots and metric data"
    
  submission:
    file_format: "disavow.txt"
    update_frequency: "Quarterly or after penalty"
    monitoring: "Rankings and traffic impact"
```

## 📈 Outreach Automation Framework

### **Email Templates по типам:**
```yaml
guest_post_outreach:
  subject_lines:
    - "Guest post collaboration for [DOMAIN]"
    - "[TOPIC] expert content for your audience"
    - "High-quality content partnership proposal"
  
  personalization_fields:
    - website_name
    - recent_article_title
    - author_name
    - specific_topic_gap
    
  follow_up_sequence:
    - day_0: Initial outreach
    - day_7: Soft follow-up
    - day_14: Value-added follow-up
    - day_30: Final attempt

resource_page_outreach:
  subject_lines:
    - "Resource addition for your [TOPIC] page"
    - "Valuable tool for your [CATEGORY] collection"
    - "Enhancement for your resource list"
    
  content_requirements:
    - relevance_explanation
    - unique_value_proposition
    - quality_credentials
    - social_proof
```

### **Success Rate Optimization:**
```python
outreach_optimization = {
    "personalization_level": {
        "basic": {"success_rate": "5-8%", "effort": "low"},
        "moderate": {"success_rate": "12-18%", "effort": "medium"},
        "high": {"success_rate": "25-35%", "effort": "high"}
    },
    "timing_factors": {
        "best_days": ["Tuesday", "Wednesday", "Thursday"],
        "best_times": ["9-11 AM", "2-4 PM"],
        "avoid_times": ["Monday morning", "Friday afternoon"],
        "timezone": "Moscow time preferred"
    },
    "follow_up_optimization": {
        "sequence_length": "3-4 emails maximum",
        "interval": "7-10 days between emails",
        "value_addition": "New info/resource each follow-up"
    }
}
```

## 🎯 ROI & Performance Tracking

### **Link Building KPIs:**
```yaml
performance_metrics:
  quantity_metrics:
    - links_acquired: "Monthly count"
    - referring_domains: "Unique domains"
    - link_velocity: "Links per week"
    - outreach_volume: "Emails sent"
    
  quality_metrics:
    - average_da: "Domain Authority"
    - average_tf: "Trust Flow"
    - relevance_score: "Topic match %"
    - link_placement: "Editorial vs footer"
    
  efficiency_metrics:
    - success_rate: "Links acquired / outreach sent"
    - cost_per_link: "Total spend / links acquired"
    - time_to_placement: "Days from outreach to live"
    - response_rate: "Replies / emails sent"
    
  impact_metrics:
    - ranking_improvements: "Position gains"
    - organic_traffic_lift: "Traffic increase %"
    - domain_authority_gain: "DA improvements"
    - brand_mentions: "Unlinked mentions"
```

### **ROI Calculation Framework:**
```python
def calculate_link_building_roi(campaign_data):
    total_investment = campaign_data['budget'] + campaign_data['time_cost']
    
    # Direct impact
    ranking_improvements = campaign_data['avg_position_gain']
    traffic_increase = campaign_data['organic_traffic_lift']
    conversion_value = traffic_increase * campaign_data['conversion_rate'] * campaign_data['avg_order_value']
    
    # Long-term value (links compound over time)
    link_lifespan = 24  # months average
    compound_value = conversion_value * link_lifespan * 0.8  # decay factor
    
    # Brand value
    brand_value = campaign_data['brand_mentions'] * 5000  # ₽ per mention
    
    total_value = compound_value + brand_value
    roi_percentage = ((total_value - total_investment) / total_investment) * 100
    
    return {
        "roi_percentage": roi_percentage,
        "total_value": total_value,
        "payback_period_months": total_investment / (conversion_value * 12),
        "cost_per_ranking_improvement": total_investment / ranking_improvements
    }
```

## 🔍 Competitor Analysis Framework

### **Backlink Gap Analysis:**
```python
competitor_analysis = {
    "link_gaps": {
        "methodology": "Identify competitor links we don't have",
        "tools": ["Ahrefs", "SEMrush", "Majestic"],
        "prioritization": "DA + relevance + obtainability",
        "action": "Outreach to gap opportunities"
    },
    "content_gaps": {
        "methodology": "Find linkable content we're missing",
        "analysis": "Competitor content with most backlinks",
        "opportunity": "Create superior versions",
        "timeline": "2-6 months production"
    },
    "strategy_gaps": {
        "methodology": "Analyze competitor link building tactics",
        "insights": "Successful outreach patterns",
        "adaptation": "Improve our approaches",
        "innovation": "Identify untapped opportunities"
    }
}
```

## 🔄 Automated Workflows

### **Daily Tasks:**
```python
daily_automation = [
    "new_prospect_discovery",        # Find new link opportunities
    "backlink_monitoring",           # Track new/lost links
    "toxic_link_detection",          # Scan for harmful links
    "outreach_follow_ups",           # Send scheduled follow-ups
    "competitor_link_alerts",        # Monitor competitor gains
    "brand_mention_tracking"         # Unlinked mention detection
]
```

### **Weekly Tasks:**
```python
weekly_automation = [
    "prospect_qualification",        # Score and prioritize prospects
    "outreach_campaign_analysis",    # Performance review
    "link_placement_verification",   # Confirm links are live
    "content_ideation",              # Linkable asset ideas
    "relationship_nurturing",        # Maintain publisher relationships
    "competitive_intelligence"       # Deeper competitor analysis
]
```

### **Monthly Tasks:**
```python
monthly_automation = [
    "link_audit_comprehensive",      # Full backlink profile review
    "strategy_optimization",         # Refine based on performance
    "disavow_file_update",          # Update toxic link list
    "roi_calculation",              # Campaign performance analysis
    "budget_allocation",            # Optimize spend distribution
    "team_training"                 # Update outreach training
]
```

## 💼 Budget Allocation Framework

### **Budget Distribution по каналам:**
```yaml
budget_allocation:
  tier_1_premium: "40%"     # High DA, news sites, government
  tier_2_quality: "35%"     # Industry sites, quality blogs
  tier_3_volume: "15%"      # Mass outreach, directories
  content_creation: "7%"    # Linkable assets production
  tools_software: "3%"      # Outreach and monitoring tools

monthly_budgets_by_client_size:
  enterprise: "500,000-2,000,000 ₽"
  mid_market: "200,000-500,000 ₽"
  small_business: "50,000-200,000 ₽"
  startup: "20,000-50,000 ₽"
```

---

**Последнее обновление:** 2025-08-05  
**Версия:** 1.0  
**Совместимость:** AI SEO Architects v1.3+