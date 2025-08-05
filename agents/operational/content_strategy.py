"""
Content Strategy Agent - Комплексная контентная стратегия для SEO
Operational Level Agent
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

from core.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ContentStrategyAgent(BaseAgent):
    """
    Content Strategy Agent - Operational уровень
    
    Специализация: Keyword research, контентная стратегия, E-E-A-T оптимизация,
    TF-IDF анализ, топиковая кластеризация, content calendar планирование
    """
    
    def __init__(self, data_provider, **kwargs):
        super().__init__(
            agent_id="content_strategy_agent",
            name="Content Strategy Agent",
            data_provider=data_provider,
            **kwargs
        )
        
        # Content strategy configuration
        self.content_config = {
            "keyword_research_depth": "comprehensive",  # basic, standard, comprehensive
            "content_quality_threshold": 85,  # Минимальный E-E-A-T score
            "topic_cluster_size": 15,  # Среднее количество статей в кластере
            "content_calendar_horizon": 90,  # Дней планирования вперед
            "competitor_analysis_depth": 5,  # Количество конкурентов для анализа
            "industry_expertise_level": "expert"  # basic, intermediate, expert
        }
        
        # Supported industries
        self.industry_specialization = [
            "fintech", "ecommerce", "saas", "healthcare", 
            "real_estate", "education", "manufacturing", "consulting"
        ]
        
        # Content types expertise
        self.content_types = [
            "blog_posts", "pillar_pages", "landing_pages", "product_pages",
            "category_pages", "guides", "whitepapers", "case_studies",
            "infographics", "videos", "podcasts", "webinars"
        ]
        
        logger.info(f"🎯 Content Strategy Agent инициализирован:")
        logger.info(f"📊 Keyword Research: {self.content_config['keyword_research_depth']}")
        logger.info(f"🎯 Quality Threshold: {self.content_config['content_quality_threshold']}+ E-E-A-T")
        logger.info(f"📅 Planning Horizon: {self.content_config['content_calendar_horizon']} дней")
        logger.info(f"🏭 Industries: {len(self.industry_specialization)} вертикалей")
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика обработки задач Content Strategy Agent
        
        Поддерживаемые типы задач:
        - keyword_research: Комплексное исследование ключевых слов
        - content_audit: Аудит существующего контента
        - content_strategy: Разработка контентной стратегии
        - topic_clustering: Кластеризация тем
        - content_calendar: Планирование контент-календаря
        - competitor_content_analysis: Анализ контента конкурентов
        - eeat_optimization: E-E-A-T оптимизация
        """
        
        start_time = datetime.now()
        
        try:
            # Извлекаем данные задачи
            input_data = task_data.get("input_data", {})
            task_type = input_data.get("task_type", "content_strategy")
            
            logger.info(f"🎯 Обработка Content Strategy задачи: {task_type}")
            
            # Определяем тип обработки
            if task_type == "keyword_research":
                result = await self._process_keyword_research(input_data)
            elif task_type == "content_audit":
                result = await self._process_content_audit(input_data)
            elif task_type == "content_strategy":
                result = await self._process_content_strategy(input_data)
            elif task_type == "topic_clustering":
                result = await self._process_topic_clustering(input_data)
            elif task_type == "content_calendar":
                result = await self._process_content_calendar(input_data)
            elif task_type == "competitor_content_analysis":
                result = await self._process_competitor_analysis(input_data)
            elif task_type == "eeat_optimization":
                result = await self._process_eeat_optimization(input_data)
            else:
                # Default: комплексная контентная стратегия
                result = await self._process_comprehensive_strategy(input_data)
            
            # Рассчитываем время выполнения
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Записываем метрики
            self.metrics.record_task(True, processing_time)
            
            logger.info(f"✅ Content Strategy задача завершена за {processing_time:.2f}с")
            
            return {
                "success": True,
                "agent": self.agent_id,
                "task_type": task_type,
                "result": result,
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat(),
                "content_quality": self._assess_content_quality(result),
                "strategy_confidence": self._calculate_strategy_confidence(result)
            }
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.metrics.record_task(False, processing_time)
            
            logger.error(f"❌ Ошибка в Content Strategy Agent: {str(e)}")
            
            return {
                "success": False,
                "agent": self.agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "processing_time": processing_time
            }
    
    async def _process_keyword_research(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Комплексное исследование ключевых слов"""
        
        domain = input_data.get("domain", "example.com")
        industry = input_data.get("industry", "general")
        seed_keywords = input_data.get("seed_keywords", [])
        research_depth = input_data.get("depth", self.content_config["keyword_research_depth"])
        
        logger.info(f"🔍 Keyword research для {domain} в {industry}")
        
        # Симуляция comprehensive keyword research
        if research_depth == "comprehensive":
            primary_keywords = self._generate_primary_keywords(industry, seed_keywords, 50)
            long_tail_keywords = self._generate_long_tail_keywords(primary_keywords, 200)
            question_keywords = self._generate_question_keywords(primary_keywords, 100)
            commercial_keywords = self._generate_commercial_keywords(industry, 75)
        else:
            primary_keywords = self._generate_primary_keywords(industry, seed_keywords, 25)
            long_tail_keywords = self._generate_long_tail_keywords(primary_keywords, 100)
            question_keywords = self._generate_question_keywords(primary_keywords, 50)
            commercial_keywords = self._generate_commercial_keywords(industry, 35)
        
        return {
            "keyword_research_results": {
                "primary_keywords": primary_keywords,
                "long_tail_keywords": long_tail_keywords,
                "question_keywords": question_keywords,
                "commercial_keywords": commercial_keywords,
                "total_keywords": len(primary_keywords) + len(long_tail_keywords) + len(question_keywords) + len(commercial_keywords),
                "research_depth": research_depth,
                "industry_focus": industry
            },
            "keyword_difficulty_analysis": self._analyze_keyword_difficulty(primary_keywords),
            "search_intent_mapping": self._map_search_intent(primary_keywords + long_tail_keywords),
            "content_opportunities": self._identify_content_opportunities(primary_keywords, industry)
        }
    
    async def _process_content_strategy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Разработка комплексной контентной стратегии"""
        
        domain = input_data.get("domain", "example.com")
        industry = input_data.get("industry", "general")
        business_goals = input_data.get("business_goals", ["traffic_growth", "lead_generation"])
        target_audience = input_data.get("target_audience", {})
        content_budget = input_data.get("monthly_budget", 100000)  # рублей
        
        logger.info(f"📋 Content strategy для {domain}, бюджет: {content_budget:,} ₽")
        
        # Content pillars для индустрии
        content_pillars = self._define_content_pillars(industry, business_goals)
        
        # Content types recommendation
        recommended_content_types = self._recommend_content_types(industry, content_budget, business_goals)
        
        # Publishing frequency
        publishing_schedule = self._calculate_publishing_schedule(content_budget, industry)
        
        # ROI projection
        roi_projection = self._calculate_content_roi_projection(content_budget, industry, publishing_schedule)
        
        return {
            "content_strategy": {
                "industry": industry,
                "monthly_budget": content_budget,
                "content_pillars": content_pillars,
                "recommended_content_types": recommended_content_types,
                "publishing_schedule": publishing_schedule,
                "roi_projection": roi_projection
            },
            "implementation_roadmap": self._create_implementation_roadmap(content_pillars, publishing_schedule),
            "success_metrics": self._define_success_metrics(business_goals),
            "resource_requirements": self._calculate_resource_requirements(publishing_schedule, content_budget)
        }
    
    async def _process_topic_clustering(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Кластеризация тем для контентной стратегии"""
        
        keywords = input_data.get("keywords", [])
        industry = input_data.get("industry", "general")
        cluster_strategy = input_data.get("cluster_strategy", "topic_based")  # topic_based, intent_based, funnel_based
        
        logger.info(f"🗂️ Topic clustering: {len(keywords)} keywords, стратегия: {cluster_strategy}")
        
        # Создаем кластеры тем
        if cluster_strategy == "topic_based":
            clusters = self._create_topic_based_clusters(keywords, industry)
        elif cluster_strategy == "intent_based":
            clusters = self._create_intent_based_clusters(keywords)
        else:  # funnel_based
            clusters = self._create_funnel_based_clusters(keywords, industry)
        
        # Приоритизация кластеров
        prioritized_clusters = self._prioritize_clusters(clusters, industry)
        
        return {
            "topic_clusters": {
                "total_clusters": len(clusters),
                "clustering_strategy": cluster_strategy,
                "clusters": prioritized_clusters
            },
            "content_hub_recommendations": self._recommend_content_hubs(prioritized_clusters),
            "internal_linking_strategy": self._design_internal_linking_strategy(prioritized_clusters),
            "pillar_page_opportunities": self._identify_pillar_page_opportunities(prioritized_clusters)
        }
    
    async def _process_content_calendar(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Планирование контент-календаря"""
        
        content_strategy = input_data.get("content_strategy", {})
        topic_clusters = input_data.get("topic_clusters", [])
        publishing_frequency = input_data.get("publishing_frequency", "weekly")
        calendar_horizon = input_data.get("calendar_horizon", self.content_config["content_calendar_horizon"])
        
        logger.info(f"📅 Content calendar планирование на {calendar_horizon} дней")
        
        # Создаем календарь публикаций
        content_calendar = self._generate_content_calendar(
            topic_clusters, publishing_frequency, calendar_horizon
        )
        
        # Seasonal content opportunities
        seasonal_content = self._identify_seasonal_opportunities(calendar_horizon)
        
        # Content distribution plan
        distribution_plan = self._create_distribution_plan(content_calendar)
        
        return {
            "content_calendar": {
                "planning_horizon_days": calendar_horizon,
                "publishing_frequency": publishing_frequency,
                "total_planned_content": len(content_calendar),
                "calendar": content_calendar
            },
            "seasonal_opportunities": seasonal_content,
            "distribution_plan": distribution_plan,
            "resource_allocation": self._calculate_calendar_resource_allocation(content_calendar)
        }
    
    async def _process_eeat_optimization(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """E-E-A-T оптимизация контента"""
        
        content_audit = input_data.get("content_audit", {})
        industry = input_data.get("industry", "general")
        expertise_level = input_data.get("target_expertise_level", "expert")
        
        logger.info(f"🎓 E-E-A-T оптимизация для {industry}, уровень: {expertise_level}")
        
        # E-E-A-T assessment
        current_eeat_score = self._assess_current_eeat_score(content_audit, industry)
        
        # Improvement recommendations
        eeat_improvements = self._recommend_eeat_improvements(current_eeat_score, expertise_level, industry)
        
        # Author strategy
        author_strategy = self._develop_author_strategy(industry, expertise_level)
        
        # Content credibility enhancements
        credibility_enhancements = self._recommend_credibility_enhancements(industry)
        
        return {
            "eeat_optimization": {
                "current_eeat_score": current_eeat_score,
                "target_expertise_level": expertise_level,
                "improvement_priority": eeat_improvements["priority_areas"],
                "implementation_plan": eeat_improvements["implementation_plan"]
            },
            "author_strategy": author_strategy,
            "credibility_enhancements": credibility_enhancements,
            "success_metrics": self._define_eeat_success_metrics(expertise_level)
        }
    
    async def _process_comprehensive_strategy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Комплексная контентная стратегия (default processing)"""
        
        domain = input_data.get("domain", "example.com")
        industry = input_data.get("industry", "general")
        
        logger.info(f"📊 Comprehensive content strategy для {domain}")
        
        # Выполняем все основные компоненты
        keyword_research = await self._process_keyword_research(input_data)
        content_strategy = await self._process_content_strategy(input_data)
        topic_clustering = await self._process_topic_clustering({
            "keywords": keyword_research["keyword_research_results"]["primary_keywords"],
            "industry": industry
        })
        content_calendar = await self._process_content_calendar({
            "topic_clusters": topic_clustering["topic_clusters"]["clusters"][:10],
            "publishing_frequency": "bi-weekly"
        })
        
        return {
            "comprehensive_strategy": {
                "domain": domain,
                "industry": industry,
                "strategy_scope": "comprehensive"
            },
            "keyword_research": keyword_research,
            "content_strategy": content_strategy,
            "topic_clustering": topic_clustering,
            "content_calendar": content_calendar,
            "implementation_priority": self._prioritize_implementation_steps(
                keyword_research, content_strategy, topic_clustering
            )
        }
    
    def _generate_primary_keywords(self, industry: str, seed_keywords: List[str], count: int) -> List[Dict[str, Any]]:
        """Генерация primary keywords"""
        
        # Industry-specific keyword patterns
        industry_patterns = {
            "fintech": ["финтех", "цифровой банк", "мобильный банкинг", "инвестиции", "криптовалюта"],
            "ecommerce": ["интернет магазин", "онлайн покупки", "доставка", "товары", "скидки"],
            "saas": ["программное обеспечение", "облачные решения", "автоматизация", "crm система"],
            "healthcare": ["медицина", "здоровье", "лечение", "диагностика", "клиника"],
            "real_estate": ["недвижимость", "квартиры", "дома", "ипотека", "аренда"],
            "education": ["образование", "обучение", "курсы", "университет", "школа"],
            "general": ["услуги", "компания", "решения", "консультации", "специалисты"]
        }
        
        base_patterns = industry_patterns.get(industry, industry_patterns["general"])
        
        keywords = []
        for i, pattern in enumerate(base_patterns[:count]):
            keywords.append({
                "keyword": pattern,
                "search_volume": 10000 - (i * 500),
                "difficulty": 45 + (i * 3),
                "cpc": 150 + (i * 25),
                "intent": "informational" if i % 3 == 0 else "commercial",
                "priority": "high" if i < 10 else "medium"
            })
        
        return keywords
    
    def _generate_long_tail_keywords(self, primary_keywords: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """Генерация long-tail keywords"""
        
        long_tail = []
        modifiers = ["как", "что такое", "лучший", "топ", "руководство", "инструкция", "отзывы", "цена"]
        
        for i, primary in enumerate(primary_keywords[:count//8]):
            for j, modifier in enumerate(modifiers):
                if len(long_tail) >= count:
                    break
                long_tail.append({
                    "keyword": f"{modifier} {primary['keyword']}",
                    "search_volume": max(100, primary["search_volume"] // 10),
                    "difficulty": max(15, primary["difficulty"] - 20),
                    "cpc": max(50, primary["cpc"] // 2),
                    "intent": "informational" if modifier in ["как", "что такое"] else "commercial",
                    "priority": "medium",
                    "parent_keyword": primary["keyword"]
                })
        
        return long_tail[:count]
    
    def _generate_question_keywords(self, primary_keywords: List[Dict[str, Any]], count: int) -> List[Dict[str, Any]]:
        """Генерация question-based keywords"""
        
        question_keywords = []
        question_patterns = ["как выбрать", "что лучше", "почему", "где найти", "когда использовать"]
        
        for i, primary in enumerate(primary_keywords[:count//5]):
            for pattern in question_patterns:
                if len(question_keywords) >= count:
                    break
                question_keywords.append({
                    "keyword": f"{pattern} {primary['keyword']}",
                    "search_volume": max(50, primary["search_volume"] // 20),
                    "difficulty": max(10, primary["difficulty"] - 25),
                    "cpc": max(30, primary["cpc"] // 3),
                    "intent": "informational",
                    "priority": "high",  # Question-based content часто хорошо ранжируется
                    "content_type": "faq_or_guide",
                    "parent_keyword": primary["keyword"]
                })
        
        return question_keywords[:count]
    
    def _generate_commercial_keywords(self, industry: str, count: int) -> List[Dict[str, Any]]:
        """Генерация commercial intent keywords"""
        
        commercial_patterns = {
            "fintech": ["купить", "цена", "стоимость", "тариф", "подключить"],
            "ecommerce": ["заказать", "купить", "доставка", "оплата", "каталог"],
            "saas": ["подписка", "демо", "пробная версия", "цена", "тариф"],
            "general": ["заказать", "купить", "цена", "услуги", "консультация"]
        }
        
        patterns = commercial_patterns.get(industry, commercial_patterns["general"])
        
        commercial_keywords = []
        for i, pattern in enumerate(patterns):
            for j in range(count // len(patterns)):
                commercial_keywords.append({
                    "keyword": f"{pattern} {industry}",
                    "search_volume": 2000 - (i * 100),
                    "difficulty": 55 + (i * 5),
                    "cpc": 300 + (i * 50),
                    "intent": "commercial",
                    "priority": "high",
                    "conversion_potential": "high"
                })
        
        return commercial_keywords[:count]
    
    def _analyze_keyword_difficulty(self, keywords: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Анализ сложности ключевых слов"""
        
        difficulty_distribution = {"easy": 0, "medium": 0, "hard": 0}
        total_keywords = len(keywords)
        
        for keyword in keywords:
            difficulty = keyword.get("difficulty", 50)
            if difficulty < 30:
                difficulty_distribution["easy"] += 1
            elif difficulty < 60:
                difficulty_distribution["medium"] += 1
            else:
                difficulty_distribution["hard"] += 1
        
        return {
            "difficulty_distribution": difficulty_distribution,
            "average_difficulty": sum(kw.get("difficulty", 50) for kw in keywords) / total_keywords,
            "quick_wins": [kw for kw in keywords if kw.get("difficulty", 50) < 30],
            "competitive_keywords": [kw for kw in keywords if kw.get("difficulty", 50) > 70],
            "recommendations": self._generate_difficulty_recommendations(difficulty_distribution)
        }
    
    def _generate_difficulty_recommendations(self, difficulty_distribution: Dict[str, int]) -> List[str]:
        """Генерация рекомендаций на основе распределения сложности"""
        recommendations = []
        
        total_keywords = sum(difficulty_distribution.values())
        if total_keywords == 0:
            return ["Добавить ключевые слова для анализа"]
        
        easy_percentage = difficulty_distribution.get("easy", 0) / total_keywords
        medium_percentage = difficulty_distribution.get("medium", 0) / total_keywords  
        hard_percentage = difficulty_distribution.get("hard", 0) / total_keywords
        
        if easy_percentage > 0.6:
            recommendations.append("Добавить более конкурентные ключевые слова для роста")
        elif easy_percentage < 0.2:
            recommendations.append("Добавить низкоконкурентные ключевые слова для быстрых побед")
        
        if hard_percentage > 0.4:
            recommendations.append("Сосредоточиться сначала на менее конкурентных запросах")
        
        if medium_percentage < 0.3:
            recommendations.append("Добавить ключевые слова средней сложности для баланса")
        
        return recommendations if recommendations else ["Сбалансированное распределение сложности"]
    
    def _map_search_intent(self, keywords: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Маппинг поисковых интентов"""
        
        intent_mapping = {
            "informational": [],
            "commercial": [],
            "navigational": [],
            "transactional": []
        }
        
        for keyword in keywords:
            intent = keyword.get("intent", "informational")
            if intent in intent_mapping:
                intent_mapping[intent].append(keyword)
            else:
                intent_mapping["informational"].append(keyword)
        
        return {
            "intent_distribution": {intent: len(kws) for intent, kws in intent_mapping.items()},
            "intent_mapping": intent_mapping,
            "content_recommendations": self._generate_intent_based_content_recommendations(intent_mapping)
        }
    
    def _generate_intent_based_content_recommendations(self, intent_mapping: Dict[str, List]) -> List[str]:
        """Генерация рекомендаций на основе поисковых интентов"""
        recommendations = []
        
        total_keywords = sum(len(keywords) for keywords in intent_mapping.values())
        if total_keywords == 0:
            return ["Добавить ключевые слова для анализа интентов"]
        
        # Анализ распределения интентов
        informational_pct = len(intent_mapping.get("informational", [])) / total_keywords
        commercial_pct = len(intent_mapping.get("commercial", [])) / total_keywords
        transactional_pct = len(intent_mapping.get("transactional", [])) / total_keywords
        navigational_pct = len(intent_mapping.get("navigational", [])) / total_keywords
        
        if informational_pct > 0.6:
            recommendations.append("Создать больше коммерческого и транзакционного контента")
        elif informational_pct < 0.2:
            recommendations.append("Добавить образовательный контент для привлечения новых посетителей")
        
        if commercial_pct < 0.2:
            recommendations.append("Увеличить количество контента для коммерческих запросов")
        
        if transactional_pct < 0.15:
            recommendations.append("Создать больше продающих страниц и лендингов")
        
        if navigational_pct > 0.3:
            recommendations.append("Оптимизировать брендинг и узнаваемость")
        
        return recommendations if recommendations else ["Сбалансированное распределение интентов"]
    
    def _identify_content_opportunities(self, keywords: List[Dict[str, Any]], industry: str) -> List[Dict[str, Any]]:
        """Выявление контентных возможностей"""
        
        opportunities = []
        
        # High-volume, low-difficulty opportunities
        for keyword in keywords:
            if keyword.get("search_volume", 0) > 5000 and keyword.get("difficulty", 100) < 40:
                opportunities.append({
                    "type": "quick_win",
                    "keyword": keyword["keyword"],
                    "opportunity_score": keyword["search_volume"] / keyword["difficulty"],
                    "recommended_content_type": "blog_post",
                    "priority": "high"
                })
        
        # Question-based content opportunities
        question_keywords = [kw for kw in keywords if any(q in kw["keyword"].lower() 
                           for q in ["как", "что", "почему", "где", "когда"])]
        
        for keyword in question_keywords[:10]:
            opportunities.append({
                "type": "faq_content",
                "keyword": keyword["keyword"], 
                "opportunity_score": keyword.get("search_volume", 100) * 2,  # FAQ контент часто хорошо ранжируется
                "recommended_content_type": "faq_or_guide",
                "priority": "medium"
            })
        
        return sorted(opportunities, key=lambda x: x["opportunity_score"], reverse=True)[:20]
    
    def _define_content_pillars(self, industry: str, business_goals: List[str]) -> List[Dict[str, Any]]:
        """Определение контентных столпов"""
        
        industry_pillars = {
            "fintech": [
                {"name": "Цифровой банкинг", "description": "Современные банковские решения"},
                {"name": "Инвестиции и финансы", "description": "Инвестиционные стратегии"},
                {"name": "Технологии в финансах", "description": "Финтех инновации"},
                {"name": "Регулирование", "description": "Финансовое законодательство"}
            ],
            "ecommerce": [
                {"name": "Товары и каталог", "description": "Продуктовый контент"},
                {"name": "Покупательский опыт", "description": "UX и сервис"},
                {"name": "Маркетинг и продажи", "description": "Продвижение товаров"},
                {"name": "Логистика", "description": "Доставка и fulfillment"}
            ],
            "general": [
                {"name": "Экспертиза", "description": "Отраслевая экспертиза"},
                {"name": "Решения", "description": "Продукты и услуги"},
                {"name": "Кейсы", "description": "Истории успеха"},
                {"name": "Тренды", "description": "Отраслевые тенденции"}
            ]
        }
        
        pillars = industry_pillars.get(industry, industry_pillars["general"])
        
        # Адаптируем под бизнес-цели
        for pillar in pillars:
            if "lead_generation" in business_goals:
                pillar["lead_generation_potential"] = "high"
            if "brand_awareness" in business_goals:
                pillar["brand_building_potential"] = "high"
        
        return pillars
    
    def _recommend_content_types(self, industry: str, budget: int, goals: List[str]) -> List[Dict[str, Any]]:
        """Рекомендация типов контента"""
        
        # Budget-based recommendations
        if budget < 50000:  # Small budget
            recommended_types = [
                {"type": "blog_posts", "frequency": "weekly", "investment": 30000},
                {"type": "social_media", "frequency": "daily", "investment": 15000}
            ]
        elif budget < 200000:  # Medium budget
            recommended_types = [
                {"type": "blog_posts", "frequency": "bi-weekly", "investment": 60000},
                {"type": "guides", "frequency": "monthly", "investment": 40000},
                {"type": "infographics", "frequency": "bi-weekly", "investment": 30000},
                {"type": "videos", "frequency": "monthly", "investment": 50000}
            ]
        else:  # Large budget
            recommended_types = [
                {"type": "blog_posts", "frequency": "daily", "investment": 80000},
                {"type": "pillar_pages", "frequency": "weekly", "investment": 60000},
                {"type": "whitepapers", "frequency": "monthly", "investment": 40000},
                {"type": "webinars", "frequency": "bi-weekly", "investment": 50000},
                {"type": "case_studies", "frequency": "weekly", "investment": 30000}
            ]
        
        # Goal-based adjustments
        for content_type in recommended_types:
            if "lead_generation" in goals:
                content_type["lead_gen_score"] = 8 if content_type["type"] in ["whitepapers", "webinars"] else 5
            if "brand_awareness" in goals:
                content_type["brand_score"] = 9 if content_type["type"] in ["videos", "infographics"] else 6
        
        return recommended_types
    
    def _calculate_publishing_schedule(self, budget: int, industry: str) -> Dict[str, Any]:
        """Расчет графика публикаций"""
        
        # Budget-based frequency calculation
        if budget < 50000:
            weekly_posts = 1
            monthly_premium = 0
        elif budget < 100000:
            weekly_posts = 2
            monthly_premium = 1
        elif budget < 200000:
            weekly_posts = 3
            monthly_premium = 2
        else:
            weekly_posts = 5
            monthly_premium = 4
        
        return {
            "weekly_blog_posts": weekly_posts,
            "monthly_premium_content": monthly_premium,
            "quarterly_major_content": max(1, monthly_premium // 2),
            "daily_social_content": min(7, budget // 10000),
            "total_monthly_pieces": (weekly_posts * 4) + monthly_premium,
            "annual_content_pieces": ((weekly_posts * 4) + monthly_premium) * 12
        }
    
    def _calculate_content_roi_projection(self, budget: int, industry: str, schedule: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет ROI проекции для контента"""
        
        # Industry multipliers
        industry_multipliers = {
            "fintech": 3.2,
            "saas": 4.1,
            "ecommerce": 2.8,
            "healthcare": 3.5,
            "general": 2.5
        }
        
        multiplier = industry_multipliers.get(industry, 2.5)
        annual_budget = budget * 12
        
        # ROI calculation based on content volume and industry
        monthly_content_pieces = schedule.get("total_monthly_pieces", 4)
        content_scaling_factor = min(2.0, 1 + (monthly_content_pieces - 4) * 0.1)
        
        projected_annual_roi = annual_budget * multiplier * content_scaling_factor
        
        return {
            "annual_investment": annual_budget,
            "projected_annual_return": projected_annual_roi,
            "roi_multiplier": projected_annual_roi / annual_budget,
            "monthly_roi_projection": projected_annual_roi / 12,
            "payback_months": max(6, 12 / (projected_annual_roi / annual_budget)),
            "confidence_level": min(85, 60 + (content_scaling_factor * 15))
        }
    
    def _assess_content_quality(self, result: Dict[str, Any]) -> str:
        """Оценка качества контентной стратегии"""
        
        # Оцениваем различные аспекты результата
        quality_score = 0
        max_score = 100
        
        # Проверяем наличие ключевых компонентов
        if "keyword_research" in result:
            quality_score += 25
        if "content_strategy" in result:
            quality_score += 25  
        if "topic_clusters" in result:
            quality_score += 20
        if "content_calendar" in result:
            quality_score += 15
        if "eeat_optimization" in result:
            quality_score += 15
        
        # Определяем качественную оценку
        if quality_score >= 85:
            return "comprehensive"
        elif quality_score >= 65:
            return "good"
        elif quality_score >= 45:
            return "basic"
        else:
            return "incomplete"
    
    def _calculate_strategy_confidence(self, result: Dict[str, Any]) -> float:
        """Расчет уверенности в стратегии"""
        
        confidence = 0.6  # Базовая уверенность
        
        # Увеличиваем уверенность на основе компонентов
        if "keyword_research" in result:
            keyword_count = result["keyword_research"].get("keyword_research_results", {}).get("total_keywords", 0)
            confidence += min(0.2, keyword_count / 1000)
        
        if "content_strategy" in result:
            budget = result["content_strategy"].get("content_strategy", {}).get("monthly_budget", 0)
            confidence += min(0.15, budget / 1000000)  # Больше бюджет = больше уверенности
        
        if "topic_clusters" in result:
            cluster_count = result["topic_clusters"].get("topic_clusters", {}).get("total_clusters", 0)
            confidence += min(0.1, cluster_count / 50)
        
        return min(0.95, confidence)
    
    # Helper methods для создания контента
    def _create_topic_based_clusters(self, keywords: List[Dict[str, Any]], industry: str) -> List[Dict[str, Any]]:
        """Создание кластеров на основе тем"""
        # Simplified clustering logic
        clusters = []
        cluster_size = self.content_config["topic_cluster_size"]
        
        for i in range(0, len(keywords), cluster_size):
            cluster_keywords = keywords[i:i+cluster_size]
            if cluster_keywords:
                clusters.append({
                    "cluster_id": f"cluster_{len(clusters)+1}",
                    "main_topic": cluster_keywords[0]["keyword"],
                    "keywords": cluster_keywords,
                    "keyword_count": len(cluster_keywords),
                    "total_search_volume": sum(kw.get("search_volume", 0) for kw in cluster_keywords),
                    "avg_difficulty": sum(kw.get("difficulty", 50) for kw in cluster_keywords) / len(cluster_keywords),
                    "content_priority": "high" if i < cluster_size * 3 else "medium"
                })
        
        return clusters
    
    def _prioritize_clusters(self, clusters: List[Dict[str, Any]], industry: str) -> List[Dict[str, Any]]:
        """Приоритизация кластеров"""
        # Сортируем по потенциальной ценности (объем поиска / сложность)
        for cluster in clusters:
            total_volume = cluster.get("total_search_volume", 1)
            avg_difficulty = cluster.get("avg_difficulty", 50)
            cluster["priority_score"] = total_volume / max(avg_difficulty, 1)
        
        return sorted(clusters, key=lambda x: x["priority_score"], reverse=True)
    
    def _generate_content_calendar(self, clusters: List[Dict[str, Any]], frequency: str, horizon: int) -> List[Dict[str, Any]]:
        """Генерация контент-календаря"""
        
        calendar = []
        frequency_map = {"daily": 1, "weekly": 7, "bi-weekly": 14, "monthly": 30}
        interval = frequency_map.get(frequency, 7)
        
        for i, cluster in enumerate(clusters):
            if i * interval < horizon:
                calendar.append({
                    "date": f"Day {(i * interval) + 1}",
                    "content_title": f"Content for {cluster.get('main_topic', f'Topic {i+1}')}",
                    "cluster_id": cluster.get("cluster_id", f"cluster_{i+1}"),
                    "content_type": "blog_post",
                    "target_keywords": cluster.get("keywords", [])[:5],  # Top 5 keywords
                    "estimated_effort": "4-6 hours",
                    "priority": cluster.get("content_priority", "medium")
                })
        
        return calendar[:horizon//7]  # Limit to reasonable number
    
    # Additional helper methods
    def _create_implementation_roadmap(self, pillars: List[Dict], schedule: Dict) -> List[Dict[str, Any]]:
        """Создание roadmap'а реализации"""
        return [
            {"phase": "Phase 1", "duration": "Month 1-2", "focus": "Keyword research & content pillars setup"},
            {"phase": "Phase 2", "duration": "Month 3-4", "focus": "Core content creation & optimization"},
            {"phase": "Phase 3", "duration": "Month 5-6", "focus": "Content distribution & performance optimization"}
        ]
    
    def _define_success_metrics(self, goals: List[str]) -> Dict[str, Any]:
        """Определение метрик успеха"""
        return {
            "traffic_growth": "25% increase in 6 months",
            "keyword_rankings": "50% of target keywords in top 10",
            "engagement_metrics": "15% increase in time on page",
            "conversion_metrics": "10% increase in organic conversions"
        }
    
    def _calculate_resource_requirements(self, schedule: Dict, budget: int) -> Dict[str, Any]:
        """Расчет требований к ресурсам"""
        return {
            "content_writers": max(1, schedule.get("weekly_blog_posts", 1) // 2),
            "editors": 1,
            "designers": 1 if budget > 100000 else 0.5,
            "monthly_budget_allocation": {
                "writing": budget * 0.4,
                "design": budget * 0.3,
                "promotion": budget * 0.3
            }
        }
    
    def _recommend_content_hubs(self, clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Рекомендации по созданию контентных хабов"""
        content_hubs = []
        
        for cluster in clusters[:5]:  # Топ-5 кластеров для хабов
            hub_keywords = cluster.get("keywords", [])
            if len(hub_keywords) >= 3:  # Достаточно ключевых слов для хаба
                
                # Определяем тип хаба на основе интентов
                hub_type = self._determine_hub_type(hub_keywords)
                
                content_hubs.append({
                    "hub_name": cluster.get("cluster_name", f"Hub {len(content_hubs) + 1}"),
                    "hub_type": hub_type,
                    "main_keywords": hub_keywords[:10],
                    "estimated_traffic_potential": sum(kw.get("search_volume", 0) for kw in hub_keywords),
                    "content_pieces_needed": min(max(len(hub_keywords) // 2, 5), 20),
                    "pillar_page_topic": cluster.get("cluster_name", ""),
                    "supporting_content": [
                        f"Подробное руководство по {kw.get('keyword', '')}" 
                        for kw in hub_keywords[:3]
                    ],
                    "internal_linking_opportunities": len(hub_keywords) * 2,
                    "recommended_update_frequency": hub_type == "evergreen" and "monthly" or "weekly"
                })
        
        return content_hubs
    
    def _determine_hub_type(self, keywords: List[Dict[str, Any]]) -> str:
        """Определение типа контентного хаба"""
        # Анализ интентов ключевых слов
        informational_count = sum(1 for kw in keywords if kw.get("intent", "").lower() == "informational")
        commercial_count = sum(1 for kw in keywords if kw.get("intent", "").lower() == "commercial")
        transactional_count = sum(1 for kw in keywords if kw.get("intent", "").lower() == "transactional")
        
        total_keywords = len(keywords)
        if total_keywords == 0:
            return "mixed"
        
        info_pct = informational_count / total_keywords
        commercial_pct = commercial_count / total_keywords
        
        if info_pct > 0.6:
            return "educational"
        elif commercial_pct > 0.4:
            return "product_focused" 
        elif transactional_count > 0:
            return "conversion_focused"
        else:
            return "evergreen"
    
    def _design_internal_linking_strategy(self, clusters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Разработка стратегии внутренней перелинковки"""
        
        linking_strategy = {
            "hub_to_spoke_links": [],
            "cross_cluster_opportunities": [],
            "anchor_text_suggestions": [],
            "linking_depth_strategy": "3-click rule implementation",
            "estimated_link_equity_flow": {}
        }
        
        # Hub-to-spoke linking для каждого кластера
        for cluster in clusters:
            cluster_name = cluster.get("cluster_name", "Unknown Cluster")
            keywords = cluster.get("keywords", [])
            
            if len(keywords) > 1:
                pillar_keyword = keywords[0].get("keyword", "") if keywords else ""
                
                linking_strategy["hub_to_spoke_links"].append({
                    "pillar_page": pillar_keyword,
                    "cluster": cluster_name,
                    "supporting_pages": [kw.get("keyword", "") for kw in keywords[1:6]],
                    "recommended_links_per_page": min(len(keywords), 8)
                })
        
        # Cross-cluster opportunities
        for i, cluster1 in enumerate(clusters):
            for cluster2 in clusters[i+1:i+3]:  # Ограничиваем количество сравнений
                similarity_score = self._calculate_cluster_similarity(cluster1, cluster2)
                if similarity_score > 0.3:
                    linking_strategy["cross_cluster_opportunities"].append({
                        "from_cluster": cluster1.get("cluster_name", ""),
                        "to_cluster": cluster2.get("cluster_name", ""),
                        "similarity_score": similarity_score,
                        "recommended_link_count": 2 if similarity_score > 0.5 else 1
                    })
        
        # Anchor text suggestions
        all_keywords = []
        for cluster in clusters:
            all_keywords.extend(cluster.get("keywords", []))
        
        linking_strategy["anchor_text_suggestions"] = [
            {
                "keyword": kw.get("keyword", ""),
                "variations": self._generate_anchor_variations(kw.get("keyword", "")),
                "recommended_distribution": "exact: 10%, partial: 40%, branded: 30%, generic: 20%"
            }
            for kw in all_keywords[:10]  # Топ-10 ключевых слов
        ]
        
        return linking_strategy
    
    def _calculate_cluster_similarity(self, cluster1: Dict[str, Any], cluster2: Dict[str, Any]) -> float:
        """Расчет семантической схожести кластеров"""
        # Упрощенный расчет на основе пересечения ключевых слов
        keywords1 = set(kw.get("keyword", "").lower().split() for kw in cluster1.get("keywords", []))
        keywords2 = set(kw.get("keyword", "").lower().split() for kw in cluster2.get("keywords", []))
        
        # Flatten sets of word lists
        words1 = set()
        words2 = set()
        for word_list in keywords1:
            words1.update(word_list)
        for word_list in keywords2:
            words2.update(word_list)
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _generate_anchor_variations(self, keyword: str) -> List[str]:
        """Генерация вариаций анкорного текста"""
        if not keyword:
            return []
        
        base_keyword = keyword.lower()
        variations = [
            keyword,  # Exact match
            f"подробнее о {base_keyword}",  # Partial match
            f"узнать больше про {base_keyword}",  # Generic
            f"что такое {base_keyword}",  # Question form
            f"{base_keyword} - полное руководство"  # Extended
        ]
        
        return variations[:4]  # Ограничиваем количество вариаций
    
    def _identify_pillar_page_opportunities(self, clusters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Выявление возможностей для создания pillar pages"""
        pillar_opportunities = []
        
        for cluster in clusters:
            keywords = cluster.get("keywords", [])
            if len(keywords) < 3:  # Минимум 3 ключевых слова для pillar page
                continue
            
            # Анализ потенциала кластера для pillar page
            total_volume = sum(kw.get("search_volume", 0) for kw in keywords)
            avg_difficulty = sum(kw.get("difficulty", 50) for kw in keywords) / len(keywords)
            
            if total_volume > 1000:  # Минимальный объем поиска
                main_keyword = keywords[0] if keywords else {}
                
                pillar_opportunity = {
                    "pillar_topic": cluster.get("cluster_name", main_keyword.get("keyword", "")),
                    "main_keyword": main_keyword.get("keyword", ""),
                    "supporting_keywords": [kw.get("keyword", "") for kw in keywords[1:10]],
                    "total_search_volume": total_volume,
                    "average_difficulty": round(avg_difficulty, 1),
                    "estimated_word_count": min(max(len(keywords) * 200, 2000), 5000),
                    "content_sections": self._suggest_pillar_sections(keywords),
                    "supporting_content_needed": len(keywords) - 1,
                    "internal_linking_potential": len(keywords) * 3,
                    "update_frequency": "quarterly",
                    "priority_score": self._calculate_pillar_priority(total_volume, avg_difficulty, len(keywords))
                }
                
                pillar_opportunities.append(pillar_opportunity)
        
        # Сортируем по приоритету
        pillar_opportunities.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return pillar_opportunities[:5]  # Топ-5 возможностей
    
    def _suggest_pillar_sections(self, keywords: List[Dict[str, Any]]) -> List[str]:
        """Предложение разделов для pillar page"""
        sections = [
            "Введение и определения",
            "Основные принципы и концепции", 
            "Практические примеры и кейсы",
            "Пошаговые инструкции",
            "Часто задаваемые вопросы",
            "Заключение и дальнейшие шаги"
        ]
        
        # Добавляем специфичные разделы на основе ключевых слов
        keyword_based_sections = []
        for kw in keywords[:3]:
            keyword = kw.get("keyword", "")
            if keyword:
                keyword_based_sections.append(f"Детальный анализ: {keyword}")
        
        return sections + keyword_based_sections
    
    def _calculate_pillar_priority(self, volume: int, difficulty: float, keyword_count: int) -> float:
        """Расчет приоритета pillar page"""
        # Формула приоритета: (объем поиска * количество ключевых слов) / сложность
        if difficulty == 0:
            difficulty = 1  # Избегаем деления на ноль
        
        base_score = (volume * keyword_count) / difficulty
        
        # Бонусы
        if volume > 10000:
            base_score *= 1.2  # Бонус за высокий объем
        if keyword_count > 10:
            base_score *= 1.1  # Бонус за широкий кластер
        if difficulty < 30:
            base_score *= 1.15  # Бонус за низкую сложность
        
        return round(base_score, 2)
    
    def _identify_seasonal_opportunities(self, horizon_days: int) -> List[Dict[str, Any]]:
        """Выявление сезонных контентных возможностей"""
        
        # Определяем текущий месяц и сезон для планирования
        import datetime
        current_month = datetime.datetime.now().month
        
        # Базовые сезонные категории для российского рынка
        seasonal_categories = {
            "winter": {
                "months": [12, 1, 2],
                "keywords": ["новый год", "зимние скидки", "зимняя одежда", "отопление", "праздники"],
                "content_types": ["gift_guides", "winter_maintenance", "holiday_campaigns"]
            },
            "spring": {
                "months": [3, 4, 5], 
                "keywords": ["весенние скидки", "дача", "сад", "ремонт", "8 марта"],
                "content_types": ["home_improvement", "garden_guides", "spring_cleaning"]
            },
            "summer": {
                "months": [6, 7, 8],
                "keywords": ["отпуск", "лето", "дача", "отдых", "кондиционеры"],
                "content_types": ["vacation_guides", "summer_products", "outdoor_activities"]
            },
            "autumn": {
                "months": [9, 10, 11],
                "keywords": ["школа", "учеба", "осенние скидки", "подготовка к зиме"],
                "content_types": ["back_to_school", "winter_preparation", "autumn_sales"]
            }
        }
        
        # Российские праздники и события
        russian_holidays = {
            1: ["Новый год", "Рождество"],
            2: ["День защитника Отечества"],
            3: ["8 Марта"],
            4: ["Пасха", "День космонавтики"],
            5: ["Майские праздники", "9 Мая"],
            6: ["День России", "Начало лета"],
            9: ["День знаний", "Начало учебного года"],
            10: ["День учителя"],
            11: ["День народного единства"],
            12: ["Подготовка к Новому году"]
        }
        
        seasonal_opportunities = []
        
        # Планируем на следующие месяцы в рамках горизонта
        months_to_plan = min(horizon_days // 30, 12)  # Максимум 12 месяцев
        
        for month_offset in range(1, months_to_plan + 1):
            target_month = ((current_month + month_offset - 1) % 12) + 1
            
            # Определяем сезон
            season = None
            for season_name, season_data in seasonal_categories.items():
                if target_month in season_data["months"]:
                    season = season_name
                    season_info = season_data
                    break
            
            if not season:
                continue
            
            # Создаем сезонную возможность
            opportunity = {
                "month": target_month,
                "season": season,
                "preparation_time": f"за {month_offset} месяцев",
                "seasonal_keywords": season_info["keywords"],
                "content_types": season_info["content_types"],
                "holidays": russian_holidays.get(target_month, []),
                "recommended_content": self._generate_seasonal_content_ideas(season, target_month),
                "traffic_multiplier": self._estimate_seasonal_traffic_boost(season, target_month),
                "preparation_deadline": f"Month {month_offset - 1 if month_offset > 1 else 1}",
                "priority": "high" if month_offset <= 2 else "medium"
            }
            
            seasonal_opportunities.append(opportunity)
        
        return seasonal_opportunities
    
    def _generate_seasonal_content_ideas(self, season: str, month: int) -> List[str]:
        """Генерация идей сезонного контента"""
        
        content_templates = {
            "winter": [
                "Топ-10 зимних трендов",
                "Как подготовиться к холодам", 
                "Зимние скидки и предложения",
                "Новогодние идеи и подарки"
            ],
            "spring": [
                "Весенние тренды и новинки",
                "Подготовка к дачному сезону", 
                "Весенний ремонт: что нужно знать",
                "Идеи для весеннего обновления"
            ],
            "summer": [
                "Летние must-have товары",
                "Планирование отпуска",
                "Дачные лайфхаки", 
                "Летние скидки и распродажи"
            ],
            "autumn": [
                "Подготовка к учебному году",
                "Осенние тренды",
                "Подготовка к зиме",
                "Осенние скидки"
            ]
        }
        
        base_ideas = content_templates.get(season, ["Сезонный контент"])
        
        # Добавляем месяц-специфичные идеи
        if month == 12 or month == 1:
            base_ideas.extend(["Новогодние распродажи", "Итоги года"])
        elif month == 3:
            base_ideas.extend(["8 Марта: подарки и идеи"])
        elif month == 9:
            base_ideas.extend(["День знаний", "Школьные товары"])
        
        return base_ideas[:5]  # Ограничиваем количество идей
    
    def _estimate_seasonal_traffic_boost(self, season: str, month: int) -> float:
        """Оценка сезонного прироста трафика"""
        
        # Базовые множители для сезонов
        season_multipliers = {
            "winter": 1.3,  # Высокий сезон покупок
            "spring": 1.1,  # Умеренный рост
            "summer": 0.9,  # Спад (отпуска)
            "autumn": 1.2   # Возвращение активности
        }
        
        base_multiplier = season_multipliers.get(season, 1.0)
        
        # Дополнительные бонусы для праздничных месяцев
        if month in [12, 1]:  # Новогодние праздники
            base_multiplier *= 1.4
        elif month in [3, 5]:  # 8 Марта, майские праздники
            base_multiplier *= 1.2
        elif month == 9:  # Начало учебного года
            base_multiplier *= 1.15
        
        return round(base_multiplier, 2)
    
    def _create_distribution_plan(self, content_calendar: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Создание плана распространения контента"""
        
        if not content_calendar:
            return {
                "channels": [],
                "total_reach": 0,
                "estimated_traffic": 0,
                "distribution_cost": 0
            }
        
        # Основные каналы распространения
        distribution_channels = [
            {
                "channel": "Organic Search",
                "type": "earned",
                "reach_percentage": 45,
                "effort_level": "ongoing",
                "cost_per_piece": 0,
                "expected_traffic_per_piece": 150
            },
            {
                "channel": "Social Media",
                "type": "owned",
                "reach_percentage": 25,
                "effort_level": "high",
                "cost_per_piece": 500,
                "expected_traffic_per_piece": 80
            },
            {
                "channel": "Email Newsletter",
                "type": "owned", 
                "reach_percentage": 15,
                "effort_level": "medium",
                "cost_per_piece": 0,
                "expected_traffic_per_piece": 120
            },
            {
                "channel": "Paid Promotion",
                "type": "paid",
                "reach_percentage": 10,
                "effort_level": "low",
                "cost_per_piece": 2000,
                "expected_traffic_per_piece": 300
            },
            {
                "channel": "Industry Partners",
                "type": "earned",
                "reach_percentage": 5,
                "effort_level": "high",
                "cost_per_piece": 0,
                "expected_traffic_per_piece": 200
            }
        ]
        
        # Расчет общих метрик
        total_content_pieces = len(content_calendar)
        total_estimated_traffic = 0
        total_distribution_cost = 0
        
        for channel in distribution_channels:
            pieces_per_channel = int(total_content_pieces * (channel["reach_percentage"] / 100))
            channel["content_pieces"] = pieces_per_channel
            channel["total_traffic"] = pieces_per_channel * channel["expected_traffic_per_piece"]
            channel["total_cost"] = pieces_per_channel * channel["cost_per_piece"]
            
            total_estimated_traffic += channel["total_traffic"]
            total_distribution_cost += channel["total_cost"]
        
        # План по месяцам
        monthly_plan = []
        months = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
        
        for i, month in enumerate(months[:min(len(months), total_content_pieces)]):
            if i < len(content_calendar):
                content_piece = content_calendar[i]
                monthly_plan.append({
                    "month": month,
                    "content_title": content_piece.get("content_title", f"Content {i+1}"),
                    "primary_channel": "Organic Search",
                    "secondary_channels": ["Social Media", "Email Newsletter"],
                    "estimated_reach": 2500 + (i * 100),
                    "estimated_traffic": 350 + (i * 25),
                    "distribution_budget": 1000 + (i * 200)
                })
        
        return {
            "channels": distribution_channels,
            "total_content_pieces": total_content_pieces,
            "total_estimated_traffic": total_estimated_traffic,
            "total_distribution_cost": total_distribution_cost,
            "monthly_distribution_plan": monthly_plan,
            "key_recommendations": [
                "Фокус на органический поиск для долгосрочного ROI",
                "Использование социальных сетей для амплификации",
                "Регулярная email-рассылка для удержания аудитории",
                "Селективное использование платного продвижения для ключевого контента"
            ],
            "success_metrics": {
                "traffic_growth_target": "25% в квартал",
                "engagement_rate_target": "15% средний CTR",
                "conversion_rate_target": "3% от трафика",
                "brand_awareness_lift": "20% за полгода"
            }
        }
    
    def _calculate_calendar_resource_allocation(self, content_calendar: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Расчет распределения ресурсов для контент-календаря"""
        
        if not content_calendar:
            return {
                "total_pieces": 0,
                "estimated_hours": 0,
                "team_size_needed": 0,
                "monthly_budget": 0
            }
        
        # Базовые метрики для расчетов
        hours_per_blog_post = 6
        hours_per_guide = 12
        hours_per_video = 8
        hours_per_infographic = 4
        
        # Анализ типов контента в календаре
        content_type_distribution = {
            "blog_post": 0,
            "guide": 0,
            "video": 0,
            "infographic": 0,
            "other": 0
        }
        
        total_estimated_hours = 0
        
        for content_piece in content_calendar:
            content_type = content_piece.get("content_type", "blog_post")
            
            if content_type in content_type_distribution:
                content_type_distribution[content_type] += 1
            else:
                content_type_distribution["other"] += 1
            
            # Расчет часов на контент
            if content_type == "blog_post":
                total_estimated_hours += hours_per_blog_post
            elif content_type == "guide":
                total_estimated_hours += hours_per_guide
            elif content_type == "video":
                total_estimated_hours += hours_per_video
            elif content_type == "infographic":
                total_estimated_hours += hours_per_infographic
            else:
                total_estimated_hours += hours_per_blog_post  # Дефолтное значение
        
        # Расчет необходимой команды
        monthly_working_hours = 160  # 20 рабочих дней * 8 часов
        total_content_pieces = len(content_calendar)
        
        # Предполагаем календарь на 3 месяца (может быть настроено)
        calendar_duration_months = min(max(1, total_content_pieces // 8), 12)
        monthly_hours_needed = total_estimated_hours / calendar_duration_months
        
        # Размер команды (с запасом 20%)
        team_size_needed = max(1, int((monthly_hours_needed * 1.2) / monthly_working_hours))
        
        # Бюджет (базируется на часовой ставке)
        hourly_rate = 2000  # ₽ за час (средняя ставка контент-маркетолога)
        monthly_budget = int(monthly_hours_needed * hourly_rate)
        
        # Детализация по ролям
        role_distribution = {
            "content_writer": {
                "count": max(1, team_size_needed - 1),
                "monthly_hours": monthly_hours_needed * 0.7,
                "hourly_rate": 1800,
                "monthly_cost": int(monthly_hours_needed * 0.7 * 1800)
            },
            "editor": {
                "count": 1 if team_size_needed > 1 else 0.5,
                "monthly_hours": monthly_hours_needed * 0.2,
                "hourly_rate": 2500,
                "monthly_cost": int(monthly_hours_needed * 0.2 * 2500)
            },
            "designer": {
                "count": 0.5,
                "monthly_hours": monthly_hours_needed * 0.1,
                "hourly_rate": 2200,
                "monthly_cost": int(monthly_hours_needed * 0.1 * 2200)
            }
        }
        
        return {
            "total_pieces": total_content_pieces,
            "estimated_total_hours": total_estimated_hours,
            "monthly_hours_needed": int(monthly_hours_needed),
            "calendar_duration_months": calendar_duration_months,
            "team_size_needed": team_size_needed,
            "monthly_budget": monthly_budget,
            "content_type_distribution": content_type_distribution,
            "role_distribution": role_distribution,
            "efficiency_metrics": {
                "hours_per_piece": round(total_estimated_hours / max(1, total_content_pieces), 1),
                "pieces_per_month": round(total_content_pieces / calendar_duration_months, 1),
                "cost_per_piece": round(monthly_budget / max(1, (total_content_pieces / calendar_duration_months)), 0)
            },
            "scaling_recommendations": [
                f"Текущая команда из {team_size_needed} человек оптимальна",
                f"Планируемая производительность: {round(total_content_pieces / calendar_duration_months, 1)} контента/месяц",
                f"Средняя стоимость контента: {round(monthly_budget / max(1, (total_content_pieces / calendar_duration_months)), 0):,.0f} ₽",
                "Рекомендуется резерв бюджета 15% на неожиданные задачи"
            ]
        }
    
    def _prioritize_implementation_steps(self, keyword_research: Dict, content_strategy: Dict, topic_clustering: Dict) -> List[Dict[str, Any]]:
        """Приоритизация шагов реализации контентной стратегии"""
        
        implementation_steps = []
        
        # Шаг 1: Анализ и исследование
        research_priority = self._calculate_research_priority(keyword_research, topic_clustering)
        implementation_steps.append({
            "step": 1,
            "phase": "Research & Analysis",
            "title": "Глубокий анализ ключевых слов и конкурентов",
            "duration": "2-3 недели",
            "priority": research_priority,
            "tasks": [
                "Завершение keyword research по всем направлениям",
                "Анализ топ-10 конкурентов в SERP",
                "Определение content gaps и возможностей",
                "Валидация topic clusters с бизнес-целями"
            ],
            "deliverables": ["Keyword matrix", "Competitor analysis", "Content gap analysis"],
            "resources_needed": ["SEO аналитик", "Content strategist"],
            "success_criteria": "100% ключевых кластеров проанализированы и приоритизированы"
        })
        
        # Шаг 2: Техническая подготовка
        technical_priority = self._calculate_technical_priority(content_strategy)
        implementation_steps.append({
            "step": 2,
            "phase": "Technical Setup",
            "title": "Техническая подготовка и настройка инфраструктуры",
            "duration": "1-2 недели",
            "priority": technical_priority,
            "tasks": [
                "Настройка CMS и SEO-инструментов",
                "Создание шаблонов контента",
                "Настройка аналитики и трекинга",
                "Подготовка workflow для контент-команды"
            ],
            "deliverables": ["Content templates", "Analytics setup", "Workflow documentation"],
            "resources_needed": ["Technical SEO", "Web developer"],
            "success_criteria": "Вся техническая инфраструктура готова к production"
        })
        
        # Шаг 3: Создание пилотного контента
        pilot_priority = self._calculate_pilot_priority(keyword_research, topic_clustering)
        implementation_steps.append({
            "step": 3,
            "phase": "Pilot Content Creation",
            "title": "Создание пилотного контента по топ-приоритетным кластерам",
            "duration": "3-4 недели",
            "priority": pilot_priority,
            "tasks": [
                "Создание 5-10 ключевых контентных материалов",
                "Оптимизация под целевые ключевые слова",
                "A/B тестирование заголовков и meta-данных",
                "Настройка внутренней перелинковки"
            ],
            "deliverables": ["Pilot content pieces", "Performance baselines", "Optimization insights"],
            "resources_needed": ["Content writer", "SEO specialist", "Editor"],
            "success_criteria": "Pilot контент показывает рост позиций в топ-20"
        })
        
        # Шаг 4: Масштабирование
        scaling_priority = self._calculate_scaling_priority(content_strategy, topic_clustering)
        implementation_steps.append({
            "step": 4,
            "phase": "Scaling & Optimization",
            "title": "Масштабирование контентного производства",
            "duration": "8-12 недель",
            "priority": scaling_priority,
            "tasks": [
                "Увеличение объемов контент-производства",
                "Автоматизация рутинных SEO-процессов",
                "Построение контентных хабов и pillar pages",
                "Continuous optimization на основе данных"
            ],
            "deliverables": ["Scaled content production", "Hub architecture", "Performance reports"],
            "resources_needed": ["Content team", "SEO manager", "Data analyst"],
            "success_criteria": "Стабильный рост органического трафика на 25%+"
        })
        
        # Сортируем по приоритету
        implementation_steps.sort(key=lambda x: x["priority"], reverse=True)
        
        # Добавляем общие рекомендации
        implementation_summary = {
            "total_phases": len(implementation_steps),
            "estimated_timeline": "14-21 неделя",
            "critical_success_factors": [
                "Качественный keyword research как фундамент",
                "Техническая готовность платформы",
                "Консистентность в создании контента",
                "Continuous monitoring и optimization"
            ],
            "risk_mitigation": [
                "Weekly progress reviews",
                "Backup content calendar на случай задержек",
                "Cross-training команды для взаимозаменяемости",
                "Flexible resource allocation"
            ],
            "roi_expectations": {
                "month_3": "Первые позитивные сигналы в SERP",
                "month_6": "25-40% рост органического трафика",
                "month_12": "Достижение топ-3 позиций по ключевым запросам"
            }
        }
        
        return {
            "implementation_steps": implementation_steps,
            "summary": implementation_summary,
            "next_actions": [
                implementation_steps[0]["tasks"][0] if implementation_steps else "Начать keyword research",
                "Собрать проектную команду",
                "Установить KPI и метрики успеха"
            ]
        }
    
    def _calculate_research_priority(self, keyword_research: Dict, topic_clustering: Dict) -> float:
        """Расчет приоритета этапа исследования"""
        base_priority = 0.9  # Высокий приоритет для research
        
        # Бонусы за качество данных
        if keyword_research.get("keyword_research_results", {}).get("total_keywords", 0) > 1000:
            base_priority += 0.05
        if topic_clustering.get("topic_clusters", {}).get("total_clusters", 0) > 10:
            base_priority += 0.03
        
        return min(1.0, base_priority)
    
    def _calculate_technical_priority(self, content_strategy: Dict) -> float:
        """Расчет приоритета технической подготовки"""
        return 0.85  # Стандартный высокий приоритет
    
    def _calculate_pilot_priority(self, keyword_research: Dict, topic_clustering: Dict) -> float:
        """Расчет приоритета пилотного контента"""
        base_priority = 0.8
        
        # Увеличиваем приоритет если много high-volume keywords
        total_keywords = keyword_research.get("keyword_research_results", {}).get("total_keywords", 0)
        if total_keywords > 500:
            base_priority += 0.1
        
        return min(1.0, base_priority)
    
    def _calculate_scaling_priority(self, content_strategy: Dict, topic_clustering: Dict) -> float:
        """Расчет приоритета масштабирования"""
        return 0.7  # Средний приоритет, зависит от успеха предыдущих этапов