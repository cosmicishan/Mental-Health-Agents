from typing_extensions import TypedDict
from typing import Annotated, Optional, List, Dict, Any
from langgraph.graph.message import add_messages

class EnhancedState(TypedDict):
    """Enhanced state for comprehensive mental health support system."""
    
    # Core conversation state
    messages: Annotated[List[Dict[str, Any]], add_messages]
    
    # User profile and context
    user_profile: Optional[Dict[str, Any]]
    session_context: Optional[Dict[str, Any]]
    
    # Crisis and safety tracking
    crisis_level: Optional[int]  # 1-10 scale
    safety_plan_active: Optional[bool]
    
    # Agent coordination
    current_agent: Optional[str]
    agent_history: Optional[List[Dict[str, Any]]]
    
    # Intervention tracking
    intervention_plan: Optional[Dict[str, Any]]
    tools_used: Optional[List[str]]
    
    # Session management
    session_id: Optional[str]
    session_start_time: Optional[str]
    continue_session: Optional[bool]
    
    # Outcomes and follow-up
    session_outcomes: Optional[Dict[str, Any]]
    follow_up_needed: Optional[bool]
    referrals_made: Optional[List[str]]
