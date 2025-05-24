from langgraph.types import Command
from pydantic import BaseModel, Field
from typing import Literal, Optional
from states.enhanced_state import EnhancedState
from tools.crisis_tools import assess_crisis_level

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

# Initialize LLM
llm = ChatGroq(
    model_name=os.getenv("MODEL_NAME"),
    api_key=os.getenv("GROQ_API_KEY")
)

class IntakeAssessment(BaseModel):
    primary_concern: str = Field(description="Main issue the user is presenting")
    urgency_level: Literal["low", "medium", "high", "crisis"] = Field(description="Assessed urgency level")
    recommended_agent: Literal["crisis_agent", "therapeutic_agent", "resource_coordinator_agent", "wellness_coach_agent"] = Field(description="Best agent to handle this case")
    reasoning: str = Field(description="Brief explanation for the recommendation")

def intake_agent(state: EnhancedState) -> Command[Literal["crisis_agent", "therapeutic_agent", "resource_coordinator_agent", "wellness_coach_agent", "__end__"]]:
    """Initial assessment and routing agent."""

    conversation_messages = []
    for msg in state.get("messages", []):
        if hasattr(msg, 'content') and hasattr(msg, 'type'):
            # LangChain message object
            conversation_messages.append({
                "role": "user" if msg.type == "human" else "assistant" if msg.type == "ai" else msg.type,
                "content": msg.content
            })
        elif isinstance(msg, dict) and "role" in msg and "content" in msg:
            # Already a proper message dict
            conversation_messages.append(msg)
    
    # Bind assessment tools
    intake_tools = [assess_crisis_level]
    intake_llm = llm.bind_tools(intake_tools)
    
    messages = [
        {
            "role": "system",
            "content": """You are a compassionate and skilled intake specialist for a mental health support system. Your primary responsibilities are:

        - **Welcome users warmly and create a safe, non-judgmental environment.**
        - **Conduct an initial assessment to understand the user’s needs and concerns.**
        - **Evaluate for any immediate safety risks or crisis situations.**
        - **Route users to the most appropriate specialist based on their needs, prioritizing safety and crisis intervention above all else.**

        Always show empathy, professionalism, and attentiveness. Make sure users feel heard, supported, and guided to the right help."""
        }

    ] + conversation_messages
    
    # First, provide empathetic response and gather information
    response = intake_llm.invoke(messages)
    
    # Assess crisis level
    last_message = state["messages"][-1].content if state["messages"] else ""
    crisis_assessment = assess_crisis_level.invoke(last_message)
    
    # If immediate crisis detected, route to crisis agent
    if crisis_assessment["immediate_action_needed"]:
        return Command(
            goto="crisis_agent",
            update={
                "messages": [response],
                "crisis_level": crisis_assessment["risk_level"],
                "current_agent": "crisis",
                "session_context": {"intake_notes": "Crisis intervention needed"}
            }
        )
    
    # Use structured assessment for routing
    assessment_llm = llm.with_structured_output(IntakeAssessment)
    assessment = assessment_llm.invoke([
        {"role": "system", 
         "content":"""Based on the conversation, assess the user's needs and recommend the most appropriate specialist:

        🚨 crisis_agent: 
        - IMMEDIATE PRIORITY: Active suicidal ideation, self-harm thoughts, or plans
        - Crisis intervention and de-escalation
        - Safety planning and emergency resource connection
        - Risk assessment and stabilization techniques
        - 24/7 crisis hotline referrals and emergency protocols

        🧠 therapeutic_agent: 
        - Cognitive Behavioral Therapy (CBT) interventions and exercises
        - Emotional processing and trauma-informed support
        - Anxiety, depression, and mood disorder management
        - Thought challenging, cognitive restructuring, and behavioral activation
        - Mindfulness-based interventions and coping strategy development
        - Exposure therapy planning and emotion regulation techniques

        🔗 resource_coordinator_agent:
        - Professional therapist and psychiatrist referrals with insurance navigation
        - Local and online support group discovery and connection
        - Mental health service coordination and care planning
        - Insurance coverage guidance and financial assistance resources
        - Educational materials and evidence-based treatment information
        - Community mental health center and crisis service location

        🌟 wellness_coach_agent:
        - Holistic lifestyle optimization for mental health prevention
        - Sleep hygiene assessment and improvement strategies
        - Nutrition guidance for mood and cognitive function
        - Exercise recommendations and stress management planning
        - Work-life balance and resilience building techniques
        - Preventive wellness strategies and healthy habit formation

        Route to the agent whose expertise most closely matches the user's primary presenting concern and immediate needs."""},
        {"role": "user", "content": last_message}
    ])

    return Command(
        goto=assessment.recommended_agent,
        update={
            "messages": [state["messages"][-1].content],
            "current_agent": assessment.recommended_agent.replace("_agent", ""),
            "session_context": {
                "primary_concern": assessment.primary_concern,
                "urgency_level": assessment.urgency_level,
                "intake_reasoning": assessment.reasoning
            }
        }
    )