from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from typing import Dict, Any, List
import json

# Initialize search wrapper
search_wrapper = GoogleSerperAPIWrapper()

@tool
def assess_crisis_level(user_message: str) -> Dict[str, Any]:
    """Analyze message for crisis indicators and return comprehensive risk assessment."""
    
    # Crisis keywords with severity weights
    high_risk_keywords = ["suicide", "kill myself", "end it all", "want to die", "better off dead"]
    medium_risk_keywords = ["self-harm", "hurt myself", "cut myself", "can't go on", "no point"]
    low_risk_keywords = ["hopeless", "worthless", "give up", "tired of living"]
    
    message_lower = user_message.lower()
    
    high_risk_score = sum(2 for keyword in high_risk_keywords if keyword in message_lower)
    medium_risk_score = sum(1.5 for keyword in medium_risk_keywords if keyword in message_lower)
    low_risk_score = sum(1 for keyword in low_risk_keywords if keyword in message_lower)
    
    total_risk_score = high_risk_score + medium_risk_score + low_risk_score
    risk_level = min(int(total_risk_score * 2), 10)
    
    return {
        "risk_level": risk_level,
        "immediate_action_needed": risk_level >= 6,
        "high_risk_indicators": [kw for kw in high_risk_keywords if kw in message_lower],
        "medium_risk_indicators": [kw for kw in medium_risk_keywords if kw in message_lower],
        "recommended_action": "immediate_crisis_intervention" if risk_level >= 8 else "crisis_support" if risk_level >= 6 else "standard_support",
        "safety_planning_needed": risk_level >= 4
    }

@tool
def find_crisis_resources(location: str = "general", crisis_type: str = "mental_health") -> str:
    """Find immediate crisis intervention resources including hotlines and emergency services."""
    
    # Always include national resources
    national_resources = """
    🚨 IMMEDIATE CRISIS RESOURCES:
    
    National Suicide Prevention Lifeline: 988 or 1-800-273-8255
    Crisis Text Line: Text HOME to 741741
    National Domestic Violence Hotline: 1-800-799-7233
    SAMHSA National Helpline: 1-800-662-4357
    Veterans Crisis Line: 1-800-273-8255 (Press 1)
    
    🆘 If you are in immediate danger, call 911 or go to your nearest emergency room.
    """
    
    try:
        if location != "general":
            query = f"crisis mental health hotlines emergency resources {location} local immediate help"
            local_results = search_wrapper.run(query)
            return f"{national_resources}\n\n🏥 LOCAL RESOURCES for {location}:\n{local_results}"
        else:
            return national_resources
    except Exception as e:
        return national_resources + f"\n\nNote: Unable to search for local resources at this time."

@tool
def create_safety_plan(triggers: str, coping_strategies: str = "") -> Dict[str, Any]:
    """Create a personalized safety plan for crisis situations."""
    
    safety_plan = {
        "warning_signs": f"Personal triggers identified: {triggers}",
        "coping_strategies": [
            "Deep breathing exercises (4-7-8 technique)",
            "Grounding techniques (5-4-3-2-1 method)",
            "Call a trusted friend or family member",
            "Go to a safe, public place",
            "Use crisis hotline numbers"
        ],
        "support_contacts": [
            "National Suicide Prevention Lifeline: 988",
            "Crisis Text Line: Text HOME to 741741",
            "Trusted friend/family member (add personal contact)",
            "Mental health professional (add personal contact)"
        ],
        "environment_safety": [
            "Remove or secure potential means of self-harm",
            "Stay with trusted person when feeling unsafe",
            "Avoid alcohol and substances",
            "Create a calm, safe space at home"
        ],
        "professional_contacts": [
            "Primary therapist/counselor",
            "Psychiatrist (if applicable)", 
            "Primary care physician",
            "Local emergency room",
            "Crisis mobile team (if available)"
        ],
        "reasons_for_living": [
            "Family and friends who care about you",
            "Future goals and dreams",
            "Pets or responsibilities",
            "Things you enjoy doing",
            "People who depend on you"
        ]
    }
    
    if coping_strategies:
        safety_plan["personal_coping_strategies"] = coping_strategies.split(",")
    
    return safety_plan

@tool
def generate_grounding_exercise(technique: str = "5-4-3-2-1") -> Dict[str, Any]:
    """Generate immediate grounding exercises for crisis de-escalation."""
    
    exercises = {
        "5-4-3-2-1": {
            "name": "5-4-3-2-1 Sensory Grounding",
            "instructions": [
                "5 things you can SEE around you",
                "4 things you can TOUCH",
                "3 things you can HEAR", 
                "2 things you can SMELL",
                "1 thing you can TASTE"
            ],
            "duration": "3-5 minutes",
            "purpose": "Brings attention to present moment and away from distressing thoughts"
        },
        "box_breathing": {
            "name": "Box Breathing Technique",
            "instructions": [
                "Breathe in for 4 counts",
                "Hold breath for 4 counts",
                "Breathe out for 4 counts", 
                "Hold empty for 4 counts",
                "Repeat 4-8 times"
            ],
            "duration": "2-4 minutes",
            "purpose": "Activates parasympathetic nervous system to reduce anxiety"
        },
        "progressive_muscle": {
            "name": "Progressive Muscle Relaxation",
            "instructions": [
                "Tense feet muscles for 5 seconds, then release",
                "Tense leg muscles for 5 seconds, then release",
                "Tense stomach muscles for 5 seconds, then release",
                "Tense arm muscles for 5 seconds, then release",
                "Tense face muscles for 5 seconds, then release",
                "Notice the contrast between tension and relaxation"
            ],
            "duration": "5-10 minutes",
            "purpose": "Releases physical tension and promotes relaxation"
        }
    }
    
    return exercises.get(technique, exercises["5-4-3-2-1"])

@tool
def emergency_contact_finder(location: str, service_type: str = "mobile_crisis") -> str:
    """Find local emergency mental health services and mobile crisis teams."""
    
    query = f"{service_type} team {location} emergency mental health services local"
    
    try:
        results = search_wrapper.run(query)
        return f"Emergency mental health services in {location}:\n{results}"
    except Exception as e:
        return f"Unable to search for emergency services. Please call 911 or go to your nearest emergency room for immediate help."
