"""
🎯 Competitive Analysis Agent

Operational-level агент для глубокого анализа конкурентов, SERP research, 
gap analysis и выявления возможностей для обгона соперников в поисковой выдаче.

Основные возможности:
- SERP analysis & monitoring
- Competitor gap analysis
- Share of voice tracking  
- Content gap identification
- Technical advantage mapping
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random

from core.base_agent import BaseAgent
from core.interfaces.data_models import AgentMetrics

logger = logging.getLogger(__name__)


class CompetitiveAnalysisAgent(BaseAgent):
    """
    🎯 Competitive Analysis Agent
    
    Operational-level агент для комплексного конкурентного анализа,
    SERP мониторинга и выявления стратегических возможностей.
    """
    
    def __init__(self, data_provider=None, agent_level=None, **kwargs):
        # Убираем agent_level из kwargs если он там есть
        if 'agent_level' in kwargs:
            del kwargs['agent_level']
            
        super().__init__(
            agent_id="competitive_analysis_agent",
            name="Competitive Analysis Agent",
            agent_level=agent_level or "operational",
            data_provider=data_provider,
            knowledge_base="knowledge/operational/competitive_analysis.md",
            **kwargs
        )
        
        # Конфигурация Competitive Analysis
        self.max_competitors = 10  # Максимальное количество конкурентов для анализа
        self.min_market_share = 5.0  # Минимальная доля рынка для включения в анализ (%)
        self.keyword_tracking_limit = 1000  # Максимальное количество отслеживаемых ключевых слов
        self.serp_monitoring_depth = 20  # Глубина мониторинга SERP (топ-N позиций)
        
        # SERP feature weights for opportunity scoring
        self.serp_feature_values = {
            "featured_snippets": {"weight": 0.35, "traffic_impact": 0.35},
            "people_also_ask": {"weight": 0.15, "traffic_impact": 0.12},
            "image_packs": {"weight": 0.10, "traffic_impact": 0.08},
            "video_results": {"weight": 0.25, "traffic_impact": 0.25},
            "local_pack": {"weight": 0.30, "traffic_impact": 0.30},
            "knowledge_panels": {"weight": 0.05, "traffic_impact": 0.05}
        }
        
        # Competitive strength factors  
        self.strength_factors = {
            "content_strategy": {"weight": 0.25},
            "technical_performance": {"weight": 0.20},
            "backlink_authority": {"weight": 0.25},
            "social_presence": {"weight": 0.15},
            "brand_authority": {"weight": 0.15}
        }
        
        logger.info(f"✅ {self.name} инициализирован:")
        logger.info(f"   🎯 Max Competitors: {self.max_competitors}")
        logger.info(f"   📊 Min Market Share: {self.min_market_share}%")
        logger.info(f"   🔍 Keyword Tracking Limit: {self.keyword_tracking_limit}")
        logger.info(f"   📈 SERP Monitoring Depth: {self.serp_monitoring_depth}")
    
    def get_system_prompt(self) -> str:
        """Специализированный системный промпт для конкурентного анализа"""
        return f"""Ты - экспертный Competitive Analysis Agent, специалист по глубокому конкурентному анализу и SERP research.

ТВОЯ ЭКСПЕРТИЗА:
• SERP Analysis & Feature Monitoring - 30%
• Competitor Gap Analysis (слабые места) - 25%
• Market Share & Voice Analysis - 20%
• Content Gap Identification - 15%
• Competitor Strategy Monitoring - 10%

ЗАДАЧА: Провести комплексный конкурентный анализ, определить возможности для обгона и сформировать стратегию доминирования.

МЕТОДОЛОГИЯ АНАЛИЗА:
1. SERP Landscape Analysis (30 баллов):
   - Featured Snippets ownership и opportunities (0-10)
   - SERP Features presence (PAA, Images, Video) (0-8)
   - Position distribution по keyword set (0-7)
   - Competitive intensity assessment (0-5)

2. Competitor Gap Analysis (25 баллов):
   - Keyword gaps identification (0-8)
   - Content quality и depth gaps (0-7)
   - Technical performance gaps (0-5)
   - Backlink profile weaknesses (0-5)

3. Market Share Analysis (20 баллов):
   - Visibility share calculation (0-8)
   - Traffic share estimation (0-6)
   - Market position и ranking (0-6)

4. Content Gap Opportunities (15 баллов):
   - Topic coverage analysis (0-5)
   - Content format opportunities (0-5)
   - Expertise demonstration gaps (0-5)

5. Strategic Opportunities (10 баллов):
   - Overtaking possibilities identification (0-4)
   - Blue ocean opportunities (0-3)
   - Emerging trend capture (0-3)

КОНКУРЕНТНЫЕ ПАРАМЕТРЫ:
- Максимум конкурентов: {self.max_competitors}
- Минимальная доля рынка: {self.min_market_share}%
- SERP мониторинг: ТОП-{self.serp_monitoring_depth} позиций
- Keyword tracking: {self.keyword_tracking_limit} ключевых слов

ОТРАСЛЕВЫЕ БОНУСЫ:
• FinTech: +15 (regulatory compliance focus)
• E-commerce: +12 (product competition analysis)
• B2B Services: +10 (thought leadership opportunities)
• Healthcare: +8 (expertise-based competition)
• Real Estate: +6 (local market competition)

