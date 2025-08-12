"""
Proposal Generation Agent - Автоматизированное создание коммерческих предложений
Часть AI SEO Architects - Milestone 3
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ProposalGenerationAgent(BaseAgent):
    """
    Агент автоматической генерации коммерческих предложений

    Возможности:
    - Создание персонализированных предложений на основе lead data
    - Динамическое ценообразование по отраслям
    - ROI калькуляции и прогнозы
    - Интеграция с результатами Lead Qualification
    """

    def __init__(self, data_provider=None, **kwargs):
        super().__init__(
            agent_id="proposal_generation_agent",
            name="Proposal Generation Agent",
            agent_level="operational",
            data_provider=data_provider,
            knowledge_base="knowledge/operational/proposal_generation.md",
            model_name="gpt-4o-mini",
            **kwargs
        )

        # Загружаем knowledge base при инициализации
        self.knowledge_content = self._load_knowledge_base()

        # Конфигурация pricing стратегий
        self.pricing_config = {
            "base_rates": {
                "seo_audit": {"smb": 250000, "mid_market": 500000, "enterprise": 1200000},
                "monthly_retainer": {"smb": 350000, "mid_market": 850000, "enterprise": 2500000},
                "content_strategy": {"smb": 150000, "mid_market": 350000, "enterprise": 800000},
                "link_building": {"smb": 200000, "mid_market": 450000, "enterprise": 1500000}
            },
            "industry_multipliers": {
                "e-commerce": 1.2,
                "saas": 1.3,
                "b2b_services": 1.0,
                "healthcare": 1.4,
                "real_estate": 1.1,
                "default": 1.0
            },
            "lead_score_multipliers": {
                "hot": 1.2,      # 80-100 points
                "warm": 1.0,     # 60-79 points
                "cold": 0.8,     # 40-59 points
                "mql": 1.1,      # 50-79 points
                "unqualified": 0.7  # <40 points
            }
        }

    def _load_knowledge_base(self) -> str:
        """Загрузка базы знаний из файла"""
        try:
            kb_path = Path(self.knowledge_base)
            if kb_path.exists():
                with open(kb_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                logger.warning(f"Knowledge base file not found: {kb_path}")
                return "# Proposal Generation Knowledge Base\n\nBase knowledge for proposal generation."
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            return "# Proposal Generation Knowledge Base\n\nFallback knowledge base."

    def get_system_prompt(self) -> str:
        """Системный промпт для Proposal Generation Agent"""
        return """Ты - Proposal Generation Agent, эксперт по созданию персонализированных коммерческих предложений для SEO-услуг.

ТВОЯ ЭКСПЕРТИЗА:
• Персонализированные предложения - 40%
• Динамическое ценообразование - 30%
• ROI калькуляции и прогнозы - 20%
• Интеграция с lead данными - 10%

ЗАДАЧА: Создай comprehensive коммерческое предложение на основе lead данных.

