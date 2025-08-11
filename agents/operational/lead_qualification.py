"""
Lead Qualification Agent для AI SEO Architects
Полноценная версия с Pydantic моделями и comprehensive функциональностью
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging
import asyncio
import re

from pydantic import BaseModel, Field, validator
from core.base_agent import BaseAgent

logger = logging.getLogger(__name__)


# =================================================================
# PYDANTIC MODELS ДЛЯ ВАЛИДАЦИИ ДАННЫХ
# =================================================================

class LeadData(BaseModel):
    """Модель данных лида для валидации"""
    
    # Основная информация
    company_name: str = Field(..., min_length=2, description="Название компании")
    email: str = Field(..., description="Email контакт")
    phone: Optional[str] = Field(None, description="Телефон")
    website: Optional[str] = Field(None, description="Веб-сайт")
    
    # Контактное лицо
    contact_name: Optional[str] = Field(None, description="Имя контакта")
    contact_role: Optional[str] = Field(None, description="Роль контакта")
    
    # Бизнес информация
    industry: Optional[str] = Field(None, description="Отрасль")
    company_size: Optional[str] = Field(None, description="Размер компании")
    budget_range: Optional[str] = Field(None, description="Бюджетный диапазон")
    timeline: Optional[str] = Field(None, description="Временные рамки")
    
    # SEO специфика
    current_seo: Optional[str] = Field(None, description="Текущее SEO состояние")
    pain_points: Optional[List[str]] = Field(default_factory=list, description="Проблемы клиента")
    goals: Optional[List[str]] = Field(default_factory=list, description="Цели клиента")
    
    # Источник лида
    source: Optional[str] = Field(None, description="Источник лида")
    utm_campaign: Optional[str] = Field(None, description="UTM кампания")
    utm_source: Optional[str] = Field(None, description="UTM источник")
    
    # Дополнительная информация
    notes: Optional[str] = Field(None, description="Дополнительные заметки")
    referral_source: Optional[str] = Field(None, description="Источник рекомендации")
    
    @validator('email')
    def validate_email(cls, v):
        """Валидация email"""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Некорректный формат email')
        return v.lower()
    
    @validator('website')
    def validate_website(cls, v):
        """Валидация веб-сайта"""
        if v and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v


class QualificationResult(BaseModel):
    """Результат квалификации лида"""
    
    # Основные результаты
    lead_score: int = Field(..., ge=0, le=100, description="Общий скор лида")
    qualification: str = Field(..., description="Квалификация лида")
    
    # Детальные scores
    bant_score: int = Field(..., ge=0, le=100, description="BANT скор")
    meddic_score: int = Field(..., ge=0, le=100, description="MEDDIC скор")
    pain_score: int = Field(..., ge=0, le=100, description="Скор болевых точек")
    authority_score: int = Field(..., ge=0, le=100, description="Скор полномочий")
    
    # Классификации
    lead_type: str = Field(..., description="Тип лида (SMB/Mid-market/Enterprise)")
    priority: str = Field(..., description="Приоритет обработки")
    industry_fit: str = Field(..., description="Соответствие отрасли")
    
    # Аналитика
    strengths: List[str] = Field(default_factory=list, description="Сильные стороны лида")
    weaknesses: List[str] = Field(default_factory=list, description="Слабые стороны лида")
    risks: List[str] = Field(default_factory=list, description="Потенциальные риски")
    opportunities: List[str] = Field(default_factory=list, description="Возможности")
    
    # Рекомендации
    next_actions: List[str] = Field(default_factory=list, description="Следующие действия")
    recommended_approach: str = Field(..., description="Рекомендуемый подход")
    estimated_close_probability: float = Field(..., ge=0.0, le=1.0, description="Вероятность закрытия")
    estimated_deal_value: int = Field(..., ge=0, description="Ожидаемая стоимость сделки")
    
    # Метаданные
    qualification_timestamp: datetime = Field(default_factory=datetime.now)
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Уверенность в квалификации")


# =================================================================
# ОСНОВНОЙ КЛАСС АГЕНТА
# =================================================================

class LeadQualificationAgent(BaseAgent):
    """Агент квалификации лидов с comprehensive функциональностью"""
    
    def __init__(self, data_provider=None, agent_level=None, **kwargs):
        """Инициализация агента квалификации лидов"""
        # Убираем agent_level из kwargs если он там есть
        if 'agent_level' in kwargs:
            del kwargs['agent_level']
            
        super().__init__(
            agent_id="lead_qualification",
            name="Lead Qualification Agent",
            agent_level=agent_level or "operational",
            data_provider=data_provider,
            knowledge_base="knowledge/operational/lead_qualification.md",
            **kwargs
        )
        
        # Конфигурация скоринга
        self.scoring_weights = {
            "bant": 0.30,        # Budget, Authority, Need, Timeline
            "meddic": 0.25,      # Metrics, Economic buyer, Decision criteria, etc.
            "pain_intensity": 0.20,  # Интенсивность болевых точек
            "authority_level": 0.15, # Уровень полномочий контакта
            "industry_fit": 0.10     # Соответствие нашей экспертизе
        }
        
        # Отраслевые приоритеты
        self.industry_priorities = {
            "E-commerce": {"weight": 1.0, "expertise": "high"},
            "SaaS": {"weight": 0.95, "expertise": "high"},
            "B2B Services": {"weight": 0.90, "expertise": "high"},
            "Healthcare": {"weight": 0.85, "expertise": "medium"},
            "Real Estate": {"weight": 0.80, "expertise": "medium"},
            "Manufacturing": {"weight": 0.75, "expertise": "medium"},
            "Education": {"weight": 0.70, "expertise": "low"},
            "Non-profit": {"weight": 0.60, "expertise": "low"}
        }
        
        # Квалификационные пороги
        self.qualification_thresholds = {
            "Hot Lead": 85,
            "Warm Lead": 70,
            "Cold Lead": 50,
            "Unqualified": 0
        }
        
        logger.info(f"🎯 Инициализирован {self.name} с comprehensive scoring system")
    

    def calculate_lead_score(self, lead_data: Dict[str, Any]) -> int:
        """Агрессивная функция scoring для enterprise компаний"""
        
        company_name = lead_data.get('company_name', 'Unknown')
        print(f"🔍 АГРЕССИВНЫЙ Scoring для: {company_name}")
        
        # ОЧЕНЬ ВЫСОКИЙ базовый score
        score = 70
        
        # Размер компании - ГЛАВНЫЙ ФАКТОР
        company_size = str(lead_data.get('company_size', '0'))
        print(f"🏢 Размер компании: {company_size}")
        
        try:
            size_num = int(company_size.replace(',', '').replace(' ', ''))
            if size_num >= 5000:
                score += 30
                print(f"🏢 MEGA Enterprise bonus: +30")
            elif size_num >= 1000:
                score += 25
                print(f"🏢 Enterprise bonus: +25")
            elif size_num >= 500:
                score += 20
                print(f"🏢 Large company bonus: +20")
            elif size_num >= 100:
                score += 10
                print(f"🏢 Medium company bonus: +10")
        except Exception as e:
            print(f"⚠️ Ошибка парсинга размера: {e}")
        
        # Бюджет - ВТОРОЙ ВАЖНЫЙ ФАКТОР
        budget = str(lead_data.get('budget_range', ''))
        print(f"💰 Бюджет: {budget}")
        
        if '100000000' in budget or '100м' in budget.lower():
            score += 20
            print(f"💰 Ultra high budget bonus (100М ₽+ ₽): +20")
        elif '50000000' in budget or '50м' in budget.lower():
            score += 15
            print(f"💰 Very high budget bonus (50М ₽+ ₽): +15")
        elif '20000000' in budget or '20м' in budget.lower():
            score += 10
            print(f"💰 High budget bonus (20М ₽+ ₽): +10")
        
        # Индустрия
        industry = str(lead_data.get('industry', '')).lower()
        print(f"🏭 Индустрия: {industry}")
        
        if industry == 'fintech':
            score += 15
            print(f"🏦 FinTech bonus: +15")
        elif industry in ['ecommerce', 'fintech']:
            score += 10
            print(f"💻 Tech bonus: +10")
        
        # Timeline urgency
        timeline = str(lead_data.get('timeline', '')).lower()
        if timeline == 'urgent':
            score += 5
            print(f"⚡ Urgent timeline bonus: +5")
        
        # Email качество
        email = str(lead_data.get('email', '')).lower()
        if 'ceo@' in email or 'cto@' in email or 'director@' in email:
            score += 5
            print(f"📧 Executive email bonus: +5")
        
        final_score = min(100, score)
        print(f"📊 FINAL АГРЕССИВНЫЙ SCORE: {final_score}/100")
        
        return final_score

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Основная логика квалификации лида
        
        Args:
            task_data: Данные задачи с информацией о лиде
            
        Returns:
            Dict с результатами квалификации
        """
        try:
            # Извлекаем и валидируем входные данные
            input_data = task_data.get("input_data", {})
            
            # Безопасное создание LeadData с обработкой отсутствующих полей
            try:
                lead_data = LeadData(**input_data)
            except Exception as validation_error:
                # Если валидация не прошла, создаем минимальный объект
                logger.warning(f"Validation error, using basic data: {validation_error}")
                lead_data = LeadData(
                    company_name=input_data.get("company_name", "Unknown Company"),
                    email=input_data.get("email", "unknown@example.com")
                )
                # Добавляем дополнительные поля если они есть
                for field in ["industry", "company_size", "budget_range", "timeline", "phone", "website"]:
                    if field in input_data:
                        setattr(lead_data, field, input_data[field])
            
            logger.info(f"🔍 Начинаем квалификацию лида: {lead_data.company_name}")
            
            # 🧠 RAG: Получаем релевантные знания для квалификации
            query_text = f"lead qualification {lead_data.company_name} {lead_data.industry or ''} {lead_data.company_size or ''}"
            knowledge_context = await self.get_knowledge_context(query_text)
            
            if knowledge_context:
                logger.info(f"✅ Получен контекст знаний ({len(knowledge_context)} символов) для квалификации")
            else:
                logger.info("⚠️ Контекст знаний не найден, используем базовую логику")
            
            # Обогащаем данные лида
            enriched_data = await self._enrich_lead_data(lead_data)
            
            # Выполняем BANT анализ
            bant_score = self._calculate_bant_score(enriched_data)
            
            # Выполняем MEDDIC анализ  
            meddic_score = self._calculate_meddic_score(enriched_data)
            
            # Анализируем болевые точки
            pain_score = self._analyze_pain_points(enriched_data)
            
            # Оцениваем уровень полномочий
            authority_score = self._assess_authority_level(enriched_data)
            
            # Проверяем соответствие отрасли
            industry_score = self._evaluate_industry_fit(enriched_data)
            
            # Вычисляем общий скор
            total_score = self.calculate_lead_score(enriched_data.__dict__)






            
            # Определяем квалификацию и тип лида
            qualification = self._determine_qualification(total_score)
            lead_type = self._classify_lead_type(enriched_data)
            priority = self._assign_priority(total_score, lead_type)
            
            # Проводим SWOT анализ
            swot_analysis = self._perform_swot_analysis(enriched_data, total_score)
            
            # Генерируем рекомендации
            recommendations = self._generate_recommendations(enriched_data, total_score, qualification)
            
            # Прогнозируем стоимость сделки
            estimated_value = self._estimate_deal_value(enriched_data, lead_type)
            close_probability = self._estimate_close_probability(total_score, swot_analysis)
            
            # Создаем результат
            qualification_result = QualificationResult(
                lead_score=total_score,
                qualification=qualification,
                bant_score=bant_score,
                meddic_score=meddic_score,
                pain_score=pain_score,
                authority_score=authority_score,
                lead_type=lead_type,
                priority=priority,
                industry_fit=self.industry_priorities.get(enriched_data.industry, {}).get("expertise", "unknown"),
                strengths=swot_analysis["strengths"],
                weaknesses=swot_analysis["weaknesses"], 
                risks=swot_analysis["risks"],
                opportunities=swot_analysis["opportunities"],
                next_actions=recommendations["next_actions"],
                recommended_approach=recommendations["approach"],
                estimated_close_probability=close_probability,
                estimated_deal_value=estimated_value,
                confidence_level=self._calculate_confidence_level(enriched_data, total_score)
            )
            
            logger.info(f"✅ Квалификация завершена: {qualification} (Score: {total_score})")
            
            return {
                "success": True,
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "qualification_result": qualification_result.dict(),
                "lead_score": total_score,
                "qualification": qualification,
                "lead_type": lead_type,
                "priority": priority,
                "estimated_value": estimated_value,
                "close_probability": close_probability,
                "next_actions": recommendations["next_actions"],
                "recommended_approach": recommendations["approach"],
                "confidence_score": qualification_result.confidence_level,
                "enriched_data": enriched_data.dict(),
                "detailed_scores": {
                    "bant": bant_score,
                    "meddic": meddic_score,
                    "pain": pain_score, 
                    "authority": authority_score,
                    "industry": industry_score
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка квалификации лида: {str(e)}")
            return {
                "success": False,
                "agent": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "error": f"Lead qualification failed: {str(e)}",
                "lead_score": 0,
                "qualification": "error"
            }
    
    async def _enrich_lead_data(self, lead_data: LeadData) -> LeadData:
        """Обогащение данных лида через внешние источники"""
        
        try:
            # Получаем дополнительные данные о компании через data provider
            if lead_data.website:
                domain = lead_data.website.replace('https://', '').replace('http://', '').split('/')[0]
                
                try:
                    # Пытаемся получить SEO данные о сайте
                    seo_data = await self.get_seo_data(domain)
                    
                    # Обогащаем данные на основе SEO анализа
                    if not lead_data.industry and seo_data.content_analysis:
                        # Можем попытаться определить отрасль по контенту
                        lead_data.industry = self._infer_industry_from_content(seo_data.content_analysis)
                    
                    if not lead_data.company_size:
                        # Можем оценить размер компании по техническим показателям
                        lead_data.company_size = self._estimate_company_size(seo_data)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Не удалось получить SEO данные для {domain}: {str(e)}")
            
            # Нормализуем и дополняем данные
            if not lead_data.pain_points:
                lead_data.pain_points = self._infer_pain_points(lead_data)
            
            if not lead_data.contact_role and lead_data.contact_name:
                lead_data.contact_role = self._infer_contact_role(lead_data.contact_name, lead_data.email)
            
            return lead_data
            
        except Exception as e:
            logger.warning(f"⚠️ Ошибка обогащения данных: {str(e)}")
            return lead_data
    
    def _calculate_bant_score(self, lead_data: LeadData) -> int:
        """Расчет BANT score (Budget, Authority, Need, Timeline)"""
        
        score = 0
        
        # Budget (25 points)
        if lead_data.budget_range:
            budget_score = self._score_budget(lead_data.budget_range)
            score += budget_score
        
        # Authority (25 points)
        if lead_data.contact_role:
            authority_score = self._score_authority(lead_data.contact_role)
            score += authority_score
        
        # Need (25 points) 
        if lead_data.pain_points:
            need_score = self._score_need(lead_data.pain_points, lead_data.current_seo)
            score += need_score
        
        # Timeline (25 points)
        if lead_data.timeline:
            timeline_score = self._score_timeline(lead_data.timeline)
            score += timeline_score
        
        return min(score, 100)
    
    def _calculate_meddic_score(self, lead_data: LeadData) -> int:
        """Расчет MEDDIC score (Metrics, Economic buyer, Decision criteria, Decision process, Identify pain, Champion)"""
        
        score = 0
        
        # Metrics (определяем по целям и болевым точкам)
        if lead_data.goals:
            score += 15
        
        # Economic buyer (по роли контакта)
        if lead_data.contact_role:
            if any(role in lead_data.contact_role.lower() for role in ['ceo', 'cto', 'cmo', 'founder', 'owner']):
                score += 20
            elif any(role in lead_data.contact_role.lower() for role in ['director', 'manager', 'head']):
                score += 15
            else:
                score += 5
        
        # Decision criteria (по бюджету и timeline)
        if lead_data.budget_range and lead_data.timeline:
            score += 15
        
        # Decision process (по размеру компании)
        if lead_data.company_size:
            if 'enterprise' in lead_data.company_size.lower() or '500+' in lead_data.company_size:
                score += 10
            else:
                score += 15
        
        # Identify pain (болевые точки)
        if lead_data.pain_points:
            score += min(len(lead_data.pain_points) * 5, 20)
        
        # Champion (источник лида)
        if lead_data.referral_source or lead_data.source == 'referral':
            score += 15
        elif lead_data.source in ['website', 'content', 'webinar']:
            score += 10
        
        return min(score, 100)
    
    def _analyze_pain_points(self, lead_data: LeadData) -> int:
        """Анализ интенсивности болевых точек"""
        
        if not lead_data.pain_points:
            return 30  # Базовый score если нет информации
        
        high_impact_pains = [
            'low traffic', 'poor rankings', 'no leads', 'competitors outranking',
            'revenue decline', 'losing customers', 'poor roi', 'manual processes'
        ]
        
        medium_impact_pains = [
            'slow growth', 'inconsistent results', 'limited visibility',
            'outdated website', 'poor user experience'
        ]
        
        score = 20  # Базовый score
        
        for pain in lead_data.pain_points:
            pain_lower = pain.lower()
            
            if any(high_pain in pain_lower for high_pain in high_impact_pains):
                score += 20
            elif any(medium_pain in pain_lower for medium_pain in medium_impact_pains):
                score += 10
            else:
                score += 5
        
        return min(score, 100)
    
    def _assess_authority_level(self, lead_data: LeadData) -> int:
        """Оценка уровня полномочий контакта"""
        
        if not lead_data.contact_role:
            return 40  # Средний score без информации
        
        role = lead_data.contact_role.lower()
        
        # C-level executives
        if any(title in role for title in ['ceo', 'cto', 'cmo', 'cfo', 'founder', 'owner', 'president']):
            return 100
        
        # VP level
        elif any(title in role for title in ['vp', 'vice president', 'director']):
            return 85
        
        # Manager level  
        elif any(title in role for title in ['manager', 'head of', 'lead']):
            return 70
        
        # Specialist level
        elif any(title in role for title in ['specialist', 'coordinator', 'analyst']):
            return 50
        
        # Entry level
        elif any(title in role for title in ['assistant', 'intern', 'junior']):
            return 25
        
        return 40
    
    def _evaluate_industry_fit(self, lead_data: LeadData) -> int:
        """Оценка соответствия отрасли нашей экспертизе"""
        
        if not lead_data.industry:
            return 60  # Средний score без информации
        
        industry_info = self.industry_priorities.get(lead_data.industry, {"weight": 0.5, "expertise": "unknown"})
        
        base_score = int(industry_info["weight"] * 100)
        
        # Корректируем на основе экспертизы
        if industry_info["expertise"] == "high":
            return min(base_score + 10, 100)
        elif industry_info["expertise"] == "low":
            return max(base_score - 10, 20)
        
        return base_score
    
    def _calculate_total_score(self, scores: Dict[str, int]) -> int:
        """Расчет общего взвешенного score"""
        
        weighted_score = (
            scores["bant"] * self.scoring_weights["bant"] +
            scores["meddic"] * self.scoring_weights["meddic"] +
            scores["pain"] * self.scoring_weights["pain_intensity"] +
            scores["authority"] * self.scoring_weights["authority_level"] +
            scores["industry"] * self.scoring_weights["industry_fit"]
        )
        
        return int(weighted_score)
    
    def _determine_qualification(self, score: int) -> str:
        """Определение квалификации на основе score"""
        
        for qualification, threshold in self.qualification_thresholds.items():
            if score >= threshold:
                return qualification
        
        return "Unqualified"
    
    def _classify_lead_type(self, lead_data: LeadData) -> str:
        """Классификация типа лида (SMB/Mid-market/Enterprise)"""
        
        # Анализируем по размеру компании
        if lead_data.company_size:
            size = lead_data.company_size.lower()
            if '500+' in size or 'enterprise' in size or 'large' in size:
                return "Enterprise"
            elif any(indicator in size for indicator in ['50-500', '100-500', 'medium']):
                return "Mid-market"
            else:
                return "SMB"
        
        # Анализируем по бюджету
        if lead_data.budget_range:
            budget = lead_data.budget_range.lower()
            if any(indicator in budget for indicator in ['5000000+', '10000000+', '5м+', '10м+']):
                return "Enterprise"
            elif any(indicator in budget for indicator in ['1000000-5000000', '1м-5м', '1500000-3000000']):
                return "Mid-market"
            else:
                return "SMB"
        
        # По роли контакта
        if lead_data.contact_role:
            role = lead_data.contact_role.lower()
            if any(title in role for title in ['ceo', 'founder', 'owner']) and lead_data.industry in ['SaaS', 'E-commerce']:
                return "Mid-market"
        
        return "SMB"  # По умолчанию
    
    def _assign_priority(self, score: int, lead_type: str) -> str:
        """Назначение приоритета обработки"""
        
        if score >= 85:
            return "Critical"
        elif score >= 70:
            return "High"
        elif score >= 50:
            return "Medium"
        else:
            return "Low"
    
    def _perform_swot_analysis(self, lead_data: LeadData, score: int) -> Dict[str, List[str]]:
        """SWOT анализ лида"""
        
        strengths = []
        weaknesses = []
        opportunities = []
        risks = []
        
        # Strengths
        if score >= 80:
            strengths.append("Высокий общий скор квалификации")
        
        if lead_data.referral_source:
            strengths.append("Пришел по рекомендации")
        
        if lead_data.budget_range and any(indicator in lead_data.budget_range for indicator in ['2500000+', '5000000+']):
            strengths.append("Достаточный бюджет")
        
        if lead_data.contact_role and any(role in lead_data.contact_role.lower() for role in ['ceo', 'founder', 'cto']):
            strengths.append("Контакт с высокими полномочиями")
        
        # Weaknesses
        if score < 50:
            weaknesses.append("Низкий общий скор квалификации")
        
        if not lead_data.budget_range:
            weaknesses.append("Неизвестен бюджет")
        
        if not lead_data.timeline:
            weaknesses.append("Неопределенные временные рамки")
        
        if not lead_data.pain_points:
            weaknesses.append("Не выявлены болевые точки")
        
        # Opportunities
        if lead_data.industry in ['E-commerce', 'SaaS']:
            opportunities.append("Отрасль с высоким потенциалом")
        
        if lead_data.current_seo == 'none' or lead_data.current_seo == 'basic':
            opportunities.append("Большой потенциал для улучшения SEO")
        
        if 'growth' in str(lead_data.goals).lower():
            opportunities.append("Ориентированность на рост")
        
        # Risks
        if not lead_data.contact_role or 'assistant' in lead_data.contact_role.lower():
            risks.append("Низкий уровень полномочий контакта")
        
        if lead_data.budget_range and any(indicator in lead_data.budget_range.lower() for indicator in ['5000', '2500', 'low']):
            risks.append("Ограниченный бюджет")
        
        if lead_data.industry in ['Non-profit', 'Education']:
            risks.append("Отрасль с ограниченным бюджетом")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "opportunities": opportunities,
            "risks": risks
        }
    
    def _generate_recommendations(self, lead_data: LeadData, score: int, qualification: str) -> Dict[str, Any]:
        """Генерация рекомендаций по работе с лидом"""
        
        next_actions = []
        approach = ""
        
        if qualification == "Hot Lead":
            next_actions = [
                "Немедленно связаться по телефону",
                "Отправить персонализированное предложение",
                "Предложить бесплатный SEO аудит",
                "Назначить демонстрацию в течение 24 часов"
            ]
            approach = "Агрессивный sales подход с быстрым закрытием"
            
        elif qualification == "Warm Lead":
            next_actions = [
                "Отправить welcome email с case studies",
                "Предложить консультацию по SEO стратегии",
                "Добавить в nurturing campaign",
                "Запланировать follow-up через 2-3 дня"
            ]
            approach = "Консультативный подход с построением доверия"
            
        elif qualification == "Cold Lead":
            next_actions = [
                "Добавить в long-term nurturing",
                "Отправить образовательный контент",
                "Подписать на newsletter",
                "Follow-up через 2 недели"
            ]
            approach = "Образовательный подход с длительным nurturing"
            
        else:  # Unqualified
            next_actions = [
                "Добавить в базу для будущего контакта",
                "Отправить общий информационный материал",
                "Попытаться дополнительно квалифицировать",
                "Переоценить через 3 месяца"
            ]
            approach = "Минимальные усилия, периодическая переоценка"
        
        # Добавляем специфичные рекомендации
        if not lead_data.budget_range:
            next_actions.append("Выяснить бюджетные рамки")
        
        if not lead_data.timeline:
            next_actions.append("Уточнить временные рамки принятия решения")
        
        if not lead_data.contact_role:
            next_actions.append("Определить роль и полномочия контакта")
        
        return {
            "next_actions": next_actions,
            "approach": approach
        }
    
    def _estimate_deal_value(self, lead_data: LeadData, lead_type: str) -> int:
        """Оценка потенциальной стоимости сделки"""
        
        base_values = {
            "SMB": 15000,
            "Mid-market": 45000,
            "Enterprise": 120000
        }
        
        base_value = base_values.get(lead_type, 15000)
        
        # Корректируем на основе бюджета
        if lead_data.budget_range:
            budget = lead_data.budget_range.lower()
            if '10000000+' in budget or '10м+' in budget:
                base_value = max(base_value, 10000000)
            elif '5000000+' in budget or '5м+' in budget:
                base_value = max(base_value, 5000000)
            elif '2500000+' in budget or '2.5м+' in budget:
                base_value = max(base_value, 2500000)
        
        # Корректируем на основе отрасли
        if lead_data.industry:
            industry_multiplier = self.industry_priorities.get(lead_data.industry, {}).get("weight", 1.0)
            base_value = int(base_value * industry_multiplier)
        
        return base_value
    
    def _estimate_close_probability(self, score: int, swot_analysis: Dict[str, List[str]]) -> float:
        """Оценка вероятности закрытия сделки"""
        
        # Базовая вероятность на основе score
        base_probability = score / 100.0
        
        # Корректируем на основе SWOT
        strengths_bonus = len(swot_analysis["strengths"]) * 0.05
        risks_penalty = len(swot_analysis["risks"]) * 0.03
        
        probability = base_probability + strengths_bonus - risks_penalty
        
        return max(0.05, min(0.95, probability))
    
    def _calculate_confidence_level(self, lead_data: LeadData, score: int) -> float:
        """Расчет уверенности в квалификации"""
        
        data_completeness = 0
        total_fields = 0
        
        # Проверяем заполненность ключевых полей
        key_fields = [
            lead_data.company_name, lead_data.email, lead_data.contact_role,
            lead_data.industry, lead_data.budget_range, lead_data.timeline,
            lead_data.pain_points, lead_data.company_size
        ]
        
        for field in key_fields:
            total_fields += 1
            if field:
                data_completeness += 1
        
        completeness_ratio = data_completeness / total_fields
        
        # Высокая уверенность при высоком score и полных данных
        confidence = (completeness_ratio * 0.6) + (score / 100.0 * 0.4)
        
        return round(confidence, 2)
    
    # =================================================================
    # HELPER МЕТОДЫ ДЛЯ SCORING
    # =================================================================
    
    def _score_budget(self, budget_range: str) -> int:
        """Скоринг бюджета"""
        budget = budget_range.lower()
        
        if any(indicator in budget for indicator in ['10000000+', '10м+', '6 figures']):
            return 25
        elif any(indicator in budget for indicator in ['5000000+', '5м+', '25000-50000']):
            return 20
        elif any(indicator in budget for indicator in ['15000-25000', '10000-25000']):
            return 15
        elif any(indicator in budget for indicator in ['5000-15000', '5k-15k']):
            return 10
        else:
            return 5
    
    def _score_authority(self, contact_role: str) -> int:
        """Скоринг полномочий"""
        role = contact_role.lower()
        
        if any(title in role for title in ['ceo', 'founder', 'owner', 'president']):
            return 25
        elif any(title in role for title in ['cto', 'cmo', 'cfo', 'vp']):
            return 20
        elif any(title in role for title in ['director', 'head of']):
            return 15
        elif any(title in role for title in ['manager', 'lead']):
            return 10
        else:
            return 5
    
    def _score_need(self, pain_points: List[str], current_seo: Optional[str]) -> int:
        """Скоринг потребности"""
        score = 5  # Базовый score
        
        # За каждую болевую точку
        score += min(len(pain_points) * 3, 15)
        
        # За текущее состояние SEO
        if current_seo:
            seo_state = current_seo.lower()
            if seo_state in ['none', 'no seo', 'nothing']:
                score += 5
            elif seo_state in ['basic', 'minimal', 'poor']:
                score += 3
        
        return min(score, 25)
    
    def _score_timeline(self, timeline: str) -> int:
        """Скоринг временных рамок"""
        timeline_lower = timeline.lower()
        
        if any(indicator in timeline_lower for indicator in ['asap', 'immediately', 'urgent', 'now']):
            return 25
        elif any(indicator in timeline_lower for indicator in ['1 month', '30 days', 'q1', 'q2']):
            return 20
        elif any(indicator in timeline_lower for indicator in ['2-3 months', '3 months', 'q3']):
            return 15
        elif any(indicator in timeline_lower for indicator in ['6 months', 'next year', 'q4']):
            return 10
        else:
            return 5
    
    # =================================================================
    # ДОПОЛНИТЕЛЬНЫЕ HELPER МЕТОДЫ
    # =================================================================
    
    def _infer_industry_from_content(self, content_analysis: Dict[str, Any]) -> Optional[str]:
        """Определение отрасли по контенту сайта"""
        # Простая логика определения отрасли - можно улучшить с ML
        content_text = str(content_analysis).lower()
        
        if any(keyword in content_text for keyword in ['ecommerce', 'shop', 'buy', 'cart', 'product']):
            return "E-commerce"
        elif any(keyword in content_text for keyword in ['saas', 'saas', 'platform', 'api']):
            return "SaaS"
        elif any(keyword in content_text for keyword in ['consulting', 'services', 'business']):
            return "B2B Services"
        elif any(keyword in content_text for keyword in ['health', 'medical', 'clinic', 'doctor']):
            return "Healthcare"
        elif any(keyword in content_text for keyword in ['real estate', 'property', 'homes', 'realty']):
            return "Real Estate"
        
        return None
    
    def _estimate_company_size(self, seo_data) -> Optional[str]:
        """Оценка размера компании по SEO данным"""
        try:
            crawl_data = seo_data.crawl_data
            if isinstance(crawl_data, dict):
                pages_count = crawl_data.get('pages_crawled', 0)
                
                if pages_count > 1000:
                    return "Large (500+ employees)"
                elif pages_count > 100:
                    return "Medium (50-500 employees)"
                else:
                    return "Small (1-50 employees)"
        except Exception as e:
            print(f"Ошибка при анализе размера компании: {str(e)}")
            return "Unknown size"
        
        return None
    
    def _infer_pain_points(self, lead_data: LeadData) -> List[str]:
        """Определение болевых точек на основе доступных данных"""
        pain_points = []
        
        # На основе источника лида
        if lead_data.source == 'organic search':
            pain_points.append("Поиск SEO решений")
        elif lead_data.source == 'paid ads':
            pain_points.append("Высокая стоимость платного трафика")
        
        # На основе отрасли
        if lead_data.industry == 'E-commerce':
            pain_points.extend(["Низкая конверсия", "Слабые позиции товаров в поиске"])
        elif lead_data.industry == 'SaaS':
            pain_points.extend(["Недостаток органического трафика", "Высокая стоимость привлечения клиентов"])
        
        return pain_points
    
    def _infer_contact_role(self, contact_name: str, email: str) -> Optional[str]:
        """Определение роли контакта по имени и email"""
        if not contact_name:
            return None
        
        name_lower = contact_name.lower()
        email_lower = email.lower()
        
        # Простые эвристики
        if any(title in email_lower for title in ['ceo', 'founder', 'owner']):
            return "CEO/Founder"
        elif any(title in email_lower for title in ['marketing', 'cmo']):
            return "Marketing Manager"
        elif any(title in name_lower for title in ['john', 'jane']) and 'info@' in email_lower:
            return "General Contact"
        
        return "Unknown Role"
