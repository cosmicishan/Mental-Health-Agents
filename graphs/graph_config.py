from typing import Dict, Any
import os

class GraphConfig:
    """Configuration settings for the mental health support graph."""
    
    def __init__(self):
        self.llm_config = {
            "model": "anthropic:claude-3-5-sonnet-latest",
            "temperature": 0.1,
            "max_tokens": 1000
        }
        
        self.crisis_config = {
            "high_risk_threshold": 8,
            "immediate_intervention_threshold": 9,
            "safety_plan_threshold": 6
        }
        
        self.session_config = {
            "max_session_length": 60,  # minutes
            "max_agent_switches": 5,
            "auto_end_threshold": 3  # consecutive end requests
        }
        
        self.routing_config = {
            "default_agent": "intake_agent",
            "crisis_override": True,
            "allow_agent_loops": True,
            "max_loops": 3
        }
    
    def get_config(self) -> Dict[str, Any]:
        """Get complete configuration dictionary."""
        return {
            "llm": self.llm_config,
            "crisis": self.crisis_config,
            "session": self.session_config,
            "routing": self.routing_config
        }

def load_graph_config() -> GraphConfig:
    """Load and return graph configuration."""
    config = GraphConfig()
    
    # Override with environment variables if available
    if os.getenv("LLM_TEMPERATURE"):
        config.llm_config["temperature"] = float(os.getenv("LLM_TEMPERATURE"))
    
    if os.getenv("CRISIS_THRESHOLD"):
        config.crisis_config["high_risk_threshold"] = int(os.getenv("CRISIS_THRESHOLD"))
    
    return config
