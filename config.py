"""
Configuration module for Langflow API integration.
Loads environment variables and provides configuration settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for Langflow API settings."""
    
    # Langflow API endpoint URL
    LANGFLOW_API_URL = os.getenv(
        "LANGFLOW_API_URL", 
        "http://localhost:7860/api/v1/run"
    )
    
    # Langflow API key (optional, for authentication)
    LANGFLOW_API_KEY = os.getenv("LANGFLOW_API_KEY", "")
    
    # Gemini API key (required for Langflow workflow)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Langflow Flow ID (optional, if using specific flow)
    LANGFLOW_FLOW_ID = os.getenv("LANGFLOW_FLOW_ID", "")
    
    # Request timeout in seconds
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.LANGFLOW_API_URL:
            raise ValueError("LANGFLOW_API_URL is required")
        return True
