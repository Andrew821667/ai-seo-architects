"""
LangGraph оркестратор для координации AI SEO Architects
Управляет потоком задач между агентами трех уровней
"""
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from core.state_models import SEOArchitectsState
from core.config import config
import logging
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SEOArchitectsOrchestrator:
    """Главный оркестратор системы AI SEO Architects"""
    
    def __init__(self):
        """Инициализация оркестратора"""
        self.agents = {}
        self.graph = None
        self.compiled_graph = None
        logger.info("🏗️ Инициализация AI SEO Architects Orchestrator")
    
    def register_agent(self, agent_name: str, agent_instance) -> None:
        """
        Регистрация агента в системе
        
        Args:
            agent_name: Имя агента
            agent_instance: Экземпляр агента
        """
        self.agents[agent_name] = agent_instance
        logger.info(f"🤖 Зарегистрирован агент: {agent_name}")
    
    def create_workflow_graph(self) -> StateGraph:
        """
        Создает граф workflow для LangGraph
        
        Returns:
            StateGraph: Граф состояний для выполнения
        """
        # Создаем основной граф
        workflow = StateGraph(SEOArchitectsState)
        
        # Добавляем узлы для каждого уровня агентов
        
        # Executive Level
        workflow.add_node("chief_seo_strategist", self._executive_node)
        workflow.add_node("business_development_director", self._executive_node)
        
        # Management Level  
        workflow.add_node("task_coordinator", self._management_node)
        workflow.add_node("sales_operations_manager", self._management_node)
        workflow.add_node("technical_seo_operations_manager", self._management_node)
        workflow.add_node("client_success_manager", self._management_node)
        
        # Operational Level
        workflow.add_node("lead_qualification_agent", self._operational_node)
        workflow.add_node("sales_conversation_agent", self._operational_node)
        workflow.add_node("proposal_generation_agent", self._operational_node)
        workflow.add_node("technical_seo_auditor", self._operational_node)
        workflow.add_node("content_strategy_agent", self._operational_node)
        workflow.add_node("link_building_agent", self._operational_node)
        workflow.add_node("competitive_analysis_agent", self._operational_node)
        workflow.add_node("reporting_agent", self._operational_node)
        
        # Устанавливаем точку входа
        workflow.set_entry_point("task_coordinator")
        
        # Добавляем условную логику маршрутизации
        workflow.add_conditional_edges(
            "task_coordinator",
            self._route_from_coordinator,
            {
                "sales_flow": "lead_qualification_agent",
                "seo_audit": "technical_seo_auditor",
                "content_strategy": "content_strategy_agent",
                "strategic_planning": "chief_seo_strategist",
                "end": END
            }
        )
        
        # Добавляем маршрутизацию для sales flow
        workflow.add_conditional_edges(
            "lead_qualification_agent",
            self._route_from_lead_qualification,
            {
                "hot_lead": "sales_conversation_agent",
                "warm_lead": "sales_operations_manager", 
                "cold_lead": "client_success_manager",
                "end": END
            }
        )
        
        # Добавляем завершающие переходы
        workflow.add_edge("sales_conversation_agent", "proposal_generation_agent")
        workflow.add_edge("proposal_generation_agent", END)
        workflow.add_edge("technical_seo_auditor", "reporting_agent")
        workflow.add_edge("content_strategy_agent", "reporting_agent")
        workflow.add_edge("reporting_agent", END)
        
        self.graph = workflow
        return workflow
    
    async def _executive_node(self, state: SEOArchitectsState) -> SEOArchitectsState:
        """Обработка задач Executive уровня - БЕЗ ЗАГЛУШЕК"""
        current_agent = state["current_agent"]
        logger.info(f"🎯 Executive узел: {current_agent}")
        
        if current_agent in self.agents:
            # РЕАЛЬНЫЙ ВЫЗОВ АГЕНТА
            agent_instance = self.agents[current_agent]
            task_data = {
                "task_type": state.get("task_type", ""),
                "input_data": state.get("input_data", {}),
                "client_context": state.get("client_context", {}),
                "domain": state.get("domain", ""),
                "client_id": state.get("client_id", "")
            }
            
            try:
                result = await agent_instance.process_task(task_data)
                state["processing_results"].append({
                    "agent": current_agent,
                    "level": "executive",
                    "status": "success",
                    "result": result,
                    "timestamp": state.get("timestamp", "")
                })
                logger.info(f"✅ {current_agent} успешно выполнен")
            except Exception as e:
                logger.error(f"❌ Ошибка в {current_agent}: {str(e)}")
                state["processing_results"].append({
                    "agent": current_agent,
                    "level": "executive", 
                    "status": "error",
                    "error": str(e)
                })
        else:
            logger.warning(f"⚠️ Агент {current_agent} не зарегистрирован")
            state["processing_results"].append({
                "agent": current_agent,
                "level": "executive",
                "status": "not_found",
                "message": f"Агент {current_agent} не найден в системе"
            })
        
        return state
    
    async def _management_node(self, state: SEOArchitectsState) -> SEOArchitectsState:
        """Обработка задач Management уровня - БЕЗ ЗАГЛУШЕК"""
        current_agent = state["current_agent"]
        logger.info(f"📊 Management узел: {current_agent}")
        
        if current_agent in self.agents:
            # РЕАЛЬНЫЙ ВЫЗОВ АГЕНТА
            agent_instance = self.agents[current_agent]
            task_data = {
                "task_type": state.get("task_type", ""),
                "input_data": state.get("input_data", {}),
                "client_context": state.get("client_context", {}),
                "domain": state.get("domain", ""),
                "client_id": state.get("client_id", "")
            }
            
            try:
                result = await agent_instance.process_task(task_data)
                state["processing_results"].append({
                    "agent": current_agent,
                    "level": "management",
                    "status": "success",
                    "result": result,
                    "timestamp": state.get("timestamp", "")
                })
                logger.info(f"✅ {current_agent} успешно выполнен")
            except Exception as e:
                logger.error(f"❌ Ошибка в {current_agent}: {str(e)}")
                state["processing_results"].append({
                    "agent": current_agent,
                    "level": "management",
                    "status": "error", 
                    "error": str(e)
                })
        else:
            logger.warning(f"⚠️ Агент {current_agent} не зарегистрирован")
            state["processing_results"].append({
                "agent": current_agent,
                "level": "management",
                "status": "not_found",
                "message": f"Агент {current_agent} не найден в системе"
            })
        
        return state
    
    async def _operational_node(self, state: SEOArchitectsState) -> SEOArchitectsState:
        """Обработка задач Operational уровня - БЕЗ ЗАГЛУШЕК"""
        current_agent = state["current_agent"]
        logger.info(f"⚙️ Operational узел: {current_agent}")
        
        if current_agent in self.agents:
            # РЕАЛЬНЫЙ ВЫЗОВ АГЕНТА
            agent_instance = self.agents[current_agent]
            task_data = {
                "task_type": state.get("task_type", ""),
                "input_data": state.get("input_data", {}),
                "client_context": state.get("client_context", {}),
                "domain": state.get("domain", ""),
                "client_id": state.get("client_id", "")
            }
            
            try:
                result = await agent_instance.process_task(task_data)
                state["processing_results"].append({
                    "agent": current_agent,
                    "level": "operational",
                    "status": "success",
                    "result": result,
                    "timestamp": state.get("timestamp", "")
                })
                logger.info(f"✅ {current_agent} успешно выполнен")
            except Exception as e:
                logger.error(f"❌ Ошибка в {current_agent}: {str(e)}")
                state["processing_results"].append({
                    "agent": current_agent,
                    "level": "operational",
                    "status": "error",
                    "error": str(e)
                })
        else:
            logger.warning(f"⚠️ Агент {current_agent} не зарегистрирован")
            state["processing_results"].append({
                "agent": current_agent,
                "level": "operational",
                "status": "not_found",
                "message": f"Агент {current_agent} не найден в системе"
            })
        
        return state
    
    def _route_from_coordinator(self, state: SEOArchitectsState) -> str:
        """Маршрутизация от Task Coordinator"""
        task_type = state.get("task_type", "")
        
        if task_type == "lead_processing":
            return "sales_flow"
        elif task_type == "seo_audit":
            return "seo_audit"
        elif task_type == "content_strategy":
            return "content_strategy"
        elif task_type == "strategic_planning":
            return "strategic_planning"
        else:
            return "end"
    
    def _route_from_lead_qualification(self, state: SEOArchitectsState) -> str:
        """Маршрутизация от Lead Qualification Agent"""
        # Проверяем результаты квалификации
        if state["processing_results"]:
            last_result = state["processing_results"][-1]
            if last_result.get("status") == "success" and "result" in last_result:
                agent_result = last_result["result"]
                if "lead_score" in agent_result:
                    score = agent_result["lead_score"]
                    if score >= 90:
                        return "hot_lead"
                    elif score >= 70:
                        return "warm_lead"
                    elif score >= 50:
                        return "cold_lead"
        
        return "end"
    
    def compile_workflow(self) -> Any:
        """
        Компилирует workflow для выполнения
        
        Returns:
            Скомпилированный граф
        """
        if not self.graph:
            self.create_workflow_graph()
        
        self.compiled_graph = self.graph.compile()
        logger.info("✅ Workflow скомпилирован и готов к выполнению")
        return self.compiled_graph
    
    async def execute_workflow(self, initial_state: SEOArchitectsState) -> SEOArchitectsState:
        """
        Выполняет workflow с начальным состоянием
        
        Args:
            initial_state: Начальное состояние
            
        Returns:
            SEOArchitectsState: Финальное состояние после выполнения
        """
        if not self.compiled_graph:
            self.compile_workflow()
        
        logger.info("🚀 Запуск workflow AI SEO Architects")
        
        # Выполняем граф
        final_state = await self.compiled_graph.ainvoke(initial_state)
        
        logger.info("✅ Workflow завершен успешно")
        return final_state

# Глобальный экземпляр оркестратора
orchestrator = SEOArchitectsOrchestrator()
