"""
Configuration module for Gemini API integration.
Loads environment variables and provides configuration settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for Gemini API settings."""
    
    # Gemini API key (required)
    # Get your API key from: https://makersuite.google.com/app/apikey
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Request timeout in seconds
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required. Please add it to your .env file.")
        return True
