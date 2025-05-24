from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from typing import Dict, Any
import json

@tool
def generate_cbt_exercise(issue_type: str, difficulty_level: str = "beginner", specific_trigger: str = None) -> Dict[str, Any]:
    """Search for and generate personalized CBT exercises based on current evidence-based practices."""
    
    search_wrapper = GoogleSerperAPIWrapper()
    
    # Construct targeted search queries
    base_query = f"CBT cognitive behavioral therapy exercises for {issue_type} {difficulty_level} level"
    
    if specific_trigger:
        specific_query = f"CBT exercises for {issue_type} triggered by {specific_trigger} evidence based"
    else:
        specific_query = f"evidence based CBT techniques {issue_type} therapy worksheets"
    
    # Search for current exercises
    general_results = search_wrapper.run(base_query)
    specific_results = search_wrapper.run(specific_query)
    
    # Search for professional worksheets and resources
    worksheet_query = f"CBT worksheet {issue_type} therapist resources PDF download"
    worksheet_results = search_wrapper.run(worksheet_query)
    
    # Search for step-by-step instructions
    instructions_query = f"how to do CBT {issue_type} exercise step by step instructions"
    instructions_results = search_wrapper.run(instructions_query)
    
    # Search for effectiveness and research
    research_query = f"CBT {issue_type} effectiveness research studies evidence"
    research_results = search_wrapper.run(research_query)
    
    return {
        "exercise_type": f"Evidence-Based CBT for {issue_type.title()}",
        "difficulty_level": difficulty_level,
        "current_exercises": general_results,
        "specific_techniques": specific_results,
        "professional_worksheets": worksheet_results,
        "step_by_step_instructions": instructions_results,
        "research_backing": research_results,
        "customization_note": f"Customized for {specific_trigger}" if specific_trigger else "General approach",
        "recommendation": "Review the search results above to find the most current and evidence-based exercises. Look for resources from licensed therapists, psychology organizations, or peer-reviewed sources.",
        "next_steps": [
            "Choose an exercise that resonates with your current situation",
            "Download any worksheets from reputable sources",
            "Follow the step-by-step instructions carefully",
            "Track your progress over time",
            "Consider working with a licensed therapist for personalized guidance"
        ]
    }

@tool
def mindfulness_exercise_generator(duration: int, focus_area: str, experience_level: str = "beginner", current_mood: str = "neutral") -> Dict[str, Any]:
    """Search for current, evidence-based mindfulness exercises tailored to specific needs and duration."""
    
    search_wrapper = GoogleSerperAPIWrapper()
    
    # Search for duration-specific exercises
    duration_query = f"mindfulness meditation {duration} minutes {focus_area} guided exercise"
    duration_results = search_wrapper.run(duration_query)
    
    # Search for experience-level appropriate exercises
    level_query = f"{experience_level} mindfulness {focus_area} meditation instructions"
    level_results = search_wrapper.run(level_query)
    
    # Search for mood-specific adaptations
    mood_query = f"mindfulness for {current_mood} mood {focus_area} meditation techniques"
    mood_results = search_wrapper.run(mood_query)
    
    # Search for guided audio/video resources
    guided_query = f"free guided mindfulness meditation {focus_area} {duration} minutes audio video"
    guided_results = search_wrapper.run(guided_query)
    
    # Search for scientific backing
    science_query = f"mindfulness {focus_area} research benefits neuroscience studies"
    science_results = search_wrapper.run(science_query)
    
    # Search for apps and digital resources
    apps_query = f"best mindfulness apps {focus_area} meditation {experience_level}"
    apps_results = search_wrapper.run(apps_query)
    
    return {
        "exercise_focus": f"Mindfulness for {focus_area.title()}",
        "duration": f"{duration} minutes",
        "experience_level": experience_level,
        "current_mood_consideration": current_mood,
        "duration_specific_exercises": duration_results,
        "level_appropriate_techniques": level_results,
        "mood_adapted_practices": mood_results,
        "guided_resources": guided_results,
        "scientific_evidence": science_results,
        "recommended_apps": apps_results,
        "personalized_recommendation": f"Based on your {experience_level} level and focus on {focus_area}, review the search results above for the most current and effective practices.",
        "implementation_guide": [
            "Choose a quiet space where you won't be interrupted",
            "Set a timer for your desired duration",
            "Follow one of the guided exercises from the search results",
            "Start with shorter sessions if you're a beginner",
            "Track your experience and adjust based on what works best"
        ],
        "progress_tracking": "Use the apps mentioned in the search results to track your meditation progress and build consistency"
    }
