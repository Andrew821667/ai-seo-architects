# 🎯 Competitive Analysis Agent - Knowledge Base

## 📋 Роль и ответственности

**Competitive Analysis Agent** - операционный агент, специализирующийся на глубоком анализе конкурентов, SERP research, gap analysis и выявлении возможностей для обгона соперников в поисковой выдаче.

### 🎯 **Основные задачи:**
- **SERP analysis** - анализ поисковой выдачи по ключевым запросам
- **Competitor gap analysis** - выявление слабых мест конкурентов
- **Share of voice tracking** - отслеживание доли голоса в нише
- **Content gap identification** - поиск контентных возможностей
- **Technical advantage mapping** - анализ технических преимуществ

## 🔧 Технические возможности

### **SERP Analysis Framework:**
```python
serp_analysis_metrics = {
    "ranking_factors": {
        "content_quality": {"weight": 0.25, "measurement": "word_count, expertise, depth"},
        "technical_seo": {"weight": 0.20, "measurement": "page_speed, mobile_friendly, schema"},
        "backlink_profile": {"weight": 0.20, "measurement": "domain_authority, link_quality"},
        "user_experience": {"weight": 0.15, "measurement": "bounce_rate, time_on_page, CTR"},
        "content_freshness": {"weight": 0.10, "measurement": "last_updated, publication_date"},
        "brand_authority": {"weight": 0.10, "measurement": "brand_searches, mentions, trust"}
    },
    "serp_features": {
        "featured_snippets": {"opportunity_value": "high", "traffic_impact": "30-40%"},
        "people_also_ask": {"opportunity_value": "medium", "traffic_impact": "10-15%"},
        "image_packs": {"opportunity_value": "medium", "traffic_impact": "5-10%"},
        "video_results": {"opportunity_value": "high", "traffic_impact": "20-30%"},
        "local_pack": {"opportunity_value": "high", "traffic_impact": "25-35%"},
        "knowledge_panels": {"opportunity_value": "low", "traffic_impact": "brand"}
    }
}
```

### **Competitor Scoring Matrix:**
```yaml
competitor_strength_assessment:
  content_strategy:
    blog_frequency: "posts_per_month"
    content_depth: "avg_word_count"  
    topic_coverage: "keyword_clusters_covered"
    content_quality: "expert_score_1_10"
    
  technical_performance:
    site_speed: "core_web_vitals_score"
    mobile_optimization: "mobile_usability_score" 
    crawlability: "indexation_rate_percentage"
    schema_markup: "structured_data_coverage"
    
  backlink_authority:
    domain_authority: "moz_domain_authority"
    referring_domains: "unique_linking_domains"
    link_velocity: "new_links_monthly"
    link_quality: "avg_referring_domain_authority"
    
  social_presence:
    social_signals: "shares_mentions_combined"
    brand_awareness: "branded_search_volume"
    engagement_rate: "social_media_engagement"
    influencer_connections: "partnerships_count"
```

### **Gap Analysis Opportunities:**
```python
gap_analysis_framework = {
    "keyword_gaps": {
        "identification": "Keywords competitors rank for but we don't",
        "scoring": "search_volume * difficulty_inverse * relevance",
        "priority_matrix": {
            "quick_wins": {"volume": "1k-10k", "difficulty": "<30", "timeline": "1-3 months"},
            "strategic": {"volume": "10k+", "difficulty": "30-60", "timeline": "3-6 months"},
            "long_term": {"volume": "50k+", "difficulty": "60+", "timeline": "6-12 months"}
        }
    },
    "content_gaps": {
        "topic_clusters": "Missing topic coverage areas",
        "content_formats": "Video, infographic, tool opportunities",
        "content_depth": "Shallow content that can be improved",
        "user_intent": "Informational, commercial, navigational gaps"
    },
    "technical_gaps": {
        "site_speed": "Page load performance advantages",
        "mobile_optimization": "Mobile UX improvements",
        "structured_data": "Schema markup opportunities",
        "site_architecture": "URL structure and navigation"  
    },
    "backlink_gaps": {
        "link_opportunities": "Sites linking to competitors but not us",
        "content_assets": "Linkable content we're missing",
        "relationship_gaps": "Industry connections to build",
        "pr_opportunities": "Media coverage gaps"
    }
}
```

