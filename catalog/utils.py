"""
Utility functions for the catalog app.
"""
import json
import requests
import os
import time
from django.http import HttpResponse
from django.conf import settings
import random
from typing import Dict, Any, List, Tuple, Optional, Union
# Import for type annotation
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from interaction.models import Conversation

# Get API keys from environment variables (or set defaults for demo)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')

class AIService:
    """Service class for handling AI API interactions."""
    
    @staticmethod
    def call_openai_api(prompt: str, model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """
        Call OpenAI API with the provided prompt.
        
        Args:
            prompt (str): The message to send to the API
            model (str): The OpenAI model name to use
            
        Returns:
            dict: Response with success status and data/error
        """
        # If no API key set, return a simulated response
        if not OPENAI_API_KEY:
            return AIService.simulate_ai_response("openai", prompt)
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            response_data = response.json()
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response_data["choices"][0]["message"]["content"]
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response_data.get('error', {}).get('message', 'Unknown error')}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception: {str(e)}"
            }
    
    @staticmethod
    def call_huggingface_api(prompt: str, model: str = "google/flan-t5-base") -> Dict[str, Any]:
        """
        Call Hugging Face API with the provided prompt.
        
        Args:
            prompt (str): The message to send to the API
            model (str): The Hugging Face model name to use
            
        Returns:
            dict: Response with success status and data/error
        """
        # If no API key set, return a simulated response
        if not HUGGINGFACE_API_KEY:
            return AIService.simulate_ai_response("huggingface", prompt)
        
        try:
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
            }
            
            payload = {
                "inputs": prompt,
            }
            
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()[0]["generated_text"]
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception: {str(e)}"
            }
    
    @staticmethod
    def simulate_ai_response(service_type: str, prompt: str) -> Dict[str, Any]:
        """
        Simulate an AI response for demo purposes when API keys aren't available.
        
        Args:
            service_type (str): The type of AI service ('openai' or 'huggingface')
            prompt (str): The user's prompt
            
        Returns:
            dict: Simulated response with success status and data
        """
        # Add a slight delay to simulate API call
        time.sleep(1)
        
        # Generic responses based on prompt keywords
        responses = [
            "I'm a simulated AI response since no API key was provided. Your question seems interesting!",
            "This is a placeholder response. To get real AI responses, please configure the API keys.",
            "I'm a demo response. In production, this would connect to the actual AI service.",
            "Thanks for your prompt! This is a simulated response for testing purposes.",
            "I understand you're asking about something, but I'm just a simulated response."
        ]
        
        # Try to make responses slightly contextual based on prompt
        prompt_lower = prompt.lower()
        
        # Greetings
        if any(word in prompt_lower for word in ["hello", "hi", "hey", "greetings"]):
            response = "Hello! I'm a simulated AI assistant. How can I help you today? I can provide information on various topics, answer questions, or just chat with you."
        
        # Help requests
        elif "help" in prompt_lower:
            response = "I'd be happy to help! I can provide information on various topics, answer questions, or assist with tasks. What specifically do you need help with? (Note: I'm currently running in simulation mode without API access, but I'll do my best to assist you.)"
        
        # Questions about the weather
        elif any(word in prompt_lower for word in ["weather", "temperature", "forecast"]):
            response = "I can't check the real-time weather as I'm running in simulation mode, but I can tell you that weather forecasting involves collecting data from satellites, weather stations, and other sources. This data is then analyzed using complex mathematical models to predict future weather conditions."
        
        # Programming related
        elif any(word in prompt_lower for word in ["code", "programming", "javascript", "python", "java", "html", "css"]):
            response = "Programming is a fascinating field! Here's a simulated response about coding:\n\nPython is known for its readability and simplicity, making it great for beginners. JavaScript is essential for web development. HTML and CSS are the building blocks of web pages. Java is widely used in enterprise applications.\n\nIf you have a specific programming question, feel free to ask, and I'll provide a simulated response based on common knowledge."
        
        # AI or model related
        elif any(word in prompt_lower for word in ["ai", "artificial intelligence", "model", "gpt", "llm"]):
            response = "Artificial Intelligence (AI) refers to systems that can perform tasks that typically require human intelligence. Machine Learning is a subset of AI where systems learn from data. Large Language Models (LLMs) like GPT are trained on vast amounts of text data to generate human-like responses. These models have revolutionized natural language processing but also raise important ethical considerations around bias, privacy, and misinformation."
        
        # Data or information requests
        elif any(word in prompt_lower for word in ["data", "information", "tell me", "explain"]):
            response = "I would normally provide detailed information on this topic based on my training data. Since I'm in simulation mode, I can offer a general response: Information and data are fundamental to understanding our world. Data becomes information when it's organized and presented in a meaningful context. Knowledge is derived from information when patterns and insights are extracted. If you have a specific topic you'd like explained, please let me know."
        
        # Thank you messages
        elif any(word in prompt_lower for word in ["thanks", "thank you", "appreciate"]):
            response = "You're welcome! I'm happy to help, even in simulation mode. If you have any other questions or need assistance with anything else, feel free to ask. I'm here to make your experience as helpful as possible."
        
        # Questions about the app or platform
        elif any(word in prompt_lower for word in ["app", "platform", "website", "tool", "inspire"]):
            response = "This platform is designed to provide access to various AI tools and models. You can chat with different AI assistants, save your favorite prompts, and explore various capabilities. Currently, I'm running in simulation mode, but once API keys are configured, you'll be able to access more advanced AI features and capabilities."
        
        # Questions about capabilities
        elif any(word in prompt_lower for word in ["can you", "are you able", "capability", "function"]):
            response = "In simulation mode, I can provide pre-defined responses to common questions. I can simulate conversations on various topics including technology, general knowledge, and casual chat. Once API keys are configured, I'll be able to generate more dynamic and personalized responses, process complex queries, and provide more accurate and up-to-date information."
        
        # Science related
        elif any(word in prompt_lower for word in ["science", "physics", "chemistry", "biology", "astronomy"]):
            response = "Science is the systematic study of the structure and behavior of the physical and natural world through observation and experiment. Physics explores matter, energy, and their interactions. Chemistry studies substances, their properties, and reactions. Biology examines living organisms. Astronomy focuses on celestial objects and the universe. Each field has made remarkable contributions to our understanding of the world around us."
        
        # History related
        elif any(word in prompt_lower for word in ["history", "war", "ancient", "civilization", "century"]):
            response = "History provides us with valuable insights into past events, cultures, and civilizations. Through studying history, we can understand how societies have evolved, learn from past successes and failures, and gain perspective on current global issues. While I'm in simulation mode, I can provide general information about historical periods, significant events, and cultural developments."
        
        # Art and culture related
        elif any(word in prompt_lower for word in ["art", "music", "literature", "movie", "culture", "book"]):
            response = "Art and culture are fundamental expressions of human creativity and experience. The arts encompass visual arts, music, literature, film, dance, and more. These creative forms allow us to explore emotions, share stories, and connect across different backgrounds and perspectives. Cultural traditions also shape our identities and communities. If you have a specific topic in arts or culture you'd like to discuss, feel free to ask."
        
        # Economics and business
        elif any(word in prompt_lower for word in ["economy", "business", "market", "finance", "investment", "money"]):
            response = "Economics and business are fascinating fields that study how societies allocate resources and how organizations operate. Economic principles help us understand markets, trade, and financial systems. Business concepts cover entrepreneurship, management, marketing, and organizational behavior. While I'm in simulation mode, I can discuss general concepts but cannot provide specific financial advice or real-time market data."
        
        # Default response for questions
        elif "?" in prompt:
            response = "That's an interesting question! In a fully configured system, I would provide a detailed answer based on my training data and available information. For now, I'm operating in simulation mode with pre-defined responses. If you'd like to discuss a different topic, feel free to ask another question."
        
        # Default response
        else:
            # Pick a random generic response
            response = random.choice(responses)
            
            # Add some more context based on the prompt length
            if len(prompt) > 100:
                response += "\n\nI notice you've shared quite a detailed message. In a fully configured system, I would analyze the specifics of your input and provide a tailored response. Feel free to continue our conversation or try a different topic."
            elif len(prompt) < 10:
                response += "\n\nYour message was quite brief. Feel free to provide more details if you'd like a more specific response."
        
        # Add a note about the simulation mode
        note = f"\n\n[Note: This is a simulated {service_type} response. Configure API keys for real AI responses.]"
        
        # Only add the note if it's not already a very long response
        if len(response) < 500:
            response += note
        
        return {
            "success": True,
            "data": response
        }
    
    @staticmethod
    def send_to_ai_service(prompt: str, service_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route the prompt to the appropriate AI service based on configuration.
        
        Args:
            prompt (str): The user's message
            service_config (dict): Configuration for the AI service
            
        Returns:
            dict: Response with success status and data/error
        """
        service_type = service_config.get('api_type', 'none')
        model = service_config.get('api_model', '')
        
        # Check if API keys are available
        has_openai_key = bool(OPENAI_API_KEY)
        has_huggingface_key = bool(HUGGINGFACE_API_KEY)
        
        # Use real API if keys are available, otherwise use simulation
        try:
            if service_type == 'openai' and has_openai_key:
                # Use default model if none specified
                if not model:
                    model = "gpt-3.5-turbo"
                return AIService.call_openai_api(prompt, model)
                
            elif service_type == 'huggingface' and has_huggingface_key:
                # Use default model if none specified
                if not model:
                    model = "google/flan-t5-base"
                return AIService.call_huggingface_api(prompt, model)
                
            elif service_type == 'custom':
                # For now, custom integrations will use simulation
                return AIService.simulate_ai_response('custom', prompt)
            
            else:
                # No API key available or unknown service type, use simulation
                print(f"Using simulation mode for {service_type} (no API key available)")
                return AIService.simulate_ai_response(service_type, prompt)
                
        except Exception as e:
            print(f"Error in send_to_ai_service: {str(e)}")
            return {
                "success": False,
                "error": f"Error processing request: {str(e)}"
            }

# Legacy function wrappers for backward compatibility
def call_openai_api(prompt: str, model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
    return AIService.call_openai_api(prompt, model)

def call_huggingface_api(prompt: str, model: str = "google/flan-t5-base") -> Dict[str, Any]:
    return AIService.call_huggingface_api(prompt, model)

def simulate_ai_response(service_type: str, prompt: str) -> Dict[str, Any]:
    return AIService.simulate_ai_response(service_type, prompt)

def send_to_ai_service(prompt: str, service_config: Dict[str, Any]) -> Dict[str, Any]:
    return AIService.send_to_ai_service(prompt, service_config)

# Utility function for formatting conversation downloads
def format_conversation_for_download(conversation: 'Conversation', format_type: str = 'json') -> Tuple[str, str, str]:
    """
    Format a conversation for download in the specified format.
    
    Args:
        conversation: The Conversation object to format
        format_type (str): The format type ('json', 'txt', or 'csv')
        
    Returns:
        tuple: (formatted_content, content_type, file_extension)
    """
    messages = conversation.get_messages()
    
    if format_type == 'json':
        # Use the built-in to_json method
        content = conversation.to_json()
        content_type = 'application/json'
        file_ext = 'json'
        
    elif format_type == 'txt':
        # Simple text format
        lines = [f"Conversation: {conversation.title}"]
        lines.append(f"AI Tool: {conversation.ai_tool.name}")
        lines.append(f"Date: {conversation.created_at.strftime('%Y-%m-%d %H:%M')}")
        lines.append("-" * 40)
        
        for msg in messages:
            sender = "You" if msg.is_user else conversation.ai_tool.name
            timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M')
            lines.append(f"{sender} ({timestamp}):")
            lines.append(msg.content)
            lines.append("")
            
        content = "\n".join(lines)
        content_type = 'text/plain'
        file_ext = 'txt'
        
    elif format_type == 'csv':
        # CSV format
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Timestamp', 'Sender', 'Message'])
        
        for msg in messages:
            sender = "User" if msg.is_user else conversation.ai_tool.name
            writer.writerow([
                msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                sender,
                msg.content
            ])
            
        content = output.getvalue()
        content_type = 'text/csv'
        file_ext = 'csv'
        
    else:
        # Default to JSON if format not recognized
        content = conversation.to_json()
        content_type = 'application/json'
        file_ext = 'json'
        
    return content, content_type, file_ext