ФОРМАТ ОТВЕТА (JSON):
{
  "proposal": {
    "executive_summary": "string",
    "service_packages": [],
    "pricing": {},
    "roi_projections": {},
    "timeline": {}
  },
  "personalization": {},
  "competitive_advantages": [],
  "next_steps": []
}"""

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная функция обработки задачи создания предложения с LLM
        """
        try:
            input_data = task_data.get("input_data", {})
            
            print(f"🎯 Proposal Generation Agent обрабатывает задачу")

            # Промпт для LLM
            user_prompt = f"""Создай персонализированное коммерческое предложение:
            
LEAD ДАННЫЕ:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

Создай comprehensive proposal с учетом специфики клиента."""
            
            # LLM вызов
            llm_result = await self.process_with_llm(user_prompt, task_data)
            
            if llm_result["success"]:
                try:
                    import re
                    llm_content = llm_result["result"]
                    if isinstance(llm_content, str):
                        json_match = re.search(r'\{.*\}', llm_content, re.DOTALL)
                        if json_match:
                            result = json.loads(json_match.group())
                        else:
                            result = self._create_fallback_proposal(input_data)
                    else:
                        result = llm_content
                except (json.JSONDecodeError, AttributeError):
                    result = self._create_fallback_proposal(input_data)
            else:
                result = self._create_fallback_proposal(input_data)

            return {
                "success": True,
                "agent": self.agent_id,
                "result": result,
                "model_used": llm_result.get('model_used') if llm_result["success"] else None,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "agent": self.agent_id, "error": str(e)}

    def _create_fallback_proposal(self, input_data):
        """Fallback proposal"""
        return {
            "proposal": {
                "executive_summary": "Персонализированное SEO предложение для вашего бизнеса",
                "service_packages": ["Technical SEO", "Content Strategy", "Link Building"],
                "pricing": {"monthly": 150000, "setup": 50000},
                "roi_projections": {"6_months": 2.5, "12_months": 4.2},
                "timeline": {"implementation": "4-6 недель", "results": "3-6 месяцев"}
            },
            "personalization": {"industry_focus": True, "custom_kpis": True},
            "competitive_advantages": ["AI-powered optimization", "Real-time reporting"],
            "next_steps": ["Подписание договора", "Техническое ТЗ", "Начало работ"],
            "fallback_used": True
        }

    def _analyze_lead_data(self, lead_result: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ данных лида для персонализации предложения (ИСПРАВЛЕННАЯ ВЕРСИЯ)"""

        # Извлекаем ключевую информацию
        lead_data = lead_result.get("enriched_data", {})
        final_score = lead_result.get("final_score", 0)
        classification = lead_result.get("classification", "unqualified")

        # Определяем размер компании
        employees = lead_data.get("employees", 0)
        if isinstance(employees, str):
            try:
                employees = int(employees.replace(',', '').replace('employees', '').strip())
            except:
                employees = 0
        
        if employees >= 1000:
            company_size = "enterprise"
        elif employees >= 50:
            company_size = "mid_market"
        else:
            company_size = "smb"

        # Анализируем отрасль
        industry = lead_data.get("industry", "").lower()
        industry_category = self._map_industry_category(industry)

        # Определяем уровень зрелости SEO
        seo_maturity = self._assess_seo_maturity(company_size, industry_category, final_score)

        # 🔧 КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Добавляем estimated_issues
        estimated_issues = self._estimate_seo_issues(seo_maturity)

        # Формируем результат с ПОЛНОЙ структурой данных
        return {
            "client_info": {
                "company_name": lead_data.get("company_name", "Ваша компания"),
                "contact_name": lead_data.get("contact_name", ""),
                "website": lead_data.get("website", ""),
                "employees": employees,
                "industry": industry_category,
                "company_size": company_size
            },
            "lead_scoring": {
                "final_score": final_score,
                "classification": classification,
                "priority_level": "high" if final_score >= 80 else "medium" if final_score >= 60 else "low"
            },
            "seo_analysis": {
                "website": lead_data.get("website", ""),
                "current_budget": lead_data.get("current_budget", 0),
                "maturity_level": seo_maturity,
                "challenges": lead_data.get("challenges", []),
                "estimated_issues": estimated_issues,  # 🔧 ИСПРАВЛЕНО!
                "opportunity_score": min(0.99, final_score / 100 + 0.1)
            },
            "priority_services": self._identify_priority_services(lead_data, {"maturity_level": seo_maturity}),
            "pain_points": lead_data.get("pain_points", []),
            "goals": lead_data.get("goals", [])
        }
    def _map_industry_category(self, industry: str) -> str:
        """Маппинг отрасли к категории для pricing"""
        industry_mapping = {
            "ecommerce": "e-commerce",
            "e-commerce": "e-commerce",
            "online store": "e-commerce",
            "retail": "e-commerce",
            "saas": "saas",
            "software": "saas",
            "technology": "saas",
            "healthcare": "healthcare",
            "medical": "healthcare",
            "real estate": "real_estate",
            "property": "real_estate",
            "consulting": "b2b_services",
            "services": "b2b_services",
            "b2b": "b2b_services"
        }

        for key, category in industry_mapping.items():
            if key in industry.lower():
                return category

        return "default"

    
    def _assess_seo_maturity(self, company_size: str, industry_category: str, final_score: int) -> str:
        """Оценка уровня зрелости SEO (СОЗДАННЫЙ МЕТОД)"""
        
        # Базовая оценка по размеру компании
        if company_size == "enterprise":
            base_maturity = "intermediate"
        elif company_size == "mid_market":
            base_maturity = "basic"
        else:
            base_maturity = "beginner"
        
        # Корректировка по отрасли
        if industry_category in ["fintech", "saas", "ecommerce"]:
            # Цифровые отрасли обычно более зрелые в SEO
            if base_maturity == "beginner":
                base_maturity = "basic"
            elif base_maturity == "basic":
                base_maturity = "intermediate"
        
        # Корректировка по Lead Score
        if final_score >= 80:
            if base_maturity == "beginner":
                base_maturity = "basic"
            elif base_maturity == "basic": 
                base_maturity = "intermediate"
        elif final_score <= 30:
            base_maturity = "beginner"
        
        return base_maturity

    def _analyze_current_seo(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ текущего состояния SEO клиента"""

        # Базовый анализ на основе lead данных
        website = lead_data.get("website", "")
        current_seo_budget = lead_data.get("current_seo_budget", 0)
        seo_challenges = lead_data.get("seo_challenges", [])

        # Оценка текущего состояния
        if current_seo_budget == 0:
            seo_maturity = "beginner"
        elif current_seo_budget < 5000:
            seo_maturity = "basic"
        elif current_seo_budget < 15000:
            seo_maturity = "intermediate"
        else:
            seo_maturity = "advanced"

        return {
            "website": website,
            "current_budget": current_seo_budget,
            "maturity_level": seo_maturity,
            "challenges": seo_challenges,
            "estimated_issues": self._estimate_seo_issues(seo_maturity),
            "opportunity_score": self._calculate_opportunity_score(current_seo_budget, seo_challenges)
        }

    def _estimate_seo_issues(self, maturity_level: str) -> List[str]:
        """Оценка вероятных SEO проблем на основе уровня зрелости"""

        issue_templates = {
            "beginner": [
                "Отсутствие базовой технической оптимизации",
                "Неоптимизированная структура URL",
                "Медленная скорость загрузки страниц",
                "Отсутствие или неполная настройка Google Analytics",
                "Базовые проблемы с мета-тегами"
            ],
            "basic": [
                "Неэффективная внутренняя перелинковка",
                "Отсутствие стратегии контент-маркетинга",
                "Ограниченная мобильная оптимизация",
                "Слабый профиль внешних ссылок"
            ],
            "intermediate": [
                "Субоптимальная техническая архитектура",
                "Недостаточная оптимизация для локального поиска",
                "Неэффективное использование структурированных данных"
            ],
            "advanced": [
                "Оптимизация для новых алгоритмических обновлений",
                "Advanced technical optimizations",
                "Международная SEO стратегия"
            ]
        }

        return issue_templates.get(maturity_level, issue_templates["beginner"])

    def _calculate_opportunity_score(self, current_budget: float, challenges: List[str]) -> float:
        """Расчет оценки потенциала улучшения"""

        base_score = 0.7  # Базовая оценка потенциала

        # Корректировка на основе текущего бюджета
        if current_budget == 0:
            budget_multiplier = 1.3  # Большой потенциал
        elif current_budget < 5000:
            budget_multiplier = 1.1
        else:
            budget_multiplier = 0.9

        # Корректировка на основе количества вызовов
        challenge_multiplier = min(1.2, 1.0 + len(challenges) * 0.05)

        return min(1.0, base_score * budget_multiplier * challenge_multiplier)

    def _identify_priority_services(self, lead_data: Dict[str, Any], seo_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Определение приоритетных услуг для клиента"""

        services = []
        maturity = seo_state.get("maturity_level", "beginner")

        # Технический аудит - почти всегда нужен
        services.append({
            "name": "Технический SEO аудит",
            "priority": "high",
            "rationale": "Выявление и устранение технических проблем сайта"
        })

        # Определяем дополнительные услуги на основе зрелости
        if maturity in ["beginner", "basic"]:
            services.extend([
                {
                    "name": "Базовая оптимизация",
                    "priority": "high",
                    "rationale": "Настройка основ SEO для фундамента роста"
                },
                {
                    "name": "Контент-стратегия",
                    "priority": "medium",
                    "rationale": "Создание SEO-оптимизированного контента"
                }
            ])

        if maturity in ["intermediate", "advanced"]:
            services.extend([
                {
                    "name": "Ссылочная стратегия",
                    "priority": "high",
                    "rationale": "Наращивание авторитета домена"
                },
                {
                    "name": "Продвинутая аналитика",
                    "priority": "medium",
                    "rationale": "Глубокий анализ и оптимизация конверсий"
                }
            ])

        # Месячное сопровождение - для всех
        services.append({
            "name": "Месячное SEO-сопровождение",
            "priority": "medium",
            "rationale": "Непрерывный мониторинг и улучшение результатов"
        })

        return services[:4]  # Максимум 4 приоритетные услуги

    async def _generate_pricing(self, lead_analysis: Dict[str, Any], client_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация ценового предложения"""

        company_size = lead_analysis["client_info"]["company_size"]
        industry = lead_analysis["client_info"]["industry"]
        classification = lead_analysis["lead_scoring"]["classification"]
        priority_services = lead_analysis["priority_services"]

        # Базовые цены
        base_rates = self.pricing_config["base_rates"]
        industry_multiplier = self.pricing_config["industry_multipliers"].get(industry, 1.0)
        score_multiplier = self.pricing_config["lead_score_multipliers"].get(classification, 1.0)

        # Расчет цен по услугам
        service_pricing = {}
        total_one_time = 0
        total_monthly = 0

        for service in priority_services:
            service_name = service["name"]

            if "аудит" in service_name.lower():
                base_price = base_rates["seo_audit"][company_size]
                service_pricing["seo_audit"] = {
                    "name": "Технический SEO аудит",
                    "type": "one_time",
                    "base_price": base_price,
                    "final_price": int(base_price * industry_multiplier * score_multiplier),
                    "description": "Комплексный технический анализ сайта"
                }
                total_one_time += service_pricing["seo_audit"]["final_price"]

            elif "сопровождение" in service_name.lower():
                base_price = base_rates["monthly_retainer"][company_size]
                service_pricing["monthly_retainer"] = {
                    "name": "Месячное SEO-сопровождение",
                    "type": "monthly",
                    "base_price": base_price,
                    "final_price": int(base_price * industry_multiplier * score_multiplier),
                    "description": "Ежемесячная оптимизация и мониторинг"
                }
                total_monthly += service_pricing["monthly_retainer"]["final_price"]

            elif "контент" in service_name.lower():
                base_price = base_rates["content_strategy"][company_size]
                service_pricing["content_strategy"] = {
                    "name": "Контент-стратегия",
                    "type": "one_time",
                    "base_price": base_price,
                    "final_price": int(base_price * industry_multiplier * score_multiplier),
                    "description": "Разработка стратегии контент-маркетинга"
                }
                total_one_time += service_pricing["content_strategy"]["final_price"]

            elif "ссылочная" in service_name.lower():
                base_price = base_rates["link_building"][company_size]
                service_pricing["link_building"] = {
                    "name": "Ссылочная стратегия",
                    "type": "monthly",
                    "base_price": base_price,
                    "final_price": int(base_price * industry_multiplier * score_multiplier),
                    "description": "Наращивание качественного ссылочного профиля"
                }
                total_monthly += service_pricing["link_building"]["final_price"]

        # Создание пакетных предложений
        packages = self._create_package_options(service_pricing, total_one_time, total_monthly)

        return {
            "individual_services": service_pricing,
            "packages": packages,
            "total_one_time": total_one_time,
            "total_monthly": total_monthly,
            "total_annual": total_monthly * 12 + total_one_time,
            "pricing_factors": {
                "company_size": company_size,
                "industry_multiplier": industry_multiplier,
                "lead_score_multiplier": score_multiplier,
                "effective_multiplier": industry_multiplier * score_multiplier
            }
        }

    def _create_package_options(self, service_pricing: Dict[str, Any], total_one_time: int, total_monthly: int) -> Dict[str, Any]:
        """Создание пакетных предложений с скидками"""

        packages = {}

        # Базовый пакет
        if "seo_audit" in service_pricing:
            packages["basic"] = {
                "name": "SEO Старт",
                "services": ["seo_audit"],
                "one_time_price": service_pricing["seo_audit"]["final_price"],
                "monthly_price": 0,
                "discount": 0,
                "description": "Комплексный технический аудит для начала оптимизации"
            }

        # Стандартный пакет
        if total_one_time > 0 and total_monthly > 0:
            discount = 0.1  # 10% скидка
            packages["standard"] = {
                "name": "SEO Рост",
                "services": list(service_pricing.keys()),
                "one_time_price": int(total_one_time * (1 - discount)),
                "monthly_price": int(total_monthly * (1 - discount)),
                "discount": discount,
                "description": "Полный комплекс SEO услуг со скидкой 10%"
            }

        # Премиум пакет (с дополнительными услугами)
        if total_monthly > 0:
            premium_multiplier = 1.5
            discount = 0.15  # 15% скидка
            packages["premium"] = {
                "name": "SEO Максимум",
                "services": list(service_pricing.keys()) + ["advanced_analytics", "priority_support"],
                "one_time_price": int(total_one_time * premium_multiplier * (1 - discount)),
                "monthly_price": int(total_monthly * premium_multiplier * (1 - discount)),
                "discount": discount,
                "description": "Расширенный пакет с приоритетной поддержкой и продвинутой аналитикой"
            }

        return packages

    def _calculate_roi_projections(self, lead_analysis: Dict[str, Any], pricing_proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет ROI проекций для обоснования инвестиций"""

        company_size = lead_analysis["client_info"]["company_size"]
        industry = lead_analysis["client_info"]["industry"]
        opportunity_score = lead_analysis["seo_analysis"]["opportunity_score"]

        # Базовые множители роста трафика по размеру компании
        traffic_growth_potential = {
            "smb": {"6_months": 1.5, "12_months": 2.2, "24_months": 3.5},
            "mid_market": {"6_months": 1.3, "12_months": 1.8, "24_months": 2.8},
            "enterprise": {"6_months": 1.2, "12_months": 1.5, "24_months": 2.2}
        }

        # Отраслевые конверсии (среднестатистические)
        industry_conversions = {
            "e-commerce": 0.025,
            "saas": 0.035,
            "b2b_services": 0.045,
            "healthcare": 0.030,
            "real_estate": 0.040,
            "default": 0.035
        }

        # Средний чек по отраслям и размерам
        average_deal_value = {
            "smb": {"e-commerce": 150, "saas": 500, "b2b_services": 2500, "healthcare": 800, "real_estate": 5000, "default": 800},
            "mid_market": {"e-commerce": 400, "saas": 1500, "b2b_services": 8000, "healthcare": 2000, "real_estate": 15000, "default": 2500},
            "enterprise": {"e-commerce": 800, "saas": 500000, "b2b_services": 2500000, "healthcare": 500000, "real_estate": 5000000, "default": 800000}
        }

        # Получаем базовые параметры
        traffic_potential = traffic_growth_potential[company_size]
        conversion_rate = industry_conversions.get(industry, industry_conversions["default"])
        avg_deal = average_deal_value[company_size].get(industry, average_deal_value[company_size]["default"])

        # Корректируем на основе opportunity score
        adjusted_potential = {
            period: growth * opportunity_score
            for period, growth in traffic_potential.items()
        }

        # Рассчитываем проекции
        annual_investment = pricing_proposal["total_annual"]

        projections = {}
        for period, traffic_growth in adjusted_potential.items():
            # Предполагаем базовый трафик для расчета
            estimated_base_traffic = self._estimate_base_traffic(company_size)
            new_traffic = estimated_base_traffic * (traffic_growth - 1)  # Прирост трафика

            # Конверсии и выручка
            monthly_conversions = (new_traffic / 12) * conversion_rate
            monthly_revenue = monthly_conversions * avg_deal
            annual_revenue = monthly_revenue * 12

            # ROI расчет
            roi_ratio = annual_revenue / annual_investment if annual_investment > 0 else 0
            roi_percentage = (roi_ratio - 1) * 100

            projections[period] = {
                "traffic_growth": f"{(traffic_growth - 1) * 100:.0f}%",
                "additional_monthly_traffic": int(new_traffic / 12),
                "monthly_conversions": round(monthly_conversions, 1),
                "monthly_revenue": int(monthly_revenue),
                "annual_revenue": int(annual_revenue),
                "roi_ratio": round(roi_ratio, 1),
                "roi_percentage": f"{roi_percentage:.0f}%"
            }

        return {
            "assumptions": {
                "conversion_rate": f"{conversion_rate * 100:.1f}%",
                "average_deal_value": f"{avg_deal:,}",
                "opportunity_score": f"{opportunity_score:.1f}",
                "annual_investment": f"{annual_investment:,}"
            },
            "projections": projections,
            "summary": {
                "breakeven_months": self._calculate_breakeven_months(projections, annual_investment),
                "total_3_year_roi": f"{((projections['24_months']['annual_revenue'] * 1.5) / annual_investment - 1) * 100:.0f}%"
            }
        }

    def _estimate_base_traffic(self, company_size: str) -> int:
        """Оценка базового трафика по размеру компании"""
        base_traffic_estimates = {
            "smb": 5000,        # 5K посетителей в месяц
            "mid_market": 25000,  # 25K посетителей в месяц
            "enterprise": 100000  # 100K посетителей в месяц
        }
        return base_traffic_estimates.get(company_size, 10000)

    def _calculate_breakeven_months(self, projections: Dict[str, Any], annual_investment: float) -> int:
        """Расчет времени окупаемости в месяцах"""
        try:
            monthly_investment = annual_investment / 12
            monthly_revenue_12m = projections["12_months"]["monthly_revenue"]

            if monthly_revenue_12m > monthly_investment:
                return int(monthly_investment / (monthly_revenue_12m - monthly_investment))
            else:
                return 24  # Если не окупается за год, возвращаем 24 месяца
        except:
            return 18  # Fallback значение

    async def _generate_proposal_content(self, lead_analysis: Dict[str, Any],
                                       pricing_proposal: Dict[str, Any],
                                       roi_projections: Dict[str, Any],
                                       proposal_type: str) -> Dict[str, Any]:
        """Генерация основного содержания предложения"""

        client_info = lead_analysis["client_info"]
        company_name = client_info["company_name"]
        industry = client_info["industry"]
        priority_services = lead_analysis["priority_services"]

        # Executive Summary
        executive_summary = self._create_executive_summary(
            company_name, industry, priority_services, roi_projections
        )

        # Situation Analysis
        situation_analysis = self._create_situation_analysis(lead_analysis)

        # Recommended Strategy
        strategy = self._create_strategy_section(priority_services, industry)

        # Implementation Timeline
        timeline = self._create_implementation_timeline(priority_services)

        # Investment Overview
        investment = self._create_investment_section(pricing_proposal)

        # Expected Results
        results = self._create_results_section(roi_projections)

        # Case Studies (based on industry)
        case_studies = self._select_relevant_case_studies(industry)

        # Next Steps
        next_steps = self._create_next_steps_section()

        return {
            "executive_summary": executive_summary,
            "situation_analysis": situation_analysis,
            "recommended_strategy": strategy,
            "implementation_timeline": timeline,
            "investment_overview": investment,
            "expected_results": results,
            "case_studies": case_studies,
            "next_steps": next_steps,
            "appendices": {
                "about_company": "AI SEO Architects - ведущее агентство по поисковой оптимизации",
                "team_credentials": "Наша команда экспертов с 10+ летним опытом",
                "certifications": ["Google Partner", "Bing Ads Accredited", "SEMrush Certified"]
            }
        }

    def _create_executive_summary(self, company_name: str, industry: str,
                                priority_services: List[Dict], roi_projections: Dict[str, Any]) -> str:
        """Создание executive summary"""

        service_names = [service["name"] for service in priority_services[:3]]
        roi_12m = roi_projections["projections"]["12_months"]["roi_percentage"]

        return f"""
# Коммерческое предложение для {company_name}

## Краткое изложение

{company_name} имеет значительный потенциал для роста органического трафика и онлайн-присутствия.

Наш анализ показывает возможности для:
- Увеличения органического трафика на {roi_projections["projections"]["12_months"]["traffic_growth"]}
- Улучшения конверсии сайта через SEO-оптимизацию
- Достижения ROI {roi_12m} в течение 12 месяцев

**Рекомендуемые приоритетные услуги:**
{chr(10).join([f"- {service}" for service in service_names])}

**Инвестиции:** {roi_projections["assumptions"]["annual_investment"]}
**Ожидаемая дополнительная выручка:** {roi_projections["projections"]["12_months"]["annual_revenue"]:,} ₽ ₽ в год
"""

    def _create_situation_analysis(self, lead_analysis: Dict[str, Any]) -> str:
        """Создание анализа текущей ситуации"""

        seo_analysis = lead_analysis["seo_analysis"]
        pain_points = lead_analysis.get("pain_points", [])

        issues_text = "\n".join([f"- {issue}" for issue in seo_analysis["estimated_issues"][:5]])
        pain_points_text = "\n".join([f"- {pain}" for pain in pain_points[:3]]) if pain_points else "- Необходимость повышения видимости в поиске"

        return f"""
## Анализ текущей ситуации

### Текущее состояние SEO
- Уровень SEO зрелости: {seo_analysis["maturity_level"]}
- Текущий SEO бюджет: {seo_analysis["current_budget"]:,} ₽ ₽/месяц
- Оценка потенциала: {seo_analysis["opportunity_score"]:.1f}/1.0

### Выявленные проблемы
{issues_text}

### Ключевые вызовы
{pain_points_text}

### Возможности для роста
На основе нашего анализа, мы видим существенные возможности для улучшения органических позиций и трафика за счет комплексного подхода к SEO-оптимизации.
"""

    def _create_strategy_section(self, priority_services: List[Dict], industry: str) -> str:
        """Создание раздела стратегии"""

        strategy_text = ""
        for i, service in enumerate(priority_services, 1):
            strategy_text += f"""
### {i}. {service["name"]} ({service["priority"]} приоритет)
**Обоснование:** {service["rationale"]}
"""

        return f"""
## Рекомендуемая стратегия

Для достижения максимальных результатов мы рекомендуем поэтапный подход:
{strategy_text}

### Специфика отрасли: {industry}
Учитывая особенности вашей отрасли, мы применим специализированные методики оптимизации и ключевые метрики успеха.
"""

    def _create_implementation_timeline(self, priority_services: List[Dict]) -> str:
        """Создание временной шкалы реализации"""

        timeline = """
## План реализации

### Месяц 1-2: Аудит и планирование
- Комплексный технический аудит
- Анализ конкурентов и ключевых слов
- Создание стратегии контента

### Месяц 2-4: Техническая оптимизация
- Устранение технических проблем
- Оптимизация скорости загрузки
- Настройка аналитики и отслеживания

### Месяц 3-6: Контент и ссылки
- Реализация контент-плана
- Начало работы со ссылочным профилем
- Оптимизация существующих страниц

### Месяц 6-12: Масштабирование и рост
- Расширение семантического ядра
- Дополнительные каналы трафика
- Постоянная оптимизация и улучшение
"""
        return timeline

    def _create_investment_section(self, pricing_proposal: Dict[str, Any]) -> str:
        """Создание раздела инвестиций"""

        packages = pricing_proposal.get("packages", {})

        investment_text = """
## Варианты инвестиций

"""

        for package_key, package in packages.items():
            discount_text = f" (скидка {package['discount']*100:.0f}%)" if package['discount'] > 0 else ""
            investment_text += f"""
### {package["name"]}{discount_text}
{package["description"]}

- Первоначальная стоимость: {package["one_time_price"]:,} ₽ ₽
- Ежемесячная стоимость: {package["monthly_price"]:,} ₽ ₽
- Годовая стоимость: {(package["one_time_price"] + package["monthly_price"] * 12):,} ₽ ₽

"""

        investment_text += """
### Что включено в стоимость
- Персональный менеджер проекта
- Ежемесячные отчеты о прогрессе
- Неограниченные консультации
- Гарантия качества работ
"""

        return investment_text

    def _create_results_section(self, roi_projections: Dict[str, Any]) -> str:
        """Создание раздела ожидаемых результатов"""

        proj_6m = roi_projections["projections"]["6_months"]
        proj_12m = roi_projections["projections"]["12_months"]

        return f"""
## Ожидаемые результаты

### Через 6 месяцев
- Прирост трафика: {proj_6m["traffic_growth"]}
- Дополнительный трафик: {proj_6m["additional_monthly_traffic"]:,} ₽ посетителей/месяц
- Конверсии: {proj_6m["monthly_conversions"]} заявок/месяц
- Дополнительная выручка: {proj_6m["monthly_revenue"]:,} ₽ ₽/месяц

### Через 12 месяцев
- Прирост трафика: {proj_12m["traffic_growth"]}
- Дополнительный трафик: {proj_12m["additional_monthly_traffic"]:,} ₽ посетителей/месяц
- Конверсии: {proj_12m["monthly_conversions"]} заявок/месяц
- Дополнительная выручка: {proj_12m["monthly_revenue"]:,} ₽ ₽/месяц
- **ROI: {proj_12m["roi_percentage"]}**

### Ключевые метрики успеха
- Увеличение позиций в топ-10 на 50+ ключевых запросах
- Рост органического трафика на {proj_12m["traffic_growth"]}
- Улучшение технических показателей сайта на 40%
- Повышение конверсии сайта на 15-25%
"""

    def _select_relevant_case_studies(self, industry: str) -> List[Dict[str, Any]]:
        """Выбор релевантных кейсов для отрасли"""

        # База кейсов по отраслям (в реальном проекте это будет из базы данных)
        case_studies_db = {
            "e-commerce": [
                {
                    "title": "Интернет-магазин электроники: +340% трафика за 8 месяцев",
                    "industry": "E-commerce",
                    "results": "Рост органического трафика с 12,000 до 52,800 посетителей/месяц",
                    "timeline": "8 месяцев",
                    "key_activities": ["Техническая оптимизация", "Контент-маркетинг", "Локальное SEO"]
                }
            ],
            "saas": [
                {
                    "title": "SaaS платформа: увеличение MRR на 4,700,000 ₽ через SEO",
                    "industry": "SaaS",
                    "results": "Рост квалифицированного трафика на 280%, +4.7М ₽ MRR",
                    "timeline": "12 месяцев",
                    "key_activities": ["Content marketing", "Technical SEO", "Link building"]
                }
            ],
            "default": [
                {
                    "title": "B2B сервис: кратный рост лидов через поисковую оптимизацию",
                    "industry": "B2B Services",
                    "results": "Увеличение органических лидов на 420% за 10 месяцев",
                    "timeline": "10 месяцев",
                    "key_activities": ["Техническая оптимизация", "Контент-стратегия", "Local SEO"]
                }
            ]
        }

        return case_studies_db.get(industry, case_studies_db["default"])

    def _create_next_steps_section(self) -> Dict[str, Any]:
        """Создание раздела следующих шагов"""

        return {
            "immediate_steps": [
                "Подписание договора и техническое задание",
                "Предоставление доступов к сайту и аналитике",
                "Начало технического аудита (1-2 рабочих дня)"
            ],
            "timeline": {
                "contract_signing": "В течение 3 рабочих дней",
                "project_kickoff": "В течение 5 рабочих дней",
                "first_deliverables": "14 рабочих дней"
            },
            "contact_info": {
                "next_meeting": "Предлагаем созвониться для обсуждения деталей",
                "decision_timeline": "Предложение действительно 30 дней",
                "support": "Готовы ответить на любые вопросы в течение 24 часов"
            }
        }

    def _generate_next_steps(self, lead_analysis: Dict[str, Any], urgency: str) -> List[str]:
        """Генерация рекомендаций по следующим шагам"""

        classification = lead_analysis["lead_scoring"]["classification"]
        final_score = lead_analysis["lead_scoring"]["final_score"]

        steps = []

        # Базовые шаги для всех
        steps.append("Отправить подробное предложение клиенту")

        # Шаги на основе классификации лида
        if classification == "hot" or final_score >= 80:
            steps.extend([
                "Немедленно связаться для обсуждения (в течение 4 часов)",
                "Предложить демо-презентацию с конкретными рекомендациями",
                "Подготовить персонализированную презентацию с кейсами"
            ])
        elif classification == "warm" or final_score >= 60:
            steps.extend([
                "Связаться в течение 24 часов для уточнения потребностей",
                "Отправить релевантные кейсы и материалы",
                "Запланировать презентацию на следующую неделю"
            ])
        elif classification == "cold" or final_score >= 40:
            steps.extend([
                "Добавить в nurturing последовательность",
                "Отправить образовательные материалы",
                "Запланировать follow-up через 2 недели"
            ])
        else:  # unqualified
            steps.extend([
                "Добавить в базу для долгосрочного nurturing",
                "Отправить общие материалы о SEO",
                "Переоценить через 3 месяца"
            ])

        # Коррекция на срочность
        if urgency == "high":
            steps.insert(1, "СРОЧНО: Приоритетная обработка - ответить в течение 2 часов")

        return steps[:5]  # Максимум 5 шагов

    def _calculate_confidence_score(self, lead_analysis: Dict[str, Any]) -> float:
        """Расчет уверенности в предложении"""

        base_confidence = 0.75

        # Факторы уверенности
        lead_score = lead_analysis["lead_scoring"]["final_score"]
        opportunity_score = lead_analysis["seo_analysis"]["opportunity_score"]

        # Корректировки
        score_factor = min(1.2, lead_score / 80)  # Нормализуем к 80 как макс
        opportunity_factor = opportunity_score

        final_confidence = min(0.95, base_confidence * score_factor * opportunity_factor)

        return round(final_confidence, 2)

    def _get_priority_level(self, score: float) -> str:
        """Определение уровня приоритета по score"""
        if score >= 80:
            return "high"
        elif score >= 60:
            return "medium"
        else:
            return "low"