## 📊 Competitive Intelligence Framework

### **Market Share Analysis:**
```yaml
market_analysis_metrics:
  organic_visibility:
    share_of_voice: "percentage_of_total_keyword_visibility"
    ranking_distribution: "positions_1_3_vs_4_10_distribution"
    featured_snippet_ownership: "percentage_of_featured_snippets"
    serp_feature_dominance: "various_serp_features_captured"
    
  traffic_estimation:
    organic_traffic: "estimated_monthly_organic_visitors"
    paid_traffic: "estimated_ppc_traffic"
    social_traffic: "social_media_referrals"
    direct_traffic: "brand_search_driven_visits"
    
  content_performance:
    top_pages_traffic: "highest_performing_content"
    content_velocity: "new_content_publishing_rate"
    engagement_metrics: "time_on_page_bounce_rate"
    conversion_indicators: "lead_gen_conversion_signals"
```

### **Competitive Benchmarking:**
```python
benchmarking_categories = {
    "seo_performance": {
        "organic_keywords": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0},
        "organic_traffic": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0},
        "domain_authority": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0},
        "backlinks": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0}
    },
    "content_metrics": {
        "content_volume": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0},
        "avg_content_length": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0},
        "content_freshness": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0},
        "expert_content_ratio": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0}
    },
    "technical_performance": {
        "site_speed": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0},
        "mobile_score": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0},
        "core_web_vitals": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0},
        "crawl_efficiency": {"our_site": 0, "competitor_avg": 0, "best_competitor": 0}
    }
}
```

## 🎯 SERP Domination Strategy

### **SERP Feature Optimization:**
```yaml
serp_feature_strategies:
  featured_snippets:
    target_format: "paragraphs, lists, tables"
    content_structure: "question-answer format"
    optimization_tactics:
      - "Direct question targeting in H2/H3"
      - "Concise 40-50 word answers"
      - "Structured data markup"
      - "High-authority page targeting"
    
  people_also_ask:
    expansion_strategy: "Answer related questions comprehensively"
    content_approach: "FAQ sections and detailed Q&A"
    monitoring: "Track PAA box changes and new questions"
    
  image_optimization:
    visual_content: "High-quality, original images"
    alt_text: "Descriptive, keyword-rich alt tags"  
    file_naming: "SEO-friendly image file names"
    image_sitemaps: "Comprehensive image XML sitemaps"
    
  video_content:
    video_seo: "YouTube optimization for video results"
    embedded_videos: "Strategic video embedding on pages"
    video_schema: "VideoObject structured data"
    transcriptions: "Full video transcripts for indexing"
```

### **Content Superiority Framework:**
```python
content_superiority_metrics = {
    "comprehensiveness": {
        "word_count": "Target 2x competitor average",
        "topic_coverage": "Cover 100% of user questions",
        "depth_of_analysis": "Expert-level insights and data",
        "unique_information": "Exclusive data, research, quotes"
    },
    "user_experience": {
        "readability": "Flesch reading score optimization",
        "visual_elements": "Images, charts, infographics",
        "interactive_elements": "Calculators, tools, quizzes",
        "mobile_optimization": "Perfect mobile reading experience"
    },
    "authority_signals": {
        "expert_authors": "Industry expert bylines",
        "citations_sources": "Authoritative source citations",
        "original_research": "Primary data and studies",
        "expert_quotes": "Industry leader interviews"
    },
    "freshness_factors": {
        "publication_date": "Recent publication timestamps",
        "content_updates": "Regular content refreshes",
        "trending_topics": "Current industry trends coverage",
        "seasonal_relevance": "Timely, seasonal content updates"
    }
}
```

## 🔍 Competitive Monitoring System

