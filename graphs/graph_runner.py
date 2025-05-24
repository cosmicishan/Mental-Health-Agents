from typing import Dict, Any, Optional
import uuid
from datetime import datetime
from graphs.main_graph import build_mental_health_graph
from graphs.graph_config import load_graph_config
from states.enhanced_state import EnhancedState

class MentalHealthGraphRunner:
    """Runner class for the mental health support graph."""
    
    def __init__(self):
        self.config = load_graph_config()
        self.graph = build_mental_health_graph()
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    def start_session(self, user_id: Optional[str] = None) -> str:
        """Start a new mental health support session."""
        session_id = str(uuid.uuid4())
        
        initial_state = {
            "messages": [],
            "user_profile": {"user_id": user_id} if user_id else None,
            "session_context": {
                "session_id": session_id,
                "start_time": datetime.now().isoformat(),
                "agent_switches": 0
            },
            "crisis_level": None,
            "safety_plan_active": False,
            "current_agent": None,
            "agent_history": [],
            "intervention_plan": None,
            "tools_used": [],
            "session_id": session_id,
            "session_start_time": datetime.now().isoformat(),
            "continue_session": True,
            "session_outcomes": None,
            "follow_up_needed": False,
            "referrals_made": []
        }
        
        self.active_sessions[session_id] = initial_state
        return session_id
    
    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """Process a user message through the graph."""
        
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        state = self.active_sessions[session_id]
        
        # Add user message to state
        user_msg = {"role": "user", "content": user_message}
        state["messages"].append(user_msg)
        
        # Check for session end requests
        if self._is_end_request(user_message):
            return self._end_session(session_id)
        
        # Process through graph
        try:

            result = self.graph.invoke(state)
            self.active_sessions[session_id] = result
            
            # Extract assistant response
            assistant_response = ""
            if len(result["messages"]) > 0:
                last_message = result["messages"][-1]
                assistant_response = last_message.content
            
            return {
                "session_id": session_id,
                "response": assistant_response,
                "current_agent": result.get("current_agent"),
                "crisis_level": result.get("crisis_level"),
                "session_active": result.get("continue_session", True),
                "tools_used": result.get("tools_used", []),
                "intervention_plan": result.get("intervention_plan")
            }
            
        except Exception as e:
            # Error handling

            print(e)

            error_response = {
                "session_id": session_id,
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again or contact emergency services if you're in crisis.",
                "error": str(e),
                "session_active": True
            }
            return error_response
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """Manually end a session."""
        return self._end_session(session_id)
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of session activities."""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        state = self.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "start_time": state.get("session_start_time"),
            "agents_used": [entry.get("agent") for entry in state.get("agent_history", [])],
            "crisis_level": state.get("crisis_level"),
            "interventions": state.get("intervention_plan"),
            "tools_used": state.get("tools_used", []),
            "referrals_made": state.get("referrals_made", []),
            "message_count": len(state.get("messages", [])),
            "session_outcomes": state.get("session_outcomes")
        }
    
    def _is_end_request(self, message: str) -> bool:
        """Check if user wants to end the session."""
        end_phrases = ["goodbye", "bye", "end session", "quit", "exit", "stop", "thank you, that's all"]
        return any(phrase in message.lower() for phrase in end_phrases)
    
    def _end_session(self, session_id: str) -> Dict[str, Any]:
        """End session and provide summary."""
        
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        state = self.active_sessions[session_id]
        
        # Create session summary
        summary = self.get_session_summary(session_id)
        
        # Generate closing message
        closing_message = self._generate_closing_message(state)
        
        # Clean up session
        del self.active_sessions[session_id]
        
        return {
            "session_id": session_id,
            "response": closing_message,
            "session_active": False,
            "session_summary": summary
        }
    
    def _generate_closing_message(self, state: EnhancedState) -> str:
        """Generate appropriate closing message based on session."""
        
        crisis_level = state.get("crisis_level", 0)
        interventions = state.get("intervention_plan", {})
        
        if crisis_level and crisis_level >= 6:
            return """Thank you for reaching out today. Your safety is important. Please remember:
            
🚨 Crisis Resources (available 24/7):
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- Emergency: 911

You've shown courage by seeking help. Please continue to reach out to professional support."""
        
        elif interventions:
            return """Thank you for our session today. You've taken important steps toward your mental health and wellbeing.

Remember:
- Practice the techniques we discussed
- Reach out to the resources we identified
- Be patient and kind with yourself
- Professional help is always available

Take care, and remember that seeking support is a sign of strength."""
        
        else:
            return """Thank you for connecting with our mental health support system. Remember that help is always available when you need it.

If you need immediate support:
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741

Take care of yourself, and don't hesitate to reach out again."""