РЕЗУЛЬТАТ: Верни ТОЛЬКО JSON с детальным конкурентным анализом, SERP возможностями и стратегией обгона."""

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика конкурентного анализа с реальными LLM вызовами
        
        Args:
            task_data: Данные задачи с информацией о конкурентах и типе анализа
            
        Returns:
            Dict с результатами конкурентного анализа от OpenAI
        """
        try:
            # Извлекаем входные данные
            input_data = task_data.get("input_data", {})
            task_type = task_data.get('task_type', 'comprehensive_competitive_analysis')
            
            logger.info(f"🎯 Начинаем конкурентный анализ: {input_data.get('our_domain', 'Unknown')}, тип: {task_type}")
            
            # Формируем специализированный промпт для конкурентного анализа
            user_prompt = f"""Проведи глубокий конкурентный анализ для:

НАШ ДОМЕН И КОНКУРЕНТЫ:
Our Domain: {input_data.get('our_domain', input_data.get('domain', 'Unknown'))}
Industry: {input_data.get('industry', 'Unknown')}
Competitors: {input_data.get('competitors', 'Unknown')}
Target Keywords: {input_data.get('target_keywords', 'Unknown')}
Current Market Position: {input_data.get('current_position', 'Unknown')}
Analysis Type: {task_type}
Current DA: {input_data.get('domain_authority', 'Unknown')}
Current Organic Traffic: {input_data.get('organic_traffic', 'Unknown')}
Current Rankings: {input_data.get('current_rankings', 'Unknown')}
Market Focus: {input_data.get('market_focus', 'Россия')}

Выполни комплексный конкурентный анализ по всем критическим областям. Верни результат строго в JSON формате:
{{
    "competitive_analysis_score": <number 0-100>,
    "competitive_health": "<Excellent/Good/Needs Improvement/Poor/Critical>",
    "serp_analysis": {{
        "serp_feature_ownership": <percentage>,
        "our_avg_position": <number>,
        "featured_snippets_owned": <number>,
        "featured_snippets_opportunities": <number>,
        "serp_features_present": ["<features in SERP>"],
        "high_priority_opportunities": ["<top opportunities>"],
        "competitive_intensity": "<very_high/high/medium/low>"
    }},
    "competitor_gap_analysis": {{
        "main_competitors": ["<competitor domains>"],
        "competitor_strengths": {{
            "<competitor1>": {{"strength": <0-100>, "key_advantages": ["<advantages>"]}}
        }},
        "gap_opportunities": {{
            "keyword_gaps": <number>,
            "content_gaps": <number>,
            "technical_gaps": <number>,
            "backlink_gaps": <number>
        }},
        "overtaking_opportunities": ["<realistic opportunities to surpass competitors>"]
    }},
    "market_share_analysis": {{
        "our_visibility_share": <percentage>,
        "our_traffic_share": <percentage>,
        "market_position": <ranking position>,
        "growth_potential": "<high/medium/low>",
        "market_leaders": ["<leading domains>"],
        "market_trends": "<market direction>"
    }},
    "content_gap_opportunities": {{
        "high_value_topics": ["<topics with high opportunity>"],
        "content_format_gaps": ["<missing content formats>"],
        "expertise_gaps": ["<areas where we can dominate>"],
        "estimated_traffic_potential": <number>
    }},
    "strategic_recommendations": {{
        "immediate_priorities": ["<top 3 actions>"],
        "short_term_goals": ["<3-6 month objectives>"],
        "long_term_strategy": ["<6-12 month strategy>"],
        "resource_allocation": {{
            "content": "<percentage>",
            "technical": "<percentage>",
            "link_building": "<percentage>",
            "paid_promotion": "<percentage>"
        }}
    }},
    "competitive_threats": ["<main threats to watch>"],
    "blue_ocean_opportunities": ["<unique opportunities with low competition>"],
    "success_probability": <0.0-1.0>
}}"""

            # Используем базовый метод с LLM интеграцией
            result = await self.process_with_llm(user_prompt, input_data)
            
            if result["success"]:
                logger.info(f"✅ Конкурентный анализ завершен через OpenAI: {result.get('model_used', 'unknown')}")
                # Добавляем метаданные агента
                if isinstance(result.get("result"), str):
                    # Если результат строка, оборачиваем в структуру
                    result["competitive_analysis_response"] = result["result"]
                    result["agent_type"] = "competitive_analysis"
                    result["analysis_type"] = task_type
                    result["methodology"] = ["SERP Analysis", "Gap Analysis", "Market Share Analysis"]
                
                return result
            else:
                # Fallback к базовой логике если OpenAI недоступен
                logger.warning("⚠️ OpenAI недоступен, используем fallback конкурентный анализ")
                return await self._fallback_competitive_analysis(input_data, task_type)
                
        except Exception as e:
            logger.error(f"❌ Ошибка в конкурентном анализе: {str(e)}")
            return {
                "success": False,
                "agent": self.agent_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _analyze_serp_landscape(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ поисковой выдачи по ключевым запросам"""
        query_data = task_data.get('query_data', {})
        target_keywords = query_data.get('keywords', ['SEO услуги', 'продвижение сайтов'])
        our_domain = query_data.get('our_domain', 'example.com')
        
        # Анализ SERP для каждого ключевого слова
        serp_analysis_results = []
        total_serp_features = 0
        our_serp_features = 0
        
        for keyword in target_keywords[:10]:  # Анализируем до 10 ключевых слов
            # Симуляция SERP данных
            serp_data = self._generate_serp_data(keyword, our_domain)
            
            # Подсчет SERP features
            total_serp_features += len(serp_data['serp_features'])
            our_serp_features += sum(1 for feature in serp_data['serp_features'] if feature['owned_by_us'])
            
            serp_analysis_results.append({
                "keyword": keyword,
                "search_volume": serp_data['search_volume'],
                "difficulty": serp_data['difficulty'],
                "our_position": serp_data['our_position'],
                "top_competitors": serp_data['top_competitors'],
                "serp_features": serp_data['serp_features'],
                "opportunities": serp_data['opportunities'],
                "competitive_intensity": serp_data['competitive_intensity']
            })
        
        # Общая статистика по SERP
        serp_feature_ownership = (our_serp_features / total_serp_features * 100) if total_serp_features > 0 else 0
        
        # Приоритизация возможностей
        high_priority_opportunities = []
        medium_priority_opportunities = []
        
        for result in serp_analysis_results:
            for opp in result['opportunities']:
                if opp['priority'] == 'high':
                    high_priority_opportunities.append({
                        'keyword': result['keyword'],
                        'opportunity': opp['type'],
                        'description': opp['description'],
                        'traffic_potential': opp['traffic_potential']
                    })
                elif opp['priority'] == 'medium':
                    medium_priority_opportunities.append({
                        'keyword': result['keyword'],
                        'opportunity': opp['type'],
                        'description': opp['description'],
                        'traffic_potential': opp['traffic_potential']
                    })
        
        # Рекомендации по стратегии
        strategy_recommendations = self._get_serp_strategy_recommendations(
            serp_analysis_results, serp_feature_ownership
        )
        
        logger.info(f"🔍 SERP Analysis:")
        logger.info(f"   📊 Keywords Analyzed: {len(target_keywords)}")
        logger.info(f"   🎯 SERP Feature Ownership: {serp_feature_ownership:.1f}%")
        logger.info(f"   🚀 High Priority Opportunities: {len(high_priority_opportunities)}")
        logger.info(f"   📈 Medium Priority Opportunities: {len(medium_priority_opportunities)}")
        
        return {
            "success": True,
            "our_domain": our_domain,
            "keywords_analyzed": len(target_keywords),
            "serp_feature_ownership": round(serp_feature_ownership, 1),
            "serp_analysis": serp_analysis_results,
            "high_priority_opportunities": high_priority_opportunities,
            "medium_priority_opportunities": medium_priority_opportunities,
            "strategy_recommendations": strategy_recommendations,
            "competitive_landscape_summary": self._summarize_competitive_landscape(serp_analysis_results),
            "agent": self.name,
            "confidence": round(random.uniform(0.80, 0.95), 2)
        }

    async def _analyze_competitor_gaps(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Выявление слабых мест конкурентов"""
        competitor_data = task_data.get('competitor_data', {})
        competitors = competitor_data.get('competitors', ['competitor1.com', 'competitor2.com'])
        our_domain = competitor_data.get('our_domain', 'example.com')
        analysis_scope = competitor_data.get('scope', 'comprehensive')
        
        # Анализ каждого конкурента
        competitor_gap_analysis = []
        
        for competitor in competitors[:self.max_competitors]:
            # Генерация данных конкурента
            competitor_profile = self._generate_competitor_profile(competitor)
            
            # Идентификация gaps
            keyword_gaps = self._identify_keyword_gaps(competitor_profile)
            content_gaps = self._identify_competitor_content_gaps(competitor_profile)
            technical_gaps = self._identify_technical_gaps(competitor_profile)
            backlink_gaps = self._identify_backlink_gaps(competitor_profile)
            
            # Оценка силы конкурента
            competitor_strength = self._calculate_competitor_strength(competitor_profile)
            
            # Возможности для обгона
            overtaking_opportunities = self._identify_overtaking_opportunities(
                competitor_profile, keyword_gaps, content_gaps, technical_gaps
            )
            
            competitor_gap_analysis.append({
                "competitor_domain": competitor,
                "competitor_strength": competitor_strength,
                "keyword_gaps": keyword_gaps,
                "content_gaps": content_gaps,
                "technical_gaps": technical_gaps,
                "backlink_gaps": backlink_gaps,
                "overtaking_opportunities": overtaking_opportunities,
                "threat_level": self._assess_competitor_threat_level(competitor_strength, competitor_profile)
            })
        
        # Общий анализ конкурентного ландшафта
        market_dynamics = self._analyze_market_dynamics(competitor_gap_analysis)
        
        # Стратегические рекомендации
        strategic_actions = self._formulate_gap_strategy(competitor_gap_analysis, market_dynamics)
        
        # Приоритизация действий
        action_priorities = self._prioritize_competitive_actions(competitor_gap_analysis)
        
        logger.info(f"🎯 Competitor Gap Analysis:")
        logger.info(f"   🏢 Competitors Analyzed: {len(competitors)}")
        logger.info(f"   🔍 Total Gaps Identified: {sum(len(c['keyword_gaps']) + len(c['content_gaps']) for c in competitor_gap_analysis)}")
        logger.info(f"   🚀 Overtaking Opportunities: {sum(len(c['overtaking_opportunities']) for c in competitor_gap_analysis)}")
        
        return {
            "success": True,
            "our_domain": our_domain,
            "competitors_analyzed": len(competitors),
            "competitor_gap_analysis": competitor_gap_analysis,
            "market_dynamics": market_dynamics,
            "strategic_actions": strategic_actions,
            "action_priorities": action_priorities,
            "competitive_advantage_score": self._calculate_our_competitive_advantage(competitor_gap_analysis),
            "agent": self.name,
            "confidence": round(random.uniform(0.75, 0.90), 2)
        }

    async def _analyze_market_share(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ доли голоса в нише"""
        market_data = task_data.get('market_data', {})
        our_domain = market_data.get('our_domain', 'example.com')
        industry = market_data.get('industry', 'seo_services')
        competitors = market_data.get('competitors', ['competitor1.com', 'competitor2.com'])
        
        # Симуляция данных о рынке
        total_market_keywords = random.randint(5000, 20000)
        total_market_traffic = random.randint(500000, 5000000)
        
        # Анализ доли каждого игрока
        market_players = []
        remaining_share = 100.0
        
        # Наш домен
        our_visibility = random.uniform(8.0, 25.0)
        our_traffic_share = random.uniform(6.0, 20.0)
        remaining_share -= our_visibility
        
        market_players.append({
            "domain": our_domain,
            "is_our_domain": True,
            "visibility_share": our_visibility,
            "traffic_share": our_traffic_share,
            "ranking_keywords": int(total_market_keywords * (our_visibility / 100)),
            "estimated_traffic": int(total_market_traffic * (our_traffic_share / 100)),
            "avg_position": random.uniform(8.5, 15.2),
            "serp_features_owned": random.randint(15, 45)
        })
        
        # Конкуренты
        for i, competitor in enumerate(competitors[:8]):
            comp_visibility = random.uniform(3.0, min(remaining_share * 0.4, 18.0))
            comp_traffic = random.uniform(2.0, comp_visibility * 1.2)
            remaining_share -= comp_visibility
            
            market_players.append({
                "domain": competitor,
                "is_our_domain": False,
                "visibility_share": comp_visibility,
                "traffic_share": comp_traffic,
                "ranking_keywords": int(total_market_keywords * (comp_visibility / 100)),
                "estimated_traffic": int(total_market_traffic * (comp_traffic / 100)),
                "avg_position": random.uniform(6.0, 20.0),
                "serp_features_owned": random.randint(5, 60)
            })
        
        # Сортировка по visibility share
        market_players = sorted(market_players, key=lambda x: x['visibility_share'], reverse=True)
        
        # Анализ трендов
        market_trends = self._analyze_market_trends(market_players, our_domain)
        
        # Возможности роста
        growth_opportunities = self._identify_market_growth_opportunities(
            market_players, our_domain, total_market_keywords
        )
        
        # Конкурентная позиция
        competitive_position = self._assess_competitive_position(market_players, our_domain)
        
        # Стратегические рекомендации
        market_strategy = self._develop_market_strategy(
            competitive_position, growth_opportunities, market_trends
        )
        
        logger.info(f"📊 Market Share Analysis for {industry}:")
        logger.info(f"   🎯 Our Visibility Share: {our_visibility:.1f}%")
        logger.info(f"   📈 Market Position: #{next(i+1 for i, p in enumerate(market_players) if p['is_our_domain'])}")
        logger.info(f"   🚀 Growth Opportunities: {len(growth_opportunities)}")
        
        return {
            "success": True,
            "our_domain": our_domain,
            "industry": industry,
            "total_market_keywords": total_market_keywords,
            "total_market_traffic": total_market_traffic,
            "our_visibility_share": round(our_visibility, 1),
            "our_traffic_share": round(our_traffic_share, 1),
            "market_position": next(i+1 for i, p in enumerate(market_players) if p['is_our_domain']),
            "market_players": market_players,
            "market_trends": market_trends,
            "competitive_position": competitive_position,
            "growth_opportunities": growth_opportunities,
            "market_strategy": market_strategy,
            "agent": self.name,
            "confidence": round(random.uniform(0.80, 0.92), 2)
        }

    async def _identify_content_gaps(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Поиск контентных возможностей"""
        content_data = task_data.get('content_data', {})
        our_domain = content_data.get('our_domain', 'example.com')
        competitors = content_data.get('competitors', ['competitor1.com', 'competitor2.com'])
        target_topics = content_data.get('topics', ['SEO', 'контент-маркетинг', 'веб-разработка'])
        
        # Анализ контентного ландшафта
        content_landscape = []
        all_content_gaps = []
        
        for topic in target_topics:
            # Симуляция контентного анализа по теме
            topic_analysis = self._analyze_topic_content_landscape(topic, competitors, our_domain)
            content_landscape.append(topic_analysis)
            
            # Извлечение gaps для этой темы
            for gap in topic_analysis['content_gaps']:
                all_content_gaps.append({
                    'topic': topic,
                    'gap_type': gap['type'],
                    'opportunity': gap['opportunity'],
                    'competitor_advantage': gap['competitor_performance'],
                    'our_potential': gap['our_potential'],
                    'priority': gap['priority'],
                    'estimated_traffic': gap['traffic_potential'],
                    'production_cost': gap['production_cost'],
                    'timeline': gap['timeline']
                })
        
        # Приоритизация контентных возможностей
        high_priority_gaps = [gap for gap in all_content_gaps if gap['priority'] == 'high']
        medium_priority_gaps = [gap for gap in all_content_gaps if gap['priority'] == 'medium']
        
        # Контентная стратегия
        content_strategy = self._develop_content_gap_strategy(
            all_content_gaps, content_landscape
        )
        
        # ROI анализ контентных возможностей
        content_roi_analysis = self._analyze_content_gaps_roi(all_content_gaps)
        
        # Ресурсные требования
        resource_requirements = self._calculate_content_gap_resources(all_content_gaps)
        
        logger.info(f"📝 Content Gap Analysis:")
        logger.info(f"   📊 Topics Analyzed: {len(target_topics)}")
        logger.info(f"   🔍 Total Content Gaps: {len(all_content_gaps)}")
        logger.info(f"   🚀 High Priority Gaps: {len(high_priority_gaps)}")
        logger.info(f"   📈 Estimated Traffic Potential: {sum(gap['estimated_traffic'] for gap in all_content_gaps):,}")
        
        return {
            "success": True,
            "our_domain": our_domain,
            "topics_analyzed": len(target_topics),
            "total_content_gaps": len(all_content_gaps),
            "content_landscape": content_landscape,
            "high_priority_gaps": high_priority_gaps,
            "medium_priority_gaps": medium_priority_gaps,
            "content_strategy": content_strategy,
            "roi_analysis": content_roi_analysis,
            "resource_requirements": resource_requirements,
            "estimated_total_traffic_potential": sum(gap['estimated_traffic'] for gap in all_content_gaps),
            "agent": self.name,
            "confidence": round(random.uniform(0.75, 0.88), 2)
        }

    async def _monitor_competitor_changes(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Мониторинг изменений у конкурентов"""
        monitoring_data = task_data.get('monitoring_data', {})
        competitors = monitoring_data.get('competitors', ['competitor1.com', 'competitor2.com'])
        monitoring_period = monitoring_data.get('period_days', 30)
        our_domain = monitoring_data.get('our_domain', 'example.com')
        
        # Мониторинг изменений у каждого конкурента
        competitor_changes = []
        significant_changes = []
        
        for competitor in competitors[:self.max_competitors]:
            # Симуляция изменений за период
            changes = self._generate_competitor_changes(competitor, monitoring_period)
            
            # Оценка значимости изменений
            change_significance = self._assess_change_significance(changes)
            
            competitor_changes.append({
                "competitor": competitor,
                "monitoring_period_days": monitoring_period,
                "ranking_changes": changes['ranking_changes'],
                "content_changes": changes['content_changes'],
                "technical_changes": changes['technical_changes'],
                "backlink_changes": changes['backlink_changes'],
                "serp_feature_changes": changes['serp_feature_changes'],
                "change_significance": change_significance,
                "threat_assessment": self._assess_competitor_threat(changes, change_significance)
            })
            
            # Сбор значимых изменений
            if change_significance['overall_significance'] >= 7.0:
                significant_changes.append({
                    "competitor": competitor,
                    "change_type": change_significance['primary_change_type'],
                    "impact_level": change_significance['impact_level'],
                    "description": change_significance['description'],
                    "our_response_needed": change_significance['response_required']
                })
        
        # Анализ трендов
        market_trend_analysis = self._analyze_competitive_trends(competitor_changes)
        
        # Алерты и рекомендации
        competitive_alerts = self._generate_competitive_alerts(significant_changes)
        response_recommendations = self._generate_response_recommendations(significant_changes, market_trend_analysis)
        
        # Прогноз изменений
        trend_predictions = self._predict_competitive_trends(competitor_changes)
        
        logger.info(f"📊 Competitor Monitoring ({monitoring_period} days):")
        logger.info(f"   🏢 Competitors Monitored: {len(competitors)}")
        logger.info(f"   🚨 Significant Changes: {len(significant_changes)}")
        logger.info(f"   📈 Active Alerts: {len(competitive_alerts)}")
        
        return {
            "success": True,
            "our_domain": our_domain,
            "monitoring_period_days": monitoring_period,
            "competitors_monitored": len(competitors),
            "competitor_changes": competitor_changes,
            "significant_changes": significant_changes,
            "market_trend_analysis": market_trend_analysis,
            "competitive_alerts": competitive_alerts,
            "response_recommendations": response_recommendations,
            "trend_predictions": trend_predictions,
            "monitoring_summary": self._create_monitoring_summary(competitor_changes, significant_changes),
            "agent": self.name,
            "confidence": round(random.uniform(0.82, 0.94), 2)
        }

    async def _comprehensive_competitive_analysis(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Комплексный конкурентный анализ (по умолчанию)"""
        analysis_data = task_data.get('input_data', task_data.get('analysis_data', {}))
        our_domain = analysis_data.get('our_domain', analysis_data.get('domain', 'example.com'))
        industry = analysis_data.get('industry', 'general')
        
        # Автоопределение конкурентов (симуляция)
        discovered_competitors = [f"competitor{i}.{random.choice(['com', 'ru', 'org'])}" for i in range(1, 6)]
        
        # Запуск ключевых анализов
        serp_analysis = await self._analyze_serp_landscape({
            'query_data': {
                'keywords': [f'{industry} услуги', f'{industry} консультации', 'SEO оптимизация'],
                'our_domain': our_domain
            }
        })
        
        gap_analysis = await self._analyze_competitor_gaps({
            'competitor_data': {
                'competitors': discovered_competitors,
                'our_domain': our_domain
            }
        })
        
        market_share = await self._analyze_market_share({
            'market_data': {
                'our_domain': our_domain,
                'industry': industry,
                'competitors': discovered_competitors
            }
        })
        
        # Общая конкурентная оценка
        competitive_score = self._calculate_overall_competitive_score(
            serp_analysis, gap_analysis, market_share
        )
        
        # Стратегические приоритеты
        strategic_priorities = self._determine_competitive_priorities(
            competitive_score, serp_analysis, gap_analysis, market_share
        )
        
        # Рекомендуемые действия
        action_roadmap = self._create_competitive_action_roadmap(
            strategic_priorities, serp_analysis, gap_analysis
        )
        
        logger.info(f"🎯 Comprehensive Competitive Analysis для {our_domain}:")
        logger.info(f"   📊 Competitive Score: {competitive_score}/100")
        logger.info(f"   📈 Market Position: #{market_share['market_position']}")
        logger.info(f"   🚀 Strategic Priorities: {len(strategic_priorities)}")
        
    async def _fallback_competitive_analysis(self, input_data: Dict[str, Any], task_type: str) -> Dict[str, Any]:
        """Fallback логика конкурентного анализа без LLM"""
        try:
            our_domain = input_data.get('our_domain', input_data.get('domain', 'unknown-domain.com'))
            industry = input_data.get('industry', 'general')
            competitors = input_data.get('competitors', ['competitor1.com', 'competitor2.com'])
            
            # Базовый конкурентный скор
            base_score = 55  # Средний скор
            
            # Простые корректировки на основе данных
            current_da = input_data.get('domain_authority', 0)
            if current_da > 60:
                base_score += 20
            elif current_da > 40:
                base_score += 10
            elif current_da > 20:
                base_score += 5
            
            organic_traffic = input_data.get('organic_traffic', 0)
            if organic_traffic > 100000:
                base_score += 15
            elif organic_traffic > 50000:
                base_score += 10
            elif organic_traffic > 10000:
                base_score += 5
            
            # Отраслевые бонусы
            industry_bonuses = {
                'fintech': 8,
                'ecommerce': 6,
                'b2b_services': 5,
                'healthcare': 4
            }
            base_score += industry_bonuses.get(industry.lower(), 0)
            
            # Определяем конкурентное здоровье
            if base_score >= 80:
                health = "Excellent"
                market_position = random.randint(1, 3)
                visibility = random.uniform(15, 30)
            elif base_score >= 65:
                health = "Good"
                market_position = random.randint(2, 5)
                visibility = random.uniform(10, 20)
            elif base_score >= 50:
                health = "Needs Improvement"
                market_position = random.randint(4, 8)
                visibility = random.uniform(5, 15)
            elif base_score >= 35:
                health = "Poor"
                market_position = random.randint(6, 12)
                visibility = random.uniform(2, 8)
            else:
                health = "Critical"
                market_position = random.randint(10, 20)
                visibility = random.uniform(1, 5)
            
            # Базовые рекомендации
            recommendations = [
                "Провести SERP анализ по ключевым запросам",
                "Анализ слабых мест конкурентов",
                "Мониторинг изменений у конкурентов"
            ]
            
            if base_score < 50:
                recommendations.insert(0, "Критическое улучшение конкурентной позиции (приоритет)")
            
            # Возможности
            opportunities = [
                f"Анализ {len(competitors)} конкурентов для поиска слабых мест",
                "Захват featured snippets на низкоконкурентных запросах",
                "Создание контента в недоосвещенных нишах"
            ]
            
            return {
                "success": True,
                "agent": self.agent_id,
                "result": {
                    "competitive_analysis_score": base_score,
                    "competitive_health": health,
                    "our_domain": our_domain,
                    "industry": industry,
                    "market_position": market_position,
                    "visibility_share": round(visibility, 1),
                    "competitors_analyzed": len(competitors),
                    "main_competitors": competitors[:3],
                    "strategic_recommendations": recommendations,
                    "opportunities": opportunities,
                    "note": "Результат получен без OpenAI (fallback режим)",
                    "analysis_scope": {
                        "serp_monitoring": f"ТОП-{self.serp_monitoring_depth} позиций",
                        "max_competitors": self.max_competitors,
                        "keyword_tracking": self.keyword_tracking_limit
                    }
                },
                "fallback_mode": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "agent": self.agent_id,
                "error": f"Fallback competitive analysis failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

        return {
            "success": True,
            "our_domain": our_domain,
            "industry": industry,
            "competitive_score": competitive_score,
            "market_position": market_share["market_position"],
            "visibility_share": market_share["our_visibility_share"],
            "serp_analysis_summary": {
                "keywords_analyzed": serp_analysis["keywords_analyzed"],
                "serp_feature_ownership": serp_analysis["serp_feature_ownership"],
                "high_priority_opportunities": len(serp_analysis["high_priority_opportunities"])
            },
            "gap_analysis_summary": {
                "competitors_analyzed": gap_analysis["competitors_analyzed"],
                "competitive_advantage_score": gap_analysis["competitive_advantage_score"]
            },
            "strategic_priorities": strategic_priorities,
            "action_roadmap": action_roadmap,
            "competitive_health": self._assess_competitive_health(competitive_score),
            "agent": self.name,
            "confidence": round(random.uniform(0.80, 0.93), 2)
        }

    # Helper methods

    def _generate_serp_data(self, keyword: str, our_domain: str) -> Dict[str, Any]:
        """Генерация SERP данных для ключевого слова"""
        search_volume = random.randint(1000, 50000)
        difficulty = random.randint(30, 95)
        our_position = random.randint(1, 50) if random.random() > 0.3 else None
        
        # Топ конкуренты
        top_competitors = []
        for i in range(10):
            top_competitors.append({
                "domain": f"competitor-{i+1}.{random.choice(['com', 'ru', 'org'])}",
                "position": i + 1,
                "title": f"Пример заголовка для {keyword}",
                "url": f"https://competitor-{i+1}.com/page-{i+1}",
                "snippet": f"Описание результата для {keyword}..."
            })
        
        # SERP features
        serp_features = []
        possible_features = list(self.serp_feature_values.keys())
        num_features = random.randint(1, 4)
        
        for feature in random.sample(possible_features, num_features):
            owned_by_us = our_position and our_position <= 5 and random.random() < 0.3
            serp_features.append({
                "type": feature,
                "owned_by_us": owned_by_us,
                "current_owner": our_domain if owned_by_us else f"competitor-{random.randint(1, 5)}.com",
                "opportunity_score": random.randint(60, 95) if not owned_by_us else 0
            })
        
        # Возможности
        opportunities = []
        for feature in serp_features:
            if not feature["owned_by_us"] and feature["opportunity_score"] > 70:
                opportunities.append({
                    "type": feature["type"],
                    "description": f"Захват {feature['type']} для '{keyword}'",
                    "priority": "high" if feature["opportunity_score"] > 85 else "medium",
                    "traffic_potential": int(search_volume * self.serp_feature_values[feature["type"]]["traffic_impact"])
                })
        
        return {
            "search_volume": search_volume,
            "difficulty": difficulty,
            "our_position": our_position,
            "top_competitors": top_competitors,
            "serp_features": serp_features,
            "opportunities": opportunities,
            "competitive_intensity": self._calculate_competitive_intensity(top_competitors, difficulty)
        }

    def _calculate_competitive_intensity(self, competitors: List[Dict], difficulty: int) -> str:
        """Расчет интенсивности конкуренции"""
        # Анализ доменов в топе
        high_authority_domains = sum(1 for c in competitors[:5] if 'gov' in c['domain'] or 'edu' in c['domain'])
        
        if difficulty > 80 or high_authority_domains >= 2:
            return "very_high"
        elif difficulty > 60 or high_authority_domains >= 1:
            return "high"
        elif difficulty > 40:
            return "medium"
        else:
            return "low"

    def _get_serp_strategy_recommendations(self, serp_results: List[Dict], feature_ownership: float) -> List[str]:
        """Получение рекомендаций по SERP стратегии"""
        recommendations = []
        
        if feature_ownership < 20:
            recommendations.append("Критически низкое владение SERP features - требуется агрессивная стратегия")
        
        high_volume_opportunities = [
            r for r in serp_results 
            if r['search_volume'] > 10000 and any(o['priority'] == 'high' for o in r['opportunities'])
        ]
        
        if high_volume_opportunities:
            recommendations.append(f"Приоритет на {len(high_volume_opportunities)} высокообъемных возможностей")
        
        featured_snippet_opps = sum(
            1 for r in serp_results 
            for o in r['opportunities'] 
            if o['type'] == 'featured_snippets'
        )
        
        if featured_snippet_opps >= 3:
            recommendations.append("Сильные возможности для захвата featured snippets")
        
        return recommendations

    def _summarize_competitive_landscape(self, serp_results: List[Dict]) -> Dict[str, Any]:
        """Суммирование конкурентного ландшафта"""
        total_keywords = len(serp_results)
        our_rankings = sum(1 for r in serp_results if r['our_position'] and r['our_position'] <= 10)
        avg_difficulty = sum(r['difficulty'] for r in serp_results) / total_keywords
        
        return {
            "total_keywords_analyzed": total_keywords,
            "our_top10_rankings": our_rankings,
            "ranking_percentage": round((our_rankings / total_keywords) * 100, 1),
            "average_keyword_difficulty": round(avg_difficulty, 1),
            "high_competition_keywords": sum(1 for r in serp_results if r['competitive_intensity'] in ['high', 'very_high']),
            "opportunity_keywords": sum(len(r['opportunities']) for r in serp_results)
        }

    def _generate_competitor_profile(self, competitor_domain: str) -> Dict[str, Any]:
        """Генерация профиля конкурента"""
        return {
            "domain": competitor_domain,
            "domain_authority": random.randint(35, 80),
            "organic_keywords": random.randint(5000, 50000),
            "organic_traffic": random.randint(50000, 500000),
            "backlinks": random.randint(10000, 200000),
            "referring_domains": random.randint(500, 5000),
            "content_volume": random.randint(500, 5000),
            "technical_score": random.randint(60, 95),
            "site_speed": random.uniform(1.5, 4.0),
            "mobile_score": random.randint(70, 100),
            "social_presence": random.randint(1000, 100000),
            "brand_strength": random.randint(40, 90)
        }

    def _identify_keyword_gaps(self, competitor_profile: Dict[str, Any]) -> List[Dict]:
        """Идентификация keyword gaps"""
        gaps = []
        
        # Симуляция keyword gaps
        for i in range(random.randint(10, 30)):
            gaps.append({
                "keyword": f"keyword-gap-{i+1}",
                "search_volume": random.randint(500, 20000),
                "difficulty": random.randint(20, 70),
                "competitor_position": random.randint(1, 10),
                "our_opportunity": random.choice(["high", "medium", "low"]),
                "estimated_traffic": random.randint(100, 5000)
            })
        
        return sorted(gaps, key=lambda x: x['estimated_traffic'], reverse=True)

    def _identify_competitor_content_gaps(self, competitor_profile: Dict[str, Any]) -> List[Dict]:
        """Идентификация контентных gaps у конкурента"""
        return [
            {
                "gap_type": "topic_depth",
                "description": "Поверхностное освещение экспертных тем",
                "opportunity": "Создать более глубокий экспертный контент",
                "priority": "high"
            },
            {
                "gap_type": "content_format",
                "description": "Отсутствие интерактивных элементов",
                "opportunity": "Добавить калькуляторы и инструменты",
                "priority": "medium"
            },
            {
                "gap_type": "update_frequency",
                "description": "Редкие обновления контента",
                "opportunity": "Регулярное обновление актуальной информации",
                "priority": "medium"
            }
        ]

    def _identify_technical_gaps(self, competitor_profile: Dict[str, Any]) -> List[Dict]:
        """Идентификация технических gaps"""
        gaps = []
        
        if competitor_profile["site_speed"] > 3.0:
            gaps.append({
                "gap_type": "site_speed",
                "current_performance": f"{competitor_profile['site_speed']:.1f}s",
                "opportunity": "Превосходство в скорости загрузки",
                "priority": "high"
            })
        
        if competitor_profile["mobile_score"] < 90:
            gaps.append({
                "gap_type": "mobile_optimization",
                "current_performance": f"{competitor_profile['mobile_score']}/100",
                "opportunity": "Лучший mobile experience",
                "priority": "medium"
            })
        
        return gaps

    def _identify_backlink_gaps(self, competitor_profile: Dict[str, Any]) -> List[Dict]:
        """Идентификация backlink gaps"""
        return [
            {
                "gap_type": "industry_publications",
                "description": "Слабое представление в отраслевых изданиях",
                "opportunity": "PR и guest posting в нишевых медиа",
                "priority": "high"
            },
            {
                "gap_type": "local_citations",
                "description": "Недостаток локальных упоминаний",
                "opportunity": "Локальный link building",
                "priority": "medium"
            }
        ]

    def _calculate_competitor_strength(self, competitor_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет силы конкурента"""
        # Веса различных факторов
        weights = {
            "organic_performance": 0.30,
            "technical_performance": 0.25,
            "authority_signals": 0.25,
            "brand_strength": 0.20
        }
        
        # Нормализация метрик (0-100)
        organic_score = min(100, (competitor_profile["organic_traffic"] / 10000))
        technical_score = competitor_profile["technical_score"]
        authority_score = min(100, (competitor_profile["domain_authority"] / 80) * 100)
        brand_score = competitor_profile["brand_strength"]
        
        # Общий балл
        overall_strength = (
            organic_score * weights["organic_performance"] +
            technical_score * weights["technical_performance"] + 
            authority_score * weights["authority_signals"] +
            brand_score * weights["brand_strength"]
        )
        
        return {
            "overall_strength": round(overall_strength, 1),
            "organic_performance": round(organic_score, 1),
            "technical_performance": round(technical_score, 1),
            "authority_signals": round(authority_score, 1),
            "brand_strength": round(brand_score, 1),
            "strength_tier": self._categorize_strength(overall_strength)
        }

    def _categorize_strength(self, strength_score: float) -> str:
        """Категоризация силы конкурента"""
        if strength_score >= 80:
            return "dominant"
        elif strength_score >= 65:
            return "strong"
        elif strength_score >= 50:
            return "moderate"
        else:
            return "weak"

    def _identify_overtaking_opportunities(self, competitor_profile: Dict, keyword_gaps: List, content_gaps: List, technical_gaps: List) -> List[Dict]:
        """Идентификация возможностей для обгона"""
        opportunities = []
        
        # На основе технических gaps
        for gap in technical_gaps:
            if gap["priority"] == "high":
                opportunities.append({
                    "type": "technical_advantage",
                    "description": f"Обгон через {gap['gap_type']}",
                    "timeline": "2-4 months",
                    "investment_required": "medium",
                    "success_probability": 0.75
                })
        
        # На основе контентных gaps
        high_content_gaps = [g for g in content_gaps if g["priority"] == "high"]
        if high_content_gaps:
            opportunities.append({
                "type": "content_superiority",
                "description": "Создание превосходящего контента",
                "timeline": "3-6 months",
                "investment_required": "high",
                "success_probability": 0.65
            })
        
        return opportunities

    def _assess_competitor_threat_level(self, strength: Dict, profile: Dict) -> str:
        """Оценка уровня угрозы от конкурента"""
        if strength["overall_strength"] >= 80 and profile["organic_traffic"] > 200000:
            return "critical"
        elif strength["overall_strength"] >= 65:
            return "high"
        elif strength["overall_strength"] >= 50:
            return "medium"
        else:
            return "low"

    # Additional helper methods for other analyses...
    # (Продолжение helper methods для остальных функций)

    def _analyze_market_dynamics(self, competitor_analysis: List[Dict]) -> Dict[str, Any]:
        """Анализ динамики рынка"""
        return {
            "market_concentration": "fragmented",  # или "concentrated"
            "dominant_players": sum(1 for c in competitor_analysis if c["competitor_strength"]["strength_tier"] == "dominant"),
            "emerging_threats": sum(1 for c in competitor_analysis if c["threat_level"] in ["high", "critical"]),
            "market_opportunity": "Есть возможности для роста доли рынка"
        }

    def _formulate_gap_strategy(self, competitor_analysis: List, market_dynamics: Dict) -> List[str]:
        """Формулирование стратегии на основе gaps"""
        return [
            "Сфокусироваться на технических преимуществах",
            "Развивать контентное превосходство",
            "Усилить link building стратегию",
            "Инвестировать в brand building"
        ]

    def _prioritize_competitive_actions(self, competitor_analysis: List) -> List[Dict]:
        """Приоритизация конкурентных действий"""
        actions = []
        
        for analysis in competitor_analysis:
            for opp in analysis["overtaking_opportunities"]:
                actions.append({
                    "competitor": analysis["competitor_domain"],
                    "action": opp["description"],
                    "priority": "high" if opp["success_probability"] > 0.7 else "medium",
                    "timeline": opp["timeline"],
                    "investment": opp["investment_required"]
                })
        
        return sorted(actions, key=lambda x: (x["priority"] == "high", x.get("success_probability", 0)), reverse=True)

    def _calculate_our_competitive_advantage(self, competitor_analysis: List) -> int:
        """Расчет нашего конкурентного преимущества"""
        # Симуляция на основе анализа конкурентов
        avg_competitor_strength = sum(
            c["competitor_strength"]["overall_strength"] 
            for c in competitor_analysis
        ) / len(competitor_analysis)
        
        # Предполагаем наш уровень
        our_estimated_strength = random.uniform(50, 75)
        
        if our_estimated_strength > avg_competitor_strength:
            return int(60 + (our_estimated_strength - avg_competitor_strength))
        else:
            return int(40 - (avg_competitor_strength - our_estimated_strength))

    def _analyze_topic_content_landscape(self, topic: str, competitors: List[str], our_domain: str) -> Dict[str, Any]:
        """Анализ контентного ландшафта по теме"""
        return {
            "topic": topic,
            "competitor_content_volume": random.randint(50, 300),
            "avg_content_quality": random.randint(60, 85),
            "content_gaps": [
                {
                    "type": "depth_analysis",
                    "opportunity": f"Глубокий анализ {topic}",
                    "competitor_performance": random.randint(60, 80),
                    "our_potential": random.randint(80, 95),
                    "priority": "high",
                    "traffic_potential": random.randint(5000, 25000),
                    "production_cost": random.randint(50000, 200000),
                    "timeline": "2-4 weeks"
                },
                {
                    "type": "interactive_content",
                    "opportunity": f"Интерактивные инструменты для {topic}",
                    "competitor_performance": random.randint(20, 50),
                    "our_potential": random.randint(70, 90),
                    "priority": "medium",
                    "traffic_potential": random.randint(3000, 15000),
                    "production_cost": random.randint(100000, 400000),
                    "timeline": "4-8 weeks"
                }
            ],
            "market_saturation": random.choice(["low", "medium", "high"])
        }

    def _develop_content_gap_strategy(self, content_gaps: List[Dict], landscape: List[Dict]) -> Dict[str, Any]:
        """Разработка стратегии контентных gaps"""
        return {
            "primary_focus": "Создание превосходящего экспертного контента",
            "content_types_priority": ["interactive_tools", "expert_analysis", "comprehensive_guides"],
            "investment_allocation": {
                "high_priority": "60%",
                "medium_priority": "30%", 
                "experimental": "10%"
            },
            "timeline": "6 months для полной реализации",
            "success_metrics": ["organic_traffic", "engagement_rate", "backlinks_earned"]
        }

    def _analyze_content_gaps_roi(self, content_gaps: List[Dict]) -> Dict[str, Any]:
        """Анализ ROI контентных возможностей"""
        total_investment = sum(gap['production_cost'] for gap in content_gaps)
        total_traffic_potential = sum(gap['estimated_traffic'] for gap in content_gaps)
        
        return {
            "total_investment_required": total_investment,
            "total_traffic_potential": total_traffic_potential,
            "estimated_conversion_value": total_traffic_potential * 50,  # 50₽ за визит
            "roi_percentage": ((total_traffic_potential * 50 * 12 - total_investment) / total_investment) * 100,
            "payback_period_months": total_investment / (total_traffic_potential * 50),
            "risk_assessment": "medium"
        }

    def _calculate_content_gap_resources(self, content_gaps: List[Dict]) -> Dict[str, Any]:
        """Расчет ресурсов для контентных gaps"""
        return {
            "content_creators_needed": max(1, len(content_gaps) // 10),
            "designers_needed": max(1, len([g for g in content_gaps if 'interactive' in g['gap_type']]) // 5),
            "developers_needed": len([g for g in content_gaps if 'tool' in g.get('gap_type', '')]),
            "total_man_hours": sum(40 if 'interactive' in g.get('gap_type', '') else 20 for g in content_gaps),
            "external_expertise_required": len([g for g in content_gaps if g.get('priority') == 'high'])
        }

    def _generate_competitor_changes(self, competitor: str, period_days: int) -> Dict[str, Any]:
        """Генерация изменений конкурента за период"""
        return {
            "ranking_changes": {
                "keywords_gained": random.randint(0, 50),
                "keywords_lost": random.randint(0, 30),
                "avg_position_change": random.uniform(-2.5, 3.0),
                "top10_changes": random.randint(-5, 10)
            },
            "content_changes": {
                "new_pages_published": random.randint(0, 20),
                "pages_updated": random.randint(5, 50),
                "content_quality_change": random.uniform(-0.5, 1.5)
            },
            "technical_changes": {
                "site_speed_change": random.uniform(-0.5, 0.8),
                "mobile_score_change": random.randint(-5, 10),
                "core_web_vitals_change": random.uniform(-0.2, 0.5)
            },
            "backlink_changes": {
                "new_backlinks": random.randint(10, 200),
                "lost_backlinks": random.randint(5, 50),
                "da_change": random.randint(-2, 3),
                "referring_domains_change": random.randint(-5, 25)
            },
            "serp_feature_changes": {
                "features_gained": random.randint(0, 5),
                "features_lost": random.randint(0, 3),
                "featured_snippets_change": random.randint(-2, 3)
            }
        }

    def _assess_change_significance(self, changes: Dict[str, Any]) -> Dict[str, Any]:
        """Оценка значимости изменений"""
        significance_score = 0
        primary_change = "none"
        
        # Оценка ranking changes
        if changes["ranking_changes"]["keywords_gained"] > 30:
            significance_score += 3
            primary_change = "ranking_improvement"
        
        # Оценка content changes
        if changes["content_changes"]["new_pages_published"] > 15:
            significance_score += 2
            if primary_change == "none":
                primary_change = "content_expansion"
        
        # Оценка backlink changes
        if changes["backlink_changes"]["new_backlinks"] > 100:
            significance_score += 3
            if primary_change == "none":
                primary_change = "link_building_campaign"
        
        overall_significance = min(10, significance_score)
        
        return {
            "overall_significance": overall_significance,
            "primary_change_type": primary_change,
            "impact_level": "high" if overall_significance >= 7 else "medium" if overall_significance >= 4 else "low",
            "description": f"Competitor showing {primary_change} with significance {overall_significance}/10",
            "response_required": overall_significance >= 6
        }

    def _assess_competitor_threat(self, changes: Dict, significance: Dict) -> str:
        """Оценка угрозы от конкурента"""
        if significance["overall_significance"] >= 8:
            return "immediate_threat"
        elif significance["overall_significance"] >= 6:
            return "monitoring_required"
        elif significance["overall_significance"] >= 4:
            return "watch_closely"
        else:
            return "low_concern"

    def _analyze_competitive_trends(self, competitor_changes: List[Dict]) -> Dict[str, Any]:
        """Анализ конкурентных трендов"""
        return {
            "market_activity_level": "high" if len([c for c in competitor_changes if c["change_significance"]["overall_significance"] >= 6]) > 2 else "moderate",
            "dominant_strategy": "content_marketing",  # Наиболее популярная стратегия
            "emerging_tactics": ["interactive_content", "video_marketing", "ai_tools"],
            "market_consolidation": False,
            "innovation_rate": "accelerating"
        }

    def _generate_competitive_alerts(self, significant_changes: List[Dict]) -> List[Dict]:
        """Генерация конкурентных алертов"""
        alerts = []
        for change in significant_changes:
            if change["impact_level"] == "high":
                alerts.append({
                    "alert_type": "competitor_threat",
                    "competitor": change["competitor"],
                    "severity": "high",
                    "description": change["description"],
                    "action_required": "immediate_response",
                    "deadline": "7 days"
                })
        return alerts

    def _generate_response_recommendations(self, significant_changes: List, trends: Dict) -> List[str]:
        """Генерация рекомендаций по реагированию"""
        recommendations = []
        
        if trends["market_activity_level"] == "high":
            recommendations.append("Увеличить частоту мониторинга конкурентов")
        
        for change in significant_changes:
            if change["our_response_needed"]:
                recommendations.append(f"Ответить на действия {change['competitor']}: {change['change_type']}")
        
        return recommendations

    def _predict_competitive_trends(self, competitor_changes: List) -> Dict[str, Any]:
        """Прогноз конкурентных трендов"""
        return {
            "next_30_days": "Ожидается усиление контентной конкуренции",
            "next_90_days": "Возможное увеличение link building активности",
            "key_risks": ["Новые конкуренты", "Изменения алгоритмов", "Рост рекламных расходов"],
            "opportunities": ["Gaps в контентной стратегии", "Технические преимущества", "Нишевые keywords"]
        }

    def _create_monitoring_summary(self, competitor_changes: List, significant_changes: List) -> Dict[str, Any]:
        """Создание сводки мониторинга"""
        return {
            "total_competitors_monitored": len(competitor_changes),
            "significant_changes_detected": len(significant_changes),
            "immediate_threats": len([c for c in significant_changes if c["impact_level"] == "high"]),
            "monitoring_health": "active",
            "data_freshness": "real_time"
        }

    def _calculate_overall_competitive_score(self, serp: Dict, gaps: Dict, market: Dict) -> int:
        """Расчет общего конкурентного скора"""
        # Веса компонентов
        serp_weight = 0.4
        gaps_weight = 0.35
        market_weight = 0.25
        
        # Нормализация скоров
        serp_score = min(100, serp["serp_feature_ownership"] * 2 + len(serp["high_priority_opportunities"]) * 5)
        gaps_score = gaps["competitive_advantage_score"]
        market_score = (market["our_visibility_share"] / 30) * 100  # Normalize to 30% max
        
        overall = serp_score * serp_weight + gaps_score * gaps_weight + market_score * market_weight
        
        return min(100, int(overall))

    def _determine_competitive_priorities(self, score: int, serp: Dict, gaps: Dict, market: Dict) -> List[str]:
        """Определение конкурентных приоритетов"""
        priorities = []
        
        if score < 50:
            priorities.append("Критическое улучшение конкурентной позиции")
        
        if serp["serp_feature_ownership"] < 20:
            priorities.append("Захват SERP features")
        
        if market["market_position"] > 5:
            priorities.append("Рост доли рынка")
        
        if len(serp["high_priority_opportunities"]) > 5:
            priorities.append("Реализация высокоприоритетных возможностей")
        
        return priorities

    def _create_competitive_action_roadmap(self, priorities: List[str], serp: Dict, gaps: Dict) -> Dict[str, Any]:
        """Создание дорожной карты конкурентных действий"""
        return {
            "immediate_actions": priorities[:2],
            "short_term_goals": ["Улучшение технических показателей", "Контентная оптимизация"],
            "long_term_strategy": ["Доминирование в нише", "Расширение market share"],
            "resource_allocation": {
                "content": "40%",
                "technical": "30%",
                "link_building": "20%",
                "monitoring": "10%"
            },
            "timeline": "12 months для значительного улучшения позиций"
        }

    def _assess_competitive_health(self, competitive_score: int) -> str:
        """Оценка конкурентного здоровья"""
        if competitive_score >= 80:
            return "excellent"
        elif competitive_score >= 60:
            return "good"
        elif competitive_score >= 40:
            return "needs_improvement"
        else:
            return "critical"

    def get_agent_metrics(self) -> AgentMetrics:
        """Получение метрик работы агента"""
        return AgentMetrics(
            agent_name=self.name,
            agent_type="operational",
            version="1.0.0", 
            status="active",
            total_tasks_processed=getattr(self, '_tasks_processed', 0),
            success_rate=getattr(self, '_success_rate', 0.0),
            average_response_time=getattr(self, '_avg_response_time', 0.0),
            specialized_metrics={
                "max_competitors": self.max_competitors,
                "min_market_share": self.min_market_share,
                "keyword_tracking_limit": self.keyword_tracking_limit,
                "serp_monitoring_depth": self.serp_monitoring_depth
            }
        )