### **Automated Tracking Metrics:**
```yaml
monitoring_automation:
  daily_tracking:
    - ranking_position_changes: "Track top 100 keyword positions"
    - serp_feature_changes: "Monitor featured snippet ownership"
    - new_content_detection: "Identify new competitor content"
    - backlink_acquisition: "Track new competitor backlinks"
    
  weekly_analysis:
    - content_gap_updates: "Refresh content opportunity analysis"
    - technical_performance: "Site speed and technical metrics"
    - social_media_activity: "Competitor social engagement"
    - paid_advertising_intel: "PPC campaign monitoring"
    
  monthly_reporting:
    - market_share_analysis: "Share of voice calculations"
    - competitive_landscape: "New competitors identification"
    - strategy_effectiveness: "Our performance vs competitors"
    - opportunity_prioritization: "Updated action recommendations"
```

### **Alert System Configuration:**
```python
competitive_alerts = {
    "ranking_threats": {
        "trigger": "Competitor gains 3+ positions on target keywords",
        "severity": "high",
        "action": "Immediate content optimization review"
    },
    "content_opportunities": {
        "trigger": "Competitor content gets 10k+ social shares",
        "severity": "medium", 
        "action": "Create superior version of content"
    },
    "backlink_threats": {
        "trigger": "Competitor acquires 5+ high DA links in week",
        "severity": "high",
        "action": "Accelerate link building efforts"
    },
    "serp_feature_loss": {
        "trigger": "Lose featured snippet to competitor",
        "severity": "critical",
        "action": "Emergency content optimization"
    },
    "new_competitor": {
        "trigger": "New domain appears in top 10 for target keywords",
        "severity": "medium",
        "action": "Full competitive analysis of new entrant"
    }
}
```

## 📈 Strategic Response Framework

### **Competitive Response Strategies:**
```yaml
response_strategies:
  defensive_tactics:
    content_improvement:
      - "Enhance existing content that competitors are targeting"
      - "Add unique value propositions to vulnerable pages"
      - "Increase content depth and expert analysis"
      - "Improve user engagement metrics"
      
    technical_fortification:
      - "Improve site speed beyond competitor benchmarks"
      - "Enhance mobile user experience"
      - "Implement advanced schema markup"
      - "Optimize core web vitals performance"
      
    link_defense:
      - "Strengthen backlink profile with high-authority links"
      - "Diversify link sources and anchor text"
      - "Build relationships with competitor link sources"
      - "Create linkable assets that outperform competitors"
  
  offensive_tactics:
    content_superiority:
      - "Create 10x better content than top-ranking competitors"
      - "Develop unique content formats (tools, calculators)"
      - "Publish expert interviews and original research"
      - "Target competitor content gaps with superior alternatives"
      
    serp_domination:
      - "Target featured snippets competitors own"
      - "Optimize for multiple SERP features simultaneously"
      - "Create comprehensive topic cluster content"
      - "Build topical authority in competitor weak areas"
      
    market_expansion:  
      - "Target keywords competitors ignore"
      - "Enter related niches where competitors are weak"
      - "Capture emerging trend keywords before competitors"
      - "Develop international SEO where competitors lack presence"
```

## 💼 ROI & Business Impact Analysis

### **Competitive Advantage Measurement:**
```python
competitive_roi_framework = {
    "market_share_gains": {
        "metric": "Organic visibility share increase",
        "calculation": "Our visibility % - Competitor avg %",
        "target": "+5% quarterly market share gain",
        "business_impact": "Direct correlation to revenue growth"
    },
    "traffic_acquisition": {
        "metric": "Organic traffic gained from competitors", 
        "calculation": "Traffic from keywords where we outranked competitors",
        "target": "20% of new traffic from competitive gains",
        "business_impact": "Lower customer acquisition cost"
    },
    "serp_feature_dominance": {
        "metric": "Featured snippets and SERP features owned",
        "calculation": "Our features / Total available features",
        "target": "30%+ SERP feature ownership in niche",
        "business_impact": "Higher CTR and brand authority"
    },
    "content_superiority": {
        "metric": "Content performance vs competitors",
        "calculation": "Our content engagement / Competitor avg",
        "target": "2x better engagement than competitors",
        "business_impact": "Higher conversion rates and user satisfaction"
    }
}
```

