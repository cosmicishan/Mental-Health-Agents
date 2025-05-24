from langgraph.types import Command
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import Literal
from states.enhanced_state import EnhancedState

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

# Initialize LLM
llm = ChatGroq(
    model_name=os.getenv("MODEL_NAME"),
    api_key=os.getenv("GROQ_API_KEY")
)

class AgentRouter(BaseModel):
    recommended_agent: Literal[
        "crisis_agent", 
        "therapeutic_agent", 
        "resource_coordinator_agent", 
        "wellness_coach_agent",
        "intake_agent",
        "__end__"
    ] = Field(description="Most appropriate agent for this user need")
    reasoning: str = Field(description="Brief explanation for routing decision")
    urgency_level: Literal["low", "medium", "high", "crisis"] = Field(description="Assessed urgency level")

def coordinator_agent(state: EnhancedState) -> Command[Literal["crisis_agent", "therapeutic_agent", "resource_coordinator_agent", "wellness_coach_agent", "intake_agent", "__end__"]]:
    """Master coordinator that intelligently routes between specialized agents."""
    
    last_message = state["messages"][-1].content if state["messages"] else ""
    crisis_level = state.get("crisis_level", 0)
    current_agent = state.get("current_agent")
    
    # Crisis override - always prioritize safety
    if crisis_level and crisis_level > 7:
        return Command(
            goto="crisis_agent",
            update={"current_agent": "crisis"}
        )
    
    # Intelligent routing based on conversation analysis
    routing_llm = llm.with_structured_output(AgentRouter)
    
    conversation_context = ""
    if len(state["messages"]) > 1:
        conversation_context = f"Previous conversation context: {state['messages'][-3:]}"
    
    session_context = state.get("session_context", {})
    context_info = f"Session context: {session_context}" if session_context else ""
    
    router_response = routing_llm.invoke([
        {"role": "system", 
         "content": f"""You are the master coordinator for a mental health support system. 
                       Analyze the user's message and route to the most appropriate specialist:
                       
                       🚨 crisis_agent: Immediate safety concerns, self-harm, suicide ideation, crisis situations
                       🧠 therapeutic_agent: Emotional processing, therapy needs, coping strategies, trauma, anxiety, depression
                       🔗 resource_coordinator_agent: Need for professional help, therapists, support groups, insurance questions
                       🌟 wellness_coach_agent: Lifestyle factors, prevention, wellness planning, stress management, sleep, nutrition
                       📋 intake_agent: Initial assessment, unclear needs, general questions
                       🏁 __end__: User wants to end the conversation or says goodbye
                       
                       Current context:
                       - Previous agent: {current_agent}
                       - Crisis level: {crisis_level}
                       {context_info}
                       {conversation_context}
                       
                       Consider:
                       1. Safety first - any mention of self-harm goes to crisis_agent
                       2. Continuity - if user is engaged with current agent and making progress, consider staying
                       3. Specialization - route to the agent best equipped for the specific need
                       4. User intent - respect if they want to end or switch topics"""},
        {"role": "user", "content": last_message}
    ])
    
    next_agent = router_response.recommended_agent
    
    # Update state with routing information
    updated_state = {
        "current_agent": next_agent.replace("_agent", "") if next_agent != "__end__" else "ended",
        "agent_history": state.get("agent_history", []) + [
            {
                "agent": next_agent,
                "reasoning": router_response.reasoning,
                "urgency": router_response.urgency_level,
                "timestamp": "current"
            }
        ]
    }
    
    # Add crisis level if assessed as high urgency
    if router_response.urgency_level == "crisis":
        updated_state["crisis_level"] = 9
    elif router_response.urgency_level == "high":
        updated_state["crisis_level"] = 6
    
    return Command(
        goto=next_agent,
        update=updated_state
    )
