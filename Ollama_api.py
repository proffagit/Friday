import requests
from typing import List, Optional, Dict

class OllamaAPI:
    """Handles communication with a local Ollama API instance"""

    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.response = None

    def generate(self, 
                 prompt: str = None,
                 model: str = "mistral-small",
                 system: str = None,
                 history: List[Dict[str, str]] = None) -> Optional[str]:
        
        # Build context from ALL conversation history
        # The oldest messages first and the newest messages last.
        # Expected history format:
        # history = [
        #     {"role": "user", "content": "Hello, how are you?"},
        #     {"role": "assistant", "content": "I'm doing well, thank you!"},
        #     {"role": "user", "content": "What's the weather like?"}
        # ]
        
        # The context string will be formatted as:
        # user: Hello, how are you?
        # assistant: I'm doing well, thank you!
        # user: What's the weather like?
        
        conversation_context = ""
        if history:
            for msg in history: 
                # Extract role (user/assistant) and message content
                role = msg['role']
                content = msg['content']
                # Build context string with role-based formatting
                conversation_context += f"{role}: {content}\n"

        # Add current prompt to the full context
        full_prompt = f"{conversation_context}{prompt}" if conversation_context else prompt

        # Build payload with proper context handling
        payload = {
            "model": model,
            "prompt": full_prompt,
            "stream": False,
        }
        
        # Only add system if provided
        if system:
            payload["system"] = system
            
        endpoint = f"{self.base_url.rstrip('/')}/api/generate"

        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code != 200:
                print(f"Error response from Ollama: {response.text}")
            response.raise_for_status()
            # Store response in class attribute
            self.response = response.json().get('response')
            return self.response
        except requests.exceptions.RequestException as e:
            print(f"Error generating response: {e}")
            # Set response to error message
            self.response = f"Sorry, I encountered an error: {str(e)}"
            return None




    
