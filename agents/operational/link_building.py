"""
🔗 Link Building Agent

Operational-level агент для стратегий наращивания ссылочной массы, outreach automation 
и анализа качества ссылок для улучшения позиций в поисковых системах.

Основные возможности:
- Link prospect identification & scoring
- Outreach automation & templates
- Link quality assessment
- Toxic link detection & disavow
- Competitor backlink analysis
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random

from core.base_agent import BaseAgent
from core.interfaces.data_models import AgentMetrics

logger = logging.getLogger(__name__)


class LinkBuildingAgent(BaseAgent):
    """
    🔗 Link Building Agent
    
    Operational-level агент для комплексного управления ссылочным профилем,
    автоматизации outreach кампаний и анализа качества ссылок.
    """
    
    def __init__(self, data_provider=None, **kwargs):
        super().__init__(
            agent_id="link_building_agent", 
            name="Link Building Agent",
            data_provider=data_provider,
            **kwargs
        )
        
        # Конфигурация Link Building
        self.min_da_threshold = 30  # Минимальный Domain Authority
        self.max_spam_score = 15    # Максимальный spam score
        self.min_relevance_score = 70  # Минимальная релевантность %
        self.target_monthly_links = 25  # Целевое количество ссылок в месяц
        
        # Quality scoring weights
        self.quality_factors = {
            "domain_authority": {"weight": 0.25, "min_threshold": 30},
            "page_authority": {"weight": 0.20, "min_threshold": 25},
            "traffic_volume": {"weight": 0.15, "min_threshold": 5000},
            "content_relevance": {"weight": 0.15, "min_threshold": 70},
            "spam_score": {"weight": 0.10, "max_threshold": 15},
            "trust_flow": {"weight": 0.10, "min_threshold": 20},
            "citation_flow": {"weight": 0.05, "min_threshold": 15}
        }
        
        # Outreach strategies
        self.outreach_strategies = {
            "guest_posting": {"success_rate": 0.20, "avg_da": 50, "cost": 25000},
            "resource_page": {"success_rate": 0.25, "avg_da": 45, "cost": 14000},
            "broken_link_building": {"success_rate": 0.125, "avg_da": 55, "cost": 20000},
            "skyscraper_technique": {"success_rate": 0.10, "avg_da": 60, "cost": 42500},
            "haro_pr": {"success_rate": 0.075, "avg_da": 70, "cost": 7500},
            "digital_pr": {"success_rate": 0.15, "avg_da": 65, "cost": 50000}
        }
        
        logger.info(f"✅ {self.name} инициализирован:")
        logger.info(f"   🎯 Min DA Threshold: {self.min_da_threshold}")
        logger.info(f"   🚫 Max Spam Score: {self.max_spam_score}")
        logger.info(f"   📊 Min Relevance: {self.min_relevance_score}%")
        logger.info(f"   🔗 Monthly Target: {self.target_monthly_links} links")

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка задач Link Building Agent
        
        Поддерживаемые типы задач:
        - link_prospect_analysis: Анализ и скоринг потенциальных доноров
        - outreach_campaign_planning: Планирование outreach кампании
        - link_quality_audit: Аудит качества существующих ссылок
        - toxic_link_detection: Выявление токсичных ссылок
        - competitor_backlink_analysis: Анализ ссылочного профиля конкурентов
        """
        task_type = task_data.get('task_type', 'link_prospect_analysis')
        
        try:
            if task_type == 'link_prospect_analysis':
                return await self._analyze_link_prospects(task_data)
            elif task_type == 'outreach_campaign_planning':
                return await self._plan_outreach_campaign(task_data)
            elif task_type == 'link_quality_audit':
                return await self._audit_link_quality(task_data)
            elif task_type == 'toxic_link_detection':
                return await self._detect_toxic_links(task_data)
            elif task_type == 'competitor_backlink_analysis':
                return await self._analyze_competitor_backlinks(task_data)
            else:
                # Default: комплексный анализ ссылочного профиля
                return await self._comprehensive_link_analysis(task_data)
                
        except Exception as e:
            logger.error(f"❌ Ошибка в Link Building Agent: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

    async def _analyze_link_prospects(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ и скоринг потенциальных доноров ссылок"""
        domain_data = task_data.get('domain_data', {})
        domain = domain_data.get('domain', 'example.com')
        industry = domain_data.get('industry', 'general')
        
        # Симуляция найденных prospects
        num_prospects = random.randint(50, 200)
        prospects = []
        
        for i in range(min(num_prospects, 20)):  # Показываем топ-20
            prospect = self._generate_prospect_data(industry)
            quality_score = self._calculate_prospect_quality_score(prospect)
            
            prospects.append({
                "domain": f"prospect-{i+1}.{random.choice(['com', 'ru', 'org', 'net'])}",
                "da": prospect["da"],
                "pa": prospect["pa"],
                "spam_score": prospect["spam_score"],
                "traffic": prospect["traffic"],
                "relevance": prospect["relevance"],
                "trust_flow": prospect["trust_flow"],
                "quality_score": quality_score,
                "outreach_strategy": self._recommend_outreach_strategy(prospect),
                "estimated_cost": self._estimate_link_cost(quality_score),
                "success_probability": self._calculate_success_probability(prospect)
            })
        
        # Сортировка по quality score
        prospects = sorted(prospects, key=lambda x: x['quality_score'], reverse=True)
        
        # Категоризация prospects
        premium_prospects = [p for p in prospects if p['quality_score'] >= 80]
        high_quality = [p for p in prospects if 60 <= p['quality_score'] < 80]
        medium_quality = [p for p in prospects if 40 <= p['quality_score'] < 60]
        low_quality = [p for p in prospects if p['quality_score'] < 40]
        
        # Рекомендации по стратегии
        strategy_recommendations = self._get_prospect_strategy_recommendations(
            len(premium_prospects), len(high_quality), len(medium_quality)
        )
        
        logger.info(f"🔍 Link Prospect Analysis для {domain}:")
        logger.info(f"   📊 Total Prospects: {num_prospects}")
        logger.info(f"   💎 Premium Quality: {len(premium_prospects)}")
        logger.info(f"   🎯 High Quality: {len(high_quality)}")
        logger.info(f"   📈 Medium Quality: {len(medium_quality)}")
        
        return {
            "success": True,
            "domain": domain,
            "total_prospects_found": num_prospects,
            "prospects_analyzed": len(prospects),
            "quality_distribution": {
                "premium": len(premium_prospects),
                "high": len(high_quality),
                "medium": len(medium_quality),
                "low": len(low_quality)
            },
            "top_prospects": prospects[:10],
            "strategy_recommendations": strategy_recommendations,
            "estimated_monthly_capacity": self._calculate_monthly_capacity(prospects),
            "agent": self.name,
            "confidence": round(random.uniform(0.75, 0.90), 2)
        }

    async def _plan_outreach_campaign(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Планирование outreach кампании"""
        campaign_data = task_data.get('campaign_data', {})
        budget = campaign_data.get('monthly_budget', random.randint(200000, 1000000))
        target_links = campaign_data.get('target_links', self.target_monthly_links)
        industry = campaign_data.get('industry', 'general')
        
        # Распределение бюджета по стратегиям
        budget_allocation = self._allocate_outreach_budget(budget)
        
        # Планирование кампаний по каждой стратегии
        campaign_strategies = []
        total_expected_links = 0
        total_outreach_volume = 0
        
        for strategy, allocation in budget_allocation.items():
            strategy_config = self.outreach_strategies[strategy]
            strategy_budget = budget * allocation
            
            expected_links = strategy_budget / strategy_config["cost"]
            outreach_needed = expected_links / strategy_config["success_rate"]
            
            campaign_strategies.append({
                "strategy": strategy,
                "budget_allocation": allocation,
                "budget_amount": int(strategy_budget),
                "expected_links": int(expected_links),
                "outreach_volume": int(outreach_needed),
                "avg_da": strategy_config["avg_da"],
                "success_rate": strategy_config["success_rate"],
                "timeline": self._get_strategy_timeline(strategy)
            })
            
            total_expected_links += expected_links
            total_outreach_volume += outreach_needed
        
        # Timeline planning
        campaign_timeline = self._create_campaign_timeline(campaign_strategies)
        
        # Resource requirements
        resource_requirements = self._calculate_resource_requirements(
            total_outreach_volume, total_expected_links
        )
        
        # Risk assessment
        risk_factors = self._assess_campaign_risks(campaign_strategies, budget)
        
        logger.info(f"📋 Outreach Campaign Planning:")
        logger.info(f"   💰 Budget: {budget:,} ₽/мес")
        logger.info(f"   🎯 Target Links: {target_links}")
        logger.info(f"   📊 Expected Links: {int(total_expected_links)}")
        logger.info(f"   📧 Outreach Volume: {int(total_outreach_volume)}")
        
        return {
            "success": True,
            "campaign_budget": budget,
            "target_links": target_links,
            "expected_links": int(total_expected_links),
            "total_outreach_volume": int(total_outreach_volume),
            "budget_allocation": budget_allocation,
            "campaign_strategies": campaign_strategies,
            "timeline": campaign_timeline,
            "resource_requirements": resource_requirements,
            "risk_factors": risk_factors,
            "success_probability": self._calculate_campaign_success_probability(campaign_strategies),
            "agent": self.name,
            "confidence": round(random.uniform(0.70, 0.85), 2)
        }

    async def _audit_link_quality(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Аудит качества существующих ссылок"""
        domain_data = task_data.get('domain_data', {})
        domain = domain_data.get('domain', 'example.com')
        
        # Симуляция существующего ссылочного профиля
        total_backlinks = random.randint(500, 5000)
        referring_domains = random.randint(100, 800)
        
        # Генерация анализа ссылок
        link_analysis = []
        quality_distribution = {"premium": 0, "high": 0, "medium": 0, "low": 0, "toxic": 0}
        
        for i in range(min(referring_domains, 50)):  # Анализируем топ-50 доменов
            link_data = self._generate_existing_link_data()
            quality_score = self._calculate_link_quality_score(link_data)
            
            if quality_score >= 80:
                quality_tier = "premium"
            elif quality_score >= 60:
                quality_tier = "high"
            elif quality_score >= 40:
                quality_tier = "medium"
            elif quality_score >= 20:
                quality_tier = "low"
            else:
                quality_tier = "toxic"
            
            quality_distribution[quality_tier] += 1
            
            link_analysis.append({
                "referring_domain": f"backlink-{i+1}.{random.choice(['com', 'ru', 'org', 'net'])}",
                "da": link_data["da"],
                "pa": link_data["pa"],
                "spam_score": link_data["spam_score"],
                "trust_flow": link_data["trust_flow"],
                "quality_score": quality_score,
                "quality_tier": quality_tier,
                "link_count": random.randint(1, 5),
                "anchor_text_quality": random.choice(["good", "over-optimized", "natural"]),
                "link_placement": random.choice(["editorial", "footer", "sidebar", "author_bio"]),
                "nofollow": random.choice([True, False])
            })
        
        # Сортировка по quality score
        link_analysis = sorted(link_analysis, key=lambda x: x['quality_score'], reverse=True)
        
        # Общие метрики профиля
        avg_da = sum(link['da'] for link in link_analysis) / len(link_analysis)
        avg_quality_score = sum(link['quality_score'] for link in link_analysis) / len(link_analysis)
        
        # Toxic links для disavow
        toxic_links = [link for link in link_analysis if link['quality_tier'] == 'toxic']
        
        # Health assessment
        link_profile_health = self._assess_link_profile_health(quality_distribution, avg_quality_score)
        
        # Рекомендации по улучшению
        improvement_recommendations = self._get_link_profile_recommendations(
            quality_distribution, toxic_links, avg_quality_score
        )
        
        logger.info(f"🔗 Link Quality Audit для {domain}:")
        logger.info(f"   📊 Total Backlinks: {total_backlinks:,}")
        logger.info(f"   🌐 Referring Domains: {referring_domains}")
        logger.info(f"   📈 Avg DA: {avg_da:.1f}")
        logger.info(f"   💎 Avg Quality Score: {avg_quality_score:.1f}")
        logger.info(f"   🚨 Toxic Links: {len(toxic_links)}")
        
        return {
            "success": True,
            "domain": domain,
            "total_backlinks": total_backlinks,
            "referring_domains": referring_domains,
            "avg_da": round(avg_da, 1),
            "avg_quality_score": round(avg_quality_score, 1),
            "quality_distribution": quality_distribution,
            "link_profile_health": link_profile_health,
            "top_quality_links": link_analysis[:10],
            "toxic_links_count": len(toxic_links),
            "toxic_links": toxic_links[:5] if toxic_links else [],
            "improvement_recommendations": improvement_recommendations,
            "disavow_required": len(toxic_links) > 0,
            "agent": self.name,
            "confidence": round(random.uniform(0.80, 0.95), 2)
        }

    async def _detect_toxic_links(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Выявление токсичных ссылок для disavow"""
        domain_data = task_data.get('domain_data', {})
        domain = domain_data.get('domain', 'example.com')
        
        # Симуляция анализа токсичных ссылок
        total_links_analyzed = random.randint(1000, 8000)
        
        # Различные типы токсичных ссылок
        toxic_categories = {
            "spam_domains": {"count": random.randint(5, 25), "severity": "high"},
            "pbn_networks": {"count": random.randint(2, 15), "severity": "critical"},
            "adult_content": {"count": random.randint(0, 8), "severity": "high"},
            "malware_sites": {"count": random.randint(0, 5), "severity": "critical"},
            "link_farms": {"count": random.randint(3, 20), "severity": "high"},
            "irrelevant_links": {"count": random.randint(10, 50), "severity": "medium"},
            "over_optimization": {"count": random.randint(5, 30), "severity": "medium"}
        }
        
        # Подробные токсичные ссылки
        toxic_links = []
        total_toxic = 0
        
        for category, data in toxic_categories.items():
            total_toxic += data["count"]
            for i in range(min(data["count"], 3)):  # Показываем по 3 примера
                toxic_links.append({
                    "referring_domain": f"toxic-{category}-{i+1}.{random.choice(['com', 'ru', 'biz'])}",
                    "category": category,
                    "severity": data["severity"],
                    "spam_score": random.randint(60, 95),
                    "da": random.randint(1, 20),
                    "toxic_signals": self._get_toxic_signals(category),
                    "link_count": random.randint(1, 10),
                    "discovery_date": datetime.now() - timedelta(days=random.randint(1, 180)),
                    "disavow_priority": "immediate" if data["severity"] == "critical" else "next_cycle"
                })
        
        # Сортировка по приоритету
        priority_order = {"critical": 0, "high": 1, "medium": 2}
        toxic_links = sorted(toxic_links, key=lambda x: priority_order[x['severity']])
        
        # Создание disavow файла
        disavow_file_content = self._generate_disavow_file(toxic_links)
        
        # Risk assessment
        penalty_risk = self._assess_penalty_risk(toxic_categories, total_toxic)
        
        # Action plan
        cleanup_action_plan = self._create_cleanup_action_plan(toxic_categories, penalty_risk)
        
        logger.info(f"🚨 Toxic Link Detection для {domain}:")
        logger.info(f"   📊 Links Analyzed: {total_links_analyzed:,}")
        logger.info(f"   ☠️ Toxic Links Found: {total_toxic}")
        logger.info(f"   🔥 Critical Issues: {sum(1 for cat in toxic_categories.values() if cat['severity'] == 'critical')}")
        logger.info(f"   📈 Penalty Risk: {penalty_risk}")
        
        return {
            "success": True,
            "domain": domain,
            "total_links_analyzed": total_links_analyzed,
            "total_toxic_links": total_toxic,
            "toxic_categories": toxic_categories,
            "toxic_links_sample": toxic_links[:15],
            "penalty_risk": penalty_risk,
            "disavow_file_content": disavow_file_content,
            "cleanup_action_plan": cleanup_action_plan,
            "immediate_action_required": penalty_risk in ["high", "critical"],
            "estimated_cleanup_time": f"{random.randint(2, 8)} weeks",
            "agent": self.name,
            "confidence": round(random.uniform(0.85, 0.95), 2)
        }

    async def _analyze_competitor_backlinks(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ ссылочного профиля конкурентов"""
        competitor_data = task_data.get('competitor_data', {})
        competitors = competitor_data.get('competitors', ['competitor1.com', 'competitor2.com'])
        our_domain = competitor_data.get('our_domain', 'example.com')
        
        # Анализ каждого конкурента
        competitor_analysis = []
        all_competitor_links = []
        
        for competitor in competitors[:3]:  # Анализируем до 3 конкурентов
            comp_links = random.randint(800, 4000)
            comp_domains = random.randint(150, 900)
            comp_avg_da = random.randint(35, 70)
            
            # Топ ссылки конкурента
            top_links = []
            for i in range(10):
                link = {
                    "referring_domain": f"comp-{competitor.replace('.', '-')}-link-{i+1}.com",
                    "da": random.randint(40, 85),
                    "pa": random.randint(35, 75),
                    "trust_flow": random.randint(25, 65),
                    "spam_score": random.randint(1, 25),
                    "traffic": random.randint(10000, 500000),
                    "obtainability": random.choice(["easy", "medium", "hard", "impossible"]),
                    "relevance": random.randint(60, 95)
                }
                top_links.append(link)
                all_competitor_links.append(link)
            
            competitor_analysis.append({
                "domain": competitor,
                "total_backlinks": comp_links,
                "referring_domains": comp_domains,
                "avg_da": comp_avg_da,
                "domain_authority": random.randint(45, 80),
                "top_referring_domains": top_links,
                "link_building_velocity": random.randint(20, 100),  # links per month
                "content_strategy": random.choice(["guest_posts", "pr_heavy", "resource_focused", "skyscraper"])
            })
        
        # Gap analysis - ссылки, которые есть у конкурентов, но нет у нас
        link_gap_opportunities = self._identify_link_gaps(all_competitor_links, our_domain)
        
        # Content gaps - контент, который привлекает ссылки у конкурентов
        content_gaps = self._identify_content_gaps(competitors)
        
        # Strategy insights
        strategy_insights = self._extract_strategy_insights(competitor_analysis)
        
        # Actionable recommendations
        action_recommendations = self._create_competitor_action_plan(
            link_gap_opportunities, content_gaps, strategy_insights
        )
        
        logger.info(f"🎯 Competitor Backlink Analysis:")
        logger.info(f"   🏢 Competitors Analyzed: {len(competitors)}")
        logger.info(f"   🔗 Gap Opportunities: {len(link_gap_opportunities)}")
        logger.info(f"   📄 Content Gaps: {len(content_gaps)}")
        logger.info(f"   💡 Strategy Insights: {len(strategy_insights)}")
        
        return {
            "success": True,
            "our_domain": our_domain,
            "competitors_analyzed": len(competitors),
            "competitor_analysis": competitor_analysis,
            "link_gap_opportunities": link_gap_opportunities[:20],
            "content_gaps": content_gaps,
            "strategy_insights": strategy_insights,
            "action_recommendations": action_recommendations,
            "competitive_advantage_score": self._calculate_competitive_advantage(competitor_analysis),
            "priority_targets": [opp for opp in link_gap_opportunities if opp["priority"] == "high"][:10],
            "agent": self.name,
            "confidence": round(random.uniform(0.75, 0.90), 2)
        }

    async def _comprehensive_link_analysis(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Комплексный анализ ссылочного профиля (по умолчанию)"""
        domain_data = task_data.get('input_data', task_data.get('domain_data', {}))
        domain = domain_data.get('domain', 'example.com')
        industry = domain_data.get('industry', 'general')
        
        # Запуск ключевых анализов
        prospect_analysis = await self._analyze_link_prospects({'domain_data': domain_data})
        quality_audit = await self._audit_link_quality({'domain_data': domain_data})
        toxic_detection = await self._detect_toxic_links({'domain_data': domain_data})
        
        # Общая оценка ссылочного профиля
        link_profile_score = self._calculate_overall_link_score(
            quality_audit, toxic_detection, prospect_analysis
        )
        
        # Стратегические рекомендации
        strategic_priorities = self._get_link_building_priorities(
            link_profile_score, quality_audit, toxic_detection, prospect_analysis
        )
        
        # Budget recommendations
        recommended_budget = self._recommend_link_building_budget(
            link_profile_score, prospect_analysis['total_prospects_found']
        )
        
        logger.info(f"🔗 Comprehensive Link Analysis для {domain}:")
        logger.info(f"   📊 Link Profile Score: {link_profile_score}/100")
        logger.info(f"   🎯 Prospects Available: {prospect_analysis['total_prospects_found']}")
        logger.info(f"   💰 Recommended Budget: {recommended_budget:,} ₽/мес")
        
        return {
            "success": True,
            "domain": domain,
            "link_profile_score": link_profile_score,
            "current_link_health": quality_audit["link_profile_health"],
            "prospect_opportunities": {
                "total_prospects": prospect_analysis["total_prospects_found"],
                "quality_distribution": prospect_analysis["quality_distribution"]
            },
            "toxic_link_issues": {
                "total_toxic": toxic_detection["total_toxic_links"],
                "penalty_risk": toxic_detection["penalty_risk"],
                "cleanup_required": toxic_detection["immediate_action_required"]
            },
            "strategic_priorities": strategic_priorities,
            "recommended_monthly_budget": recommended_budget,
            "expected_monthly_links": self._calculate_expected_links(recommended_budget),
            "timeline_to_improvement": f"{random.randint(3, 8)} months",
            "agent": self.name,
            "confidence": round(random.uniform(0.80, 0.92), 2)
        }

    # Helper methods

    def _generate_prospect_data(self, industry: str) -> Dict[str, Any]:
        """Генерация данных prospect'а"""
        return {
            "da": random.randint(25, 85),
            "pa": random.randint(20, 75),
            "spam_score": random.randint(1, 30),
            "traffic": random.randint(3000, 200000),
            "relevance": random.randint(50, 95),
            "trust_flow": random.randint(15, 70),
            "citation_flow": random.randint(10, 65)
        }

    def _calculate_prospect_quality_score(self, prospect: Dict[str, Any]) -> int:
        """Расчет quality score для prospect'а"""
        score = 0
        
        # Domain Authority (25%)
        da_score = min(100, (prospect["da"] / 80) * 100)
        score += da_score * 0.25
        
        # Page Authority (20%)
        pa_score = min(100, (prospect["pa"] / 70) * 100)
        score += pa_score * 0.20
        
        # Traffic Volume (15%)
        traffic_score = min(100, (prospect["traffic"] / 100000) * 100)
        score += traffic_score * 0.15
        
        # Content Relevance (15%)
        score += prospect["relevance"] * 0.15
        
        # Spam Score (10% - инвертированный)
        spam_penalty = max(0, (30 - prospect["spam_score"]) / 30 * 100)
        score += spam_penalty * 0.10
        
        # Trust Flow (10%)
        tf_score = min(100, (prospect["trust_flow"] / 60) * 100)
        score += tf_score * 0.10
        
        # Citation Flow (5%)
        cf_score = min(100, (prospect["citation_flow"] / 55) * 100)
        score += cf_score * 0.05
        
        return min(100, int(score))

    def _recommend_outreach_strategy(self, prospect: Dict[str, Any]) -> str:
        """Рекомендация стратегии outreach для prospect'а"""
        if prospect["da"] >= 70 and prospect["traffic"] >= 50000:
            return "digital_pr"
        elif prospect["da"] >= 50 and prospect["relevance"] >= 80:
            return "guest_posting"
        elif prospect["da"] >= 40:
            return "resource_page"
        elif prospect["relevance"] >= 85:
            return "broken_link_building"
        else:
            return "skyscraper_technique"

    def _estimate_link_cost(self, quality_score: int) -> int:
        """Оценка стоимости получения ссылки"""
        if quality_score >= 80:
            return random.randint(40000, 100000)
        elif quality_score >= 60:
            return random.randint(20000, 40000)
        elif quality_score >= 40:
            return random.randint(8000, 20000)
        else:
            return random.randint(3000, 8000)

    def _calculate_success_probability(self, prospect: Dict[str, Any]) -> float:
        """Расчет вероятности успеха outreach"""
        base_rate = 0.15  # 15% базовая вероятность
        
        # Бонусы
        if prospect["relevance"] >= 85:
            base_rate += 0.10
        if prospect["da"] < 50:
            base_rate += 0.05  # Менее авторитетные сайты более доступны
        if prospect["spam_score"] < 10:
            base_rate += 0.05
        
        # Штрафы
        if prospect["da"] >= 70:
            base_rate -= 0.05  # Высокоавторитетные сайты менее доступны
        if prospect["spam_score"] > 20:
            base_rate -= 0.10
        
        return round(max(0.05, min(0.35, base_rate)), 2)

    def _get_prospect_strategy_recommendations(self, premium: int, high: int, medium: int) -> List[str]:
        """Рекомендации по стратегии на основе качества prospects"""
        recommendations = []
        
        if premium >= 5:
            recommendations.append("Focus on premium prospects with digital PR approach")
        if high >= 10:
            recommendations.append("Strong guest posting opportunities available")
        if medium >= 15:
            recommendations.append("Scale with resource page and broken link building")
        if premium + high < 8:
            recommendations.append("Consider content creation to attract higher-quality prospects")
        
        return recommendations

    def _calculate_monthly_capacity(self, prospects: List[Dict]) -> Dict[str, int]:
        """Расчет месячной capacity по качеству prospects"""
        premium = len([p for p in prospects if p['quality_score'] >= 80])
        high = len([p for p in prospects if 60 <= p['quality_score'] < 80])
        medium = len([p for p in prospects if 40 <= p['quality_score'] < 60])
        
        return {
            "premium_links": min(premium, 5),    # Максимум 5 премиум ссылок в месяц
            "high_quality_links": min(high, 15), # Максимум 15 высококачественных
            "medium_quality_links": min(medium, 30), # Максимум 30 средних
            "total_realistic_capacity": min(premium, 5) + min(high, 15) + min(medium, 30)
        }

    def _allocate_outreach_budget(self, budget: int) -> Dict[str, float]:
        """Распределение бюджета по стратегиям outreach"""
        if budget >= 800000:  # Большой бюджет
            return {
                "digital_pr": 0.35,
                "guest_posting": 0.30,
                "skyscraper_technique": 0.20,
                "resource_page": 0.10,
                "haro_pr": 0.05
            }
        elif budget >= 400000:  # Средний бюджет
            return {
                "guest_posting": 0.40,
                "resource_page": 0.25,
                "digital_pr": 0.20,
                "broken_link_building": 0.15
            }
        else:  # Небольшой бюджет
            return {
                "resource_page": 0.40,
                "guest_posting": 0.30,
                "broken_link_building": 0.20,
                "haro_pr": 0.10
            }

    def _get_strategy_timeline(self, strategy: str) -> str:
        """Получение timeline для стратегии"""
        timelines = {
            "guest_posting": "4-8 weeks",
            "resource_page": "2-4 weeks", 
            "broken_link_building": "3-6 weeks",
            "skyscraper_technique": "8-12 weeks",
            "haro_pr": "2-8 weeks",
            "digital_pr": "4-10 weeks"
        }
        return timelines.get(strategy, "4-6 weeks")

    def _create_campaign_timeline(self, strategies: List[Dict]) -> Dict[str, Any]:
        """Создание timeline кампании"""
        return {
            "week_1_2": "Prospect research and qualification",
            "week_3_4": "Outreach template creation and initial campaigns",
            "week_5_8": "Full outreach execution and follow-ups",
            "week_9_12": "Link placement and monitoring",
            "ongoing": "Relationship nurturing and maintenance"
        }

    def _calculate_resource_requirements(self, outreach_volume: float, expected_links: float) -> Dict[str, Any]:
        """Расчет требований к ресурсам"""
        return {
            "outreach_specialist_hours": int(outreach_volume * 0.5),  # 30 мин на письмо
            "content_creation_hours": int(expected_links * 4),        # 4 часа на контент
            "relationship_management_hours": int(expected_links * 2), # 2 часа на поддержание
            "tools_required": ["Ahrefs", "Pitchbox", "Hunter.io", "BuzzStream"],
            "team_size_recommended": max(1, int(outreach_volume / 200))  # 1 человек на 200 писем
        }

    def _assess_campaign_risks(self, strategies: List[Dict], budget: int) -> List[str]:
        """Оценка рисков кампании"""
        risks = []
        
        if budget < 300000:
            risks.append("Limited budget may restrict high-quality opportunities")
        
        total_outreach = sum(s["outreach_volume"] for s in strategies)
        if total_outreach > 500:
            risks.append("High outreach volume may impact personalization quality")
        
        if any(s["success_rate"] < 0.10 for s in strategies):
            risks.append("Some strategies have low success rates")
        
        return risks

    def _calculate_campaign_success_probability(self, strategies: List[Dict]) -> float:
        """Расчет вероятности успеха кампании"""
        weighted_success = sum(
            s["success_rate"] * s["budget_allocation"] 
            for s in strategies
        )
        return round(weighted_success, 2)

    # Additional helper methods for other functions would continue here...
    # (Продолжение методов для audit_link_quality, detect_toxic_links, etc.)

    def _generate_existing_link_data(self) -> Dict[str, Any]:
        """Генерация данных существующей ссылки"""
        return {
            "da": random.randint(15, 80),
            "pa": random.randint(10, 70),
            "spam_score": random.randint(1, 50),
            "trust_flow": random.randint(5, 65),
            "citation_flow": random.randint(5, 60)
        }

    def _calculate_link_quality_score(self, link_data: Dict[str, Any]) -> int:
        """Расчет quality score для существующей ссылки"""
        return self._calculate_prospect_quality_score(link_data)

    def _assess_link_profile_health(self, quality_dist: Dict, avg_score: float) -> str:
        """Оценка здоровья ссылочного профиля"""
        if avg_score >= 70 and quality_dist.get("toxic", 0) == 0:
            return "excellent"
        elif avg_score >= 50 and quality_dist.get("toxic", 0) <= 5:
            return "good"
        elif avg_score >= 35:
            return "needs_improvement"
        else:
            return "poor"

    def _get_link_profile_recommendations(self, quality_dist: Dict, toxic_links: List, avg_score: float) -> List[str]:
        """Рекомендации по улучшению ссылочного профиля"""
        recommendations = []
        
        if toxic_links:
            recommendations.append(f"Immediate disavow of {len(toxic_links)} toxic links required")
        
        if quality_dist.get("premium", 0) < 10:
            recommendations.append("Focus on acquiring high-authority premium links")
        
        if avg_score < 50:
            recommendations.append("Overall link quality improvement needed")
        
        return recommendations

    def _get_toxic_signals(self, category: str) -> List[str]:
        """Получение сигналов токсичности по категории"""
        signals_map = {
            "spam_domains": ["High spam score", "Low DA", "Excessive outbound links"],
            "pbn_networks": ["PBN footprints", "Similar IP ranges", "Thin content"],
            "adult_content": ["Adult keywords", "Inappropriate content"],
            "malware_sites": ["Security warnings", "Malicious code detected"],
            "link_farms": ["Link exchange schemes", "Reciprocal linking"],
            "irrelevant_links": ["Topic mismatch", "Geographic irrelevance"],
            "over_optimization": ["Exact match anchors", "Keyword stuffing"]
        }
        return signals_map.get(category, ["Suspicious patterns detected"])

    def _generate_disavow_file(self, toxic_links: List[Dict]) -> str:
        """Генерация содержимого disavow файла"""
        content = "# Disavow file generated by AI SEO Architects\n"
        content += f"# Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        for link in toxic_links:
            content += f"domain:{link['referring_domain']}\n"
        
        return content

    def _assess_penalty_risk(self, toxic_categories: Dict, total_toxic: int) -> str:
        """Оценка риска получения пенальти"""
        critical_count = sum(
            data["count"] for data in toxic_categories.values() 
            if data["severity"] == "critical"
        )
        
        if critical_count > 10 or total_toxic > 100:
            return "critical"
        elif critical_count > 5 or total_toxic > 50:
            return "high"
        elif total_toxic > 20:
            return "medium"
        else:
            return "low"

    def _create_cleanup_action_plan(self, toxic_categories: Dict, penalty_risk: str) -> Dict[str, Any]:
        """Создание плана очистки ссылочного профиля"""
        if penalty_risk == "critical":
            return {
                "timeline": "Immediate (1-2 weeks)",
                "actions": ["Emergency disavow submission", "Manual link removal requests", "Google reconsideration"],
                "priority": "critical",
                "estimated_cost": "100,000-300,000 ₽"
            }
        elif penalty_risk == "high":
            return {
                "timeline": "Urgent (2-4 weeks)",
                "actions": ["Comprehensive disavow file", "Outreach for link removal", "Profile monitoring"],
                "priority": "high", 
                "estimated_cost": "50,000-150,000 ₽"
            }
        else:
            return {
                "timeline": "Standard (4-8 weeks)",
                "actions": ["Regular disavow update", "Gradual cleanup", "Quality improvement focus"],
                "priority": "medium",
                "estimated_cost": "20,000-75,000 ₽"
            }

    def _identify_link_gaps(self, competitor_links: List[Dict], our_domain: str) -> List[Dict]:
        """Идентификация gap opportunities в ссылках"""
        gaps = []
        for link in competitor_links:
            if link["obtainability"] in ["easy", "medium"]:
                gaps.append({
                    "domain": link["referring_domain"],
                    "da": link["da"],
                    "relevance": link["relevance"],
                    "obtainability": link["obtainability"],
                    "priority": "high" if link["da"] > 60 and link["obtainability"] == "easy" else "medium",
                    "estimated_cost": self._estimate_link_cost(link["da"]),
                    "strategy": self._recommend_outreach_strategy(link)
                })
        return sorted(gaps, key=lambda x: x["da"], reverse=True)

    def _identify_content_gaps(self, competitors: List[str]) -> List[Dict]:
        """Идентификация контентных gap'ов"""
        return [
            {
                "content_type": "Industry Report 2025",
                "competitor_links": random.randint(50, 200),
                "our_opportunity": "Create comprehensive industry analysis",
                "estimated_links": random.randint(80, 300),
                "production_cost": random.randint(300000, 800000)
            },
            {
                "content_type": "Interactive Calculator",
                "competitor_links": random.randint(30, 150),
                "our_opportunity": "Develop specialized tool for industry",
                "estimated_links": random.randint(60, 250),
                "production_cost": random.randint(500000, 1200000)
            }
        ]

    def _extract_strategy_insights(self, competitor_analysis: List[Dict]) -> List[str]:
        """Извлечение стратегических инсайтов"""
        return [
            "Competitors focus heavily on guest posting strategy",
            "High-authority news sites are common targets",
            "Resource pages in industry are underutilized",
            "Digital PR campaigns show strong results"
        ]

    def _create_competitor_action_plan(self, gaps: List, content_gaps: List, insights: List) -> List[str]:
        """Создание плана действий на основе конкурентного анализа"""
        return [
            f"Target {len([g for g in gaps if g['priority'] == 'high'])} high-priority gap opportunities",
            f"Develop {len(content_gaps)} linkable content assets",
            "Implement competitor monitoring system",
            "Execute strategic outreach to identified prospects"
        ]

    def _calculate_competitive_advantage(self, competitor_analysis: List[Dict]) -> int:
        """Расчет конкурентного преимущества"""
        our_estimated_da = random.randint(35, 65)
        avg_competitor_da = sum(c["domain_authority"] for c in competitor_analysis) / len(competitor_analysis)
        
        if our_estimated_da > avg_competitor_da:
            return random.randint(60, 85)
        else:
            return random.randint(25, 55)

    def _calculate_overall_link_score(self, quality_audit: Dict, toxic_detection: Dict, prospect_analysis: Dict) -> int:
        """Расчет общего скора ссылочного профиля"""
        quality_score = quality_audit["avg_quality_score"]
        toxic_penalty = min(30, toxic_detection["total_toxic_links"] * 0.5)
        prospect_bonus = min(20, prospect_analysis["quality_distribution"]["premium"] * 2)
        
        return max(0, min(100, int(quality_score - toxic_penalty + prospect_bonus)))

    def _get_link_building_priorities(self, profile_score: int, quality_audit: Dict, toxic_detection: Dict, prospect_analysis: Dict) -> List[str]:
        """Определение приоритетов link building"""
        priorities = []
        
        if toxic_detection["immediate_action_required"]:
            priorities.append("Priority 1: Immediate toxic link cleanup")
        
        if profile_score < 50:
            priorities.append("Priority 2: Quality improvement focus")
        
        if prospect_analysis["quality_distribution"]["premium"] > 10:
            priorities.append("Priority 3: Premium prospect targeting")
        
        return priorities

    def _recommend_link_building_budget(self, profile_score: int, total_prospects: int) -> int:
        """Рекомендация бюджета на link building"""
        base_budget = 200000  # Базовый бюджет
        
        if profile_score < 40:
            base_budget *= 2  # Удвоение для низкого качества
        elif profile_score > 70:
            base_budget *= 1.5  # Увеличение для поддержания высокого качества
        
        # Корректировка на количество prospects
        if total_prospects > 100:
            base_budget *= 1.3
        
        return int(base_budget)

    def _calculate_expected_links(self, budget: int) -> int:
        """Расчет ожидаемого количества ссылок"""
        avg_cost_per_link = 25000  # Средняя стоимость ссылки
        return int(budget / avg_cost_per_link)

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
                "min_da_threshold": self.min_da_threshold,
                "max_spam_score": self.max_spam_score,
                "min_relevance_score": self.min_relevance_score,
                "target_monthly_links": self.target_monthly_links
            }
        )