"""
Lead Qualification Agent - Агент квалификации лидов
Первый operational агент для демонстрации работы системы
"""
from typing import Dict, Any
from core.base_agent import BaseAgent
from core.state_models import SEOArchitectsState
from datetime import datetime

class LeadQualificationAgent(BaseAgent):
    """Агент для квалификации входящих лидов"""
    
    def __init__(self):
        """Инициализация агента квалификации лидов"""
        super().__init__(
            name="Lead Qualification Agent",
            level="operational", 
            specialization="Квалификация и скоринг лидов"
        )
        
        # Критерии скоринга из базы знаний
        self.scoring_criteria = {
            "company_size": 25,
            "budget": 30, 
            "timeline": 15,
            "authority": 15,
            "technical_level": 10,
            "competition": 5
        }
    
    async def process_task(self, state: SEOArchitectsState) -> SEOArchitectsState:
        """
        Обрабатывает задачу квалификации лида
        
        Args:
            state: Текущее состояние системы
            
        Returns:
            SEOArchitectsState: Обновленное состояние
        """
        self.log_action("Начало квалификации лида", {
            "client_id": state.get("client_id", "unknown"),
            "task_type": state.get("task_type", "unknown")
        })
        
        # Получаем данные лида
        lead_data = state.get("input_data", {})
        
        # Выполняем скоринг
        lead_score = self._calculate_lead_score(lead_data)
        
        # Определяем классификацию
        lead_classification = self._classify_lead(lead_score)
        
        # Создаем результат
        qualification_result = {
            "lead_score": lead_score,
            "classification": lead_classification,
            "qualification_details": self._generate_qualification_details(lead_data, lead_score),
            "recommended_next_steps": self._get_next_steps(lead_classification),
            "processed_at": datetime.now().isoformat()
        }
        
        # Обновляем состояние
        updated_state = self.update_state(
            state=state,
            result=qualification_result,
            next_agent=self._determine_next_agent(lead_classification)
        )
        
        self.log_action("Квалификация завершена", {
            "score": lead_score,
            "classification": lead_classification,
            "next_agent": self._determine_next_agent(lead_classification)
        })
        
        return updated_state
    
    def _calculate_lead_score(self, lead_data: Dict[str, Any]) -> int:
        """Расчет скоринга лида по критериям"""
        total_score = 0
        
        # Размер компании
        company_size = lead_data.get("company_size", "unknown")
        if company_size == "enterprise":
            total_score += 25
        elif company_size == "large":
            total_score += 20
        elif company_size == "medium":
            total_score += 15
        elif company_size == "small":
            total_score += 10
        else:
            total_score += 5
        
        # Бюджет
        budget = lead_data.get("budget_range", "unknown")
        if "50k+" in str(budget).lower():
            total_score += 30
        elif "15-50k" in str(budget).lower():
            total_score += 25
        elif "5-15k" in str(budget).lower():
            total_score += 15
        elif "1-5k" in str(budget).lower():
            total_score += 10
        else:
            total_score += 5
        
        # Срочность
        timeline = lead_data.get("timeline", "unknown")
        if "immediate" in str(timeline).lower():
            total_score += 15
        elif "quarter" in str(timeline).lower():
            total_score += 10
        elif "year" in str(timeline).lower():
            total_score += 6
        else:
            total_score += 3
        
        # Полномочия
        authority = lead_data.get("decision_authority", "unknown")
        if "economic_buyer" in str(authority).lower():
            total_score += 15
        elif "decision_maker" in str(authority).lower():
            total_score += 10
        else:
            total_score += 5
        
        return min(total_score, 100)  # Максимум 100 баллов
    
    def _classify_lead(self, score: int) -> str:
        """Классификация лида по скорингу"""
        if score >= 90:
            return "Hot Lead"
        elif score >= 70:
            return "Warm Lead"
        elif score >= 50:
            return "Cold Lead"
        elif score >= 30:
            return "MQL"
        else:
            return "Unqualified"
    
    def _generate_qualification_details(self, lead_data: Dict[str, Any], score: int) -> Dict[str, Any]:
        """Генерация детальной информации о квалификации"""
        return {
            "company_profile": {
                "name": lead_data.get("company_name", "Unknown"),
                "size": lead_data.get("company_size", "Unknown"),
                "industry": lead_data.get("industry", "Unknown"),
                "website": lead_data.get("website", "")
            },
            "contact_info": {
                "name": lead_data.get("contact_name", "Unknown"),
                "email": lead_data.get("email", ""),
                "position": lead_data.get("position", "Unknown")
            },
            "business_context": {
                "budget_range": lead_data.get("budget_range", "Unknown"),
                "timeline": lead_data.get("timeline", "Unknown"),
                "current_challenges": lead_data.get("challenges", []),
                "goals": lead_data.get("goals", [])
            },
            "technical_assessment": {
                "current_seo_level": lead_data.get("seo_maturity", "Unknown"),
                "website_issues": lead_data.get("technical_issues", []),
                "competition_level": lead_data.get("competition", "Unknown")
            },
            "qualification_score": score
        }
    
    def _get_next_steps(self, classification: str) -> List[str]:
        """Определение следующих шагов на основе классификации"""
        if classification == "Hot Lead":
            return [
                "Немедленный звонок Senior Sales Representative",
                "Подготовка персонализированной презентации",
                "Экспресс-аудит сайта клиента",
                "Составление предварительного предложения"
            ]
        elif classification == "Warm Lead":
            return [
                "Передача Sales Conversation Agent",
                "Планирование discovery call",
                "Отправка релевантных case studies",
                "Nurturing email sequence"
            ]
        elif classification == "Cold Lead":
            return [
                "Добавление в long-term nurturing",
                "Подписка на образовательный контент",
                "Quarterly check-in планирование",
                "Monitoring изменений в компании"
            ]
        else:
            return [
                "Образовательный контент",
                "Newsletter подписка",
                "Resource library доступ"
            ]
    
    def _determine_next_agent(self, classification: str) -> str:
        """Определение следующего агента для обработки"""
        if classification == "Hot Lead":
            return "sales_conversation_agent"
        elif classification == "Warm Lead":
            return "sales_operations_manager"
        elif classification == "Cold Lead":
            return "client_success_manager"
        else:
            return "END"
