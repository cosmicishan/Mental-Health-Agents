import os
from dotenv import load_dotenv

def load_config():
    """Load environment variables and configuration."""
    load_dotenv()
    
    # Validate required API keys
    required_keys = ["GROQ_API_KEY", "SERPER_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        raise ValueError(f"Missing required environment variables: {missing_keys}")
