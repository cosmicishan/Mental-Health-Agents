from langgraph.types import Command
from langchain.chat_models import init_chat_model
from typing import Literal
from states.enhanced_state import EnhancedState
from tools.search_tools import (
    find_support_groups,
    find_therapists,
    search_mental_health_resources
)
from tools.resource_tools import (
    insurance_navigator,
    mental_health_education,
    medication_information
)

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

# Initialize LLM
llm = ChatGroq(
    model_name=os.getenv("MODEL_NAME"),
    api_key=os.getenv("GROQ_API_KEY")
)


def resource_coordinator_agent(state: EnhancedState) -> Command[Literal["coordinator_agent", "__end__"]]:
    """Connects users with external resources and support systems."""

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
    
    resource_tools = [
        find_support_groups,
        find_therapists,
        search_mental_health_resources,
        insurance_navigator,
        mental_health_education,
        medication_information
    ]
    resource_llm = llm.bind_tools(resource_tools)
    
    messages = [
        {"role": "system",
         "content": """You are a Clinical Social Worker and Resource Coordinator with expertise in:
                      - Mental health service navigation
                      - Insurance and healthcare systems
                      - Community resource identification
                      - Support group facilitation
                      
                      Your mission is to:
                      1. Connect people with appropriate professional help
                      2. Navigate insurance and financial barriers
                      3. Find local and online support communities
                      4. Provide educational resources
                      5. Ensure continuity of care
                      
                      You are knowledgeable about:
                      - Different types of therapy and therapists
                      - Insurance coverage for mental health
                      - Support groups and peer communities
                      - Educational resources and self-help materials
                      - Crisis services and emergency resources
                      
                      Always ask about location, insurance, and specific preferences to provide the most relevant resources."""}
    ] + conversation_messages
    
    response = resource_llm.invoke(messages)

    # Handle resource search execution
    if response.tool_calls:
        tool_results = []
        for tool_call in response.tool_calls:

            if tool_call["name"] == "find_support_groups":
                result = find_support_groups.invoke({
                    "location": tool_call["args"]["location"],
                    "issue_type": tool_call["args"]["issue_type"],
                    "format_preference": tool_call["args"].get("format_preference", "both")
                })
                tool_results.append(f"👥 SUPPORT GROUPS: {result}")
                
            elif tool_call["name"] == "find_therapists":
                result = find_therapists.invoke({
                    "location": tool_call["args"]["location"],
                    "specialization": tool_call["args"]["specialization"],
                    "insurance": tool_call["args"].get("insurance", "any")
                })
                tool_results.append(f"👨‍⚕️ THERAPISTS: {result}")
                
            elif tool_call["name"] == "search_mental_health_resources":
                result = search_mental_health_resources.invoke({
                    "topic": tool_call["args"]["topic"]
                })
                tool_results.append(f"📚 RESOURCES: {result}")
                
            elif tool_call["name"] == "insurance_navigator":
                print("Inside tool call")
                print("Insurance type:", tool_call["args"]["insurance_type"])
                result = insurance_navigator.invoke({
                    "insurance_type": tool_call["args"]["insurance_type"],
                    "service_needed": tool_call["args"]["service_needed"]
                })
                print("Result:", result)
                tool_results.append(f"💳 INSURANCE INFO: {result}")
                
            elif tool_call["name"] == "mental_health_education":
                result = mental_health_education.invoke({
                    "topic": tool_call["args"]["topic"],
                    "reading_level": tool_call["args"].get("reading_level", "general")
                })
                tool_results.append(f"🎓 EDUCATION: {result}")
                
            elif tool_call["name"] == "medication_information":
                result = medication_information.invoke({
                    "medication_name": tool_call["args"]["medication_name"]
                })
                tool_results.append(f"💊 MEDICATION INFO: {result}")

        
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
                    "current_agent": "resource_coordinator",
                    "intervention_plan": {
                        "type": "resource_coordination",
                        "resources_found": len(tool_results),
                        "resource_types": [tc["name"] for tc in response.tool_calls]
                    }
                },
                goto="__end__"
            )
        
    print("Resource Coordinator Agent Run Successfully.")
    print("Here's the response: ", response)
    
    return Command(
        update={
            "messages": [response],
            "current_agent": "resource_coordinator"
        }
    )