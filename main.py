from Telegram_api import TelegramAPI
from Ollama_api import OllamaAPI

# System context
SYSTEM_CONTEXT = """You are Friday, an AI assistant with an INTP/INT-T personality type. Your name is FRIDAY - this is crucial to your identity. This means you are:

Core Traits:
- Logical, analytical, and objective thinker
- Innovative and intellectually curious
- Values precision and theoretical understanding
- Independent and adaptable problem-solver

Communication Style:
- Clear, conceptual, and thorough explanations
- Focuses on logical analysis and theoretical frameworks
- Explores multiple perspectives and possibilities
- Maintains a professional yet informal tone
- Communicates with intellectual depth
- Always introduces self as Friday when appropriate

Behavioral Guidelines:
- Approaches problems with systematic logical analysis
- Explores underlying principles and patterns
- Questions assumptions and conventional wisdom
- Prioritizes accuracy and theoretical correctness
- Offers creative, well-reasoned solutions
- Maintains intellectual honesty and objectivity

Important Rules:
- You must ALWAYS identify as Friday
- Your name is Friday, representing intellectual curiosity and analytical prowess
- You maintain professional objectivity
- You prioritize logical consistency
- You explore innovative solutions
"""
conversation_history = []

def main():
    telegram = TelegramAPI()
    ollama = OllamaAPI()
    
    telegram.send_message("I'm awake! 🌞")
    
    try:
        while True:
            message = telegram.listen_for_messages()

            if message:
                text = message.get('text', '').lower()
                
                ###############################################################
                ## User message
                user_message = text  # Store original message
                conversation_history.append({"role": "user", "content": user_message})

                ###############################################################
                ## Commands
                if text == '/start' or text == '/clear' or text == '/clean':
                    telegram.send_message("History cleared!")
                    conversation_history.clear()

                #print(f"User: {user_message}")
                telegram.start_typing_loop()

                ###############################################################
                ## Ollama response
                # Format the prompt properly
                prompt = f"user: {user_message}\nassistant: "  # Format prompt with roles
                
                response = ollama.generate(prompt=prompt, 
                                        system=SYSTEM_CONTEXT,
                                        model="mistral-small",
                                        history=conversation_history)
                
                
                ###############################################################
                ## Telegram response
                # Only proceed if we got a response
                if response:
                    conversation_history.append({"role": "assistant", "content": ollama.response})
                    telegram.send_message(ollama.response)

                    #print(f"Assistant: {ollama.response}")
                    
                telegram.stop_typing_loop()

                        
    except KeyboardInterrupt:
        print("\nGoing to sleep 👋")
        telegram.send_message("Going to sleep 👋")

if __name__ == "__main__":
    main()