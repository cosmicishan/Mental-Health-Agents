from langgraph.types import Command
from typing import Literal
from states.enhanced_state import EnhancedState
from tools.crisis_tools import find_crisis_resources, create_safety_plan

import os
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
from langchain_groq import ChatGroq

# Initialize LLM
llm = ChatGroq(
    model_name=os.getenv("MODEL_NAME"),
    api_key=os.getenv("GROQ_API_KEY")
)

def crisis_agent(state: EnhancedState) -> Command[Literal["coordinator_agent", "__end__"]]:
    """Specialized crisis intervention and safety planning agent."""

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
    
    crisis_tools = [find_crisis_resources, create_safety_plan]
    crisis_llm = llm.bind_tools(crisis_tools)
    
    messages = [
        {"role": "system",
         "content": """You are a crisis intervention specialist with experience.
                      Your immediate priorities are:
                      1. SAFETY FIRST - Assess immediate risk and provide crisis resources
                      2. De-escalation and emotional stabilization
                      3. Safety planning and coping strategies
                      4. Connection to professional crisis services
                      
                      You are trained in:
                      - Crisis de-escalation techniques
                      - Suicide risk assessment
                      - Safety planning protocols
                      - Grounding and stabilization techniques
                      
                      Always be calm, direct, and supportive. Encourage professional help.
                      If someone is in immediate danger, provide crisis hotline numbers immediately."""}
    ] + conversation_messages
    
    response = crisis_llm.invoke(messages)
    
    # Handle crisis tool execution
    if response.tool_calls:
        tool_results = []
        for tool_call in response.tool_calls:
            if tool_call["name"] == "find_crisis_resources":
                result = find_crisis_resources.invoke({
                    "location": tool_call["args"].get("location", "general")
                })
                tool_results.append(f"🚨 CRISIS RESOURCES: {result}")

            elif tool_call["name"] == "create_safety_plan":
                result = create_safety_plan.invoke({
                    "triggers": tool_call["args"].get("triggers", "general stress")
                })
                tool_results.append(f"🛡️ SAFETY PLAN: {result}")

        
        if tool_results:
            final_messages = messages + [response] + [
                {
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tool_call["id"]
                }
                for tool_result, tool_call in zip(tool_results, response.tool_calls)
            ]
            final_response = llm.invoke(final_messages)
            
            return Command(
                update={
                    "messages": [final_response],
                    "current_agent": "crisis",
                    "intervention_plan": {
                        "type": "crisis_intervention",
                        "resources_provided": True,
                        "safety_plan_created": "create_safety_plan" in [tc["name"] for tc in response.tool_calls]
                    }
                },
                goto="__end__"
            )
    
    return Command(
        update={
            "messages": [response],
            "current_agent": "crisis"
        },
        goto="__end__"
    )
