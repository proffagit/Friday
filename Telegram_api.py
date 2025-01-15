import os
from typing import Optional
import requests
from dotenv import load_dotenv
import threading
import time

class TelegramAPI:
    # Handles Telegram bot API interactions
    
    def __init__(self):
        # Initialize API with credentials
        load_dotenv()
        
        # Set up API access
        self.api_key = os.getenv('TELEGRAM_API_KEY')
        self.chat_id = os.getenv('TELEGRAM_ID')
        self.base_url = f"https://api.telegram.org/bot{self.api_key}"
        
        # Initialize typing action thread control
        self._typing_thread = None
        self._stop_typing = threading.Event()

    def send_message(self, message: str) -> Optional[dict]:
        # Send message to chat
        try:
            endpoint = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message
            }
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error sending message: {e}")
            return None

    def get_updates(self, offset: Optional[int] = None) -> Optional[list]:
        # Get new messages
        try:
            endpoint = f"{self.base_url}/getUpdates"
            params = {
                "timeout": 1,  # Fast response time
                "allowed_updates": ["message"]
            }
            if offset:
                params["offset"] = offset
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json().get('result', [])
        except Exception as e:
            print(f"Error getting updates: {e}")
            return None

    def listen_for_messages(self) -> Optional[dict]:
        # Get latest message and mark as read

        try:
            updates = self.get_updates()
            if updates:
                last_update = updates[-1]
                self.get_updates(offset=last_update['update_id'] + 1)
                return last_update.get('message')
            return None
        except Exception as e:
            print(f"Error listening for messages: {e}")
            return None

    def send_typing_action(self) -> Optional[dict]:
        # Show typing indicator
        try:
            endpoint = f"{self.base_url}/sendChatAction"
            payload = {
                "chat_id": self.chat_id,
                "action": "typing"
            }
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error sending typing action: {e}")
            return None

    def start_typing_loop(self):
        """Starts a background thread that shows typing indicator every 4 seconds"""
        # Stop any existing typing thread
        self.stop_typing_loop()
        
        # Create and start new typing thread
        self._stop_typing.clear()
        self._typing_thread = threading.Thread(target=self._typing_loop)
        self._typing_thread.daemon = True  # Thread will stop when main program exits
        self._typing_thread.start()

    def stop_typing_loop(self):
        """Stops the typing indicator thread if running"""
        if self._typing_thread and self._typing_thread.is_alive():
            self._stop_typing.set()
            self._typing_thread.join()
            self._typing_thread = None

    def _typing_loop(self):
        """Internal method that runs in thread to show typing indicator"""
        while not self._stop_typing.is_set():
            self.send_typing_action()
            time.sleep(4)