### **Competitive Intelligence Value:**
```yaml
intelligence_value_metrics:
  strategic_insights:
    - market_trend_prediction: "Early identification of industry shifts"
    - opportunity_sizing: "Quantification of traffic/revenue potential"
    - threat_assessment: "Risk evaluation from competitive moves"
    - resource_allocation: "Data-driven budget distribution"
    
  tactical_advantages:
    - content_creation_guidance: "Data-backed content strategy"
    - keyword_prioritization: "ROI-focused keyword targeting"
    - link_building_direction: "Competitor-informed link strategy"
    - technical_optimization: "Performance benchmarking insights"
    
  time_to_market:
    - faster_decision_making: "Real-time competitive data"
    - reduced_research_time: "Automated intelligence gathering"
    - proactive_strategy: "Anticipate rather than react"
    - resource_efficiency: "Focus efforts on highest-impact areas"
```

## 🔄 Automated Workflows

### **Daily Intelligence Tasks:**
```python
daily_automation = [
    "keyword_ranking_tracking",      # Monitor position changes
    "serp_feature_monitoring",       # Track SERP feature ownership
    "competitor_content_discovery",  # Identify new competitor content
    "backlink_acquisition_alerts",   # Monitor new competitor links
    "social_media_monitoring",       # Track competitor social activity
    "technical_performance_check"    # Monitor site performance changes
]
```

### **Weekly Analysis Tasks:**
```python
weekly_automation = [
    "content_gap_analysis_update",   # Refresh content opportunities
    "link_building_gap_assessment",  # Update link gap analysis
    "serp_landscape_analysis",       # Comprehensive SERP review
    "competitor_strategy_analysis",  # Identify strategy changes
    "market_share_calculation",      # Update visibility metrics
    "opportunity_prioritization"     # Rank action opportunities
]
```

### **Monthly Strategic Tasks:**
```python
monthly_automation = [
    "competitive_landscape_review",  # Full market analysis
    "strategy_effectiveness_audit",  # Measure our competitive performance
    "new_competitor_identification", # Discover emerging competitors
    "market_trend_analysis",         # Industry trend assessment
    "roi_competitive_analysis",      # Business impact measurement
    "strategic_recommendation_update" # Update competitive strategy
]
```

## 🎯 Industry-Specific Frameworks

### **B2B SaaS Competitive Analysis:**
```yaml
b2b_saas_focus_areas:
  feature_comparison:
    - product_feature_analysis: "Competitive feature matrices"
    - pricing_strategy_tracking: "Competitor pricing changes"
    - integration_ecosystem: "Third-party integration coverage"
    - customer_testimonial_analysis: "Social proof strategies"
    
  content_strategy:
    - thought_leadership_content: "Industry expert content analysis"
    - case_study_strategies: "Customer success story approaches"
    - educational_content: "How-to and tutorial coverage"
    - industry_report_frequency: "Original research publication rates"
    
  technical_marketing:
    - api_documentation_quality: "Developer experience optimization"
    - technical_blog_content: "Developer-focused content strategy"
    - integration_guides: "Technical onboarding content"
    - security_content: "Compliance and security positioning"
```

### **E-commerce Competitive Analysis:**
```yaml
ecommerce_focus_areas:
  product_strategy:
    - product_catalog_coverage: "SKU overlap and gaps analysis"
    - pricing_competitiveness: "Dynamic pricing monitoring"
    - product_page_optimization: "Conversion optimization tactics"
    - inventory_strategy: "Stock availability tracking"
    
  content_marketing:
    - buyer_guide_content: "Purchase decision support content"
    - product_comparison_content: "Competitive product comparisons"
    - seasonal_content_strategy: "Holiday and seasonal campaigns"
    - user_generated_content: "Review and testimonial strategies"
    
  technical_ecommerce:
    - site_search_functionality: "Internal search optimization"
    - checkout_process_analysis: "Conversion funnel optimization"
    - mobile_commerce_experience: "Mobile shopping optimization"
    - page_speed_performance: "Site performance for conversions"
```

---

**Последнее обновление:** 2025-08-05  
**Версия:** 1.0  
**Совместимость:** AI SEO Architects v1.3+