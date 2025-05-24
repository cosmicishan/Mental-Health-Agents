from langgraph.types import Command
from langchain.chat_models import init_chat_model
from typing import Literal
from states.enhanced_state import EnhancedState
from tools.therapeutical_tools import (
    generate_cbt_exercise, 
    mindfulness_exercise_generator
)
from tools.wellness_tools import generate_coping_strategies

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

# Initialize LLM
llm = ChatGroq(
    model_name=os.getenv("MODEL_NAME"),
    api_key=os.getenv("GROQ_API_KEY")
)

def therapeutic_agent(state: EnhancedState) -> Command[Literal["coordinator_agent", "__end__"]]:
    """CBT and therapeutic intervention specialist."""

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
    
    therapy_tools = [
        generate_cbt_exercise,
        mindfulness_exercise_generator,
        generate_coping_strategies
    ]
    therapy_llm = llm.bind_tools(therapy_tools)
    
    messages = [
        {"role": "system",
         "content": """You are a clinical psychologist specializing in:
                      - Cognitive Behavioral Therapy (CBT)
                      - Mindfulness-Based Interventions
                      - Emotion Regulation Techniques
                      - Trauma-Informed Care
                      
                      Your approach is:
                      1. Empathetic and non-judgmental
                      2. Evidence-based and practical
                      3. Collaborative and empowering
                      4. Focused on building coping skills
                      
                      You help users:
                      - Process emotions and thoughts
                      - Develop healthy coping strategies
                      - Challenge negative thought patterns
                      - Build emotional resilience
                      - Practice mindfulness and grounding
                      
                      Always validate feelings while providing practical tools and exercises."""}
    ] + conversation_messages
    
    response = therapy_llm.invoke(messages)
    
    # Handle therapeutic tool execution
    if response.tool_calls:
        tool_results = []
        for tool_call in response.tool_calls:
            if tool_call["name"] == "generate_cbt_exercise":
                result = generate_cbt_exercise.invoke({
                    "issue_type": tool_call["args"]["issue_type"],
                    "difficulty_level": tool_call["args"].get("difficulty_level", "beginner")
                })
                tool_results.append(f"🧠 CBT EXERCISE: {result}")

            elif tool_call["name"] == "mindfulness_exercise_generator":
                result = mindfulness_exercise_generator.invoke({
                    "duration": tool_call["args"]["duration"],
                    "focus_area": tool_call["args"]["focus_area"]
                })
                tool_results.append(f"🧘‍♀️ MINDFULNESS: {result}")

            elif tool_call["name"] == "generate_coping_strategies":
                result = generate_coping_strategies.invoke({
                    "situation": tool_call["args"]["situation"]
                })
                tool_results.append(f"🛠️ COPING STRATEGIES: {result}")

        
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
                    "current_agent": "therapeutic",
                    "intervention_plan": {
                        "type": "therapeutic_intervention",
                        "exercises_provided": len(tool_results),
                        "focus_areas": [tc["args"].get("issue_type", tc["args"].get("focus_area", "general")) for tc in response.tool_calls]
                    }
                },
                goto="__end__"
            )
    
    return Command(
        update={
            "messages": [response],
            "current_agent": "therapeutic"
        },
        goto="__end__"
    )
