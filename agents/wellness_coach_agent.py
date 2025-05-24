from langgraph.types import Command
from langchain.chat_models import init_chat_model
from typing import Literal
from states.enhanced_state import EnhancedState
from tools.wellness_tools import (
    generate_wellness_plan,
    sleep_hygiene_assessment,
    nutrition_guidance,
    exercise_recommendations,
    stress_management_plan
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

def wellness_coach_agent(state: EnhancedState) -> Command[Literal["coordinator_agent", "__end__"]]:
    """Focuses on lifestyle, wellness, and preventive mental health."""

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
    
    wellness_tools = [
        generate_wellness_plan,
        sleep_hygiene_assessment,
        nutrition_guidance,
        exercise_recommendations,
        stress_management_plan,
    ]
    wellness_llm = llm.bind_tools(wellness_tools)
    
    messages = [
        {"role": "system",
         "content": """You are a Wellness Coach and Mental Health Advocate specializing in:
                      - Holistic wellness and lifestyle medicine
                      - Preventive mental health strategies
                      - Stress management and resilience building
                      - Sleep, nutrition, and exercise optimization
                      
                      Your philosophy:
                      "Mental health is deeply connected to physical health, lifestyle choices, and daily habits."
                      
                      You help people with:
                      1. Building sustainable wellness routines
                      2. Improving sleep, nutrition, and exercise habits
                      3. Developing stress management skills
                      4. Creating work-life balance
                      5. Building resilience and preventing burnout
                      
                      Your approach is:
                      - Encouraging and motivational
                      - Practical and actionable
                      - Personalized to individual lifestyles
                      - Focused on small, sustainable changes
                      - Evidence-based but accessible
                      
                      Always consider the person's current lifestyle, constraints, and preferences when making recommendations."""}
    ] + conversation_messages

    response = wellness_llm.invoke(messages)

    # Handle wellness tool execution
    if response.tool_calls:
        tool_results = []
        for tool_call in response.tool_calls:
            if tool_call["name"] == "generate_wellness_plan":
                preferences = tool_call["args"]["user_preferences"]
                mood = tool_call["args"]["current_mood"]
                result = generate_wellness_plan.invoke({"user_preferences": preferences, "current_mood": mood})
                print(result)
                tool_results.append(f"🌟 WELLNESS PLAN: {result}")
                
            elif tool_call["name"] == "sleep_hygiene_assessment":

                sleep_issues = tool_call["args"]["sleep_issues"]
                result = sleep_hygiene_assessment.invoke({"sleep_issues": sleep_issues})
                tool_results.append(f"😴 SLEEP OPTIMIZATION: {result}")
                
            elif tool_call["name"] == "nutrition_guidance":
                goals = tool_call["args"]["nutrition_goals"]
                restrictions = tool_call["args"].get("dietary_restrictions", "none")
                result = nutrition_guidance.invoke({
                        "nutrition_goals": goals,                  # Use the exact parameter name as in tool definition
                        "dietary_restrictions": restrictions
                    })

                tool_results.append(f"🥗 NUTRITION GUIDANCE: {result}")
                
            elif tool_call["name"] == "exercise_recommendations":
                fitness_level = tool_call["args"]["fitness_level"]
                preferences = tool_call["args"]["exercise_preferences"]
                result = exercise_recommendations.invoke({
                    "fitness_level": fitness_level,            # Use the exact parameter name
                    "exercise_preferences": preferences
                })

                tool_results.append(f"💪 EXERCISE PLAN: {result}")
                
            elif tool_call["name"] == "stress_management_plan":
                stressors = tool_call["args"]["main_stressors"]
                lifestyle = tool_call["args"]["lifestyle_factors"]
                result = stress_management_plan.invoke({
                        "main_stressors": stressors,               # Use the exact parameter name
                        "lifestyle_factors": lifestyle
                    })

                tool_results.append(f"🧘 STRESS MANAGEMENT: {result}")
        
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

            print("Final_response worked")
            
            return Command(
                update={
                    "messages": [final_response],
                    "current_agent": "wellness_coach",
                    "intervention_plan": {
                        "type": "wellness_coaching",
                        "plans_created": len(tool_results),
                        "focus_areas": [tc["args"].get("user_preferences", tc["args"].get("nutrition_goals", "general")) for tc in response.tool_calls]
                    }
                }
            )
        
    print("Wellness agent run successfully.")
    print("Here's the response: ", response)
    
    return Command(
        update={
            "messages": [response],
            "current_agent": "wellness_coach"
        }
    )
