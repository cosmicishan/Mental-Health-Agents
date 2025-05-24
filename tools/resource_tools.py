from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from typing import Dict, Any

# Initialize search wrapper
search_wrapper = GoogleSerperAPIWrapper()

@tool
def insurance_navigator(insurance_type: str, service_needed: str) -> str:
    """Help navigate insurance coverage for mental health services."""
    
    query = f"{insurance_type} insurance coverage {service_needed} mental health benefits therapy counseling"
    
    try:
        results = search_wrapper.run(query)
        return f"Insurance information for {insurance_type} covering {service_needed}:\n{results}"
    except Exception as e:
        return f"""General insurance guidance for mental health services:
        
        Under the Mental Health Parity Act, insurance must cover mental health services similarly to physical health.
        
        Common covered services:
        - Outpatient therapy/counseling
        - Psychiatric medication management
        - Intensive outpatient programs
        - Inpatient psychiatric care
        
        To verify coverage:
        1. Call the number on your insurance card
        2. Ask about mental health benefits and copays
        3. Request a list of in-network providers
        4. Understand your deductible and out-of-pocket costs
        
        If you need help understanding your benefits, contact your insurance company directly."""

@tool
def mental_health_education(topic: str, reading_level: str = "general") -> str:
    """Provide educational content about mental health topics."""
    
    query = f"mental health education {topic} {reading_level} evidence-based information patient education"
    
    try:
        results = search_wrapper.run(query)
        return f"Educational resources about {topic} (reading level: {reading_level}):\n{results}"
    except Exception as e:
        return f"""Educational information about {topic}:
        
        For reliable mental health information, visit:
        - National Institute of Mental Health (NIMH.nih.gov)
        - National Alliance on Mental Illness (NAMI.org)
        - MentalHealth.gov
        - American Psychological Association (APA.org)
        - Substance Abuse and Mental Health Services Administration (SAMHSA.gov)
        
        These sources provide evidence-based information about mental health conditions, treatments, and resources."""

@tool
def medication_information(medication_name: str) -> str:
    """Provide general information about psychiatric medications."""
    
    query = f"{medication_name} psychiatric medication information side effects patient education FDA approved"
    
    try:
        results = search_wrapper.run(query)
        return f"General information about {medication_name}:\n{results}\n\n⚠️ IMPORTANT: This is general information only. Always consult with your prescribing physician about medications, side effects, and any concerns."
    except Exception as e:
        return f"""General medication information for {medication_name}:
        
        ⚠️ IMPORTANT DISCLAIMER: This is general information only. Always consult with your prescribing physician about medications.
        
        For reliable medication information:
        - Consult your prescribing doctor or psychiatrist
        - Speak with your pharmacist
        - Visit FDA.gov for official drug information
        - Use MedlinePlus.gov for patient-friendly information
        
        Never start, stop, or change medications without consulting your healthcare provider."""

@tool
def community_resources(location: str, resource_type: str = "general") -> str:
    """Find local community mental health resources and services."""
    
    query = f"community mental health resources {location} {resource_type} local services support"
    
    try:
        results = search_wrapper.run(query)
        return f"Community mental health resources in {location}:\n{results}"
    except Exception as e:
        return f"""To find community mental health resources in {location}:
        
        1. Contact your local health department
        2. Call 211 (community resource helpline)
        3. Visit SAMHSA.gov treatment locator
        4. Check with local hospitals for mental health services
        5. Contact local NAMI chapter
        6. Search for community mental health centers
        7. Check with religious organizations for counseling services
        8. Look into employee assistance programs (EAP) if employed"""

@tool
def crisis_resource_locator(location: str, crisis_type: str = "general") -> str:
    """Locate specific crisis intervention resources and services."""
    
    query = f"crisis intervention resources {location} {crisis_type} emergency mental health mobile crisis team"
    
    try:
        results = search_wrapper.run(query)
        return f"Crisis intervention resources in {location}:\n{results}"
    except Exception as e:
        return f"""Crisis resources for {location}:
        
        🚨 IMMEDIATE CRISIS:
        - Call 911 for immediate danger
        - National Suicide Prevention Lifeline: 988
        - Crisis Text Line: Text HOME to 741741
        
        LOCAL RESOURCES:
        - Contact your local emergency room
        - Call your local police (ask for crisis intervention team)
        - Search for "mobile crisis team {location}"
        - Contact local community mental health center
        - Call 211 for local crisis resources"""
