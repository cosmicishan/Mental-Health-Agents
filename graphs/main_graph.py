from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, Optional, Literal
from typing_extensions import TypedDict

# Import all agents
from agents.intake_agent import intake_agent
from agents.crisis_agent import crisis_agent
from agents.therapeutical_agent import therapeutic_agent
from agents.resource_coordinator_agent import resource_coordinator_agent
from agents.wellness_coach_agent import wellness_coach_agent
from agents.coordinator_agent import coordinator_agent

# Import state
from states.enhanced_state import EnhancedState

def build_mental_health_graph():
    """Build and return the complete mental health support graph."""
    
    # Create the main graph with enhanced state
    graph_builder = StateGraph(EnhancedState)
    
    # Add all specialized agent nodes
    graph_builder.add_node("intake_agent", intake_agent)
    graph_builder.add_node("coordinator_agent", coordinator_agent)
    graph_builder.add_node("crisis_agent", crisis_agent)
    graph_builder.add_node("therapeutic_agent", therapeutic_agent)
    graph_builder.add_node("resource_coordinator_agent", resource_coordinator_agent)
    graph_builder.add_node("wellness_coach_agent", wellness_coach_agent)
    
    # Entry point - always start with intake assessment
    graph_builder.add_edge(START, "intake_agent")
    
    # Intake agent routing - can go to any specialist or coordinator
    graph_builder.add_conditional_edges(
        "intake_agent",
        lambda state: state.get("current_agent", "coordinator_agent"),
        {
            "crisis": "crisis_agent",
            "therapeutic": "therapeutic_agent", 
            "resource_coordinator": "resource_coordinator_agent",
            "wellness_coach": "wellness_coach_agent",
            "coordinator": "coordinator_agent"
        }
    )
    
    # Coordinator agent - master router that can send to any specialist
    graph_builder.add_conditional_edges(
        "coordinator_agent",
        lambda state: determine_next_agent(state),
        {
            "crisis_agent": "crisis_agent",
            "therapeutic_agent": "therapeutic_agent",
            "resource_coordinator_agent": "resource_coordinator_agent", 
            "wellness_coach_agent": "wellness_coach_agent",
            "intake_agent": "intake_agent",
            "__end__": END
        }
    )
    
    # Crisis agent - highest priority, can end or go to coordinator
    graph_builder.add_conditional_edges(
        "crisis_agent",
        lambda state: determine_crisis_next_step(state),
        {
            "coordinator_agent": "coordinator_agent",
            "therapeutic_agent": "therapeutic_agent",
            "__end__": END
        }
    )
    
    # Therapeutic agent - can continue with coordinator or end
    graph_builder.add_conditional_edges(
        "therapeutic_agent", 
        lambda state: determine_therapeutic_next_step(state),
        {
            "coordinator_agent": "coordinator_agent",
            "resource_coordinator_agent": "resource_coordinator_agent",
            "wellness_coach_agent": "wellness_coach_agent",
            "__end__": END
        }
    )
    
    # Resource coordinator - can refer to other specialists or end
    graph_builder.add_conditional_edges(
        "resource_coordinator_agent",
        lambda state: determine_resource_next_step(state),
        {
            "coordinator_agent": "coordinator_agent",
            "therapeutic_agent": "therapeutic_agent",
            "wellness_coach_agent": "wellness_coach_agent",
            "__end__": END
        }
    )
    
    # Wellness coach - can coordinate with others or end
    graph_builder.add_conditional_edges(
        "wellness_coach_agent",
        lambda state: determine_wellness_next_step(state),
        {
            "coordinator_agent": "coordinator_agent", 
            "therapeutic_agent": "therapeutic_agent",
            "resource_coordinator_agent": "resource_coordinator_agent",
            "__end__": END
        }
    )
    
    compiled_graph = graph_builder.compile()
 
    return compiled_graph

def determine_next_agent(state: EnhancedState) -> str:
    """Determine next agent based on coordinator's routing decision."""
    
    # Check for crisis override
    crisis_level = state.get("crisis_level", 0)
    if crisis_level and crisis_level >= 8:
        return "crisis_agent"
    
    # Check current agent recommendation from coordinator
    current_agent = state.get("current_agent", "")
    
    # Map current agent to next node
    agent_mapping = {
        "crisis": "crisis_agent",
        "therapeutic": "therapeutic_agent", 
        "resource_coordinator": "resource_coordinator_agent",
        "wellness_coach": "wellness_coach_agent",
        "intake": "intake_agent",
        "coordinator": "coordinator_agent",
        "ended": "__end__"
    }
    
    return agent_mapping.get(current_agent, "__end__")

def determine_crisis_next_step(state: EnhancedState) -> str:
    """Determine next step after crisis intervention."""
    
    # Check if crisis is resolved or needs follow-up
    intervention_plan = state.get("intervention_plan", {})
    crisis_level = state.get("crisis_level", 0)
    
    # If crisis level is still high, continue crisis support
    if crisis_level >= 8:
        return "__end__"  # End for immediate professional help
    
    # If safety plan created and crisis reduced, can move to therapeutic support
    if intervention_plan.get("safety_plan_created") and crisis_level < 6:
        return "therapeutic_agent"
    
    # Default to coordinator for further assessment
    return "coordinator_agent"

def determine_therapeutic_next_step(state: EnhancedState) -> str:
    """Determine next step after therapeutic intervention."""
    
    # Check session context and user needs
    session_context = state.get("session_context", {})
    intervention_plan = state.get("intervention_plan", {})
    
    # If user needs resources (therapists, support groups)
    if "resource" in str(session_context).lower() or "therapist" in str(session_context).lower():
        return "resource_coordinator_agent"
    
    # If user needs lifestyle/wellness support
    if "wellness" in str(session_context).lower() or "lifestyle" in str(session_context).lower():
        return "wellness_coach_agent"
    
    # Check if multiple sessions or complex needs
    if intervention_plan.get("exercises_provided", 0) > 2:
        return "coordinator_agent"
    
    # Default to ending after therapeutic intervention
    return "__end__"

def determine_resource_next_step(state: EnhancedState) -> str:
    """Determine next step after resource coordination."""
    
    intervention_plan = state.get("intervention_plan", {})
    session_context = state.get("session_context", {})

    if intervention_plan is None:

        return "__end__"
    
    # If resources found and user might need ongoing support
    if intervention_plan.get("resources_found", 0) > 0:
        # Check if user also needs therapeutic support
        if "therapy" in str(session_context).lower() or "counseling" in str(session_context).lower():
            return "therapeutic_agent"
        
        # Check if user needs wellness planning
        if "wellness" in str(session_context).lower():
            return "wellness_coach_agent"
    
    # Default to coordinator for further needs assessment
    return "__end__"

def determine_wellness_next_step(state: EnhancedState) -> str:
    """Determine next step after wellness coaching."""
    
    intervention_plan = state.get("intervention_plan", {})
    session_context = state.get("session_context", {})

    if intervention_plan is None:

        return "__end__"
    
    # If wellness plan created and user has therapeutic needs
    if intervention_plan.get("plans_created", 0) > 0:
        if "therapy" in str(session_context).lower() or "emotional" in str(session_context).lower():
            return "therapeutic_agent"
        
        # If user needs professional resources
        if "therapist" in str(session_context).lower() or "support group" in str(session_context).lower():
            return "resource_coordinator_agent"
    
    # Default to ending after wellness coaching
    return "__end__"
