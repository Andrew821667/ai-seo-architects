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