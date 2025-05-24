from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
import os

# Initialize search wrapper
search_wrapper = GoogleSerperAPIWrapper()

@tool
def find_support_groups(location: str, issue_type: str, format_preference: str = "both") -> str:
    """Find local and online support groups for specific mental health issues."""
    
    format_query = ""
    if format_preference == "online":
        format_query = "online virtual"
    elif format_preference == "in_person":
        format_query = "local in-person"
    else:
        format_query = "online virtual local in-person"
    
    query = f"{format_query} support groups {issue_type} {location} mental health community peer support"
    
    try:
        results = search_wrapper.run(query)
        return f"Support groups for {issue_type} in {location} ({format_preference} format):\n{results}"
    except Exception as e:
        return f"Unable to search for support groups at this time. Please try contacting local mental health organizations or searching online for '{issue_type} support groups {location}'."

@tool
def find_therapists(location: str, specialization: str, insurance: str = "any") -> str:
    """Find licensed therapists and mental health professionals in the area."""
    
    insurance_query = f"{insurance} insurance" if insurance != "any" else "insurance accepted"
    query = f"licensed therapists {specialization} {location} {insurance_query} mental health counselors psychologists"
    
    try:
        results = search_wrapper.run(query)
        return f"Licensed therapists specializing in {specialization} in {location}:\n{results}"
    except Exception as e:
        return f"Unable to search for therapists at this time. Consider contacting your insurance provider or visiting Psychology Today's therapist directory."

@tool
def search_mental_health_resources(topic: str) -> str:
    """Search for comprehensive mental health resources, educational materials, and support information."""
    
    query = f"mental health resources {topic} educational materials support information evidence-based treatment"
    
    try:
        results = search_wrapper.run(query)
        return f"Mental health resources and information about {topic}:\n{results}"
    except Exception as e:
        return f"Unable to search for resources at this time. Consider visiting reputable sites like NAMI.org, MentalHealth.gov, or NIMH.nih.gov for {topic} information."

@tool
def search_crisis_hotlines(location: str = "national") -> str:
    """Search for crisis hotlines and emergency mental health services."""
    
    if location == "national":
        query = "national crisis hotlines mental health emergency suicide prevention 24/7"
    else:
        query = f"crisis hotlines {location} local emergency mental health services suicide prevention"
    
    try:
        results = search_wrapper.run(query)
        return f"Crisis hotlines and emergency services ({location}):\n{results}"
    except Exception as e:
        return """National Crisis Resources:
        - National Suicide Prevention Lifeline: 988
        - Crisis Text Line: Text HOME to 741741
        - SAMHSA National Helpline: 1-800-662-4357
        - If in immediate danger, call 911"""

@tool
def search_medication_information(medication_name: str) -> str:
    """Search for general information about psychiatric medications."""
    
    query = f"{medication_name} psychiatric medication information side effects patient education FDA approved"
    
    try:
        results = search_wrapper.run(query)
        return f"General information about {medication_name}:\n{results}\n\nIMPORTANT: Always consult with your prescribing physician about medications."
    except Exception as e:
        return f"Unable to search for medication information. Please consult your prescribing physician, pharmacist, or visit FDA.gov for information about {medication_name}."

@tool
def search_treatment_options(condition: str, location: str = "general") -> str:
    """Search for evidence-based treatment options for specific mental health conditions."""
    
    if location == "general":
        query = f"evidence-based treatment options {condition} therapy approaches mental health treatment guidelines"
    else:
        query = f"treatment options {condition} {location} mental health services therapy evidence-based"
    
    try:
        results = search_wrapper.run(query)
        return f"Treatment options for {condition}:\n{results}"
    except Exception as e:
        return f"Unable to search for treatment options. Consider consulting with a mental health professional about evidence-based treatments for {condition}."
