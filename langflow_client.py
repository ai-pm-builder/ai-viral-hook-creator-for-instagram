"""
Langflow API client for interacting with Langflow flows.
Handles API requests, response parsing, and error handling.
"""

import requests
import json
from typing import Dict, Any, Optional
from config import Config


class LangflowClient:
    """Client for interacting with Langflow API."""
    
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize Langflow client.
        
        Args:
            api_url: Langflow API endpoint URL (defaults to Config.LANGFLOW_API_URL)
            api_key: API key for authentication (defaults to Config.LANGFLOW_API_KEY)
        """
        self.api_url = api_url or Config.LANGFLOW_API_URL
        self.api_key = api_key or Config.LANGFLOW_API_KEY
        self.timeout = Config.REQUEST_TIMEOUT
        
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def generate_hooks(self, video_description: str, flow_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate viral hooks for Instagram food content.
        
        Args:
            video_description: User's description of the video they want to create
            flow_id: Optional Langflow flow ID (defaults to Config.LANGFLOW_FLOW_ID)
            
        Returns:
            Dictionary containing the response from Langflow API
            
        Raises:
            requests.exceptions.RequestException: If API request fails
            ValueError: If response is invalid
        """
        flow_id = flow_id or Config.LANGFLOW_FLOW_ID
        
        # Prepare request payload
        payload = {
            "input_value": video_description,
            "output_type": "chat",
            "input_type": "chat"
        }
        
        # Add flow_id if provided
        if flow_id:
            payload["flow_id"] = flow_id
        
        try:
            # Make API request
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            # Raise exception for bad status codes
            response.raise_for_status()
            
            # Parse JSON response
            result = response.json()
            
            return result
            
        except requests.exceptions.Timeout:
            raise requests.exceptions.RequestException(
                f"Request to Langflow API timed out after {self.timeout} seconds"
            )
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.RequestException(
                f"Could not connect to Langflow API at {self.api_url}. "
                "Please check if the API is running and the URL is correct."
            )
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.RequestException(
                f"Langflow API returned error: {e.response.status_code} - {e.response.text}"
            )
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from Langflow API")
    
    def parse_hooks_response(self, response: Dict[str, Any]) -> list:
        """
        Parse Langflow API response to extract hook recommendations.
        
        Args:
            response: Raw response from Langflow API
            
        Returns:
            List of hook strings
        """
        hooks = []
        
        # Try to extract hooks from different possible response structures
        if isinstance(response, dict):
            # Check for common response fields
            if "outputs" in response:
                outputs = response["outputs"]
                if isinstance(outputs, list) and len(outputs) > 0:
                    output = outputs[0]
                    if isinstance(output, dict) and "outputs" in output:
                        data = output["outputs"]
                        if isinstance(data, list) and len(data) > 0:
                            result = data[0]
                            if isinstance(result, dict) and "results" in result:
                                results = result["results"]
                                if isinstance(results, dict) and "message" in results:
                                    message = results["message"]
                                    if isinstance(message, dict) and "content" in message:
                                        content = message["content"]
                                        hooks = self._extract_hooks_from_content(content)
            
            # Alternative: check for direct content field
            if not hooks and "content" in response:
                hooks = self._extract_hooks_from_content(response["content"])
            
            # Alternative: check for message field
            if not hooks and "message" in response:
                message = response["message"]
                if isinstance(message, dict) and "content" in message:
                    hooks = self._extract_hooks_from_content(message["content"])
                elif isinstance(message, str):
                    hooks = self._extract_hooks_from_content(message)
            
            # Alternative: check for text field
            if not hooks and "text" in response:
                hooks = self._extract_hooks_from_content(response["text"])
        
        # If response is a string, treat it as a single hook
        elif isinstance(response, str):
            hooks = self._extract_hooks_from_content(response)
        
        # If no hooks found, return the response as a single hook
        if not hooks:
            hooks = [str(response)]
        
        return hooks
    
    def _extract_hooks_from_content(self, content: str) -> list:
        """
        Extract individual hooks from content string.
        
        Args:
            content: Content string that may contain multiple hooks
            
        Returns:
            List of hook strings
        """
        if not content:
            return []
        
        hooks = []
        
        # Try to split by common delimiters
        # Check for numbered list (1., 2., etc.)
        import re
        numbered_pattern = r'\d+[\.\)]\s*(.+?)(?=\d+[\.\)]|$)'
        matches = re.findall(numbered_pattern, content, re.DOTALL)
        if matches:
            hooks = [match.strip() for match in matches if match.strip()]
        
        # Check for bullet points (-, *, •)
        if not hooks:
            bullet_pattern = r'[-*•]\s*(.+?)(?=[-*•]|$)'
            matches = re.findall(bullet_pattern, content, re.DOTALL)
            if matches:
                hooks = [match.strip() for match in matches if match.strip()]
        
        # Check for line breaks (each line as a hook)
        if not hooks:
            lines = content.split('\n')
            hooks = [line.strip() for line in lines if line.strip() and len(line.strip()) > 10]
        
        # If still no hooks, return the whole content as a single hook
        if not hooks:
            hooks = [content.strip()]
        
        return hooks
